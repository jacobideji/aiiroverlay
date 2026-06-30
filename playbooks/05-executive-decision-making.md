<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 05: Executive Decision-Making With AI in the Loop        -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The executive decision-making discipline. AI incidents require defensible decisions under uncertainty, before facts are complete and before the regulatory or customer disclosure window forces a commitment. PB05 specifies the Executive Decision Packet (AI Edition), the CIA+T impact framing that adds Trust as a peer dimension to Confidentiality, Integrity, and Availability, the 4/24/72-hour planning horizon for next steps, and the Approval Receipt discipline that prevents human approval from degrading into rubber-stamping. Read by executives during incidents; designed by the IC and CISO at peace time.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 05: Executive Decision-Making With AI in the Loop

> *During an AI incident, the executive team faces three converging pressures: the technical situation is unfolding, the disclosure window may already be running, and the stakeholders (board, customers, regulators, employees) are asking for an answer that the technical investigation cannot yet defensibly produce. Executives do not need the technical details that the incident commander is working through; they need a structured, AI-aware decision packet that lets them act confidently within uncertainty. PB05 specifies what that packet contains, what cadence it arrives at, what impact dimensions it covers, and what approval discipline it preserves. The Mental Model's accountability clause and the framework's response disciplines all flow through the executive layer; PB05 is how that flow becomes operationally legible to the people who must defend the customer's posture in front of the board, the regulator, and the customer.*

## Premise

Other playbooks specify what the response team does technically (PB01, PB03, PB06, PB07, PB08, PB09, PB10, PB12, PB21, PB22) and how the response team communicates (PB17). PB05 specifies how the **executive team** makes decisions during an AI incident, what information they need, in what structure, at what cadence, and under what accountability framing.

This makes PB05 operationally distinct from the rest of the framework's playbooks in four ways:

| Aspect | Technical-response playbook | Executive decision-making playbook |
|---|---|---|
| Primary audience | The IC, the on-call responder, the platform engineer | The CEO, CFO, COO, CISO, GC, CCO, CHRO, board chair, audit-committee chair |
| Time horizon | First-hour technical actions; 5-business-day hardening SLA | First-hour decision packet, 4-hour update cadence, 24-hour and 72-hour planning horizons |
| Information density | Technical-detail-rich; evidence references; tool-call ledger excerpts | Decision-relevant; business-language framing; deliberately low technical density |
| Failure mode | Containment delay, evidence loss, response sequence error | Decision under incomplete information that creates legal exposure; over-correction that compounds harm; rubber-stamp approval that defeats safety review |

AI incidents produce a distinctive executive-decision shape that traditional-IR executive briefings do not address:

- **The "is this a breach?" question is harder.** Classic breach criteria (unauthorized data access, exfiltration, credential compromise) may not apply to an AI incident that nonetheless produced material harm. The agent acted with valid credentials through legitimate APIs; the data exposure (where it occurred) came through authorized output channels; the integrity violation came through correctly-executed-but-incorrect agent actions. Executives need a framing that captures the harm without forcing it into a traditional-breach taxonomy that does not fit.
- **The "what do we tell customers?" question is more time-pressured.** Customer-trust impact may be the dominant material-harm dimension even when no traditional breach has occurred. Incorrect outputs delivered to customers, customer-facing records altered by the agent's actions, customer-visible recommendations based on poisoned context: each produces customer-trust impact that compounds with delay. PB05's 4/24/72-hour planning horizon names the executive cadence explicitly.
- **The "what are we required to disclose?" question is more ambiguous.** The framework's [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) discipline supports the materiality determination; PB05 specifies the executive packet that the determination is made from. SEC Item 1.05, NY DFS 23 NYCRR Part 500.17(a), GDPR Article 33, HIPAA breach-notification, and state breach-notification laws all have AI-incident applicability that the executive team must evaluate against an incident class that may not match any single rule's example fact pattern.
- **The "did a human approve this?" question becomes load-bearing.** When the agent's harmful action proceeded through a documented human approval, the approval itself is part of the response scope. If the human approver had inadequate context (the change preview was misleading, the destination domain was obscured, the source citations were absent), the approval is a rubber-stamp finding rather than a defensible safeguard. PB05's Approval Receipt discipline addresses this directly.

The biggest operational problem with AI-incident executive decision-making is not the absence of information; the technical team produces a great deal of information during the response. The problem is the **density mismatch**: the executive needs structured decision-support, not technical evidence narration. A 20-bullet update with retrieval-trace excerpts, configuration-diff references, and tool-call-ledger samples does not produce a defensible decision; a 5-section AI Decision Packet does.

**Mental Model clauses engaged:** all four, applied to the executive layer. The Acts clause produces the **Agent Capability Profile** section of the decision packet (what the AI could do); the Retrieves and Remembers clauses produce the **Provenance Summary** (what the AI relied on); the Changes clause produces the change-event evaluation that PB22 (Drift) operationalizes downstream.

