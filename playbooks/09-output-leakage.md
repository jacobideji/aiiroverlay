<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 09: Leakage Without a Breach (AI Output Incidents)       -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The output-side playbook. The agent does not need to exfiltrate data. It just needs to include the data in its output. Treat output channels as exfiltration paths, because in practice they are.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 09: Leakage Without a Breach (AI Output Incidents)

> *In production AI deployments, the most common data incident in 2026 is not a breach. It is a confidentiality failure stemming from the agent's own output: a copilot pasting internal escalation notes into a customer ticket, a sales assistant CC'ing the wrong customer on a contract draft, a code copilot logging credentials in a public response. No malware alert fires. No unauthorized login appears. The agent does exactly what it was designed to do: retrieve context, generate an answer, and share it in the workflow. The incident lives at the output layer, in ordinary business systems, and is often invisible until a human spots the error.*

## Premise

Traditional incident response assumes a breach pattern: someone got in, or something left the network. The forensic question is *"how did the attacker bypass our controls?"* AI output incidents invert that pattern. The agent has legitimate access. The output channel is sanctioned. The destination is a normal business system. The leaked content was retrieved through authorized retrieval. Every step looks routine in isolation. The harm is in the composition.

The incident class this playbook addresses is **data leakage without a breach**: the agent's output, generated and distributed through authorized channels, contains information the agent should not have shared with the destination it reached. Concretely:

- A support copilot includes internal escalation notes in a customer-facing ticket comment.
- A sales assistant CC's a fragment of one customer's record on a different customer's email.
- A code-completion agent posts plaintext credentials in a response logged to a public commit history.
- A research assistant cites an internal document the customer should not have access to.
- An HR copilot summarizes a confidential personnel matter in a ticket visible to the wider team.
- A vendor copilot's output reaches an external partner with content the customer never authorized to share.

The common pattern: there is no breach signal. No DLP rule on the egress firewall fires. No identity provider flags unusual access. The agent's audit log shows a legitimate retrieve, a legitimate generate, and a legitimate write to a configured destination. The exposure is real. The investigative tools the security team is used to deploying are tuned for a different incident class.

This playbook ships the operational discipline for the output-side response: the safe-mode sequence that contains output exposure without erasing the trail, the **two-perspectives scoping** (what the agent saw and where the output traveled), the output-channel-classified containment via the **M3-Output** kill-switch variant, the evidence-set extensions that distinguish output incidents from input or context incidents, and the architectural defense (output-layer DLP) that converts the response into permanent guardrails.

