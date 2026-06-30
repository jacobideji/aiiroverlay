<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Kill-Switch Modes (M0-M5)                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Containment is not one switch. Six modes with TTA targets.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Kill-Switch Modes: The Containment Ladder

> The "kill switch" is not one switch. It is six modes that escalate from passive observation to full disable, and back.

Binary on/off is rarely appropriate in production. The Overlay defines **six modes** so containment can be calibrated to confidence, impact, and business need.

---

## The Modes at a Glance

| Mode | Name | Use when | TTA target | Approver |
|---|---|---|---|---|
| **M0** | Observe | Normal operations | n/a | Owner |
| **M1** | Read-Only | Suspicious behavior; low/moderate impact | **≤ 10 min** | Tier-1 SOC |
| **M2** | Approvals Required | Agent must keep operating; actions need two-person rule | **≤ 10 min** | Tier-1 SOC |
| **M3** | Tool Tiering | Targeted containment. Disable high-risk tools only | **≤ 10 min** | Tier-1 SOC |
| **M4** | Full Disable | Active harm, confirmed misuse, or evidence of compromise | **≤ 10 min** | Tier-1 SOC |
| **M5** | Controlled Re-Enable | Containment validated; staged recovery | n/a | CISO / IC |

> **TTA** = Time-To-Activate. Measured from incident-commander order to mode in effect. TTA targets are **drill-measured**. Live-incident TTA is tracked separately under [Playbook 13 Metric 2](../playbooks/13-six-metrics.md). The targets define readiness; live measurement reveals operational reality. A live TTA above target enters the [Playbook 18](../playbooks/18-post-incident-hardening.md) hardening cycle, not a conformance failure.

> **Autonomous-agent qualification (v0.33.0):** the ≤ 10-min Tier-1 SOC activation owner assumes a staffed Security Operations Center available to receive the incident-commander order. For purely autonomous agents in 24/7 operation where no SOC is staffed off-hours (and the agent owner is the only human in the loop), the M3/M4 activation path requires **automation** that this v0.33.0 specification does not yet define. Adopters in this profile should treat automated activation triggers as an MVO-2 prerequisite and document the trigger rules (signal source, threshold, mode, scope) per their own conformance discipline pending the v1.1 automation-trigger specification (see [`CHANGELOG.md`](../CHANGELOG.md) `[Unreleased]` v1.1 backlog).

### Mode Variants

The six modes above are canonical. Several playbooks document scenario-specific **variants** that scope an existing mode more narrowly. Variants are extensions of an existing mode, not new modes. The canonical ladder remains M0 through M5.

**Variant Selector (quick reference for 3am responders).** Match your signal pattern to the recommended variant; the source playbook holds the full activation discipline.

| Signal pattern (what you observe) | Recommended variant | Source playbook |
|---|---|---|
| Suspected corpus poisoning; retrieved content tampered or includes injected instructions | **M3-RAG** | [PB03](../playbooks/03-rag-knowledge-base-forensics.md) |
| Injection arriving through a content channel (email, ticket, calendar, document) the agent reads | **M3-Workflow** | [PB06](../playbooks/06-prompt-injection-workflow.md) |
| Output-leakage incident; data exposure through routine agent outputs | **M3-Output** | [PB09](../playbooks/09-output-leakage.md) |
| Vendor copilot under shared responsibility; vendor-side containment needed | **M3-Vendor** | [PB10](../playbooks/10-vendor-copilots.md) |
| Cascade propagating through multi-agent delegation chain | **M3-Delegation Cap** | [PB08](../playbooks/08-multi-agent-blast-radius.md) |
| Behavior shift traceable to a recent model upgrade, prompt edit, policy tune, retriever change, or index rebuild | **M3-Drift** | [PB22](../playbooks/22-model-policy-drift.md) |
| Active misuse confirmed against a single corpus only; other corpora can keep serving | **M4 (corpus-scoped)** | [PB12](../playbooks/12-insider-threat-3.md) |
| Single user identified as suspect; their broader access must stay live for HR/Legal protocols | **M4 (agent-suspended-for-user)** | [PB12](../playbooks/12-insider-threat-3.md) |

**Full variant catalog (with scoping detail and use-case prose):**