**Use this playbook when:** an AI incident has been declared and the executive team requires the first decision packet · the Materiality and Disclosure call is convening and the convening discipline requires the executive packet structure · the customer is being contacted by a regulator, an auditor, or the press about an AI incident and the executive team requires the briefing structure to support the response · the customer's board chair, audit-committee chair, or CEO is being briefed out-of-cycle on AI risk posture · the customer is designing a new high-impact AI agent deployment and the executive approval discipline (Approval Receipt) needs to be documented before deployment · the [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) retrospective surfaces an executive-layer process failure (decisions made on incomplete information, communication misaligned with the technical track, approval that was not informed) · the [Playbook 16 (Training)](16-training-your-team.md) curriculum is being extended to include executive-layer drills.

## First-Hour Actions

The first hour of an AI incident's executive layer is time-boxed by the framework's response targets: technical containment per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) inside 10 minutes, evidence export per [Minimum Evidence Set](../evidence/minimum-evidence-set.md) inside 60 minutes, first stakeholder update per [Playbook 17 (Communication)](17-communication-techniques.md) inside 30 minutes. The executive packet runs alongside.

### The 60-minute executive triage

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Convene the executive incident channel.** The IC notifies the executive team (CEO, CISO, GC, CFO at minimum; additional executives based on incident class) of the incident declaration. The notification is structured: incident class, agent affected, initial scope, containment activated, materiality status (pending, in progress, declared), next-update time. The channel is the operational coordination surface; the formal decision packet follows. | Incident Commander + CISO |
| 10–25 | **Draft the Executive Decision Packet (AI Edition).** Five sections (see Evidence Priorities below): Situation (facts only, status-tagged per the [Playbook 17 (Communication)](17-communication-techniques.md) Three-Status Taxonomy); Agent Capability Profile (what the AI could do); Provenance Summary (what the AI relied on); Impact (CIA+T framing); Actions Taken and Next Steps (with owners, 4/24/72-hour horizons). The packet is drafted from the customer's pre-positioned [Template Library](17-communication-techniques.md) and customized to the current incident. | IC + CISO + Communications |
| 25–35 | **Apply the Three-Status Taxonomy to every claim in the packet.** Per the [Playbook 17 (Communication)](17-communication-techniques.md) discipline: Confirmed, Suspected, or Validating. The executive team is making decisions under uncertainty; the status tags name the uncertainty so the decisions can be made defensibly. Untagged claims are removed or tagged. | IC + Legal |
| 35–45 | **Convene the Materiality and Disclosure call** per [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md) if any of the convening triggers apply (customer data touched, regulated data touched, external recipients affected, financial actions involved, customer-facing trust impact identified). The Materiality call is structured around the Executive Decision Packet; the materiality determination is made with the packet as the documentation artifact. | IC + Legal + Privacy |
| 45–55 | **Issue the first Executive Decision Packet** to the executive team (CEO, CFO, COO, CISO, GC, CCO, CHRO as applicable). The packet is delivered through the executive incident channel and is logged in the customer's decision-log discipline per [Playbook 15 (Records, Retention)](15-records-retention.md) as a Type B equivalent for the executive track. | IC |
| 55–60 | **Confirm the 4-hour next-update cadence.** The next Executive Decision Packet is scheduled. The executive team understands what to expect when. Cadence missed without proactive extension is itself a process finding for the post-incident retrospective. | IC + Communications |

**Discipline:** the Executive Decision Packet is not a status report. It is structured decision-support. The packet's job is to enable the executive team to make defensible decisions about disclosure, customer communication, regulator engagement, and operational continuity. A packet that buries the decisions in technical detail produces deferred decisions; a packet that omits the technical anchors produces undefendable decisions. The 5-section structure is calibrated for both.

**Critical rule:** every Executive Decision Packet is reviewed by Legal before issuance during an active incident. The discipline is not bureaucratic; the packet's claims may be referenced in regulatory disclosure, customer communication, or downstream legal proceedings, and the Three-Status Taxonomy tags constrain the customer's later reframing options. The two-pass discipline (Template-Library structure pre-approved at design time; incident-time customization reviewed at issuance) is the operational compromise between speed and review.

## Containment Options

PB05 does not introduce a kill-switch variant because executive decision-making is a discipline, not a containment surface. The framework's existing [Kill-Switch Modes](../kill-switches/overview.md) apply unchanged to the operational containment. PB05's containment-equivalent discipline is the **decision-scope containment**: the actions that bound executive decision-making to defensible scope while the response proceeds.

### Decision-scope containment

