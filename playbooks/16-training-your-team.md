<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 16: Training Your Team for AI Incidents                  -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The training-discipline playbook. The framework's operational disciplines (kill-switch activation, evidence export, communication) only work if the responders can execute them under pressure. PB16 converts the framework from documentation into operational capability through the 30-Minute Micro-Drill, the Four Core Moves, the two permanent operating roles (Safe Mode Owner and Evidence Owner), and the Curriculum-of-Six that focuses training on practical actions rather than AI theory. Run monthly, measure rigorously, fix the failures rather than re-explain them.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 16: Training Your Team for AI Incidents

> *Every other playbook in this framework assumes the response team can execute the operational discipline it specifies. Activate Mode M3 Tool Tiering inside 10 minutes per [Playbook 04](04-tool-design-is-containment.md). Export the Minimum Evidence Set A through F inside 60 minutes per the [Evidence Export Script Contract](../schemas/evidence-export.spec.md). Issue the first stakeholder update inside 30 minutes per [Playbook 17](17-communication-techniques.md). None of those time budgets survive untrained execution. The first time a responder activates safe mode, exports evidence, applies the Three-Status Taxonomy, or convenes the Materiality call should not be during a real incident. PB16 is the training discipline that converts the framework's documented capabilities into the team's operational muscle memory.*

## Premise

Traditional incident response training (annual tabletops, theory-heavy curricula, generic SANS-style courses) is materially insufficient for AI incidents in four ways:

| Aspect | Traditional IR training | AI IR training |
|---|---|---|
| Cadence | Annual or twice-yearly tabletop | Monthly micro-drill plus quarterly full scenario |
| Format | 2-to-4-hour facilitated discussion | 30-minute time-boxed live execution |
| Content scope | Threat-model awareness, IR-process review, scenario discussion | Direct execution of the framework's operational moves (safe mode activation, evidence export, communication tagging) against live or staging-environment AI agents |
| Measurement | Participation logged, exercise completed | Time-to-Safe-Mode, Time-to-Evidence, 5-bullet executive update produced, all measured and bench-marked against the framework's targets |

The mismatch matters because AI incidents have a distinctive response shape that traditional training does not prepare responders for:

- **Sub-10-minute containment expectation.** [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) and [Playbook 11 (Monitoring)](11-monitoring-detection.md) operate under the assumption that the responder can activate M3 Tool Tiering inside 10 minutes. The activation is a specific sequence (locate the agent's tier configuration, identify the Tier-T2 tools, disable them through the documented mechanism, verify deactivation, log the action). A responder who has not rehearsed the sequence will not complete it in 10 minutes under operational pressure.
- **60-minute evidence-export expectation.** The [Minimum Evidence Set](../evidence/minimum-evidence-set.md) specifies the 60-minute export discipline. The export is six parallel streams (Types A through F) against six different data stores with six different access patterns. A responder who has not rehearsed the export will not complete six parallel streams in 60 minutes, and the responder who improvises will produce gaps the post-incident retrospective surfaces as findings.
- **30-minute first-update expectation.** [Playbook 17 (Communication)](17-communication-techniques.md) specifies the 30-minute first-update SLA. The discipline includes Template Library lookup, Three-Status Taxonomy application, Four-Element Update Standard adherence, and Responsible Reframing pass. A responder who has not rehearsed the discipline drafts the first update from scratch under time pressure with predictable failure-mode patterns.
- **Multi-stakeholder coordination expectation.** [Playbook 23 (Logging and Privacy)](23-logging-privacy.md), [Playbook 15 (Records, Retention)](15-records-retention.md), and the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) all assume the responder can coordinate across Security, Privacy, Legal, and Engineering under time pressure. The coordination is itself a learned skill; theory-heavy training does not produce it.

The biggest operational problem with AI IR readiness is not the absence of documentation; the framework's playbooks document the disciplines extensively. The problem is the gap between *the team has read the documentation* and *the team can execute the documentation under operational pressure at 02:30 on a Saturday morning*. This playbook's job is to close that gap through structured, measured, repeated practice.

**Mental Model clauses engaged:** PB16 operationalizes the entire Mental Model through training. The Acts clause is rehearsed through Tool-Call Ledger export and tool-tier disablement drills; the Remembers clause through Memory Snapshot drills; the Retrieves clause through Retrieval Trace drills; the Changes clause through Configuration Snapshot drills. Each clause has a training move; each training move has a measured target.

