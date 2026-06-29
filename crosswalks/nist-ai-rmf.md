<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Crosswalk — AI IR Overlay vs NIST AI RMF                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Mappings to GOVERN/MAP/MEASURE/MANAGE functions.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Crosswalk: AI IR Overlay ↔ NIST AI Risk Management Framework (AI RMF 1.0)

This crosswalk maps AI IR Overlay controls to NIST AI RMF functions, with emphasis on the **MANAGE** function (where incident response lives) and the **MEASURE** and **GOVERN** functions where preparation lives.

## At a Glance

| AI IR Overlay Control | NIST AI RMF Function | RMF Subcategory (representative) |
|---|---|---|
| **MVO-1 Inventory** | GOVERN, MAP | GOVERN 1.6, MAP 1.1, MAP 4.1 |
| **MVO-2 Safe Modes (Kill-Switches)** | MANAGE | MANAGE 1.3, MANAGE 2.3, MANAGE 2.4 |
| **MVO-3 Minimum Evidence Set** | MEASURE, MANAGE | MEASURE 2.7, MANAGE 4.1 |
| **MVO-4 Controlled Re-Enable** | MANAGE | MANAGE 4.2, MANAGE 4.3 |
| Six Triage Questions | MAP, MEASURE | MAP 2.3, MEASURE 2.5 |
| Mental Model | GOVERN | GOVERN 1.1 (legal/regulatory), GOVERN 3.2 (human-AI roles) |
| Maturity Roadmap | GOVERN, MEASURE, MANAGE | GOVERN 1.4 (risk-management process), MEASURE 4.2, MANAGE 4.2 (continual improvement) |

## Detailed Mappings

### MVO-1 Inventory ↔ GOVERN + MAP

The [AI-BOM template](../templates/ai-bom.yaml) (see [README](../templates/README-ai-bom.md)) operationalizes:

- **GOVERN 1.6:** *"Mechanisms are in place to inventory AI systems and are resourced according to organizational risk priorities."*
- **MAP 1.1:** *"Intended purposes, potentially beneficial uses, context-specific laws, norms and expectations, and prospective settings in which the AI system will be deployed are understood and documented."*
- **MAP 4.1:** *"Approaches for mapping AI technology and legal risks of its components, including the use of third-party data or software, are in place, followed, and documented."*

**Gap note:** AI RMF does not specify an inventory schema. AI-BOM fills this gap with a concrete YAML template. AI RMF also does not specify the **discovery boundary** that brings previously-undocumented agents into inventory; [Playbook 21: Shadow AI](../playbooks/21-shadow-ai.md) fills this gap with the 24-hour intake standard, identity-level containment fallback discipline, and the migrate/redesign/retire decision path. AI RMF does not specify the **procurement-time precondition** that determines whether a platform can support the response disciplines at all; [Playbook 19: Build vs Buy for Agent Controls](../playbooks/19-build-vs-buy.md) fills this gap with the 60-minute Proof of Readiness Test, the eight critical procurement questions, the Build vs Buy Decision Matrix, and the post-procurement hardening discipline.

**Privacy-discipline gap note:** AI RMF identifies privacy as a trustworthiness characteristic (MEASURE 2.10) and mandates legal/regulatory context including privacy regimes (GOVERN 1.1) plus impact assessment that includes privacy (MAP 5.1), but does not specify the **multi-stakeholder governance discipline** that operationalizes privacy alongside the framework's forensic claims for AI logs. [Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World](../playbooks/23-logging-privacy.md) fills this gap with the Multi-Stakeholder Governance Matrix (Security, Privacy, Legal, and Engineering each holding a defensible interest, a load-bearing artifact, and an acceptance criterion), the Three-Layer Logging Model (Layer 1 metadata broadly retained; Layer 2 selective payload narrowly triggered; Layer 3 escalation capture under legal hold), the Forensically Useful standard (the six core questions logs must answer at Layer 1 alone for typical incidents), and the redaction-and-tokenization discipline with structural preservation.

### MVO-2 Safe Modes ↔ MANAGE

The Kill-Switch Modes (M0–M5) operationalize:

