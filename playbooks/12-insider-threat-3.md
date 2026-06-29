<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 12: Insider Threat 3.0 (AI-Driven Misuse)                    -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                  -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0. See LICENSE file in this package.                -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The insider threat playbook for the AI agent era. The credentials are legitimate. The behavior looks normal. The misuse runs at 100× the scale. Capability is not intent, and the response framework must separate them.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 12: Insider Threat 3.0 (AI-Driven Misuse)

> *Insider Threat 1.0 was the disgruntled employee with credentials. Insider Threat 2.0 was the user with anomalous behavior. Insider Threat 3.0 is the AI agent with legitimate credentials performing expected actions for unintended purposes, or the human using an AI agent to execute insider misuse at scale that previously took weeks.*

## Premise

Twenty-five years of insider threat programs taught security teams how to catch humans abusing credentials. The programs were built around three patterns that AI agents break.

The first pattern was **operational friction**. Bulk searching, aggregation, and exfiltration took time, attention, and visible effort. DLP, UEBA, and SOC dashboards were tuned to the resulting patterns: large queries, multi-step exports, after-hours access. AI agents remove that friction. *"Summarize every contract that mentions termination for convenience"* compiles in seconds what previously took a paralegal weeks. The action does not require malicious code, technical expertise, or visible effort. It looks like a normal business request, while quietly producing the kind of dataset that previously tripped every DLP rule on the network.

The second pattern was **identity-as-actor**. Insider threat programs assumed a human at the keyboard. UEBA models built behavioral baselines on user accounts and flagged deviation. AI agents change that assumption. The credentials are the user's. The session is the user's. The audit logs attribute the action to the user. But the prompt that drove the action came from the user. The interpretation came from the agent. The retrieval scope came from the agent's tooling. The output destination came from the agent's defaults. **The agent is a mediator between intent and action, and traditional insider programs do not model the mediator.**

The third pattern was **drift over time**. Insider risk programs typically watched users for sudden behavioral changes. AI agents drift gradually. Memory accumulates context the user did not explicitly authorize. Tool authorizations granted for project A get used for project B. System prompts edited months ago shape behavior nobody currently audits. The agent's effective behavior on June 27 is not the behavior shipped on March 1, and no insider threat program is configured to notice that drift unless something dramatic happens.

This is **Insider Threat 3.0**, and the response framework must change with it. The framework addresses two concrete scenarios that the prior insider threat generations conflate or miss entirely:

- **The human-with-agent insider:** a user with legitimate access uses an AI agent to compile, summarize, or exfiltrate data at a scale or with a discretion that bypasses traditional DLP and UEBA controls. The credentials are legitimate. The user is authorized. The agent multiplies the impact.
- **The agent-as-insider:** the AI agent itself, through drift, compromise, or prompt injection, performs actions misaligned with current organizational intent. The credentials are legitimate. The behavior is statistically within the user's normal patterns. UEBA fires no alerts. Yet the agent is operating against intent.

Both scenarios require the same investigative discipline: separate **capability** from **intent** from **impact**. Investigate each independently. Do not conflate "the agent could do X" with "the user wanted X" with "X actually caused harm." Most insider threat investigations fail at this triad.

**Mental Model clauses engaged:** *Acts* (primary). The agent operates inside the user's authorized perimeter; its tool list is a delegated extension of the user's privileges. *Remembers* (secondary). Memory accumulates context the user did not explicitly authorize, and that context shapes the agent's behavior over time. *Retrieves* (secondary). Corpus access at agent speeds scales beyond what the user could browse manually, which is the central attack pattern for the human-with-agent scenario.

**Use this playbook when:** an AI agent is suspected of operating against organizational intent (drift, compromise, prompt injection); a human user is suspected of using an AI agent to compile or exfiltrate sensitive data at scale; UEBA flags a user as anomalous and an AI agent is involved; HR or Legal opens an investigation involving AI agent use; or [Playbook 11 (Monitoring)](11-monitoring-detection.md) detection rules fire on capability-family signals that suggest scope abuse.

## First-Hour Actions

The first hour of an Insider Threat 3.0 incident has one job that previous insider threat playbooks did not have to do: **engage HR and Legal at minute zero, not minute sixty**. AI-augmented insider cases are joint by default. Containment without HR concurrence creates remediation problems. Investigation without Legal concurrence creates discoverability problems. Both functions need to be in the room (or on the bridge) from the start.

