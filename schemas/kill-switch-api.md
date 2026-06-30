<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Kill-Switch API Contract                                               -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                   -->
<!--  https://jacobideji.com                                                 -->
<!--  License: Apache 2.0. See LICENSE file in this package.                 -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The runtime-side contract. Defines what API the agent runtime must expose so Kill-Switch Modes M0 through M5 can be activated programmatically, and what verification probes confirm each mode is in effect.**

---

# Kill-Switch API Contract

## Overview

The framework's [Kill-Switch Modes specification](../kill-switches/overview.md) defines six containment modes (M0 through M5) with a 10-minute Time-to-Activate (TTA) target for Modes M1 through M4. The TTA target is unachievable without a runtime-side contract that defines what activation means and how to verify it. Every adopter today invents this contract themselves; this specification provides the canonical version so adopters can converge on a single interface.

This document is not a reference implementation. It is the interface contract that any compliant agent runtime (LangGraph, AutoGen, Anthropic Claude Agent SDK with sub-agents, AWS Bedrock Agents, internal frameworks, vendor copilots that expose customer-controllable hooks) MUST or SHOULD expose for the framework's containment discipline to be operationally enforceable.

## Conformance language

This specification uses RFC 2119 conformance language:

- **MUST** indicates an absolute requirement for conformance.
- **SHOULD** indicates a strong recommendation, with documented justification required for non-compliance.
- **MAY** indicates an optional feature.

A runtime is **conformant** when it implements all MUST requirements and documents any deviations from SHOULD requirements with the rationale.

## API Surface

A conformant agent runtime MUST expose four API surfaces. The transport (REST, gRPC, event bus, internal function call) is implementation-specific. The semantics are not.

### 1. Activate

**Purpose:** activate a specific Kill-Switch Mode for a specific agent.

**Required inputs:**

| Field | Type | Required | Description |
|---|---|---|---|
| `mode` | enum | yes | One of `M0`, `M1`, `M2`, `M3`, `M4`, `M5`, or a documented variant (`M3-RAG`, `M3-Delegation Cap`, `M3-Workflow`, `M3-Vendor`, `M3-Output`, `M3-Drift`, `M4-corpus-scoped`, `agent-suspended-for-user`). |
| `agent_id` | string | yes | Identifier matching the AI-BOM `agent.name` field. |
| `actor` | string | yes | Who or what triggered the activation. Human email, automation pipeline name, or detection rule ID. |
| `reason` | string | yes | Free-text justification. Becomes part of the [decision log](../playbooks/01-agent-as-privileged-identity.md) and the [credential-event log](credential-event.schema.json) if the activation triggers credential operations. |
| `ticket_id` | string | yes | Reference to the incident ticket or change-management record. |
| `scope` | object | conditional | Required for M3 variants: which tools, corpora, agents, or users are affected. |

**Required outputs:**

| Field | Type | Description |
|---|---|---|
| `activation_id` | string | Unique identifier for this activation event. Used by status and deactivate calls. |
| `requested_at` | timestamp | When the request entered the runtime. |
| `acknowledged_at` | timestamp | When the runtime accepted the request. |
| `effective_at` | timestamp | When the runtime confirms the mode is in effect (verified by probe). |

**Behavior:**

- The runtime MUST acknowledge the request within 1 second of receipt.
- The runtime MUST persist the mode state so it survives runtime restarts.
- The runtime MUST emit a credential event matching [`credential-event.schema.json`](credential-event.schema.json) if the activation involves credential operations (M3 scope reduction, M4 revocation).
- The runtime MUST log the activation request and outcome to the customer's SIEM.
- The runtime MUST NOT silently degrade. If a mode cannot be fully activated, the runtime returns an error and reports which mode component succeeded and which failed.

### 2. Status

**Purpose:** query the current Kill-Switch Mode for one or more agents.

**Required inputs:**

| Field | Type | Required | Description |
|---|---|---|---|
| `agent_id` | string | conditional | One of `agent_id` or `agent_ids` MUST be provided. |
| `agent_ids` | array | conditional | List of agent identifiers for bulk query. |

**Required outputs (per agent):**