| Variant | Scopes | Source playbook | Use when |
|---|---|---|---|
| **M3-RAG** | M3 Tool Tiering applied to the retrieval layer | [Playbook 03: RAG / Knowledge-Base Forensics](../playbooks/03-rag-knowledge-base-forensics.md) | Suspected corpus poisoning. Disable retrieval against the suspect corpus while preserving the agent's other capabilities. |
| **M3-Delegation Cap** | M3 Tool Tiering applied to inter-agent delegation depth | [Playbook 08: Multi-Agent Systems Multiply Blast Radius](../playbooks/08-multi-agent-blast-radius.md) | Cascade is propagating through deep delegation chains. Cap maximum delegation depth (typical floor: 2 hops). |
| **M3-Workflow** | M3 Tool Tiering applied to the content channel feeding the agent | [Playbook 06: Rethinking Prompt Injection as a Workflow Threat](../playbooks/06-prompt-injection-workflow.md) | Workflow injection is arriving through a specific corpus, queue, or inbox. Pause ingestion from the affected channel while leaving the agent's other capabilities live. |
| **M3-Vendor** | M3 Tool Tiering executed vendor-side for a vendor-managed agent | [Playbook 10: Vendor Copilots and Mutual Responsibility](../playbooks/10-vendor-copilots.md) | The agent is a vendor copilot under shared responsibility. Customer-controllable containment (identity boundary, data scope) activates immediately; vendor-side granular containment runs in parallel under the contracted SLA. |
| **M3-Output** | M3 Tool Tiering applied to a specific output channel or destination class | [Playbook 09: Leakage Without a Breach (AI Output Incidents)](../playbooks/09-output-leakage.md) | Output-leakage incident: disable a specific output channel (external email send, customer-facing ticket comment, public chat post, auto-CC) or destination class (external systems, customer-facing systems, regulated-data destinations) while preserving the agent's other capabilities. |
| **M3-Drift** | M3 Tool Tiering scoped to a specific recently-changed component while pre-change state is restored | [Playbook 22: Model and Policy Drift](../playbooks/22-model-policy-drift.md) | Change-window analysis has identified a specific component (model version pin, system prompt, policy configuration, retriever parameters, tool schema, memory configuration) as the most likely drift source. Roll back the identified component to the last known-good state and validate against the Drift Canary pack; the agent's other capabilities are preserved. |
| **M4 (corpus-scoped)** | M4 Full Disable bounded to a specific corpus | [Playbook 12: Insider Threat 3.0](../playbooks/12-insider-threat-3.md) | Active misuse confirmed against one corpus; other corpora can keep serving. |
| **Agent suspended for user** | M4 Full Disable bounded to a specific user identity | [Playbook 12: Insider Threat 3.0](../playbooks/12-insider-threat-3.md) | Single user is the suspect; HR/Legal protocols require their broader access stay live for investigation. |

A reader claiming framework conformance is conforming to **M0 through M5**. Variants are operational refinements documented in their source playbooks; they do not add new mode numbers.

---

## Mode 0: Observe (Baseline)

**Purpose:** Normal operations with logging.

**Requirements:**

- Tool calls logged with parameters and outcomes
- Prompt/response logged for the configured retention window
- Identity correlation in SaaS audit logs

**Exit criteria:** Incident declared. Step up to M1 (or further) based on confidence.

---

## Mode 1: Read-Only (Preferred First Containment)

**Purpose:** Stop writes without stopping the business.

**What changes:** All write tools are stripped from the agent's tool set. Read and query tools remain.

**Use when:**

- Suspicious behavior with unclear scope
- Business impact appears low to moderate
- You need time to investigate without triggering customer-visible failures

**Operational checks:**

- [ ] All write tools confirmed disabled in production config
- [ ] Test query confirms reads still function
- [ ] Logging continues at M0 fidelity

**Exit criteria:** Investigation confirms benign (return to M0), confirms harm (step up to M3/M4), or needs continued operation with control (step to M2).

---

## Mode 2: Approvals Required (Two-Person Rule)

**Purpose:** Continue operation, but no action without a human approver.

**What changes:** Every tool call is queued for human approval before execution.

**Use when:**

- Agent must continue for business continuity
- Risk of automated action is unacceptable
- Cost of full disable is higher than approval latency

