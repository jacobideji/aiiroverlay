<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Crosswalk — AI IR Overlay vs NIST CSF 2.0                                                             -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Mappings to the six CSF 2.0 functions: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Crosswalk: AI IR Overlay ↔ NIST Cybersecurity Framework 2.0 (CSF 2.0)

This crosswalk maps AI IR Overlay controls to NIST CSF 2.0 functions and categories. CSF 2.0 (February 2024) introduced **GOVERN** as a sixth function and is the foundation for NIST SP 800-61 r3's incident-response Community Profile (April 2025).

The crosswalk gives auditors, regulators, and boards a direct path from AI IR Overlay conformance to CSF 2.0 outcomes, and by extension, to SP 800-61 r3 alignment.

## At a Glance

| AI IR Overlay Control | Primary CSF 2.0 Function(s) | Categories |
|---|---|---|
| **MVO-1 Inventory** | IDENTIFY (+ GOVERN) | ID.AM, GV.OC, GV.RR |
| **MVO-2 Safe Modes (Kill-Switches)** | RESPOND | RS.MA, RS.MI |
| **MVO-3 Minimum Evidence Set** | RESPOND (+ DETECT) | RS.AN, DE.AE |
| **MVO-4 Controlled Re-Enable** | RECOVER | RC.RP, RC.CO |
| Six Triage Questions | RESPOND | RS.MA, RS.AN |
| Mental Model | GOVERN (+ PROTECT) | GV.PO, GV.RM, PR.AA |
| Maturity Roadmap | IDENTIFY + GOVERN | ID.IM, GV.OV |

## Detailed Mappings

### MVO-1 Inventory ↔ IDENTIFY + GOVERN

The [AI-BOM template](../templates/ai-bom.yaml) (see [README](../templates/README-ai-bom.md)) operationalizes:

- **ID.AM-01:** *"Inventories of hardware managed by the organization are maintained."* Extends to runtime hosts of AI agents.
- **ID.AM-02:** *"Inventories of software, services, and systems managed by the organization are maintained."* Captures agent platforms, model providers, retrieval frameworks.
- **ID.AM-04:** *"Inventories of services provided by suppliers are maintained."* Captures SaaS targets the agent can write to.
- **ID.AM-05:** *"Assets are prioritized based on classification, criticality, resources, and impact."* The `risk_tier` field on each tool drives prioritization.
- **GV.OC-02:** *"Internal and external stakeholders are understood…"* The `business_owner` and `technical_owner` fields per agent satisfy this.
- **GV.RR-02:** *"Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced."* Owner assignment is mandatory in AI-BOM.

**Gap note:** CSF 2.0 doesn't specify an inventory schema for AI agents. AI-BOM fills the gap with a concrete YAML template.

### MVO-2 Safe Modes ↔ RESPOND

The Kill-Switch Modes (M0–M5) operationalize:

- **RS.MA-01:** *"The incident response plan is executed in coordination with relevant third parties once an incident is declared."* Modes are activated as part of the documented IR plan.
- **RS.MA-04:** *"Incidents are escalated or elevated as needed."* TTA ≤ 10 min for Tier-1 SOC is the escalation criterion for M1–M4.
- **RS.MI-01:** *"Incidents are contained."* M1 (Read-Only), M2 (Approvals), M3 (Tool Tiering), and M4 (Full Disable) provide graduated containment.
- **RS.MI-02:** *"Incidents are eradicated."* The M4 → M5 sequence requires evidence capture before token rotation.

**Gap note:** CSF 2.0 specifies that incidents must be contained but not *how* to graduate containment to preserve business value while preventing harm. The six-mode ladder fills this operational gap.

### MVO-3 Minimum Evidence Set ↔ RESPOND (with DETECT inputs)

The Six Evidence Types (A–F) operationalize:

