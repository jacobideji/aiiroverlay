<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Materiality and Disclosure                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Convene CISO, General Counsel, and Incident Commander. Walk the determination. Document the decision. The clock has already started.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Materiality and Disclosure

Most AI agent incidents will not trigger regulatory disclosure. The ones that do operate under tight statutory clocks that start at incident detection, not at the close of investigation. This chapter establishes the convening protocol and the determination discipline that decide which clock applies and when it starts.

This is not a legal authority. Materiality determination is jurisdiction-specific, depends on facts the framework cannot know in advance, and is ultimately the responsibility of the registrant's General Counsel and audit committee. This chapter operationalizes the procedure: who is convened, what they walk through, how the decision is documented. The legal substance comes from your jurisdiction's specific regulations.

## Why this discipline matters

A publicly-traded organization that takes 8 business days to determine an AI incident is material has missed the SEC's 4-business-day window. A deployer who treats an EU AI Act Article 26(7) "serious incident" as a routine post-mortem has missed the 15-day reporting window. A covered entity that lets an AI incident's customer-data exposure age past 72 hours without notification has missed NY DFS Part 500. In each case, the disclosure failure is itself a separate violation, often more consequential than the underlying incident.

The [Six Triage Questions](../triage/six-questions.md) tell the responder what's happening. The [Kill-Switch Modes](../kill-switches/overview.md) contain the incident. The [Minimum Evidence Set](../evidence/minimum-evidence-set.md) preserves what occurred. None of those tell the CISO whether the General Counsel needs to be on the call. This chapter does.

## The convening protocol

When an incident reaches **Kill-Switch Mode M3 (Tool Tiering) or higher**, OR when any of the trigger conditions below applies, the Incident Commander convenes the **Materiality and Disclosure call** within one hour:

| Role | Responsibility on the call |
|---|---|
| **CISO** | Owns the incident's technical scope. Brings the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) snapshot and the current containment Mode. |
| **General Counsel** | Owns the disclosure determination. Brings the regulatory inventory: which regimes apply to this organization, which clocks run from which trigger. |
| **Incident Commander** | Owns the timeline. Documents who said what, when. Maintains the decision log per [Playbook 01](../playbooks/01-agent-as-privileged-identity.md). |
| **Communications lead** (observer) | Listens. Does not draft external statements until General Counsel signals the materiality determination. |

**The canonical convening trigger.** The Materiality and Disclosure call is convened when **either** of the following applies. Downstream playbooks reference this canonical list rather than restating it.

**Mode-based trigger:**

- Kill-Switch Mode M3 (Tool Tiering) or higher is activated for the affected agent

**Condition-based triggers (apply regardless of Kill-Switch Mode):**

- Customer data exposure suspected or confirmed
- External recipient of an unauthorized message (email, ticket, support response)
- Financial action executed by the agent without authorization
- Regulatory data category touched (PII, PHI, payment card data, regulated AI use case)
- Customer-facing trust impact identified (incorrect information sent externally per the CIA+T framing in [Playbook 05](../playbooks/05-executive-decision-making.md))
- Public attention (researcher disclosure, customer report, social media)
- Any incident that would be embarrassing on the front page of a financial news outlet

**The framework's convening posture is over-convene rather than under-convene.** Where a playbook's response sequence is uncertain whether to convene, the default is to convene; the materiality determination then runs through the four-question walkthrough below and may determine "not material," which is itself a documented outcome.

**The CISO does not unilaterally defer the call.** General Counsel's calendar is not a precondition. If General Counsel is unreachable, the CISO documents the unavailability and proceeds with the materiality walkthrough, then re-convenes when GC is available.

## The materiality walkthrough

The call walks four questions in order. The answers are documented in the decision log. Each answer is a finding, not an opinion.

### 1. What clock(s) run from this incident?

For US registrants: SEC Item 1.05 of Form 8-K runs 4 business days from materiality determination. The clock starts when the registrant determines the incident is material, not when the incident occurred.

For EU deployers of high-risk AI systems: EU AI Act Article 26 requires the deployer, upon identifying a serious incident, to inform the provider, distributor, and the relevant market surveillance authority without undue delay. EU AI Act Article 73 then runs against the **provider** to report the serious incident to market surveillance authorities. The reporting window under Article 73 is 15 days from awareness in the default case, 2 days for incidents resulting in the death of a person or in serious and irreversible harm, and 10 days for widespread infringement. Deployer detection effectively starts the provider's clock, so the deployer's own materiality determination timing is load-bearing for the cumulative regulatory window.

For NY DFS-covered entities: 23 NYCRR Part 500.17(a) (as amended in November 2023) requires notification to the Superintendent within 72 hours after determining that a Cybersecurity Event has occurred.

For HIPAA covered entities or business associates: 45 CFR §164.408 requires breach notification timelines that depend on the size and category.

The General Counsel names which clock(s) apply. The Incident Commander documents the start-of-clock determination separately from the incident-detection timestamp.

### 2. What does the evidence currently show?

The CISO walks the [A–F evidence set](../evidence/minimum-evidence-set.md) at its current capture state:

- **Type A (Prompt and Response Record):** what did the agent receive and produce
- **Type B (Tool-Call Ledger):** what did the agent attempt and what succeeded
- **Type C (Retrieval Traces):** what context entered the model
- **Type D (Memory Snapshot):** what state persisted
- **Type E (Configuration Snapshot):** what was the agent supposed to do
- **Type F (Identity and SaaS Audit-Log Correlation):** what actually reached downstream systems