| Action | Use when | What changes |
|---|---|---|
| **Status taxonomy enforcement on the packet** | Draft packets contain unhedged claims that exceed the available evidence | All claims are re-tagged with Confirmed, Suspected, or Validating; unhedged claims either acquire a status tag or are removed; the executive team makes decisions on tagged claims rather than implicit speculation |
| **Materiality determination scoping** | The materiality call is being convened and the determination scope is unclear | The Materiality and Disclosure call's scope is named explicitly: which incident facts, which evidence types, which stakeholder impact dimensions, which regulatory or contractual disclosure obligations. An undefined scope produces an indeterminate determination |
| **Approval-Receipt enforcement on the action plan** | The packet's "Next Steps" section includes high-impact actions that require human approval (per [PB04 Tool Tiering T2](04-tool-design-is-containment.md), [PB17 Communication](17-communication-techniques.md) external statement, financial action, customer notification) | The action is gated by the Approval Receipt discipline: the approver sees the change preview, the destination and domain, the source citations, and the object count or cap before approving. Rubber-stamp approvals are blocked structurally |
| **Two-trap callout activation** | The customer is under reputational pressure (press inquiry, customer escalation, social-media coverage) and the executive instinct is to act fast | The two reputational traps (over-correcting publicly with incomplete information; re-enabling systems without proper re-qualification) are named explicitly in the packet; the executive's decision is informed by the trap framing rather than just the current pressure |
| **Decision-log lock** | A high-impact decision is being made under time pressure and the customer's post-incident defensibility depends on the rationale being captured | The decision log records the decision, the rationale, the evidence relied upon, the alternatives considered and rejected, the approver, and the timestamp. The lock means the decision cannot proceed without the log entry; the log is part of the framework's evidence chain per [Playbook 15 (Records, Retention)](15-records-retention.md) |
| **Disclosure-window clock activation** | The Materiality determination has identified that a regulatory or contractual disclosure window has started | The clock is started explicitly with the trigger event, the window duration, and the disclosure target (SEC, state regulator, GDPR supervisory authority, HIPAA-covered-entity counterpart, customer per contract). The clock is reviewed at every Executive Decision Packet issuance |

The six actions are complementary. The discipline is to be explicit about which decision-scope containment is active and which is dormant for the current incident state.

## Evidence Priorities

PB05's evidence discipline is the **Executive Decision Packet (AI Edition)**. The packet is the operational specification for executive-layer information density during AI incidents; every section has a defined content scope, an approval path, and an integration point with the framework's broader evidence machinery.

### The Executive Decision Packet (AI Edition)

#### Section 1: Situation (Facts Only)

The packet's anchor. Plain-language statement of what is happening, status-tagged per the Three-Status Taxonomy from [Playbook 17 (Communication)](17-communication-techniques.md).

**Content scope:**
- What is happening (the surfaced behavior, the affected agent, the duration of the activity)
- When was it detected (the detection timestamp, the detection source)
- Which systems and customers are potentially affected (per the [AI-BOM](../templates/ai-bom.yaml) blast radius)
- What is **Confirmed** versus **Suspected** versus **Validating** (every claim tagged)

**Length target:** 5 to 10 bullets. The Situation section is the executive's first reading; density beyond 10 bullets defeats the structured-decision-support purpose.

#### Section 2: Agent Capability Profile (What the AI Could Do)

The "what was authorized" anchor. Defines the agent's potential blast radius from the customer's inventory rather than from inference during the incident.

**Content scope:**
- Identity: the agent's service account, delegated OAuth grants, impersonation tokens (per [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md))
- Enabled tools: especially Tier-T2 write actions per the [Privilege Matrix](../templates/agent-privilege-matrix.csv) and [Playbook 04 (Tool Design)](04-tool-design-is-containment.md)
- Systems of record with access: email, CRM, ERP, ticketing, code repositories, cloud control plane
- Memory status: off, per-user, or shared per the AI-BOM
- Connected corpora: which retrieval sources the agent can read from

**The section defines the **potential** blast radius**, not the actual exposure. The actual exposure is in Section 4 (Impact). The Capability Profile says what the agent could have done; the Impact says what evidence suggests the agent actually did.

#### Section 3: Provenance Summary (What the AI Relied On)

The "what was its context" anchor. Defines what the agent saw and what it remembered, which determines whether the surfaced behavior is isolated or systemic.

**Content scope:**
- Retrieval activity: which corpora were queried, which documents were retrieved, at which version
- Newly edited or influential documents: any document that changed in the incident window and reached the agent's context (signals corpus-poisoning per [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md))
- Signs of instruction hijack: prompt-injection indicators per [Playbook 06 (Workflow Injection)](06-prompt-injection-workflow.md); poisoned context patterns
- Memory entries created or used: the persistent context the agent carried into this interaction

