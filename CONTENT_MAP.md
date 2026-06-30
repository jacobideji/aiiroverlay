# Content Map: Newsletter Issues to Repository Files

This repository's framework, playbooks, crosswalks, and templates trace back to the *AI IR Overlay™* LinkedIn newsletter series authored by Jacob Ideji (2025 through 2026). Each newsletter issue has a specific home in this repo. This file is the canonical "where did this come from?" reference.

## How releases ship

The framework ships incrementally. Earlier plans assumed one playbook per release in newsletter order: PB01 in `v0.2`, PB02 in `v0.3`, and so on. The actual ship arc has been narrative-driven instead:

1. **Foundation** (`v0.1.x`): framework core, triage, kill-switches, evidence, templates.
2. **Response** (`v0.2.0`): Playbook 01 establishes the privileged-identity lens that every later playbook builds on.
3. **Prevention** (`v0.3.0`): Playbook 04 (Tool Design) closes the most leveraged pre-incident gap.
4. **Closure** (`v0.4.0`): Playbook 18 (Post-Incident Hardening) completes the incident arc.
5. **Governance** (`v0.5.0`): Playbook 24 (Board-Ready Scorecard) translates the arc into executive posture.
6. **Measurement and Depth** (`v0.6.0`): Playbook 13 (Six Metrics), Playbook 03 (RAG Forensics), and Playbook 14 (Testing) make the arc measurable and operationally deep.

The remaining playbooks ship as future MINOR releases. `v1.0.0` is cut once the remaining playbook ships (the target is 24 playbooks; PB02 was originally absorbed into the framework core in `v0.1.0` and was subsequently promoted to a separate foundational-concepts playbook in `v0.23.0` to honor the "every newsletter issue maps to one playbook" provenance principle from the [README](README.md)) and a Steering Committee is announced. See [GOVERNANCE.md](GOVERNANCE.md).

### Why 24 playbooks shipped (content gate complete)