**Mental Model clauses engaged:** *Acts* (primary, since the agent's output is the action that creates exposure); *Retrieves* (the source of the leaked content); *Remembers* (conditional, if agent memory contributed to the output context).

**Use this playbook when:** an agent output contains sensitive data that should not have reached the destination it reached · a customer-facing ticket, email, chat post, or CRM record contains internal-only or other-customer content · a downstream system or user reports unexpected content from an AI assistant · a retrieval-dominance or anomalous-output detection per [Playbook 11](11-monitoring-detection.md) correlates with an external-facing tool call · a vendor copilot output (per [Playbook 10](10-vendor-copilots.md)) is implicated in customer-side confidentiality exposure · a credential, key, PII, PHI, or other sensitive data class appears in an agent-generated output anywhere it should not.

## First-Hour Actions

The first hour of an output-leakage incident has two jobs that distinguish it from input-side (PB06) or context-side (PB03) response: **stop the agent from generating additional leaked output**, and **map the existing output distribution before any cleanup begins**. Cleanup destroys the trail. The investigation has to capture distribution first.

### The 60-minute output-leakage triage

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Switch the agent to [Mode M1 Read-Only](../kill-switches/overview.md), [Mode M2 Approvals Required](../kill-switches/overview.md), or the M3-Output variant described below.** The choice depends on whether output is in flight. If outputs are still being generated and posted, M3-Output (disable the specific output channels involved) is the surgical move. If the harm vector is unclear, M1 stops all writes while you investigate. | Tier-1 SOC |
| 10–20 | **Preserve evidence before cleanup.** Export prompt and output logs for the incident window per [Minimum Evidence Set Type A](../evidence/minimum-evidence-set.md). Export the tool-call ledger per Type B, including denied calls and approval-gate denials. Export retrieval traces per Type C. Capture the configuration snapshot per Type E. Do not modify the system prompt, retraining policy, or output filter yet. Cleanup destroys the trail. | Detection engineer |
| 20–35 | **Map the output distribution.** For every channel the agent writes to (email, CRM records, ticketing comments, chat channels, code repos, public web surfaces), enumerate where the implicated output landed. Internal vs external. Customer-facing vs employee-facing. Auto-archived vs ephemeral. Sent and confirmed vs queued and not yet delivered. This is the **output-side complement to Type F (Identity and SaaS Audit-Log Correlation)**; the distribution map is what scopes the incident. | Agent owner + the platform team(s) for each destination |
| 35–45 | **Restrict retrieval at the source.** Narrow the agent's retrieval corpora to known-safe sources for the duration of the investigation. Disable connectors to sensitive sources (HR, finance, legal, identity stores, anything that holds the data class implicated in the leak). Add temporary filters for high-risk document types until the investigation closes the retrieval-side gap. Without this step, the agent will re-retrieve the same sensitive content and re-leak it the next time the prompt context aligns. | Platform engineer + corpus owner |
| 45–55 | **Walk the [Six Triage Questions](../triage/six-questions.md) with one extension.** Q1 (tools), Q2 (write targets), Q3 (identity), Q6 (evidence plan) follow standard discipline. Add a seventh: *what is in the output that should not be there, and where did the output go?* The output-class incident is defined by the answer to that pair. | Incident Commander |
| 55–60 | **Convene the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) if any of the following applies.** Customer data was included in the output. PII, PHI, payment card data, or other regulated data class appeared. The output reached an external recipient. A credential or secret was included in an output logged anywhere accessible. Any of these triggers the convening protocol regardless of containment mode. | Incident Commander |

**Discipline:** the output distribution map is the chain-of-custody anchor for an output incident. Without it, the investigation cannot answer *"who saw what?"* with evidence, only with inference. Treat the distribution map with the same discipline as token snapshotting in [Playbook 07](07-secrets-and-tokens.md). The instinct to delete the leaked content from the ticket, the email, or the chat post before mapping is the most common response failure in this incident class. Cleanup happens after distribution is mapped, not before.

**Critical rule:** the output content remains in place (with restricted visibility if necessary) until the distribution map is complete. Removing the leaked output from one destination without mapping all destinations risks declaring an incident closed when the same content is still live in other systems.

## Containment Options

Containment for an output-leakage incident maps to the framework's [Kill-Switch Modes](../kill-switches/overview.md) with one variant introduced by this playbook: **M3-Output**.

### Mode mapping for output-leakage incidents

| Mode | Use when | What changes |
|---|---|---|
| **M0 Observe** | Normal operation with output-DLP active per the hardening section below | Full logging continues. Output channel classification and sensitive-content scanning operate on every generated output before it reaches its destination. |
| **M1 Read-Only** | Suspected output leakage with unclear scope or unclear channel | All write tools stripped. The agent can still serve read-only requests but cannot generate new outputs that reach business systems. Useful when the harm vector is not yet bounded to a specific channel. |
| **M2 Approvals Required** | Agent must continue serving (high-volume support, ops desk) and the output vector is bounded | Every output above a sensitivity threshold (defined per channel) routes to a human approver who sees the proposed output, its retrieval sources, and the destination before authorizing the post or send. |
| **M3 Tool Tiering** | Known vector: a specific tool is generating the leaked output (e.g., external email send) | Disable the affected tool class fleet-wide. Keep low-tier tools live for business continuity. |
| **M3-Output (variant introduced by this playbook)** | The harm vector is a specific output channel or destination class, not the agent's tools generally | **Disable specific output channels or destination classes** (external email sending; customer-facing ticket comment fields; public chat posts; auto-CC; any destination class with the specific leakage profile) **while preserving the agent's other capabilities**. Useful when the channel cannot be globally locked but the leakage destination class is identified. |
| **M4 Full Disable** | Confirmed irreversible external exposure (credential leaked to an external recipient, customer data confirmed reached a non-authorized customer, regulated data confirmed in an unauthorized system) | Stop the agent. Snapshot evidence per [Playbook 07](07-secrets-and-tokens.md) before any token rotation. |
| **M5 Controlled Re-Enable** | Output-layer DLP shipped, channel classification deployed, replay validation passes | Staged recovery per the Recovery Sequence below. |

