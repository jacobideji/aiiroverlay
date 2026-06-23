<!-- ────────────────────────────────────────────────────────────────── -->
<!--  AI IR Overlay · Framework Overview                                -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Why an overlay, not a replacement. The thesis.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*
---

# The AI IR Overlay: Framework Overview

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/jacobideji/aiiroverlay?label=release)](https://github.com/jacobideji/aiiroverlay/releases)
[![Standards: NIST · OWASP · ISO/IEC](https://img.shields.io/badge/standards-NIST%20800--61%20r3%20%C2%B7%20AI%20RMF%20%C2%B7%20OWASP%20%C2%B7%20ISO%2FIEC%2042001-informational)](#related-work)

> Establishing the minimum standard for safe and effective operations of AI agents in production.

## Why an overlay, not a replacement

Traditional incident response (codified in NIST SP 800-61 r3, which superseded r2 in April 2025) was built around unauthorized access vectors: malware, exploits, credential theft, lateral movement. AI agents change the failure mode.

AI incidents often manifest through *authorized* channels:

- **Legitimate identities.** Service accounts or delegated OAuth grants that execute unintended actions.
- **Legitimate APIs.** Tool calls to email, CRM, and ERP that operate within allowed parameters but still produce harm.
- **Legitimate sources.** Retrieval layers pulling from trusted but outdated or inappropriate knowledge.
- **Legitimate workflows.** Automations that execute policy as written, yet produce harmful outcomes.

When the actor is authorized, the question shifts from *"who got in?"* to *"what could it touch, and what did it do?"* Crucial evidence now lives in prompts, tool calls, retrieval traces, and configuration state. Not on endpoints.

## What stays the same

The core mechanics of effective incident response remain unchanged:

- Clear command and control
- Evidence-first discipline
- Rapid containment with minimal disruption
- Scoping using *confirmed* versus *suspected* terminology
- Recovery via controlled, staged re-enablement
- Defensible decision logs

AI doesn't rewrite the rules of effective IR. It changes the map.

## The Overlay model

The AI IR Overlay adds four agent-aware controls (the **Minimum Viable Overlay**, or MVO) on top of your existing IR program.

> **Note:** The NIST 800-61 r2 phases shown below remain widely understood operational shorthand. r3 (April 2025) restructures incident response around CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover). See the AI IR Overlay to CSF 2.0 crosswalk at [`crosswalks/nist-csf-2.md`](crosswalks/nist-csf-2.md).

```text
┌─────────────────────────────────────────────────────────┐
│                NIST 800-61 IR Lifecycle                 │
│  Preparation → Detection → Containment → Eradication →  │
│              Recovery → Post-Incident                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              AI IR Overlay · MVO Controls               │
│                                                         │
│  1. INVENTORY     · Agents · Identities · Tools ·       │
│                     Write Targets                       │
│  2. SAFE MODES    · Kill-Switch Ladder (Modes 0 to 5)   │
│  3. EVIDENCE      · Minimum AI Evidence Set (A–F)       │
│  4. CONTROLLED    · Staged, validated re-enablement     │
│     RE-ENABLE                                           │
└─────────────────────────────────────────────────────────┘
```

## Reading order

Read the framework in this order. Items 1 through 6 are the core. Items 7 through 9 are the working artifacts.

1. **The Minimum Viable Overlay.** The four controls in detail: [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md)
2. **The Mental Model.** Four sentences that govern every decision: [`framework/02-mental-model.md`](framework/02-mental-model.md)
3. **The Maturity Roadmap.** Where your program is, and how to advance it: [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md)
4. **The Six Triage Questions.** First-hour discipline: [`triage/six-questions.md`](triage/six-questions.md). Printable card: [`triage/six-questions-card.md`](triage/six-questions-card.md).
5. **Kill-Switch Modes.** Containment ladder: [`kill-switches/overview.md`](kill-switches/overview.md)
6. **Minimum Evidence Set.** What to preserve, and in what order: [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md)
7. **Templates.** [`templates/ai-bom.yaml`](templates/ai-bom.yaml) (AI Bill of Materials for MVO-1 Inventory) · [`templates/agent-privilege-matrix.csv`](templates/agent-privilege-matrix.csv) (tool-tier matrix for MVO-2 Mode M3)
8. **Crosswalks.** [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) (NIST AI RMF 1.0) · [`crosswalks/nist-csf-2.md`](crosswalks/nist-csf-2.md) (NIST CSF 2.0 and SP 800-61 r3) · [`crosswalks/owasp-agentic-top-10.md`](crosswalks/owasp-agentic-top-10.md) (OWASP Agentic Top 10 2026)
9. **Playbooks.** [`playbooks/01-agent-as-privileged-identity.md`](playbooks/01-agent-as-privileged-identity.md) (privileged-identity response) · [`playbooks/03-rag-knowledge-base-forensics.md`](playbooks/03-rag-knowledge-base-forensics.md) (RAG and KB forensics, with a 90-minute Freeze-the-World sequence) · [`playbooks/04-tool-design-is-containment.md`](playbooks/04-tool-design-is-containment.md) (pre-incident tool design) · [`playbooks/13-six-metrics.md`](playbooks/13-six-metrics.md) (the six metrics behind the Maturity Roadmap) · [`playbooks/14-testing-for-agent-failure-modes.md`](playbooks/14-testing-for-agent-failure-modes.md) (pre-production Kill-Switch testing) · [`playbooks/18-post-incident-hardening.md`](playbooks/18-post-incident-hardening.md) (post-incident hardening with a 5-business-day SLA) · [`playbooks/24-board-ready-scorecard.md`](playbooks/24-board-ready-scorecard.md) (executive-layer scorecard across 4 domains). More playbooks ship as MINOR releases. See [CONTENT_MAP.md](CONTENT_MAP.md) and [CHANGELOG.md](CHANGELOG.md).

## Provenance

The AI IR Overlay was developed and field-tested through the *AI IR Overlay* LinkedIn newsletter series (Issues 1 through 24, 2025 to 2026), authored by Jacob Ideji. Each newsletter issue maps to one playbook in the full framework. See [CONTENT_MAP.md](CONTENT_MAP.md) for the issue-to-file index.

## Related work

- NIST SP 800-61 r3: *Incident Response Recommendations and Considerations for Cybersecurity Risk Management*, a CSF 2.0 Community Profile (April 2025, supersedes r2)
- NIST AI Risk Management Framework (AI RMF 1.0)
- OWASP Top 10 for LLM Applications (2025.1)
- OWASP Top 10 for Agentic Applications 2026 (ASI01 through ASI10, OWASP GenAI Security Project)
- ISO/IEC 42001:2023: *Information technology, Artificial intelligence, Management system* (AIMS)
- EU AI Act (Regulation 2024/1689), Article 26 obligations for deployers
- MITRE ATLAS: Adversarial Threat Landscape for Artificial-Intelligence Systems

## Acronyms

- **AI-BOM**: AI Bill of Materials
- **ASI**: Agentic Security Initiative (OWASP)
- **CSF**: (NIST) Cybersecurity Framework
- **IC**: Incident Commander
- **IR**: Incident Response
- **MVO**: Minimum Viable Overlay
- **PAM**: Privileged Access Management
- **RAG**: Retrieval-Augmented Generation
- **RMF**: (NIST AI) Risk Management Framework
- **SOC**: Security Operations Center *(distinct from SOC 2, the AICPA audit standard)*
- **TTA**: Time-to-Activate
- **TTE**: Time-to-Evidence
- **TTSM**: Time-to-Safe-Mode
