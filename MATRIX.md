<!-- ────────────────────────────────────────────────────────────────── -->
<!--  AI IR Overlay Framework Matrix                                    -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

# AI IR Overlay Framework Matrix

> *Self-contained tabular reference for the AI IR Overlay™ framework at v0.33.0. Single document, all tables. Distinct from prose narratives elsewhere in the repo: this is the matrix view of the framework, calibrated for board briefings, onboarding, auditor walkthroughs, and one-page references.*

**Current release:** [v0.33.0](https://github.com/jacobideji/aiiroverlay/releases/tag/v0.33.0) · 2026-06-29

## How to read this document

The matrix in [Section 1](#1-the-matrix-response-phases--operational-controls) is the primary artifact: response phases sequenced across the top per NIST SP 800-61 r3; controls, playbooks, and primitives listed in each phase column. Every cell points to a repo artifact that operationalizes the corresponding step.

Sections 2 through 9 expand each cross-cutting reference (kill-switch ladder, evidence taxonomy, metrics, MVO controls, maturity levels, playbook index, standards crosswalk, quick-read legend). Use them as appendices to the matrix.

This document is intended to be:

- **Printable.** Fits on one large screen or two letter pages.
- **Citable.** Section anchors are stable. Cite as `MATRIX.md#section-N`.
- **Auditor-ready.** Every cell traces to a specific file in the repo.

---

## 1. The Matrix: Response Phases × Operational Controls

Rows in each column are the controls, playbooks, and primitives that operate at that phase. Phases are sequenced per NIST SP 800-61 r3 (Preparation, Detection and Analysis, Containment / Eradication / Recovery, Post-Incident Activity), unpacked into seven operationally-distinct columns.

| **Preparation** | **Detection** | **Triage** | **Containment** | **Evidence** | **Recovery** | **Closure** |
|---|---|---|---|---|---|---|
| MVO-1 Inventory (AI-BOM) | PB11 Monitoring + Detection | Six Triage Questions | M0 Observe | A. Prompt and Response Record | MVO-4 Controlled Re-Enable | PB18 Post-Incident Hardening |
| MVO-2 Privilege Matrix | PB13 Inventory Currency | Materiality + Disclosure Trigger | M1 Read-Only | B. Tool-Call Ledger | PB14 Failure-Mode Testing | PB15 Records Retention |
| PB01 Agent as Privileged Identity | PB14 Pre-Production Testing | Executive Decision Packet (PB05) | M2 Approvals Required | C. Retrieval Traces | PB22 Drift Canary pack | PB23 AI Logging and Privacy |
| PB02 Three Realities of AI Evidence | PB21 Shadow AI Discovery | CIA+T Impact Framing (PB05) | M3 Tool Tiering | D. Memory Snapshot | Layered Rollback (PB22) | PB17 Stakeholder Communication |
| PB04 Tool Design (T0 / T1 / T2) | PB22 Change-Event Drift Detection | Approval Receipt Discipline (PB05) | M3-RAG (PB03) | E. Configuration Snapshot | | PB16 Training and Drills |
| PB07 Secrets and Tokens | Drift Canary pack (PB22) | Three-Status Taxonomy (PB17) | M3-Workflow (PB06) | F. Identity + SaaS Audit Correlation | | PB24 Board-Ready Scorecard |
| PB10 Vendor Copilots | | | M3-Output (PB09) | PB03 Type C deep-dive | | Reconstructability Test (PB15) |
| PB19 Build vs Buy | | | M3-Vendor (PB10) | PB09 Type F deep-dive (output distribution map) | | Two-Tier Retention Standard (PB15) |
| PB20 Maturity Roadmap | | | M3-Delegation Cap (PB08) | PB15 Lifecycle deep-dive | | Three-Layer Logging Model (PB23) |
| PB21 Shadow AI Discovery | | | M3-Drift (PB22) | PB23 Privacy companion | | Forensically Useful standard (PB23) |
| 60-min Proof of Readiness Test (PB19) | | | M4 Full Disable | | | Multi-Stakeholder Governance Matrix (PB23) |
| 24-hr Shadow Agent Intake (PB21) | | | M5 Controlled Re-Enable | | | Responsible Reframing Discipline (PB17) |
| Mental Model (four sentences) | | | PB08 Multi-Agent containment | | | |
| | | | PB12 Insider Threat variants | | | |

**How to use the matrix.** Identify the phase you are in, scan the column for the relevant controls, follow the parenthetical playbook reference to the deep-dive. Every primitive (M3-RAG, A through F, CIA+T, Six Triage Questions, etc.) has a canonical home in the repo; the sections below are the index.

---

## 2. Kill-Switch Ladder (Containment column expanded)

The canonical containment surface. Modes M0 through M5 are conformance scope; M3 variants are operational refinements documented in their source playbook.

| Mode | Name | Use When | Activation SLA | Owner | Source |
|---|---|---|---|---|---|
| **M0** | Observe | Normal operations | n/a | Owner | [`kill-switches/overview.md`](kill-switches/overview.md) |
| **M1** | Read-Only | Suspicious behavior; low to moderate impact | ≤ 10 min | Tier-1 SOC | [`kill-switches/overview.md`](kill-switches/overview.md) |
| **M2** | Approvals Required | Agent must keep operating; actions need two-person rule | ≤ 10 min | Tier-1 SOC | [`kill-switches/overview.md`](kill-switches/overview.md) |
| **M3** | Tool Tiering | Targeted containment; disable high-risk tools only | ≤ 10 min | Tier-1 SOC | [`kill-switches/overview.md`](kill-switches/overview.md) |
| **M4** | Full Disable | Active harm, confirmed misuse, or evidence of compromise | ≤ 10 min | Tier-1 SOC | [`kill-switches/overview.md`](kill-switches/overview.md) |
| **M5** | Controlled Re-Enable | Containment validated; staged recovery | n/a | CISO / IC | [`kill-switches/overview.md`](kill-switches/overview.md) |

### M3 Variants (operational refinements, not new mode numbers)

| Variant | What It Scopes | Use When | Source |
|---|---|---|---|
| **M3-RAG** | M3 applied to the retrieval layer | Suspected corpus poisoning | [PB03](playbooks/03-rag-knowledge-base-forensics.md) |
| **M3-Workflow** | M3 applied to the content channel feeding the agent | Workflow injection through a corpus, queue, or inbox | [PB06](playbooks/06-prompt-injection-workflow.md) |
| **M3-Output** | M3 applied to a specific output channel or destination class | Output-leakage incident | [PB09](playbooks/09-output-leakage.md) |
| **M3-Vendor** | M3 executed vendor-side for a vendor-managed agent | Vendor copilot under shared responsibility | [PB10](playbooks/10-vendor-copilots.md) |
| **M3-Delegation Cap** | M3 applied to inter-agent delegation depth | Cascade propagating through deep delegation chains | [PB08](playbooks/08-multi-agent-blast-radius.md) |
| **M3-Drift** | M3 scoped to a recently-changed component; pre-change state restored | Change-window analysis identifies a specific component | [PB22](playbooks/22-model-policy-drift.md) |
| **M4 (corpus-scoped)** | M4 bounded to a specific corpus | Active misuse confirmed against one corpus | [PB12](playbooks/12-insider-threat-3.md) |
| **Agent suspended for user** | M4 bounded to a specific user identity | Single user is the suspect | [PB12](playbooks/12-insider-threat-3.md) |

---

## 3. Minimum Evidence Set (Evidence column expanded)

The six AI-agent-specific evidence types that disappear fastest in an incident. Capture order matters; evidence is fragile.

| Code | Evidence Type | What It Captures | Deep-Dive |
|---|---|---|---|
| **A** | Prompt and Response Record | Full prompt context plus response output for the suspect window | [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) |
| **B** | Tool-Call Ledger | Action log: every tool invocation, parameter, destination, return | [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) |
| **C** | Retrieval Traces | RAG and knowledge-base retrieval records: query, retrieved chunks, source documents | [PB03 Type C deep dive](playbooks/03-rag-knowledge-base-forensics.md) |
| **D** | Memory Snapshot | Agent memory state if persistent memory is enabled | [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) |
| **E** | Configuration Snapshot | Model version, system prompt, policy configuration, tool schema, retriever parameters | [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) |
| **F** | Identity and SaaS Audit-Log Correlation | Identity-side and SaaS-side audit-log records that corroborate the AI evidence; extended by the output distribution map for output-leakage incidents | [PB09 Type F deep dive](playbooks/09-output-leakage.md) |

### Evidence Discipline Concepts

| Concept | Source | What It Specifies |
|---|---|---|
| **60-minute Minimum Evidence Set export SLA** | MVO-3 | Drill-measured target for capturing A through F |
| **Two-Tier Retention Standard** | [PB15](playbooks/15-records-retention.md) | Metadata-tier vs payload-tier retention windows calibrated per evidence class |
| **Chain-of-custody discipline** | [PB15](playbooks/15-records-retention.md) | Tamper-evident integrity for A through F |
| **Incident-triggered legal-hold mechanism** | [PB15](playbooks/15-records-retention.md) | Hold escalation when retention windows extend |
| **Reconstructability Test (quarterly at 30, 60, 90 days)** | [PB15](playbooks/15-records-retention.md) | Empirical validation that captured evidence still tells the story |
| **Three-Layer Logging Model** | [PB23](playbooks/23-logging-privacy.md) | Layer 1 metadata broadly retained · Layer 2 selective payload narrowly triggered · Layer 3 escalation under legal hold |
| **Forensically Useful standard** | [PB23](playbooks/23-logging-privacy.md) | Six questions logs must answer through metadata alone |
| **Redaction-and-tokenization discipline** | [PB23](playbooks/23-logging-privacy.md) | Role-separated access with audited break-glass |
| **Multi-Stakeholder Governance Matrix** | [PB23](playbooks/23-logging-privacy.md) | Security / Privacy / Legal / Engineering joint governance |
| **Output distribution map** | [PB09](playbooks/09-output-leakage.md) | Type F extension scoping output-leakage incidents (per destination, per recipient) |

---

## 4. Six Metrics (Measurement Discipline)

The six metrics from PB13. Two have canonical acronyms (TTSM, TTE); the others use full names.

| # | Metric | Maps To | Standards mapping (per PB13) |
|---|---|---|---|
| 1 | **Inventory Currency** | AI-BOM freshness within the 7-day window | NIST AI RMF GOVERN 1.6 |
| 2 | **Containment Time-to-Activate (TTSM)** | M1 through M4 activation latency from declaration | NIST CSF 2.0 RS.MA-04 |
| 3 | **Evidence Export Time (TTE)** | A through F capture latency from declaration | NIST AI RMF MEASURE 2.7 + MANAGE 4.1 |
| 4 | **Drill Currency** | Last live drill of M1 through M4 against drill-measured targets | NIST AI RMF MANAGE 2.4 |
| 5 | **Hardening SLA Compliance** | [PB18](playbooks/18-post-incident-hardening.md) 5-business-day hardening backlog burndown | NIST AI RMF MANAGE 4.2 |
| 6 | **Controlled Re-Enable Success Rate** | MVO-4 staged recovery success rate over rolling window | NIST AI RMF MANAGE 4.3 |

---

## 5. MVO Controls (Framework Foundation)

The four Minimum Viable Overlay controls. See [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md) for the full specification.

| Code | Name | Extends | What It Adds for AI Agents |
|---|---|---|---|
| **MVO-1** | Inventory | NIST CSF 2.0 ID.AM | AI-BOM: agent identity, tooling, write targets, retrieval corpora, memory configuration in one canonical artifact |
| **MVO-2** | Safe Modes | NIST SP 800-61 r3 containment | Graduated kill-switch ladder M0 through M5 calibrated to agent action surface |
| **MVO-3** | Minimum Evidence Set | NIST SP 800-61 r3 evidence | Six AI-agent-specific evidence types A through F; 60-minute export SLA |
| **MVO-4** | Controlled Re-Enable | NIST CSF 2.0 RC.RP | Staged re-enablement pattern with validation gates |

---

## 6. Maturity Levels (Adoption Discipline)

Four levels from [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md).

| Level | Name | One-Sentence Definition | Required Controls |
|---|---|---|---|
| **1** | Aware | The organization has basic visibility into its AI assets | MVO-1 |
| **2** | Containable | Harm can be contained without a complete shutdown | MVO-1 + MVO-2 |
| **3** | Provable | The organization can demonstrate scope under time pressure | Level 2 + MVO-3 |
| **4** | Resilient | Continuous improvement with measured recovery | Level 3 + MVO-4 + [PB13](playbooks/13-six-metrics.md) + [PB14](playbooks/14-testing-for-agent-failure-modes.md) |

---

## 7. Playbook Quick Reference (PB01 through PB24)

All 24 playbooks. Category assignments per the [README reading order](README.md#reading-order).

| ID | Title | Category | Key Concept Introduced |
|---|---|---|---|
| [**PB01**](playbooks/01-agent-as-privileged-identity.md) | Agent as Privileged Identity | Foundation | The privileged-identity lens; operational keystone |
| [**PB02**](playbooks/02-evidence-lives-in-new-places.md) | Evidence Lives in New Places | Foundation | Three Realities of AI Evidence |
| [**PB03**](playbooks/03-rag-knowledge-base-forensics.md) | RAG and Knowledge-Base Forensics | Measurement and Depth | 90-minute Freeze-the-World sequence; M3-RAG; Type C deep-dive |
| [**PB04**](playbooks/04-tool-design-is-containment.md) | Tool Design Is Containment | Prevention | Tool tiering T0 / T1 / T2 |
| [**PB05**](playbooks/05-executive-decision-making.md) | Executive Decision-Making | Governance | Executive Decision Packet; CIA+T framing; Approval Receipt |
| [**PB06**](playbooks/06-prompt-injection-workflow.md) | Prompt Injection as Workflow Threat | Operations | M3-Workflow containment |
| [**PB07**](playbooks/07-secrets-and-tokens.md) | Secrets and Tokens | Operations | Credential discipline for agent world |
| [**PB08**](playbooks/08-multi-agent-blast-radius.md) | Multi-Agent Blast Radius | Operations | Orchestrator-first containment; M3-Delegation Cap |
| [**PB09**](playbooks/09-output-leakage.md) | Leakage Without a Breach | Operations | Output distribution map; M3-Output; Type F deep-dive |
| [**PB10**](playbooks/10-vendor-copilots.md) | Vendor Copilots and Mutual Responsibility | Operations | M3-Vendor; quarterly Vendor Evidence Drill |
| [**PB11**](playbooks/11-monitoring-detection.md) | Monitoring That Truly Detects | Operations | Three signal families for authorized misuse |
| [**PB12**](playbooks/12-insider-threat-3.md) | Insider Threat 3.0 | Operations | Capability-intent-impact triad; HR/Legal engagement |
| [**PB13**](playbooks/13-six-metrics.md) | The Six Metrics | Measurement and Depth | The Six Metrics |
| [**PB14**](playbooks/14-testing-for-agent-failure-modes.md) | Testing for Agent Failure Modes | Measurement and Depth | Pre-production kill-switch testing |
| [**PB15**](playbooks/15-records-retention.md) | Records, Retention, and Proving What Happened | Measurement and Depth | Two-Tier Retention; Reconstructability Test |
| [**PB16**](playbooks/16-training-your-team.md) | Training Your Team | Measurement and Depth | 30-Minute Micro-Drill; Four Core Moves; Curriculum-of-Six |
| [**PB17**](playbooks/17-communication-techniques.md) | Communication Techniques | Governance | 30-minute first-update SLA; Three-Status Taxonomy; Responsible Reframing |
| [**PB18**](playbooks/18-post-incident-hardening.md) | Post-Incident Hardening | Closure | 5-business-day hardening SLA |
| [**PB19**](playbooks/19-build-vs-buy.md) | Build vs Buy for Agent Controls | Prevention | 60-minute Proof of Readiness Test; eight critical procurement questions |
| [**PB20**](playbooks/20-maturity-roadmap.md) | AI IR Maturity Roadmap (operating view) | Operations | Operating view of `framework/03` |
| [**PB21**](playbooks/21-shadow-ai.md) | Shadow AI Discovery | Operations | 60-minute Discovery Snapshot; 24-hour Intake Standard |
| [**PB22**](playbooks/22-model-policy-drift.md) | Model and Policy Drift | Measurement and Depth | M3-Drift; Post-Change Configuration Snapshot; Drift Canary pack |
| [**PB23**](playbooks/23-logging-privacy.md) | AI Logging and Privacy in a Multi-Stakeholder World | Measurement and Depth | Three-Layer Logging Model; Forensically Useful standard |
| [**PB24**](playbooks/24-board-ready-scorecard.md) | Board-Ready Scorecard | Governance | Containment / Evidence / Governance / Recovery domains |

---

## 8. Standards Crosswalk Summary

| Standard | Crosswalk File | Coverage Posture |
|---|---|---|
| **NIST AI RMF 1.0** | [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) | MVO-1 → GOVERN/MAP · MVO-2 → MANAGE · MVO-3 → MEASURE/MANAGE · MVO-4 → MANAGE |
| **NIST CSF 2.0 + SP 800-61 r3** | [`crosswalks/nist-csf-2.md`](crosswalks/nist-csf-2.md) | DETECT (PB11) · PR.AA-05 (PB07) · PR.DS-01 (PB03 + PB06; PB23 for AI logs) · RS.AN-06 and RS.AN-07 (PB15) |
| **OWASP Top 10 Agentic 2026** | [`crosswalks/owasp-agentic-top-10.md`](crosswalks/owasp-agentic-top-10.md) | ASI04 (PB10) · ASI07 + ASI08 (PB08) · ASI10 (PB12) |
| **ISO/IEC 27035** | forthcoming | Planned community contribution lane (referenced in `framework/01`) |
| **ISO/IEC 42001:2023** | forthcoming | Planned community contribution lane |
| **EU AI Act (Reg 2024/1689)** | forthcoming | Planned community contribution lane |

---

## 9. Quick-Read Legend

- **Phase**: where in the incident lifecycle the control activates
- **Source**: the file in the repo where the control is canonically defined
- **PB**: playbook (1 through 24)
- **MVO**: Minimum Viable Overlay (the four foundation controls)
- **M0 through M5**: the canonical Kill-Switch Modes
- **A through F**: the Minimum Evidence Set types
- **TTSM**: Time-to-Safe-Mode (Metric 2 acronym)
- **TTE**: Time-to-Evidence (Metric 3 acronym)
- **CIA+T**: Confidentiality, Integrity, Availability, Trust (PB05 impact-framing extension)

For the full acronym list see the [README Acronyms section](README.md#acronyms).

---

## Source

*This matrix synthesizes the AI IR Overlay™ framework at v0.33.0. It will be revised as the framework evolves toward v1.0.0 and as the Steering Committee announcement and external contributions land. Suggested edits welcome via Pull Request per [`CONTRIBUTING.md`](CONTRIBUTING.md).*

*Source: AI IR Overlay framework, by Jacob Ideji.*

*Last revised: 2026-06-29 (v0.33.0 introduction).*

<https://www.linkedin.com/in/jacobideji/>
