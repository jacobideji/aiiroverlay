<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 20: AI IR Maturity Roadmap (Operating View)                  -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                  -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0. See LICENSE file in this package.                -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The operating playbook for the AI IR Maturity Roadmap. How you run the model in production, what cadence holds it honest, and how a maturity claim moves from documented to demonstrated.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Playbook 20: AI IR Maturity Roadmap (Operating View)

> *Maturity is not a document. It is the answer to one question, asked under time pressure: if your most privileged AI agent misbehaved right now, could you stop, prove, and scope it within the first hour?*

## Premise

The framework view of maturity defines four levels (Aware, Containable, Provable, Resilient) and the test question at each. That view lives in [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md) and answers *"what does maturity mean?"* This playbook is the **operating view**. It answers a different question: *"how do you run the model so the level you claim is the level you actually have?"*

Most organizations claim Level 3 (Provable) and discover during a real incident that they are honestly at Level 1 (Aware) plus some Level 2 capability that has never been tested under pressure. The gap is rarely a knowledge gap. It is an **operating discipline gap**. The model itself is sound. The cadence behind it is the failure.

This playbook fills that gap. It defines the operating cadence (weekly, monthly, quarterly, annual), the realistic activities at each level, the gap that stalls progression at each level, and the 30-minute agent-focused reality check that converts a level claim into a level demonstration. It also names the most common failure mode that turns a maturity program into a documentation theater: pursuing Level 4 metrics on top of Level 2 controls that were never tested.

**Mental Model clauses engaged:** all four. Maturity is the operating expression of the framework's full discipline. *Acts* (the privileged-identity lens shapes Level 1 inventory and Level 2 containment), *Remembers* (memory scope is in the AI-BOM at Level 1 and audited at Level 3), *Retrieves* (corpus discipline shapes Level 2 tool tiering and Level 3 evidence), *Changes* (every level requires the version-controlled artifacts that Level 4 measures).

**Use this playbook when:** building a 12-month AI IR program plan, responding to a board or audit question about maturity, preparing a quarterly readiness review, recovering after a real incident exposed a maturity gap, or kicking off a new AI agent rollout that requires a defensible posture from day one.

## First-Hour Actions

You do not need a 12-month plan to begin operating the roadmap. The first hour is about producing one honest data point on one agent, using one assessment, and committing to the next reading.

### The 60-minute first-pass

| Minute | Action | Owner |
|---|---|---|
| 0–10 | Pick **one** production AI agent. Pull its [AI-BOM](../templates/ai-bom.yaml), or write the missing fields if the AI-BOM does not yet exist. | Agent business owner |
| 10–25 | Run the 30-minute reality check (defined below) on that agent. Three questions. Record the answers honestly, not aspirationally. | Incident Commander or risk owner |
| 25–35 | Map the answers to a level claim. Most agents land at Level 1 with partial Level 2 on first measurement. That is normal. | Incident Commander |
| 35–45 | Identify **one** capability gap. Not three. Not five. The one that, if closed, lifts the agent the most. Common single-gap candidates: an untested M3 Tool Tiering activation, a missing Type C retrieval trace, an AI-BOM that is more than 7 days old. | Agent business owner |
| 45–55 | Open a 30-day commitment to close that one gap. Owner, deadline, acceptance criterion. Treat it as a [Playbook 18](18-post-incident-hardening.md) hardening backlog item with the same 5-business-day SLA discipline applied to the gap-closure design. | Agent business owner + CISO |
| 55–60 | Schedule the next reassessment. **30 days from today**, same agent, same three questions. Pre-commit to the date. | Incident Commander |

That is the entire first hour. One agent, one reality check, one gap, one commitment. Do **not** scale to other agents until the first one has shown one measured improvement. The 90-day rule applies in reverse here too: if a capability you claim has not been measured in 90 days, you do not have it.

## Containment Options