**Use this playbook when:** designing or revising the customer's AI IR training curriculum · onboarding a new responder to the on-call rotation · scoping the [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) testing discipline for the training-side complement · scoping the [Playbook 20 (Maturity Roadmap)](20-maturity-roadmap.md) Level 2 (Containable) and Level 3 (Provable) capability validations · designing the quarterly board metric for [Playbook 24 (Board-Ready Scorecard)](24-board-ready-scorecard.md) training-readiness · responding to an audit finding that the customer's AI IR training is insufficient · onboarding a newly-acquired business unit or subsidiary that needs to come into AI IR conformance · supporting the customer's IR-mutual-aid arrangement with a partner organization where joint drills are required · responding to a regulator's question about the customer's AI IR team competence.

## First-Hour Actions

PB16 is structurally a design-time and cadence-driven playbook. Its First-Hour Actions activate in three scenarios: the monthly micro-drill itself, an onboarding session for a new responder, and a post-incident competence review when an incident response surfaced a training gap.

### Case A: The monthly micro-drill (the load-bearing cadence)

The 30-Minute Micro-Drill is the framework's primary training artifact. Run monthly, against a representative agent in the customer's deployment, with the on-call responder executing live.

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Phase 1: Trigger and Contain.** Drill lead presents a realistic scenario (anomalous tool-call spike, suspicious agent output, customer complaint about agent behavior, drift signal per [Playbook 22](22-model-policy-drift.md)). On-call responder activates the appropriate safe mode (typically M1 Read-Only or M3 Tool Tiering depending on the scenario). The responder logs the activation time, the mode chosen, the rationale, and the affected agent's AI-BOM identifier. **Measured target: Time-to-Safe-Mode under 10 minutes.** | Drill lead + On-call responder + Safe Mode Owner |
| 10–20 | **Phase 2: Pull Evidence.** Responder exports the Minimum Evidence Set per the [Evidence Export Script Contract](../schemas/evidence-export.spec.md): prompt and response logs (Type A), tool-call ledger (Type B), retrieval traces (Type C), memory snapshot (Type D), configuration snapshot (Type E), identity and SaaS audit-log correlation (Type F). The export uses the customer's actual export procedure against the actual evidence store. Gaps, access issues, or timeouts are logged. **Measured target: Time-to-Evidence under 60 minutes; export completeness scored against the six types.** | On-call responder + Evidence Owner |
| 20–30 | **Phase 3: Scope and Brief.** Responder produces the 5-bullet executive update per [Playbook 17](17-communication-techniques.md) Template Library: confirmed facts (per the Three-Status Taxonomy), suspected issues (explicitly tagged), containment status (mode active, time-to-activation), potential impact (data, actions, trust), following actions and ownership. The brief is reviewed for Responsible Reframing adherence (zero anthropomorphizing language) and Four-Element Update Standard completeness. **Measured target: 5-bullet brief delivered inside the 30-minute window, all elements present, status taxonomy applied to every claim.** | On-call responder + Incident Commander (drill role) |