- **RS.AN-03:** *"Analysis is performed to establish what has occurred during an incident."* Types A (prompts), B (tool calls), and F (downstream audit logs) directly support this.
- **RS.AN-06:** *"Actions performed during an investigation are recorded, and the records' integrity and provenance are preserved."* The capture order (Step 1 → Step 2 → Step 3) with snapshot-before-rotation enforces this discipline.
- **RS.AN-07:** *"Incident data and metadata are collected, and their integrity and provenance are preserved."* Each A–F type has a documented capture format and retention window.
- **DE.AE-02:** *"Potentially adverse events are analyzed to better understand associated activities."* Type A (prompts/responses) is the primary input.
- **DE.AE-03:** *"Information is correlated from multiple sources."* Type F (Identity and SaaS Audit-Log Correlation) is the multi-source correlation step.

**Gap note:** CSF 2.0 mandates evidence collection and preservation but doesn't enumerate AI-specific evidence types. The A–F set provides the operational specification.

### MVO-4 Controlled Re-Enable ↔ RECOVER

Staged recovery operationalizes:

- **RC.RP-01:** *"The recovery portion of the incident response plan is executed once initiated from the incident response process."* M5 follows a documented sequence (M1 read-only → validate → replay → incremental re-enable → M0).
- **RC.RP-02:** *"Recovery actions are selected, scoped, prioritized, and performed."* Staged tool re-enablement starts with the lowest-risk tier.
- **RC.RP-03:** *"The integrity of backups and other restoration assets is verified before using them for restoration."* Corpora versions confirmed clean is an explicit step.
- **RC.RP-04:** *"Critical mission functions and cybersecurity risk management are considered to establish post-incident operational norms."* The approver is the CISO or Incident Commander, not the original agent owner alone.
- **RC.CO-03:** *"Recovery activities and progress are communicated to internal and external stakeholders."* Post-incident hardening communication is documented in [Playbook 18: Post-Incident Hardening](../playbooks/18-post-incident-hardening.md).

### Six Triage Questions ↔ RESPOND

The first-hour discipline operationalizes:

- **RS.MA-02:** *"Incident reports are triaged and validated."* The six questions are the validation checklist.
- **RS.MA-04:** *"Incidents are escalated or elevated as needed."* Q5 (the least-disruptive safe mode) determines escalation level.
- **RS.AN-03:** *"Analysis is performed to establish what has occurred during an incident."* Q1–Q4 establish scope, and Q6 protects evidence required for analysis.

### Mental Model ↔ GOVERN + PROTECT

The four-clause model operationalizes:

- **GV.PO-01:** *"Policy for managing cybersecurity risks is established based on organizational context, cybersecurity strategy, and priorities."* The four clauses are an organization-level policy lens for AI agents.
- **GV.RM-02:** *"Risk appetite and risk tolerance statements are established, communicated, and maintained."* Clause-by-clause appetite (acts, remembers, retrieves, changes) supports tolerance articulation.
- **PR.AA-01 / PR.AA-05:** Identity/credential management and access policies. The *"if it can act, govern it as a privileged identity"* clause maps directly to existing PAM disciplines for service accounts and OAuth grants.
- **PR.AT-01:** *"Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind."* Insider Threat 3.0 response requires HR, Legal, and the Incident Commander to be trained in joint-engagement protocols and AI-mediated misuse investigation ([Playbook 12: Insider Threat 3.0](../playbooks/12-insider-threat-3.md)).

### Maturity Roadmap ↔ IDENTIFY + GOVERN

The four-level model operationalizes:

- **ID.IM-01:** *"Improvements are identified from evaluations."* Level 4 (Resilient) requires measured improvement over rolling 90-day windows.
- **ID.IM-02:** *"Improvements are identified from security tests and exercises…"* Quarterly tabletops are the Level 4 driver.
- **GV.OV-01:** *"Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction."* The board-question mapping in the Maturity Roadmap supports OV-01 reviews.
- **GV.OV-02:** *"The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organizational requirements and risks."* The Level 1–4 progression is the review structure.

## How to Use This Crosswalk

When responding to an auditor, regulator, board member, or downstream contributor framing a question in CSF 2.0 terms, this crosswalk provides direct evidence of AI IR Overlay conformance.

**Example:** *"How does your organization satisfy RS.MI-01 (incidents are contained) for your AI agents?"*