### The destination-class scoping principle

The first investigative decision in an output-leakage incident is **what class of destination received the leaked content**. The containment response differs by destination class.

| Destination class | Default containment | Rationale |
|---|---|---|
| **Internal-only system (employee-facing chat, internal wiki, internal ticket comment, engineering log)** | M2 Approvals on the affected channel; agent continues other operations | Exposure is bounded to internal audience; investigation can proceed without taking the agent offline |
| **Customer-facing system (customer ticket, customer email, customer-visible CRM field, customer chat)** | M3-Output on the affected channel class; agent continues other capabilities | Exposure has reached customers; channel must be paused; agent's other capabilities preserved for business continuity |
| **External system (public web surface, partner-shared document, vendor-side log, third-party SaaS the customer's customers can read)** | M3-Output fleet-wide on external classes + M4 escalation review | External exposure has highest disclosure consequence; pause all external output classes immediately while investigation runs |
| **Regulated data class in any destination (credentials, PHI, payment card data, regulated AI use case data)** | M4 Full Disable plus immediate Materiality and Disclosure convening | Regulatory clocks may have started; preserve forensic state before any cleanup |

## Evidence Priorities

The output-leakage evidence set extends the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A-F with explicit emphasis on the **output distribution map** as a Type F extension and on the **prompt-to-output composition trail** as a Type A extension.

### Evidence priorities ranked for output leakage

| Code | Evidence Type | Priority | Why it matters |
|---|---|---|---|
| **A** | Prompt and Response Record | **Critical** | The leaked content is in the response. Capture the full assembled prompt (system, developer, retrieved context, user message) and the full output including every fragment that reached a destination. The composition trail is what proves whether the leak was prompt-driven, retrieval-driven, memory-driven, or a combination. |
| **B** | Tool-Call Ledger | **Critical** | Every output that reached a business system was a tool call. Capture the tool calls with parameters (the full output content as the parameter), results (the destination acknowledgment), and approver identity if an approval gate was active. Denied calls are evidence the gate held; successful calls are evidence the gate did not catch the sensitive content. |
| **F** | Identity and SaaS Audit-Log Correlation (extended with output distribution map) | **Critical** | Where the output went after the agent posted it. For each destination class identified in the First-Hour distribution map, pull the downstream system's audit logs to confirm who accessed the leaked content, who forwarded it, who exported it. The **distribution map is the output-side Type F**; it is what answers "who saw the leak?" with evidence rather than inference. |
| **C** | Retrieval Traces | **Critical** | The leaked content came from somewhere. The retrieval trace identifies the source corpus, document, version, and chunk that ended up in the output. Without it, the investigation cannot determine whether the same source will re-leak under similar future prompts. This is the load-bearing connection to [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md) when retrieval is the source vector. |
| **D** | Memory Snapshot | High if memory `scope: per_user` or `scope: shared` | If the agent's memory carried the leaked content forward from a prior session, the memory snapshot is the evidence. Memory-driven leakage is the cross-session class that is particularly difficult to detect with output-only monitoring. |
| **E** | Configuration Snapshot | **Critical** | The agent's system prompt, tool definitions, output filters (if any), and destination configurations active at incident time. The configuration is what the agent was supposed to do; the response is what it actually did; the configuration snapshot proves whether the gap was a policy gap or an enforcement gap. |

### Output-incident-specific captures

In addition to A through F, capture:

- **The output distribution map** as a formal artifact: for each destination class, a list of specific destinations (ticket IDs, email message-IDs, CRM record IDs, chat channel + message IDs, repository commit IDs) that received the leaked content, with timestamps and recipient identities. This is the single most valuable artifact for the materiality call.
- **The downstream propagation log**: for destinations that allow secondary distribution (email forwarding, ticket sharing, chat reactions and replies that trigger notifications, CRM record exports), capture the propagation events that occurred between the initial leak and the containment activation.
- **The retrieval-to-output composition map**: for each fragment of leaked content in the output, identify the retrieval trace entry that produced it. This is the composition trail; without it, the post-incident hardening cannot target the source-side fix.

**Operational requirement:** the full output-leakage evidence set must be exportable within **60 minutes** of incident declaration. The distribution map and the retrieval-to-output composition map are the time-sensitive captures: downstream systems may have shorter retention windows than the agent's own logs (CRM update history, email send confirmations, chat message edit history). The evidence-export procedure must include the destination-side owners, not only the agent platform engineers.

## Recovery Sequence

Output-leakage recovery follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **three output-specific gates** added.

### Gate 1: Downstream content cleanup with chain-of-custody preservation

Recovery cannot begin before downstream content cleanup is planned. For each destination identified in the distribution map:

1. Coordinate with the destination's data custodian (ticketing system admin, CRM owner, email administrator, chat platform admin, repository owner). The agent owner does not unilaterally delete content from downstream systems.
2. Capture the leaked content in a read-only investigation store **before** removal from the production destination. The original remains as case file evidence.
3. Where customer data was exposed to other customers, follow the customer's regulatory disclosure determination from the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md). The cleanup sequence does not substitute for the disclosure obligation.
4. Where credentials or secrets were leaked, follow [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md) rotation discipline for those credentials before any cleanup; rotation precedes deletion.
5. Where the destination is external (vendor system, partner system, public surface), the cleanup may not be unilaterally possible. Document the limitation and the customer's communication plan with the affected external party.

### Gate 2: Source-side retrieval policy strengthened before agent re-enable

Recovery cannot proceed without addressing the source-side cause:

1. The retrieval corpus that produced the leaked content is re-classified. If the corpus contained data the agent should not have surfaced in the destination class, the classification was wrong. Update.
2. The retrieval filter rule that should have prevented the sensitive content from reaching the prompt assembly is shipped. This is a code or configuration change, not a prompt-engineering tweak in the system prompt.
3. The agent's retrieval scope is narrowed where appropriate. Where business need does not require the agent to retrieve a given corpus for a given task, the corpus is removed from the agent's retrieval set.
4. Validation: replay the original triggering prompt against the recovered retrieval configuration in a staging environment. The retrieval should no longer return the sensitive content. If it does, the source-side fix is insufficient.

### Gate 3: Output-layer DLP shipped before output tools re-enable

The post-incident architectural commitment is **output-layer DLP** (described in the Hardening section). Recovery does not re-enable output tools until output-layer DLP is operational:

1. The DLP rule that should have caught the sensitive pattern is shipped at the output layer (in the tool wrapper, not in the system prompt).
2. The DLP rule is tested against the original leaked content. The rule should block, redact, or queue for approval the content that was leaked.
3. The DLP rule is tested against benign business content. False positives are documented; if false-positive rate exceeds the operational threshold for the channel, the rule is tuned before re-enable.
4. The agent is re-enabled in [M1 Read-Only](../kill-switches/overview.md) first to confirm reads function and logs flow.
5. The output tools are re-enabled in destination-class order: internal-only destinations first, customer-facing destinations second, external destinations last. Each re-enable is a separate decision with a separate monitoring window.
6. Return to [M0 Observe](../kill-switches/overview.md) only after the agent has carried production traffic for 72 hours without anomaly. Lower the [Playbook 11](11-monitoring-detection.md) output-anomaly threshold to mean + 2σ for the first 14 days post-incident.

**Approver:** CISO or designated Incident Commander. **Never** the agent owner alone. The output-layer DLP fix must be validated by someone whose incentive is not to ship.

## Post-Incident Hardening

Output-leakage hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert the output channel from an exfiltration path into a governed surface.

### Boundary 1: Output channel classification

- **Every output channel the agent can write to is classified.** Internal-only (employee-facing chat, internal ticket comments, internal wikis); customer-facing (customer tickets, customer email, customer-visible CRM fields); external (partner systems, public surfaces, vendor-side logs). The classification is recorded in the agent's [AI-BOM](../templates/ai-bom.yaml) `tools[].write_targets` block with the destination class.
- **Output operations are tier-classified per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md).** Internal-only outputs default to Tier 1 with caps and allowlists. Customer-facing and external outputs default to Tier 2 with approval gates.
- **Channel-specific destination allowlists** are configured for every customer-facing and external channel. The agent cannot output to a destination outside the allowlist without explicit approval.
- **The destination class is logged with every output**, so the post-incident composition map can be reconstructed without manual correlation.