**Discipline:** the drill is **time-boxed**. A drill that runs over 30 minutes is itself a training finding (the response sequence is too slow; the training has not yet produced the framework's expected response time). A drill that completes inside 30 minutes but with skipped steps is also a finding (the responder is meeting the time budget by shortcutting the discipline). Both failures enter the drill retrospective and the [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) 5-business-day SLA backlog.

**Critical rule:** the on-call responder executes the drill **without engineering assistance**. Permission issues, missing logs, unclear runbooks, or unfamiliar tools that block the responder during the drill are infrastructure findings, not training failures. The drill is also a test of the customer's operational substrate; gaps are fixed in the runbook, the access controls, or the tooling rather than absorbed as the responder's responsibility.

### Case B: Onboarding a new responder

A new responder enters the on-call rotation when they can complete the 30-Minute Micro-Drill independently. The onboarding sequence:

| Phase | Action | Owner |
|---|---|---|
| Week 1 | **Curriculum-of-Six.** The new responder learns the six core training topics (see Evidence Priorities below) through documented runbooks, framework playbook reading, and shadowing the current on-call responder during a real incident or a drill | Training lead + Senior responder |
| Week 2 | **Assisted drill.** The new responder runs the 30-Minute Micro-Drill with the senior responder shadowing. The senior responder coaches in real time; the drill is not time-bounded as strictly as a measured drill | Senior responder + New responder |
| Week 3 | **Solo drill.** The new responder runs the drill independently against a representative agent. The drill is fully time-bounded. The drill lead reviews the result and identifies remaining gaps | Drill lead + New responder |
| Week 4 | **On-call eligibility.** The new responder enters the on-call rotation. The first three on-call shifts include a senior responder available for backup; the new responder owns the response but can escalate quickly | Training lead + New responder |

### Case C: Post-incident competence review

After a real incident, the post-incident retrospective per [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) includes a training-side review. The discipline is to distinguish capability gaps from operational gaps:

| Phase | Action | Owner |
|---|---|---|
| Day 1 of retrospective | **Inventory the response-execution timeline.** Document each operational step the responder took, with timestamps, against the framework's target time budgets (TTSM, TTE, TT-first-update) | IC + Training lead |
| Day 2 of retrospective | **Categorize gaps.** Distinguish capability gaps (the responder did not know how to do X) from substrate gaps (the responder knew but was blocked by access, tooling, or runbook gaps). Capability gaps drive training curriculum updates; substrate gaps drive PB18 hardening items | Training lead + IC + Platform engineer |
| Day 3 of retrospective | **Update the curriculum.** Capability gaps surfaced by the incident are added to the next monthly micro-drill scenario and to the Curriculum-of-Six documentation. A capability gap that surfaces twice is a curriculum-design finding | Training lead |
| Day 5 of retrospective | **Confirm hardening discipline closure.** Per PB18's 5-business-day SLA, both capability and substrate gaps have action items with owners and target dates by day 5 of the retrospective | IC + Training lead + Platform engineer |

## Containment Options

PB16 does not introduce a new kill-switch variant because training is a discipline, not a containment surface. The framework's existing [Kill-Switch Modes](../kill-switches/overview.md) apply unchanged. PB16's containment-equivalent discipline is the **competence-scope containment**: the actions that limit response responsibility to trained capability while training catches up to expected scope.

### Competence-scope containment

| Action | Use when | What changes |
|---|---|---|
| **Restricted on-call rotation** | New responder has not yet completed the onboarding sequence; an existing responder has been off the rotation for an extended period (parental leave, sabbatical, role change); a quarterly competence review has identified a capability gap | The responder is removed from solo on-call; their on-call shifts include a senior backup; they continue to develop competence through assisted drills and shadowing |
| **Buddy-system on-call** | The team has only one fully-trained responder; the team is geographically distributed and timezone coverage requires multiple responders who each have partial competence | On-call shifts are run as pairs; each pair includes at least one fully-trained responder; the buddy system is documented as the customer's interim posture and the recruiting or training plan to exit it is named |
| **Capability-scoped escalation** | A specific incident class (e.g., insider threat per [Playbook 12](12-insider-threat-3.md), vendor copilot incident per [Playbook 10](10-vendor-copilots.md)) requires specialized response that not every on-call responder has been trained on | The on-call responder activates initial containment and escalates to the specialized responder; the escalation path is documented and time-bounded; the customer's training plan progresses every responder toward the specialized scope |
| **External-IR-mutual-aid activation** | The customer's incident is beyond the trained team's capacity (scale, complexity, scope); the customer has an MSA with an external IR provider | The mutual-aid provider is engaged per the contracted SLA; the customer's responders retain decision authority and drive the response; the mutual-aid provider augments capacity rather than replacing the customer's discipline |
| **Drill-pause cooldown** | The team has run drills aggressively without time to absorb the findings; the operational substrate gaps are accumulating faster than they are being closed | The drill cadence is temporarily reduced to allow PB18 hardening backlog closure; the cooldown is documented with an explicit end date and a target backlog state before resumption |
| **Training-substrate fix as containment** | A drill surfaces a substrate gap (access issue, runbook gap, tool gap) that compromises the response readiness even of fully-trained responders | The substrate fix takes priority over continued drills; the framework's training claims for this agent or scenario class are paused until the fix is complete; the pause is communicated to the customer's leadership and tracked in the PB24 scorecard |

The six actions are operational pragmatism. The discipline is to be explicit about when each is in use; an implicit "we don't have anyone trained for that yet" posture compounds quietly into a capability gap that the customer cannot defend in a regulator review.

## Evidence Priorities

PB16's evidence discipline operates at two levels: the **Curriculum-of-Six** that defines what the training covers, and the **drill-artifact archive** that preserves training evidence for the customer's records discipline per [Playbook 15 (Records, Retention)](15-records-retention.md).

### The Curriculum-of-Six

The Curriculum-of-Six is the framework's minimum-viable training scope. Each topic is taught in accessible, practical language with hands-on practice rather than theoretical discussion. The discipline is to teach the moves, not the AI theory underneath them.

| Topic | What the responder must be able to do |
|---|---|
| **1. Safe modes** | Activate M0 through M5 per [Kill-Switch Modes](../kill-switches/overview.md) for any agent in the AI-BOM. Identify which mode the scenario calls for. Verify activation. Document the activation in the response log. Roll back to M0 when the response sequence supports it. Recognize the M3 variants (M3-RAG, M3-Workflow, M3-Output, M3-Vendor, M3-Delegation Cap, M3-Drift) and apply them where appropriate |
| **2. Tool tiering** | Classify each tool an agent uses as Tier-T0 (low risk), Tier-T1 (medium risk), or Tier-T2 (high risk) per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md). Read the agent's [Privilege Matrix](../templates/agent-privilege-matrix.csv) entry. Disable T2 tools while preserving T0/T1 capability. Understand the operational meaning of each tier classification for the response scope |
| **3. Retrieval traces** | Identify which corpora the agent retrieved from in the incident window. Read retrieval-trace logs from the customer's vector store or RAG framework. Determine which documents influenced the agent's outputs and at which corpus version. Apply [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md) seven-component pipeline forensics |
| **4. Tool-call logs** | Read the agent's tool-call ledger (Type B evidence). Correlate tool calls with downstream SaaS audit records (Type F evidence) using the customer's correlation identifier per [Playbook 19 (Build vs Buy)](19-build-vs-buy.md). Identify denied calls (evidence of intent) alongside successful calls (evidence of impact) |
| **5. Memory state** | Determine whether the agent has memory enabled and at what scope (off, per-user, shared) per the AI-BOM. Snapshot memory before any rotation or cleanup per [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) discipline. Understand memory bleed across users as its own incident class |
| **6. Configuration snapshots** | Pull the agent's current configuration: system prompts, tool definitions, policies, retriever settings, memory configuration, model version pin. Compare against the customer's last known-good baseline per [Playbook 22 (Model and Policy Drift)](22-model-policy-drift.md). Maintain configuration as evidence per [Playbook 15 (Records, Retention)](15-records-retention.md) Two-Tier Retention Standard |