**Answer:** *"We implement the AI IR Overlay Kill-Switch Modes M1–M4 (Read-Only, Approvals Required, Tool Tiering, Full Disable), tabletop-tested quarterly per the [Kill-Switch Modes specification](../kill-switches/overview.md). Our [AI-BOM](../templates/ai-bom.yaml) documents which modes each agent supports, with last-tested dates and measured Time-to-Activate (TTA) values."*

## Relationship to SP 800-61 r3

NIST SP 800-61 r3 (April 2025) is itself a CSF 2.0 Community Profile for incident response. The AI IR Overlay can be read as an **AI-specific extension** of SP 800-61 r3:

- SP 800-61 r3 establishes incident-response outcomes per CSF 2.0 function, particularly RESPOND and RECOVER.
- The AI IR Overlay specifies *how* those outcomes are achieved for AI agents: Inventory schema (AI-BOM), six-mode containment ladder, six evidence types, staged recovery procedure.

A future release will formalize this layered relationship in a companion SP 800-61 r3 ↔ AI IR Overlay crosswalk. See [CHANGELOG.md](../CHANGELOG.md) `[Unreleased]` for status.

## Status

- **Mapping completeness:** all six CSF 2.0 functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER) have substantive playbook coverage. GV.SC (supply chain risk management) procurement-time discipline for AI platforms is covered by [Playbook 19: Build vs Buy for Agent Controls](../playbooks/19-build-vs-buy.md). ID.AM (asset management) operational discipline for AI agents, including the Shadow AI discovery boundary that closes the inventory-gap precondition, is covered by [Playbook 21: Shadow AI](../playbooks/21-shadow-ai.md). ID.RA (risk assessment of change events) and PR.PS (platform security configuration management) applied to AI agents are covered by [Playbook 22: Model and Policy Drift](../playbooks/22-model-policy-drift.md), with the change-pipeline event ledger and the Post-Change Configuration Snapshot as the empirical evidence that supports both subcategories. PR.AA-05 (access policies on AI agent identities) is covered by [Playbook 07: Secrets and Tokens](../playbooks/07-secrets-and-tokens.md). PR.DS-01 (data-at-rest protection for agent memory and retrieval corpora, and for the evidence store itself) is covered by [Playbook 03: RAG / Knowledge-Base Forensics](../playbooks/03-rag-knowledge-base-forensics.md) (corpus and vector-store integrity discipline), [Playbook 06: Rethinking Prompt Injection as a Workflow Threat](../playbooks/06-prompt-injection-workflow.md) (content-trust labeling at the ingestion boundary), and [Playbook 15: Records, Retention, and Proving What Happened](../playbooks/15-records-retention.md) (the evidence store as a Tier-T2 asset with chain-of-custody discipline, tamper-evident integrity, and the Two-Tier Retention Standard). PR.DS-02 (data-in-transit protection on the output path, including output-layer DLP, channel classification, and destination-aware approval gates) is covered by [Playbook 09: Leakage Without a Breach](../playbooks/09-output-leakage.md). DE.CM (continuous monitoring) is covered by [Playbook 11: Monitoring That Truly Detects Agent Incidents](../playbooks/11-monitoring-detection.md) and extended by [Playbook 22: Model and Policy Drift](../playbooks/22-model-policy-drift.md) along the drift-detection dimension (tool-invocation-frequency, retrieval-pattern, and refusal-pattern signals that surface change-event regressions independent of any specific external trigger). **RS.AN-06** (actions performed during an investigation are recorded; records' integrity and provenance are preserved) and **RS.AN-07** (incident data and metadata are collected; their integrity and provenance are preserved) are covered by [Playbook 15: Records, Retention, and Proving What Happened](../playbooks/15-records-retention.md), with the chain-of-custody discipline, the tamper-evidence anchor, the integrity manifest, and the quarterly Reconstructability Test as the empirical artifacts that support both subcategories.
- **Validation:** unreviewed by NIST. This is the maintainer's interpretation, offered in good faith.

## Source

- NIST Cybersecurity Framework 2.0, February 26, 2024.
- NIST SP 800-61 r3, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*, April 3, 2025.

---

*Last revised: 2026-06-29 · Maintainer interpretation, not a NIST publication.*

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
