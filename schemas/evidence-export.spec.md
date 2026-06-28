<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Evidence Export Script Contract                                        -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                   -->
<!--  https://jacobideji.com                                                 -->
<!--  License: Apache 2.0. See LICENSE file in this package.                 -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The evidence export contract. Defines the script that captures the Minimum Evidence Set (Types A through F) within the framework's drill-measured 60-minute target, emits timing telemetry that Playbook 13 Metric 3 consumes, and operates on pre-staged access paths that exist before an incident.**

---

# Evidence Export Script Contract

## Overview

The framework's [Minimum Evidence Set specification](../evidence/minimum-evidence-set.md) defines six evidence types (A through F) that must be exportable within **60 minutes** of incident declaration. The 60-minute target is drill-measured per [framework/01 Measurement Scope](../framework/01-minimum-viable-overlay.md); live-incident timing is tracked separately under [Playbook 13 Metric 3 (Evidence Export Time / TTE)](../playbooks/13-six-metrics.md).

The 60-minute target is unachievable without a documented export script that operates on pre-staged access paths. Every adopter today writes their own. This specification provides the canonical script contract so adopters can converge on a single interface, share implementations across runtimes, and make Metric 3 measurement reproducible.

This document is not a reference implementation. It is the interface contract that any compliant evidence export script (a Python CLI, a Lambda function, a Step Functions workflow, an Argo Workflows pipeline, an internal SaaS) MUST or SHOULD implement for the framework's 60-minute SLA to be operationally achievable.

## Conformance language

This specification uses RFC 2119 conformance language:

- **MUST** indicates an absolute requirement.
- **SHOULD** indicates a strong recommendation, with documented justification for non-compliance.
- **MAY** indicates an optional feature.

A script is **conformant** when it implements all MUST requirements and documents any SHOULD-level deviations with the rationale.

## Script Interface

A conformant evidence export script MUST accept a single structured input, produce a single structured output, and emit timing telemetry throughout execution. The transport (CLI argument, JSON input, function call payload, workflow event) is implementation-specific. The semantics are not.

### Required inputs

| Field | Type | Required | Description |
|---|---|---|---|
| `incident_id` | string | yes | Reference to the incident ticket. The script's outputs are scoped to this identifier. |
| `agent_id` | string | yes | The agent identifier. Must match the AI-BOM `agent.name` field for cross-record join. |
| `window_start` | timestamp | yes | RFC 3339 timestamp for the start of the evidence window. The script MUST capture evidence from `window_start` onward. |
| `window_end` | timestamp | yes | RFC 3339 timestamp for the end of the evidence window. The script MUST NOT capture evidence after this time, even if the source system has additional data. |
| `evidence_types` | array | conditional | List of types to capture. If omitted, the script MUST capture all six (A through F). Adopters MAY pass a subset for partial exports (e.g., during retention emergencies). |
| `output_destination` | string | yes | The investigation store path or URI where the script writes outputs. The script MUST NOT write outputs to a destination the Incident Commander cannot access. |
| `actor` | string | yes | The Incident Commander or automated invoker. Becomes part of the manifest's authorization trail. |

### Required outputs

A conformant script MUST produce a **manifest** and one **artifact** per requested evidence type.

#### The manifest

A JSON document at `<output_destination>/<incident_id>/manifest.json` with the following structure:

| Field | Type | Description |
|---|---|---|
| `incident_id` | string | Matches the input. |
| `agent_id` | string | Matches the input. |
| `script_version` | string | Semantic version of the export script. Required for reproducibility. |
| `requested_at` | timestamp | When the script received the request. This is the Metric 3 measurement origin. |
| `completed_at` | timestamp | When the script finished (success or partial). |
| `actor` | string | Matches the input. |
| `requested_window_start` | timestamp | Matches the input. |
| `requested_window_end` | timestamp | Matches the input. |
| `overall_status` | enum | `success` (all requested types captured), `partial` (some types failed), or `failed` (all types failed). |
| `types` | array | Per-type records; see schema below. |

Per-type record schema:

