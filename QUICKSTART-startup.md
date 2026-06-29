<!-- ────────────────────────────────────────────────────────────────── -->
<!--  QUICKSTART for startups and small security teams                  -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The 5-person-team adoption path. Three playbooks, two templates, four weekends. Reach Maturity Level 1 (Aware) in week 1, Level 2 (Containable) in week 4. The full framework is comprehensive; you do not have to adopt all of it on day one.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](CONTENT_MAP.md) for the full repository map and [QUICKSTART.md](QUICKSTART.md) for the standard 30-day adoption path.*

---

# Startup QUICKSTART: Minimum Viable Adoption

## Who this is for

This artifact is for **security teams of 5 or fewer** who need to defensibly respond to AI agent incidents but cannot adopt the full 24-playbook framework in their first month. The standard [QUICKSTART.md](QUICKSTART.md) assumes well-resourced security teams with full platform control; this artifact assumes the opposite.

**You should still read this if any of these apply to your situation:**

- You are the only security person at your organization
- You have 1-3 AI agents in production but no formal incident-response process for them
- You depend on vendor copilots (Copilot for Microsoft 365, Salesforce Einstein, ChatGPT Enterprise) and have limited control-plane access
- Your AI agents touch customer data or external recipients but you cannot afford a 6-month adoption project
- You need to defensibly answer "what are we doing about AI risk?" to your board, customers, or regulators within 30-60 days

If you are at a 50-person-plus security team with full platform control, use [QUICKSTART.md](QUICKSTART.md) instead. It targets a deeper adoption path that this artifact deliberately defers.

## The startup-minimum subset

The full framework has 24 playbooks, 4 framework foundation docs, 5 templates, 3 crosswalks, and a validator. The startup-minimum subset is **3 playbooks + 2 templates + 1 triage card**:

| Artifact | Why it is in the minimum subset |
|---|---|
| **[Playbook 02: Evidence Lives in New Places](playbooks/02-evidence-lives-in-new-places.md)** | The conceptual foundation. Three Realities of AI Evidence. If your team does not internalize these, every other discipline is at risk. Read first. |
| **[Playbook 01: The Agent Is a Privileged Identity](playbooks/01-agent-as-privileged-identity.md)** | The operational keystone. Six Triage Questions. First-Hour Actions. Materiality and Disclosure call convening. This is the playbook your on-call responder works through during an incident. |
| **[Playbook 18: Post-Incident Hardening](playbooks/18-post-incident-hardening.md)** | The 5-business-day closure SLA. Turns lessons into permanent guardrails. Without this, the same incident recurs. |
| **[AI-BOM template](templates/ai-bom.yaml)** | The inventory artifact. Per-agent record of identity, tools, write targets, retrieval, memory, kill-switch status. Exportable in 5 minutes. |
| **[Agent Privilege Matrix](templates/agent-privilege-matrix.csv)** | The tool-tier classification. T0/T1/T2 per tool, with approval gates and reversibility. The substrate for Kill-Switch Mode M3 Tool Tiering. |
| **[Six Triage Questions card](triage/six-questions-card.md)** | The print-and-keep-at-the-desk artifact. Q1 through Q6 plus the Mental Model and Kill-Switch ladder on one page. The most useful single artifact under operational pressure. |

**That is the minimum subset.** Six files. Everything else (the other 21 playbooks, the crosswalks, the schemas, the validator) is the depth that supports specific incident classes and maturity progression beyond Level 2.

## The 4-week adoption path

### Week 1: Inventory (Maturity Level 1: Aware)

**Goal:** know what AI agents you run.

| Day | Action | Effort | Owner |
|---|---|---|---|
| Day 1 | Read [Playbook 02 (Three Realities)](playbooks/02-evidence-lives-in-new-places.md). Internalize the mental shifts. Read [Playbook 01 (The Agent Is a Privileged Identity)](playbooks/01-agent-as-privileged-identity.md) for the operational lens. | ~2 hours | One person |
| Day 2 | List every AI agent in production. Vendor copilots count. Shadow AI counts (per [Playbook 21](playbooks/21-shadow-ai.md) if curious). | ~1 hour | One person |
| Day 3-5 | For each agent: copy [`templates/ai-bom.yaml`](templates/ai-bom.yaml), rename to per-agent (e.g., `ai-bom-customer-support-copilot.yaml`), fill in: agent name, business owner, identity, model, tools, write targets, retrieval corpora, memory configuration. **Set `kill_switches.maturity_target: "level_1_aware"`** for week 1 (you are not yet at Level 2). | ~30-60 min per agent | One person, coordinating with IT for identity scopes |
| Day 7 | **Validate.** Run the [validator](scripts/validate.py) against each AI-BOM. Output should be `OK`. If failures: read the errors, fix the AI-BOM, re-run. | ~15 min | One person |

