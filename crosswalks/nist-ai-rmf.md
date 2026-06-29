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

## How to Use This Crosswalk

When responding to an auditor, regulator, or board question framed in AI RMF terms, this crosswalk lets you point to specific AI IR Overlay artifacts as evidence of conformance to the corresponding RMF subcategory.

**Example:** "How does your organization satisfy MANAGE 2.4?"
**Answer:** "We implement the AI IR Overlay Kill-Switch Modes M1–M4, tested quarterly. Our [AI-BOM](../templates/ai-bom.yaml) documents implementation and last-tested dates per agent."

## Status

- **Mapping completeness:** Functions GOVERN, MAP, MEASURE, MANAGE. High-level mapping complete.
- **Coverage gap:** specific RMF subcategories under MEASURE 4.x (Trustworthiness characteristics) need separate playbook treatment in v1.0.
- **Validation:** unreviewed by NIST. This is the maintainer's interpretation, offered in good faith.

## Source

- NIST AI Risk Management Framework (AI RMF 1.0), January 2023.
- NIST AI 600-1, Generative AI Profile, July 2024.

---

*Last revised: 2026-06-29 · Maintainer interpretation, not a NIST publication.*

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