| Field | Type | Description |
|---|---|---|
| `type` | enum | `A`, `B`, `C`, `D`, `E`, or `F`. |
| `status` | enum | `success`, `partial`, `failed`, or `skipped`. |
| `source_system` | string | The system the data was pulled from (e.g., `okta-system-log`, `salesforce-audit-trail`, `m365-unified-audit-log`, `langsmith`, `litellm-proxy-logs`). |
| `records_captured` | integer | Number of records in the artifact. |
| `output_path` | string | Path relative to the manifest where the artifact lives. |
| `started_at` | timestamp | When capture for this type started. |
| `completed_at` | timestamp | When capture for this type finished. |
| `duration_seconds` | integer | `completed_at - started_at` in seconds. |
| `failure_reason` | string | Required when status is `partial` or `failed`. Stable error code (e.g., `retention-exceeded`, `auth-failure`, `source-unreachable`, `timeout`). |
| `failure_detail` | string | Human-readable detail when status is not `success`. |

#### The artifacts

Per evidence type, an artifact at `<output_destination>/<incident_id>/<type>/`:

| Type | Output format | Required structure |
|---|---|---|
| **A** Prompt and Response Record | JSON Lines (`.jsonl`) | One line per prompt-response pair. Each line: `{timestamp, user_id, session_id, system_prompt_hash, user_prompt, assistant_response, tool_calls_invoked, model_id, model_params}`. |
| **B** Tool-Call Ledger | JSON Lines | One line per tool call. Each line: `{timestamp, tool_name, agent_id, principal, parameters, result_status, result_payload_summary, denied_reason}`. **Attempted AND denied calls MUST be included.** Per evidence/minimum-evidence-set.md, denied calls are evidence of intent. |
| **C** Retrieval Traces | JSON Lines | One line per retrieval event. Each line: `{timestamp, query, corpus_id, documents_retrieved: [{doc_id, version, similarity_score, chunk_index}], reranker_version, top_k_setting, filters_applied}`. |
| **D** Memory Snapshot | JSON | One snapshot per user or shared memory store, depending on `memory.scope` in the AI-BOM. Each snapshot: `{timestamp, scope, memory_store_id, contents_summary, retention_remaining}`. May be omitted with `status: skipped` if `memory.enabled: false`. |
| **E** Configuration Snapshot | JSON | One snapshot of the agent's configuration at `window_end`. Schema: `{timestamp, agent_id, system_prompts: [{version, hash, active_at}], tool_definitions: [...], guardrail_policies, retriever_settings, model_id, model_version}`. |
| **F** Identity and SaaS Audit-Log Correlation | JSON Lines per target system | One file per downstream SaaS system the agent has scopes for. Each line: `{timestamp, identity_principal, target_system, action, target_object, target_object_class, source_ip, correlation_id}`. The script MUST correlate `correlation_id` across systems where the agent's tool call produced traceable downstream actions. |

### Exit codes

A CLI implementation MUST use the following exit codes:

| Code | Meaning |
|---|---|
| 0 | `overall_status: success` |
| 1 | `overall_status: partial` |
| 2 | `overall_status: failed` |
| 3 | Invalid input (missing required field, malformed timestamp, etc.) |
| 4 | Output destination unavailable |
| 5 | Authorization failure (script lacks pre-staged access to one or more sources) |

Non-CLI implementations MUST emit a structured status that maps to these conditions.

## Per-Type Evidence Contracts

Each type below specifies the canonical source systems and the failure modes the script MUST handle.

### Type A: Prompt and Response Record

**Canonical sources:**

- Model provider APIs (Anthropic, OpenAI, Google) with appropriate retention extensions.
- LLM proxy logs (LiteLLM, Portkey, internal gateway) with structured prompt and response capture.
- LangSmith, LangFuse, or equivalent observability platforms.
- Vendor copilot prompt logs where the customer has documented export access per [Playbook 10](../playbooks/10-vendor-copilots.md).

**Failure modes:**

- **Retention exceeded:** model provider TTLs are often 24 to 72 hours per [evidence/minimum-evidence-set.md](../evidence/minimum-evidence-set.md). The script SHOULD invoke retention extension before pulling if the source supports it.
- **Vendor evidence pending:** vendor copilots may require named-escalation request per Playbook 10. The script MAY return `status: partial` with `failure_reason: vendor-pending` and continue with other types.

### Type B: Tool-Call Ledger

**Canonical sources:**