A maturity roadmap is **not** an incident response playbook. But the level you operate at directly determines which [Kill-Switch Modes](../kill-switches/overview.md) you can execute under pressure. The roadmap is the precondition that makes containment real.

### Level-to-containment realism mapping

| Maturity level | Containment modes you can credibly execute | Containment modes that are documented but not real |
|---|---|---|
| **Level 1 (Aware)** | M0 Observe | M1–M4 exist on paper. None will activate cleanly in 10 minutes. |
| **Level 2 (Containable)** | M0, M1, M2 (tested in last 90 days) | M3 Tool Tiering may exist but is unrehearsed. M4 disable may have credential-rotation timing problems. |
| **Level 3 (Provable)** | M0, M1, M2, M3, M4 (all tested in last 90 days) AND evidence capture in 60 min | M5 Controlled Re-Enable is documented but may collapse to a single binary decision under business pressure. |
| **Level 4 (Resilient)** | All six modes, all tested quarterly, plus measured improvement in TTA and Time-to-Evidence over 90-day windows | None. |

**The asymmetry to internalize:** a Level 1 organization claiming Level 3 capability believes its runbook describes a real procedure. When the incident hits, the runbook describes a wish. The operating cadence in this playbook is the work that converts the wish into a procedure.

### When to step the agent down a level

A maturity roadmap is not monotonic. Agents move backwards. Common triggers:

- A new write tool was added without an updated AI-BOM. The agent regresses to Level 1 by definition.
- The M3 tool-tiering matrix was not refreshed after a new T2 tool joined the agent's registry. The agent regresses to Level 2 partial.
- The retrieval corpus list changed but Type C traces were not re-enabled for the new corpus. The agent regresses to Level 2 from Level 3.
- A quarter slipped without a tabletop. By definition, every untested mode is no longer tested in the last 90 days. The agent regresses one level.

**Operational requirement:** the roadmap reading on every production agent updates at least quarterly. Faster (monthly) during program ramp or after material configuration change. The level claim has a freshness date attached.

## Evidence Priorities

Maturity claims are testable. The evidence the roadmap requires is mostly produced by other playbooks already; this playbook puts the chain together.

| Maturity level | Required evidence | Lives in |
|---|---|---|
| **Level 1 (Aware)** | A current AI-BOM (refreshed within 7 days) for every production agent. | [`templates/ai-bom.yaml`](../templates/ai-bom.yaml) per agent, version-controlled. |
| **Level 2 (Containable)** | M1, M2, M3, M4 `tested_at` fields populated within last 90 days. Drill TTA values recorded. | AI-BOM `kill_switches` section, per agent. |
| **Level 3 (Provable)** | A documented [Minimum Evidence Set A–F](../evidence/minimum-evidence-set.md) export within the 60-minute SLA, from a drill in the last 90 days. Export logs preserved. | Drill records, per agent. |
| **Level 4 (Resilient)** | [Six Metrics](13-six-metrics.md) published on a fixed cadence. Trend lines moving in the right direction over rolling 90 days. Hardening backlog closures within 5-business-day SLA. | Metrics dashboard, hardening backlog, [Playbook 24 Board Scorecard](24-board-ready-scorecard.md). |

**Operational rule:** if you cannot produce the evidence above for the level you claim, the level you claim is the level above the highest level whose evidence you can produce. Most teams are humbled by this rule the first time they run it on a real agent. That humbling is the most valuable output of the first quarterly assessment.

### The 30-minute reality check (single-agent assessment)

Use this on a single agent. It does not require a tabletop, an external auditor, or a long meeting. It requires three honest answers, in writing, with the evidence beside each.