**End of Week 1 deliverable:** one AI-BOM per agent, validated against schema, with `maturity_target: level_1_aware` set explicitly. Your organization can now answer "what AI agents do we run?" in under 5 minutes.

### Week 2: Tool tiering (preparation for Level 2)

**Goal:** know what each agent can do.

| Day | Action | Effort | Owner |
|---|---|---|---|
| Day 8 | Read [Playbook 04 (Tool Design Is Containment)](playbooks/04-tool-design-is-containment.md). Focus on the T0/T1/T2 vocabulary. | ~1 hour | One person |
| Day 9-12 | Copy [`templates/agent-privilege-matrix.csv`](templates/agent-privilege-matrix.csv). For each tool of each agent: classify as T0 (read-only), T1 (bounded writes), or T2 (systems of record). When unsure, **default to T2**. Specify approval_required, cap_per_run, reversible, write_targets, allowlist. | ~1-2 hours per agent | One person, coordinating with business owner for reversibility |
| Day 14 | **Validate.** Run the validator against the matrix. Output should be `OK`. | ~15 min | One person |

**End of Week 2 deliverable:** Privilege Matrix populated for every agent, with at least one T2 tool per agent showing approval_required=yes. You now have the substrate for Mode M3 Tool Tiering.

### Week 3: Tabletop the kill-switches (Maturity Level 2: Containable)

**Goal:** prove you can stop harm.

| Day | Action | Effort | Owner |
|---|---|---|---|
| Day 15 | Read [Kill-Switch Modes](kill-switches/overview.md). Understand M0-M5 and the M3 variants. | ~1 hour | Whole team |
| Day 16 | For each agent, identify how to activate each of M1 (Read-Only), M2 (Approvals Required), M3 (Tool Tiering), M4 (Full Disable). For vendor copilots: document where M3 and M4 require vendor coordination (per [Playbook 10](playbooks/10-vendor-copilots.md)). | ~2-4 hours per agent | One person + business owner |
| Day 17-19 | **Tabletop each mode.** Walk through what activating each mode looks like in practice. Measure TTA (Time-to-Activate) in minutes. Update the AI-BOM's `kill_switches.mX.tested_at` to today's date and `tta_minutes` to the measured time. | ~1-2 hours per mode per agent | Whole team |
| Day 19 end | Update each AI-BOM: **change `maturity_target` to `level_2_containable`**. Re-run validator. | ~15 min | One person |
| Day 21 | **Print the [Six Triage Questions card](triage/six-questions-card.md).** Distribute to the on-call team. | ~5 min | One person |

**End of Week 3 deliverable:** every agent has all four kill-switch modes tabletop-tested within the past 7 days. Your organization is at Maturity Level 2 (Containable) by the framework's discipline.

### Week 4: Post-incident readiness and trigger the first drill

**Goal:** be ready to respond.

| Day | Action | Effort | Owner |
|---|---|---|---|
| Day 22 | Read [Playbook 18 (Post-Incident Hardening)](playbooks/18-post-incident-hardening.md). Understand the 5-business-day SLA. | ~1 hour | One person |
| Day 23-24 | Document **who is the on-call responder** for each agent and **who approves T2 actions**. Add to the AI-BOM `agent.business_owner` and `agent.technical_owner` fields. If your team is too small for separation: document the contingency (vendor support contact, mutual-aid agreement, board-level escalation path). | ~30 min per agent | Whole team |
| Day 26 | **Run a synthetic incident drill.** Pick one agent. Simulate the scenario: anomalous tool-call spike, suspicious agent output, or customer complaint. Walk through the Six Triage Questions card. Activate Mode M3 Tool Tiering. Document the response timeline. | ~2 hours | Whole team |
| Day 28-30 | **Retrospective.** What worked. What did not. What hardening item is on the 5-business-day list for next week. Update the runbook. Commit to the next monthly drill. | ~2 hours | Whole team |