- Application middleware logs (the tool wrapper layer per [Playbook 04](../playbooks/04-tool-design-is-containment.md)).
- LangGraph, AutoGen, Bedrock Agents internal traces.
- API gateway or proxy logs for tool invocations.

**Special requirements:**

- **Denied calls MUST be included.** Per evidence/minimum-evidence-set.md, denied calls are evidence of injection or misuse intent.
- The ledger MUST include attempted calls that were rejected by the tool wrapper before the model received a response.

### Type C: Retrieval Traces

**Canonical sources:**

- RAG framework traces (LangChain, LlamaIndex, custom RAG).
- Vector store query logs (Pinecone, Weaviate, pgvector, Vertex AI Vector Search).
- Knowledge-base access logs.

**Special requirements:**

- Each retrieved chunk MUST carry `doc_id`, `version`, and `ingestion_timestamp` per [Playbook 03](../playbooks/03-rag-knowledge-base-forensics.md) Type C-extended discipline.
- The script MUST capture the embedding model version at retrieval time. Embedding version changes affect ranking and are forensically relevant.

### Type D: Memory Snapshot

**Canonical sources:**

- Agent memory backend (Redis, vector DB, application database).
- Agent framework state stores.

**Special requirements:**

- Per [Playbook 12](../playbooks/12-insider-threat-3.md), `memory.scope: shared` snapshots are the highest-risk evidence class for cross-tenant bleed investigations.
- If memory is disabled (`memory.enabled: false` in the AI-BOM), the script MUST emit `status: skipped` with no failure_reason.

### Type E: Configuration Snapshot

**Canonical sources:**

- Configuration management system (Git, ConfigMap, Parameter Store).
- Deployment manifests (Helm, Terraform, CloudFormation).
- Feature flag systems (LaunchDarkly, Split, internal).

**Special requirements:**

- The script MUST capture every system prompt version active during the evidence window, not only the current version.
- The script MUST capture the tool authorization rationale (the documented business need for each scope) per [Playbook 12 intent vector](../playbooks/12-insider-threat-3.md) discipline.

### Type F: Identity and SaaS Audit-Log Correlation

**Canonical sources:**

- Identity provider audit logs (Okta System Log, Entra Audit Logs, Auth0).
- SaaS audit logs (Salesforce Setup Audit Trail, M365 Unified Audit Log, ServiceNow, Workday, GitHub Audit Log).
- Cloud audit logs (AWS CloudTrail, GCP Cloud Audit Logs, Azure Activity Log).

**Special requirements:**

- The script MUST correlate identity attribution across systems using a stable correlation key per [Playbook 08](../playbooks/08-multi-agent-blast-radius.md) W3C `traceparent` discipline where applicable.
- Type F is the longest-tail capture in most environments. The script SHOULD parallelize source-system pulls.
- Vendor copilot Type F per [Playbook 10](../playbooks/10-vendor-copilots.md) splits between customer-side (IdP plus target systems) and vendor-side (vendor activity logs). The script MUST mark vendor-side captures with the vendor name in `source_system`.

## Timing Telemetry

The script MUST emit timing telemetry that [Playbook 13 Metric 3 (Evidence Export Time / TTE)](../playbooks/13-six-metrics.md) consumes. The telemetry interface:

### Required telemetry events

The script MUST emit the following events to the customer's observability stack (OpenTelemetry, Datadog, SIEM, internal):

| Event | When emitted | Required attributes |
|---|---|---|
| `evidence_export.started` | When the script receives the request | `incident_id, agent_id, requested_window_seconds, requested_types` |
| `evidence_export.type_started` | When capture for a specific type begins | `incident_id, agent_id, type, source_system` |
| `evidence_export.type_completed` | When capture for a specific type ends (any status) | `incident_id, agent_id, type, status, duration_seconds, records_captured` |
| `evidence_export.completed` | When the script finishes (success or partial) | `incident_id, agent_id, overall_status, total_duration_seconds, types_succeeded, types_partial, types_failed` |

### Metric 3 derivation

Per Playbook 13:

> *Metric 3: Evidence Export Time. Median minutes from incident-declaration order to full Minimum Evidence Set A-F captured.*

The script's emitted telemetry MUST permit computation of:

`total_duration_seconds / 60`

as the per-incident contribution to Metric 3. The aggregation (median across incidents in the rolling 90-day window) happens at the consumer side, not in the script.

