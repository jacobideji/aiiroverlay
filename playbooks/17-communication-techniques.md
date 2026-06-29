<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 17: Communication Techniques for AI-Involved IR          -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The crisis-communication discipline. Technical containment is half of an AI incident response; the other half is the communication that holds stakeholder trust through the response window. Lead with impact and containment, not speculation. Use the three-status taxonomy of Confirmed, Suspected, and Validating to discipline language. Issue the first update within 30 minutes. Pre-write templates for each stakeholder class. Reframe responsibly: "an authorized automation behaved incorrectly under investigation" rather than "the AI did it."**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 17: Communication Techniques for AI-Involved Incident Response

> *AI automation introduces new enterprise risks: unintended outputs, unauthorized operations, harm distributed through authorized channels. The response framework's technical playbooks (PB01, PB03, PB06, PB07, PB08, PB09, PB10, PB12, PB21, PB22) cover what to do operationally. None of them cover what to say. Communication failures multiply incident harm: a poorly-worded executive update breaks board confidence, a speculative external statement creates legal exposure, an internal Slack thread that anthropomorphizes the AI defeats the framework's accountability discipline, an update that arrives too late forces stakeholders to fill the gap with rumor. The communication discipline turns the response from "we contained it technically" into "we held stakeholder trust through it." Both halves of the response are load-bearing.*

## Premise

Every other playbook in this framework specifies what the response team does. PB17 specifies what the response team **says**, to **whom**, **when**, and in **what language**. Communication is not a peripheral discipline; it is the load-bearing artifact for stakeholder-trust preservation during the response window where the technical response cannot yet produce a complete answer to the questions the stakeholders are asking.

This makes PB17 operationally distinct from the rest of the framework's playbooks in four ways:

| Aspect | Technical-response playbook | Communication playbook |
|---|---|---|
| Primary artifact | Containment action, evidence capture, recovery sequence | Stakeholder-facing message, internal update, regulator notification, board briefing |
| Time pressure | First-hour discipline (the framework's First-Hour Actions) | First-30-minute discipline (the first message is more time-sensitive than the first containment action in many stakeholder views) |
| Audience | The response team itself, the IC, the operational owners | Internal executives, customers, regulators, the board, employees, the press; each a distinct audience with distinct information needs |
| Failure mode | Containment delay, evidence loss, response sequence error | Speculation that creates legal exposure, premature root-cause attribution that breaks trust, anthropomorphizing language that defeats accountability, no update for 4 hours while rumor fills the gap |

Communication failures during AI incidents have a distinctive pattern that traditional-IR communication discipline does not fully address:

- **The anthropomorphic-attribution trap.** "The AI hallucinated" / "the model decided to" / "the agent went rogue" framings hand the customer's accountability to a non-accountable actor. The accountability lives with the customer; the AI is a tool under the customer's permissions, access, and control. Framing that obscures this point fails on both ethical grounds (it misrepresents the actual responsibility chain) and legal grounds (it sets up unfavorable disclosure framing). The reframing discipline names the same incident as *"an authorized automation behaved incorrectly under investigation"* or *"a privileged AI workflow executed unintended actions"*: the customer's automation, the customer's investigation, the customer's accountability.
- **The premature-root-cause trap.** The response team's instinct under pressure to demonstrate competence is to state the cause early. The framework's [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) discipline depends on accurate scoping; a premature cause attribution that is later contradicted erodes credibility for the rest of the response window. The Three-Status Taxonomy (Confirmed, Suspected, Validating) is the discipline that prevents premature commitment.
- **The technical-detail trap.** The instinct to explain the model's internal mechanics in the first update produces messages that the non-technical audience cannot evaluate (and that the legal team cannot review for disclosure exposure on the first pass). The discipline is to lead with **impact and containment**, not internals.
- **The cadence-drift trap.** The first update is issued; the second update is "when we know more." The gap fills with stakeholder anxiety, internal rumor, and external speculation. The discipline is a stated next-update time at every update, met or proactively extended.
- **The stakeholder-class confusion trap.** A single update is drafted for "stakeholders" without recognizing that the internal executive team, the customer-facing audience, the regulator-facing audience, and the board-facing audience need materially different information at materially different cadences. A one-size message is read as the worst-case message by each audience.

Most AI incident communication failures are downstream of one of these five traps. The communication discipline's job is to make each failure mode recognizable before it lands in the outbound message.

The biggest operational problem with AI incident communication is not the writing; it is the **time pressure / accuracy / accountability triangle**. The response team has 30 minutes for the first message, 60 minutes for the materiality determination, and the rest of the day for the regulator and customer disclosures. Each of those windows compresses the time available for careful language. Pre-written templates, the Three-Status Taxonomy, and the Four-Element Update Standard exist to make accurate, accountable language fast enough to satisfy the time pressure without sacrificing either accuracy or accountability.

**Mental Model clauses engaged:** *Acts* (when communication shapes the response to actions the agent took); *Changes* (when communication addresses configuration or model changes that contributed to the incident); the discipline's principal contribution is the **accountability framing** that runs alongside every other Mental Model clause: the customer is accountable for what the customer's automation does.

**Use this playbook when:** an AI incident has been declared and the first stakeholder update is due · the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) has determined that external disclosure is required · the [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) investigation requires careful communication with HR, Legal, and the affected user · the [Playbook 21 (Shadow AI)](21-shadow-ai.md) discovery requires communication with the shadow agent's owner (as a partner, not a suspect) · the [Playbook 22 (Drift)](22-model-policy-drift.md) change-event response requires communication with the change-pipeline owner and downstream business owners · the customer has been contacted by a regulator, an auditor, or the press about an AI incident · the [Playbook 24 (Board-Ready Scorecard)](24-board-ready-scorecard.md) quarterly review or an out-of-cycle board briefing on AI risk posture is being prepared · the [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) drill includes a communication exercise.

