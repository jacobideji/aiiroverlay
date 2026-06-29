<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Worked Example — Synthetic AI Incident Walkthrough                -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

# Worked Example: Synthetic AI Incident Walkthrough

> *A fictional but specific scenario showing the framework end-to-end. This is not a real incident. Use it to internalize the response arc before adopting the framework.*

This walkthrough demonstrates how the AI IR Overlay's controls work together when a real-looking AI agent incident occurs. The scenario is fictional. All organization names, ticket numbers, and customer identities are invented. The point is to show the framework operating as a coherent system, not to claim this incident actually happened.

## Scenario setup

**Organization:** *Northstar Cloud*, a fictional mid-market B2B SaaS company (1,400 employees). Customer-success operations are handled by a vendor-managed AI copilot ("Northstar Support Copilot") that triages incoming support tickets, drafts responses, and routes escalations.

**Agent inventory (from Northstar's AI-BOM):**

- **Identity:** delegated OAuth grant `svc-support-copilot@northstar.example.com`
- **Tools:**
  - `zendesk_query_ticket` (T0 read)
  - `zendesk_update_ticket` (T1 write; internal comments only)
  - `zendesk_close_ticket` (T2 write; approval required)
  - `salesforce_query_account` (T0 read)
  - `outlook_send_email` (T2 write; internal domains only, approval required for external)
- **Memory:** per-user, 30-day retention
- **Retrieval:** SharePoint corpus `support-knowledge-base`; vector store `customer-history`

**Pre-incident posture:** Northstar has adopted the AI IR Overlay through v0.14.1. They ran the 30-day [QUICKSTART](../QUICKSTART.md) on this agent two months ago. Last tabletop drill: 8 weeks ago. Last evidence export drill: 6 weeks ago. Maturity claim: Level 3 (Provable).

**Regulatory posture:** Northstar is privately held (no SEC reporting obligations), incorporated and operating solely in the United States with no EU customers or operations (no EU AI Act Article 26 deployer obligations), not a financial-services entity (no NY DFS Part 500), and not a healthcare covered entity or business associate (BAA registry empty for this agent's data scope; no PHI processed). Standard SaaS compliance posture: SOC 2 Type II audit annual; GDPR scope limited to internal employee data unrelated to this agent.

## Incident timeline

### Minute 0 (Tuesday, 10:14am): detection signal

The detection rules from [Playbook 11 (Monitoring)](../playbooks/11-monitoring-detection.md) Family 2 (influence-based) fire. The Northstar Support Copilot's retrieval traces from the last 24 hours show a single document accounting for **62%** of all retrievals across all support tickets, far above the 40% threshold per PB11.

The flagged document is a support ticket (`SUP-29481`) opened that morning by an external email address (`refunds-team@external-vendor-domain.example.net`) that is **not** in Northstar's vendor allowlist.

The alert routes to Northstar's SOC.

### Minute 5: triage call opens

The SOC analyst on duty opens a Zoom bridge with:

- Incident Commander (IC): Sarah, the on-call security engineer
- Support Operations lead (the agent's business owner)
- A platform engineer
- The CISO is paged but not yet on the bridge

Sarah opens the AI-BOM for the Support Copilot in one tab and the framework's [Six Triage Questions](../triage/six-questions.md) in another.

### Minute 8: walk the Six Triage Questions

Sarah walks the six questions in order (no skipping):

1. **What tools can the agent call?** Sarah reads from the AI-BOM `tools[]` block. Five tools, two of them T2: `zendesk_close_ticket` and `outlook_send_email`. Action surface known in under 60 seconds.

2. **What systems can it write to?** From `tools[].write_targets`: Zendesk tickets (status field) and M365 Outlook (sent items). External recipients flag is set on `outlook_send_email`.

3. **What identity does it run as?** Delegated OAuth as `svc-support-copilot`. Sarah notes this for the Identity team to query audit logs.

4. **Does it have memory? What is the scope?** Per-user, 30-day retention. Memory bleed across users is the relevant risk class.

5. **What is the least disruptive safe mode?** Sarah walks the [Kill-Switch Modes](../kill-switches/overview.md). The retrieval-dominance signal (62% from one document) suggests **workflow injection** per [Playbook 06](../playbooks/06-prompt-injection-workflow.md). The agent is consuming an unusually high volume from one source. She chooses **M3-Workflow**: pause retrieval from the affected source ticket while keeping the agent's other capabilities live so customer support continues.

6. **What is your evidence plan before you rotate keys?** Sarah opens [Playbook 03 (RAG Forensics)](../playbooks/03-rag-knowledge-base-forensics.md) for the Type C-extended capture sequence. Evidence capture starts before any cleanup.

**Discipline check:** every Six Triage answer takes under 60 seconds. The AI-BOM is current. The inventory gap is zero. The team has all the data they need to scope the incident.

### Minute 12: activate M3-Workflow

The platform engineer pauses retrieval from ticket `SUP-29481` and any documents recently created by the external email address. Other corpora (the main support KB, the customer-history vector store) remain available. The agent continues to triage other tickets in the queue.

**Time-to-Activate (TTA), per the framework definition in [`kill-switches/overview.md`](../kill-switches/overview.md):** approximately 2 minutes from the Incident Commander's order (around minute 10, after completing the Six Triage Questions walk) to mode effective (minute 12). Well within the 10-minute drill-measured target.

**Alert-to-containment latency (a distinct, complementary metric):** 12 minutes from the detection signal fire (minute 0) to M3-Workflow effective (minute 12). This is the human-mediated equivalent of [Playbook 11](../playbooks/11-monitoring-detection.md)'s sub-60-second target, which applies to automated containment pipelines. Both metrics matter: TTA measures the framework's containment-machinery readiness; alert-to-containment measures the full detection-to-response loop including human triage. The framework specifies TTA as the conformance metric because the human-triage interval is organization-specific and not framework-controlled.

### Minute 15: convene the Materiality call

Sarah confirms the agent has executed at least one tool call against the suspect content. The conditions for a [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) convene are met:

- **External recipient:** the agent attempted to send an email to a customer (caught by the approval gate before sending, but the attempt is evidence of intent)
- **Customer data exposure suspected:** the suspect ticket asks for refund details across multiple customers

Sarah pages the CISO and General Counsel. The Materiality call convenes within the 1-hour window per framework/04.

### Minute 20-45: evidence capture (parallel to containment)

While the IC and platform engineer work containment, the Identity / SaaS owners execute the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) capture in parallel:

- **Type A (Prompt/Response Record):** pulled from the model provider's logs covering the last 24 hours. Model provider TTL is 72 hours; capture before that window closes.
- **Type B (Tool-Call Ledger):** application middleware emits every attempted tool call. Captured the full ledger including the denied `outlook_send_email` call (the approval gate caught it).
- **Type C (Retrieval Traces) extended per PB03:** the seven sub-types C1-C7 captured. Document `SUP-29481` is identified in C1 (source system state) as created 18 hours before the incident by the unallowlisted external email.
- **Type D (Memory Snapshot):** captured. No customer-data bleed across users detected.
- **Type E (Configuration Snapshot):** system prompt, tool definitions, retriever settings frozen at incident time.
- **Type F (Identity and SaaS Audit-Log Correlation):** IdP logs confirm the agent's principal performed the actions; Zendesk audit logs confirm no destructive writes occurred; M365 Outlook sent-items folder confirms no email was sent.

**Time-to-Evidence (TTE):** 30 minutes from incident declaration. Well within the 60-minute drill-measured target. Maturity Level 3 (Provable) claim holds.

### Minute 60: Materiality call convenes

CISO, General Counsel, Incident Commander, and Communications lead (observer) meet over Zoom.

The Incident Commander presents:
- The Type B ledger showing the agent **attempted** an external email but the approval gate denied it. No external recipient received agent output.
- The Type F correlation showing no successful customer-data exfiltration.
- The C1 sub-type showing the suspect ticket was created externally by an unallowlisted source.

General Counsel walks the four-question materiality walkthrough:

1. **What clocks run?** Per Northstar's Regulatory posture (see Scenario setup), no statutory clock applies in this incident: not a SEC registrant (Item 1.05 not applicable), no EU operations or customers (Article 26 deployer obligations not applicable), not NY DFS-covered, BAA registry empty for this agent's data scope (HIPAA not applicable). The Incident Commander documents the Regulatory posture review as the basis for the no-clock determination.
2. **What does the evidence show?** Attempted unauthorized action; no successful action; no external recipient.
3. **Is the evidence sufficient?** Yes.
4. **What action follows?** **Outcome A: Not material.** Documented, with supporting evidence in the decision log.

**Determination time:** 28 minutes (call duration). No regulatory clock runs.

### Hour 2: containment validated, eradication begins

Sarah confirms M3-Workflow is holding (no further retrievals from the suspect ticket). The platform engineer:

- Quarantines `SUP-29481` (moves to a read-only investigation store; does not delete)
- Adds the external email address to a deny list at the ticketing system's intake
- Reviews other recent tickets from similar external addresses; finds none

### Day 1 (later afternoon): recovery sequence begins

Recovery follows [MVO-4 (Controlled Re-Enable)](../framework/01-minimum-viable-overlay.md) with PB06's workflow-specific gates:

1. Source artifact (`SUP-29481`) is quarantined, not deleted. Original is preserved as case file evidence.
2. Architectural guardrail strengthened: the tool wrapper for `outlook_send_email` now requires explicit allowlist match for external recipients, not just internal-domain filtering. Code change shipped same day.
3. Agent re-enabled in M1 (Read-Only) at 4:00pm. Confirmed reading from the main corpus, not the quarantined ticket.
4. Retrieval policy validated; content-trust labeling confirmed (untrusted external content is labeled).
5. Sandboxed replay: the original quarantined ticket is fed back to the recovered agent in a staging environment. The agent produces a draft email but the new wrapper blocks the send. Recovery validated.
6. Tier-1 tools re-enabled with caps at half pre-incident value through the next 48 hours.
7. Tier-2 tools re-enabled one at a time with approval gates active.

**M5 approver:** CISO (not the agent's business owner).

### Day 3: full operation restored, monitoring tightened

Agent returned to M0 (Observe). [PB11 (Monitoring)](../playbooks/11-monitoring-detection.md) retrieval-anomaly threshold lowered to mean+2σ for the next 14 days post-incident.

### Day 5: Post-Incident Hardening Fix List shipped

Per [Playbook 18 (Post-Incident Hardening)](../playbooks/18-post-incident-hardening.md)'s 5-business-day SLA, the Incident Commander publishes the Fix List:

- **Tool architecture:** the `outlook_send_email` wrapper now enforces external recipient allowlist in code, not in the system prompt (architectural fix, not prompt-engineering fix).
- **Content trust labeling:** tickets from non-allowlisted external sources are now labeled `untrusted-source` in the retrieval pipeline.
- **Detection thresholds:** retrieval-anomaly threshold permanently lowered.
- **AI-BOM update:** the agent's `tools[].write_targets` and `guardrails` blocks updated to reflect the new wrapper behavior. Re-validated against [`schemas/ai-bom.schema.json`](../schemas/ai-bom.schema.json).
- **Tabletop scheduled** within 30 days using the same scenario class.

**Materiality verification per PB18:** confirmed the determination was captured in the decision log. SLA clock runs (no material disclosure required, so the 5-day clock is not regulatory; it is the framework's own commitment for hardening close-out).

### Day 30: scorecard rolled up

The agent's [Playbook 24 (Board-Ready Scorecard)](../playbooks/24-board-ready-scorecard.md) row for this incident:

- **C (Containment):** GREEN. TTA 7 min, within target.
- **E (Evidence):** GREEN. TTE 30 min, within target. All six Types captured.
- **G (Governance):** GREEN. Materiality determination documented within 60 min. C3 scorecard row passes.
- **R (Recovery):** GREEN. Staged re-enable completed. Tabletop scheduled.

The incident is closed in the AI-BOM `incidents_history` block:

```yaml
incidents_history:
  - date: "2026-MM-DD"
    summary: "Workflow injection attempt via support ticket; M3-Workflow contained; no external action taken; not material"
    mode_activated: "M3-Workflow"
    duration_minutes: 145
    outcome: "passed"
```

## What this walkthrough demonstrates

This scenario shows the framework's controls operating as a system:

1. **Inventory** (MVO-1, AI-BOM) made triage answers available in under 60 seconds.
2. **Graduated safe modes** (MVO-2, Kill-Switch ladder) allowed surgical containment via M3-Workflow without taking the agent offline.
3. **Evidence preservation** (MVO-3, A-F set with Type C extended) captured the full incident timeline before any tokens were rotated or tickets cleaned.
4. **Controlled re-enable** (MVO-4) prevented re-triggering the same incident through staged recovery with sandboxed replay.
5. **Materiality protocol** (framework/04) ensured General Counsel made the disclosure determination in a documented, defensible way within the regulatory windows that could have applied.
6. **The 5-business-day Post-Incident Hardening SLA** (PB18) converted lessons into permanent guardrails by Day 5.
7. **The Six Metrics** (PB13) and the scorecard (PB24) rolled the incident up to executive posture without losing the technical detail.

## What this walkthrough is NOT

- This is **not** a real incident. The organization name, ticket numbers, and customer identities are invented.
- This is **not** a guarantee that every workflow-injection incident closes this cleanly. The scenario is designed to show the framework operating well; real incidents have more friction.
- This is **not** a substitute for adopting the framework on your own agent. Use the [QUICKSTART](../QUICKSTART.md) for that.

The point of this walkthrough is to show that the framework is a coherent system, not a list of disconnected controls. If you internalize how the controls hand off to each other across this incident, you understand the framework.

## Related

- **The Six Triage Questions:** [`triage/six-questions.md`](../triage/six-questions.md). The first-hour discipline this walkthrough operationalizes.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M3-Workflow variant used here.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A-F evidence types captured.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). The convening protocol the IC followed at minute 15.
- **Playbook 01: The Agent Is a Privileged Identity:** [`playbooks/01-agent-as-privileged-identity.md`](../playbooks/01-agent-as-privileged-identity.md). The keystone playbook this scenario consumes.
- **Playbook 03: RAG / Knowledge-Base Forensics:** [`playbooks/03-rag-knowledge-base-forensics.md`](../playbooks/03-rag-knowledge-base-forensics.md). The Type C-extended capture used at minute 20.
- **Playbook 06: Rethinking Prompt Injection as a Workflow Threat:** [`playbooks/06-prompt-injection-workflow.md`](../playbooks/06-prompt-injection-workflow.md). The scenario class this walkthrough belongs to.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents:** [`playbooks/11-monitoring-detection.md`](../playbooks/11-monitoring-detection.md). The detection rules that fired at minute 0.
- **Playbook 18: Post-Incident Hardening:** [`playbooks/18-post-incident-hardening.md`](../playbooks/18-post-incident-hardening.md). The 5-day SLA for Day 5.
- **Playbook 24: Board-Ready Scorecard:** [`playbooks/24-board-ready-scorecard.md`](../playbooks/24-board-ready-scorecard.md). The Day 30 scorecard row.

---

*Source: AI IR Overlay framework, by Jacob Ideji. Synthetic worked example, not a real incident.*
<https://www.linkedin.com/in/jacobideji/>