The 24 currently-shipped playbooks (PB01 through PB24, with no absorptions remaining after PB02's promotion in v0.23.0) were prioritized along three axes:

#### 1. Standards-gap closure

Playbooks that closed a specific function in **NIST CSF 2.0** or a category in the **OWASP Top 10 for Agentic Applications 2026** shipped first so the framework's standards posture stayed coherent.

**NIST CSF 2.0 function closures:**

- **PB11** closed **DETECT**
- **PB07** closed **PR.AA-05**
- **PB03 + PB06** closed **PR.DS-01**
- **PB15** closed **RS.AN-06 and RS.AN-07** (records integrity and provenance)
- **PB23** closed **PR.DS-01** (privacy controls applied to AI logs) and **PR.AA** (access control on the evidence store)

**OWASP Agentic Top 10 category closures:**

- **PB08** closed **ASI07 and ASI08**
- **PB10** closed **ASI04**
- **PB12** closed **ASI10**

#### 2. Operational arc completeness

Foundation, Prevention, Closure, Governance, Measurement, and depth on retrieval ship before scenario-specific playbooks so the framework reads as a complete arc rather than a list of scenarios.

**The six-stage operational arc:**

- **Foundation**: PB01 (Agent as Privileged Identity)
- **Prevention**: PB04 (Tool Design Is Containment)
- **Closure**: PB18 (Post-Incident Hardening)
- **Governance**: PB24 (Board-Ready Scorecard)
- **Measurement**: PB13 (Six Metrics) and PB14 (Testing for Agent Failure Modes)
- **Depth on retrieval**: PB03 (RAG and Knowledge-Base Forensics)

**Evidence taxonomy full-depth coverage (MVO-3):**

- PB03 is the **Type C deep-dive**
- PB09 is the **Type F deep-dive**
- PB15 is the **lifecycle deep-dive** across all six evidence types
- PB23 is the **privacy-discipline companion** to PB15 that specifies how each evidence type is captured without overcollecting regulated data

Together PB15 and PB23 form the **capture / retain / prove triad** on top of the Minimum Evidence Set: PB23 specifies how to capture; PB15 specifies how to retain and prove.

#### 3. 2026 production-pattern relevance

Playbooks that map to deployment patterns common in current production AI agents ship before less-time-sensitive scenarios. Each closes a specific precondition that prior playbooks assumed but did not specify:

- **PB09 (Output Leakage)** closes the dominant 2026 data-incident class: confidentiality failures stemming from AI outputs rather than traditional breach vectors. Completes the **input → context → output coverage triad** with PB06 + PB03 and introduces the **M3-Output containment variant** plus output-layer DLP and channel classification as architectural defense.

- **PB21 (Shadow AI)** closes the **inventory-gap precondition** that makes every other playbook's discipline applicable to only the documented portion of the agent fleet; without Shadow AI discovery the AI-BOM is incomplete by definition. Introduces the **60-minute Discovery Snapshot**, the **24-hour Shadow Agent Intake Standard**, identity-level containment for non-modifiable runtimes, the **migrate / redesign / retire decision path**, and the four-boundary hardening including the governed integration path that prevents the next shadow agent from staying shadow.

- **PB19 (Build vs Buy for Agent Controls)** closes the **procurement-time precondition** that determines whether the response playbooks' commitments can be honored at all. Introduces the **60-minute Proof of Readiness Test**, the **eight critical procurement questions**, the **Build vs Buy Decision Matrix**, and the post-procurement hardening that converts platform-capability gaps into contractual commitments or customer-side build commitments.

- **PB22 (Model and Policy Drift)** closes the **change-event precondition**. Prior playbooks assume the AI system is operating in a steady state, but production AI systems are constantly evolving through model upgrades, prompt edits, policy tunes, retriever changes, and index rebuilds. Introduces the **change-window forensics discipline** (Post-Change Configuration Snapshot, change-pipeline event ledger, Drift Canary pack, layered rollback) and the **M3-Drift kill-switch variant**. PB22 and PB14 form the **pre-production-testing and continuous-monitoring pair**.

- **PB15 (Records, Retention, and Proving What Happened)** closes the **proof-discipline precondition**. Prior playbooks specify what to capture and the 60-minute export discipline, but proof requires retention that survives the regulatory, legal, and business-trust review window. Introduces the **Two-Tier Retention Standard** (metadata-tier vs payload-tier windows calibrated per evidence class), the **incident-triggered legal-hold mechanism**, the **chain-of-custody discipline** with tamper-evident integrity, and the quarterly **Reconstructability Test**.

- **PB23 (AI Logging and Privacy in a Multi-Stakeholder World)** closes the **privacy-discipline precondition**. AI logs themselves carry regulated content (PII, PHI, secrets, customer-confidential data) and require multi-stakeholder governance to be defensible by Security, Privacy, Legal, and Engineering simultaneously. Introduces the **Multi-Stakeholder Governance Matrix**, the **Three-Layer Logging Model** (Layer 1 metadata broadly retained, Layer 2 selective payload narrowly triggered, Layer 3 escalation capture under legal hold), the **Forensically Useful standard** (six questions logs must answer through metadata alone for typical incidents), and the **redaction-and-tokenization discipline** with role-separated access controls and audited break-glass procedures.

- **PB17 (Communication Techniques)** closes the **communication-discipline precondition**. Prior playbooks specify what the response team does technically, but stakeholder trust through the response window depends on what the response team says. Introduces the **30-minute first-update SLA**, the **Three-Status Taxonomy** (Confirmed, Suspected, Validating), the **Four-Element Update Standard** (factual impact, immediate containment, evidence-collection activity, next-update timing), the **Stakeholder Communication Matrix** (internal executive, internal business owners, affected end-users, customers, regulator, board, press, employees broadly), the **Template Library** with version-controlled pre-approved templates per stakeholder class, and the **Responsible Reframing discipline** that converts anthropomorphizing language ("the AI did it") to system-accountability language ("an authorized automation behaved incorrectly under investigation").

- **PB16 (Training Your Team)** closes the **training-discipline precondition**. Prior playbooks specify what the response team does and says, but the framework's time budgets (TTSM ≤ 10 minutes, TTE ≤ 60 minutes, first-update inside 30 minutes) require trained execution under operational pressure. Introduces the **30-Minute Micro-Drill** (Trigger and Contain → Pull Evidence → Scope and Brief, each 10 minutes), the **Four Core Moves** (activate safe mode, preserve and export evidence, scope impact in business terms, communicate with disciplined language), the **two permanent operating roles** (Safe Mode Owner and Evidence Owner), the **Curriculum-of-Six** (safe modes, tool tiering, retrieval traces, tool-call logs, memory state, configuration snapshots), the **monthly drill cadence**, and the **measurable training targets** that feed Six Metrics and the PB24 board scorecard. PB16 and PB14 together form the **testing and training pair**: PB14 is system-side testing (does the substrate support the discipline?); PB16 is human-side training (can the responders execute it?).

- **PB02 (Evidence Lives in New Places)** closes the **conceptual-foundation gap**. Prior playbooks specify operational responses, but the response team's evidence-preservation reflexes depend on internalizing the three foundational realities of AI evidence. Names these as the **Three Realities of AI Evidence** (the actor is a workflow, not a workstation; the payload can be language, not malware; evidence is fragile) and establishes them as the pedagogical foundation of the framework's evidence discipline. PB02 was originally absorbed into the framework core via [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md); v0.23.0 promoted PB02 to a separate foundational-concepts playbook to honor the "every newsletter issue maps to one playbook" provenance principle and to make the Three Realities explicit as named principles. PB02 and PB01 together form the framework's **two foundational playbooks**: PB02 is the conceptual foundation; PB01 is the operational keystone.

- **PB05 (Executive Decision-Making)** closes the **executive decision-making discipline** that operationalizes accountable decisions under uncertainty during AI incidents. Introduces the **Executive Decision Packet (AI Edition)** (a five-section structured update: Situation, Agent Capability Profile, Provenance Summary, Impact with CIA+T framing, Actions Taken and Next Steps with 4/24/72-hour planning horizons), the **CIA+T framing** that elevates Trust to peer status alongside Confidentiality, Integrity, and Availability, the **4-hour cadence** for subsequent Decision Packets, the **Approval Receipt discipline** that prevents human approval workflows from degrading into rubber-stamping (every high-impact action's approver sees the change preview, destination and domain, source citations, and object count or cap before approving), and the **Three Executive Routine Additions** (capability assessment, provenance tracking, approval-chain awareness). PB05, PB17, and PB24 together form the framework's **executive-layer trio**: PB05 is the decision-during-incident; PB17 is the communication-of-the-decision; PB24 is the periodic governance review of the customer's overall posture.

#### Framework concepts at a glance

The 24-playbook arc introduces named framework concepts that are invented terminology, not borrowed from prior standards. For a reader who wants to know what the framework adds beyond NIST and OWASP, this table is the receipt:

| Framework concept | Originating playbook(s) |
|---|---|
| **Three Realities of AI Evidence** (actor-as-workflow, language-as-payload, evidence-fragile) | PB02 |
| **Two foundational playbooks** (conceptual + operational keystone) | PB02 + PB01 |
| **Capture / retain / prove triad** | PB23 + PB15 + Minimum Evidence Set |
| **Input → context → output coverage triad** | PB06 + PB03 + PB09 |
| **Testing and training pair** | PB14 + PB16 |
| **Pre-production-testing and continuous-monitoring pair** | PB14 + PB22 |
| **Executive-layer trio** | PB05 + PB17 + PB24 |
| **CIA+T framing** (Trust as a peer dimension with Confidentiality, Integrity, Availability) | PB05 |
| **Executive Decision Packet (AI Edition)** | PB05 |
| **Approval Receipt discipline** | PB05 |
| **Three Executive Routine Additions** | PB05 |
| **30-minute first-update SLA** | PB17 |
| **Three-Status Taxonomy** (Confirmed / Suspected / Validating) | PB17 |
| **Four-Element Update Standard** | PB17 |
| **Stakeholder Communication Matrix** (eight stakeholder classes) | PB17 |
| **Template Library** (version-controlled pre-approved templates) | PB17 |
| **Responsible Reframing discipline** | PB17 |
| **30-Minute Micro-Drill** | PB16 |
| **Four Core Moves** | PB16 |
| **Two permanent operating roles** (Safe Mode Owner, Evidence Owner) | PB16 |
| **Curriculum-of-Six** | PB16 |
| **Monthly drill cadence with measurable training targets** | PB16 |
| **Two-Tier Retention Standard** | PB15 |
| **Incident-triggered legal-hold mechanism** | PB15 |
| **Chain-of-custody discipline** (tamper-evident integrity) | PB15 |
| **Reconstructability Test** (quarterly at 30, 60, 90 days) | PB15 |
| **Multi-Stakeholder Governance Matrix** (Security / Privacy / Legal / Engineering) | PB23 |
| **Three-Layer Logging Model** | PB23 |
| **Forensically Useful standard** (six questions logs must answer through metadata alone) | PB23 |
| **Redaction-and-tokenization discipline** | PB23 |
| **M3-Drift kill-switch variant** | PB22 |
| **Post-Change Configuration Snapshot** | PB22 |
| **Drift Canary pack** | PB22 |
| **Layered rollback** | PB22 |
| **60-minute Proof of Readiness Test** | PB19 |
| **Eight critical procurement questions** | PB19 |
| **Build vs Buy Decision Matrix** | PB19 |
| **60-minute Discovery Snapshot** | PB21 |
| **24-hour Shadow Agent Intake Standard** | PB21 |
| **Migrate / redesign / retire decision path** | PB21 |
| **90-minute Freeze-the-World sequence** | PB03 |
| **M3-Output containment variant** | PB09 |
| **Six Metrics** (Inventory Currency, Containment TTSM, Evidence TTE, Drill Currency, Hardening SLA Compliance, Re-Enable Success Rate) | PB13 |
| **Six M3 kill-switch variants** (RAG, Workflow, Output, Vendor, Delegation Cap, Drift) | PB03 / PB06 / PB09 / PB10 / PB08 / PB22 |
| **MVO controls** (Inventory, Safe Modes M0 through M5, Evidence A through F, Controlled Re-Enable) | framework/01 |

**The content gate is now complete.** All 24 playbooks (PB01 through PB24) are shipped. The v1.0 cut now turns entirely on the Steering Committee announcement (the governance gate) rather than the content gate.

## Foundational source

| Source artifact | Repository home |
|---|---|
| **AI IR Overlay synthesis (thesis)** | [README.md](README.md), [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md), [`framework/02-mental-model.md`](framework/02-mental-model.md), [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md) |

## Issue-by-issue mapping

Legend: ✅ shipped · 🟡 drafted (in maintainer's working folder) · ⬜ planned · 📚 absorbed into framework core

| Issue | LinkedIn title | Repo destination | Status (release) |
|---|---|---|---|
| 1 | The Agent Is a Privileged Identity | [`playbooks/01-agent-as-privileged-identity.md`](playbooks/01-agent-as-privileged-identity.md) | ✅ `v0.2.0` |
| 2 | Evidence Lives in New Places | [`playbooks/02-evidence-lives-in-new-places.md`](playbooks/02-evidence-lives-in-new-places.md) and [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) | ✅ playbook (`v0.23.0`, foundational-concepts) · ✅ framework-core operational specification (`v0.1.0`) |
| 3 | RAG and Knowledge-Base Forensics | [`playbooks/03-rag-knowledge-base-forensics.md`](playbooks/03-rag-knowledge-base-forensics.md) | ✅ `v0.6.0` |
| 4 | Tool Design Is Containment | [`playbooks/04-tool-design-is-containment.md`](playbooks/04-tool-design-is-containment.md) | ✅ `v0.3.0` |
| 5 | Executive Decision-Making with AI in the Loop | [`playbooks/05-executive-decision-making.md`](playbooks/05-executive-decision-making.md) | ✅ `v0.24.0` |
| 6 | Rethinking Prompt Injection: A Workflow Threat | [`playbooks/06-prompt-injection-workflow.md`](playbooks/06-prompt-injection-workflow.md) | ✅ `v0.12.0` |
| 7 | Secrets and Tokens in an Agent World | [`playbooks/07-secrets-and-tokens.md`](playbooks/07-secrets-and-tokens.md) | ✅ `v0.8.0` |
| 8 | Multi-Agent Systems Multiply Blast Radius | [`playbooks/08-multi-agent-blast-radius.md`](playbooks/08-multi-agent-blast-radius.md) | ✅ `v0.10.0` |
| 9 | Leakage Without a Breach: AI Output Incidents | [`playbooks/09-output-leakage.md`](playbooks/09-output-leakage.md) | ✅ `v0.15.0` |
| 10 | Vendor Copilots and Mutual Responsibility | [`playbooks/10-vendor-copilots.md`](playbooks/10-vendor-copilots.md) | ✅ `v0.13.0` |
| 11 | Monitoring That Truly Detects Agent Incidents | [`playbooks/11-monitoring-detection.md`](playbooks/11-monitoring-detection.md) | ✅ `v0.9.0` |
| 12 | Insider Threat 3.0: AI-Driven Misuse | [`playbooks/12-insider-threat-3.md`](playbooks/12-insider-threat-3.md) | ✅ `v0.11.0` |
| 13 | The Six Metrics | [`playbooks/13-six-metrics.md`](playbooks/13-six-metrics.md) | ✅ `v0.6.0` |
| 14 | Testing for Agent Failure Modes | [`playbooks/14-testing-for-agent-failure-modes.md`](playbooks/14-testing-for-agent-failure-modes.md) | ✅ `v0.6.0` |
| 15 | Records, Retention, and Proving What Happened | [`playbooks/15-records-retention.md`](playbooks/15-records-retention.md) | ✅ `v0.19.0` |
| 16 | Training Your Team for AI Incidents | [`playbooks/16-training-your-team.md`](playbooks/16-training-your-team.md) | ✅ `v0.22.0` |
| 17 | Communication Techniques for AI-Involved IR | [`playbooks/17-communication-techniques.md`](playbooks/17-communication-techniques.md) | ✅ `v0.21.0` |
| 18 | Post-Incident Hardening | [`playbooks/18-post-incident-hardening.md`](playbooks/18-post-incident-hardening.md) | ✅ `v0.4.0` |
| 19 | Build vs Buy for Agent Controls | [`playbooks/19-build-vs-buy.md`](playbooks/19-build-vs-buy.md) | ✅ `v0.17.0` |
| 20 | AI IR Maturity Roadmap | [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md) (framework view) and [`playbooks/20-maturity-roadmap.md`](playbooks/20-maturity-roadmap.md) (operating view) | ✅ framework view (`v0.1.0`) · ✅ operating view (`v0.7.0`) |
| 21 | The Evolution from Shadow IT to Shadow AI | [`playbooks/21-shadow-ai.md`](playbooks/21-shadow-ai.md) | ✅ `v0.16.0` |
| 22 | Model and Policy Drift | [`playbooks/22-model-policy-drift.md`](playbooks/22-model-policy-drift.md) | ✅ `v0.18.0` |
| 23 | AI Logging and Privacy in a Multi-Stakeholder World | [`playbooks/23-logging-privacy.md`](playbooks/23-logging-privacy.md) and [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) | ✅ playbook (`v0.20.0`) · ✅ crosswalk (`v0.1.5`) |
| 24 | Board-Ready Scorecard | [`playbooks/24-board-ready-scorecard.md`](playbooks/24-board-ready-scorecard.md) and `templates/board-scorecard.md` (printable) | ✅ playbook (`v0.5.0`) · ⬜ printable template planned |

## Crosswalks (cross-cutting, not 1:1 with issues)

| Standard | Repo home | Status |
|---|---|---|
| NIST AI RMF 1.0 | [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) | ✅ `v0.1.0` |
| NIST CSF 2.0 + SP 800-61 r3 | [`crosswalks/nist-csf-2.md`](crosswalks/nist-csf-2.md) | ✅ `v0.1.5` |
| OWASP Top 10 for Agentic Applications 2026 | [`crosswalks/owasp-agentic-top-10.md`](crosswalks/owasp-agentic-top-10.md) | ✅ `v0.1.5` |
| ISO/IEC 27035 (Information security incident management) | *forthcoming* | ⬜ planned (referenced from `framework/01-minimum-viable-overlay.md` as a base IR discipline the MVO extends for AI agents) |
| ISO/IEC 42001:2023 | *forthcoming* | ⬜ planned |
| EU AI Act (Regulation 2024/1689) | *forthcoming* | ⬜ planned |
| CIS Controls, SOC 2, HIPAA | *forthcoming* (community contributions welcome via Issues) | ⬜ planned |

## Templates

| Template | Repo home | Status |
|---|---|---|
| AI Bill of Materials (AI-BOM) | [`templates/ai-bom.yaml`](templates/ai-bom.yaml), [`templates/README-ai-bom.md`](templates/README-ai-bom.md) | ✅ `v0.1.0` |
| Agent Privilege Matrix | [`templates/agent-privilege-matrix.csv`](templates/agent-privilege-matrix.csv), [`templates/README-privilege-matrix.md`](templates/README-privilege-matrix.md) | ✅ `v0.1.0` |
| Board Scorecard (printable) | `templates/board-scorecard.md` | ⬜ planned (ships with the PB24 operating revision) |

## Schemas

| Schema | Repo home | Status |
|---|---|---|
| AI-BOM JSON Schema | [`schemas/ai-bom.schema.json`](schemas/ai-bom.schema.json) | ✅ `v0.14.0` |
| Agent Privilege Matrix JSON Schema | [`schemas/privilege-matrix.schema.json`](schemas/privilege-matrix.schema.json) | ✅ `v0.14.0` |
| Credential Event Log JSON Schema | [`schemas/credential-event.schema.json`](schemas/credential-event.schema.json) | ✅ `v0.14.0` |
| Kill-Switch API Contract | [`schemas/kill-switch-api.md`](schemas/kill-switch-api.md) | ✅ `v0.14.0` |
| Evidence Export Script Contract | [`schemas/evidence-export.spec.md`](schemas/evidence-export.spec.md) | ✅ `v0.14.0` |

## Reference implementations

| Artifact | Repo home | Status |
|---|---|---|
| AI-BOM + Privilege Matrix validator (Python 3) | [`scripts/validate.py`](scripts/validate.py) | ✅ `v0.14.1`; v0.26.0 adds maturity-target-conditional schema validation, last_reviewed and kill_switches.tested_at staleness checks, and `--strict` flag |
| CI workflow (GitHub Actions) running the validator on every PR touching `templates/`, `schemas/`, or `scripts/validate.py`. Supports manual dispatch via the Actions tab. | [`.github/workflows/validate-templates.yml`](.github/workflows/validate-templates.yml) | ✅ `v0.14.2` |
| Evidence Exporter (Python CLI implementing the Evidence Export Script Contract for Types A through F; six stub adapters; manifest with SHA-256 integrity; parallel-export; telemetry events) | [`reference-impls/evidence_exporter/`](reference-impls/evidence_exporter/) | ✅ `v0.26.0` |
| Kill-Switch Demo (Python in-memory tool registry showing M0/M1/M2/M3/M4 with the Activate/Status/Deactivate/Probe API shape, separation-of-duties, scope parameter) | [`reference-impls/kill_switch_demo/`](reference-impls/kill_switch_demo/) | ✅ `v0.26.0` |

## Operational entry points

| Artifact | Purpose | Status |
|---|---|---|
| [`QUICKSTART.md`](QUICKSTART.md) | 30-day adoption path for one production AI agent. Day 1 AI-BOM, Day 7 Privilege Matrix, Day 14 tabletop M1-M4, Day 21 evidence drill, Day 30 Level 2/3 maturity claim. | ✅ `v0.14.2` |
| [`QUICKSTART-startup.md`](QUICKSTART-startup.md) | The startup-minimum adoption path. 3 playbooks + 2 templates + 1 triage card. 4-week path to Maturity Level 2. Targets security teams of 5 or fewer with limited platform control. | ✅ `v0.26.0` |
| [`examples/incident-walkthrough.md`](examples/incident-walkthrough.md) | Synthetic worked example of an end-to-end incident response, demonstrating the framework as a coherent system rather than a list of controls. | ✅ `v0.14.2` |
| [`MATRIX.md`](MATRIX.md) | Self-contained tabular reference for the framework. Nine sections: response-phase matrix (Preparation, Detection, Triage, Containment, Evidence, Recovery, Closure), kill-switch ladder with all M3 variants, Minimum Evidence Set, Six Metrics, MVO controls, maturity levels, 24-playbook quick reference, standards crosswalk summary, quick-read legend. Calibrated for board briefings, onboarding, auditor walkthroughs, and one-page references. | ✅ `v0.33.0` |
| [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) | Pre-flight and post-push checklist for the maintainer. Closes the release-hygiene gaps surfaced in v0.14.1. | ✅ `v0.14.2` |

## Drafted but unshipped: conversion notes

Each playbook marked 🟡 drafted has source content in the maintainer's working folder (`AI IR Overlay-Linkedin-Post_completed/`) and in the package drafts under `aiiroverlay-packages/`. Promoting a drafted playbook to a shipped release means expanding the draft from its newsletter footprint (about 7 KB) to a full operational playbook (around 15 to 20 KB). The expansion follows the established skeleton:

1. **Premise**: what's AI-specific, in one or two paragraphs.
2. **First-Hour Actions**: a table with minute markers and owners.
3. **Containment Options**: mapped to Kill-Switch Modes M0 through M5.
4. **Evidence Priorities**: which of the A–F evidence types are load-bearing for this scenario.
5. **Recovery Sequence**: staged re-enablement, aligned with MVO-4.
6. **Post-Incident Hardening**: what enters [Playbook 18](playbooks/18-post-incident-hardening.md)'s five-business-day SLA.
7. **Common Pitfalls**: the failure modes specific to this scenario class.
8. **Related**: relative-path links to every framework artifact and adjacent playbook.
9. **The Question to Carry Forward**: a single-question close.

The current live playbooks are the structural reference for tone, depth, and cross-linking. See [PB01](playbooks/01-agent-as-privileged-identity.md), [PB03](playbooks/03-rag-knowledge-base-forensics.md), [PB04](playbooks/04-tool-design-is-containment.md), [PB13](playbooks/13-six-metrics.md), [PB14](playbooks/14-testing-for-agent-failure-modes.md), [PB18](playbooks/18-post-incident-hardening.md), and [PB24](playbooks/24-board-ready-scorecard.md).

## Citation rule

Every playbook must include this footer:

```text
*Source: AI IR Overlay newsletter, Issue #N, "Title," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
```

This supports academic citability and the trademark and attribution model documented in [LICENSE](LICENSE).

## Why this file exists

A reader who lands on the framework asking "are all 24 playbooks shipped?" deserves an honest answer: **yes, as of v0.24.0 (content gate complete; current release is v0.33.0)**. Every issue has a destination, every shipped artifact has a release tag, and the framework's content gate is complete. The v1.0 cut now turns entirely on the Steering Committee announcement (see [GOVERNANCE.md](GOVERNANCE.md)). The framework's promise was incremental shipping; this map is the receipt.

---

<!-- Last revised: 2026-06-29 (v0.33.0 added MATRIX.md row to Operational entry points; v0.32.0 P2 polish + Why-24-shipped section restructured: sub-bullets per axis for NIST CSF 2.0 closures and OWASP Agentic closures, six-stage operational arc and evidence-taxonomy coverage broken out, bullet 3 split into per-playbook sub-bullets with framework concepts bolded up-front, and a new Framework Concepts at a Glance table added) -->