## First-Hour Actions

PB17's First-Hour Actions are tightly time-boxed because stakeholder-trust preservation is most sensitive to delay in the first 30 to 60 minutes. The discipline is parallel to the operational First-Hour Actions in the technical playbooks: communication runs alongside containment rather than after it.

### The 60-minute communication triage

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Confirm the stakeholder classes affected and the disclosure-window status.** Document which audiences need an update in this incident (internal executive team, internal IT/business teams, affected end-users, customers, regulator, board, press, employees broadly). Each class has a different first-update cadence, different content scope, and different approval path. Confirm whether any external disclosure window has started clock per [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md): SEC Item 1.05 (4 business days from materiality determination), GDPR Article 33 (72 hours from awareness of personal-data breach), HIPAA (60 days from discovery of breach affecting 500+ individuals), state breach-notification laws (varies, often without delay or specific deadlines), customer contractual disclosure (per customer contract terms). | Incident Commander + Legal + Communications |
| 10–20 | **Pull the relevant pre-written template per stakeholder class** from the customer's [Template Library](#the-template-library) (see Evidence Priorities below). Each template is a starting structure, not a final message; the discipline is to customize from a calibrated baseline rather than to draft from scratch under time pressure. | Communications + IC |
| 20–25 | **Apply the Four-Element Update Standard** to the first stakeholder message: factual impact statement, immediate containment controls activated, evidence-collection activity underway, next-update timing. The standard is the structural minimum; first-update messages that omit any of the four elements produce predictable follow-on questions that the next update must address. | IC + Communications |
| 25–30 | **Apply the Three-Status Taxonomy.** Every claim in the message is tagged with status: **Confirmed** (verified through direct evidence), **Suspected** (plausible based on the agent's documented capabilities and the surfaced behavior, but not yet evidenced), **Validating** (evidence collection and analysis underway, expected resolution in stated timeframe). Claims without a status tag are removed; speculative claims are explicitly tagged Suspected. | IC + Communications + Legal |
| 30 | **First update issued to the highest-priority stakeholder class.** For internal stakeholders this is typically the executive team and the affected business owners. For external stakeholders the first update is the regulator (where the disclosure window has started) or the affected customers (where customer-trust preservation is the highest priority). The discipline is to issue something accurate at 30 minutes rather than the perfect message at 90 minutes. | IC |
| 30–45 | **Apply the Responsible Reframing discipline** to subsequent message drafts. Replace anthropomorphizing language ("the AI decided", "the model hallucinated", "the agent went rogue") with system-accountability language ("an authorized automation behaved incorrectly under investigation", "a privileged AI workflow executed unintended actions", "the agent operating under the customer's permissions performed unexpected actions"). The reframing serves the customer's accountability posture and the regulator's expected framing. | Communications + Legal |
| 45–55 | **Draft and queue the second update for each stakeholder class** using the stated next-update times from the first updates. The cadence is the discipline; an update at the stated time (even if the message is "investigation continues, next update in 60 minutes") is materially better than silence. | Communications |
| 55–60 | **Verify the decision log captures every communication decision.** What was said, to whom, when, under whose authority, with which approver. The decision log itself is evidence per [Playbook 15 (Records, Retention)](15-records-retention.md). | IC + Evidence custodian |

**Discipline:** the 30-minute first-update SLA is the most important discipline in this playbook. Silence in the first 30 minutes is interpreted by stakeholders as either *the team has not noticed* or *the team is hiding something*; neither is the reputational outcome the customer needs. The first update can be brief and explicitly preliminary; it cannot be absent.

**Critical rule:** every external statement is reviewed by Legal before issuance during an active incident. The discipline is not bureaucratic; speculative external claims have created material legal exposure in past incidents that more deliberate language would have avoided. Pre-written templates are pre-approved at design time; customizations during incident response are reviewed at issuance time. The two-pass discipline (pre-approved structure + incident-time customization review) is the operational compromise between speed and review.

## Containment Options

PB17 does not introduce a new kill-switch variant because communication is a discipline, not a containment surface. The framework's existing [Kill-Switch Modes](../kill-switches/overview.md) apply unchanged to the operational containment. PB17's containment-equivalent discipline is the **information-scope containment**: the actions that bound what is communicated externally while the response proceeds.

### Information-scope containment

| Action | Use when | What changes |
|---|---|---|
| **Status taxonomy enforcement** | The response team's draft messages contain unhedged claims that exceed the available evidence | All claims are re-tagged with Confirmed, Suspected, or Validating per the Three-Status Taxonomy; unhedged claims either acquire a status tag or are removed from the message |
| **Spokesperson channeling** | Multiple internal voices are responding to external inquiries without coordination | A single designated spokesperson (typically the CISO or the IC for technical questions; the Communications lead for press; Legal for regulator) is the sole external voice for the incident; other team members are explicitly briefed not to comment |
| **Pre-approval gate activation** | An external statement is being drafted under time pressure and the standard pre-approval flow is too slow | The two-pass discipline activates: pre-written template structure is the pre-approved baseline; the incident-specific customization is reviewed at issuance by Legal and the IC; the review is an explicit step rather than an implicit one |
| **Update cadence commitment** | Stakeholders are filling silence with rumor or external speculation | The next update time is named in every issued message and is met without exception; an update that arrives at the stated time even with limited new content (*"investigation continues, next substantive update in 60 minutes"*) is materially better than missing the stated time |
| **Reframing pass** | Draft messages contain anthropomorphizing language that defeats the customer's accountability posture | Every message is run through the Responsible Reframing discipline before issuance: "the AI" becomes "the agent operating under the customer's permissions"; "the model" becomes "an authorized automation"; "the agent decided" becomes "the workflow executed" |
| **Stakeholder-class scoping** | A single message is being drafted for multiple stakeholder classes (internal exec, customer, regulator, board) and the lowest-common-denominator content is producing a message that satisfies none | Per-stakeholder-class messages are drafted from per-class templates; the per-class messages may share factual content but differ on scope, depth, framing, and call-to-action |

The six actions are complementary, not exclusive. A complex incident may use status taxonomy enforcement, spokesperson channeling, pre-approval gate activation, update cadence commitment, reframing pass, and stakeholder-class scoping all in parallel, depending on the specific failure modes the draft messages exhibit.

## Evidence Priorities

PB17's evidence discipline operates at two levels: the **Stakeholder Communication Matrix** that names each audience and the calibrated communication artifact for each, and the **Template Library** that pre-positions the customer's per-stakeholder-class communication assets so they are available under time pressure rather than drafted from scratch.

### The Stakeholder Communication Matrix

Each stakeholder class has a defensible information need, a calibrated first-update cadence, and a load-bearing content scope. The matrix names each explicitly so the customer's communication discipline operates from a shared structure rather than per-incident improvisation.

| Stakeholder class | First-update cadence | Content scope | Authoring + approval |
|---|---|---|---|
| **Internal executive (CEO, COO, GC, CFO)** | 30 minutes from incident declaration | Confirmed impact statement; immediate containment activated; evidence-collection underway; next-update time; the executive's specific action item if any (typically "no action required at this time; awaiting next update") | IC drafts; CISO reviews; the executive receives directly (not through chain) |
| **Internal business owners (the agent's owning team)** | 30 minutes from incident declaration | Same factual baseline as executive; plus the operational impact on the business owner's domain; plus the IC's specific request of the owner (e.g., *"please pause the marketing-automation pipeline this agent feeds"*) | IC drafts; Communications reviews; owner receives directly |
| **Affected end-users (employees if internal-facing agent; users if customer-facing)** | 1 to 4 hours from incident declaration depending on user-facing impact; the framework's recommendation is to err on the side of earlier rather than later when the user-facing impact is material | Plain-language description of what the user may have observed; what the customer is doing about it; what the user should do (or explicitly: *"no action required from you at this time"*); next-update time | Communications drafts; IC reviews factual claims; Legal reviews for disclosure exposure |
| **Customers (external)** | Per customer contract terms, typically 24 hours from confirmed material-impact determination | Confirmed impact scope; the customer's specific exposure if individualized; the customer's accountability framing per the Responsible Reframing discipline; what the customer is doing; next-update time | Communications drafts; Legal reviews for disclosure exposure; executive approves issuance |
| **Regulator** | Per regulatory disclosure window: SEC Item 1.05 (4 business days from materiality determination), GDPR Article 33 (72 hours from awareness of personal-data breach), HIPAA (60 days for breaches affecting 500+ individuals), state breach-notification laws (varies, often immediate) | Per regulatory disclosure standard (each regulator has a specific form, content scope, and channel) | Legal drafts; Communications reviews factual claims; CISO and senior executive approve issuance |
| **Board of directors** | Per the board's calibrated incident-notification standard (commonly material-incident notification at the time of materiality determination; routine incident reporting in the quarterly board briefing per [Playbook 24](24-board-ready-scorecard.md)) | The framework's Six Metrics values for the incident; the materiality determination; the disclosure determinations and their basis; the operational posture going forward; the requested board action if any | IC and CISO co-draft; Legal reviews; CEO or CISO presents |
| **Press / public** | Reactive (in response to a media inquiry) or proactive (in response to a public exposure that will be reported regardless) | The minimum factually accurate statement; the customer's accountability framing; explicit hand-off to the customer's standard press response process; explicit refusal to speculate | Communications drafts; Legal reviews; designated spokesperson (typically the CCO, GC, or CEO depending on incident severity) is the sole external voice |
| **Employees broadly (not just affected)** | Per the customer's internal-communication standard, typically following the external announcement so employees are not surprised by external coverage that mentions the customer | Plain-language description; the customer's accountability framing; what the employee should know; what the employee should not do (typically: *"please refer external inquiries to Communications; please do not comment on social media about the incident"*) | Communications drafts; IC reviews; CHRO or CCO approves issuance |

The matrix is the structural input for the Template Library; each row produces one or more pre-written templates.

### The Template Library

The Template Library is the customer's pre-positioned communication asset that operationalizes the Stakeholder Communication Matrix. Templates are designed at peace time, reviewed by Legal and Communications, and pre-approved for structure and language; incident-time customization fills in incident-specific facts within the pre-approved structure.

#### Core template set

The framework's recommended minimum Template Library includes:

1. **Internal Executive Update Template (5-bullet format).** Used for the first executive update at 30 minutes and for subsequent cadence updates. Five bullets: confirmed impact; safe mode and containment status; evidence-export status; materiality and disclosure determination status; next update time.
2. **Internal Business-Owner Update Template.** The executive template plus an explicit owner action item or a "no action required at this time" statement.
3. **External Customer Statement Template.** Brief, factual, focused on containment. The customer's accountability framing. No technical model details. Next-update time.
4. **Regulator Disclosure Template Set.** One template per applicable regulatory regime (SEC, GDPR, HIPAA, state breach-notification, sector-specific regulators per the customer's scope). Each template is the regulator's required form structure with placeholders for incident-specific facts.
5. **Board Briefing Template.** The PB24 Six-Metric-aligned briefing structure with placeholders for the incident's specific metric values and posture statement.
6. **Press Response Template (Reactive).** The minimum factually accurate response to a media inquiry, with the spokesperson designation and the customer's no-speculation policy.
7. **Employee Broadcast Template.** Plain-language description, customer's accountability framing, employee guidance ("refer external inquiries", "do not comment on social media").

#### Template discipline

Each template:

- Names the **stakeholder class** explicitly so the customer's response team selects the correct template under time pressure.
- Names the **first-update cadence** so the response team knows the SLA the template is calibrated against.
- Specifies the **mandatory elements** (the Four-Element Update Standard for first updates; the variations for subsequent updates).
- Specifies the **placeholder fields** that the response team fills in with incident-specific facts (the impact statement, the containment controls, the evidence-collection status, the next-update time, the materiality determination).
- Specifies the **forbidden phrases** that the response team must remove if they appear in a draft (anthropomorphizing language; premature root-cause attribution; technical model internals; blame attribution to external actors without evidence).
- Specifies the **approval path** for issuance (who reviews; who approves; who signs).

Templates are version-controlled per the framework's [Playbook 22 (Drift)](22-model-policy-drift.md) discipline; template changes are deployment events with the same review cadence as production policy changes.

### Communication-evidence captures

Beyond the Stakeholder Communication Matrix and the Template Library, PB17's evidence priorities include:

- **The decision log of communication decisions.** Every message, to whom, when, with which approver, drafted from which template, with which customizations. The decision log enters the framework's evidence chain per [Playbook 15](15-records-retention.md) as a Type B equivalent for the communication track.
- **The issued-message archive.** Each issued message is preserved in its exact issued form with timestamp, recipient class, and the approver chain. The archive supports post-incident retrospective and regulator review.
- **The inbound-inquiry log.** External inquiries received during the response window (from press, customers, regulators, affected users) are logged with the inquiry, the responder, the response, and the timestamp. The log supports the customer's spokesperson-channeling discipline and the regulator's ability to verify the customer's response process.
- **The communication-drill artifacts** from the customer's [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) drill cadence: the practice messages, the time-to-first-update measurements, the template-application accuracy, the Three-Status Taxonomy adherence. The drill artifacts are the empirical baseline that supports the customer's communication-discipline posture claim.

**Operational requirement:** the first stakeholder update must issue within **30 minutes** of incident declaration. The Template Library must be locatable and applicable within 5 minutes of the IC's request; templates that require 15 minutes to find or 20 minutes to customize do not satisfy the SLA. The Reconstructability Test from [Playbook 15](15-records-retention.md) and the Communication Drill from [Playbook 14](14-testing-for-agent-failure-modes.md) are the empirical validations of the customer's communication posture.

## Recovery Sequence

PB17 recovery addresses three scenarios: restoring stakeholder trust after a communication misstep, restoring the communication discipline itself after a process failure, and restoring the customer's brand and credibility after an externally-visible AI incident.

### Path 1: Restore stakeholder trust after a communication misstep

A failure mode: a draft message issued externally contained a premature root-cause attribution, anthropomorphizing language, or an unhedged claim that later evidence contradicts. The recovery sequence:

1. **Acknowledge the misstep explicitly.** A correction that acknowledges the prior message's inaccuracy is materially more credible than a silent revision. The acknowledgment is brief, factual, and applies the Three-Status Taxonomy to the corrected claim.
2. **Re-issue the corrected message** through the same channel as the original. Customers, regulators, and the press should encounter the correction in the same place they encountered the original.
3. **Apply the Responsible Reframing discipline** to the correction itself. The correction is also an opportunity to demonstrate the customer's accountability posture; framing the correction with system-accountability language reinforces the discipline.
4. **Document the misstep in the decision log.** What was said, why it was inaccurate, what was corrected, what the customer's process change is to prevent recurrence. The decision log is part of the post-incident retrospective.
5. **Brief the affected stakeholders directly** where the misstep is significant. A direct executive call to the affected customer, regulator, or board member that the misstep occurred and the correction has been issued is materially more effective than passive re-issuance.

### Path 2: Restore the communication discipline after a process failure

A failure mode: a quarterly retrospective or a post-incident review surfaces that the customer's communication discipline was not adhered to during a recent incident (first-update SLA missed, template not used, Three-Status Taxonomy not applied, spokesperson channeling broken). The recovery sequence:

1. **Inventory the discipline failures.** Document each failure mode that occurred and the operational pressure that produced it. The inventory is the input for the corrective design.
2. **Distinguish design failures from execution failures.** A design failure is a template that did not exist or a discipline that was unclear; the corrective is to add the missing template or clarify the discipline. An execution failure is a present template not used or a clear discipline not followed; the corrective is training and drill cadence.
3. **Update the Template Library and the discipline documentation.** The corrective design is reflected in the customer's communication-discipline artifacts.
4. **Run a communication drill** per [Playbook 14](14-testing-for-agent-failure-modes.md) within 30 days of the retrospective. The drill validates that the corrective design works under time pressure; a corrective that passes the retrospective but fails the drill is not yet complete.

### Path 3: Restore brand and credibility after an externally-visible AI incident

A failure mode: an AI incident has resulted in significant external coverage (press, social media, customer escalation, regulator scrutiny) and the customer's brand and credibility are materially affected. The recovery sequence:

1. **Engage the customer's standard reputation-recovery process** (typically owned by the Chief Communications Officer and informed by the Chief Marketing Officer, the General Counsel, and the CEO). PB17's role is to integrate the AI-specific accountability framing and the framework's response posture into the broader reputation-recovery effort.
2. **Position the customer's response framework as the credibility anchor.** A customer that can demonstrate the framework's adoption (the AI-BOM, the Kill-Switch ladder, the Six Metrics, the Reconstructability Test, the Multi-Stakeholder Governance Matrix from [Playbook 23](23-logging-privacy.md)) has a defensible posture even after a visible incident. The framework is the customer's *"this is how we are responsible about AI"* story.
3. **Run an explicit lessons-learned communication** to affected stakeholders (customers, regulators, board) that names the specific hardening items the customer has implemented per [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) and the timeline. The lessons-learned communication is itself a credibility artifact when handled with the framework's accountability discipline.
4. **Brief the customer's broader employee base** on the framework's response posture so internal credibility is preserved alongside external credibility. Employees who do not understand the framework cannot defend the customer's response in their own conversations.

**Approver for recovery actions:** Path 1 and Path 2 recoveries are approved by the IC and the Communications lead; Path 3 recovery is approved by the CEO, the CCO, and the General Counsel. The discipline is the same four-eyes principle from [Playbook 15](15-records-retention.md): communication recovery decisions affect every stakeholder class and warrant senior-leader review.

## Post-Incident Hardening

PB17 hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert AI-incident communication from a per-incident scramble into a continuous discipline that the customer's stakeholders can rely on.

### Boundary 1: The Template Library codified and rehearsed

- **The Template Library exists, is version-controlled, and is locatable within 5 minutes** of the IC's request. A library that requires 15 minutes to find does not satisfy the first-update SLA.
- **Every template is reviewed annually by Legal and Communications** for accuracy, regulatory alignment, and language calibration. Templates that have not been reviewed in the past 12 months are findings.
- **The Template Library is tested in the [Playbook 14 (Testing)](14-testing-for-agent-failure-modes.md) drill cadence.** Each quarter, one drill includes a communication exercise; the drill measures time-to-first-update, template-application accuracy, and Three-Status Taxonomy adherence.
- **The library covers all stakeholder classes from the Communication Matrix.** A customer with a customer-facing AI agent but no External Customer Statement Template is not yet at framework conformance for PB17.

### Boundary 2: The Three-Status Taxonomy embedded in IR discipline

- **Every IR-team member is trained on the Three-Status Taxonomy.** The taxonomy is the team's shared vocabulary for incident claims; the training is part of [Playbook 16 (Training)](#related) when shipped, or part of the customer's IR-training discipline in the interim.
- **The taxonomy is enforced in the response team's internal communication during active incidents.** Internal Slack threads, IR channel updates, and IC briefings use the same taxonomy as external messages. The discipline is consistent across internal and external surfaces because mixed discipline produces leakage.
- **Each incident's decision log records the taxonomy application** per [Playbook 15](15-records-retention.md). Claims tagged at the wrong status (Confirmed when only Suspected was warranted) are themselves findings in the post-incident retrospective.

### Boundary 3: The Responsible Reframing discipline as cultural artifact

- **The customer's IR culture treats anthropomorphizing language as a defect to be corrected.** The discipline is not punitive; it is the same discipline as removing speculation or unhedged claims from a draft message.
- **The reframing examples are part of the customer's IR training and onboarding** so new team members acquire the discipline from the start.
- **The reframing discipline applies to internal communication as well as external.** Internal Slack threads, IR channels, and executive briefings that anthropomorphize the agent are corrected in real time. The cultural posture compounds across incidents.
- **The reframing pattern is documented with the customer's specific examples** drawn from the customer's actual deployment. Generic reframing examples are starting points; the customer's mature discipline is calibrated to the customer's specific agents and incident classes.

### Boundary 4: The Communication Drill cadence

- **A communication drill runs at least quarterly** per [Playbook 14](14-testing-for-agent-failure-modes.md). The drill is a tabletop or live exercise that simulates an AI incident's communication track from the 0-minute incident declaration through the 4-hour materiality determination and the regulator/customer disclosure issuance.
- **Each drill measures:** time-to-first-update (against the 30-minute SLA), Template Library locate-and-customize time (against the 5-minute baseline), Three-Status Taxonomy adherence (every claim correctly tagged), Responsible Reframing adherence (zero anthropomorphizing language in issued messages), cadence adherence (every stated next-update time met).
- **Drill findings enter the [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) 5-business-day SLA backlog.** A missed first-update SLA in the drill becomes a 5-business-day corrective item.
- **Drill maturity progresses across quarters.** Early drills focus on internal-executive and internal-business-owner communication. Subsequent drills add external customer, regulator disclosure, board briefing, and press-response scenarios. The progression matches the [Maturity Roadmap](../framework/03-maturity-roadmap.md) level progression.

## Common Pitfalls

These are the highest-frequency failure modes in AI-incident communication. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Anthropomorphic attribution ("the AI did it")** | Surface language describes the agent as an actor; under time pressure the same language reaches external messages | The customer's accountability posture is undermined; legal exposure increases; the regulator's expected framing is contradicted; the framework's accountability discipline is defeated |
| **Premature root-cause attribution** | The response team's instinct under pressure is to demonstrate competence by stating a cause | The cause attribution is contradicted by later evidence; the customer's credibility for the remaining response window is materially diminished; correction itself becomes a communication event |
| **Lead with technical model details** | The technical team drafts the first update from technical-team perspective | Non-technical audiences cannot evaluate the message; Legal cannot review for disclosure exposure on the first pass; the impact-and-containment substance is buried in technical detail |
| **No first-update SLA** | The customer's communication discipline does not name an explicit time-to-first-update target | The first update slides to 90 minutes, 2 hours, or later; stakeholders fill the silence with rumor; the customer's response posture is interpreted as either unaware or hiding |
| **No next-update cadence** | The first update is issued; the second update is "when we know more" | The gap between updates fills with stakeholder anxiety, internal rumor, and external speculation; subsequent updates have to address the rumor as well as the actual incident |
| **No pre-written templates** | Communication artifacts are drafted from scratch under time pressure | First-update quality is materially worse than the customer's mature template would produce; review time consumes the 30-minute SLA; the message arrives later than the framework's discipline requires |
| **Single message for all stakeholders** | The response team treats "stakeholders" as one audience | The lowest-common-denominator content satisfies none of the stakeholder classes; each class reads the message as the worst-case message |
| **Status taxonomy not applied** | The team has not internalized the Confirmed/Suspected/Validating discipline | Unhedged claims reach external messages; later corrections compound the credibility cost; the customer's response window credibility is broken |
| **Spokesperson channeling broken** | Multiple internal voices respond to external inquiries during an incident | Contradictory external statements appear; the press, the regulator, and the customer assemble a coherent narrative from incoherent sources; the customer's narrative control is lost |
| **Legal review skipped for time pressure** | The pre-approval flow is slow; the response team bypasses it | External statements create material legal exposure that more deliberate language would have avoided; the customer's posture for the disclosure obligations is compromised |
| **Decision log absent or partial** | Communication decisions are made in Slack threads that are not archived; the decision log is treated as a nice-to-have | The post-incident retrospective cannot reconstruct who said what when; the regulator's process review cannot verify the customer's discipline; the audit-defensibility of the communication track is compromised |
| **No communication drill cadence** | The customer tests technical IR but not communication IR | The first AI incident is the first time the customer's communication discipline is tested under operational pressure; the failure modes from this Pitfalls table all surface at once; the customer's posture is materially worse than the customer believed |
| **No board-briefing template** | Board communications are drafted from scratch for each material incident | Board credibility takes longer to rebuild than necessary; the customer's executive posture under board review is compromised; the PB24 scorecard's board-readiness claim is not validated |
| **No regulator-disclosure templates** | Regulatory disclosure is treated as a Legal-only activity disconnected from the broader communication track | The regulator's disclosure is inconsistent with the customer's parallel customer and press communications; the regulator notices the inconsistency; the customer's regulatory posture is compromised |
| **Internal employee broadcast skipped** | The customer focuses on external communication and treats internal employees as a downstream audience | Employees encounter external coverage of the customer's incident before the customer has communicated with them; the customer's internal credibility is materially diminished; the employees' confidence in the customer's AI posture is broken |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). PB17 is the communication-discipline overlay on the four MVO controls; every MVO control's operational use produces communication artifacts that this playbook calibrates.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). The four-clause model is the structural framework for the customer's accountability posture; PB17's Responsible Reframing discipline operationalizes the model's accountability framing in every communication artifact.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). The Template Library completeness is a Level 2 (Containable) capability; the 30-minute first-update SLA achievement is a Level 3 (Provable) capability; the quarterly Communication Drill cadence is a Level 4 (Resilient) capability.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). PB17 is the communication track that runs alongside every Materiality and Disclosure call; the disclosure determinations from the materiality framework become the load-bearing content of PB17's external communications.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The full M0-M5 ladder is the operational containment vocabulary that PB17's first updates name explicitly; the Template Library's Internal Executive Update Template includes the kill-switch mode status as a mandatory element.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A-F evidence taxonomy is referenced in PB17's first updates as evidence-collection underway; the Reconstructability Test from [Playbook 15](15-records-retention.md) is the empirical validation that the evidence claims in the communication are defensible.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The AI-BOM entry for the affected agent is the source for the impact-statement factual claims (which business owners, which connectors, which write targets); a first update that cannot cite the AI-BOM is operating with stale inventory.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook that establishes the privileged-identity lens; PB17's Responsible Reframing discipline applies the lens to communication: the agent is a privileged identity under the customer's control, not an autonomous actor.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The T0/T1/T2 tool tiering is the operational vocabulary for communication: "the agent's Tier-T2 tools have been disabled" is materially more precise than "the agent has been restricted."
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). Output-leakage incidents are particularly sensitive to communication discipline because the leak distributes through authorized channels; PB17's Stakeholder Communication Matrix and the destination-class scoping from PB09 together determine the customer's per-class communication strategy.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). Vendor-managed agents introduce a third-party communication dimension: the customer's communication and the vendor's communication must be coordinated. PB10's contracting discipline includes vendor communication coordination as a contract term.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). Insider-threat investigations carry the highest communication-sensitivity bar in the framework; PB17's spokesperson channeling, Three-Status Taxonomy, and decision-log discipline are the load-bearing artifacts for PB12's HR/Legal joint-engagement protocol.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). The Six Metrics values are the structural input for the Board Briefing Template; PB17 operationalizes the board-facing communication of the metrics.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The quarterly Communication Drill cadence lives in PB14's testing discipline; PB17 specifies the drill's content, scoring, and follow-through.
- **Playbook 15: Records, Retention, and Proving What Happened** ([`playbooks/15-records-retention.md`](15-records-retention.md)). The decision log of communication decisions, the issued-message archive, and the inbound-inquiry log are all evidence artifacts under PB15's lifecycle discipline; PB17's communication track produces evidence that PB15's retention discipline preserves.
- **Playbook 16: Training Your Team for AI Incidents** ([`playbooks/16-training-your-team.md`](16-training-your-team.md)). PB16 operationalizes the training cadence for PB17's communication discipline: the monthly micro-drill's Phase 3 (Scope and Brief) rehearses the Three-Status Taxonomy application, the Four-Element Update Standard adherence, the Responsible Reframing pass, and the Template Library lookup-and-customize sequence. PB16 and PB17 together form the **communication training pair**: PB17 specifies the discipline; PB16 trains the team to apply it under operational pressure.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to PB17 findings (Template Library gaps, missed first-update SLAs, taxonomy adherence failures, Reframing adherence failures, drill findings).
- **Playbook 21: Shadow AI** ([`playbooks/21-shadow-ai.md`](21-shadow-ai.md)). Shadow AI discovery requires careful communication with the shadow agent's owner (as a partner, not a suspect); PB17's Responsible Reframing discipline applies to the owner-engagement framing.
- **Playbook 22: Model and Policy Drift** ([`playbooks/22-model-policy-drift.md`](22-model-policy-drift.md)). Drift incidents require careful communication with the change-pipeline owner; PB17's spokesperson channeling discipline keeps the communication coordinated as the rollback proceeds. Templates are themselves PB22 configuration; template changes are deployment events with rollback capability.
- **Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World** ([`playbooks/23-logging-privacy.md`](23-logging-privacy.md)). The Multi-Stakeholder Governance Matrix's stakeholder classes (Security, Privacy, Legal, Engineering) are the same internal classes that PB17's Stakeholder Communication Matrix addresses; PB23 and PB17 share the multi-stakeholder lens.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). The Six-Metric-aligned board briefing structure is PB17's Board Briefing Template; PB24 specifies what the board sees, PB17 specifies how it is communicated.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MANAGE 4.3 incident communication to AI actors and affected communities, MANAGE 3.1 risk response with stakeholder engagement, and GOVERN 1.7 information sharing including incident disclosure).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook is the direct operational response for **RS.CO** incident communication, **RC.CO** recovery communication, and **GV.OC** organizational context including stakeholder communication; supports RS.MA-04 incident escalation discipline through the Stakeholder Communication Matrix).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses the human side of **ASI09 Human-Agent Trust Exploitation**: when AI trust is broken by an incident, the communication discipline is what rebuilds the trust through the response window; the Responsible Reframing and Three-Status Taxonomy disciplines are the trust-preservation machinery alongside the framework's technical response).