### Conformance with framework SLA

- `total_duration_seconds` MUST NOT exceed 3600 (60 minutes) for the script to claim drill-conformance with framework/01 MVO-3.
- Per [framework/01 Measurement Scope](../framework/01-minimum-viable-overlay.md): the 60-minute target is drill-measured. A live-incident export that exceeds 60 minutes is a Playbook 18 hardening backlog item, not a conformance failure.

## Pre-Staged Access Requirements

The script MUST operate on pre-staged access paths. Negotiating IAM access during an incident is the framework's "ticketed" failure mode per [evidence/minimum-evidence-set.md](../evidence/minimum-evidence-set.md). The 60-minute SLA assumes `emergency_access: preapproved` per the [AI-BOM schema](ai-bom.schema.json).

### Pre-staged access checklist

Before the script can be invoked, the customer's platform team MUST establish:

| Resource | Purpose | Owner |
|---|---|---|
| **Investigation IAM role** | Read access to evidence sources without write permissions. Must be invocable by the Incident Commander without ticketing. | IAM team |
| **Identity-provider audit-log scope** | Read access to Okta System Log, Entra Audit Logs, etc., for the agent's principal | IdP team |
| **SaaS audit-log scopes** | Read access to Salesforce Setup Audit, M365 Unified Audit Log, ServiceNow, etc., for the target systems the agent writes to | SaaS owners |
| **Model provider retention extension** | Standing extension or per-incident-invocable extension for Type A data beyond the provider's default TTL | Procurement and platform |
| **Vendor copilot evidence export contract** | Documented vendor evidence export SLA per [Playbook 10](../playbooks/10-vendor-copilots.md) Boundary 1 (Contract) | Vendor management + legal |
| **Investigation store with chain-of-custody controls** | Tamper-evident destination for the script's outputs; access restricted to the Incident Commander and General Counsel | Security + legal |

### Validation

A conformant script SHOULD include a `--validate-access` mode that exercises each pre-staged access path WITHOUT capturing evidence. The mode MUST:

- Confirm the Investigation IAM role can be assumed.
- Confirm a read query against each canonical source system succeeds.
- Confirm the output destination is writable.
- Return a structured report listing any pre-staged access gaps.

The customer's platform team SHOULD run `--validate-access` quarterly per [Playbook 14 (Testing for Agent Failure Modes)](../playbooks/14-testing-for-agent-failure-modes.md) as part of the drill discipline.

## Failure Modes and Reporting

When the script cannot fully capture a requested evidence type, it MUST return a structured failure record in the manifest. The script MUST NOT silently degrade.

| Failure mode | When it occurs | Required action |
|---|---|---|
| `retention-exceeded` | The requested window falls outside the source's retention policy | Status `failed`. `failure_detail` lists the source's actual earliest available record. |
| `auth-failure` | IAM role expired or scope insufficient | Status `failed`. `failure_detail` lists the missing permission. Exit code 5. |
| `source-unreachable` | Source system API returned errors during the script's retry window | Status `partial` if some records were captured, `failed` if none. |
| `timeout` | The 60-minute budget was exhausted before this type completed | Status `partial`. `failure_detail` lists `records_captured / records_expected`. |
| `vendor-pending` | Vendor copilot evidence export pending vendor response | Status `partial`. Continue with other types. |
| `output-destination-unavailable` | Cannot write to investigation store | Status `failed` for all types. Exit code 4. |

The Incident Commander MUST receive the manifest regardless of overall status. A partial export is more useful than a missing export.

## Reference Implementations (informative)

The following are illustrative integration patterns. They are not normative and conformance does not require them.

- **Python CLI:** the canonical reference shape. Invoked as `evidence-export --incident-id ... --agent-id ... --window-start ... --window-end ... --output ...`. Parallelizes per-type captures using `asyncio` or `concurrent.futures`. Emits telemetry through OpenTelemetry.
- **AWS Step Functions:** state machine with per-type Lambda invocations in parallel; aggregator Lambda produces the manifest. Pre-staged IAM via cross-account assume-role.
- **Argo Workflows:** DAG with per-type pods in parallel; sidecar emits telemetry to Datadog. Pre-staged access via Kubernetes ServiceAccount tokens.
- **GitHub Actions on-call workflow:** triggered by PagerDuty webhook; runs export script in a hardened runner with pre-staged secrets. Suitable for smaller deployments.