### The 60-minute Insider Threat 3.0 triage

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Convene HR + Legal + Incident Commander + Agent Owner**, in that order. Insider cases are not security-only investigations. Document the convening time and attendees. | Incident Commander |
| 10–25 | **Classify the scenario.** Human-with-agent (the user is the suspect), agent-as-insider (the agent itself is misaligned), or undetermined (investigate both branches). The classification determines the containment response. Misclassification at this step degrades every later step. | Incident Commander + HR |
| 25–35 | **Contain the agent's access without containing the user yet.** Suspend the agent for the suspect user. Do **not** suspend the user's broader access. This preserves evidence (the user can still be observed) and follows HR/Legal protocols (suspending a user before investigation is closed creates wrongful-action exposure). | SOC + IT Operations |
| 35–45 | **Walk the [Six Triage Questions](../triage/six-questions.md) with one extension: *who prompted, and why?*** Pull the prompt history for the agent under suspicion. Identify the requesting user identity for every prompt in the suspicious window. The prompts are evidence. | Incident Commander |
| 45–55 | **Activate [Mode M2 Approvals](../kill-switches/overview.md) corpus-wide.** Every bulk read, summarize-and-compile request, and export across **all users** in the affected corpus is queued for human approval. This catches downstream copycats and gives the investigation breathing room. | Tier-1 SOC |
| 55–60 | **Snapshot the Insider-Threat Evidence Set:** A (prompts, with requesting user identity), B (tool calls), C (retrieval traces), F (downstream identity correlation). Plus the credential-event log from [Playbook 07](07-secrets-and-tokens.md) and detection records from [Playbook 11](11-monitoring-detection.md). The combined picture is the case file. | Detection engineer + Incident Commander |

**Discipline:** in single-user insider investigations, the user's identity is the case. In AI-mediated insider investigations, the **prompt** is the case. *Who asked* is the question that drives the rest. Without prompt-level identity attribution, the investigation reverts to inference.

**Critical rule from HR/Legal:** the user under suspicion is not informed of the investigation. The user is not suspended. The user is not interviewed. This is HR and Legal's call to make. Security's role in minute zero is to preserve evidence and contain the agent, not to act on the user.

## Containment Options

Containment for an Insider Threat 3.0 incident is more nuanced than other incident classes because containment affects three parties: the agent, the suspect user, and the corpus. Each requires a separate decision.

### Mode mapping for insider-threat-class incidents

| Mode | Use when | Containment scope |
|---|---|---|
| **M1 Read-Only (corpus-wide)** | The corpus is sensitive (HR records, financial data, M&A documents) and broad write access is unnecessary during investigation | All users in the corpus lose write through the AI agent. Reads continue. |
| **M2 Approvals Required (corpus-wide)** | Bulk-summarize and export requests must be gated while the investigation runs | Every Tier-2 read and write across the corpus queued for approval. This is the **default first move** for Insider Threat 3.0. |
| **M3 Tool Tiering (export/share disabled)** | The specific harm vector is distribution (the data was retrieved; the export step is where it leaves the org) | Disable export, share, and external-send tools across the agent fleet. The agent can still retrieve and summarize internally. Distribution is blocked. |
| **Agent suspended for user** | Single user is the suspect; their broader access remains for investigation visibility | The agent is unavailable to that user only. Other users continue normally. |
| **M4 Full Disable (corpus-scoped)** | Active distribution is confirmed AND HR/Legal authorize | Agent offline for the affected corpus. [Playbook 07](07-secrets-and-tokens.md) snapshot-before-revocation sequence applies for any credential rotation. |
| **M4 Full Disable (agent-wide)** | The agent-as-insider scenario is confirmed and drift or compromise is the diagnosis | Agent offline entirely. Treat as a [Playbook 11](11-monitoring-detection.md) capability-anomaly incident in parallel. |

### The classification-drives-containment principle

The first major investigative decision is which scenario you are in. The containment response differs by scenario:

| Scenario classification | Default containment | Rationale |
|---|---|---|
| Human-with-agent (drift, compromise, intentional misuse by user) | M2 Approvals corpus-wide, agent suspended for user, user NOT suspended | Preserves evidence; respects HR/Legal investigation protocols |
| Agent-as-insider (drift, compromise of agent itself, prompt injection cascade) | M4 Full Disable on agent; [Playbook 07](07-secrets-and-tokens.md) credential sequence | The agent is the entity acting against intent; containment is at the agent layer |
| Undetermined | M2 Approvals corpus-wide, no agent suspension yet, preserve both investigative branches | Cannot prejudge the case; preserve evidence for both possibilities |