## The Question to Carry Forward

If your AI agent caused a customer-visible incident at 14:00 tomorrow, could you issue an accurate, accountable, evidence-tagged first update to the executive team by 14:30? Could you locate the appropriate template from your Template Library within 5 minutes? Could you tag every claim in the message with Confirmed, Suspected, or Validating? Could you reframe every anthropomorphic phrase to system-accountability language without slowing the response? Could you coordinate the messages to internal executives, affected customers, the regulator, the board, and employees broadly without contradicting yourself across audiences? Could you maintain the stated next-update cadence through a 6-hour response window?

The honest answer is the gap. If any of those answers is *"only for traditional IR, not AI-specific incidents"* or *"only for one stakeholder class"*, the Template Library, the Three-Status Taxonomy, the Responsible Reframing discipline, or the quarterly Communication Drill is the corresponding hardening priority.

AI incidents arrive with operational complexity, regulatory exposure, and stakeholder anxiety in the same hour. The technical response is necessary; the communication response is what determines whether stakeholders experience the technical response as reassuring or as alarming. The framework's job is not to choose between technical depth and communication clarity; it is to make both load-bearing from the first minute. When the customer's Template Library and the Three-Status Taxonomy and the Responsible Reframing discipline are operational, the communication track becomes a credibility multiplier for the technical response rather than a credibility risk that runs alongside it.

---

*Source: AI IR Overlay newsletter, Issue #17, "Communication Techniques for AI-Involved Incident Response," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