### Boundary 2: Output-layer DLP

- **DLP scanning operates at the output layer**, in the tool wrapper, before the output reaches the destination. Prompt-layer instructions to "do not include sensitive data" are not DLP; they are theatrical safety.
- **The DLP rule set covers the sensitive patterns the organization actually cares about**: credentials and keys, PII (SSN, customer identifiers, account numbers), PHI (if applicable), payment card data (if applicable), internal classifications (confidential, internal-only, attorney-client privileged), and any other organization-specific patterns the post-incident review surfaced.
- **DLP rules are channel-aware.** A sensitive pattern that is acceptable in an internal-only destination (where staff have the authorization) may be unacceptable in a customer-facing destination (where they do not). The DLP rule fires based on **content + destination class**, not on content alone.
- **DLP outcomes are logged per output**: matched, redacted, blocked, approved-after-review. The log is the source of the [Playbook 13 (Six Metrics)](13-six-metrics.md) DLP signal that joins the broader monitoring posture.

### Boundary 3: Approval gates for outputs containing sensitive content

- **Outputs that match DLP rules above the channel-specific threshold route to a human approver.** The reviewer sees the output content, the retrieved source(s) that contributed to the output, the destination, and the DLP rule that matched. The reviewer's authorization is logged with their identity and rationale.
- **The approval queue is staffed for the agent's operating hours**, with documented backup approvers. Approval latency is tracked per [Playbook 13](13-six-metrics.md) Metric 2-class measurement; if approval latency exceeds the business need, the channel's threshold is the gap, not the approval discipline.
- **Approval gates are not bypassed by retry logic.** If the agent generates an output that is blocked, the resolution is human-mediated, not an automatic prompt rewrite that may strip the DLP signal without addressing the underlying retrieval gap.