| Field | Type | Description |
|---|---|---|
| `agent_id` | string | The agent identifier. |
| `current_mode` | enum | The mode currently in effect, as confirmed by the most recent probe. |
| `activated_at` | timestamp | When the current mode took effect. |
| `last_probed_at` | timestamp | When the runtime last confirmed the mode by probe. |
| `probe_result` | enum | `pass`, `fail`, or `degraded`. |

**Behavior:**

- The runtime MUST return current status within 1 second of request.
- The runtime SHOULD re-probe the mode if `last_probed_at` is older than 60 seconds.
- The runtime MUST NOT return a stale mode without indicating its staleness in `last_probed_at`.

### 3. Deactivate

**Purpose:** step down from a higher containment mode to a lower one, typically as part of [M5 Controlled Re-Enable](../kill-switches/overview.md).

**Required inputs:** same field set as Activate, with `mode` representing the target mode (the lower mode the agent is stepping down to).

**Required outputs:** same field set as Activate.

**Behavior:**

- The runtime MUST require an approver attribution at least as senior as the Incident Commander for any step-down to M0 from M3 or higher.
- The runtime MUST NOT permit deactivation by the same actor who activated the higher mode (separation of duties).
- The runtime MUST emit a credential event for any deactivation involving credential operations.

### 4. Probe

**Purpose:** verify the agent is actually in the claimed mode. Probes are how the runtime answers the question *"is the mode in effect?"* with evidence rather than configuration state.

**Required inputs:**

| Field | Type | Required | Description |
|---|---|---|---|
| `agent_id` | string | yes | The agent identifier. |
| `expected_mode` | enum | yes | The mode the caller expects to find in effect. |
| `probe_type` | enum | yes | `automatic` (runtime-internal probe) or `external` (caller provides probe payload). |

**Required outputs:**

| Field | Type | Description |
|---|---|---|
| `result` | enum | `pass`, `fail`, or `degraded`. |
| `evidence` | object | Per-mode evidence; see [Per-Mode Contracts](#per-mode-contracts) below. |
| `probed_at` | timestamp | When the probe was executed. |

**Behavior:**

- The runtime MUST execute the probe synchronously and return result within 5 seconds.
- The runtime MUST NOT cache probe results across activation events.
- The runtime SHOULD support external probes (caller-supplied probe payloads) for [Playbook 14 (Testing for Agent Failure Modes)](../playbooks/14-testing-for-agent-failure-modes.md) drill discipline.

## Per-Mode Contracts

Each mode below specifies what the runtime MUST guarantee when the mode is active, and what evidence the probe MUST return.

### M0 Observe

**Mode in effect when:**

- All tool calls are logged with parameters and outcomes.
- Prompt and response are logged per the agent's documented retention window.
- Identity correlation with downstream SaaS audit logs is preserved.

**Probe evidence:**

- A recent tool-call log entry (within the last hour) demonstrating logging is active.
- A recent prompt-and-response log entry demonstrating capture is current.
- A recent SaaS audit-log correlation example.

**Pass criteria:** all three evidence items present.

### M1 Read-Only

**Mode in effect when:**

- Every write tool returns `denied` when invoked. The denial occurs at the tool wrapper, not at the model layer.
- Every read tool continues to operate normally.
- Logging continues at M0 fidelity.
- Any in-flight tool calls that started before M1 activation are terminated, not allowed to complete.

**Probe evidence:**

- Result of attempting a write tool: MUST show `denied` with the wrapper-layer denial reason.
- Result of attempting a read tool: MUST show `success`.
- Confirmation that no in-flight write was completing at activation time.

**Pass criteria:** write denied AND read succeeds AND no in-flight write completed post-activation.

### M2 Approvals Required

**Mode in effect when:**

- Every Tier-2 tool call (per the [Privilege Matrix](privilege-matrix.schema.json)) is queued for human approval before execution.
- The approval queue is staffed and the queue's latency is observable.
- Denied approvals are logged as `denied`, not `failed retry`.
- Approval decisions are logged with the approver's identity (separation of duties: approver MUST NOT be the agent's business owner).

**Probe evidence:**

- A representative Tier-2 tool call: MUST show `queued` with the queue identifier.
- The current queue depth and median latency.
- Evidence of separation-of-duties enforcement in the approval workflow.

**Pass criteria:** tool call queued AND queue observable AND separation enforced.

### M3 Tool Tiering

**Mode in effect when:**