Training on topics beyond the Curriculum-of-Six is optional but recommended. The minimum-viable training scope is competence on these six; everything else is depth and specialization.

### The Four Core Moves

Every drill rehearses the same four operational moves. Mastery is measured by execution under time pressure rather than by curriculum-coverage breadth.

| Move | Operational specification | Measured target |
|---|---|---|
| **1. Activate safe mode** | Locate the agent in the AI-BOM, identify the appropriate Kill-Switch Mode, execute the activation through the customer's documented mechanism, verify activation, log the action | Time-to-Safe-Mode (TTSM) ≤ 10 minutes |
| **2. Preserve and export evidence** | Run the [Evidence Export Script Contract](../schemas/evidence-export.spec.md) for the Minimum Evidence Set A through F against the affected agent and time window; verify completeness; document gaps | Time-to-Evidence (TTE) ≤ 60 minutes; export completeness score against six types |
| **3. Scope the impact in business terms** | Translate the technical evidence into business-impact statements: which customers affected, which records affected, which downstream actions taken, which regulatory or contractual obligations triggered | Brief delivered inside 30-minute window; uses business-impact language rather than technical-detail language |
| **4. Communicate findings with disciplined language** | Apply the [Playbook 17 (Communication)](17-communication-techniques.md) Three-Status Taxonomy (Confirmed, Suspected, Validating), the Four-Element Update Standard (factual impact, immediate containment, evidence-collection activity, next-update timing), and the Responsible Reframing discipline (system-accountability language rather than anthropomorphic attribution) | 5-bullet update with status tags on every claim; zero anthropomorphizing language; next-update time named |

### The Two Permanent Roles

The customer's AI IR team has two named roles that own specific drill-and-incident responsibilities. The roles are documented in the AI-BOM per agent or per fleet; the named role-holders rotate but the role itself is permanent.

| Role | Responsibility | Drill-day function |
|---|---|---|
| **Safe Mode Owner** | Owns the kill-switch activation mechanism per agent. Validates that M0 through M5 (and the M3 variants) are operable at any given time. Maintains the runbook for safe mode activation. Tracks Time-to-Activate metrics per [Playbook 13 (Six Metrics)](13-six-metrics.md) Metric 4 | During the drill, the Safe Mode Owner verifies the activation sequence and signs off on Time-to-Safe-Mode measurement |
| **Evidence Owner** | Owns the evidence-export mechanism per agent. Validates that the [Evidence Export Script Contract](../schemas/evidence-export.spec.md) is operable for the six evidence types. Maintains the runbook for evidence export. Tracks Time-to-Evidence metrics per Metric 3. Coordinates with [Playbook 23 (Logging and Privacy)](23-logging-privacy.md) discipline for access governance | During the drill, the Evidence Owner verifies the export sequence and signs off on Time-to-Evidence measurement |

### Drill-artifact archive