The Provenance Summary tells the executive whether the harm is **isolated** (one anomalous interaction) or **systemic** (the agent's context is contaminated and other interactions are also affected). This is one of the most decision-relevant pieces of information in the packet: an isolated incident produces a different disclosure and customer-communication strategy than a systemic one.

#### Section 4: Impact (Business-Language CIA+T Framing)

The "what does this mean" anchor. Translates the technical situation into business-impact dimensions the executive team can act on.

**The CIA+T framing extends the traditional CIA triad with Trust:**

| Dimension | Question | AI-incident applicability |
|---|---|---|
| **Confidentiality** | Was any data accessed or exposed? | Per [Playbook 09 (Output Leakage)](09-output-leakage.md): leakage can occur through authorized outputs without classic breach signals; the assessment must include the output distribution map |
| **Integrity** | Were records or actions altered? | Per [Playbook 22 (Drift)](22-model-policy-drift.md) and [Playbook 06 (Workflow Injection)](06-prompt-injection-workflow.md): the agent may have written incorrect records to systems of record; the affected record count and the corrective discipline are the load-bearing details |
| **Availability** | Were operations disrupted? | The containment activation (Mode M3 or M4 per [Kill-Switch Modes](../kill-switches/overview.md)) itself produces availability impact; the assessment includes both the incident's direct availability cost and the response's cost |
| **Trust** | Was incorrect information sent externally, and to whom? | The dimension this playbook elevates to peer status. Trust impact may be the dominant material-harm dimension even when no classic breach has occurred. The assessment must identify the affected stakeholders, the scope of incorrect information, the visibility of the harm, and the trajectory of trust restoration |

The Trust dimension is the framework's recognition that AI incidents produce material harm even when the classic CIA triad shows minimal impact. A finance copilot that recommended an incorrect payment based on a poisoned invoice has produced an Integrity impact (the agent's recommendation was incorrect) and a Trust impact (the executive who acted on the recommendation has the customer's trust at stake), but may have produced zero Confidentiality impact and minimal Availability impact. A traditional CIA framing would understate the actual material harm.

**Metrology qualification (v0.33.0):** Confidentiality, Integrity, and Availability have established quantitative measurement instruments (classification levels, hash/signature checks, SLO numbers respectively). Trust at v0.33.0 is a **qualitative impact lens**, not a measurable property with peer instrumentation. The Executive Decision Packet captures Trust as the affected-stakeholder count, the identifiability scope, the externally-visible-harm flag, and the trust-restoration trajectory; these are scoping signals, not metric values. A v1.1 candidate is the operational metrology specification that would convert Trust to a measurable peer dimension (see [`CHANGELOG.md`](../CHANGELOG.md) `[Unreleased]` v1.1 backlog).

#### Section 5: Actions Taken and Next Steps (With Owners)

The "what are we doing" anchor. Defines the response's current state and the planned trajectory, with named owners for accountability.

**Content scope:**
- **Current containment measures:** what mode is active (M1 Read-Only, M2 Approvals Required, M3 Tool Tiering with variant, M4 Full Disable), what specific restrictions are in place, what the time-to-activate was
- **Evidence captured:** which of the Minimum Evidence Set A through F has been exported, gaps identified, retention extensions applied per [Playbook 15 (Records, Retention)](15-records-retention.md)
- **Planned actions over the 4/24/72-hour horizons:** the next 4 hours' technical actions (continued investigation, additional containment, evidence-gap closure); the next 24 hours' decisions (materiality determination, customer notification, regulator engagement); the next 72 hours' actions (broader hardening, public communication if applicable, post-incident retrospective initiation)
- **Assigned owners** for IR (the IC), Legal (named counsel), Communications (named CCO or designee), Operations (the affected business owner), Privacy (the DPO or equivalent per [Playbook 23 (Logging and Privacy)](23-logging-privacy.md)), and additional roles as applicable

### The Approval Receipt discipline

PB05 introduces the **Approval Receipt** as the discipline that prevents human approval workflows from degrading into rubber-stamping. Every high-impact AI action that requires human approval (per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) Tier-T2 tool tiering, [Playbook 17 (Communication)](17-communication-techniques.md) external-statement approval, [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) regulator-disclosure approval, [Playbook 19 (Build vs Buy)](19-build-vs-buy.md) procurement approval) must produce an Approval Receipt for the approver before the action proceeds.

**Required elements of an Approval Receipt:**

| Element | What the approver sees | Why it matters |
|---|---|---|
| **Change preview (diff)** | The exact action being proposed, with the before-state and after-state | The approver cannot evaluate the change without seeing the change; "approve this email send" is materially different from "approve this email send showing the diff against the agent's draft" |
| **Destination and domain overview** | Who or what receives the action's effect; for emails: the recipient list and domain classification (internal, customer-facing, external, regulated); for writes: the target system, record type, and record count | Destination classification is the load-bearing context for the approval; an internal-only action is different from an external-recipient action even when the change content is identical |
| **Source citations and provenance** | Which documents, retrievals, prompts, or prior memory entries informed the agent's proposed action | The approver can evaluate whether the agent's information sources are appropriate; an action based on a 6-month-old document or a customer-uploaded document warrants different scrutiny than one based on the customer's authoritative system of record |
| **Object count or cap** | How many objects (emails, records, transactions) the action would affect; the cap that triggers escalation | An approval for "1 email" is different from an approval for "1,000 emails"; the cap discipline prevents scope creep within an approval |