- **MANAGE 1.3:** *"Responses to the AI risks deemed high priority, as identified by the map function, are developed, planned, and documented."*
- **MANAGE 2.3:** *"Procedures are followed to respond to and recover from a previously unknown risk when it is identified."*
- **MANAGE 2.4:** *"Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use."*

**Gap note:** AI RMF specifies the *requirement* to disengage AI systems but not the *graduated mechanism*. The Kill-Switch ladder provides the operational specification.

### MVO-3 Minimum Evidence Set ↔ MEASURE + MANAGE

The Minimum Evidence Set (A–F) operationalizes:

- **MEASURE 2.7:** *"AI system security and resilience, as identified in the map function, are evaluated and documented."*
- **MANAGE 4.1:** *"Post-deployment AI system monitoring plans are implemented, including mechanisms for capturing and evaluating input from users and other relevant AI actors, appeal and override, decommissioning, incident response, recovery, and change management."*

**Gap note:** AI RMF does not enumerate evidence types. The A–F set provides the operational specification. AI RMF also does not specify the **evidence-retention lifecycle** that determines whether captured evidence remains defensible across the regulatory, legal, and business-trust review window where post-incident proof is required; [Playbook 15: Records, Retention, and Proving What Happened](../playbooks/15-records-retention.md) fills this gap with the Two-Tier Retention Standard (metadata-tier and payload-tier windows calibrated per evidence class), the incident-triggered legal-hold mechanism, the chain-of-custody discipline (every access to the evidence store is access-logged with actor identity, timestamp, query, and access purpose), the tamper-evidence anchor (cryptographic integrity hashes computed at capture time and verifiable on subsequent access), and the quarterly Reconstructability Test that empirically validates the framework's evidence claims at 30, 60, and 90 days.

### MVO-4 Controlled Re-Enable ↔ MANAGE

Staged recovery operationalizes:

- **MANAGE 4.2:** *"Measurable activities for continual improvements are integrated into AI system updates and include regular engagement with interested parties, including relevant AI actors."*
- **MANAGE 4.3:** *"Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented."*

**Gap note:** AI RMF specifies the *requirement* for continual improvement integrated with AI system updates (MANAGE 4.2) and for monitoring post-deployment (MANAGE 4.1) but not the *change-event forensics discipline* that connects an observed behavior shift to the specific update that produced it. [Playbook 22: Model and Policy Drift](../playbooks/22-model-policy-drift.md) fills this gap with the Post-Change and Pre-Change Configuration Snapshots, the change-pipeline event ledger, the Drift Canary pack, the layered rollback sequence (tool policies → retriever parameters → system prompt → policy and moderation configuration → memory and context window → tool schemas → retrieval index and corpus version → model version pin), and the M3-Drift kill-switch variant that scopes containment to the specific recently-changed component while pre-change state is restored.

**Communication-discipline gap note:** AI RMF mandates incident communication to AI actors and affected communities (MANAGE 4.3), risk response with stakeholder engagement (MANAGE 3.1), and information sharing including incident disclosure (GOVERN 1.7), but does not specify the AI-specific communication discipline that operationalizes these mandates under incident-response time pressure. [Playbook 17: Communication Techniques for AI-Involved IR](../playbooks/17-communication-techniques.md) fills this gap with the 30-minute first-update SLA, the Three-Status Taxonomy (Confirmed, Suspected, Validating), the Four-Element Update Standard, the Stakeholder Communication Matrix (eight stakeholder classes each with calibrated cadence, content scope, and approval path), the Template Library with version-controlled pre-approved templates per stakeholder class, and the Responsible Reframing discipline that operationalizes the AI accountability framing across every communication artifact.

