<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 06: Rethinking Prompt Injection as a Workflow Threat          -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                   -->
<!--  https://jacobideji.com                                                 -->
<!--  License: Apache 2.0. See LICENSE file in this package.                 -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The workflow injection playbook. The serious attacks do not happen in chat. They hide in tickets, emails, web pages, and policy documents that agents read as part of automated workflows. Architectural defense, not prompt engineering, is the counter.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 06: Rethinking Prompt Injection as a Workflow Threat

> *Prompt injection is widely thought of as a chat-UI risk. In production, the dominant pattern is a workflow attack: harmful instructions hidden inside the everyday content the agent already reads as part of its job. The agent obediently executes those instructions using its authorized tools. The defensive posture must shift from prompting to architecture.*

## Premise

Many security teams still picture prompt injection as someone typing *"ignore previous instructions"* into a chatbot. In production, that picture is wrong on every dimension. The serious attacks rarely involve a malicious user at the chat interface. They involve harmful instructions hidden inside the content the agent processes as part of an automated workflow: a customer support ticket whose hidden text tells the agent to email itself a list of high-value contracts, a vendor email whose footer carries instructions to update a vendor record, a web page whose markup includes an "agent context" block instructing the agent to disable its own guardrails, a policy document whose embedded notes redirect the agent's interpretation of permission rules.

This is **Prompt Injection 2.0**. The user did not type the instruction. The agent retrieved it. The injection enters through business processes that already exist and that the agent is supposed to trust. By the time the model sees the harmful instruction, the workflow has already routed it past every conventional defense: spam filters that scan for malicious code, DLP rules tuned for outbound data, endpoint security looking for unauthorized executables. None of those tools recognize a paragraph of natural language as an attack.

The risk is not that the model produces bad output. The risk is that the agent takes **authorized actions in the deployer's name**, through its own legitimate tools, against systems that audit-log the action as routine. The downstream record shows the agent's identity, the agent's authorized scopes, and a legitimate API call. The forensic question shifts from *"how did the attacker get in?"* to *"what did the agent see that told it to do this?"*

The defensive shift is fundamental. Prompt engineering ("tell the model to ignore injection attempts") is a model-layer defense against a workflow-layer attack. It is theatrical safety. The architectural counter is to treat retrieved content the way mature security treats untrusted code: never let raw external content reach an action context. Conversion of retrieved data into action requires approval, change preview, and destination checks.

**Mental Model clauses engaged:** *Retrieves* (primary; untrusted external content is the attack surface), *Acts* (secondary; the agent's tools execute the injected instruction), and *Remembers* (conditional; injection can persist in agent memory across sessions if the harmful instruction was summarized into long-term context).

**Use this playbook when:** an AI agent exhibits unexpected tool behavior after processing external content (tickets, emails, web pages, ingested documents, vendor data); a researcher reports indirect prompt injection on a deployed agent; the agent's output quotes or restates instructions found in retrieved content; a vendor copilot acts on customer-supplied data in ways inconsistent with the copilot's documented role; [Playbook 11 (Monitoring)](11-monitoring-detection.md) detection rules fire on influence-family signals correlated with new or recently modified external sources; or pre-production review identifies an agent that consumes untrusted external content as part of its normal workflow.

## First-Hour Actions

The first hour of a workflow-injection incident has two jobs that distinguish it from generic prompt-injection response: **preserve the source artifact before anyone cleans the channel**, and **stop the agent without destroying the retrieval chain**. The source ticket, email, or document is the primary evidence. The retrieval trace ties the source to the agent's behavior. Both must survive the first hour.

### The 60-minute workflow-injection triage

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Switch the agent to [Mode M1 Read-Only](../kill-switches/overview.md) or [Mode M2 Approvals Required](../kill-switches/overview.md).** Strip write tools for the affected agent. If the harmful action is already in flight, escalate to [Mode M4 Full Disable](../kill-switches/overview.md) and follow the [Playbook 07 snapshot-before-revocation sequence](07-secrets-and-tokens.md). | Tier-1 SOC |
| 10–20 | **Preserve the source artifact.** Capture the exact content the agent consumed: full body, hidden fields, attachments, version history, formatting metadata. Do not delete the source ticket, email, or document. Do not mark it as spam. Quarantine it with read access for the investigation. | Agent owner + ticketing/email/CMS owner |
| 20–35 | **Export the retrieval record.** Document retrieval traces (IDs, chunks, similarity scores) per [Playbook 03: RAG / Knowledge-Base Forensics](03-rag-knowledge-base-forensics.md). Pull connector logs and the assembled prompt context at the time of the agent's harmful behavior. | RAG/platform engineer |
| 35–45 | **Export the action record.** Archive tool-call logs with parameters, results, timestamps, and correlation IDs per [Minimum Evidence Set Type B](../evidence/minimum-evidence-set.md). Pay extra attention to attempted-but-denied calls; they are evidence of the injection's intent even where the agent's guardrails caught the obvious cases. | Detection engineer |
| 45–55 | **Walk the [Six Triage Questions](../triage/six-questions.md) with one extension.** Q1 (tools), Q2 (write targets), Q3 (identity), Q6 (evidence plan) follow standard discipline. Add a seventh: *what content did the agent consume that we did not author?* | Incident Commander |
| 55–60 | **Convene the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md)** if the injection reached Mode M3 or higher, OR if external recipients received agent output, OR if regulated data was touched. The convening protocol applies regardless of whether the agent's action was technically reversible. | Incident Commander |

