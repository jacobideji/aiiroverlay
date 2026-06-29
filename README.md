<!-- ────────────────────────────────────────────────────────────────── -->
<!--  AI IR Overlay · Framework Overview                                -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Why an overlay, not a replacement. The thesis.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](CONTENT_MAP.md) for the full repository map.*
---

# The AI IR Overlay: Framework Overview

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/jacobideji/aiiroverlay?label=release)](https://github.com/jacobideji/aiiroverlay/releases)
[![References: NIST · OWASP](https://img.shields.io/badge/references-NIST%20800--61%20r3%20%C2%B7%20AI%20RMF%20%C2%B7%20OWASP-informational)](#related-work)

> A practical incident-response baseline for AI agents in production. Adapt and critique freely.

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

## Scope

The AI IR Overlay operationalizes **deployer obligations** for AI systems in production. A deployer is the organization that uses an AI system in its own operations, under its own oversight (per EU AI Act Article 3). This framework is for the security team responding to incidents in agents the deployer's organization runs.

**Out of scope:**

- **Provider obligations** for placing AI systems on the market (EU AI Act Articles 16-21)
- **General-purpose AI model (GPAI) provider obligations** (EU AI Act Article 51 and following)
- **Prohibited AI practices** (EU AI Act Article 5)
- **Conformity assessment and CE marking** (EU AI Act Article 43)

Vendor copilots that an organization deploys are in scope for the deployer (the customer side). The vendor's provider obligations are not addressed here.

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

**New here? Start with [QUICKSTART.md](QUICKSTART.md)** for a 30-day adoption path, or [`examples/incident-walkthrough.md`](examples/incident-walkthrough.md) for an end-to-end worked example of an incident response using the framework.

For the full conceptual reading order, items 1 through 6 are the core, items 7 through 11 are the working artifacts.

1. **The Minimum Viable Overlay.** The four controls in detail: [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md)
2. **The Mental Model.** Four sentences that govern every decision: [`framework/02-mental-model.md`](framework/02-mental-model.md)
3. **The Maturity Roadmap.** Where your program is, and how to advance it: [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md)
4. **The Six Triage Questions.** First-hour discipline: [`triage/six-questions.md`](triage/six-questions.md). Printable card: [`triage/six-questions-card.md`](triage/six-questions-card.md).
5. **Kill-Switch Modes.** Containment ladder: [`kill-switches/overview.md`](kill-switches/overview.md)
6. **Minimum Evidence Set.** What to preserve, and in what order: [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md)
7. **Templates.** [`templates/ai-bom.yaml`](templates/ai-bom.yaml) (AI Bill of Materials for MVO-1 Inventory) · [`templates/agent-privilege-matrix.csv`](templates/agent-privilege-matrix.csv) (tool-tier matrix for MVO-2 Mode M3)
8. **Crosswalks.** [`crosswalks/nist-ai-rmf.md`](crosswalks/nist-ai-rmf.md) (NIST AI RMF 1.0) · [`crosswalks/nist-csf-2.md`](crosswalks/nist-csf-2.md) (NIST CSF 2.0 and SP 800-61 r3) · [`crosswalks/owasp-agentic-top-10.md`](crosswalks/owasp-agentic-top-10.md) (OWASP Agentic Top 10 2026)
9. **Playbooks.** Nineteen shipped playbooks, organized by the arc described in [CONTENT_MAP.md](CONTENT_MAP.md):

   - **Foundation:** [`playbooks/01-agent-as-privileged-identity.md`](playbooks/01-agent-as-privileged-identity.md) (the keystone playbook; every later playbook builds on the privileged-identity lens).
   - **Prevention:** [`playbooks/04-tool-design-is-containment.md`](playbooks/04-tool-design-is-containment.md) (pre-incident tool tiering T0/T1/T2 that makes Kill-Switch Mode M3 surgical), [`playbooks/19-build-vs-buy.md`](playbooks/19-build-vs-buy.md) (procurement-time discipline: the 60-minute Proof of Readiness Test, the eight critical procurement questions, the Build vs Buy Decision Matrix, and the post-procurement hardening that converts platform-capability gaps into contractual commitments or customer-side build commitments).
   - **Closure:** [`playbooks/18-post-incident-hardening.md`](playbooks/18-post-incident-hardening.md) (the 5-business-day hardening SLA that turns lessons into permanent guardrails).
   - **Governance:** [`playbooks/24-board-ready-scorecard.md`](playbooks/24-board-ready-scorecard.md) (executive-layer scorecard across four domains: Containment, Evidence, Governance, Recovery).
   - **Measurement and Depth:** [`playbooks/13-six-metrics.md`](playbooks/13-six-metrics.md) (the six metrics), [`playbooks/14-testing-for-agent-failure-modes.md`](playbooks/14-testing-for-agent-failure-modes.md) (pre-production Kill-Switch testing), [`playbooks/03-rag-knowledge-base-forensics.md`](playbooks/03-rag-knowledge-base-forensics.md) (90-minute Freeze-the-World sequence for retrieval incidents), [`playbooks/22-model-policy-drift.md`](playbooks/22-model-policy-drift.md) (change-event forensics for model upgrades, prompt edits, policy tunes, retriever changes, and index rebuilds; introduces the M3-Drift containment variant, the Post-Change Configuration Snapshot, the change-pipeline event ledger, the Drift Canary pack, and the layered rollback sequence; forms the pre-production-testing / continuous-monitoring pair with PB14), [`playbooks/15-records-retention.md`](playbooks/15-records-retention.md) (the proof-discipline playbook: the lifecycle deep-dive on the A-F evidence taxonomy across capture, retention, chain-of-custody, tamper-evidence, and disposal; introduces the Two-Tier Retention Standard, the incident-triggered legal-hold mechanism, and the quarterly Reconstructability Test that empirically validates the framework's evidence claims at 30, 60, and 90 days).
   - **Operations:** [`playbooks/20-maturity-roadmap.md`](playbooks/20-maturity-roadmap.md) (operating view of the Maturity Roadmap), [`playbooks/07-secrets-and-tokens.md`](playbooks/07-secrets-and-tokens.md) (credential discipline), [`playbooks/11-monitoring-detection.md`](playbooks/11-monitoring-detection.md) (three signal families for authorized misuse), [`playbooks/06-prompt-injection-workflow.md`](playbooks/06-prompt-injection-workflow.md) (workflow injection: harmful instructions hidden in tickets, emails, web pages, and documents the agent reads; architectural defense over prompt engineering), [`playbooks/09-output-leakage.md`](playbooks/09-output-leakage.md) (leakage without a breach: data exposure through routine AI outputs; M3-Output containment variant; output-layer DLP and channel classification as architectural defense; completes the input → context → output coverage triad with PB06 and PB03), [`playbooks/08-multi-agent-blast-radius.md`](playbooks/08-multi-agent-blast-radius.md) (multi-agent topologies, orchestrator-first containment), [`playbooks/10-vendor-copilots.md`](playbooks/10-vendor-copilots.md) (vendor copilots: customer-controlled identity boundary, contracted evidence and containment SLAs, quarterly Vendor Evidence Drill; M3-Vendor containment variant), [`playbooks/12-insider-threat-3.md`](playbooks/12-insider-threat-3.md) (Insider Threat 3.0, capability-intent-impact triad, HR/Legal joint engagement), [`playbooks/21-shadow-ai.md`](playbooks/21-shadow-ai.md) (Shadow AI discovery: the 60-minute Discovery Snapshot, the 24-hour Shadow Agent Intake Standard, identity-level containment for non-modifiable runtimes, migrate/redesign/retire decision path, and the four-boundary hardening including the governed integration path that prevents the next shadow agent from staying shadow).

   More playbooks ship as MINOR releases. See [CHANGELOG.md](CHANGELOG.md) for the full release schedule.

10. **Schemas.** Machine-readable contracts for CI validation: [`schemas/ai-bom.schema.json`](schemas/ai-bom.schema.json) (AI-BOM validator) · [`schemas/privilege-matrix.schema.json`](schemas/privilege-matrix.schema.json) (Privilege Matrix row validator) · [`schemas/credential-event.schema.json`](schemas/credential-event.schema.json) (PB07 credential-event log validator) · [`schemas/kill-switch-api.md`](schemas/kill-switch-api.md) (Mode M0 through M5 activation API contract) · [`schemas/evidence-export.spec.md`](schemas/evidence-export.spec.md) (Type A through F evidence export script contract).

11. **Reference validator.** [`scripts/validate.py`](scripts/validate.py) (Python 3, runs every AI-BOM YAML and Privilege Matrix CSV against the JSON Schemas). A GitHub Action at [`.github/workflows/validate-templates.yml`](.github/workflows/validate-templates.yml) runs the validator on every pull request touching `templates/`, `schemas/`, or the script itself.

## Provenance

The AI IR Overlay was developed through the *AI IR Overlay* LinkedIn newsletter series (Issues 1 through 24, 2025 to 2026), authored by Jacob Ideji, as a synthesis of NIST AI RMF 1.0, NIST CSF 2.0, NIST SP 800-61 r3, OWASP Top 10 for Agentic Applications 2026, EU AI Act deployer obligations, and the maintainer's incident response and AI security experience. The framework has not yet been deployed in a documented production AI incident; adopters who use it in a real incident are encouraged to submit anonymized case studies via [Discussions](https://github.com/jacobideji/aiiroverlay/discussions). Each newsletter issue maps to one playbook in the full framework. See [CONTENT_MAP.md](CONTENT_MAP.md) for the issue-to-file index.

## Related work

- NIST SP 800-61 r3: *Incident Response Recommendations and Considerations for Cybersecurity Risk Management*, a CSF 2.0 Community Profile (April 2025, supersedes r2)
- NIST AI Risk Management Framework (AI RMF 1.0)
- OWASP Top 10 for LLM Applications (2025.1)
- OWASP Top 10 for Agentic Applications 2026 (ASI01 through ASI10, OWASP GenAI Security Project)
- ISO/IEC 42001:2023: *Information technology, Artificial intelligence, Management system* (AIMS)
- EU AI Act (Regulation 2024/1689), Article 26 obligations for deployers
- MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems): adjacent prior art on AI threat modeling. Not currently mapped in the crosswalks; an ATLAS crosswalk is welcome as a community contribution

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