The Approval Receipt's discipline is structural rather than procedural: the approval workflow technically cannot proceed without the four elements visible to the approver. A workflow that allows approval without the receipt is itself a process finding.

### Operational requirement

The first Executive Decision Packet must issue within **60 minutes** of incident declaration. Subsequent packets follow the 4-hour cadence until the incident closes or the cadence is explicitly extended. The Approval Receipt discipline applies to every high-impact action in every packet's "Next Steps" section; an approval workflow that bypasses the Receipt discipline during an active incident is a finding for the post-incident retrospective.

## Recovery Sequence

PB05 recovery addresses three scenarios: restoring executive-layer trust after a decision was made on incomplete information, restoring the approval-receipt discipline after a rubber-stamp finding, and restoring brand and credibility after an externally-visible AI incident.

### Path 1: Restore executive-layer trust after a decision on incomplete information

A failure mode: an executive decision (disclosure, customer communication, public statement) was made on information later contradicted by evidence. The recovery sequence:

1. **Document the decision and the information state at the time it was made.** What information was available, what was tagged Confirmed, Suspected, or Validating, what evidence emerged after the decision. The documentation is honest about what was knowable and what was not.
2. **Apply the [Playbook 17 (Communication)](17-communication-techniques.md) Path 1 misstep-recovery discipline** for the external-communication dimension. The correction acknowledges the misstep explicitly rather than silently revising.
3. **Brief the executive team on the post-decision evidence.** The executive who made the decision is updated directly; the broader executive team is updated through the next Decision Packet's Situation section with explicit revision tagging.
4. **Update the customer's executive-decision-discipline artifact** if the misstep reveals a structural gap (the Three-Status Taxonomy was not enforced; the packet's Provenance section was thin; the materiality determination was made on incomplete impact scoping).

### Path 2: Restore approval-receipt discipline after a rubber-stamp finding

A failure mode: a post-incident retrospective surfaces that an approval workflow proceeded without the Approval Receipt; the human approval was therefore not informed in the way the framework specifies. The recovery sequence:

1. **Inventory the affected approval workflows.** Which workflows allow approval without the Receipt? The inventory is the corrective scope.
2. **Apply the four-element discipline to each workflow.** Change preview, destination and domain, source citations, object count or cap. Each workflow either implements the Receipt or is reclassified as a non-approval-gated workflow (which is itself a separate finding requiring evaluation).
3. **Run a [Playbook 14 (Testing)](14-testing-for-agent-failure-modes.md) drill** that exercises the Approval Receipt against a representative high-impact action; the drill validates that the corrective is operational and not just documented.
4. **Update the [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) backlog** with the workflow inventory and the corrective timeline.

### Path 3: Restore brand and credibility after an externally-visible AI incident

A failure mode: the AI incident has produced significant external coverage and the customer's brand is materially affected. The recovery sequence:

1. **Engage the customer's standard reputation-recovery process** per [Playbook 17 (Communication)](17-communication-techniques.md) Path 3. PB05's role is to integrate the executive-layer accountability framing and the framework's response posture into the broader reputation-recovery effort.
2. **Position the customer's framework adoption as the credibility anchor.** A customer that can demonstrate Approval Receipt discipline, Executive Decision Packet history, Materiality determinations made on documented evidence, and the framework's Mental Model accountability framing has a defensible posture even after a visible incident. The framework is the customer's "this is how we are responsible about AI" story.
3. **Run an explicit lessons-learned executive briefing** to the board and (where appropriate) to affected customers. The briefing names the specific PB05-discipline hardening items the customer has implemented and the timeline.
4. **Update the customer's quarterly PB24 board scorecard** with the executive-layer findings; the scorecard's Governance domain absorbs PB05 process findings as part of the customer's ongoing posture.

**Approver for recovery actions:** CEO and General Counsel for Path 1 and Path 3; CISO and IC for Path 2. The discipline is the same four-eyes principle from [Playbook 15 (Records, Retention)](15-records-retention.md): executive-layer recovery decisions warrant senior-leader review.

## Post-Incident Hardening

PB05 hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert AI-incident executive decision-making from a per-incident scramble into a continuous discipline that the customer's stakeholders can rely on.

### Boundary 1: The Executive Decision Packet codified and rehearsed

- **The Executive Decision Packet (AI Edition) template is published, version-controlled, and locatable within 5 minutes** of the IC's request. The template lives in the customer's [Template Library](17-communication-techniques.md) per PB17.
- **The template is reviewed annually** by Legal, Communications, and the CISO for accuracy, regulatory alignment, and language calibration.
- **The template is exercised in the quarterly [Playbook 14 (Testing)](14-testing-for-agent-failure-modes.md) drill cadence.** Each year, at least two drills include a full executive-layer exercise that produces a Decision Packet against a synthetic scenario.
- **The packet's CIA+T framing is the customer's standard impact taxonomy** for AI incidents. A packet that omits Trust as a peer dimension is a finding regardless of the incident's apparent CIA-triad impact.