**Discipline:** the source artifact is the chain-of-custody anchor. Without it, the investigation reconstructs the attack from inference rather than evidence. A ticket marked as spam or a deleted email cannot be re-examined. A quarantined source can. Treat the preservation step with the same discipline as token snapshotting in [Playbook 07](07-secrets-and-tokens.md).

**Critical rule:** the source artifact must be preserved **before** any cleanup of the ticketing, email, or CMS system. Operations teams routinely clean up after incidents; that cleanup destroys the workflow injection evidence by design. Pause the cleanup until the source artifact is captured.

## Containment Options

Containment for a workflow-injection incident maps to the framework's [Kill-Switch Modes](../kill-switches/overview.md) with adaptations specific to the attack surface. The injection enters through a content channel, so containment must address both the agent's tool surface and the content channel itself.

### Mode mapping for workflow-injection incidents

| Mode | Use when | What changes |
|---|---|---|
| **M0 Observe** | Normal operation with retrieval-anomaly detection active per [Playbook 11](11-monitoring-detection.md) | Full logging continues; retrieval traces, prompt assembly, and tool calls captured |
| **M1 Read-Only** | Suspected injection, no confirmed irreversible action yet | Strip write tools; reads continue so the agent still serves customers |
| **M2 Approvals Required** | Agent must continue serving (high-volume support, ops desk) and the harm vector is bounded | Every Tier-2 call routes to a human reviewer who sees the source content alongside the proposed action |
| **M3 Tool Tiering** | Known vector: a specific tool is being abused (typical case: the injection rides through external-email-send) | Disable the affected tool class; keep low-tier tools live for business continuity |
| **M3-Workflow (variant)** | The harm vector is the content channel itself: a specific corpus, queue, or inbox is delivering injected instructions | Pause ingestion from the affected channel while leaving the agent's other capabilities live. Useful when the channel cannot be globally locked but the injection source is identified. |
| **M4 Full Disable** | Confirmed irreversible external action triggered (external email sent, financial action committed, record changed in customer-visible system) | Stop the agent. Snapshot evidence per [Playbook 07](07-secrets-and-tokens.md) before any token rotation. |
| **M5 Controlled Re-Enable** | Source quarantined, architectural guardrail strengthened, drill replay passes | Staged recovery per the Recovery Sequence below |

### The classification-drives-containment principle

The first investigative decision in a workflow-injection incident is **whether the injection is a one-off or a campaign**. The containment response differs by classification.