Misclassification is the most common Insider Threat 3.0 failure. The detection signal (an agent doing something concerning) does not name the cause. The investigator's first job is to distinguish.

## Evidence Priorities

The Insider Threat 3.0 evidence set extends the [Minimum Evidence Set A–F](../evidence/minimum-evidence-set.md) with explicit attention to the **capability/intent/impact** investigator triad.

### The investigator's triad: separate, do not conflate

| Dimension | What it answers | Where the evidence lives |
|---|---|---|
| **Capability** | What *could* the agent do at the time of the incident? | AI-BOM `tools`, `retrieval`, and `identity` sections at incident time (Type E) |
| **Intent** | What did the requesting user *ask for*, and what was the agent's role definition? | Prompt records (Type A) with requesting user identity; system prompt and role definition; tool authorization rationale |
| **Impact** | What *actually happened* in downstream systems? | Tool-call ledger (Type B), retrieval traces (Type C), downstream SaaS audit logs (Type F) |

Conflating these dimensions is the most common investigative failure. *"The agent could do X"* is not *"the user wanted X."* *"The user wanted X"* is not *"X actually caused harm."* HR and Legal will challenge investigations that confuse the three. Anchor every finding to a specific dimension.

### Evidence priorities ranked for Insider Threat 3.0

| Code | Evidence Type | Priority | Why it matters |
|---|---|---|---|
| **A** | Prompt and Response Record | **Critical** | The prompt **is** the intent evidence. Capture verbatim with the requesting user identity attached. Without prompt-level identity attribution, the agent cannot be distinguished from the user. |
| **C** | Retrieval Traces | **Critical** | What documents the agent retrieved, with versions, scores, and corpus identity. The retrieval traces show the capability the user accessed through the agent. |
| **B** | Tool-Call Ledger | **Critical** | The actions the agent took based on the prompt. Particularly: bulk operations, export calls, and external-share calls. |
| **F** | Identity and SaaS Audit-Log Correlation | **Critical** | The downstream blast radius. Where the agent's output went after the agent produced it. |
| **E** | Configuration Snapshot | High | System prompt at incident time, role definition, tool authorization rationale. The intent vector lives here. Drift between the documented intent and the active configuration is itself a finding. |
| **D** | Memory Snapshot | High if memory `scope: shared` or `per-user` with significant retention | Memory drift contributes to rogue behavior over time. For the agent-as-insider scenario, the memory at incident time is causally relevant. |

### Insider-Threat-specific captures

In addition to A–F, capture:

- **Credential-event log from [Playbook 07](07-secrets-and-tokens.md)** for the suspect agent identity, covering the 90 days prior to incident. Scope expansions or new OAuth grants in this window are causally relevant.
- **Detection signal history from [Playbook 11](11-monitoring-detection.md)** for the suspect agent. Capability-family signals (scope expansions, new tool integrations) in the prior 90 days correlate with the rogue-agent diagnosis.
- **The agent-dependency graph from [Playbook 08](08-multi-agent-blast-radius.md)** if the suspect agent participates in a multi-agent topology. Downstream agents may have consumed the rogue output before containment.
- **Soft cap and hard cap event log** for the affected corpus. Every triggered soft cap (a summarize-and-compile that crossed the threshold) is investigative input.

**Operational requirement:** the full insider-threat evidence set must be exportable within **60 minutes** of incident declaration, with the requesting user identity correctly attributed to every prompt in the window. If the identity attribution gap exceeds 5% of prompts in the window, this is the highest-priority [Playbook 18](18-post-incident-hardening.md) hardening item from this incident.

## Recovery Sequence

Insider Threat 3.0 recovery follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **two insider-threat-specific gates** added. Both gates respect HR and Legal participation that began at minute zero.