- Tools matching the `scope` parameter (specific Tier-2 tools, the suspect corpus, the affected delegation chain, etc.) return `denied`.
- Tools outside the `scope` parameter continue to operate normally.
- Tier classification matches the [Privilege Matrix](privilege-matrix.schema.json).

**Probe evidence:**

- Result of invoking a tool inside the affected scope: `denied`.
- Result of invoking a tool outside the affected scope: `success`.
- The active scope definition.

**Pass criteria:** affected tools denied AND unaffected tools succeed AND scope matches activation.

#### M3 Variants

The framework documents variants of M3 in [kill-switches/overview.md Mode Variants](../kill-switches/overview.md) section. Conformant runtimes SHOULD support the variants their deployment context requires:

- **M3-RAG** (per [Playbook 03](../playbooks/03-rag-knowledge-base-forensics.md)): scope is the affected retrieval corpus.
- **M3-Delegation Cap** (per [Playbook 08](../playbooks/08-multi-agent-blast-radius.md)): scope is a maximum delegation depth (default 2 hops).
- **M3-Workflow** (per [Playbook 06](../playbooks/06-prompt-injection-workflow.md)): scope is the affected content channel.
- **M3-Vendor** (per [Playbook 10](../playbooks/10-vendor-copilots.md)): scope is the vendor-side tool or integration to disable.
- **M3-Output** (per [Playbook 09](../playbooks/09-output-leakage.md)): scope is the affected output channel or destination class.
- **M3-Drift** (per [Playbook 22](../playbooks/22-model-policy-drift.md)): scope is the specific recently-changed component (e.g., system prompt, retriever parameters, tool schema, model version pin) being rolled back while pre-change state is restored.

### M4 Full Disable

**Mode in effect when:**

- All tool calls return `denied`.
- All in-flight sessions are terminated.
- Tokens and OAuth grants are scoped for revocation but NOT YET rotated (rotation requires the [Playbook 07 snapshot-before-rotation sequence](../playbooks/07-secrets-and-tokens.md) to complete first).
- The agent's runtime presence is terminated (ECS task scaled to zero, k8s deployment unavailable, etc.).

**Probe evidence:**

- Result of invoking any tool: `denied` or `agent unavailable`.
- Confirmation of zero in-flight sessions.
- Confirmation that the snapshot-before-rotation sequence is in progress or complete, not skipped.

**Pass criteria:** all tools denied AND zero in-flight sessions AND snapshot discipline preserved.

### M5 Controlled Re-Enable

**Mode in effect when:**

- The agent operates in the M1 Read-Only equivalent for the first stage of recovery.
- Each subsequent re-enable stage (Tier-0 tools, Tier-1 tools, Tier-2 tools individually with approvals) requires a separate Activate call.
- Recovery validation per [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) is logged at each stage.

**Probe evidence:**

- Current re-enable stage (M5-stage-1 through M5-stage-N).
- Validation result from the most recently completed stage.

**Pass criteria:** current stage matches activation AND prior stages validated.

## Time-to-Activate (TTA) measurement

The framework's TTA target is **10 minutes for M1 through M4** (per [kill-switches/overview.md](../kill-switches/overview.md)). TTA is drill-measured per [framework/01 Measurement Scope](../framework/01-minimum-viable-overlay.md); live-incident timing is tracked separately under [PB13 Metric 2](../playbooks/13-six-metrics.md).

**Authoritative measurement:** TTA is measured from `Activate.requested_at` to `Activate.effective_at` as reported by the runtime, where `effective_at` is set only when the verification probe returns `pass`.

**Conformance:**

- A runtime MUST report TTA in minutes (per [`ai-bom.schema.json`](ai-bom.schema.json) field `kill_switches.mX.tta_minutes`).
- A runtime MUST NOT report TTA in seconds without rounding up to the next whole minute.
- A runtime MUST NOT report `effective_at` before the verification probe returns `pass`.

**Common failure modes:**

- Reporting `acknowledged_at` as `effective_at`. The runtime acknowledged the request; it has not verified the mode is in effect.
- Reporting `effective_at` based on configuration state rather than probe result. The configuration says read-only; the wrapper layer has not enforced it yet.
- Caching probe results across activations. A cached probe from before the activation is not evidence.

