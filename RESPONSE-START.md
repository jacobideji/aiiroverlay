<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Response Start: AI IR Overlay paged-responder entry point         -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

# Response Start

> **If you are responding to an AI agent incident RIGHT NOW, this is your starting point. Four files, in order, take you from 3am page to a defensible 60-minute checkpoint.**

## The 60-minute navigation path

| Minute | Open | Why |
|---|---|---|
| **0–2** | The AI-BOM YAML for the affected agent (per [`templates/ai-bom.yaml`](templates/ai-bom.yaml) schema; one file per agent in production) | Know what the agent is, what it can do, what it writes to. If you don't have an AI-BOM for this agent, you have an inventory problem, not just an incident |
| **2–15** | [`triage/six-questions.md`](triage/six-questions.md) | Walk the six questions in order. The "Where each answer routes" table at the end points you to the right playbook |
| **10–20** | [`kill-switches/overview.md`](kill-switches/overview.md) | At Question 5, pick the Mode (M1–M4) and variant. Use the **Variant Selector** quick reference for fast matching. Activation SLA: ≤ 10 minutes from IC order |
| **30–60** | [`framework/04-materiality-and-disclosure.md`](framework/04-materiality-and-disclosure.md) | Convene the Materiality and Disclosure call if Mode ≥ M3 OR any condition trigger applies (customer data, external recipients, regulated data, financial actions, customer-facing trust, public attention). CISO + General Counsel + Incident Commander within 1 hour |

## During response, you may also need

- **The scenario-specific playbook** (PB01 through PB24). See [`MATRIX.md`](MATRIX.md) Section 7 for the 24-playbook index, or use the triage-questions routing table to navigate.
- **The Three Realities reflex**: [Playbook 02: Evidence Lives in New Places](playbooks/02-evidence-lives-in-new-places.md). Snapshot before rotate. Snapshot before clean. Snapshot before redeploy.
- **The Executive Decision Packet template**: [Playbook 05: Executive Decision-Making](playbooks/05-executive-decision-making.md). Required when executive convening is triggered.
- **The Stakeholder Communication Matrix**: [Playbook 17: Communication Techniques](playbooks/17-communication-techniques.md). 30-minute first-update SLA.
- **The evidence export script**: [`reference-impls/evidence_exporter/`](reference-impls/evidence_exporter/) (60-minute Minimum Evidence Set capture per [`schemas/evidence-export.spec.md`](schemas/evidence-export.spec.md)).

## After response

- **Hardening**: [Playbook 18: Post-Incident Hardening](playbooks/18-post-incident-hardening.md) (5-business-day SLA, gated on materiality record completeness).
- **Evidence retention**: [Playbook 15: Records, Retention, and Proving What Happened](playbooks/15-records-retention.md) (Two-Tier Retention Standard; chain-of-custody discipline; quarterly Reconstructability Test).
- **Privacy review**: [Playbook 23: AI Logging and Privacy](playbooks/23-logging-privacy.md) (Three-Layer Logging Model; Forensically Useful standard).
- **Board signal**: [Playbook 24: Board-Ready Scorecard](playbooks/24-board-ready-scorecard.md) (Containment, Evidence, Governance, Recovery domains).

## What this file is not

This is not a playbook. This is the entry-point map for paged responders. The disciplined response that survives a board review, a regulator inquiry, or a legal deposition is in the playbooks themselves; this file just gets you to the right playbook fast.

For adoption (not response), see [`QUICKSTART.md`](QUICKSTART.md) (30-day path) or [`QUICKSTART-startup.md`](QUICKSTART-startup.md) (4-week startup-minimum path). For the framework's structural reference, see [`MATRIX.md`](MATRIX.md) and [`CONTENT_MAP.md`](CONTENT_MAP.md).

---

*Source: AI IR Overlay framework, by Jacob Ideji.*

*Last revised: 2026-06-30 (v0.33.0 A1.3 navigation fix).*

<https://www.linkedin.com/in/jacobideji/>
