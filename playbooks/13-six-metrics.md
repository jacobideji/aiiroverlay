<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 13: The Six Metrics                                          -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                  -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The measurement playbook. Six metrics that convert AI IR posture from opinion into evidence.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Playbook 13: The Six Metrics

> *Maturity is a number, not an adjective. If you can't graph it, you can't manage it. If you can't manage it, you can't defend it.*

## Premise

The [AI IR Overlay Maturity Roadmap](../framework/03-maturity-roadmap.md) sets four levels: Aware, Containable, Provable, Resilient. Level 4 is defined by a single question: *are the Six Metrics trending in the right direction over rolling 90 days?* This playbook defines those six metrics, the data they require, and the discipline that keeps them honest.

Every CISO has been in the meeting where AI IR readiness is described as *"we're in good shape"* or *"we're getting there."* Those answers don't survive a regulator interview, a board challenge, or an incident post-mortem. The Six Metrics replace adjectives with numbers. Each one is small enough to capture from existing telemetry, repeatable enough to track on a rolling 90-day window, and concrete enough that *trend* (not just *level*) is the primary signal.

The Six Metrics aren't research. They're operational measurements derived from artifacts the framework already produces: the [AI-BOM](../templates/README-ai-bom.md), the [Kill-Switch drill records](14-testing-for-agent-failure-modes.md), the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) capture timestamps, and the [post-incident hardening backlog](18-post-incident-hardening.md). If you've adopted the framework, you already have most of the inputs. This playbook teaches you how to aggregate them.

**Mental Model clause engaged:** *if it can change, manage it as software, with rollback and auditability.* Metrics make AI IR a software-style management discipline: version the measurements, review the trends, and act when the line moves the wrong way.

**Use this playbook when:** building the quarterly board update on AI IR posture, responding to a regulator request for "evidence of continuous improvement," constructing the AI IR section of an internal control self-assessment, or graduating your program from Level 3 (Provable) to Level 4 (Resilient). Use it monthly during the first quarter of a new program. Settle into quarterly cadence once the data stabilizes.

## First-Hour Actions

You don't need a data warehouse to start. The first hour is about establishing one baseline measurement and committing to a publication cadence.

**The 60-minute first metric:**

| Minute | Action |
|---|---|
| 0–10 | Pick **Metric 1: Inventory Currency** (defined below). It's the cheapest to measure and the most strategically informative. |
| 10–25 | Count production agents in your environment. For each, check whether the [AI-BOM](../templates/README-ai-bom.md) `last_reviewed` field is within 7 days. |
| 25–35 | Calculate the percentage. Record it with today's date in a single shared location (Confluence page, spreadsheet, or dashboard). Pick one and commit to it. |
| 35–50 | Define the *trend*: schedule the next measurement for 30 days from today. Same calculation, same place. |
| 50–60 | Tell one person (your manager, your CISO, your risk-committee chair) what number you just measured and what it means. Pre-commit to the next reading. |

That's the first hour. One metric. One reading. One commitment to read it again. Don't define the other five until this one is published twice.

## Containment Options

The Six Metrics cover the four MVO controls plus the two operational disciplines (testing and hardening) that keep the controls real. Each metric has a definition, a data source, and a target.

### Metric 1: Inventory Currency

**Question answered:** *Do we know what's in production right now?*

**Definition:** Percentage of production AI agents with an AI-BOM `last_reviewed` timestamp within the last 7 days.

**Data source:** [AI-BOM](../templates/README-ai-bom.md) repository.

**Target:** ≥ 95% rolling weekly.

**What the trend says:** A declining trend means either new agents are deploying without inventory entries, or existing entries are not being refreshed after configuration changes. Both are MVO-1 violations.

**Maps to NIST AI RMF:** GOVERN 1.6 (inventory mechanisms in place and resourced).

### Metric 2: Containment Time-to-Activate (TTA)

**Question answered:** *Can we actually stop harm fast?*

**Definition:** Median measured TTA across the most recent M1, M2, M3, and M4 drills for each production agent, in minutes.

**Data source:** [Kill-Switch drill records](14-testing-for-agent-failure-modes.md) stored in the AI-BOM `kill_switches.mX.tta_measured` fields.

**Target:** ≤ 10 minutes for M1, M2, M3, M4 (per [Kill-Switch Modes specification](../kill-switches/overview.md)).