Each drill produces evidence artifacts that enter the customer's records discipline:

- **The drill scenario brief** (the trigger, the agent, the time window, the expected response sequence)
- **The drill execution log** (the actions taken, the timestamps, the mode chosen, the evidence types exported, the brief produced)
- **The drill measurement record** (TTSM, TTE, brief-delivery time, completeness scores)
- **The drill retrospective findings** (capability gaps, substrate gaps, action items with owners and target dates)
- **The drill follow-up closure log** (each finding's closure status against the PB18 5-business-day SLA)

The drill artifacts are retained at the metadata tier per [Playbook 15](15-records-retention.md) Two-Tier Retention Standard (typically 3 to 5 years) so the customer's training discipline is demonstrable to auditors, regulators, and the board on demand.

**Operational requirement:** the monthly micro-drill must run at the documented cadence. A month without a drill is itself a finding. The drill cadence reverts to twice-monthly during the 60 days following a real incident, so the post-incident retrospective findings get reinforced through repeated execution rather than absorbed into a single annual review.

## Recovery Sequence

PB16 recovery addresses three scenarios: restoring training cadence after a cadence lapse, restoring competence after a responder turnover, and restoring training discipline after an audit finding.

### Path 1: Restore training cadence after a lapse

A failure mode: the monthly drill cadence has slipped (one or more months without a drill). The recovery sequence:

1. **Document the cadence gap.** Record the lapse duration, the contributing factors (competing priorities, drill-substrate gaps that blocked previous drills, responder turnover), and the affected responders.
2. **Run a catch-up drill within 5 business days.** The drill follows the standard 30-Minute Micro-Drill structure; the catch-up drill is scenario-realistic rather than reduced-scope.
3. **Diagnose the root cause.** A single-month lapse is typically operational; a multi-month lapse suggests a structural issue with the customer's training prioritization or substrate readiness.
4. **Update the cadence-protection mechanism.** The customer's training discipline includes a documented owner whose role responsibilities include drill execution; cadence drift is itself a metric for that owner.

### Path 2: Restore competence after responder turnover

A failure mode: a fully-trained responder leaves the team; the team's solo-on-call coverage is materially diminished. The recovery sequence:

1. **Activate the buddy-system on-call posture** from the Competence-scope containment until the new responder reaches solo eligibility.
2. **Compress the onboarding sequence where appropriate.** New responders with prior IR experience and prior AI familiarity may complete the onboarding sequence faster than the standard 4-week pattern; the discipline is to compress based on demonstrated competence rather than seniority.
3. **Document the knowledge transfer from the departing responder.** Specific agent quirks, customer-specific runbook tweaks, and informal knowledge are documented before the departure rather than reconstructed afterward.
4. **Update the team's resilience posture.** A team that has been single-point-of-failure on a fully-trained responder has a hidden risk that the responder's departure exposed; the customer's medium-term posture grows the trained-responder count to a documented minimum (typically 3 for adequate coverage).

### Path 3: Restore training discipline after an audit finding

A failure mode: an internal audit, external audit, or regulator review has surfaced that the customer's AI IR training is insufficient. The recovery sequence:

1. **Categorize the finding.** Substrate-side findings (the documentation is missing, the runbook is unclear, the access path is broken) are different from competence-side findings (the responder cannot perform the move). Each requires a different corrective.
2. **Apply substrate fixes first.** A responder who cannot perform a move because the substrate is broken does not need more training; they need a fixed substrate.
3. **Build curriculum to close the competence gap.** Each competence-side finding produces a specific curriculum addition with measurable target.
4. **Run validation drills.** The customer demonstrates the corrective through 2-to-3 consecutive drills that exhibit the previously-failing capability inside the framework's time budgets.
5. **Document the closure in the customer's posture artifact.** The audit-response artifact references the framework's training discipline, the specific curriculum addition, and the validated drill outcomes as the empirical closure evidence.

**Approver for recovery actions:** Training lead, in consultation with the CISO and the Incident Commander. The customer's training discipline is owned at the IR-program level; ad-hoc recovery decisions by individual responders without the Training lead's authorization tend to produce inconsistent practice across the team.

## Post-Incident Hardening

PB16 hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert AI IR training from an annual checkbox into a continuous operational discipline.

### Boundary 1: The monthly drill cadence

- **The monthly micro-drill is non-negotiable.** A month without a drill is a finding; an explanation for the lapse is documented and the catch-up drill is scheduled within 5 business days. The cadence is the customer's primary training-discipline artifact.
- **The drill cadence is owned by a named Training lead** with documented decision authority over drill content, drill outcomes, and curriculum updates. The owner is rotated as a role, not as a person.
- **The drill schedule is published 30 days in advance** so on-call responders can plan; same-day drill activation is exceptional and reserved for post-incident reinforcement.
- **The drill outcomes are reported on the customer's quarterly PB24 board scorecard** as part of the Governance domain signals; consistently-passing drills are a board-defensible operational-readiness indicator.

### Boundary 2: The Curriculum-of-Six current and complete

- **The customer's training curriculum covers the six core topics** with hands-on practice, not theory. A curriculum that emphasizes AI theory at the expense of operational moves is a finding regardless of how thorough the theory coverage is.
- **The curriculum is updated quarterly** based on the prior quarter's drill findings and any real-incident retrospectives. A curriculum that has not been revised in 12 months is operating on assumptions that the team's response history may have invalidated.
- **The curriculum addresses framework-evolution updates.** When the framework ships a new M3 variant, a new playbook, or a new evidence-type extension, the curriculum reflects the change within the next training cycle (typically 30 to 60 days).
- **The curriculum is accessible to all on-call responders** with appropriate access controls. New responders can begin the onboarding sequence without waiting for permission or scheduling; the substrate supports asynchronous learning before the assisted-drill phase.

### Boundary 3: The two permanent roles assigned and current

- **Safe Mode Owner and Evidence Owner roles are documented per agent or per fleet** in the AI-BOM. The named role-holders may rotate, but the role itself is always assigned.
- **The role-holders maintain the relevant runbooks** as part of their role responsibility. A Safe Mode Owner who has not exercised their agent's kill-switch in 90 days is a finding; the operational discipline is reinforced through participation in the monthly drill.
- **Role transitions are documented.** When a role-holder transfers off the role (rotation, promotion, departure), the transition includes a runbook walkthrough, a drill with the new role-holder, and a documented handoff in the customer's records discipline.
- **Role coverage is tracked.** A single role-holder for any agent is a single-point-of-failure finding; the customer's medium-term posture has at least two trained role-holders per role per agent.

### Boundary 4: Measurable training targets reported and improved

- **The framework's measured targets are tracked.** TTSM ≤ 10 minutes, TTE ≤ 60 minutes, 5-bullet brief inside 30 minutes. Each drill's measurements feed the customer's [Playbook 13 (Six Metrics)](13-six-metrics.md) baseline.
- **Drill measurements are reviewed monthly** by the Training lead and the IC. Deviations beyond tolerance bands enter the PB18 5-business-day SLA backlog.
- **Drill outcomes are not punitive.** A drill that misses a target produces a corrective for the substrate or the curriculum; the corrective does not produce a performance-management consequence for the responder. The customer's training culture treats drill outcomes as system signals, not individual ratings.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to drill findings. Drill-discipline gaps do not wait for the next monthly drill.

## Common Pitfalls

These are the highest-frequency failure modes in AI IR training. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Annual tabletop only, no monthly micro-drill** | Traditional IR training culture defaults to large quarterly or annual exercises | The team's operational discipline does not develop muscle memory; the first AI incident is the first time the framework's time budgets are tested under pressure; the response fails the targets |
| **Theory-heavy curriculum** | The complexity of AI tempts trainers to cover the underlying technology in depth | The curriculum produces responders who can discuss model architecture but cannot activate M3 Tool Tiering inside 10 minutes; the framework's operational claims are unsupported by the team's actual capability |
| **No measured time-to-safe-mode** | The drill is treated as a participation exercise rather than a measured execution | TTSM drifts upward without anyone noticing; the customer believes the team is at the framework's standard when the team is materially slower |
| **No measured time-to-evidence** | The evidence export is treated as a post-incident activity; the 60-minute target is aspirational rather than measured | TTE drifts upward; evidence is lost to vendor TTL expiry per [Playbook 15](15-records-retention.md); the framework's evidence claims become indefensible |
| **Drill blocked by substrate, finding absorbed as responder gap** | The drill identifies an access issue, missing log, or unclear runbook; the team treats it as something the responder should have figured out | The substrate gap recurs in real incidents; the team has misallocated training cycles to capability development when substrate fix was the actual corrective |
| **No Safe Mode Owner role** | The kill-switch activation is treated as collectively-owned | Activation drifts because nobody is accountable for keeping it operable; M3 variants in particular suffer because they are agent-specific and require active maintenance |
| **No Evidence Owner role** | The evidence-export pipeline is treated as collectively-owned | Export gaps accumulate (per-type retention drift, access path changes, vendor TTL shifts); the 60-minute discipline becomes unmeasurable |
| **Drill participants opt-out from the on-call responder** | The same senior responder runs every drill | The team's competence concentrates in one person; the buddy-system or rotation discipline is implicit; the senior's eventual departure exposes the gap |
| **No catch-up drill after a cadence lapse** | A missed month is treated as routine | Multi-month lapses compound; the team's competence regresses; the framework's training claims are not empirically valid |
| **Drill scenarios divorced from the customer's actual deployment** | Generic drill scenarios are used regardless of the customer's specific agent landscape | The team rehearses against fictional incidents; real-incident response surfaces gaps the generic drills did not exercise |
| **Punitive response to drill failures** | The customer's culture treats drill outcomes as individual-performance ratings | Responders avoid drill ownership; substrate and curriculum gaps are obscured by responder defensiveness; the drill discipline becomes ceremonial |
| **No curriculum update after framework revisions** | New M3 variants, new playbooks, or new evidence-type extensions ship; the training curriculum does not absorb them | The team's discipline reflects the framework as it was at training time, not as it is at incident time; gaps accumulate at every framework update |
| **No board-reported training metrics** | Training is treated as internal-operations rather than governance-visible | Training cadence drifts because no senior leader sees the lapse; the customer's PB24 scorecard's operational-readiness claim is not empirically validated |
| **No external mutual-aid relationship** | The customer's team is assumed sufficient for all foreseeable incidents | A scale or scope incident overwhelms the team; the customer's response capacity exceeds the team's trained capability without a planned escalation path |
| **Single-trained-responder dependency** | The on-call rotation runs with one fully-trained responder and informal backups | Single-point-of-failure on responder availability; vacation, illness, or departure exposes the gap during the response window |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). PB16 is the training-discipline operationalization of all four MVO controls; every MVO control's operational use depends on the team's trained capability.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). The four-clause model (Acts, Remembers, Retrieves, Changes) is rehearsed through the Curriculum-of-Six: tool-tier and tool-call drills exercise Acts; memory-snapshot drills exercise Remembers; retrieval-trace drills exercise Retrieves; configuration-snapshot drills exercise Changes.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). The monthly drill cadence is a Level 2 (Containable) capability; passing the framework's time budgets in the drills is a Level 3 (Provable) capability; consistent passing over rolling 90-day windows is a Level 4 (Resilient) capability.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). The convening discipline depends on the team's training to recognize material incidents quickly; PB16's training scope includes materiality-recognition criteria as part of the scoping move (Move 3).
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M0 through M5 ladder and the M3 variants are the load-bearing operational vocabulary that the Safe Mode Owner role and the Curriculum-of-Six's safe-modes topic teach.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A through F taxonomy and the 60-minute export discipline are the Evidence Owner role's operational scope and the Curriculum-of-Six's evidence-export topics.
- **Evidence Export Script Contract:** [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md). The export contract is the operational specification the Evidence Owner runs against and trains the team on.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The Safe Mode Owner and Evidence Owner roles are documented per agent in the AI-BOM; the role-holder field is the customer's authoritative record of role assignment.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The tool-tiering training topic depends on the Privilege Matrix being current per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md); the matrix is the responder's operational reference for the tier classification.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook that establishes the privileged-identity lens; PB16 trains the team to apply the lens reflexively in incident response.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). The Type C deep-dive; the Curriculum-of-Six's retrieval-traces topic and the seven-component pipeline forensics depend on PB03's operational specification.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The T0/T1/T2 tiering discipline; the Curriculum-of-Six's tool-tiering topic teaches the operational meaning of each tier and the M3 activation sequence.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). Credential discipline applies to the responders themselves: PB16 trains the team on the role-separated access discipline per [Playbook 23 (Logging and Privacy)](23-logging-privacy.md) and the secrets-rotation sequence the response may trigger.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). Detection signals are the trigger for many drills; PB16 trains the team to read PB11's three signal families (action-based, context-based, capability-based) and respond to each appropriately.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). PB16's measured drill targets (TTSM, TTE, brief-delivery time) feed the Six Metrics baseline; the metric values inform the customer's PB24 board scorecard.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). PB14 is **system-side testing** (does the system support the kill-switch? Can the canary catch drift?); PB16 is **human-side training** (can the responders execute under pressure?). Together they form the **testing-and-training pair** that empirically validates the framework's operational claims. The PB14 Drift Canary and PB23 Forensically Useful tests are the technical-test complements to PB16's human-test drills.
- **Playbook 15: Records, Retention, and Proving What Happened** ([`playbooks/15-records-retention.md`](15-records-retention.md)). PB16's drill artifacts (scenario briefs, execution logs, measurements, retrospectives, follow-up closure logs) are retained at the metadata tier per PB15's Two-Tier Retention Standard; the drill artifacts support the customer's training-discipline audit-defensibility.
- **Playbook 17: Communication Techniques for AI-Involved IR** ([`playbooks/17-communication-techniques.md`](17-communication-techniques.md)). PB17 specifies the communication discipline; PB16 trains the team to apply it. The Three-Status Taxonomy, the Four-Element Update Standard, the Template Library, and the Responsible Reframing discipline are all PB16 curriculum scope. PB16 also includes the quarterly Communication Drill per PB17's discipline.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to PB16 findings (drill cadence lapses, curriculum gaps, substrate gaps surfaced by drills, role-coverage gaps).
- **Playbook 19: Build vs Buy for Agent Controls** ([`playbooks/19-build-vs-buy.md`](19-build-vs-buy.md)). The Proof of Readiness Test from PB19 includes operational readiness, which is a function of trained responder capability; PB16's drill metrics are the empirical input for PB19's procurement-time evaluation.
- **Playbook 20: AI IR Maturity Roadmap** ([`playbooks/20-maturity-roadmap.md`](20-maturity-roadmap.md)). The level progression depends on training discipline; PB16's drill cadence and drill outcomes are the measured input for the customer's maturity-level claims. PB16 and PB20 together form the **training and maturity discipline pair**: PB16 produces the empirical measurements; PB20 places them in the level-progression framework.
- **Playbook 21: Shadow AI** ([`playbooks/21-shadow-ai.md`](21-shadow-ai.md)). Shadow AI discovery and migration require the team to be trained on the discovery boundary, the intake standard, and the identity-level containment discipline; PB16's curriculum incorporates PB21 scenarios into drill rotations.
- **Playbook 22: Model and Policy Drift** ([`playbooks/22-model-policy-drift.md`](22-model-policy-drift.md)). Drift response requires the team to be trained on the layered rollback sequence, the canary replay discipline, and the M3-Drift variant activation; PB16's curriculum incorporates PB22 scenarios into drill rotations.
- **Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World** ([`playbooks/23-logging-privacy.md`](23-logging-privacy.md)). PB23's multi-stakeholder discipline (Security, Privacy, Legal, Engineering) is operationalized through the team's trained ability to coordinate under time pressure; PB16's drills include cross-stakeholder coordination as part of the scoping and briefing move.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). PB16's drill cadence, drill outcomes, and role-coverage status are board-defensible Governance and Recovery domain signals; the scorecard reports the training discipline as part of the customer's quarterly posture artifact.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 3.2 documented and trained human-AI roles, MAP 3.4 personnel training adequacy, MANAGE 1.3 risk-response readiness, and MANAGE 3.1 risk response with stakeholder engagement).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook is the direct operational response for **PR.AT-01** general awareness and training, **PR.AT-02** personnel performing specialized roles, and **GV.RR** roles and responsibilities; supports RS.MA-04 incident escalation readiness through the trained-team posture).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses the operator-training dimension of **ASI09 Human-Agent Trust Exploitation**: the Mental Model's accountability framing and the framework's response disciplines are only effective when the team can apply them under pressure; PB16 is the human-side machinery that makes the framework's countermeasures executable).

