# Changelog

All notable changes to the AI IR Overlay framework live here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/spec/v2.0.0.html).

During the `v0.x` series, each substantive content drop ships as its own MINOR release. `v1.0.0` arrives once the framework core is stable, the remaining playbooks are live, and a Steering Committee is in place.

## [Unreleased]

### Planned

- **Content gate complete after v0.24.0.** No remaining drafted playbooks.
- Additional crosswalks: CIS Controls, SOC 2, HIPAA, and a companion NIST SP 800-61 r3 ↔ AI IR Overlay crosswalk (referenced from `crosswalks/nist-csf-2.md`)
- Printable Board Scorecard template (`templates/board-scorecard.md`)
- **Steering Committee announcement (cuts `v1.0.0`)**: the remaining governance gate

## [0.24.0] · 2026-06-29 · Playbook 05: Executive Decision-Making With AI in the Loop (content gate complete)

### Added

- `playbooks/05-executive-decision-making.md`: the executive decision-making discipline playbook. Closes the final content-gate playbook for v1.0; addresses the precondition that prior framework releases depended on but did not specify: AI incidents require defensible executive decisions under uncertainty, before facts are complete and before the regulatory or customer disclosure window forces a commitment. Establishes the **Executive Decision Packet (AI Edition)** as a five-section structured update (Situation with facts only and Three-Status-Taxonomy tagging; **Agent Capability Profile** with identity, enabled tools, systems of record, memory status, connected corpora; **Provenance Summary** with retrieval activity, newly edited or influential documents, instruction-hijack signs, memory entries; **Impact** with the CIA+T framing that elevates Trust to peer status alongside Confidentiality, Integrity, and Availability; **Actions Taken and Next Steps** with named owners across IR, Legal, Communications, Operations, Privacy and 4/24/72-hour planning horizons), the **4-hour cadence** for subsequent packets, the **Approval Receipt discipline** that prevents human approval workflows from degrading into rubber-stamping (every high-impact action's approver sees four required elements before approving: change preview or diff, destination and domain overview, source citations and provenance, object count or cap), the **Three Executive Routine Additions** (capability assessment, provenance tracking, approval-chain awareness as standing executive responsibilities), and the **decision-scope containment** (six actions including status-taxonomy enforcement, materiality-determination scoping, Approval-Receipt enforcement, two-trap callout activation, decision-log lock, disclosure-window clock activation). Sixteen common pitfalls including decision packet as status report not decision-support, CIA framing without Trust, no Three-Status Taxonomy on packet claims, Provenance section thin or absent, Approval Receipt absent for high-impact action, 4-hour cadence slips silently, over-correction under reputational pressure, re-enablement without re-qualification, no 4/24/72-hour planning horizon, owners not named per action item, Materiality determination made without the packet, Legal review skipped for time pressure, decision log absent or partial, no board-briefing readiness, no quarterly executive drill, and Trust impact assessed without affected-stakeholder count.

### Changed

- `CONTENT_MAP.md` Issue 5 status flipped from 🟡 drafted to ✅ `v0.24.0`. The "Why this file exists" section updated to acknowledge that all 24 playbooks are now shipped and the v1.0 cut turns entirely on the Steering Committee announcement. The "Why 23 playbooks shipped so far" subsection renamed to "Why 24 playbooks shipped (content gate complete)" with PB05 added to the operational-arc-completeness rationale (PB05, PB17, PB24 together form the **executive-layer trio**: decision-during-incident, communication-of-the-decision, periodic governance review).
- `README.md` reading order updated from "Twenty-three shipped playbooks" to "All twenty-four playbooks shipped (content gate complete)". PB05 added to the Governance arc bucket alongside PB24 and PB17.
- `crosswalks/nist-csf-2.md` Status section adds **GV.OV** (organizational oversight by senior leaders), **GV.OC** (organizational context for executive decision-making), and **GV.RM** (risk-management decision-making) operational coverage by PB05.
- `crosswalks/nist-ai-rmf.md` GOVERN section adds an executive-decision-making gap-note acknowledging that AI RMF mandates organizational risk-management decision-making (GOVERN 1.4) and organizational accountability for AI risk (GOVERN 4.1) but does not specify the AI-specific executive-decision discipline; PB05 fills the gap with the Executive Decision Packet, the CIA+T framing, the 4-hour cadence, the 4/24/72-hour planning horizons, and the Approval Receipt discipline.
- `crosswalks/owasp-agentic-top-10.md` ASI09 (Human-Agent Trust Exploitation) mapping extended to include PB05 as the executive-decision-making discipline that operationalizes accountable decisions under uncertainty when AI trust is broken. Coverage status bumped from `through v0.23.0` to `through v0.24.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.23.0` to `0.24.0`.

### Why now

PB05 closes the **executive-decision-making discipline** that is the final piece of the framework's content gate. Every prior playbook specifies what the response team does (technical playbooks) or what the response team says (PB17) or how the team is trained (PB16) or how evidence is captured, retained, and proved (PB02, PB15, PB23). None of these specify how the **executive team** makes the decisions that the regulator, the customer, the board, and the press will hold the customer to. Executive decisions during AI incidents are made under three converging pressures (unfolding technical situation, running disclosure window, stakeholder anxiety) that produce a distinctive failure pattern that traditional-IR executive briefings do not address.

PB05 addresses this with the Executive Decision Packet (AI Edition) (the five-section structured update that gives executives decision-support rather than status-narration), the CIA+T framing (elevating Trust to peer status with Confidentiality, Integrity, and Availability because AI incidents commonly produce trust impact that exceeds traditional-CIA impact even when no classic breach has occurred), the 4-hour cadence (an explicit time budget for executive-layer information density), the 4/24/72-hour planning horizons (the structured forward-look that prevents decisions from being made on immediate-only information), and the Approval Receipt discipline (the four required elements that prevent human approval workflows from degrading into rubber-stamping). The playbook makes the difference between **a defensible incident response** and **a defensible response coupled with credible executive accountability** an empirical question (does the customer's IC produce the first Decision Packet inside 60 minutes? does the Approval Receipt discipline apply to every Tier-T2 action?) rather than an asserted claim.

The playbook completes the framework's **executive-layer trio** with PB17 (Communication Techniques) and PB24 (Board-Ready Scorecard). PB05 is the decision-during-incident; PB17 is the communication-of-the-decision; PB24 is the periodic governance review. Together they convert the framework's executive-readiness from a written commitment into a measurable, drillable, board-defensible discipline.

**After v0.24.0, the framework's content gate is complete.** All 24 playbooks (PB01 through PB24) are shipped. The framework's coverage of the operational arc (Foundation, Prevention, Closure, Governance, Measurement and Depth, Operations), the six preconditions (procurement, inventory, change-event, proof, privacy, communication), the four discipline pairs (concepts-and-operations, capture-retain-prove triad, testing-and-training, governance-and-communication), and the executive-layer trio is comprehensive. The remaining v1.0 work is governance: the Steering Committee announcement and the public-interface freeze that converts the framework from single-maintainer pre-1.0 into a sustainable multi-maintainer artifact.

PB05 also closes a long-standing standards-gap pattern: NIST CSF 2.0 mandates organizational oversight (GV.OV) and risk-management decision-making (GV.RM) but does not specify the AI-specific executive-decision discipline. NIST AI RMF mandates organizational accountability for AI risk (GOVERN 4.1) but does not specify the operational mechanism. OWASP's ASI09 Human-Agent Trust Exploitation addresses the trust-exploitation risk but does not address the executive-decision-making discipline that operationalizes accountable decisions under uncertainty. PB05 fills each of those gaps with concrete operational specifications that customers can adopt, regulators can audit against, and adopters can extend.

## [0.23.0] · 2026-06-29 · Playbook 02: Evidence Lives in New Places (foundational concepts)

### Added

- `playbooks/02-evidence-lives-in-new-places.md`: the foundational concepts playbook. Establishes the **Three Realities of AI Evidence** as named principles: (1) **the actor is a workflow, not a workstation** (the agent acts through legitimate service identities and authorized API calls, so evidence lives in prompt logs, tool-call ledgers, retrieval traces, memory snapshots, configuration histories, and downstream SaaS audit records rather than on endpoints); (2) **the payload can be language, not malware** (the harmful artifact may be plain text in a prompt, a retrieved document, an agent response, or a tool-call parameter rather than an executable, so antivirus and intrusion-detection signatures do not apply); (3) **evidence is fragile** (routine response actions like token rotation, prompt updates, corpus cleanups, and redeployment destroy state by default, so the snapshot-before-rotate reflex is the precondition to defensible investigation). Maps the Three Realities to the framework's existing operational machinery: the Capture Order, the Minimum Evidence Set A through F, the Two-Tier Retention Standard from PB15, the chain-of-custody discipline, the Three-Layer Logging Model from PB23, the Reconstructability Test. Includes the **First-Hour Reflexes** that apply to every AI incident response regardless of scenario, the **state-preservation containment discipline** (snapshot-first containment, M1 over M4, identity-level over runtime destruction, corpus version preservation, configuration snapshot before policy tune, vendor-side evidence preservation request), the **A-F Quick Reference** with each evidence type mapped to the Reality it operationalizes, the **conceptual recovery paths** (recovery from an evidence-loss event, recovery from a "this was traditional IR" misframing, recovery from a "the AI did it" framing), and twelve **conceptual misframings** that PB02 exists to correct.

### Changed

- `CONTENT_MAP.md` Issue 2 row updated: PB02 status promoted from 📚 absorbed-into-framework-core to ✅ playbook + ✅ framework-core operational specification. The "Why this file exists" gap statement now excludes PB02 from the unshipped list (only PB05 remains drafted-but-unshipped). The "Why 22 playbooks shipped so far" subsection renamed to "Why 23 playbooks shipped so far" with PB02 added to the standards-gap-closure rationale (closes the conceptual-foundation gap through the Three Realities as named principles). The v1.0 criteria updated from "the target is 23 playbooks" to "the target is 24 playbooks", reflecting the PB02 promotion from absorbed-into-core to separate foundational-concepts playbook.
- `README.md` reading order updated from "Twenty-two shipped playbooks" to "Twenty-three shipped playbooks". The Foundation arc bucket now includes both PB02 (the conceptual-foundation playbook) and PB01 (the operational keystone). Foundation expanded from one playbook to two; both are referenced explicitly by every operational playbook.
- `evidence/minimum-evidence-set.md` Related section adds PB02 as the conceptual companion (the Three Realities), with `evidence/minimum-evidence-set.md` itself as the operational specification. Together they form the **concepts-and-operations pair** for the framework's evidence discipline.
- `CITATION.cff` version + preferred-citation.version bumped from `0.22.0` to `0.23.0`.

### Why now

PB02 closes the **conceptual-foundation gap** that the framework's operational playbooks have been depending on without specifying as a separate artifact. Every prior playbook references the Minimum Evidence Set A-F taxonomy and the Capture Order discipline; both flow from the three foundational realities of AI evidence that newsletter Issue 2 introduced. The original maintainer decision in v0.1.0 was to absorb PB02 into the framework core (`evidence/minimum-evidence-set.md`) because the operational substance (the A-F taxonomy, the Capture Order, the pitfalls list) was fully captured there. The decision had three downstream effects that v0.23.0 resolves:

First, the **Three Realities were not named as principles**. Issue 2's conceptual contributions ("the actor is a workflow, not a workstation"; "the payload can be language, not malware"; "evidence is fragile") were referenced implicitly across the framework but never named explicitly. Responders could read the operational playbooks without internalizing the mental shifts that the operations are built on; PB02 makes the realities explicit and named.

Second, the **"every newsletter issue maps to one playbook in the framework" provenance principle** from the README's Provenance section was violated. The v0.23.0 promotion restores the principle: PB02 now has its own playbook (the conceptual companion) alongside the framework-core operational specification.

Third, **newcomers lacked a pedagogical entry point**. The framework's existing entry points (QUICKSTART for 30-day adoption, `examples/incident-walkthrough.md` for an end-to-end worked example) are action-oriented and scenario-oriented respectively. PB02 adds a concepts-oriented entry point: "first principles of AI evidence, before any specific scenario." The three entry points (action, scenario, concept) together cover the major learning modalities for newcomers.

The playbook uses a **modified canonical skeleton** that preserves coherence with the framework's standard 9-section structure while adapting content to the foundational nature: First-Hour Actions become first-hour reflexes that apply to every AI incident; Containment Options become state-preservation discipline; Evidence Priorities map the Three Realities to the A-F taxonomy; Recovery Sequence is conceptual rather than operational. The structural coherence supports framework-wide consistency; the content adaptation honors PB02's foundational pedagogical role.

The v1.0 criteria are updated accordingly: the target is now 24 playbooks (PB01 through PB24, no absorption), 23 of which are shipped after v0.23.0. The remaining playbook is PB05 (Executive Decision-Making With AI in the Loop). After PB05 ships, the content gate is fully closed and the v1.0 cut turns entirely on the **Steering Committee announcement** (the governance gate).

## [0.22.0] · 2026-06-29 · Playbook 16: Training Your Team for AI Incidents

### Added

- `playbooks/16-training-your-team.md`: the training-discipline playbook. Addresses the precondition that prior framework releases depended on but did not specify: the framework's time budgets (TTSM ≤ 10 minutes, TTE ≤ 60 minutes, first-update inside 30 minutes) require trained execution under operational pressure that traditional annual-tabletop IR training does not produce. Establishes the **30-Minute Micro-Drill** (three time-boxed phases of 10 minutes each: Trigger and Contain, Pull Evidence, Scope and Brief), the **Four Core Moves** (activate safe mode, preserve and export evidence, scope impact in business terms, communicate with disciplined language), the **two permanent operating roles** (Safe Mode Owner who owns the kill-switch activation mechanism per agent and validates M0-M5 plus M3 variants are operable; Evidence Owner who owns the evidence-export mechanism per agent and validates the Type A-F export pipeline), the **Curriculum-of-Six** (safe modes; tool tiering; retrieval traces; tool-call logs; memory state; configuration snapshots: practical, hands-on coverage rather than AI theory), the **monthly drill cadence** (twice-monthly during the 60 days following a real incident), the **measurable training targets** (TTSM ≤ 10 minutes, TTE ≤ 60 minutes, 5-bullet brief inside 30 minutes), the **onboarding sequence** (Curriculum-of-Six → assisted drill → solo drill → on-call eligibility with senior backup for first three shifts), and the **competence-scope containment** (six actions including restricted on-call rotation, buddy-system on-call, capability-scoped escalation, external IR mutual aid, drill-pause cooldown, training-substrate fix as containment). Fifteen common pitfalls including annual-only training, theory-heavy curriculum, no measured TTSM, no measured TTE, drill blocked by substrate but absorbed as responder gap, no Safe Mode Owner role, no Evidence Owner role, drill participants opt-out from the on-call responder, no catch-up drill after cadence lapse, drill scenarios divorced from actual deployment, punitive response to drill failures, no curriculum update after framework revisions, no board-reported training metrics, no external mutual-aid relationship, and single-trained-responder dependency.

### Changed

- `CONTENT_MAP.md` Issue 16 status flipped from 🟡 drafted to ✅ `v0.22.0`. The "Why this file exists" gap statement now excludes PB16 from the unshipped list (only PB05 remains drafted-but-unshipped). The "Why 21 playbooks shipped so far" subsection renamed to "Why 22 playbooks shipped so far" with PB16 added to the 2026 production-pattern relevance rationale (closes the training-discipline precondition through the 30-Minute Micro-Drill, the Four Core Moves, the two permanent roles, the Curriculum-of-Six, the monthly cadence, and the measurable training targets). The PB14+PB16 testing-and-training pair is named explicitly: PB14 is system-side testing; PB16 is human-side training.
- `README.md` reading order updated from "Twenty-one shipped playbooks" to "Twenty-two shipped playbooks". PB16 added to the Measurement and Depth arc bucket alongside PB13, PB14, PB03, PB22, PB15, and PB23.
- `playbooks/17-communication-techniques.md` Related section updated: PB16 "forthcoming" reference replaced with the shipped reference. The interim-placeholder note about "the customer's existing IR-training discipline" is removed; the operational handoff to PB16's monthly drill cadence is named explicitly.
- `crosswalks/nist-csf-2.md` Status section adds **PR.AT-01** (general awareness and training) and **PR.AT-02** (personnel performing specialized roles) operational coverage by PB16, naming the monthly micro-drill cadence and the Curriculum-of-Six as the empirical artifacts. **GV.RR** (roles, responsibilities, and authorities) extended to include the Safe Mode Owner and Evidence Owner role definitions as the operational specification.
- `crosswalks/nist-ai-rmf.md` GOVERN section adds a gap-note acknowledging that AI RMF mandates documented and trained human-AI roles (GOVERN 3.2) and personnel training adequacy (MAP 3.4) but does not specify the AI-specific training discipline; PB16 fills the gap with the 30-Minute Micro-Drill, the Four Core Moves, the two permanent roles, the Curriculum-of-Six, and the monthly cadence with measurable targets.
- `crosswalks/owasp-agentic-top-10.md` ASI09 (Human-Agent Trust Exploitation) mapping extended to include PB16 as the operator-training discipline that makes the Mental Model's accountability framing and the framework's response disciplines executable under pressure. Coverage status bumped from `through v0.21.0` to `through v0.22.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.21.0` to `0.22.0`.

### Why now

PB16 closes the **training-discipline precondition** that the framework's operational playbooks have been depending on without specifying. Every prior playbook assumes the response team can execute its discipline under operational pressure: activate M3 Tool Tiering inside 10 minutes, export the Minimum Evidence Set A through F inside 60 minutes, issue the first stakeholder update inside 30 minutes, coordinate across Security, Privacy, Legal, and Engineering without dropping a stakeholder. None of those time budgets survive untrained execution. Traditional annual-tabletop IR training does not produce the muscle memory the framework's targets require; the first AI incident becomes the first time the team's discipline is tested under pressure, and the framework's claims surface as gaps at the moment they are most damaging.

PB16 addresses this with the 30-Minute Micro-Drill (the framework's primary training artifact, run monthly against a representative agent), the Four Core Moves (activate safe mode, preserve and export evidence, scope impact, communicate with disciplined language: the four operational moves rehearsed in every drill), the two permanent operating roles (Safe Mode Owner who owns the kill-switch mechanism per agent and validates that M0-M5 and the M3 variants are operable; Evidence Owner who owns the evidence-export mechanism and validates the Type A-F export pipeline), the Curriculum-of-Six (safe modes, tool tiering, retrieval traces, tool-call logs, memory state, configuration snapshots: practical hands-on coverage rather than AI theory), the monthly drill cadence (twice-monthly during the 60 days following a real incident so retrospective findings get reinforced through repeated execution), and the measurable training targets that feed PB13 Six Metrics and PB24 board scorecard. The playbook makes the difference between **a documented framework** and **an executable framework** an empirical question (does the on-call responder hit the framework's time budgets in the monthly drill against a representative agent?) rather than an asserted competency.

The playbook completes the framework's **testing-and-training pair** with PB14 (Testing for Agent Failure Modes). PB14 is system-side testing: does the substrate support the kill-switch ladder? Can the Drift Canary catch drift? Can the Reconstructability Test pass at 30 days? PB16 is human-side training: can the responders execute the documented discipline under pressure? Together they convert the framework's operational claims from written commitments into empirically-validated capabilities. After v0.22.0, the framework's response posture is testable on both axes: a CISO can use PB14's quarterly testing cadence to validate the substrate readiness and PB16's monthly micro-drill cadence to validate the team readiness.

PB16 also explicitly closes a long-standing standards-gap pattern: NIST CSF 2.0 mandates personnel training (PR.AT-01) and specialized-role training (PR.AT-02) but does not specify the AI-specific training discipline. NIST AI RMF mandates documented and trained human-AI roles (GOVERN 3.2) but does not specify the operational mechanism. OWASP's ASI09 Human-Agent Trust Exploitation addresses the trust-exploitation risk but does not address the operator-training discipline that makes the framework's countermeasures executable. PB16 fills each of those gaps with concrete operational specifications that customers can adopt, regulators can audit against, and adopters can extend.

After v0.22.0, the framework is **structurally complete on content**: all six preconditions are closed (procurement, inventory, change-event, proof, privacy, communication), the MVO-3 capture-retain-prove triad is shipped, the testing-and-training pair is complete, and the governance-and-communication discipline pair is operational. The single remaining drafted playbook (PB05 Executive Decision-Making With AI in the Loop) addresses an important human-side dimension but is not a structural precondition closure. The v1.0.0 cut now turns on the **Steering Committee announcement** (the documented governance gate) rather than the content gate.

## [0.21.0] · 2026-06-29 · Playbook 17: Communication Techniques for AI-Involved IR

### Added

- `playbooks/17-communication-techniques.md`: the crisis-communication discipline playbook. Addresses the half of AI incident response that the technical playbooks do not cover: what the response team says, to whom, when, and in what language. Establishes the **30-minute first-update SLA** (silence in the first 30 minutes is interpreted by stakeholders as either unaware or hiding; the first update can be brief and explicitly preliminary, but it cannot be absent), the **Three-Status Taxonomy** (Confirmed for verified-through-direct-evidence claims; Suspected for plausible-but-unevidenced; Validating for evidence-collection-and-analysis-underway with stated timeframe), the **Four-Element Update Standard** (factual impact statement, immediate containment controls activated, evidence-collection activity underway, next-update timing; first updates that omit any of the four produce predictable follow-on questions), the **Stakeholder Communication Matrix** (eight stakeholder classes each with calibrated first-update cadence, content scope, and authoring/approval path: internal executive, internal business owners, affected end-users, customers, regulator, board, press/public, employees broadly), the **Template Library** (version-controlled pre-approved templates per stakeholder class with mandatory elements, placeholder fields, forbidden phrases, and approval paths), the **Responsible Reframing discipline** (converts anthropomorphizing language like *"the AI did it"* and *"the model hallucinated"* to system-accountability language like *"an authorized automation behaved incorrectly under investigation"* and *"a privileged AI workflow executed unintended actions"*), and the **information-scope containment** (status taxonomy enforcement, spokesperson channeling, pre-approval gate activation, update cadence commitment, reframing pass, stakeholder-class scoping). Fifteen common pitfalls including anthropomorphic attribution, premature root-cause attribution, leading with technical model details, no first-update SLA, no next-update cadence, no pre-written templates, single message for all stakeholders, status taxonomy not applied, spokesperson channeling broken, Legal review skipped for time pressure, decision log absent or partial, no communication drill cadence, no board-briefing template, no regulator-disclosure templates, and internal employee broadcast skipped.

### Changed

- `CONTENT_MAP.md` Issue 17 status flipped from 🟡 drafted to ✅ `v0.21.0`. The "Why this file exists" gap statement now excludes PB17 from the unshipped list. The "Why 20 playbooks shipped so far" subsection renamed to "Why 21 playbooks shipped so far" with PB17 added to the 2026 production-pattern relevance rationale (closes the communication-discipline precondition through the 30-minute first-update SLA, the Three-Status Taxonomy, the Four-Element Update Standard, the Stakeholder Communication Matrix, the Template Library, and the Responsible Reframing discipline).
- `README.md` reading order updated from "Twenty shipped playbooks" to "Twenty-one shipped playbooks". PB17 added to the Governance arc bucket alongside PB24 (Board-Ready Scorecard), forming the **governance and communication discipline pair**: PB24 specifies what the board sees on quarterly cadence; PB17 specifies how every incident's stakeholder communications hold trust through the response window.
- `crosswalks/nist-csf-2.md` Status section adds **RS.CO** (incident communication during response), **RC.CO** (recovery communication), and **GV.OC** (organizational context including stakeholder communication) operational coverage by PB17. RS.MA-04 (incident escalation) extended to reference the Stakeholder Communication Matrix as the escalation-discipline artifact.
- `crosswalks/nist-ai-rmf.md` MANAGE section adds a gap-note acknowledging that AI RMF mandates incident communication to AI actors and affected communities (MANAGE 4.3) but does not specify the AI-specific communication discipline; PB17 fills the gap with the 30-minute first-update SLA, the Three-Status Taxonomy, the Four-Element Update Standard, the Stakeholder Communication Matrix, the Template Library, and the Responsible Reframing discipline.
- `crosswalks/owasp-agentic-top-10.md` ASI09 (Human-Agent Trust Exploitation) mapping extended to include PB17 as the trust-preservation discipline that runs alongside the framework's technical response: when AI trust is broken by an incident, the communication discipline is what rebuilds it through the response window. Coverage status bumped from `through v0.20.0` to `through v0.21.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.20.0` to `0.21.0`.

### Why now

PB17 closes the **communication-discipline precondition** that the framework's technical playbooks have been depending on without specifying. Every prior playbook specifies what the response team does operationally; none specify what the response team says. The result is that even technically excellent responses can produce poor stakeholder outcomes: a premature root-cause attribution that later evidence contradicts erodes credibility for the rest of the response window; an anthropomorphic attribution ("the AI did it") undermines the customer's accountability posture and creates legal exposure; a one-size message drafted for "stakeholders" satisfies none of the actual stakeholder classes; silence in the first 30 minutes is interpreted as either unaware or hiding. None of these failure modes are addressable through better technical response alone.

PB17 addresses this with the 30-minute first-update SLA (the empirical baseline for the customer's communication-track discipline), the Three-Status Taxonomy (the shared vocabulary that prevents premature commitment to claims that exceed the available evidence), the Four-Element Update Standard (the structural minimum that first updates must contain), the Stakeholder Communication Matrix (the per-audience calibration that prevents one-size messaging), the Template Library (the pre-positioned communication asset that makes accurate, accountable language fast enough for the time pressure), and the Responsible Reframing discipline (the language pattern that operationalizes the Mental Model's accountability framing in every communication artifact). The playbook makes the difference between **a credibility-preserving response** and **a credibility-eroding response** an empirical question (does the customer hit the 30-minute first-update SLA in the quarterly Communication Drill?) rather than an asserted competency.

The playbook completes the framework's **governance and communication discipline pair** with PB24 (Board-Ready Scorecard). PB24 specifies what the board sees on quarterly cadence; PB17 specifies how every incident's stakeholder communications hold trust through the response window. Together they convert the framework's governance posture from a documentation artifact into a continuous trust-preservation discipline. After v0.21.0, the framework's stakeholder-trust posture is testable as well as documented: a CISO can use PB17's quarterly Communication Drill to validate the customer's communication discipline against the same time pressures that real incidents impose, with the drill findings flowing into PB18's 5-business-day hardening SLA backlog and PB13's Six Metrics.

PB17 also explicitly closes a long-standing standards-gap pattern: NIST CSF 2.0 mandates incident communication (RS.CO, RC.CO) and stakeholder context (GV.OC) but does not specify the AI-specific communication discipline. NIST AI RMF mandates incident communication to AI actors and affected communities (MANAGE 4.3) but does not specify the operational mechanism. OWASP's ASI09 Human-Agent Trust Exploitation addresses the trust-exploitation risk but does not address the trust-rebuilding response. PB17 fills each of those gaps with concrete operational specifications that customers can adopt, regulators can audit against, and adopters can extend.

## [0.20.0] · 2026-06-29 · Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World

### Added

- `playbooks/23-logging-privacy.md`: the privacy-discipline playbook. Addresses the precondition that prior framework releases depended on but did not specify: AI logs themselves carry regulated content (PII, PHI, secrets, customer-confidential data, business secrets) and the framework's evidence claims require a logging discipline that satisfies privacy obligations alongside the forensic obligations. Establishes the **Multi-Stakeholder Governance Matrix** (the four primary stakeholder groups, Security and Privacy and Legal and Engineering, each with a defensible interest, a load-bearing artifact, and a measurable acceptance criterion; a logging policy that any one cannot defend is not yet a policy), the **Three-Layer Logging Model** (Layer 1 metadata captured broadly and retained long; Layer 2 selective payload captured under explicitly-documented trigger conditions and retained short; Layer 3 escalation capture under legal hold), the **Forensically Useful standard** (the six core questions logs must answer at Layer 1 alone for typical incidents: who initiated, what tools, what sources, what actions, where outputs went, how mapped to system-of-record changes), the **redaction-and-tokenization discipline** (email-content redaction with recipient-and-category retention, customer-identifier masking with structural preservation, secret-pattern replacement with context tags, document content hashing with ID-and-version retention, identity tokenization with separate mapping store), the **privacy-scope containment** (tier reclassification payload to metadata, selective redaction with hash retention, access-restriction tightening, break-glass disablement, data-subject deletion within retention boundary, vendor-side privacy-scope containment), and the **role-separated access discipline** (IR-investigator, Privacy-reviewer, Legal-counsel, Engineering-platform-administrator roles with explicit per-evidence-type authorization; break-glass mechanisms exceptional, audited, and rate-limited; access audit trail itself audited quarterly). Fourteen common pitfalls including single-stakeholder logging policy, log everything indefinitely, log nothing payload-class, no documented Layer 2 trigger conditions, redaction without forensic verification, redaction without privacy verification, no tokenization-key management, access logs without access-log review, no quarterly multi-stakeholder forum, vendor logs accepted without scrutiny, no Forensically Useful test cadence, privacy redaction breaks chain of custody, data-subject rights requests handled ad hoc, and no drill on the privacy-incident class.

### Changed

- `CONTENT_MAP.md` Issue 23 playbook status flipped from 🟡 drafted to ✅ `v0.20.0` (the crosswalk attribution was already ✅ at v0.1.5). The "Why this file exists" gap statement now excludes PB23 from the unshipped list. The "Why 19 playbooks shipped so far" subsection renamed to "Why 20 playbooks shipped so far" with PB23 added to both the standards-gap-closure rationale (PR.DS-01 privacy controls applied to AI logs, PR.AA access control on the evidence store) and the 2026 production-pattern relevance rationale (closes the privacy-discipline precondition through the Multi-Stakeholder Governance Matrix, the Three-Layer Logging Model, the Forensically Useful standard, and the redaction-and-tokenization discipline). Together PB15 and PB23 form the **capture / retain / prove triad** on top of the Minimum Evidence Set: PB23 specifies how to capture; PB15 specifies how to retain and prove.
- `README.md` reading order updated from "Nineteen shipped playbooks" to "Twenty shipped playbooks". PB23 added to the Measurement and Depth arc bucket alongside PB13, PB14, PB03, PB22, and PB15, completing the MVO-3 Evidence taxonomy capture-side discipline (PB23) alongside the lifecycle discipline (PB15).
- `evidence/minimum-evidence-set.md` Related section now lists PB23 as the shipped privacy-discipline companion to PB15 (replacing the prior "forthcoming" annotation), naming the Multi-Stakeholder Governance Matrix, the Three-Layer Logging Model, the Forensically Useful standard, and the redaction-and-tokenization discipline as the artifacts PB23 contributes to the framework's evidence-capture discipline.
- `crosswalks/nist-csf-2.md` Status section adds **PR.DS-01** privacy controls applied to AI logs (data-at-rest privacy protections through the Three-Layer Logging Model, the redaction-and-tokenization discipline, and the tier-reclassification mechanism) and **PR.AA** access control on the evidence store (role-separated access, audited break-glass procedures, explicit per-evidence-type authorization) operational coverage by PB23. GV.RM (risk management) explicitly extended to include the privacy-risk discipline that runs alongside the security-risk discipline.
- `crosswalks/nist-ai-rmf.md` GOVERN section adds a gap-note acknowledging that AI RMF's privacy mapping (GOVERN 1.1 legal/regulatory context, MAP 5.1 impact assessment, MEASURE 2.10 privacy risk measurement) does not specify the multi-stakeholder governance discipline for AI logs; PB23 fills the gap with the Multi-Stakeholder Governance Matrix, the Three-Layer Logging Model, and the Forensically Useful standard.
- `crosswalks/owasp-agentic-top-10.md` Status section adds an explicit note that PB23 extends OWASP Top 10 for LLM Applications 2025.1 **LLM02 Sensitive Information Disclosure** on the evidence-side: the logs that exist to support the LLM02 response are themselves disciplined so they do not become an LLM02 finding. PB23 also supports ASI06 (Memory & Context Poisoning) memory-hygiene discipline. Coverage status bumped from `through v0.19.0` to `through v0.20.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.19.0` to `0.20.0`.

### Why now

PB23 closes the **privacy-discipline precondition** that the framework's evidence-side playbooks have been depending on without specifying. Every prior playbook assumes that the evidence captured at incident time can be retained, accessed, and exported in a way that supports the framework's forensic claims. None of those assumptions survive routine modern privacy reality: AI logs are not metadata-only logs; they contain prompt bodies, response bodies, retrieved document content, tool-call parameters, and memory content that may include PII, PHI, regulated identifiers, business-confidential information, and even credentials. Treating these logs as if they were traditional IR telemetry produces either overcollection findings under data-minimization regulatory regimes (GDPR Article 5(1)(c), CCPA personal-information limitation, HIPAA minimum-necessary standard) or undercollection findings under the framework's own Reconstructability Test, or both simultaneously.

PB23 addresses this with the Multi-Stakeholder Governance Matrix (Security, Privacy, Legal, Engineering each name a defensible interest, a load-bearing artifact, and an acceptance criterion; a policy any one cannot defend is not yet a policy), the Three-Layer Logging Model (Layer 1 metadata broadly retained and load-bearing for the typical-incident reconstruction; Layer 2 selective payload narrowly triggered by documented high-risk actions, sensitive-corpus access, and active-incident windows; Layer 3 escalation capture under legal hold), the Forensically Useful standard (the six core questions logs must answer at Layer 1 alone, calibrating Layer 2 as the closure layer for specific gaps rather than the default), and the redaction-and-tokenization discipline (structural preservation that retains evidence value while removing sensitive content). The playbook makes the choice between **a privacy-defensible posture** and **a forensic-defensible posture** an empirical question (does the Three-Layer Logging Model satisfy all four stakeholder acceptance criteria simultaneously?) rather than a stakeholder-tribal one.

The playbook completes the framework's **capture / retain / prove triad** on top of the Minimum Evidence Set: [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) establishes the A-F taxonomy and the 60-minute export discipline; PB23 specifies how each evidence type is captured at Layer 1, Layer 2, or Layer 3 with the multi-stakeholder discipline; [Playbook 15 (Records, Retention)](playbooks/15-records-retention.md) specifies how each captured evidence artifact is retained with chain-of-custody integrity through the regulatory and legal review window. After v0.20.0, the framework's evidence claims are testable on the privacy axis as well as the forensic axis: a Data Protection Officer can use PB23's Multi-Stakeholder Governance Matrix to validate the customer's data-minimization posture against regulator review; a CISO can use PB15's Reconstructability Test to validate the customer's forensic posture against the 30-, 60-, and 90-day horizons that regulator and legal review windows typically span.

PB23 also explicitly closes a long-standing standards-gap pattern: NIST CSF 2.0 mandates data-at-rest protection (PR.DS-01) and access control (PR.AA) but does not specify the AI-specific multi-stakeholder governance discipline for logs that simultaneously serve as evidence and as regulated-data stores. NIST AI RMF mandates privacy risk measurement (MEASURE 2.10) but does not specify the operational mechanism. OWASP's LLM02 Sensitive Information Disclosure addresses the data exposure in AI outputs but does not address the exposure in the logs themselves. PB23 fills each of those gaps with concrete operational specifications that customers can adopt, regulators can audit against, and adopters can extend.

## [0.19.0] · 2026-06-29 · Playbook 15: Records, Retention, and Proving What Happened

### Added

- `playbooks/15-records-retention.md`: the proof-discipline playbook. Addresses the precondition that prior framework releases depended on but did not specify: the framework's [Minimum Evidence Set](evidence/minimum-evidence-set.md) specifies what to capture and the 60-minute export discipline, but proof requires retention that survives the regulatory, legal, and business-trust review window where the hardest post-incident conversations happen. Establishes the **Two-Tier Retention Standard** (metadata-tier and payload-tier windows calibrated per evidence class A through F, with the discipline that metadata is cheap to retain and load-bearing for reconstructability, while payload is expensive to retain and load-bearing for content-level proof), the **incident-triggered legal-hold mechanism** (the hold-scope identification, hold-class retention duration, hold notification, and hold release sequence that extends default retention past its window for events that require it), the **chain-of-custody discipline** (every access to the evidence store from the moment of incident declaration is access-logged with actor identity, timestamp, query, and access purpose; the access log itself enters the evidence chain as Type B for the evidence store), the **tamper-evidence discipline** (cryptographic integrity hashes computed at capture time, included in the [Evidence Export Script Contract](schemas/evidence-export.spec.md) manifest, verifiable on subsequent access), the **retention-class containment** (legal hold activation, access-restriction tightening, storage-tier promotion, vendor-side hold request, payload-tier hold, cross-system correlation hold; six complementary actions on the evidence store that operate in parallel with the underlying incident's operational containment), and the quarterly **Reconstructability Test** that empirically validates the framework's evidence claims at 30, 60, and 90 days from a given incident (the test selects a target incident, runs the 60-minute export against the present-day evidence store, scores reconstruction completeness across all six evidence types, identifies failure modes, and flows findings into the PB18 5-business-day SLA backlog). Fourteen common pitfalls including no payload export within the vendor TTL window, payload truncation in the telemetry pipeline, no two-tier retention separation, no incident-triggered legal hold, no chain-of-custody discipline on the evidence store, no tamper-evidence on captured artifacts, no Reconstructability Test cadence, configuration changes not versioned, redaction policies applied without forensic awareness, storage-tier transitions during the investigation window, vendor TTL not contracted for AI evidence types, cross-system correlation gap, disposal discipline absent, and no clarity on what to retain past hold release.

### Changed

- `CONTENT_MAP.md` Issue 15 status flipped from 🟡 drafted to ✅ `v0.19.0`. The "Why this file exists" gap statement now excludes PB15 from the unshipped list. The "Why 18 playbooks shipped so far" subsection renamed to "Why 19 playbooks shipped so far" with PB15 added to both the standards-gap-closure rationale (PB15 closes NIST CSF 2.0 RS.AN-06 and RS.AN-07 records integrity and provenance) and the 2026 production-pattern relevance rationale (PB15 closes the proof-discipline precondition through the Two-Tier Retention Standard, the legal-hold mechanism, the chain-of-custody discipline, and the quarterly Reconstructability Test).
- `README.md` reading order updated from "Eighteen shipped playbooks" to "Nineteen shipped playbooks". PB15 added to the Measurement and Depth arc bucket alongside PB13, PB14, PB03, and PB22, completing the MVO-3 Evidence taxonomy depth coverage: PB03 is the Type C deep-dive, PB09 is the Type F deep-dive, and PB15 is the lifecycle deep-dive across all six evidence types.
- `evidence/minimum-evidence-set.md` Related section now lists PB15 as the shipped lifecycle deep-dive (replacing the prior "forthcoming" annotation), naming the Two-Tier Retention Standard, the legal-hold mechanism, the chain-of-custody discipline, the tamper-evidence anchor, and the Reconstructability Test as the artifacts PB15 contributes to the framework's evidence discipline.
- `crosswalks/nist-csf-2.md` Status section adds **RS.AN-06** (actions performed during an investigation are recorded; records' integrity and provenance preserved) and **RS.AN-07** (incident data and metadata collection with integrity and provenance preservation) operational coverage by PB15, naming the chain-of-custody discipline, the tamper-evidence anchor, and the integrity manifest as the empirical evidence that supports both subcategories. PR.DS-01 attribution extended to include PB15 for the data-at-rest protection of the evidence store itself.
- `crosswalks/nist-ai-rmf.md` MVO-3 Minimum Evidence Set section adds a gap-note acknowledgment that AI RMF does not specify the evidence-retention lifecycle discipline; PB15 fills the gap with the Two-Tier Retention Standard, the legal-hold mechanism, the chain-of-custody discipline, the tamper-evidence anchor, and the quarterly Reconstructability Test.
- `crosswalks/owasp-agentic-top-10.md` Status section adds an explicit note that PB15 addresses the evidence-preservation precondition that every ASI category's response depends on. Coverage status bumped from `through v0.18.0` to `through v0.19.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.18.0` to `0.19.0`.

### Why now

PB15 closes the **proof-discipline precondition** that the framework's response-side playbooks have been depending on without specifying. Every prior playbook assumes the evidence captured at incident time will be available, defensible, and reconstructable when the regulatory, legal, or business-trust review asks for it weeks or months later. None of those assumptions survive routine evidence-retention defaults: vendor TTLs on prompt-and-response logs are 24 to 72 hours; telemetry pipelines truncate event payloads at default size caps; vector indices retain only the current version; storage-tier transitions move evidence from warm to cold to inaccessible on automated schedules; sensitive-data redaction policies applied without forensic awareness destroy payload-class evidence at the same time they protect the data. The first time the customer finds out about an evidence-retention failure is often during the audit, regulator review, or post-incident retrospective where the evidence is needed and discovered missing.

PB15 addresses this with the Two-Tier Retention Standard (metadata-tier and payload-tier windows calibrated per evidence class), the incident-triggered legal-hold mechanism (the hold-scope identification, hold-class retention duration, hold notification, and hold release sequence that extends default retention past its window for events that require it), the chain-of-custody discipline (every access to the evidence store from the moment of incident declaration is access-logged), the tamper-evidence anchor (cryptographic integrity hashes computed at capture time and verifiable on subsequent access), and the quarterly Reconstructability Test that empirically validates the framework's evidence claims at 30, 60, and 90 days. The playbook makes the difference between **a defensible incident** and **an unprovable one** an empirical question (does the Reconstructability Test pass at 30 days for the target scope?) rather than an asserted commitment.

The playbook completes the framework's **MVO-3 Evidence taxonomy depth coverage**: [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) establishes the A-F taxonomy and the 60-minute export discipline, [Playbook 03 (RAG Forensics)](playbooks/03-rag-knowledge-base-forensics.md) is the Type C deep-dive, [Playbook 09 (Output Leakage)](playbooks/09-output-leakage.md) is the Type F deep-dive, and PB15 is the lifecycle deep-dive across all six evidence types (capture-to-disposal, two-tier retention, chain of custody, tamper-evidence, and reconstructability). After v0.19.0, the framework's evidence claims are testable as well as documented: a CISO can use PB15's Reconstructability Test to validate the customer's posture against the 30-, 60-, and 90-day horizons that regulator and legal review windows typically span, with the test result entering [Playbook 13 (Six Metrics)](playbooks/13-six-metrics.md) Metric 3 (Time-to-Evidence) and [Playbook 24 (Board-Ready Scorecard)](playbooks/24-board-ready-scorecard.md) Evidence-domain signals.

PB15 also explicitly closes a long-standing standards-gap pattern: NIST CSF 2.0 mandates that incident records and incident data be preserved with integrity and provenance (RS.AN-06, RS.AN-07) but does not specify the AI-specific retention lifecycle, the two-tier retention discipline, the legal-hold mechanism for AI evidence, the chain-of-custody discipline for AI evidence stores, or the empirical validation cadence. PB15 fills each of those gaps with a concrete operational specification that customers can adopt, regulators can audit against, and adopters can extend.

## [0.18.0] · 2026-06-29 · Playbook 22: Model and Policy Drift

### Added

- `playbooks/22-model-policy-drift.md`: the change-event forensics playbook. Addresses the precondition that prior framework releases depended on but did not specify: production AI systems are constantly evolving through model upgrades, prompt edits, policy tunes, retriever changes, index rebuilds, tool-schema changes, and memory configuration changes. Each change can produce a behavior shift that looks like a regression, a new attack, or a quality issue depending on which component changed and what the operator expects. Establishes the **Post-Change Configuration Snapshot** as the chain-of-custody anchor (captured before any rollback so the post-incident analysis can prove what configuration produced the observed behavior), the **change-pipeline event ledger** as the time-axis equivalent of the tool-call ledger for the customer's own change pipeline, the **layered rollback sequence** (tool policies → retriever parameters → system prompt → policy and moderation configuration → memory and context window → tool schemas → retrieval index and corpus version → model version pin, with canary replay between each layer), and the **four-boundary post-incident hardening** (change control treated as release management; versioning, snapshotting, and pre-change state preservation; the Drift Canary pack with automatic blocking on canary fail; PB11 monitoring extensions for drift-class signals including tool-invocation-frequency, retrieval-pattern, and refusal-pattern shifts). Thirteen common pitfalls including rolling back before snapshotting, treating drift as an external attack, treating drift as routine production tuning, no pre-change snapshot, no change-pipeline event ledger, no Drift Canary pack, canary that gets routinely overridden, rollback at the wrong layer, vendor model version changes without notification, and no version pinning at the model layer.
- `kill-switches/overview.md` Mode Variants table adds the **M3-Drift** variant: M3 Tool Tiering scoped to the specific recently-changed component while pre-change state is restored. M3-Drift is used when the change-window analysis has identified a specific component (model version pin, system prompt, policy configuration, retriever parameters, tool schema, memory configuration) as the most likely drift source. The rolled-back component is validated against the Drift Canary pack; if the canary passes, the agent returns to M0 with the rolled-back state in place. M3-Drift is the change-event parallel to M3-RAG (retrieval-layer containment), M3-Workflow (input-channel containment), M3-Output (output-channel containment), M3-Vendor (vendor-managed containment), and M3-Delegation Cap (inter-agent containment).

### Changed

- `CONTENT_MAP.md` Issue 22 status flipped from 🟡 drafted to ✅ `v0.18.0`. The "Why this file exists" gap statement now excludes PB22 from the unshipped list. The "Why 17 playbooks shipped so far" subsection renamed to "Why 18 playbooks shipped so far" with PB22 added to the 2026 production-pattern relevance rationale (closes the change-event precondition that prior playbooks depended on but did not specify; introduces the layered rollback sequence and the M3-Drift kill-switch variant).
- `README.md` reading order updated from "Seventeen shipped playbooks" to "Eighteen shipped playbooks". PB22 added to the Measurement and Depth arc bucket alongside PB13, PB14, and PB03; together PB14 and PB22 form the **pre-production-testing / continuous-monitoring pair** for drift: PB14 catches drift before deployment with the canary pack; PB22 catches drift after deployment with the layered rollback discipline.
- `crosswalks/nist-csf-2.md` Status section adds **ID.RA** (risk assessment for change events) and **PR.PS** (platform security configuration management) procurement-time discipline coverage by PB22, naming the change-pipeline event ledger and the Post-Change Configuration Snapshot as the empirical evidence that supports the ID.RA and PR.PS subcategory requirements. DE.CM continuous-monitoring coverage extended to include the drift-detection dimension (tool-invocation-frequency, retrieval-pattern, refusal-pattern signals).
- `crosswalks/nist-ai-rmf.md` MANAGE 4 section adds a gap-note acknowledgment that AI RMF does not specify the change-event forensics discipline; PB22 fills the gap with the Post-Change and Pre-Change Configuration Snapshots, the change-pipeline event ledger, the Drift Canary pack, and the layered rollback sequence.
- `crosswalks/owasp-agentic-top-10.md` ASI06 (Memory & Context Poisoning) and ASI10 (Rogue Agents) mappings extended to include PB22 as the change-event vector that produces drift when memory or retrieval changes accumulate, and the dominant 2026 form of rogue-agent emergence (unintentional drift accumulation rather than reward hacking or goal collusion). Coverage status bumped from `through v0.17.0` to `through v0.18.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.17.0` to `0.18.0`.

### Why now

PB22 closes the **change-event precondition** that the framework's response-side playbooks have been depending on without specifying. Every prior playbook assumes the AI system it addresses is operating in a steady state: the AI-BOM entries reflect the current configuration, the canary baselines hold, the detection rules are tuned against the current behavior envelope. None of those assumptions survive routine production AI operation, where models are upgraded by vendors on their own cadence, system prompts are edited weekly, policies and moderation layers are tuned in response to user feedback, retriever parameters shift as the index is rebuilt, and tool schemas change as downstream APIs evolve. The first time the security team finds out about a drift event is often when downstream business owners report that *"the AI changed"* without a corresponding security or operational event.

PB22 addresses this with the change-window forensics discipline (Post-Change Configuration Snapshot, change-pipeline event ledger, Drift Canary pack), the **layered rollback sequence** (tool policies → retriever parameters → system prompt → policy and moderation configuration → memory and context window → tool schemas → retrieval index and corpus version → model version pin, with canary replay between each layer), and the M3-Drift kill-switch variant that scopes containment to the specific recently-changed component while pre-change state is restored. The playbook makes the distinction between **routine production tuning** and **drift event** an empirical question (does the Drift Canary pack pass against the post-change state?) rather than a judgment call.

The playbook also explicitly identifies the misdiagnosis cost as the dominant operational risk: a drift incident investigated as an external attack burns response capacity, may trigger disclosure protocols inappropriately, and ultimately fails to identify the actual cause because the change-window evidence has expired. PB22's two-snapshot pattern (Post-Change and Pre-Change Configuration Snapshots) and the change-pipeline event ledger make change-window evidence load-bearing rather than incidental.

PB22 completes the framework's **pre-production-testing / continuous-monitoring pair** with PB14 (Testing for Agent Failure Modes). PB14 catches drift before deployment with the canary pack; PB22 catches drift after deployment with the layered rollback discipline. Together they convert the framework's continuous-monitoring capability from a written commitment into a change-event-verified reality. After v0.18.0, the framework's coverage of the **precondition chain → response → measurement → continuous monitoring** arc is complete: PB19 selects the platform; PB04 tiers the tools; PB07 disciplines the credentials; PB21 brings shadow agents into inventory; the response-side playbooks execute the incident response; PB13/PB14 measure and test; PB11 detects; PB22 closes the change-event feedback loop that keeps all of the above accurate as the AI system evolves.

## [0.17.0] · 2026-06-29 · Playbook 19: Build vs Buy for Agent Controls

### Added

- `playbooks/19-build-vs-buy.md`: the procurement-time playbook. Addresses the precondition that determines whether the framework's response-side playbooks are executable on a given AI platform. Establishes the **60-minute Proof of Readiness Test** (activate read-only mode, export tool-call and retrieval logs from the past hour, identify the most-frequently-retrieved document, produce a one-page executive update), the **eight critical procurement questions** that distinguish incident-capable platforms from feature-impressive ones (tool gating, exportable logging, configurable retention, correlation identifiers, identity management, RAG governance, escalation contacts and SLAs, Build-vs-Buy clarity), the **Build vs Buy Decision Matrix** with capability-class recommendations (buy foundation model, logging pipelines, IdP, policy engines, credential stores, baseline monitoring; build workflow logic, domain-specific retrieval rules, enterprise approval workflows, golden-prompt regression suites, output-layer DLP rules, materiality protocol operationalization), and the **four-boundary post-procurement hardening framework** (capability gap closure, operational instrumentation, build-side discipline, continued vendor relationship). Ten common pitfalls including feature-driven procurement, demo-driven evaluation without proof-of-readiness testing, no correlation-identifier requirement in RFPs, vendor SLA accepted without testing, and the Build-vs-Buy decision made by procurement alone without IR input.

### Changed

- `CONTENT_MAP.md` Issue 19 status flipped from 🟡 drafted to ✅ `v0.17.0`. The "Why this file exists" gap statement excludes PB19 from the unshipped list. The "Why 16 playbooks shipped so far" subsection renamed to "Why 17 playbooks shipped so far" with PB19 added to the 2026 production-pattern relevance rationale.
- `README.md` reading order updated from "Sixteen shipped playbooks" to "Seventeen shipped playbooks". PB19 added to the Prevention arc bucket alongside PB04 (Tool Design); together PB04 and PB19 form the **pre-incident discipline pair**: PB19 selects the platform that supports response, PB04 tiers the tools that platform exposes.
- `crosswalks/nist-csf-2.md` Status section adds **GV.SC** (supply-chain risk management) procurement-time discipline coverage by PB19, naming the Proof of Readiness Test as the empirical evidence that supports the GV.SC subcategory requirements.
- `crosswalks/nist-ai-rmf.md` MVO-1 Inventory section adds a gap-note acknowledgment that AI RMF does not specify the procurement-time precondition; PB19 fills the gap with the Proof of Readiness Test and the eight critical procurement questions.
- `crosswalks/owasp-agentic-top-10.md` ASI04 (Agentic Supply Chain Compromise) mapping extended to include PB19 as the procurement-time discipline that closes the precondition gap behind ASI04 response. Coverage status bumped from `through v0.16.0` to `through v0.17.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.16.0` to `0.17.0`.

### Why now

PB19 closes the **procurement-time precondition** that determines whether the framework's response playbooks are executable at all. Every prior playbook assumes the underlying AI platform can do specific things: activate read-only mode in under 10 minutes, export prompt and tool-call logs within 60 minutes, correlate tool calls to SaaS audit records with traceable identifiers, configure data retention to match the customer's regulatory window. If the platform cannot do these things, the response playbooks cannot do these things either. The procurement decision is therefore not a vendor-selection question; it is an incident-readiness question.

PB19 addresses this with the Proof of Readiness Test (the operational substitute for vendor demonstration), the eight critical procurement questions (the framework's distillation of platform dependencies into a procurement checklist), the Build vs Buy Decision Matrix (which capabilities are typically appropriate to buy and which to build), and the post-procurement hardening discipline that converts the readiness test's findings into either contractual commitments, customer-side build commitments, or documented risk-acceptance with [PB24 C4 scorecard tracking](playbooks/24-board-ready-scorecard.md).

The playbook completes the framework's **pre-incident discipline pair** with PB04 (Tool Design Is Containment). PB19 selects the platform; PB04 tiers the tools the platform exposes. Together they convert the framework's response capability from a written commitment into a deployment-time-verified reality. After v0.17.0, the framework's coverage of the **procurement → tool design → response** pre-incident chain is complete: a CISO can use PB19 to decide whether to buy a platform, PB04 to tier the platform's tools, and the response-side playbooks (PB01, PB03, PB06, PB07, PB08, PB09, PB10, PB11, PB12, PB18) to execute the incident response the platform was selected to support.

PB19 also closes a long-standing strategic positioning gap: prior framework releases positioned the response discipline but did not specify how to verify the platform supports it. The eight critical procurement questions and the Proof of Readiness Test give CISOs a defensible artifact to take into vendor evaluations and a measurable check against existing deployments. The artifact is the kind of thing standards-body engagement (NIST AI Safety Institute, OWASP GenAI Security Project, ISO/IEC JTC 1/SC 42) can reference as a concrete operational test.

## [0.16.0] · 2026-06-29 · Playbook 21: Shadow AI (From Shadow IT to Shadow Agents)

### Added

- `playbooks/21-shadow-ai.md`: the Shadow AI discovery playbook. Addresses the inventory-gap precondition the framework's response-side playbooks depend on. Establishes the **60-minute Shadow AI Discovery Snapshot** (identity, credentials, connectors, write targets, retrieval scope, memory configuration captured before any access revocation), the **24-hour Shadow Agent Intake Standard** (owner, runtime, identity, tools, write targets, minimum viable logs, safe mode plan), **identity-level containment** as the fallback discipline when the agent's runtime is not customer-modifiable (vendor-hosted, employee-personal-account, no-code platform without admin access), the **Discover → Classify → Safe Mode → Log → Govern** sequence, and the **migrate / redesign / retire** decision path with the customer-controlled criteria for each. Ten common pitfalls including punitive response that drives the next shadow agent underground, treating shadow AI as employee misconduct rather than control gap, no identity-level containment fallback, and no governed integration path that lets teams legitimately deploy AI under governance.

### Changed

- `CONTENT_MAP.md` Issue 21 status flipped from 🟡 drafted to ✅ `v0.16.0`. The "Why this file exists" gap statement now excludes PB21 from the unshipped list. The "Why 15 playbooks shipped so far" subsection renamed to "Why 16 playbooks shipped so far" with PB21 added to the 2026 production-pattern relevance rationale.
- `README.md` reading order updated from "Fifteen shipped playbooks" to "Sixteen shipped playbooks". PB21 added to the Operations arc bucket with description naming the 60-minute Discovery Snapshot, the 24-hour Intake Standard, identity-level containment, and the migrate/redesign/retire decision path.
- `crosswalks/nist-csf-2.md` Status section adds **ID.AM** (asset management) operational discipline coverage by PB21, naming the Shadow AI discovery boundary as the closure of the inventory-gap precondition that prior framework releases depended on but did not specify.
- `crosswalks/nist-ai-rmf.md` MVO-1 Inventory section adds a gap-note acknowledgment that AI RMF does not specify the discovery boundary itself; PB21 fills the gap with the 24-hour intake standard, identity-level containment discipline, and the migrate/redesign/retire decision path.
- `crosswalks/owasp-agentic-top-10.md` ASI03 (Identity & Privilege Abuse) and ASI04 (Agentic Supply Chain Compromise) mappings extended to include PB21 as the discovery-boundary playbook that closes the inventory-gap precondition. Coverage status bumped from `through v0.15.0` to `through v0.16.0`.
- `CITATION.cff` version + preferred-citation.version bumped from `0.15.0` to `0.16.0`.

### Why now

PB21 closes the **inventory-gap precondition** the framework's response-side playbooks have been depending on without specifying. Every prior playbook assumes the agent it addresses is in the AI-BOM, has a documented identity, and has tier-classified tools. None of those assumptions hold for shadow agents. In a typical 2026 enterprise, the AI agents the security team knows about are a fraction of the agents actually running; the rest sit in product teams, marketing operations, finance automation, customer success workflows, and individual employee tooling. The first time the security team finds out about a shadow agent is often during the incident the shadow agent caused.

PB21 addresses this with the discovery boundary, the 24-hour intake standard, and the **migrate / redesign / retire** decision path that converts discovery into governed inventory growth rather than discovery into churn. The playbook's identity-level containment discipline addresses the operational case where the agent's runtime is not customer-modifiable (vendor-hosted, personal-account-hosted, no-code platform without admin access), where traditional tool-level kill-switches do not apply.

The playbook explicitly takes a non-punitive posture toward shadow agent creators: shadow AI emerges from organizational momentum and innovation, not malice. The response framework's job is to make the governed path faster than the shadow path, not to make the shadow path more painful. When the legitimate path takes a day and the shadow path takes a day, the discovery boundary becomes a governance boundary rather than an arms race. PB21 names the **governed integration path** as the fourth hardening boundary explicitly to prevent the discovery boundary from becoming a treadmill.

After v0.16.0, the framework's coverage of the **input → context → output → identity → inventory** preconditions for every other playbook is complete: PB06 (input), PB03 (context), PB09 (output), PB07 (identity), PB21 (inventory). The remaining shipped playbooks (PB01 keystone, PB04 tool design, PB08 multi-agent, PB10 vendor copilots, PB11 monitoring, PB12 insider threat, PB13 metrics, PB14 testing, PB18 hardening, PB20 maturity, PB24 board scorecard) all operate on top of this foundational coverage.

## [0.15.0] · 2026-06-29 · Playbook 09: Leakage Without a Breach (AI Output Incidents)

### Added

- `playbooks/09-output-leakage.md`: the output-side response playbook. Addresses the dominant 2026 AI data-incident class: confidentiality failures stemming from the agent's own output, distributed through authorized channels into ordinary business systems, without classic breach signals. Specifies the **two-perspectives scoping** discipline (what the agent saw, where the output traveled), the **output distribution map** as a Type F evidence extension, the **destination-class scoping principle** that calibrates containment to internal vs customer-facing vs external vs regulated destinations, and the **four-boundary hardening framework** (output channel classification; output-layer DLP; approval gates for outputs containing sensitive content; detection rules covering output-content, output-distribution, and retrieval-to-output correlation). Forms the input → context → output coverage triad with [Playbook 06 (Prompt Injection Workflow)](playbooks/06-prompt-injection-workflow.md) on the input side and [Playbook 03 (RAG Forensics)](playbooks/03-rag-knowledge-base-forensics.md) on the context side. Ten common pitfalls including the "AI outputs as low-risk text" cognitive bias, prompt-layer DLP as theatrical safety, skipping the distribution map, and the absence of output destination classification in the AI-BOM.
- `kill-switches/overview.md` Mode Variants table adds the **M3-Output** variant: M3 Tool Tiering applied to a specific output channel or destination class, sourced from PB09. M3-Output disables a specific output channel (external email send, customer-facing ticket comment, public chat post, auto-CC) or destination class (external systems, customer-facing systems, regulated-data destinations) while preserving the agent's other capabilities. Useful when the channel cannot be globally locked but the leakage destination class is identified.

### Changed

- `CONTENT_MAP.md` Issue 9 status flipped from 🟡 drafted to ✅ `v0.15.0`. The "Why this file exists" gap statement now excludes PB09 from the unshipped list. The "Why 14 playbooks shipped so far" subsection renamed to "Why 15 playbooks shipped so far" with PB09 added to the prioritization rationale (closes the dominant 2026 data-incident class; completes the input → context → output coverage triad).
- `README.md` reading order updated from "Fourteen shipped playbooks" to "Fifteen shipped playbooks". PB09 added to the Operations arc bucket with description naming the M3-Output containment variant and the input → context → output triad with PB06 and PB03.
- `crosswalks/owasp-agentic-top-10.md` Status section updated. ASI06 (Memory & Context Poisoning) mapping extended to include PB09 for the output-side response when memory carries leaked content forward. New cross-reference to OWASP Top 10 for LLM Applications 2025.1 **LLM02 Sensitive Information Disclosure** as the OWASP-named risk PB09 directly operationalizes. Coverage status bumped from `through v0.14.x` to `through v0.15.0`.
- `crosswalks/nist-csf-2.md` Status section adds PR.DS-02 (data-in-transit protection on the output path) coverage by PB09, covering output-layer DLP, channel classification, and destination-aware approval gates. PR.DS-01 attribution unchanged (PB03 + PB06).
- `evidence/minimum-evidence-set.md` Related section adds PB09 as the Type F deep-dive reference (the output distribution map as the Type F extension that scopes output-leakage incidents).
- `CITATION.cff` version + preferred-citation.version bumped from `0.14.3` to `0.15.0`.

### Why now

PB09 closes the largest remaining operational-arc gap in the framework's response posture. Prior releases shipped playbooks for input-side incidents (PB06 workflow injection), context-side incidents (PB03 RAG forensics), identity-side incidents (PB07 secrets and tokens, PB12 insider threat), tool-side incidents (PB04 tool design), multi-agent cascade (PB08), vendor-managed incidents (PB10), and detection (PB11). The framework had no dedicated response playbook for the dominant 2026 data-incident class: **output leakage**, the confidentiality failures stemming from authorized AI outputs that reach destinations they should not have reached, without classic breach signals firing.

PB09's defensive thesis (treat output channels as exfiltration paths; ship output-layer DLP in the tool wrapper, not the system prompt; classify destinations and tier outputs accordingly; map output distribution before any cleanup begins) operationalizes the response discipline that practitioners have been improvising on a per-incident basis. The newsletter issue this playbook ships from (Issue 9: *"Leakage Without a Breach"*) explicitly cites the dominant 2026 data-incident pattern: a support copilot pasting internal escalation notes into a customer ticket, a sales assistant CC'ing the wrong customer on a contract draft, a code copilot logging credentials in a public response. None of these incidents trigger traditional breach detection. All of them are real exposures.

The M3-Output containment variant introduced in this release is the architectural parallel to PB06's M3-Workflow (content-channel containment) and PB10's M3-Vendor (vendor-side containment). The framework's M3 family now covers the three production-relevant containment surfaces above the canonical M3 Tool Tiering: M3-Workflow for content channels feeding the agent, M3-Output for output channels the agent writes to, and M3-Vendor for vendor-managed deployments. Together with M3-RAG (retrieval-layer containment from PB03) and M3-Delegation Cap (inter-agent delegation from PB08), the framework now has five M3 variants documented in [`kill-switches/overview.md`](kill-switches/overview.md), each anchored to a source playbook.

PB09 also addresses the OWASP Top 10 for LLM Applications 2025.1 **LLM02 Sensitive Information Disclosure** category that prior framework releases addressed only implicitly. After v0.15.0, the framework has substantive playbook coverage of both the OWASP Agentic Top 10 ASI01-ASI10 and the operationally-significant categories of the LLM Top 10 (LLM02 by PB09; LLM03/LLM04 supply-chain and poisoning by PB04 + PB06 + PB10).

## [0.14.3] · 2026-06-28 · Calibration Tuning + Cross-Doc Coherence

### Added

- `playbooks/24-board-ready-scorecard.md` Governance Scorecard adds **C4: "Are risk-accepted non-conformant deployments documented and time-bound?"**. C4 tracks agents that do not satisfy framework conformance criteria (e.g., vendor copilots deployed without contracted Boundary 1 SLAs per PB10, or PB18 hardening items past their 5-business-day SLA without explicit risk acceptance) with CISO-signed risk acceptance, audit-trail recording, named closure plan, and quarterly review. Scoring guidance bumped from 11 to 12 items; thresholds adjusted (`0-3 strong`, `4-8 exposed`, `9+ urgent`).
- `RELEASE_CHECKLIST.md` adds two complementary pre-flight discipline guards: a **Cross-reference existence check** (catches vaporware references where one file points at an item that does not exist in the target file) and an **Attribution correctness check** (catches mis-attribution where one file claims "X maps to Y" but X and Y describe different conceptual things).

### Changed

- `README.md` hero blockquote rewritten from `"A candidate minimum-standard framework... intended as a baseline organizations can adopt, adapt, or critique"` (4 hedges) to `"A practical incident-response baseline for AI agents in production. Adapt and critique freely."` (1 hedge). The previous calibration overcorrected; this release restores confident-honest framing.
- `framework/01-minimum-viable-overlay.md` softens absolutist language: blockquote header `"Together: the minimum standard"` → `"Together: a practical baseline"`; conformance section renamed from `"Conformance: Claiming Minimum Standard"` → `"MVO Conformance Criteria"`. Adds an explicit **"overlay, not a replacement"** paragraph that frames the four MVO controls as AI-agent-specific extensions of NIST CSF 2.0 ID.AM/RS/RC functions, NIST SP 800-61 r3, and ISO/IEC 27035 disciplines (not as replacements), with crosswalk references for each base discipline.
- `playbooks/12-insider-threat-3.md` adds an explicit acknowledgment that "Insider Threat 3.0" is the framework's own coined working label, not an industry-accepted taxonomy. Alternative labels (AI-mediated insider risk, agent-assisted misuse, AI-augmented insider threat) are invited as substitutes.
- `playbooks/10-vendor-copilots.md` contractual-leverage callout reframed to use explicit risk-acceptance language: deployment without Boundary 1 SLAs is now a **"documented risk-acceptance decision, not claiming conformance to the framework's standard"**, signed by the CISO, audit-trailed, and tracked as PB24 scorecard item C4 until Boundary 1 closes. Resolves the prior tension between PB10's defensive thesis ("vendor copilots must be deployed... contracted with explicit evidence and containment SLAs") and the accommodation path.
- `playbooks/10-vendor-copilots.md` adds a Common Pitfalls row for "Contractual leverage assumed, not measured": the failure mode where the hardening framework's Boundary 1 items are written as if every customer can negotiate them into a vendor MSA.
- `playbooks/24-board-ready-scorecard.md` C4 narrowed: the original wording flagged "any deployment with active PB18 hardening items pending closure" as overbroad (would have triggered on every operationally-mature agent with normal in-flight hardening). C4 now fires only on (a) non-conformant deployments (e.g., vendor copilots without contracted Boundary 1 SLAs) and (b) PB18 hardening items that have **exceeded** their 5-business-day SLA without explicit risk acceptance. In-flight hardening items still inside their 5-business-day SLA are governed by PB18 itself, not C4.
- `playbooks/13-six-metrics.md` Governance-domain-to-metrics mapping rewritten for accuracy. The prior simplification (`"Governance domain = Metric 1"`) was imprecise. The new framing separates the metric-derived domains (Containment, Evidence, Recovery map directly to Six Metric values) from the scorecard-tracked Governance domain (C1 tier discipline, C2 M3 operational readiness, C3 materiality documentation, C4 risk-acceptance tracking are not directly metric-quantified but depend on the AI-BOM substrate that Metric 1 tracks).
- `playbooks/24-board-ready-scorecard.md` Related-section parenthetical for PB13 aligned to match the new Governance-domain framing in PB13.
- `examples/incident-walkthrough.md` Minute 12 callout rewritten to align with the canonical TTA definition in `kill-switches/overview.md`. The walkthrough now correctly distinguishes **TTA (~2 minutes, IC-order-to-effective)** from **alert-to-containment latency (12 minutes, detection-to-effective)** as two complementary metrics. Prior wording conflated the two.
- `examples/incident-walkthrough.md` Scenario setup adds an explicit **Regulatory posture** paragraph naming Northstar Cloud's SEC, NY DFS, EU AI Act, and HIPAA scope. The Materiality call's clock-question now references this posture rather than asserting "HIPAA does not apply" without basis.
- `CHANGELOG.md` v0.14.2 "Why now" section expanded from 1 paragraph to 3 paragraphs explaining why the operational entry point (QUICKSTART + worked example) is load-bearing for adopter onboarding.
- `RELEASE_CHECKLIST.md` historical-fix references made evergreen ("v0.14.x calibration cycle" rather than "Fixes 64, 65, 66" specific numbers) so the checklist stays useful as the framework evolves.
- `CITATION.cff` version + preferred-citation.version bumped from `0.14.1` to `0.14.3` (closes the recurring CITATION-stale pattern that has now followed every release; the next release-cut following the RELEASE_CHECKLIST will keep this in sync automatically).

### Why now

The v0.14.2 ship surfaced a **second-order pattern** through six follow-on hostile-critic verification passes: every internal fix that touched cross-doc claims had a non-trivial chance of introducing a new inconsistency (the "ripple"). Fix 65 introduced 1 inconsistency (PB10 callout cited PB24 functionality that did not exist). Fix 66 introduced 2 (framework/01 still said "the minimum standard" after the README softened it; PB10 callout conflicted with PB10's own defensive thesis). Fix 67 introduced 1 substantive (C4 row referenced "in-flight hardening" as overbroad scope). Fix 68 introduced 1 (PB13's precision attempt at Governance-to-Metric-1 mapping was technically wrong). Fix 69 introduced 1 stylistic (PB24 Related parenthetical still said "four domains derive from" after PB13 clarified Governance is structurally different).

Each ripple was small. Cumulatively they represented a recurring failure mode that the RELEASE_CHECKLIST did not yet catch. v0.14.3 closes all six ripples and adds the two RELEASE_CHECKLIST discipline guards (**Cross-reference existence check**, **Attribution correctness check**) that should bound this failure mode going forward.

The release also addresses two carryover positioning observations from the holistic full-repo review: the "Insider Threat 3.0" framing in PB12 was presented as established taxonomy (now explicitly framed as the framework's coined working label), and framework/01 did not preempt the "how does MVO-1 differ from NIST CSF ID.AM" question (now explicitly framed as an AI-agent-specific overlay layered on existing standards-body disciplines, not a replacement).

v0.14.3 is the calibration-arc completion release. After this release, the framework is in the most internally-consistent state internal work can produce; further improvements depend on outside-in signals (adoption case studies in Discussions, community PRs, standards-body engagement).

## [0.14.2] · 2026-06-28 · Release Hygiene + Operational Entry Points

### Added

- `QUICKSTART.md`: 30-day adoption path for one production AI agent. Day 1 AI-BOM, Day 7 Privilege Matrix, Day 14 tabletop M1-M4, Day 21 evidence drill, Day 30 maturity claim. Provides the operational entry point the framework was missing (the "what do I do on Monday" answer for CISOs and security engineers).
- `examples/incident-walkthrough.md`: synthetic worked example of an end-to-end incident response. Walks the framework's controls across a fictional workflow-injection scenario at a mid-market SaaS organization, from detection at minute 0 through Day 30 scorecard rollup. Demonstrates the framework as a coherent system, not a list of disconnected controls.
- `RELEASE_CHECKLIST.md`: pre-flight + post-push checklist for the maintainer. Codifies the release hygiene that broke between v0.11.0 and v0.14.1 (missing tags, stale CITATION.cff, workflow never firing).
- `.github/workflows/validate-templates.yml`: added `workflow_dispatch:` trigger for manual runs from the Actions tab, and added the workflow's own path to the `push` trigger so future workflow edits self-validate.

### Changed

- `README.md` hero blockquote softened from "Establishing the minimum standard for safe and effective operations of AI agents in production" to "A candidate minimum-standard framework for AI agent incident response, intended as a baseline organizations can adopt, adapt, or critique". The absolutist framing was an overclaim from a single-maintainer v0.x project.
- `README.md` "Standards" badge relabeled to "References" to remove implied third-party endorsement framing (the badge is a self-issued shields.io badge, not a NIST/OWASP-issued mark).
- `README.md` Reading order section opens with a pointer to `QUICKSTART.md` and `examples/incident-walkthrough.md` so new readers find the operational entry points before the 11-item reading order.
- `README.md` Related work updated to acknowledge MITRE ATLAS as adjacent prior art not currently mapped, with an invitation for a community-contributed ATLAS crosswalk (previously the bare ATLAS namedrop had no operational connection to the framework).
- `CONTENT_MAP.md` adds a "Why 14 playbooks shipped so far" subsection naming the three prioritization axes (standards-gap closure, operational arc completeness, 2026 production-pattern relevance). The remaining 9 drafted playbooks are now labeled "no fixed schedule" with an invitation for Issue-based prioritization or PR contribution. Replaces the bare "drafted, not yet released" status that gave no signal about timing.
- `CONTENT_MAP.md` adds an "Operational entry points" section listing QUICKSTART, the incident walkthrough, and the release checklist.
- `CITATION.cff` version and preferred-citation version bumped from `0.14.0` to `0.14.1` (the calibration pass also bumped the citation file from `0.11.0` to `0.14.0`, but the v0.14.1 cut on 2026-06-28 left CITATION.cff stale; this release closes the gap).

### Why now

The v0.14.1 fresh hostile-critic review (post-release) surfaced three new defects introduced by the release itself: `CITATION.cff` went stale again, three CHANGELOG link references pointed to release tags that were never cut (v0.12.0, v0.13.0, v0.14.0), and the validator workflow had never run because its `push` trigger did not include its own path. The same review surfaced two carryover issues from earlier passes: the README's absolutist "the minimum standard" opening, and the absence of an operational entry point ("framework-as-architecture-document, not framework-as-operational-artifact"). v0.14.2 closes the release-hygiene defects, opens the operational entry point, and softens the README opening to match the project's actual scale.

The operational entry point (`QUICKSTART.md` + `examples/incident-walkthrough.md`) is the load-bearing addition of this release. Prior releases shipped templates, schemas, playbooks, and crosswalks but no integrated **path from "I have an AI agent in production" to "I have a defensible maturity claim"**. A CISO opening the repo on Monday morning had no answer to the question "what do I actually do first?" beyond reading 43 markdown files. `QUICKSTART.md` answers that question with a 30-day path that produces a Level 2 (Containable) or Level 3 (Provable) maturity claim per [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md). The synthetic worked example in `examples/incident-walkthrough.md` then demonstrates the framework's controls operating as a coherent system across a fictional workflow-injection incident, anchoring the framework's abstract claims (six triage questions, six mode variants, six evidence types, six metrics) in a concrete operational sequence.

The release-hygiene additions (`RELEASE_CHECKLIST.md` + workflow `workflow_dispatch` trigger + `CITATION.cff` bump) close the meta-defect that prior releases had a non-repeatable release process. The checklist makes the release cycle a documented routine rather than a sequence of remembered steps.

## [0.14.1] · 2026-06-28 · Calibration Pass + Reference Validator

### Added

- `scripts/validate.py`: Python 3 reference validator that runs every AI-BOM YAML and Privilege Matrix CSV in `templates/` against the JSON Schemas in `schemas/`. Validates clean against the worked examples shipped with the framework. Supports a `--schemas-dir` flag and accepts arbitrary file paths so adopters can drop the script into their own CI.
- `.github/workflows/validate-templates.yml`: GitHub Actions workflow that runs `scripts/validate.py` on every pull request and push to `main` touching `templates/`, `schemas/`, or the script itself. Demonstrates the schemas as live CI artifacts rather than static documentation.

### Changed

- `README.md` Provenance section reworded to remove the "field-tested" claim. The framework has not yet been deployed in a documented production AI incident; adopters who use it in a real incident are now invited to submit anonymized case studies via GitHub Discussions.
- `README.md` reading order extended to item 11 (reference validator).
- `GOVERNANCE.md` restructured to separate **current governance (v0.x)** from **future governance (v1.0.0 and beyond)**. The Steering Committee, Working Group Leads, certification program, and `CONTRIBUTORS.md` are now explicitly labeled as not-yet-established, conditional on v1.0.0 readiness and community adoption.
- `CHANGELOG.md` "Why now" sections for `v0.12.0` and `v0.13.0` rewritten to remove unverifiable reviewer-attribution language. References to "SEC enforcement counsel, EU AI Act regulator, plaintiff's expert, and CISO reviewers" are replaced with the maintainer's own analysis based on the cited statutory and standards sources. The "dominant 2026 production deployment pattern" market-claim phrasing is softened to "a common 2026 deployment pattern" given the absence of supporting analyst data.
- `CONTENT_MAP.md` adds a Reference implementations section.

### Why now

The v0.14.0 ship brought the framework to a coherent baseline (schemas + crosswalks + 14 playbooks). A hostile-critic review identified a calibration gap: the framework's positioning (governance scaffolding for a multi-party project, "field-tested" claim, unverifiable reviewer attribution) exceeded the project's actual scale (single-maintainer pre-1.0 synthesis with no documented production deployments). v0.14.1 closes that gap so the framework's presentation matches its real state, and ships a working reference validator so the schemas can be cited as live CI artifacts rather than static specifications.

## [0.14.0] · 2026-06-28 · Schemas Directory: Machine-Readable Contracts

### Added

- `schemas/ai-bom.schema.json`: JSON Schema 2020-12 for the AI Bill of Materials. Encodes the [`templates/ai-bom.yaml`](templates/ai-bom.yaml) contract as a machine-validatable artifact. Enforces the T0/T1/T2 risk-tier vocabulary (aligned with the Privilege Matrix), the 10-minute Kill-Switch Mode TTA bound, the 60-minute Evidence Set bound, and the conditional CI rule that write tools must declare `write_targets`. The `$id` resolves to `https://aiir.jacobideji.com/schemas/ai-bom.schema.json` for adopter CI pipelines.

- `schemas/privilege-matrix.schema.json`: JSON Schema for a single Privilege Matrix CSV row. Encodes the three CI rules from [Playbook 04 (Tool Design Is Containment)](playbooks/04-tool-design-is-containment.md) as conditional schema constraints: T2 rows must carry `approval_required=yes`; T2 rows must carry a non-empty `reversible` value that is not `n/a`; every write row must declare non-empty `write_targets`. CSV consumers convert each row to a JSON object and validate against this schema as the runtime equivalent of the playbook's pre-incident review.

- `schemas/credential-event.schema.json`: JSON Schema for a single credential-event log entry. Operationalizes the upstream contract specified in [Playbook 07 (Secrets and Tokens)](playbooks/07-secrets-and-tokens.md) Boundary 3 (Telemetry) and consumed by [Playbook 11 (Monitoring)](playbooks/11-monitoring-detection.md) Family 3 (capability-based signals). Specifies nine required fields including `agent_id` (joins to the AI-BOM), `prior_scopes` and `new_scopes` (deterministic scope-diff computation), `actor`, `justification`, and `ticket_id` (audit-trail discipline). The `event_type` enum splits PB07's prose `scope_change` category into `scope_expansion` and `scope_reduction` for detection clarity. Semantic constraint: revocation events must end with empty `new_scopes`.

- `schemas/kill-switch-api.md`: the runtime contract for Mode M0 through M5 activation. RFC 2119 conformance language (29 MUST, 6 SHOULD, 1 MAY) specifies the four API surfaces (Activate, Status, Deactivate, Probe) and the six per-mode contracts. Documents the four M3 containment variants (M3-RAG, M3-Delegation Cap, M3-Workflow, M3-Vendor) and the M4 corpus-scoped and Agent-suspended-for-user variants introduced across PB03, PB06, PB10, and PB12. TTA is measured as the elapsed time between `Activate.requested_at` and `Activate.effective_at` (the drill-measured definition from [`framework/01`](framework/01-minimum-viable-overlay.md) Measurement Scope). Eight-test conformance suite included for adopter validation.

- `schemas/evidence-export.spec.md`: the contract for the Type A through F evidence export script referenced in [Minimum Evidence Set](evidence/minimum-evidence-set.md) and [Playbook 13 Metric 3](playbooks/13-six-metrics.md). RFC 2119 conformance language (34 MUST, 7 SHOULD, 3 MAY) specifies pre-staged access (the script cannot ask for credentials at incident time), parallel-export discipline (the 60-minute drill-measured bound is parallelism-dependent), telemetry emission (four events feeding PB13 Metric 3), and the export bundle's manifest, integrity hash, and chain-of-custody attestation requirements. Eight-test conformance suite included for adopter validation.

### Changed

- `CONTENT_MAP.md`: new "Schemas" section added between Templates and the Drafted but unshipped notes. Lists all five schemas with their repository locations and `v0.14.0` shipped status.

- `README.md`: reading order extended to include the new schemas directory. The schemas are the machine-readable contracts adopters consume in CI to validate their AI-BOM, Privilege Matrix, and credential-event logs against the framework's normative rules.

### Why now

The framework's prior releases ship the playbooks (the narrative discipline) and the templates (the human-readable starting points). The schemas directory ships the **machine-readable contracts** that connect adopter CI pipelines to the framework's normative rules. Before v0.14.0, an adopter editing their AI-BOM YAML or Privilege Matrix CSV had no automated way to verify the file still satisfied the framework's CI rules. The risk-tier vocabulary could drift from T0/T1/T2 to "low/medium/high". A T2 row could ship to production without `approval_required=yes`. A write tool could ship without declared `write_targets`. The schemas close that gap: the same CI rules that appear as English prose in the playbooks now appear as JSON Schema conditional constraints that any modern validator can enforce.

The two markdown specs (`kill-switch-api.md` and `evidence-export.spec.md`) close a parallel gap on the runtime side. Before v0.14.0, the Kill-Switch Mode M0 through M5 ladder was specified by behavior and TTA target, but not by API surface. Adopters building their own kill-switch automation had to derive the API from the playbooks. PB10's vendor copilots showed why the API surface needed formal specification: vendor-provided granular containment must be testable against a common contract. The Kill-Switch API spec and the Evidence Export Script spec together formalize the runtime contracts that PB13 Metric 2 (Time-to-Safe-Mode) and PB13 Metric 3 (Time-to-Evidence) implicitly measure against.

The schemas are not a new framework chapter. They are the machine-readable encoding of contracts that already exist in the narrative framework. The shipping discipline is the same as the rest of the repository: the schemas trace back to the playbooks that specify their rules, the playbooks trace back to the newsletter issues, and the newsletter issues trace back to the operational practice. Adopters now have CI-ready artifacts they can drop into their existing validation pipelines without writing custom validators against framework prose.

## [0.13.0] · 2026-06-28 · Playbook 10: Vendor Copilots and Mutual Responsibility

### Added

- `playbooks/10-vendor-copilots.md`: the vendor-copilot playbook. Operationalizes the customer's response when the agent is managed by the vendor. Reframes "shared responsibility" from procurement slogan to testable operational capability through three disciplines: vendor copilots must be deployed behind a customer-controlled identity boundary, contracted with explicit evidence and containment SLAs, and rehearsed quarterly through the Vendor Evidence Drill. Introduces the M3-Vendor containment variant for vendor-controlled granular containment. Specifies the customer-first containment principle (customer-controllable containment activates immediately; vendor escalation runs in parallel, not first), the independent-verification rule for evidence (never trust only vendor logs; correlate with customer-side IdP and target-system audit), and the four-boundary hardening framework (contract, identity, evidence, communication). Ten common pitfalls including untested shared responsibility, vendor-side containment treated as the only option, contract retention shorter than the customer's regulatory window, and OAuth scopes broader than business need.

### Changed

- `CONTENT_MAP.md`: Issue 10 status promoted from drafted to shipped at `v0.13.0`.

- `README.md`: playbook reading order updated to thirteen → fourteen shipped playbooks; PB10 added to the Operations arc bucket as the vendor-and-supply-chain entry.

### Why now

PB10 closes one of the two largest gaps the maintainer identified in the framework's coverage of 2026 production deployment patterns. Vendor copilots (Microsoft 365 Copilot, Salesforce Einstein, ServiceNow Now Assist, Google Workspace Gemini, GitHub Copilot, and the embedded copilots increasingly built into CRM, ERP, and ticketing platforms) are a common 2026 deployment pattern for AI agents in regulated enterprises. The framework's existing playbooks assumed customer-managed agents; PB10 ships the operational discipline for the case where the customer is responsible to the regulator but the vendor controls the agent's operational levers.

PB10's defensive thesis (deploy behind customer-controlled identity boundary, contract for testable evidence and containment SLAs, rehearse quarterly through the Vendor Evidence Drill) is the framework's first formal supply-chain response playbook. It maps directly to OWASP Agentic Top 10 ASI04 (Agentic Supply Chain Compromise), NIST CSF 2.0 GV.SC (supply chain risk management), and the EU AI Act provider/deployer distinction. Customers acting as deployers of vendor-provided AI systems can now point at a specific operational playbook when responding to regulator inquiry or auditor question about vendor copilot incident readiness.

The Materiality and Disclosure integration (from v0.12.0) extends naturally to vendor-copilot incidents: vendor incidents nearly always cross the convening threshold because external recipients (the vendor and downstream customers) are touched. PB10 makes that convening call explicit in its First-Hour Actions section.

## [0.12.0] · 2026-06-28 · Playbook 06 + Materiality and Disclosure

### Added

- `playbooks/06-prompt-injection-workflow.md`: the workflow-injection playbook. Reframes prompt injection from a chat-UI risk to a workflow attack: harmful instructions hidden inside the everyday content the agent already reads (tickets, emails, web pages, ingested documents). Introduces the M3-Workflow containment variant that pauses content-channel ingestion while preserving the agent's other capabilities. Specifies the source-artifact preservation discipline (the quarantine sequence that preserves the attack ticket or document as primary evidence), the architectural-defense pattern (untrusted content never directly triggers Tier-2 tools), and the four-boundary hardening framework (tool architecture, content trust labeling, approval gates, detection). Ten common pitfalls including the prompt-engineering theatrical fix, output-only detection that misses the retrieval vector, and vendor copilots assumed to handle injection internally.

- `framework/04-materiality-and-disclosure.md`: the Materiality and Disclosure annex. Establishes the convening protocol (CISO + General Counsel + Incident Commander) triggered at Kill-Switch Mode M3 or higher, the four-question walkthrough that decides whether a regulatory disclosure clock has started, and the three outcomes (not material, material, determination cannot be made yet). Cites SEC Item 1.05 (4-business-day clock), EU AI Act Article 26(7) (15-day reporting), NY DFS 23 NYCRR Part 500.17(c) (72-hour notification), and HIPAA 45 CFR §164.408. Frames materiality determination as procedural discipline, not legal authority.

- README "Scope" section: declares the framework operationalizes deployer obligations under EU AI Act Article 3. Lists four explicit out-of-scope categories (provider obligations, GPAI provider obligations, prohibited practices, conformity assessment). Names vendor copilots as in-scope for the deployer (customer side).

- `framework/01` "Measurement Scope" section: distinguishes drill-measured SLA targets (5-minute inventory, 10-minute Mode M1-M5, 60-minute Evidence Set) from live-incident timing. Live timing is tracked under PB13 Metric 2 and 3. Live-incident timing variability is expected and tracked, not a conformance failure.

### Changed

- `kill-switches/overview.md`: TTA definition expanded with drill-measured qualifier. Targets define readiness; live measurement reveals operational reality. A live TTA above target enters PB18 hardening, not a conformance failure.

- `playbooks/01-agent-as-privileged-identity.md`: First-Hour Actions section adds the Materiality and Disclosure trigger. When Question 5 lands on Mode M3 or higher (or the named trigger conditions in framework/04 apply), the Incident Commander convenes the materiality call within one hour.

- `playbooks/18-post-incident-hardening.md`: First-Hour Actions section adds the Materiality verification callout. Before the Fix List ships, the Incident Commander confirms the materiality determination was captured in the decision log. If missing or incomplete, hardening pauses and the 5-business-day SLA does not run.

- `playbooks/24-board-ready-scorecard.md`: adds C3 scorecard item (materiality determination documented for every incident reaching Mode M3 or higher). Scoring guidance bumps from 10 to 11 items; thresholds adjust proportionally (0-3 strong, 4-7 exposed, 8+ urgent).

- Framework metadata refresh and cross-document consistency closure: CITATION.cff bumped to v0.11.0; SECURITY.md Supported Versions table refreshed; CONTRIBUTING.md style guide updated; PB13 Metric 2/3 carry TTSM/TTE canonical aliases reconciling with PB18 and PB20; PB14 recovery sequence reconciled with kill-switches/overview.md M5 order; PB24 body section order rearranged to match the declared A-B-C-D domain flow; PR.AT-01 row added to the NIST CSF 2.0 crosswalk to support PB12's citation; concentrated Tier-2 rule defined inline in PB08; README playbook reading order restructured into the CONTENT_MAP arc; kill-switches Mode Variants subsection added to catalog M3-RAG, M3-Delegation Cap, M4 corpus-scoped, and Agent-suspended-for-user variants.

### Why now

PB06 closes one of the largest gaps the maintainer identified in the framework's previous releases. Indirect prompt injection in workflow form (harmful instructions hidden in tickets, emails, web pages, and ingested documents the agent reads as part of normal operation) is a distinct attack surface from the chat-UI form that earlier framework releases addressed in passing. PB06 ships the architectural-defense framing (untrusted content never directly triggers Tier-2 tools) as an alternative to the prompt-engineering posture common in published competing frameworks.

The Materiality and Disclosure block addresses a gap the maintainer's review of SEC Item 1.05, EU AI Act Article 26/73, NY DFS Part 500, and HIPAA §164.408 surfaced: prior framework releases shipped containment and evidence machinery but did not specify the convening protocol that determines whether a regulatory disclosure clock has started. The four-file chain (framework/04 authority, PB01 trigger, PB18 verification, PB24 governance signal) operationalizes the discipline across the response arc.

The Scope declaration and the Measurement Scope qualifier are the framework's first formal defensive language additions. They bound the framework's claims to a specific regulatory role (deployer obligations) and a specific measurement context (drill-measured targets, not live-incident performance). Both are the load-bearing language a publicly-traded adopter needs in their 10-K to defensibly cite framework conformance.

The metadata and cross-document consistency work brings the framework to a coherent v0.12.0 baseline. Twelve releases of patches, ghost references, stale version anchors, and contradictory cross-doc citations are reconciled.

## [0.11.0] · 2026-06-28 · Playbook 12: Insider Threat 3.0 (AI-Driven Misuse)

### Added

- `playbooks/12-insider-threat-3.md`: the AI-driven insider misuse playbook. Covers two scenarios that prior insider threat generations conflate or miss: the human-with-agent insider (a user with legitimate access uses an AI agent to compile or exfiltrate at scale) and the agent-as-insider (the AI agent itself drifts or is compromised, operating against organizational intent). Specifies the capability vs intent vs impact investigator triad, HR and Legal joint engagement from minute zero, the intent vector as a load-bearing AI-BOM artifact, the intent-realignment gate in recovery, and the soft cap / hard cap discipline for bulk-summarize attacks. Ten common pitfalls including conflating capability with intent, suspending the user before HR/Legal concurrence, and UEBA models tuned for humans missing agent-mediated actions.

### Changed

- `framework/02-mental-model.md` Related section: the Insider Threat 3.0 (Playbook 12) reference upgraded from "forthcoming" to a direct link. **All forthcoming references in the framework's foundational chapters are now closed.**

### Why now

PB12 closes the last remaining forthcoming reference in the framework's foundational chapters (the Mental Model's Related section). After this release, a reader following the foundational arc (README → Mental Model → Maturity Roadmap → MVO) hits zero unfinished references. The framework's foundational narrative reads as complete.

PB12 also completes the rogue-agent coverage arc. [Playbook 11](playbooks/11-monitoring-detection.md) covers detection of capability-family signals that suggest rogue behavior; PB12 covers the response and investigation when those signals fire. The two playbooks form a matched detection-response pair, the same upstream-downstream pattern PB07 → PB11 → PB08 established.

PB12's "Insider Threat 3.0" framing positions the framework ahead of the analyst category formation. Insider Threat 1.0 (humans with credentials, DLP era) and Insider Threat 2.0 (humans with anomalous behavior, UEBA era) are addressed by mature programs. The 3.0 generation, where AI agents mediate or constitute the insider action, is the rising 2026 CISO concern. PB12 ships the operational playbook before the category solidifies.

## [0.10.0] · 2026-06-26 · Playbook 08: Multi-Agent Systems Multiply Blast Radius

### Added

- `playbooks/08-multi-agent-blast-radius.md`: the multi-agent playbook. Specifies the multiplicative blast-radius thesis (one compromised agent's output becomes every downstream agent's input), the orchestrator-first containment sequence, the agent-dependency graph as an AI-BOM artifact, structured handoff contracts between agents, bounded delegation at 2 hops, trace IDs as the across-agents evidence requirement, the 5-to-30-second cascade propagation window and sub-60-second containment latency, the four-boundary hardening framework (topology documentation, inter-agent contracts, bounded delegation, telemetry), and ten common multi-agent pitfalls.

### Changed

- OWASP Agentic Top 10 crosswalk Status section updated. All 10 ASI categories now have substantive playbook coverage with direct references. ASI07 (Insecure Inter-Agent Communication) and ASI08 (Cascading Agent Failures) detailed mappings updated to reference Playbook 08 as the operational layer.

### Why now

PB08 closes the last remaining OWASP Top 10 for Agentic Applications category. With this release, the framework has substantive playbook coverage of **all 10 OWASP ASI categories AND all 6 NIST CSF 2.0 functions**. Combined with the v0.9.0 CSF DETECT closure, v0.10.0 reaches the v1.0.0-ready standards posture.

PB08 also extends the upstream-downstream contract pattern established by PB07 → PB11. Multi-agent topologies inherit the credential-event log schema from PB07 (each agent is a separate identity, no permission inheritance) and consume PB11 detection rules for inter-agent traffic anomalies.

## [0.9.0] · 2026-06-25 · Playbook 11: Monitoring That Truly Detects Agent Incidents

### Added

- `playbooks/11-monitoring-detection.md`: the detection playbook. EDR was built for malware, anomalous process trees, and lateral movement. AI agents act through authorized channels and look like normal operation to the SIEM. PB11 specifies the three signal families (action-based, influence-based, capability-based) that catch what traditional monitoring misses, the 60-minute first-rule drill, the detection-to-containment latency requirement (under 60 seconds), and the four-boundary hardening framework (signal sources, rule logic, latency and routing, procedure).

### Changed

- NIST CSF 2.0 crosswalk Status section updated. The DETECT function (DE.CM continuous monitoring) deferral is closed. All six CSF 2.0 functions now have substantive playbook coverage.
- `playbooks/07-secrets-and-tokens.md` Related section: PB11 reference upgraded from "forthcoming" to a direct link. The hardening section's identity-attribution requirement is now backed by a live downstream consumer.

### Why now

PB11 closes the last remaining NIST CSF 2.0 deferral. With this release, the framework has substantive playbook coverage of all six CSF 2.0 functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER). PB11 also consumes the credential-event log schema specified in [Playbook 07](playbooks/07-secrets-and-tokens.md), honoring the upstream-downstream contract PB07 established. The framework's IR loop (identify, protect, detect, respond, recover, improve) is now operationally complete.

PB11 covers OWASP ASI06 (Memory & Context Poisoning detection), ASI08 (Cascading Agent Failures early detection), and ASI10 (Rogue Agent drift detection).

## [0.8.0] · 2026-06-24 · Playbook 07: Secrets and Tokens in an Agent World

### Added

- `playbooks/07-secrets-and-tokens.md`: the credential-discipline playbook. Covers three credential classes (service-account secrets, delegated OAuth grants, user-impersonation tokens), the 60-minute snapshot-narrow-rotate-validate sequence, the scope-shrink rule, the break-glass procedure for credential-only containment without taking the agent offline, four-boundary hardening (lifecycle, scope, telemetry, procedure), and ten common credential pitfalls observed across engagements.

### Why now

PB07 closes the largest implicit gap in the live framework. Every shipped playbook references token rotation (PB01 names it as "the single most common evidence-destruction failure in AI IR"), yet no playbook specified the agent-specific PAM cadence, rotation discipline, OAuth grant lifecycle, or break-glass procedure. PB07 fills the gap. It also closes the NIST CSF 2.0 PR.AA-05 standards gap that was explicitly documented as deferred in the CSF crosswalk Status section.

PB07 directly extends [Playbook 01](playbooks/01-agent-as-privileged-identity.md)'s privileged-identity lens with the credential-management operational discipline that lens implies. PB11 (Monitoring, forthcoming) will consume the credential-event log this playbook specifies.

## [0.7.0] · 2026-06-24 · Playbook 20: AI IR Maturity Roadmap (Operating View)

### Added

- `playbooks/20-maturity-roadmap.md`: the operating view of the Maturity Roadmap. Covers the four-quarter cadence (weekly, monthly, quarterly, annual), the level-to-containment realism mapping, the 30-minute single-agent reality check, the four-quarter improvement loop, and the ten operating pitfalls that turn a maturity program into documentation theater.
- Maturity Roadmap framework view (`framework/03-maturity-roadmap.md`) now points readers at PB20 for execution. The two prior "forthcoming" notes are removed.
- CONTENT_MAP.md Issue 20 row updated to show the operating view as shipped.

### Why now

PB20 completes the measurement and discipline triad with [Playbook 13 (Six Metrics)](playbooks/13-six-metrics.md) and [Playbook 14 (Testing for Agent Failure Modes)](playbooks/14-testing-for-agent-failure-modes.md). Together these three carry the Level 4 (Resilient) maturity claim from aspiration to operating reality.

## [0.6.2] · 2026-06-23 · Structural Cleanup

Documentation accuracy and navigation polish. No framework substance changes.

### Fixed

- Misrouted link in `playbooks/01-agent-as-privileged-identity.md` line 111. The "Playbook 18" reference now resolves to the actual playbook (was pointing to the CSF 2.0 crosswalk by mistake).
- "Minimum Viable Overlay" link in `templates/README-ai-bom.md` repointed from `jacobideji.com` to the in-repo file.

### Changed

- 46 backtick-package-slug references across 12 files converted to relative file paths. Closes the residue from the original "ships as separate packages" distribution model.
- 5 forthcoming-playbook references (PB12, PB15, PB20, PB23) rewritten as "forthcoming, see CHANGELOG" notes instead of citing them as live packages.
- Evidence-letter notation normalized to A–F (en dash) across the repo. 12 outliers (A to F, A-F hyphen, A through F) all aligned.

### Added

- New "RAG-specific containment" note in `kill-switches/overview.md` Mode 3, pointing to Playbook 03 for the freeze-the-world sequence.
- Inbound links added for the previously underwoven playbooks: PB13 now referenced from PB18, PB24, and the Maturity Roadmap Level 4 row. PB03 now referenced from kill-switches Mode 3, evidence Type C, and OWASP ASI06.
- Printable triage card now linked from `triage/six-questions.md`.

## [0.6.1] · 2026-06-23 · Documentation Polish

Accuracy and OSS-convention round. No framework substance changes.

### Fixed

- `SECURITY.md` Supported Versions table bumped from `v0.1.x` to `v0.6.x`. The version table was stale and didn't reflect the actual current release.
- `CODE_OF_CONDUCT.md` enforcement section: "at via" template artifact replaced with "via".
- `README.md` "widely-understood" hyphenation corrected to "widely understood" (predicate adjective).
- `README.md` reading order items 1 through 6 converted from package slugs to real relative file paths.

### Added

- `README.md` now carries License, Latest Release, and Standards badges.
- `README.md` Acronyms list now includes TTE (Time-to-Evidence) and TTSM (Time-to-Safe-Mode).
- `CHANGELOG.md` (this file): Keep-a-Changelog format covering all 11 releases.
- `GOVERNANCE.md`: roles, decision-making, release cadence, trademark.
- `CONTENT_MAP.md`: newsletter issue to repo destination map with arc-based ship order.

### Changed

- Repo-wide humanization pass: em-dash density reduced from 1.0 to 7.6 per 100 words (worst-case) down to 0.08 per 100 words across the whole repo. Style guide target is 0.5.

## [0.6.0] · 2026-06-23 · Measurement Release

### Added

- Operational guidance for measuring AI incident response posture across the four MVO controls.
- `playbooks/13-six-metrics.md`: the six metrics that turn maturity from an adjective into a number.
- `playbooks/14-testing-for-agent-failure-modes.md`: how to test Kill-Switch modes M1 through M4 before you need them.
- `playbooks/03-rag-knowledge-base-forensics.md`: the freeze-the-world sequence for RAG and knowledge-base incidents.

## [0.5.0] · 2026-06-20 · Playbook 24: Board-Ready Scorecard

### Added

- `playbooks/24-board-ready-scorecard.md`: executive-layer artifact. Translates the technical IR machinery into a four-domain board view (Containment, Evidence, Governance, Recovery) with GREEN, AMBER, and RED ratings.

## [0.4.0] · 2026-06-19 · Playbook 18: Post-Incident Hardening

### Added

- `playbooks/18-post-incident-hardening.md`: closes the response arc. Turns post-incident lessons into permanent guardrails within five business days.

## [0.3.0] · 2026-06-18 · Playbook 04: Tool Design Is Containment

### Added

- `playbooks/04-tool-design-is-containment.md`: pre-incident playbook. Covers tool tiering (Tiers 0, 1, and 2) and the five-control containment model that makes Mode M3 surgical.

## [0.2.0] · 2026-06-18 · Playbook 01: The Agent Is a Privileged Identity

### Added

- `playbooks/01-agent-as-privileged-identity.md`: the first practitioner playbook. Sets the privileged-identity lens that every later playbook builds on.

## [0.1.5] · 2026-06-17 · Crosswalk Expansion

### Added

- `crosswalks/nist-csf-2.md`: NIST CSF 2.0 mapping across the six functions (Govern, Identify, Protect, Detect, Respond, Recover).
- `crosswalks/owasp-agentic-top-10.md`: OWASP Agentic Top 10 2026 (ASI01 through ASI10) mapping.

### Changed

- Citation accuracy improved across every referenced standard.

## [0.1.4] · 2026-06-17 · Content Accuracy Polish

### Changed

- Updated NIST reference from SP 800-61 r2 to r3 (April 2025), reflecting the CSF 2.0 Community Profile restructure.
- Disambiguated OWASP Top 10 for LLM Applications (2025.1) from OWASP Top 10 for Agentic Applications 2026 throughout.

## [0.1.3] · 2026-06-17 · Cosmetic Polish

### Changed

- Trivial consistency fixes (formatting, link punctuation, heading casing). No framework substance changed.

## [0.1.2] · 2026-06-17 · OSS Conventions

### Added

- `CITATION.cff`: citation file format for academic and regulatory referencing.
- `SECURITY.md`: vulnerability disclosure policy and trademark misuse channel.
- `CONTRIBUTING.md`: contribution paths, PR process, style guide.
- `CODE_OF_CONDUCT.md`: Contributor Covenant v2.1.

## [0.1.1] · 2026-06-17 · License and Lint Fixes

### Added

- Apache 2.0 LICENSE with appended trademark notice for the AI IR Overlay and AI IR Overlay Certified word marks.

### Fixed

- Markdown lint corrections across the framework, triage, kill-switches, and evidence directories.

## [0.1.0] · Foundation

The founding release. Establishes the thesis, the framework core, the triage discipline, the containment ladder, and the evidence taxonomy. No playbooks in this release. Playbook 01 ships next, in `v0.2.0`.

### Added: Framework Core

- `framework/00-overview.md`: why an overlay, not a replacement. *(Content absorbed into README.md during v0.6.x cleanup.)*
- `framework/01-minimum-viable-overlay.md`: the four MVO controls.
- `framework/02-mental-model.md`: the four-sentence model.

### Added: Triage

- `triage/six-questions.md`: the first-15-minutes discipline.
- `triage/six-questions-card.md`: printable one-page card.

### Added: Containment

- `kill-switches/overview.md`: the six-mode ladder (M0 through M5) with TTA targets.

### Added: Evidence

- `evidence/minimum-evidence-set.md`: evidence types A–F plus capture order.

### Added: Templates

- `templates/ai-bom.yaml`: machine-readable AI Bill of Materials.
- `templates/agent-privilege-matrix.csv`: Tier 0, 1, and 2 example mapping.

[Unreleased]: https://github.com/jacobideji/aiiroverlay/compare/v0.24.0...HEAD
[0.24.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.24.0
[0.23.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.23.0
[0.22.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.22.0
[0.21.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.21.0
[0.20.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.20.0
[0.19.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.19.0
[0.18.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.18.0
[0.17.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.17.0
[0.16.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.16.0
[0.15.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.15.0
[0.14.3]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.14.3
[0.14.2]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.14.2,
[0.14.1]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.14.1
[0.14.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.14.0
[0.13.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.13.0
[0.12.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.12.0
[0.11.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.11.0
[0.10.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.10.0
[0.9.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.9.0
[0.8.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.8.0
[0.7.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.7.0
[0.6.2]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.6.2
[0.6.1]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.6.1
[0.6.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.6.0
[0.5.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.5.0
[0.4.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.4.0
[0.3.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.3.0
[0.2.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.2.0
[0.1.5]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.5
[0.1.4]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.4
[0.1.3]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.3
[0.1.2]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.2
[0.1.1]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.1
[0.1.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.0