| Classification | Default containment | Rationale |
|---|---|---|
| **One-off (single source document, single agent affected)** | M3-Workflow on the affected source; agent in M2 Approvals during investigation | The architectural surface stays live for unaffected work; the specific source channel is paused |
| **Campaign (multiple sources, possibly multi-agent)** | M3 Tool Tiering fleet-wide on affected tools; M3-Workflow on all suspected sources; consider M4 if multi-agent cascade per [Playbook 08](08-multi-agent-blast-radius.md) | The fact that multiple sources carry injection indicates a coordinated effort; the containment must be at the tool surface, not the source channel |
| **Undetermined** | M2 Approvals fleet-wide; M3-Workflow on the first known source; preserve both investigative branches | Cannot prejudge; preserve evidence for both possibilities |

## Evidence Priorities

The workflow-injection evidence set extends the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A–F with explicit attention to the **source artifact** and the **retrieval-to-action chain**.

### Evidence priorities ranked for workflow injection

| Code | Evidence Type | Priority | Why it matters |
|---|---|---|---|
| **C** | Retrieval Traces | **Critical** | The chain from the harmful content to the agent's input. Without it, the injection vector is unprovable. Capture document IDs, retrieved chunks, similarity scores, and the version of the document at retrieval time. |
| **E** | Configuration Snapshot | **Critical** | The agent's system prompt, tool definitions, untrusted-content labels, and guardrail policies active at incident time. The model's susceptibility depends on configuration that may change after the incident. |
| **A** | Prompt and Response Record | **Critical** | The fully assembled prompt (system, developer, retrieved context, user message) and the model's response, including any tool-call invocations. The assembled prompt is the smoking gun: it shows what the model actually saw. |
| **B** | Tool-Call Ledger | **Critical** | The actions the agent attempted based on the injected instruction. Capture attempted **and** denied calls. Denied calls are evidence of injection intent even where guardrails held. |
| **F** | Identity and SaaS Audit-Log Correlation | **Critical** | The downstream blast radius. Where the agent's output went after the agent produced it. Required for materiality determination. |
| **D** | Memory Snapshot | High if memory `scope: shared` or `per-user` with retention | Injection can persist in agent memory if the model summarized the harmful instruction into long-term context. The memory at incident time is causally relevant for the agent-as-insider scenarios in [Playbook 12](12-insider-threat-3.md). |

### Workflow-specific captures

In addition to A–F, capture:

- **The source artifact in its original form.** Full email body with headers, full ticket including hidden fields and attachments, full document with metadata and version history. This is the primary evidence of the injection vector.
- **The content channel access log.** Who created the source artifact, when, from what IP, with what authenticated identity. The author identity is often the most direct attribution path.
- **The connector log.** The ingestion path the source artifact took to reach the agent. Connector misconfiguration is a frequent contributing factor.
- **Pre-incident retrieval baseline.** What did the agent normally retrieve from this corpus or channel before the incident? A sudden shift in retrieval pattern is itself evidence.

**Operational requirement:** the full workflow-injection evidence set must be exportable within **60 minutes** of incident declaration. The source artifact and the retrieval trace are the most time-sensitive: a routine cleanup of the ticketing system or a routine re-indexing of the corpus can destroy them within hours. The evidence-export procedure must include the content channel owners, not only the agent platform engineers.

## Recovery Sequence

Workflow-injection recovery follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **two workflow-specific gates** added.