### Boundary 2: The Approval Receipt discipline operational

- **Every high-impact AI action requires an Approval Receipt** before the action proceeds. The four required elements (change preview, destination and domain, source citations, object count or cap) are structurally enforced by the approval workflow.
- **The Approval Receipt discipline applies across the framework**: PB04 Tier-T2 tool approvals, PB17 external-statement approvals, Materiality-call disclosure approvals, PB19 procurement approvals, [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) HR/Legal-engagement approvals.
- **Approval workflows are audited quarterly** for Receipt-discipline adherence. Approvals that proceeded without the Receipt are findings; the corrective is the workflow's structural enforcement, not the approver's individual diligence.
- **Approval Receipts are themselves logged** as part of the customer's [Playbook 15 (Records, Retention)](15-records-retention.md) discipline. The Receipt history is auditable evidence of approval discipline.

### Boundary 3: The 4-hour update cadence discipline

- **The customer's incident-response runbook names the 4-hour cadence explicitly** for the Executive Decision Packet. Cadence missed without proactive extension is itself a finding.
- **The cadence is owned by the IC** during an active incident; the IC's responsibility includes packet drafting, Legal review, and timely issuance.
- **The cadence applies across the response window** until incident closure or explicit cadence-change approval by the executive team.
- **Cadence drift is tracked across incidents.** A customer that consistently issues the first packet at 60 minutes but slips to 8 hours for the second packet has a structural pattern that the post-incident retrospective surfaces.

### Boundary 4: Three executive routine additions