The materiality determination is anchored to F. The agent's intent (A, B, C, D, E) is internal. Downstream action (F) is what regulators and counterparties experience.

### 3. Is the evidence currently sufficient to determine materiality?

If yes: General Counsel makes the determination. The clock starts at the determination time. The Incident Commander documents the determination, the supporting evidence, and the decision rationale.

If no: General Counsel determines what additional evidence is needed and the latest acceptable time to obtain it. The Incident Commander schedules the re-convene. **The clock is not paused by the inability to determine.** The framework's position is that materiality determination delay must itself be documented.

### 4. What action follows the determination?

Three outcomes are possible:

**Outcome A: Not material.** The Incident Commander documents the determination, the supporting evidence, and the rationale. The incident closes per [Playbook 18: Post-Incident Hardening](../playbooks/18-post-incident-hardening.md). The decision log is preserved in case of subsequent regulator inquiry.

**Outcome B: Material.** The clock runs. General Counsel notifies Communications. The disclosure is drafted to the timing window of the most-restrictive clock (typically the 72-hour NY DFS window in the US, or the 4-business-day SEC window if no DFS exposure). The Incident Commander continues incident response in parallel.

**Outcome C: Determination cannot be made yet.** Continue the incident response. Schedule the re-convene. Document the inability to determine. A registrant that determines at the next convene is not "late" provided the inability-to-determine was itself documented and reasonable.

## Where this annex is referenced from

This annex is referenced from multiple live playbooks across three roles.

**Convening role (First-Hour Actions).** Nine playbooks convene the Materiality and Disclosure call as part of their First-Hour Actions, once Kill-Switch Mode M3 or higher is reached or when any of the canonical convening triggers named in this annex applies:

- **[Playbook 01: The Agent Is a Privileged Identity](../playbooks/01-agent-as-privileged-identity.md):** the keystone response playbook.
- **[Playbook 05: Executive Decision-Making](../playbooks/05-executive-decision-making.md):** the call is convened around the Executive Decision Packet.
- **[Playbook 06: Prompt Injection as Workflow Threat](../playbooks/06-prompt-injection-workflow.md):** external recipients and regulated-data triggers are the most common condition-based triggers for workflow-injection incidents.
- **[Playbook 09: Leakage Without a Breach](../playbooks/09-output-leakage.md):** the output distribution map drives the determination.
- **[Playbook 10: Vendor Copilots and Mutual Responsibility](../playbooks/10-vendor-copilots.md):** the customer-side convening track does not wait for vendor cooperation.
- **[Playbook 15: Records, Retention, and Proving What Happened](../playbooks/15-records-retention.md):** PB15 certifies the evidence required to defend the determination.
- **[Playbook 21: Shadow AI](../playbooks/21-shadow-ai.md):** latent regulatory exposure surfaced through retrospective CIA+T assessment.
- **[Playbook 22: Model and Policy Drift](../playbooks/22-model-policy-drift.md):** the disclosure window may have started before the drift was observed.
- **[Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World](../playbooks/23-logging-privacy.md):** privacy-side disclosure obligations run alongside the standard materiality call.

**Gating role.** Two playbooks gate downstream discipline on the materiality determination:

- **[Playbook 18: Post-Incident Hardening](../playbooks/18-post-incident-hardening.md):** verifies that the materiality determination is captured in the decision log. The 5-business-day hardening SLA does not run if the materiality record is incomplete.
- **[Playbook 24: Board-Ready Scorecard](../playbooks/24-board-ready-scorecard.md):** the Governance domain item C3 confirms that materiality determination is documented for every incident reaching Mode M3 or higher.

**Referential role.** Four additional playbooks reference this annex in supporting context: [Playbook 02 (Evidence Lives in New Places)](../playbooks/02-evidence-lives-in-new-places.md) for the evidence foundation the determination depends on; [Playbook 16 (Training Your Team)](../playbooks/16-training-your-team.md) for the materiality-recognition criteria built into the team's training scope; [Playbook 17 (Communication Techniques)](../playbooks/17-communication-techniques.md) for the time-pressure / accuracy / accountability discipline the disclosure window imposes; and [Playbook 19 (Build vs Buy)](../playbooks/19-build-vs-buy.md) for the procurement-time evaluation of platform support for the materiality determination protocol.

## What this annex is not

This annex is **not** a substitute for jurisdiction-specific legal counsel. The clocks, triggers, and thresholds named here are the framework's operational discipline based on publicly-available regulation text current as of 2026. Your General Counsel reads the current regulations of your specific jurisdictions and operating contexts. The framework's contribution is the discipline of having that conversation at minute sixty rather than minute six-thousand.

## Related

- **[Six Triage Questions](../triage/six-questions.md):** the first-15-minutes discipline; the materiality call follows the triage
- **[Kill-Switch Modes](../kill-switches/overview.md):** the M3-or-higher threshold that triggers the materiality call
- **[Minimum Evidence Set](../evidence/minimum-evidence-set.md):** the A–F evidence at the determination point
- **[Playbook 01](../playbooks/01-agent-as-privileged-identity.md):** the response playbook the materiality call sits within

---

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