## Conformance Test Suite

A script claiming conformance with this contract MUST pass the following test sequence quarterly per [Playbook 14 (Testing for Agent Failure Modes)](../playbooks/14-testing-for-agent-failure-modes.md):

1. **Cold-window export:** export a 2-hour window from 7 days ago for a representative production agent. Measure total duration.
2. **Recent-window export:** export the most recent 2 hours for the same agent. Confirm Type A data is captured before model provider TTL.
3. **Memory-disabled handling:** export from an agent with `memory.enabled: false`. Confirm Type D returns `status: skipped` without error.
4. **Vendor copilot export:** export from a vendor copilot. Confirm the manifest correctly identifies vendor-side vs customer-side sources.
5. **Validate-access dry run:** invoke `--validate-access` against all pre-staged paths. Confirm no gaps.
6. **Partial-failure reporting:** simulate Type F source-system unreachability. Confirm overall status is `partial` and other types still capture.
7. **Output integrity:** confirm the output destination preserves chain-of-custody (tamper-evident storage, audit logging of access).
8. **Telemetry consumption:** confirm the telemetry events feed into the customer's Playbook 13 Metric 3 dashboard. Compute the simulated Metric 3 value from the drill.

Drill results MUST be recorded in the AI-BOM `evidence_export.tested_export_minutes` field per [`ai-bom.schema.json`](ai-bom.schema.json).

## Related

- **[Minimum Evidence Set](../evidence/minimum-evidence-set.md):** the framework specification this contract implements.
- **[Framework Minimum Viable Overlay](../framework/01-minimum-viable-overlay.md):** MVO-3 Minimum Evidence Set + the Measurement Scope section that distinguishes drill-measured from live-incident timing.
- **[Materiality and Disclosure](../framework/04-materiality-and-disclosure.md):** the evidence captured by this script informs the materiality determination at the convening protocol.
- **[Playbook 01: The Agent Is a Privileged Identity](../playbooks/01-agent-as-privileged-identity.md):** the response playbook the export script supports.
- **[Playbook 03: RAG / Knowledge-Base Forensics](../playbooks/03-rag-knowledge-base-forensics.md):** Type C-extended discipline (the seven-component pipeline state).
- **[Playbook 04: Tool Design Is Containment](../playbooks/04-tool-design-is-containment.md):** the tool-call ledger discipline that Type B captures.
- **[Playbook 07: Secrets and Tokens](../playbooks/07-secrets-and-tokens.md):** the snapshot-before-rotation sequence the export script supports for M4 Full Disable scenarios.
- **[Playbook 08: Multi-Agent Systems Multiply Blast Radius](../playbooks/08-multi-agent-blast-radius.md):** the trace-ID correlation discipline for Type F across multi-agent topologies.
- **[Playbook 10: Vendor Copilots and Mutual Responsibility](../playbooks/10-vendor-copilots.md):** the customer-vs-vendor evidence boundary the script's `source_system` field reflects.
- **[Playbook 11: Monitoring That Truly Detects Agent Incidents](../playbooks/11-monitoring-detection.md):** detection events that may invoke the script automatically.
- **[Playbook 12: Insider Threat 3.0](../playbooks/12-insider-threat-3.md):** the intent vector documentation that Type E captures.
- **[Playbook 13: The Six Metrics](../playbooks/13-six-metrics.md):** Metric 3 (Evidence Export Time / TTE) that the script's telemetry feeds.
- **[Playbook 14: Testing for Agent Failure Modes](../playbooks/14-testing-for-agent-failure-modes.md):** the quarterly drill that exercises the conformance test suite.
- **[Playbook 18: Post-Incident Hardening](../playbooks/18-post-incident-hardening.md):** the 5-business-day SLA for closing pre-staged access gaps surfaced in drills.
- **[ai-bom.schema.json](ai-bom.schema.json):** the AI-BOM schema field `evidence_export.tested_export_minutes` consumes drill results from this script.
- **[kill-switch-api.md](kill-switch-api.md):** the companion runtime contract; mode activation may trigger evidence export as part of the response chain.

---

*Source: AI IR Overlay framework specification, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