- **Capability assessment** (what the AI system can do) is added to the executive team's routine per-agent review: which agents the customer's executive team understands the capability of, refreshed quarterly through the AI-BOM. An executive who cannot articulate the capability of a high-stakes agent in plain language is a routine-discipline finding.
- **Provenance tracking** (where the AI got its information) is added to the executive routine: which agents the executive team understands the data-sourcing of, refreshed when the agent's corpora or retrieval configuration changes per [Playbook 22 (Drift)](22-model-policy-drift.md).
- **Approval-chain awareness** (who approved the AI's actions) is added to the executive routine: which high-impact actions the executive team understands the approval discipline of, refreshed when approval workflows are updated.
- **The 5-business-day hardening SLA** from [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) applies to PB05 findings (Decision Packet template gaps, Approval Receipt discipline failures, cadence-discipline lapses, executive-routine gaps).

## Common Pitfalls

These are the highest-frequency failure modes in AI-incident executive decision-making. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Decision packet is a status report, not decision-support** | The IC defaults to narrating the technical investigation rather than structuring the executive decision | The executive team cannot make defensible decisions from the packet; decisions are deferred or made on side-channel information; the customer's response coherence is compromised |
| **CIA framing without Trust** | The executive team applies the traditional CIA triad and treats Trust as a marketing concern | Material trust impact is undercounted; the customer's response is calibrated to a smaller harm scope than is warranted; the post-incident review surfaces the gap when stakeholder reactions exceed the customer's expectations |
| **No Three-Status Taxonomy on packet claims** | Claims are stated without status tags under time pressure | Executive decisions are made on implicit assumptions about the strength of each claim; later evidence contradictions produce credibility costs that explicit tagging would have prevented |
| **Provenance section is thin or absent** | The technical team has not yet produced retrieval-trace analysis; the IC defaults to leaving Provenance empty | The executive team cannot distinguish isolated from systemic incidents; disclosure and communication strategy are calibrated against the wrong incident class |
| **Approval Receipt absent for high-impact action** | The approval workflow allows approval without the four required elements | Human approval becomes rubber-stamping; the post-incident retrospective surfaces that the approver did not have the context to evaluate the action; the customer's safeguard claim is materially weaker than the customer believed |
| **4-hour cadence slips silently** | The IC absorbs the cadence as a soft target; subsequent packets arrive at 8, 12, or 18 hours | Executive decisions are made on stale information; stakeholder communications drift out of alignment with the technical track; the customer's response posture appears uncoordinated |
| **Over-correction under reputational pressure** | The executive team's instinct under press or social-media pressure is to act fast and broad | The over-correction itself becomes a finding; customers are notified prematurely on speculation; regulator filings include unhedged claims that later evidence contradicts |
| **Re-enablement without re-qualification** | The instinct to restore operations under business pressure outweighs the discipline of validating the response | The same incident recurs because the underlying cause was not fully addressed; the customer's response credibility is materially diminished by the recurrence |
| **No 4/24/72-hour planning horizon** | The Next Steps section addresses only immediate actions | The executive team cannot evaluate the response trajectory; stakeholders cannot be told when to expect substantive updates; the disclosure window may close without the customer's preparation |
| **Owners not named per action item** | The Next Steps section lists actions without accountability | Actions slip across the response window; the post-incident retrospective surfaces accountability gaps; the customer's response discipline is compromised |
| **Materiality determination made without the packet** | The convening call proceeds without the structured information | The determination is made on incomplete or inconsistent information; the customer's documentation of the determination is weaker than the regulatory standard requires |
| **Legal review skipped for time pressure** | The pre-approval flow is bypassed by the IC during incident operations | Packet claims create legal exposure the more deliberate review would have caught; the customer's posture for regulatory disclosure is compromised |
| **Decision log absent or partial** | Decisions are made in side-channel communications that are not captured in the formal log | The post-incident retrospective cannot reconstruct who decided what when; the regulator's process review cannot verify the customer's discipline |
| **No board-briefing readiness** | The executive team focuses on incident-level decisions without the broader board readout | Board members learn about material incidents through external coverage rather than direct communication; the customer's board-trust posture is compromised; the [Playbook 24 (Board-Ready Scorecard)](24-board-ready-scorecard.md) discipline is defeated at the moment it is most needed |
| **No quarterly executive drill** | The framework's testing cadence covers technical IR but not executive-layer IR | The first AI incident is the first time the customer's executive discipline is tested under operational pressure; the failure modes from this Pitfalls table all surface at once |
| **Trust impact assessed without the affected-stakeholder count** | The Trust dimension is named but quantified loosely (e.g., "some customers affected") | The disclosure determination is made on imprecise impact scope; the customer's notification strategy is calibrated to assumed rather than measured impact |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). PB05 is the executive-layer operationalization of the four MVO controls; every executive decision references the MVO substrate (Inventory for the Capability Profile, Safe Modes for the Containment status, Evidence for the Provenance Summary, Controlled Re-Enable for the Next Steps).
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). The four-clause Mental Model (Acts, Remembers, Retrieves, Changes) produces the structural sections of the Executive Decision Packet: Acts → Agent Capability Profile (Section 2); Remembers and Retrieves → Provenance Summary (Section 3); Changes → the change-event context in Sections 1 and 4.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). The Executive Decision Packet discipline is a Level 2 (Containable) capability; Approval Receipt discipline operationalized is a Level 3 (Provable) capability; quarterly executive drills are a Level 4 (Resilient) capability.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). The Materiality call uses the Executive Decision Packet as its documentation artifact; PB05 is the operational specification for the packet that supports the Materiality determination.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M0 through M5 ladder and the M3 variants are the operational containment status that the Executive Decision Packet's Section 5 reports against.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A through F evidence taxonomy is the substrate for the Provenance Summary (Section 3) and the evidence-status reporting in Section 5.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The AI-BOM is the source for the Agent Capability Profile (Section 2); a packet that cannot cite the AI-BOM is operating on inference rather than inventory.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The Tier-T2 high-impact action set is the trigger for the Approval Receipt discipline; the Privilege Matrix is the customer's authoritative classification.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone response playbook; PB05 applies the privileged-identity lens to the executive-layer accountability framing (the customer is accountable; the agent operates under the customer's permissions).
- **Playbook 02: Evidence Lives in New Places** ([`playbooks/02-evidence-lives-in-new-places.md`](02-evidence-lives-in-new-places.md)). The Three Realities of AI Evidence are the conceptual foundation the Executive Decision Packet's Provenance Summary section operationalizes.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). Retrieval-poisoning incidents produce Provenance Summary content; PB03's seven-component pipeline forensics inform the Section 3 detail.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The T0/T1/T2 tool tiering drives the Approval Receipt trigger condition; Tier-T2 actions require the four-element Receipt before approval.
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). The Type F output-distribution-map is the substrate for the Confidentiality and Trust dimensions of the Impact assessment (Section 4); without the distribution map, the Impact section is operating on inference.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). Vendor-managed agents produce executive-decision complexity: the customer's accountability extends across the vendor relationship; PB05's packet structure includes the vendor's response posture in the Actions Taken and Next Steps section.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). Insider-threat investigations require executive-layer sensitivity; PB05's discipline includes the HR/Legal joint-engagement coordination as part of the Next Steps section.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). The Six Metrics values appear in the Actions Taken section as the customer's operational-posture indicators; TTSM, TTE, and TT-first-update are the metrics the executive team reads to evaluate response trajectory.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The quarterly executive drill cadence lives in PB14's testing discipline; PB05 specifies the drill's executive-layer content, scoring, and follow-through.
- **Playbook 15: Records, Retention, and Proving What Happened** ([`playbooks/15-records-retention.md`](15-records-retention.md)). The Executive Decision Packet history, the Approval Receipt history, and the decision log are all evidence artifacts under PB15's lifecycle discipline; PB05's executive track produces evidence that PB15's retention discipline preserves.
- **Playbook 16: Training Your Team for AI Incidents** ([`playbooks/16-training-your-team.md`](16-training-your-team.md)). The Three Executive Routine Additions (capability assessment, provenance tracking, approval-chain awareness) are part of the customer's executive-layer training; PB16's drill cadence includes the executive-layer exercise that validates the discipline.
- **Playbook 17: Communication Techniques for AI-Involved IR** ([`playbooks/17-communication-techniques.md`](17-communication-techniques.md)). PB17 specifies the stakeholder communication discipline; PB05 specifies the executive decision-making that produces the substance the communication conveys. PB05 and PB17 together form the **executive-incident-management pair**: PB05 is the decision; PB17 is the communication of the decision.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to PB05 findings (Decision Packet gaps, Approval Receipt failures, cadence-discipline lapses, executive-routine gaps).
- **Playbook 19: Build vs Buy for Agent Controls** ([`playbooks/19-build-vs-buy.md`](19-build-vs-buy.md)). The Proof of Readiness Test includes executive-decision-readiness validation; PB19's eight critical procurement questions inform the executive-layer capability assessment.
- **Playbook 20: AI IR Maturity Roadmap** ([`playbooks/20-maturity-roadmap.md`](20-maturity-roadmap.md)). The executive-discipline maturity is a level-progression artifact; PB05's discipline maps to the customer's Level 2 to Level 4 progression on the executive-decision-making dimension.
- **Playbook 22: Model and Policy Drift** ([`playbooks/22-model-policy-drift.md`](22-model-policy-drift.md)). Drift incidents produce executive-decision complexity: the customer's change pipeline produced the incident; PB05's packet structure includes the change-event context in Section 1 (Situation) and the rollback discipline in Section 5 (Next Steps).
- **Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World** ([`playbooks/23-logging-privacy.md`](23-logging-privacy.md)). The Multi-Stakeholder Governance Matrix (Security, Privacy, Legal, Engineering) maps to the executive team's coordination during AI incidents; PB05's packet structure ensures all four stakeholder classes are represented in the decision-support information density.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). PB24's quarterly board scorecard is the governance-cadence companion to PB05's incident-cadence decision packet. PB24 specifies what the board sees on quarterly cadence; PB05 specifies what the executive team sees during the incident itself. PB05, PB17, and PB24 together form the **executive-layer trio**: PB05 is the decision-during-incident; PB17 is the communication-of-the-decision; PB24 is the periodic governance review of the customer's overall posture.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.4 organizational risk-management decision-making, GOVERN 4.1 organizational accountability for AI risk, MANAGE 1.3 risk-response decision-making, and MANAGE 4.3 incident communication to affected communities).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook is the direct operational response for **GV.OV** organizational oversight by senior leaders, **GV.OC** organizational context for executive decision-making, and **GV.RM** risk-management decision-making; supports RS.MA-04 incident escalation through the executive-layer cadence).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses the executive-decision dimension of **ASI09 Human-Agent Trust Exploitation**: when AI trust is broken, the executive team's structured decision packet and the Approval Receipt discipline are the load-bearing artifacts for both incident-time response and post-incident trust restoration).