## The Question to Carry Forward

If your AI agent caused a customer-visible incident at 14:00 next month, could the on-call responder activate the appropriate safe mode inside 10 minutes without engineering assistance? Could they export the Minimum Evidence Set inside 60 minutes? Could they produce the 5-bullet executive update inside 30 minutes with status tags on every claim and zero anthropomorphizing language? Could they coordinate the multi-stakeholder response across Security, Privacy, Legal, and Engineering without dropping any stakeholder? Could they do all of this at 02:30 on a Saturday morning when the senior responder is on vacation and the buddy-system backup is on a different continent?

The honest answer is the gap. If any of those answers is *"only if I'm the one on call"* or *"only during a drill, not under real pressure"*, the monthly micro-drill cadence, the Curriculum-of-Six, the two permanent roles, or the measurable training targets is the corresponding hardening priority.

AI incidents arrive with operational complexity, regulatory exposure, stakeholder anxiety, and time pressure in the same hour. The framework's documentation is the customer's reference; the team's training is the customer's capability. The framework's job is not to choose between depth of documentation and depth of training; it is to make both load-bearing from the first incident. When the customer's monthly drill cadence and the Four Core Moves and the two permanent roles are operational, the team's capability becomes a credibility multiplier for the framework's response claims rather than the gap that surfaces when the first real incident arrives.

---

*Source: AI IR Overlay newsletter, Issue #16, "Training Your Team for AI Incidents: An Operational Approach to AI Incident Response," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