1. **Quarantine the source artifact.** Do not delete. Move the original to a read-only investigation store. The original is evidence and remains in the case file until the investigation closes.
2. **Strengthen the architectural guardrail** (*workflow-specific gate*). Before re-enabling, confirm the affected tool no longer accepts external content as a direct trigger. The architectural pattern: external content can produce drafts or proposed actions, never authorized actions. If the guardrail change requires code, ship it; if the change requires policy, document it; if the change requires both, ship and document.
3. **Re-enable the agent in [Mode M1 Read-Only](../kill-switches/overview.md).** Reads continue; writes remain blocked.
4. **Validate retrieval policy and content trust labeling.** Confirm the agent's retrieval layer correctly labels content from the affected channel as untrusted. Confirm the assembled prompt visibly distinguishes trusted system content from untrusted retrieved content.
5. **Replay the injection scenario in a sandboxed harness** (*workflow-specific gate*). Run the original source artifact (the quarantined attack) through the recovered agent with the new architectural guardrail in place. The agent should produce a draft or a proposed action, not an executed tool call. If the agent executes the tool call, the architectural fix is insufficient. Return to step 2.
6. **Re-enable Tier-1 tools incrementally** with caps at half pre-incident value for the first 24–72 hours.
7. **Re-enable Tier-2 tools one at a time** with [Approvals (M2)](../kill-switches/overview.md). Each Tier-2 re-enable is a separate decision with a separate approver and a separate monitoring window.
8. **Return to M0 Observe** only after the agent has carried production traffic for 72 hours without anomaly. Lower the [Playbook 11](11-monitoring-detection.md) retrieval-anomaly threshold to mean + 2σ for the first 14 days post-incident.

**Approver:** CISO or designated Incident Commander. **Never** the agent owner alone. The architectural fix must be validated by someone whose incentive is not to ship.

## Post-Incident Hardening

Workflow-injection hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion.

### Boundary 1: Tool architecture

- **Untrusted content never directly triggers Tier-2 tools.** External content can produce drafts, proposed actions, or summaries for human review. The architectural pattern is enforced in the tool wrapper, not in the system prompt.
- **Tier-2 tools require explicit approval** when invoked in workflows that consume external content. The approval is captured per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) discipline.
- **Tools that accept external content as a parameter** (the most common injection target) are scrutinized in code review. Treating external strings as agent instructions is a security defect, not a feature.

### Boundary 2: Content trust labeling

- **Every retrieved chunk is labeled with its source channel and trust class** before it enters the prompt assembly. Untrusted classes include customer support, vendor email, public web content, partner shared documents. Trusted classes include system prompts, internal policy documents, and configuration data.
- **The assembled prompt visibly distinguishes trusted from untrusted segments.** A common pattern: trusted system context above a delimiter, untrusted retrieved context below the delimiter with an explicit label. The label is informational for forensics, not load-bearing security.
- **The labeling is logged.** The retrieval trace captures the trust class assigned to each chunk so post-incident review can determine whether the labeling was correct.

### Boundary 3: Approval gates for content-driven actions

- **High-impact actions following retrieval of untrusted content require human review.** Examples: send external email, write to systems of record, deploy code, change security configuration, modify customer records.
- **The reviewer sees the source content alongside the proposed action.** A reviewer asked to approve a tool call without seeing the source content that prompted it cannot judge whether the call is appropriate.
- **Approval decisions are logged with reviewer identity, source content reference, and rationale** per the credential-event log schema in [Playbook 07](07-secrets-and-tokens.md).

### Boundary 4: Detection

- **Retrieval-anomaly alerting** per [Playbook 11 Family 2](11-monitoring-detection.md): a single document accounting for more than 40% of the agent's retrieval results within 24 hours; retrievals from corpora the agent does not historically use; high-frequency access to sensitive repositories the agent's business need does not require.
- **Output-pattern anomaly alerting**: the agent's response quotes or restates instructions found in retrieved content; the agent's response invokes tools without parameters the agent has historically used together; the agent's response references identities or systems outside its documented scope.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to all four boundaries. Workflow-injection findings do not wait for the next quarterly review.

## Common Pitfalls