## The Question to Carry Forward

If your AI agent caused a customer-visible incident at 14:00 next month, could your IC produce the first Executive Decision Packet within 60 minutes, including all five sections (Situation, Agent Capability Profile, Provenance Summary, Impact with CIA+T framing, Actions Taken and Next Steps with 4/24/72-hour planning horizons)? Could every claim be tagged with Confirmed, Suspected, or Validating? Could the CEO defensibly answer the board's "what are we doing about this?" question from the packet alone? Could the Trust impact dimension be quantified with affected-stakeholder counts rather than impressions? Could every high-impact action in the Next Steps section satisfy the Approval Receipt discipline (change preview, destination and domain, source citations, object count or cap)?

The honest answer is the gap. If any of those answers is *"the IC could not assemble the packet that fast"* or *"the CEO would need additional briefing first"* or *"we have approval workflows that proceed without the four required elements"*, the Executive Decision Packet template, the Three-Status Taxonomy enforcement, the CIA+T framing, the 4-hour cadence, or the Approval Receipt discipline is the corresponding hardening priority.

AI incidents arrive with operational complexity, regulatory exposure, stakeholder anxiety, and time pressure converging in the same hour. The executive team is making decisions that the customer will defend for months or years afterward, based on information that is partial and changing in real time. The framework's job is not to slow the executive decision-making to wait for complete facts; it is to make the decisions defensible under the uncertainty that is unavoidable. When the Executive Decision Packet, the CIA+T framing, the 4-hour cadence, and the Approval Receipt are operational, the executive layer becomes a credibility multiplier for the customer's response posture rather than the gap that surfaces when the first real incident arrives.

---

*Source: AI IR Overlay newsletter, Issue #5, "Executive Decision-Making With AI in the Loop," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