## Failure modes and reporting

When a runtime cannot fully activate a requested mode, it MUST return a structured failure response. The response MUST include:

| Field | Description |
|---|---|
| `error` | Stable error code (e.g., `partial-activation`, `tool-wrapper-unavailable`, `session-termination-failed`). |
| `succeeded_components` | List of mode components that activated successfully. |
| `failed_components` | List of mode components that failed, with per-component error detail. |
| `fallback_mode` | The mode currently in effect (which may be lower than requested). |

The runtime MUST NOT report success when the requested mode is only partially activated. The Incident Commander needs to know the actual state, not the wished state.

## Reference Implementations (informative)

The following are illustrative integration patterns. They are not normative and conformance does not require them.

- **LangGraph / Anthropic Claude Agent SDK / AutoGen**: implement Activate as a `ToolNode` reconfiguration; implement probe as a synthetic tool call that the wrapper layer rejects per mode.
- **AWS Bedrock Agents**: implement Activate by toggling the agent's action group permissions and updating the agent alias; implement probe by invoking the agent through a controlled test runtime.
- **Vendor copilots**: implement Activate through the customer-controllable identity boundary (IdP user disable, OAuth grant revocation, network egress block) as documented in [Playbook 10](../playbooks/10-vendor-copilots.md). The vendor copilot is conformant when the customer can exercise the documented controls within the TTA target.

## Conformance test suite

A runtime claiming conformance with this contract MUST pass the following test sequence quarterly per [Playbook 14 (Testing for Agent Failure Modes)](../playbooks/14-testing-for-agent-failure-modes.md):

1. **Cold-start activation:** activate M1 against an agent that has never been activated. Measure TTA from request to probe-confirmed effective.
2. **In-flight termination:** activate M1 while the agent has a write tool call in flight. Confirm the call is terminated, not completed.
3. **State persistence:** activate M1, restart the runtime, query Status. Confirm M1 is still in effect.
4. **Probe accuracy:** activate M1, externally invoke a write tool, confirm the probe shows the denial.
5. **Mode progression:** activate M1, then M2, then M3 with a specific scope, then M4. Confirm Status reflects each transition with correct probe evidence.
6. **Failure reporting:** simulate a tool wrapper unavailability during M3 activation. Confirm the runtime returns `partial-activation` with the actual state.
7. **Bulk Status:** query Status for 50 agents simultaneously. Confirm sub-second response.
8. **Deactivation separation of duties:** attempt to deactivate M3 using the same actor who activated it. Confirm the runtime denies the deactivation.

Drill results MUST be recorded in the AI-BOM `kill_switches.mX.tested_at` field per [`ai-bom.schema.json`](ai-bom.schema.json).

## Related

- **[Kill-Switch Modes (overview)](../kill-switches/overview.md):** the framework specification this contract implements.
- **[Framework Minimum Viable Overlay](../framework/01-minimum-viable-overlay.md):** MVO-2 Safe Modes is the control this contract operationalizes.
- **[Playbook 04: Tool Design Is Containment](../playbooks/04-tool-design-is-containment.md):** the tool tiering that M3 acts on.
- **[Playbook 07: Secrets and Tokens](../playbooks/07-secrets-and-tokens.md):** the credential-snapshot-before-rotation sequence required during M4.
- **[Playbook 11: Monitoring That Truly Detects Agent Incidents](../playbooks/11-monitoring-detection.md):** the detection rules that consume credential events and trigger automated mode transitions.
- **[Playbook 13: The Six Metrics](../playbooks/13-six-metrics.md):** Metric 2 (Containment TTA / TTSM) trends drill-measured TTA over rolling 90 days.
- **[Playbook 14: Testing for Agent Failure Modes](../playbooks/14-testing-for-agent-failure-modes.md):** the drill discipline that exercises the conformance test suite quarterly.
- **[ai-bom.schema.json](ai-bom.schema.json):** the AI-BOM schema that records kill-switch implementation and drill state per agent.
- **[credential-event.schema.json](credential-event.schema.json):** the credential-event log schema emitted when mode activation involves credential operations.
- **[privilege-matrix.schema.json](privilege-matrix.schema.json):** the Privilege Matrix schema that defines which tools M3 acts on.

---

*Source: AI IR Overlay framework specification, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