**Operational checks:**

- [ ] Approval queue is staffed
- [ ] Average approval latency is acceptable for business need
- [ ] Approver has authority to deny

**Exit criteria:** Risk reduced (return to M1 or M0), or containment must escalate (M3/M4).

---

## Mode 3: Tool Tiering

**Purpose:** Contain selectively. Disable high-risk tools, keep low-risk.

**What changes:** Specific tools (external email send, code deploy, financial actions) are disabled. Lower-risk tools (internal search, status lookup) remain.

**Use when:**

- The harm vector is known and isolated to specific tools
- Business needs require continued operation of unaffected tools
- Full disable would cause unacceptable disruption

**Operational checks:**

- [ ] Tier definitions are pre-documented (see the [Agent Privilege Matrix](../templates/agent-privilege-matrix.csv))
- [ ] Disabled tools confirmed unreachable in production
- [ ] Remaining tools confirmed operational

**Exit criteria:** Vector contained (step down to M1/M2), or scope expands (M4).

> **RAG-specific containment:** when the suspected attack path is the retrieval layer (RAG, knowledge base, vector index), use the *M3-RAG* variant. Cut retrieval to the suspect corpus and leave the other corpora alone. The agent keeps working with reduced knowledge but no exposure to poisoned content. See [Playbook 03: RAG / Knowledge-Base Forensics](../playbooks/03-rag-knowledge-base-forensics.md) for the freeze-the-world sequence and the seven-component pipeline forensics.

---

## Mode 4: Full Disable

**Purpose:** Hard stop.

**What changes:** Agent is taken offline. Active sessions are terminated. Tokens are scoped for revocation (not yet rotated; see Evidence Plan).

**Use when:**

- Active harm is occurring
- Compromise is confirmed
- Containment under M1 to M3 has failed

**Operational checks (critical sequence):**

- [ ] **Snapshot identity and capabilities BEFORE token rotation** (see Step 2 of the [Minimum Evidence Set](../evidence/minimum-evidence-set.md))
- [ ] **Capture the Minimum AI Evidence Set BEFORE redeployment**
- [ ] Only then: rotate credentials, clean corpora, redeploy

> Rotating tokens before capturing scopes is the single most common evidence-destruction failure in AI IR.

**Exit criteria:** Eradication complete. Move to M5 controlled re-enable.

---

## Mode 5: Controlled Re-Enable (Recovery)

**Purpose:** Restore operation in stages, with validation at each step.

**Sequence:**

1. **Re-enable in Read-Only (M1).** Confirm the agent functions and logs flow.
2. **Validate retrieval and tool policies.** Corpora versions confirmed clean.
3. **Replay the incident scenario in a safe harness.** Confirm fix holds.
4. **Re-enable tools incrementally.** Start with low-risk, monitor for drift.
5. **Return to M0 Observe.** Only after all of the above.

**Approver:** CISO or designated Incident Commander. **Never** the original agent owner alone.

**Operational checks:**

- [ ] Post-incident hardening complete (see [Playbook 18: Post-Incident Hardening](../playbooks/18-post-incident-hardening.md))
- [ ] Monitoring thresholds updated to detect recurrence
- [ ] Tabletop scheduled within 30 days to validate the fix

---

## Pre-Production Requirements

Before ANY agent reaches production:

- [ ] All six modes have been **implemented** in code/config
- [ ] All six modes have been **tested** in a tabletop drill
- [ ] **TTA targets are met** in measurement (not promised)
- [ ] Runbook documents who pulls which lever, with backup approvers

If any of the above is "not yet," the agent is not production-ready.

---

## Related

- **The Six Triage Questions:** [`triage/six-questions.md`](../triage/six-questions.md)
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md)
- **Tool Design Is Containment** (Playbook 04): [`playbooks/04-tool-design-is-containment.md`](../playbooks/04-tool-design-is-containment.md)
- **Testing for Agent Failure Modes** (Playbook 14): [`playbooks/14-testing-for-agent-failure-modes.md`](../playbooks/14-testing-for-agent-failure-modes.md)
- **RAG / Knowledge-Base Forensics** (Playbook 03): [`playbooks/03-rag-knowledge-base-forensics.md`](../playbooks/03-rag-knowledge-base-forensics.md)

---

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
