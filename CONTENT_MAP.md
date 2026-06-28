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

The remaining playbooks ship as future MINOR releases. `v1.0.0` is cut once the remaining playbooks ship (PB02 is absorbed into the framework core, so the target is 23 playbooks) and a Steering Committee is announced. See [GOVERNANCE.md](GOVERNANCE.md).

## Foundational source

| Source artifact | Repository home |
|---|---|
| **AI IR Overlay synthesis (thesis)** | [README.md](README.md), [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md), [`framework/02-mental-model.md`](framework/02-mental-model.md), [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md) |

## Issue-by-issue mapping

Legend: ✅ shipped · 🟡 drafted (in maintainer's working folder) · ⬜ planned · 📚 absorbed into framework core

| Issue | LinkedIn title | Repo destination | Status (release) |
|---|---|---|---|
| 1 | The Agent Is a Privileged Identity | [`playbooks/01-agent-as-privileged-identity.md`](playbooks/01-agent-as-privileged-identity.md) | ✅ `v0.2.0` |
| 2 | Evidence Lives in New Places | [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) | 📚 absorbed into framework core (`v0.1.0`). No separate playbook planned. |
| 3 | RAG and Knowledge-Base Forensics | [`playbooks/03-rag-knowledge-base-forensics.md`](playbooks/03-rag-knowledge-base-forensics.md) | ✅ `v0.6.0` |
| 4 | Tool Design Is Containment | [`playbooks/04-tool-design-is-containment.md`](playbooks/04-tool-design-is-containment.md) | ✅ `v0.3.0` |
| 5 | Executive Decision-Making with AI in the Loop | `playbooks/05-executive-decision-making.md` | 🟡 drafted, not yet released |
| 6 | Rethinking Prompt Injection: A Workflow Threat | [`playbooks/06-prompt-injection-workflow.md`](playbooks/06-prompt-injection-workflow.md) | ✅ `v0.12.0` |
| 7 | Secrets and Tokens in an Agent World | [`playbooks/07-secrets-and-tokens.md`](playbooks/07-secrets-and-tokens.md) | ✅ `v0.8.0` |
| 8 | Multi-Agent Systems Multiply Blast Radius | [`playbooks/08-multi-agent-blast-radius.md`](playbooks/08-multi-agent-blast-radius.md) | ✅ `v0.10.0` |
| 9 | Leakage Without a Breach: AI Output Incidents | `playbooks/09-output-leakage.md` | 🟡 drafted, not yet released |
| 10 | Vendor Copilots and Mutual Responsibility | `playbooks/10-vendor-copilots.md` | 🟡 drafted, not yet released |
| 11 | Monitoring That Truly Detects Agent Incidents | [`playbooks/11-monitoring-detection.md`](playbooks/11-monitoring-detection.md) | ✅ `v0.9.0` |
| 12 | Insider Threat 3.0: AI-Driven Misuse | [`playbooks/12-insider-threat-3.md`](playbooks/12-insider-threat-3.md) | ✅ `v0.11.0` |
| 13 | The Six Metrics | [`playbooks/13-six-metrics.md`](playbooks/13-six-metrics.md) | ✅ `v0.6.0` |
| 14 | Testing for Agent Failure Modes | [`playbooks/14-testing-for-agent-failure-modes.md`](playbooks/14-testing-for-agent-failure-modes.md) | ✅ `v0.6.0` |
| 15 | Records, Retention, and Proving What Happened | `playbooks/15-records-retention.md` | 🟡 drafted, not yet released |
| 16 | Training Your Team for AI Incidents | `playbooks/16-training-your-team.md` | 🟡 drafted, not yet released |
| 17 | Communication Techniques for AI-Involved IR | `playbooks/17-communication-techniques.md` | 🟡 drafted, not yet released |
| 18 | Post-Incident Hardening | [`playbooks/18-post-incident-hardening.md`](playbooks/18-post-incident-hardening.md) | ✅ `v0.4.0` |
| 19 | Build vs Buy for Agent Controls | `playbooks/19-build-vs-buy.md` | 🟡 drafted, not yet released |
| 20 | AI IR Maturity Roadmap | [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md) (framework view) and [`playbooks/20-maturity-roadmap.md`](playbooks/20-maturity-roadmap.md) (operating view) | ✅ framework view (`v0.1.0`) · ✅ operating view (`v0.7.0`) |
| 21 | The Evolution from Shadow IT to Shadow AI | `playbooks/21-shadow-ai.md` | 🟡 drafted, not yet released |
| 22 | Model and Policy Drift | `playbooks/22-model-policy-drift.md` | 🟡 drafted, not yet released |
| 23 | AI Logging and Privacy in a Multi-Stakeholder World | `playbooks/23-logging-privacy.md` and [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) | ✅ crosswalk (`v0.1.5`) · 🟡 playbook drafted |
| 24 | Board-Ready Scorecard | [`playbooks/24-board-ready-scorecard.md`](playbooks/24-board-ready-scorecard.md) and `templates/board-scorecard.md` (printable) | ✅ playbook (`v0.5.0`) · ⬜ printable template planned |

## Crosswalks (cross-cutting, not 1:1 with issues)

| Standard | Repo home | Status |
|---|---|---|
| NIST AI RMF 1.0 | [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) | ✅ `v0.1.0` |
| NIST CSF 2.0 + SP 800-61 r3 | [`crosswalks/nist-csf-2.md`](crosswalks/nist-csf-2.md) | ✅ `v0.1.5` |
| OWASP Top 10 for Agentic Applications 2026 | [`crosswalks/owasp-agentic-top-10.md`](crosswalks/owasp-agentic-top-10.md) | ✅ `v0.1.5` |
| ISO/IEC 42001:2023 | *forthcoming* | ⬜ planned |
| EU AI Act (Regulation 2024/1689) | *forthcoming* | ⬜ planned |
| CIS Controls, SOC 2, HIPAA | *forthcoming* (community contributions welcome via Issues) | ⬜ planned |

## Templates

| Template | Repo home | Status |
|---|---|---|
| AI Bill of Materials (AI-BOM) | [`templates/ai-bom.yaml`](templates/ai-bom.yaml), [`templates/README-ai-bom.md`](templates/README-ai-bom.md) | ✅ `v0.1.0` |
| Agent Privilege Matrix | [`templates/agent-privilege-matrix.csv`](templates/agent-privilege-matrix.csv), [`templates/README-privilege-matrix.md`](templates/README-privilege-matrix.md) | ✅ `v0.1.0` |
| Board Scorecard (printable) | `templates/board-scorecard.md` | ⬜ planned (ships with the PB24 operating revision) |

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

A reader who lands on the framework asking "where are playbooks 02, 05 through 12, 15 through 17, and 19 through 23?" deserves an honest answer. This file is that answer. Every issue has a destination, every shipped artifact has a release tag, and every drafted-but-unreleased artifact is named so it can't pretend to be absent. The framework's promise is incremental shipping. This map is the receipt.

---

<!-- Last revised: 2026-06-23 -->