### Boundary 4: Detection

- **Output-content monitoring** per [Playbook 11 Family 1](11-monitoring-detection.md): outputs containing classified-sensitive patterns; outputs whose destination class is inconsistent with the content sensitivity; high-volume output bursts to a single destination.
- **Output-distribution monitoring**: a single output reaching an unusually wide audience (broadcast email, public web post, public ticket reply); auto-CC or auto-forward chains that propagate an output beyond the originating destination.
- **Retrieval-to-output correlation monitoring**: outputs that quote or restate sensitive content from a source the agent should not have surfaced in that destination class. The signal correlates the retrieval-side gap (the source was reachable) with the output-side gap (the DLP did not catch it).
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to all four boundaries. Output-leakage findings do not wait for the next quarterly review.

## Common Pitfalls

These are the highest-frequency failure modes specific to output-leakage incident response. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Cleaning up the leaked content before mapping distribution** | Operations runbook says fix the customer-visible content first | Primary evidence destroyed; distribution scope cannot be reconstructed; the case file is incomplete for the materiality call |
| **Rotating credentials before capturing the prompt-to-output composition trail** | Standard IR reflex applied without considering the output context | Cannot prove which retrieved source produced the leaked credential; the source-side gap remains open |
| **Adding prompt-layer instructions ("do not include credentials in output") as the fix** | Prompt engineering feels like a control | Theatrical safety; the prompt rule is bypassed the moment the user prompt contradicts it or the retrieval returns content that re-introduces the pattern |
| **Treating AI outputs as low-risk text** | Outputs land in ordinary business systems; cognitive bias treats them as application detail | Output channels function as exfiltration paths without alarm; the organization discovers the leakage class only after a serious incident |
| **Skipping the distribution map (only fixing the source)** | The retrieval-side fix feels sufficient because it prevents future leakage | Existing leaked content in downstream systems is not addressed; customers, regulators, or auditors discover residual exposure after the incident is declared closed |
| **Cleanup of downstream destinations without coordinating with data custodians** | Agent owner unilaterally edits content the agent posted | Audit trail of the cleanup is incomplete; chain-of-custody is broken for the original leaked content; some destinations have edit-history visibility that makes the cleanup visible to recipients |
| **Assuming a one-time leak when the retrieval is consistent** | The output incident is treated as a fluke | The same source-retrieval-destination combination produces the same leak the next time a similar prompt arrives; the organization sees the leak twice |
| **Letting memory carry the leaked content forward** | Memory cleanup is deferred or skipped | The agent re-uses the leaked content in subsequent sessions for the same user or, if memory `scope: shared`, for other users; the leak becomes a memory bleed incident |
| **No output destination classification** | The AI-BOM `write_targets` block lists destinations without classifying them | The investigation cannot quickly determine which destinations are customer-facing vs internal-only; containment is over-scoped or under-scoped because the destination class is unclear |
| **Treating customer-facing outputs the same as internal-only outputs** | The DLP rule set is destination-agnostic | Internal-acceptable sensitivity classifications leak to customer destinations because the channel-aware rule does not exist; the same DLP rule that is appropriate internally is the gap externally |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 Inventory extends to documenting every output destination class for every agent.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clause 1 (Acts) is the load-bearing discipline for output-leakage response. Clause 3 (Retrieves) governs the source-side fix.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Output-layer DLP and channel classification are Level 3 (Provable) capabilities; the post-incident hardening that ships them moves the agent's posture from Level 2 to Level 3 within the 5-business-day SLA.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). Output incidents that include customer data, regulated data, or external recipients trigger the convening protocol regardless of containment mode.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M3-Output variant introduced in this playbook disables specific output channel classes while preserving the agent's other capabilities.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). Types A, B, C, and F are load-bearing for output-leakage; the output distribution map is a Type F extension introduced by this playbook.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The `tools[].write_targets` block is the inventory artifact that supports destination classification and channel-aware DLP.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). Output operations are tier-classified; customer-facing and external destinations default to Tier 2.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook the output-leakage response operationalizes.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). The retrieval-side forensic depth this playbook depends on when the leaked content originated in a retrieval corpus.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The pre-incident discipline that determines whether output destinations are tier-classified and whether the tool wrapper is the right enforcement point for output-layer DLP.
- **Playbook 06: Rethinking Prompt Injection as a Workflow Threat** ([`playbooks/06-prompt-injection-workflow.md`](06-prompt-injection-workflow.md)). The input-side complement; together with this playbook and [Playbook 03](03-rag-knowledge-base-forensics.md), PB06 + PB03 + PB09 form the framework's input → context → output coverage triad.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). The credential-snapshot sequence required if leaked content includes credentials; rotation precedes destination cleanup.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). The vendor-copilot output-leakage response combines this playbook's discipline with the vendor-evidence and vendor-containment limits PB10 specifies.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The output-content and output-distribution detection rules that catch this incident class; PB11 Family 1 (action-based) covers the output side.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). The agent-as-insider scenario where output leakage is the mechanism rather than a one-off incident.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). The DLP outcome rates from Boundary 2 feed Metric 4-class drill currency for the output-DLP discipline.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA that output-leakage hardening inherits.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MAP 2.3, MEASURE 2.5 privacy and data governance for AI outputs, MANAGE 4.1).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports PR.DS-01 and PR.DS-02 for data-in-transit protection on the output path, DE.AE-02 anomalous event analysis, RS.MI-01 incident containment).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the operational response to the output-side of ASI06 Memory and Context Poisoning when memory contributes; it also operationalizes the response to OWASP Top 10 for LLM Applications 2025.1 **LLM02 Sensitive Information Disclosure**, which OWASP names as a top concern for production LLM and agentic systems).

## The Question to Carry Forward

If your highest-volume AI workflow pasted a credential into a customer-visible ticket comment right now, would anything stop it before a human noticed? Could your team, within 2 hours, identify both what the agent retrieved and where the output ended up? Answer the question for the one agent that handles the most customer-facing traffic. The answer reveals whether your output-leakage defense is real or aspirational.

If the answer is improvised, PB09 is the work plan. Classify the agent's output destinations this week. Ship output-layer DLP for the highest-volume customer-facing channel this month. Run a leakage drill against the source-to-destination composition map this quarter. Then move to the next agent in the inventory.

That is how output-leakage defense moves from documented to demonstrated. One agent, one channel, one destination class, one DLP rule at a time, on a cadence that holds.

---

*Source: AI IR Overlay newsletter, Issue #9, "Leakage Without a Breach: Responding to AI Output Incidents," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