**What the trend says:** Rising TTA usually means runbook drift, approver-chain turnover, or tool-registry changes that broke the activation path. Falling TTA means the drill program is producing real muscle memory.

**Maps to NIST CSF 2.0:** RS.MA-04 (incident escalation timeliness).

### Metric 3: Evidence Export Time

**Question answered:** *Can we prove what happened, on demand?*

**Definition:** Median minutes from incident-declaration order to full [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A–F captured, measured in drill exercises (live incidents are too rare to drive a stable trend).

**Data source:** Drill logs from M4 Full Disable exercises.

**Target:** ≤ 60 minutes (per Overlay conformance criterion).

**What the trend says:** Rising export time usually means an evidence source has retention or access friction that wasn't there 90 days ago. Common culprits: model-provider log TTL changes, SaaS audit-log access workflow changes, vector store version-history changes.

**Maps to NIST AI RMF:** MEASURE 2.7 (security and resilience evaluated and documented), MANAGE 4.1 (post-deployment monitoring plans).

### Metric 4: Drill Currency

**Question answered:** *Is the capability real or theoretical?*

**Definition:** Percentage of production AI agents with each Kill-Switch mode (M1 through M4) tested within the last 90 days.

**Data source:** AI-BOM `kill_switches.mX.tested_at` fields.

**Target:** ≥ 90% for M1, M2, M3 per quarter. M4 tested at least annually per agent.

**What the trend says:** This is the Maturity Roadmap's hard rule made measurable: *if untested in 90 days, you don't have it.* A declining trend converts your program from Containable (Level 2) to Aware (Level 1) by definition. Watch this one weekly during a program ramp.

**Maps to NIST AI RMF:** MANAGE 2.4 (supersede, disengage, or deactivate AI systems).

### Metric 5: Hardening SLA Compliance

**Question answered:** *Are we actually getting better between incidents?*

**Definition:** Percentage of post-incident hardening backlog items closed within the 5-business-day SLA defined in [Playbook 18](18-post-incident-hardening.md).

**Data source:** Post-incident hardening backlog (typically tracked in Jira, ServiceNow, or the AI-BOM `incidents_history` block).

**Target:** ≥ 90% rolling quarter.

**What the trend says:** A declining trend means the hardening discipline is sliding from "code change" back to "memo." Without this metric, post-incident reviews silently degrade into documentation theater. With it, the SLA either holds or fails publicly.

**Maps to NIST AI RMF:** MANAGE 4.2 (continual improvement activities integrated into system updates).

### Metric 6: Controlled Re-Enable Success Rate

**Question answered:** *When we restart agents after an incident, do they stay up?*

**Definition:** Percentage of [M5 Controlled Re-Enable](../kill-switches/overview.md) sequences completed end-to-end without rollback to M4 or below within the first 72 hours.

**Data source:** Incident logs and M5 drill records.

**Target:** ≥ 85% rolling year.

**What the trend says:** A low or declining rate means recovery validation is too lax. The agent comes back online before the underlying gap is closed, and the same scenario class re-triggers. Rising rate means the M5 sequence has real gates, not ceremonial ones.

**Maps to NIST AI RMF:** MANAGE 4.3 (incidents and errors communicated, processes for recovery followed and documented).

## Evidence Priorities

The Six Metrics produce evidence, but they also depend on evidence. Treat the underlying records as primary artifacts.

| Metric | Underlying evidence to preserve |
|---|---|
| Inventory Currency | AI-BOM commit history (versioned in source control) |
| Containment TTA | Drill logs with timestamps, approver IDs, probe results |
| Evidence Export Time | Drill records showing A–F capture sequence and times |
| Drill Currency | AI-BOM `tested_at` fields and supporting drill artifacts |
| Hardening SLA | Backlog tickets with creation date, closure date, and code-change linkage |
| Re-Enable Success | M5 sequence checklists with go/no-go decisions per stage |

If the regulator or auditor asks *"show me the data behind your Level 4 claim,"* you point at this evidence chain, not at the metric values themselves. The values without their evidence are unverifiable. The evidence without the values is uninterpretable. You need both.

## Recovery Sequence

When one of the Six Metrics moves the wrong way (a single declining reading is noise; two consecutive readings is a signal), treat it as a containment-class event for your program.

1. **Confirm the data.** Pull the underlying records. Distinguish *real decline* from *measurement artifact*. A drop in Inventory Currency because three new agents shipped without AI-BOM entries is different from a drop because the dashboard query broke.
2. **Identify the operational cause.** Use the same categories as incident root-cause analysis: process gap, tooling gap, ownership gap, telemetry gap. Don't accept "we got busy" as a cause. Find the structural reason.
3. **Open a hardening backlog item.** The same 5-business-day SLA from [Playbook 18](18-post-incident-hardening.md) applies. Metrics decay is a class of incident.
4. **Adjust upstream control.** If Metric 4 (Drill Currency) is declining, the fix isn't more dashboards. It's a calendar entry, an owner change, or a tool that automates drill scheduling.
5. **Watch the next two readings.** If the trend reverses within 30 days, the fix worked. If not, the structural cause is deeper than the first attempt.

## Post-Incident Hardening

The Six Metrics program graduates from "we measure things" to "we operate by data" when three things become routine:

1. **Metrics are published on a fixed cadence.** Monthly for the first quarter. Quarterly thereafter. Publication isn't a slide deck. It's a single page with six numbers, six trend arrows, and one paragraph per metric that's red or amber.
2. **The [Board-Ready Scorecard](24-board-ready-scorecard.md) inherits from the metrics.** The four scorecard domains (Containment, Evidence, Governance, Recovery) map directly to combinations of the Six Metrics. Containment domain = Metrics 2 and 4. Evidence domain = Metric 3. Governance domain = Metric 1. Recovery domain = Metrics 5 and 6.
3. **A declining metric automatically becomes an agenda item.** Not on the next quarterly review. On the next standing risk meeting. Time matters. A metric that's been red for 90 days without action is the same operational signal as an unattended incident ticket.

This is the discipline that distinguishes Level 4 (Resilient) from Level 3 (Provable). Provable means you can demonstrate the capability when asked. Resilient means the demonstration is unnecessary because the data is already published.

## Common Pitfalls

| Pitfall | Why it happens | What it costs |
|---|---|---|
| **Measuring level, not trend** | Easier to report a single number than a 90-day arrow. | The board sees a snapshot but misses the direction of travel. Decay goes unnoticed until it's a step-change. |
| **Defining new metrics every quarter** | Each metric feels incomplete, so the team keeps adding refinements. | Trend lines reset. Comparability across quarters dies. The Six Metrics work *because* they don't change, not in spite of it. |
| **Letting Metric 4 (Drill Currency) drop quietly** | Drills slip when engineering is busy. | The program silently drops from Level 2 to Level 1 by definition, but the scorecard still says GREEN until someone notices. |
| **Reporting Inventory Currency from a wiki page** | The page exists and looks current. | Wiki pages are not source-controlled. They drift without anyone noticing. The AI-BOM repository must be the system of record. |
| **Aggregating across agents without surfacing outliers** | A 92% inventory-currency average looks fine. | The 8% missed agents are likely your highest-risk Tier-2 actors. Report the average AND the outlier list. |
| **Treating measurement as the goal** | The metric becomes the work. | The point of the Six Metrics is to drive action, not to occupy attention. If a quarter's metrics review didn't change a single backlog priority, the program is in measurement theater. |

## Related

Distributed as separate packages:

- **Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Defines the four levels these metrics measure. The Level 4 (Resilient) test points directly at this playbook.
- **AI-BOM template:** [`templates/README-ai-bom.md`](../templates/README-ai-bom.md). The primary data source for Metrics 1, 2, and 4.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). Source of the TTA targets that Metric 2 measures against.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A–F capture sequence that Metric 3 times.
- **Playbook 14 (Testing for Agent Failure Modes):** [`14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md). Generates the drill data behind Metrics 2 and 4.
- **Playbook 18 (Post-Incident Hardening):** [`18-post-incident-hardening.md`](18-post-incident-hardening.md). Defines the 5-business-day SLA measured by Metric 5.
- **Playbook 24 (Board-Ready Scorecard):** [`24-board-ready-scorecard.md`](24-board-ready-scorecard.md). The executive translation layer for all six metrics.
- **Crosswalks:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) for MEASURE and MANAGE function mappings.

## The Question to Carry Forward

When your board asks next quarter whether AI IR posture is improving, can you point at six numbers, six trend arrows, and a single sentence per arrow? If any of those three is missing, this playbook is your work plan. Build the first metric this week. Publish it. Schedule the next reading. Treat the dashboard as a product, not a deliverable.

---

*Source: AI IR Overlay newsletter, Issue #13, "The Six Metrics: Measuring AI IR Maturity," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