1. **HR/Legal sign-off on remediation scope** (*insider-threat gate*). Before re-enabling the agent for the affected user pool, HR and Legal must concur on what changes (if any) to the user's access, role, or status. Security cannot make this call alone. The sign-off is documented; the decision log lives in the case file.
2. **Re-enable the agent in [Mode M1 Read-Only](../kill-switches/overview.md)** for the affected user pool. Reads continue with monitoring on every retrieval. Writes are blocked.
3. **Enable approval gates on bulk and export workflows.** Per-corpus soft and hard caps activate before re-enabling Tier-2 actions. Soft caps trigger approval; hard caps block and alert.
4. **Validate the intent-realignment gate** (*insider-threat gate*). The agent's intent vector (system prompt, role definition, tool authorization rationale) is compared against current organizational intent. Drift between the two is itself a finding. Update the AI-BOM `agent` section to reflect current intent before proceeding.
5. **Replay the triggering prompt pattern** in a sandbox. Confirm that the new soft cap, hard cap, or approval gate fires correctly. If it does not, the recovery is incomplete. Return to step 3.
6. **Re-enable Tier-2 tools incrementally**, starting with the lowest-risk export channel. Monitor every Tier-2 call for the first 14 days post-incident. Lower the [Playbook 11](11-monitoring-detection.md) detection threshold for this agent to mean + 2σ during the observation window.
7. **Resume normal operation** with elevated monitoring. Return [Playbook 11](11-monitoring-detection.md) detection thresholds to mean + 3σ only after 14 days of clean operation.
8. **Schedule the post-incident review with HR and Legal within 5 business days** per [Playbook 18](18-post-incident-hardening.md). The review covers: what happened, what hardening shipped, what policy changes (if any) are required, and what the next quarterly review will measure.

**Approver:** CISO or designated Incident Commander, with HR and Legal sign-off documented. The agent owner alone is not sufficient. The user under investigation is not consulted on re-enablement.

## Post-Incident Hardening

Insider Threat 3.0 hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion.

### Boundary 1: Role-scoped retrieval

- **AI agents must not access information the user cannot directly retrieve.** The agent's retrieval scope is bounded by the requesting user's authorization scope, enforced at the corpus layer.
- **Per-corpus access controls are wired into the agent's retrieval layer.** SharePoint, Confluence, Google Drive, and other corpora respect the user's existing access rights; the agent inherits the user's view, not a superset.
- **Tenant boundaries for customer data are absolute.** No cross-tenant retrieval through the agent. This is a hard control, not a soft cap.

### Boundary 2: Approval gates for bulk and export actions

- **Per-corpus soft caps on summarize-and-compile requests.** Examples: more than 50 documents in a single summary triggers approval; more than 100 records in a single export triggers approval. Calibrate against historical telemetry.
- **Per-corpus hard caps on export and external-share actions.** Examples: cross-domain email send is blocked unless pre-authorized; bulk attachment to external email is blocked; file-share to external tenants is blocked.
- **Every triggered soft cap and hard cap event is logged** with requestor identity, retrieval trace, intended destination, and approval decision. The log is the audit trail.

### Boundary 3: Intent documentation and drift detection

- **The agent's intent vector is documented in the AI-BOM** `agent` section: system prompt, role definition, tool authorization rationale, business owner.
- **Intent drift is reviewed quarterly.** The agent's documented intent is compared against current operational behavior. Drift between the two is a finding (per [Playbook 20](20-maturity-roadmap.md) Maturity Level 4 cadence).
- **System prompt changes require code review.** A prompt change is a deployment, not a configuration tweak. Untracked prompt changes are a containment-class finding.

### Boundary 4: HR and Legal coordination

- **HR and Legal are documented joint owners** of Insider Threat 3.0 response. Their contact paths are in the Incident Commander's first-hour runbook.
- **Drills include HR and Legal participation** at least annually per [Playbook 14](14-testing-for-agent-failure-modes.md). A drill that does not include HR/Legal is not an Insider Threat 3.0 drill; it is a security tabletop.
- **The 5-business-day hardening SLA from [Playbook 18](18-post-incident-hardening.md) applies** to insider-threat findings. HR and Legal concurrence on policy changes within the SLA.

## Common Pitfalls