| # | Question | Evidence required to pass | Failure means |
|---|---|---|---|
| **1** | Can the agent be switched to **Read-Only (M1)** mode? | Demonstrated activation in staging or production with confirmed write-tool unreachability. Time-to-activate measured. | The agent is at Level 1 for containment. M1 is documented but not real. |
| **2** | Can you **export tool-call and retrieval logs** for the preceding hour, in structured format, with attempted-call rows present? | Files in hand within 30 minutes, opened, spot-checked for the right columns. | The agent is at Level 2 at best. Level 3 evidence claims are aspirational. |
| **3** | Can you **enumerate write targets with confidence** (downstream system + object touched)? | Citable list from the AI-BOM `tools[].write_targets` section, less than 7 days old. | The agent is at Level 1 for inventory. Containment scoping under pressure will be a guess. |

Three pass marks = Level 3 at minimum. Two pass marks = Level 2 at best. One or zero = Level 1, regardless of what the wiki page says.

## Recovery Sequence

When a quarterly assessment exposes a regression, treat it like an incident. The recovery sequence here applies to **the maturity program itself**, not to a single agent's IR.

1. **Confirm the regression with data.** Pull the drill log, the AI-BOM diff, or the missed cadence. Distinguish *real decline* (a capability was lost) from *measurement artifact* (the dashboard query broke).
2. **Identify the operational cause.** Process gap, tooling gap, ownership gap, or telemetry gap. Avoid "we got busy" as a cause. Find the structural reason.
3. **Open a maturity hardening item.** Apply the [Playbook 18 hardening discipline](18-post-incident-hardening.md): one specific control change, one owner, 5-business-day SLA, measurable acceptance criterion.
4. **Re-test within 30 days.** A fix that has not been re-drilled is theoretical. Schedule the redrill at item-creation time, not at fix-completion time.
5. **Update the maturity level claim publicly.** If the agent slipped from Level 3 to Level 2 partial, the board scorecard reflects that on the next regular publication date. Hiding the slip until it is fixed is the same operating failure that produced the slip.

A Level 4 organization is not one that never regresses. It is one that detects and recovers from regressions within the same cadence cycle in which they occurred.

## Post-Incident Hardening

The roadmap is where lessons from a real incident become next quarter's measurement target. Without this loop, a closed incident produces a memo. With it, a closed incident produces a permanently elevated measurement.

After every incident closure ([Playbook 18](18-post-incident-hardening.md)), the maturity program does three things:

1. **Convert the incident finding into a roadmap commitment.** If the incident exposed an untested M3 activation path, the commitment is to drill M3 quarterly for the next year on that agent. Add it to the quarterly cadence calendar with an owner.
2. **Add the relevant metric to the dashboard.** If TTSM regressed during the incident, add TTSM tracking to the dashboard if it was not already there. Lessons learned that do not become measurements become forgettings learned.
3. **Republish the maturity level claim for the affected agent.** If the agent regressed during the incident, the new claim reflects the post-incident state, not the pre-incident state. The Board Scorecard for next quarter reflects this honestly.

### The four-quarter improvement loop

A Level 4 organization runs this loop without ceremony:

| Quarter activity | What it produces | Where it lands |
|---|---|---|
| Inventory refresh on every production agent | Current AI-BOMs | Source-controlled `ai-bom/` directory |
| Drill each agent's M1–M4 modes | Measured TTA values | AI-BOM `kill_switches` section |
| Run one Type C–extended retrieval-forensics drill if any agent uses RAG | Verified [PB03](03-rag-knowledge-base-forensics.md) freeze-the-world sequence works | Drill records |
| Publish [Six Metrics](13-six-metrics.md) reading | Trend update | Metrics dashboard |
| Update [Board Scorecard](24-board-ready-scorecard.md) | GREEN, AMBER, RED snapshot | Board package |
| Close the top-priority hardening item from the prior quarter | One measurable risk reduction | Hardening backlog |

If all six rows are checked every quarter for every Tier-2 agent, the organization is operating at Level 4. If three or fewer are checked, the organization is operating at Level 2 with documented Level 3 ambitions.

## Common Pitfalls

