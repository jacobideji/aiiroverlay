<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Crosswalk — AI IR Overlay vs NIST AI RMF                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Mappings to GOVERN/MAP/MEASURE/MANAGE functions.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

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

The AI-BOM template (distributed as the `template-ai-bom` package) operationalizes:

- **GOVERN 1.6:** *"Mechanisms are in place to inventory AI systems and are resourced according to organizational risk priorities."*
- **MAP 1.1:** *"Intended purposes, potentially beneficial uses, context-specific laws, norms and expectations, and prospective settings in which the AI system will be deployed are understood and documented."*
- **MAP 4.1:** *"Approaches for mapping AI technology and legal risks of its components, including the use of third-party data or software, are in place, followed, and documented."*

**Gap note:** AI RMF does not specify an inventory schema. AI-BOM fills this gap with a concrete YAML template.

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

**Gap note:** AI RMF does not enumerate evidence types. The A–F set provides the operational specification.

### MVO-4 Controlled Re-Enable ↔ MANAGE

Staged recovery operationalizes:

- **MANAGE 4.2:** *"Measurable activities for continual improvements are integrated into AI system updates and include regular engagement with interested parties, including relevant AI actors."*
- **MANAGE 4.3:** *"Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented."*

## How to Use This Crosswalk

When responding to an auditor, regulator, or board question framed in AI RMF terms, this crosswalk lets you point to specific AI IR Overlay artifacts as evidence of conformance to the corresponding RMF subcategory.

**Example:** "How does your organization satisfy MANAGE 2.4?"
**Answer:** "We implement the AI IR Overlay Kill-Switch Modes M1–M4, tested quarterly. Our AI-BOM (`template-ai-bom` package) documents implementation and last-tested dates per agent."

## Status

- **Mapping completeness:** Functions GOVERN, MAP, MEASURE, MANAGE. High-level mapping complete.
- **Coverage gap:** specific RMF subcategories under MEASURE 4.x (Trustworthiness characteristics) need separate playbook treatment in v1.0.
- **Validation:** unreviewed by NIST. This is the maintainer's interpretation, offered in good faith.

## Source

- NIST AI Risk Management Framework (AI RMF 1.0), January 2023.
- NIST AI 600-1, Generative AI Profile, July 2024.

---

*Last revised: 2026-06-17 · Maintainer interpretation, not a NIST publication.*

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