These are the highest-frequency failure modes specific to Insider Threat 3.0. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Treating insider risk as access-control only** | DLP and UEBA were the legacy answers | Misses the bulk-retrieval-via-authorized-access pattern. Insider Threat 3.0 fires no DLP rules. |
| **Logging tool calls but not the requesting prompts** | The application's logging schema was designed pre-agent | Cannot prove intent. The "what was the user asking for?" question goes unanswered. |
| **No approval gate on bulk reads** | Soft and hard caps are an operational discipline, not a default | Misuse looks identical to normal work. The compounding scale advantage of AI insider misuse is fully realized. |
| **HR and Legal not engaged at minute zero** | Security tradition: secure the perimeter first, brief HR later | Investigation contaminated. HR remedies unavailable. Discoverability problems for any future action. |
| **Conflating capability and intent** | The detection signal that fires says "the agent did X" | The investigation reverts to "did the user mean it?" without evidence. HR cannot act on inference. |
| **Suspending the user at minute zero** | Security reflex when a user is suspected | Destroys evidence (the user cannot be observed). Creates wrongful-action exposure if the user is later cleared. |
| **Trusting employees as the entire control** | *"We hire good people"* | Trust is not a control. Approval gates are. AI-augmented misuse runs faster than trust-based oversight catches. |
| **No intent documentation in the AI-BOM** | The agent was built; the intent was implicit | When the agent drifts, there is no documented intent to compare against. Drift is invisible. |
| **System prompt changes happen outside code review** | The system prompt is "configuration" to engineers, not "code" | Untracked prompt changes produce silent drift. The agent on Tuesday is not the agent on Monday. |
| **UEBA modeled on humans applied to agent-mediated actions** | Existing tools, existing models | Anomalous prompts come from "normal" users; baselines look fine. The agent layer is invisible to UEBA configured for human behavior. |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 Inventory extends to intent documentation per agent.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clauses 1 (Acts) and 2 (Remembers) and 3 (Retrieves) cover the agent-mediated insider risk.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Intent drift detection is a Level 4 (Resilient) capability.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The corpus-scoped containment patterns this playbook depends on.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A–F set with capability/intent/impact priorities.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The intent vector lives here: system prompt, role definition, tool authorization rationale, business owner.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The tier discipline that supports per-corpus soft and hard caps.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The privileged-identity lens applied to the agent-mediated insider case.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). Retrieval-trace forensics for bulk-retrieval-via-summarize patterns.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The Tier-2 gating discipline behind hard caps.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). Credential-event log inputs for the agent-as-insider classification.
- **Playbook 08: Multi-Agent Systems Multiply Blast Radius** ([`playbooks/08-multi-agent-blast-radius.md`](08-multi-agent-blast-radius.md)). The dependency graph that scopes Insider Threat 3.0 across topologies.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The capability-family detection signals that trigger this playbook.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). Metric 1 (Inventory Currency) extended to intent documentation.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The drill discipline applied to Insider Threat 3.0 with HR and Legal participation.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA, with HR/Legal concurrence.
- **Playbook 20: Maturity Roadmap (Operating View)** ([`playbooks/20-maturity-roadmap.md`](20-maturity-roadmap.md)). Intent-drift detection cadence is a Level 4 capability.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MEASURE 2.7, MANAGE 2.4, MANAGE 4.3).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports PR.AT-01, RS.AN-03, RS.MA-02, RS.MI-01, GV.RR-02, ID.AM-05).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the response-side complement to [Playbook 11](11-monitoring-detection.md) for ASI10 Rogue Agents; also covers ASI03 Identity & Privilege Abuse and ASI06 Memory & Context Poisoning from the insider-misuse angle).

## The Question to Carry Forward

If an insider used your AI agent to compile sensitive data today, could you rapidly and confidently prove **who initiated** the action, **what was retrieved**, and **where the output went?** If your AI agent's behavior has drifted slightly over the last 90 days in ways that look like *"better adaptation to user needs,"* would your team recognize that as rogue agent drift, or would you celebrate it as the agent learning?

If either answer is uncertain, PB12 is the work plan. Engage HR and Legal as joint owners. Document one agent's intent in the AI-BOM this week. Establish soft caps on one sensitive corpus this month. Run an Insider Threat 3.0 drill with HR and Legal participation this quarter. Compare the agent's documented intent against its operational behavior next quarter, and treat the difference as a finding.

That is how insider threat moves from a 1.0 program (humans with credentials) through 2.0 (humans with anomalous behavior) to 3.0 (agents and humans together, with intent as the load-bearing investigative dimension). The framework's capability/intent/impact triad is the discipline that holds across all three generations.

---

*Source: AI IR Overlay newsletter, Issue #12, "Insider Threat 3.0: AI-Driven Misuse," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