These are the operating failure modes that turn a maturity program into documentation theater. Each has been observed across enough engagements to name as patterns.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Claiming Level-3 capabilities never tested in the last 90 days** | The runbook exists; the muscle memory does not. | First real incident exposes the gap publicly. Board credibility falls faster than it was earned. |
| **Skipping Level 1 (inventory) and starting at Level 4 (resilience)** | Resilience metrics are easier to defend in a board meeting than inventory completeness. | No foundation to measure against. Metrics improve while blast radius stays unchanged. |
| **Pursuing Level 4 metrics with Level 2 controls** | Dashboards are easier to ship than drill cadences. | Numbers trend right while the actual controls degrade. The first incident produces a gap between metrics and reality. |
| **Treating maturity as a destination** | "We hit Level 3" feels like an achievement to file. | Continuous improvement decays into snapshot reporting. Roadmap reading staleness becomes the leading indicator of program collapse. |
| **Outsourcing the assessment to a vendor without operating the cadence internally** | An annual external audit feels like compliance done. | The level claim is unowned in the operating model. No one inside the org drills the modes between audits. |
| **Rating across all agents into a single org-level claim** | "Our AI IR maturity is Level 3" reads better than "two of seven agents are at Level 3." | High-risk agents hide inside the average. The board sees green while the most exposed agent is amber or red. |
| **Letting the AI-BOM go stale between agent changes** | Engineering ships a new tool; the AI-BOM update is "next sprint." | The agent silently regresses to Level 1 and no one notices until an incident asks "what can this thing write to?" |
| **No public regression report when an agent slips a level** | Easier to fix quietly. | The maturity program is no longer credible to the board. The next slip will be hidden longer. |
| **Quarterly tabletops that read the runbook aloud** | Convenient. Cheap. Calendar-friendly. | The runbook gets signed off without anyone activating a mode or measuring a TTA. [Playbook 14](14-testing-for-agent-failure-modes.md)'s "tabletop theater" pitfall, applied to the maturity program itself. |
| **Scorecard published once, never republished** | One slide deck satisfies the board for the year. | By month 6, the scorecard is stale. By month 12, it is wrong. The next board meeting produces lower trust, not higher. |

## What Maturity Is NOT

A short list, because it deserves to be in writing. Maturity is **not**:

- Policy documents without operational drills behind them
- The number of AI tools deployed
- A statement that the org "uses NIST AI RMF"
- Vendor certifications attached to a procurement deck
- A scorecard that has never produced a remediation ticket
- The level claimed on the most recent self-assessment

Maturity is demonstrated, not declared. The reality check produces the demonstration.

## Related

- **The Maturity Roadmap (framework view):** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). The four-level model and test questions this playbook operationalizes.
- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 through MVO-4 are the controls each level adds.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). The four clauses cross-cut every maturity level.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The modes the levels make real.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A–F set that Level 3 must export within 60 minutes.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). Level 1 inventory artifact and Level 2 drill record.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The tier discipline Level 2 measures.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The response lens every maturity claim depends on.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). Required at Level 3 for any agent using retrieval.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). Pre-incident discipline that makes Level 2 real.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). Level 4 trend data lives here.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The drill discipline that produces the Level 2 and Level 3 evidence.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA that maturity-regression recovery inherits.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). The executive translation of the maturity reading.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.4, MANAGE 4.2, MANAGE 4.3).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports ID.IM-01, ID.IM-02, GV.OV-01, GV.OV-02).

## The Question to Carry Forward

If your most privileged AI agent misbehaved right now, could you demonstrate Containment (Level 2) and Provability (Level 3) within the first hour, using current evidence, with a named owner, citing a drill from the last 90 days? Or would the response be improvised?

If improvised, the starting point is the 60-minute first-pass at the top of this playbook. Run it on the one agent that scares you most. Schedule the next reading. Treat the reading as the deliverable, not the program plan.

That is how a maturity claim moves from documented to demonstrated. One agent, one reading, one closed gap at a time, on a calendar that holds.

---

*Source: AI IR Overlay newsletter, Issue #20, "AI IR Maturity Roadmap," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