These are the highest-frequency failure modes specific to workflow-injection response. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Cleaning the source ticket or email before snapshotting** | Operations runbook says clean up after incident | Primary evidence destroyed; attack vector becomes unprovable |
| **Rotating credentials before capturing scopes and retrieval trace** | Standard IR reflex applied without considering the workflow context | Cannot prove what the agent could do or what content drove the action |
| **Trusting only chat-UI injection testing in pre-production** | Pen test scope based on familiar attack patterns | Misses the dominant attack surface; production agents fail on day one |
| **Adding "ignore injection attempts" to the system prompt and calling the problem solved** | Prompt engineering feels like a control | Theatrical safety; the architectural surface remains; the next injection variant bypasses the prompt rule |
| **Treating the model's response as the attack** | The output is what the responder sees first | The response is the symptom; the input vector is the attack; remediation aimed at outputs misses the source |
| **Allowing external content to directly invoke Tier-2 tools** | Convenience during prototyping; the agent appears more useful | Direct compromise vector; every injection succeeds against the highest-impact tools |
| **No trust labeling on retrieved content** | The retrieval pipeline was built for relevance, not provenance | Cannot distinguish system instructions from injected instructions at the prompt-assembly layer |
| **Reviewer approves Tier-2 calls without seeing source content** | UI shows the action, not the prompt context | Approval gate is theatrical; reviewer is rubber-stamping calls without judgment |
| **Vendor copilots assumed to handle injection internally** | Vendor marketing claims robust safety | Vendor controls are vendor-side; customer's deployer obligations apply to the customer's data the vendor's agent consumes |
| **Detection only on output, not on retrieval** | Output monitoring is the easier instrumentation | The injection enters through retrieval; output detection fires after the action has occurred |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 Inventory extends to documenting the content channels each agent consumes.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clause 3 (Retrieves) is the load-bearing discipline for workflow-injection defense. Clause 1 (Acts) is what makes the injection harmful.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Workflow-injection defense maturity tracks the architectural guardrails, not the prompt-engineering effort.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). Workflow-injection incidents that reach external recipients or regulated data trigger the convening protocol regardless of containment mode.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M3-Workflow variant introduced in this playbook pauses content-channel ingestion while preserving the agent's other capabilities.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). Type C (retrieval traces) is the load-bearing evidence type for this playbook.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The `retrieval` and `tools` sections document the content channels and the tool wrappers this playbook hardens.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The tier discipline that determines which tools require human approval following retrieval of untrusted content.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook the workflow-injection response operationalizes.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). The seven-component retrieval pipeline this playbook depends on for forensic depth.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The architectural discipline this playbook applies to workflow-injection defense.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). The credential-snapshot sequence required if M4 Full Disable is invoked.
- **Playbook 08: Multi-Agent Systems Multiply Blast Radius** ([`playbooks/08-multi-agent-blast-radius.md`](08-multi-agent-blast-radius.md)). The cascade containment when workflow injection propagates through an agent topology.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The detection rules that catch workflow injection: retrieval-dominance, novel-corpus access, output anomalies.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). The agent-as-insider scenario where workflow injection drives sustained misuse rather than a single harmful action.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA that workflow-injection hardening inherits.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MAP 2.3, MEASURE 2.7, MANAGE 2.4, MANAGE 4.1).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports PR.DS-01, DE.AE-02, DE.AE-03, RS.AN-03, RS.MI-01).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the direct operational response for ASI01 Agent Goal Hijack and ASI06 Memory & Context Poisoning, and the response-side complement for ASI02 Tool Misuse).
- **OWASP Top 10 for LLM Applications (2025.1):** LLM03 Supply Chain (vector for injection via compromised content sources), LLM04 Data and Model Poisoning (training-time analogue of workflow injection).

## The Question to Carry Forward

If someone embedded harmful instructions in a support ticket today, then waited for your highest-impact production agent to read it as part of normal triage, could your team identify the source artifact, trace the agent's retrieval chain to the harmful chunk, prove which tool calls the agent attempted, and demonstrate that the architectural guardrail prevented the most consequential action? Answer the question for the one agent that scares you most. The answer reveals whether your workflow-injection defense is real or aspirational.

If the answer is improvised, PB06 is the work plan. Document the content channels the agent consumes this week. Verify that external content cannot directly invoke Tier-2 tools this month. Run an injection drill against the source-preservation sequence this quarter. Then move to the next agent in the inventory.

That is how workflow-injection defense moves from documented to demonstrated. One agent, one content channel, one architectural guardrail at a time, on a cadence that holds.

---

*Source: AI IR Overlay newsletter, Issue #6, "Rethinking Prompt Injection: A Workflow Threat," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