**End of Week 4 deliverable:** one drill complete, one retrospective documented, one hardening item committed. You are operationally ready for your first real AI incident.

## What you are deliberately deferring

This 4-week path **deliberately defers** the following from the full framework:

- **PB03 (RAG Forensics):** only adopt if your agents have retrieval-augmented generation and the volume justifies the depth.
- **PB06, PB08, PB09, PB10, PB11, PB12** (response-class specific playbooks): read on-demand when you encounter an incident class. Not required for Level 2.
- **PB13 (Six Metrics):** adopt at Level 3 when you have at least 6 months of incident data.
- **PB14 (Testing):** adopt as your drill cadence formalizes past quarterly.
- **PB15, PB23** (records, privacy): adopt when your retention discipline becomes audit-relevant.
- **PB17, PB05, PB24** (executive layer): adopt when your board engagement requires it.
- **PB16 (Training):** adopt when you have more than one on-call responder.
- **PB19, PB22** (procurement, drift): adopt when you make your next AI platform purchase or major model upgrade.
- **PB20 (Maturity Roadmap):** read for context but defer formal level-progression discipline until you have multiple agents at Level 2.
- **PB21 (Shadow AI):** adopt when your organization has more than one team building AI agents.

The framework's discipline is **"adopt only what you can sustainably operate"**. A 5-person team operating PB01 + PB02 + PB18 well is materially better than a 5-person team gesturing at all 24 playbooks badly.

## Limits and honest acknowledgments

This QUICKSTART has limits you should be aware of:

1. **The 30-day path slips for vendor-copilot-heavy environments.** If your AI agents are exclusively vendor copilots (you cannot modify the runtime), some kill-switch modes will be vendor-coordinated and slower than 10 minutes. Document the constraint; do not pretend you have something you do not.
2. **The Level 2 (Containable) claim depends on the customer actually tabletop-testing all four kill-switch modes.** A team that only practices M1 (Read-Only) and M4 (Full Disable) is at Level 1.5; it is honest to claim that explicitly per [framework/03-maturity-roadmap.md](framework/03-maturity-roadmap.md).
3. **Evidence export (Type A through F per [evidence/minimum-evidence-set.md](evidence/minimum-evidence-set.md)) is NOT included in the startup-minimum subset for Level 2.** It is required for Level 3 (Provable). For Level 2 you only need to be able to contain harm; for Level 3 you need to be able to prove what happened. The framework's discipline is honest about the difference.
4. **You will encounter gaps the QUICKSTART does not address.** When you do, the [CONTENT_MAP.md](CONTENT_MAP.md) is the navigation artifact. Read the relevant playbook on-demand rather than trying to memorize the whole framework.

## When you are ready for more

Two natural progression points:

- **When you reach Maturity Level 2 with the startup-minimum subset and have run 3 monthly drills**, graduate to the standard [QUICKSTART.md](QUICKSTART.md). Add PB13 (Six Metrics) and PB14 (Testing) to formalize measurement. Add PB17 (Communication) and PB16 (Training) when you have more than one on-call responder.
- **When you have an externally-visible incident or a customer/regulator inquiry**, add PB24 (Board-Ready Scorecard) and PB05 (Executive Decision-Making) to formalize the executive layer. The CIA+T framing is particularly valuable for incidents where traditional CIA understates the trust impact.

## Related

- **[QUICKSTART.md](QUICKSTART.md)**: the standard 30-day adoption path for well-resourced security teams. Targets Level 2 + Level 3 (Provable).
- **[CONTENT_MAP.md](CONTENT_MAP.md)**: the full repository map; navigate to specific playbooks on-demand.
- **[framework/03-maturity-roadmap.md](framework/03-maturity-roadmap.md)**: the four maturity levels with honest self-assessment criteria.
- **[examples/incident-walkthrough.md](examples/incident-walkthrough.md)**: a worked end-to-end synthetic incident showing the framework in operation. Read this once after Week 4.

---

*Source: AI IR Overlay framework, by Jacob Ideji. Startup-minimum adoption path released in v0.26.0 to close the adoption-friction gap identified in the v0.24.0 holistic critique.*

<https://www.linkedin.com/in/jacobideji/>