**Training-discipline gap note:** AI RMF mandates documented and trained human-AI roles (GOVERN 3.2), personnel training adequacy (MAP 3.4), risk-response readiness (MANAGE 1.3), and risk response with stakeholder engagement (MANAGE 3.1), but does not specify the AI-specific training discipline that produces the muscle memory the framework's response time budgets require under operational pressure. [Playbook 16: Training Your Team for AI Incidents](../playbooks/16-training-your-team.md) fills this gap with the 30-Minute Micro-Drill (three time-boxed phases of 10 minutes each: Trigger and Contain, Pull Evidence, Scope and Brief), the Four Core Moves (activate safe mode, preserve and export evidence, scope impact in business terms, communicate with disciplined language), the two permanent operating roles (Safe Mode Owner and Evidence Owner), the Curriculum-of-Six (safe modes, tool tiering, retrieval traces, tool-call logs, memory state, configuration snapshots), the monthly drill cadence with measurable training targets (TTSM ≤ 10 minutes, TTE ≤ 60 minutes, 5-bullet brief inside 30 minutes), and the structured onboarding sequence.

**Executive-decision-making gap note:** AI RMF mandates organizational risk-management decision-making (GOVERN 1.4) and organizational accountability for AI risk (GOVERN 4.1) but does not specify the AI-specific executive-decision discipline that operationalizes accountable decisions under uncertainty during AI incidents. [Playbook 05: Executive Decision-Making With AI in the Loop](../playbooks/05-executive-decision-making.md) fills this gap with the Executive Decision Packet (AI Edition) five-section structured update (Situation, Agent Capability Profile, Provenance Summary, Impact with CIA+T framing, Actions Taken and Next Steps), the CIA+T impact framing that elevates Trust to peer status alongside Confidentiality, Integrity, and Availability, the 4-hour cadence for subsequent packets, the 4/24/72-hour planning horizons, the Three Executive Routine Additions (capability assessment, provenance tracking, approval-chain awareness), and the Approval Receipt discipline that prevents human approval workflows from degrading into rubber-stamping (every high-impact action's approver sees change preview, destination and domain, source citations, and object count or cap before approving).

## How to Use This Crosswalk

When responding to an auditor, regulator, or board question framed in AI RMF terms, this crosswalk lets you point to specific AI IR Overlay artifacts as evidence of conformance to the corresponding RMF subcategory.

**Example:** "How does your organization satisfy MANAGE 2.4?"
**Answer:** "We implement the AI IR Overlay Kill-Switch Modes M1–M4, tested quarterly. Our [AI-BOM](../templates/ai-bom.yaml) documents implementation and last-tested dates per agent."

## Status

- **Mapping completeness:** Functions GOVERN, MAP, MEASURE, MANAGE. High-level mapping complete.
- **Foundational and cross-cutting playbooks:** [Playbook 02: Evidence Lives in New Places](../playbooks/02-evidence-lives-in-new-places.md) establishes the Three Realities of AI Evidence (the actor is a workflow, not a workstation; the payload can be language, not malware; evidence is fragile) as the pedagogical foundation for every MEASURE-function evidence activity. [Playbook 13: The Six Metrics](../playbooks/13-six-metrics.md) operationalizes MEASURE 4.2 (measurement effectiveness gathered and assessed) and feeds the GOVERN 1.4 risk-management process with six measurable quantities (Inventory Currency, Containment Time-to-Activate, Evidence Export Time, Drill Currency, Hardening SLA Compliance, Controlled Re-Enable Success Rate). [Playbook 14: Testing for Agent Failure Modes](../playbooks/14-testing-for-agent-failure-modes.md) operationalizes MEASURE 2.5 (deployed AI system regularly evaluated) and MANAGE 4.1 (post-deployment AI system monitoring plans implemented) through pre-production failure-mode testing of the kill-switch ladder. [Playbook 20: AI IR Maturity Roadmap (operating view)](../playbooks/20-maturity-roadmap.md) operationalizes GOVERN 1.4 (organizational risk-management process maturity) through the four maturity levels (Aware, Containable, Provable, Resilient) and the conformance criteria for each.
- **Coverage gap:** specific RMF subcategories under MEASURE 4.x (Trustworthiness characteristics) need separate playbook treatment in v1.0.
- **Validation:** unreviewed by NIST. This is the maintainer's interpretation, offered in good faith.

## Source

- NIST AI Risk Management Framework (AI RMF 1.0), January 2023.
- NIST AI 600-1, Generative AI Profile, July 2024.

---

*Last revised: 2026-06-29 · Maintainer interpretation, not a NIST publication.*

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
