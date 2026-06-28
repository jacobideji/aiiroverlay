<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 14: Testing for Agent Failure Modes                          -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                  -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The pre-production playbook. If your Kill-Switch modes haven't been tested in the last 90 days, you don't have them.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Playbook 14: Testing for Agent Failure Modes

> *Documented containment is not containment. A Kill-Switch that has never been pulled is a hope, not a capability. Test it before the regulator does.*

## Premise

Every AI IR program eventually faces the same question on a board call: *"Can you stop this agent in under ten minutes?"* The runbook says yes. The architecture diagram says yes. The Kill-Switch documentation says yes. The honest answer, for most teams, is *"we believe so, but we've never actually pulled the lever in production."*

That's the gap this playbook closes.

Testing for agent failure modes is the discipline that converts a written Kill-Switch ladder into a measured operational capability. It's also the cheapest control in the entire framework. A 90-minute tabletop costs less than one production incident. A 90-second M1 (Read-Only) activation drill costs less than one hour of regulator interview prep. Yet most organizations spend more on AI procurement than on AI containment testing, and most discover that gap the first time they need to act.

The [AI IR Overlay Maturity Roadmap](../framework/03-maturity-roadmap.md) sets a hard rule: *if a capability has never been tested in the last 90 days, you do not have it.* Playbook 14 is how you stay inside that 90-day window.

**Mental Model clause engaged:** *if it can act, govern it as a privileged identity.* You test privileged-access break-glass procedures. You should test agent break-glass procedures the same way, on the same cadence, with the same approvers.

**Use this playbook when:** you're preparing for a production agent rollout, scheduling the next quarterly tabletop, responding to an audit finding about untested controls, or writing the test plan for [Kill-Switch Modes M1 through M4](../kill-switches/overview.md). Use it during an active incident only if the incident itself exposed an untested mode. In that case, treat the live event as a forced drill and capture the gap immediately.

## First-Hour Actions

If you've never run a Kill-Switch drill, don't try to test everything at once. Start with the cheapest, lowest-risk mode and prove the muscle memory exists.

**The 60-minute first drill (M1 Read-Only only):**

| Minute | Action |
|---|---|
| 0–10 | Pick **one** production agent. Confirm its tool list from the [AI-BOM](../templates/README-ai-bom.md), not from memory. |
| 10–20 | Verify the M1 activation path in code or config. Who flips the switch? Where? With what authorization? |
| 20–35 | Run the drill against a **staging copy** of the agent. Measure Time-to-Activate (TTA) from incident-commander order to mode in effect. |
| 35–45 | Confirm logging continues at M0 fidelity during M1. Confirm read tools still respond. Confirm write tools are stripped. |
| 45–55 | Document TTA, the approver chain, and any friction observed. Update the [AI-BOM](../templates/README-ai-bom.md) `kill_switches.m1.tested_at` field. |
| 55–60 | Schedule the next drill. M2 next week. M3 the week after. M4 within 30 days. |

That's the first-hour version. One agent. One mode. One measurement. Don't theorize the rest until the first one is real.

## Containment Options

The Overlay defines four testable Kill-Switch modes plus Controlled Re-Enable. Each one has a distinct test design because each one fails differently in production.

### M1 Read-Only Drill

**Purpose:** Confirm write tools can be stripped without breaking read paths.

**Test design:**

1. Activate M1 against a staging copy of the agent (or against production during a maintenance window if staging doesn't reflect real tool configuration).
2. Issue a representative read query. Confirm it succeeds with logs.
3. Issue a representative write call. Confirm it's rejected at the tool layer, not at the model layer.
4. Measure TTA from order to mode-in-effect.

**Pass criteria:**

- TTA ≤ 10 minutes by a Tier-1 SOC analyst (not just by the agent owner).
- Read tools confirm operational by automated probe.
- Write tools confirm unreachable by automated probe.
- Logging fidelity matches M0.

**Common failure:** the "off" switch only stops *new* sessions but lets active sessions continue writing for minutes. Test session termination, not just future invocations.

### M2 Approvals Required Drill

**Purpose:** Confirm a human approver actually gates tool calls before execution.

**Test design:**

1. Activate M2. Send a tool call that should queue for approval.
2. Approver receives the request through the designated channel (Slack, PagerDuty, ServiceNow ticket, whatever's documented).
3. Approver denies the first request. Confirm the agent treats denial as terminal, not retry.
4. Approver approves a second request. Confirm execution proceeds with the approver's identity in the audit log.

**Pass criteria:**

- Approval latency stays under your business-need threshold (typically ≤ 5 minutes during business hours).
- Denied calls are logged as denied, not as failed retries.
- Approver identity appears in downstream SaaS audit logs alongside the agent identity.

**Common failure:** the approval queue is staffed by the same engineer who owns the agent. That's not two-person rule. Test that the approver and the owner are distinct roles with distinct authority.

### M3 Tool Tiering Drill

**Purpose:** Confirm Tier-2 tools can be disabled selectively without disabling Tier-0/Tier-1 tools.

**Test design:**

1. Reference the [Agent Privilege Matrix](../templates/README-privilege-matrix.md) for the agent.
2. Identify the top three Tier-2 tools (typically send external email, write to systems of record, deploy code).
3. Activate M3. Confirm each Tier-2 tool returns disabled status to an automated probe.
4. Confirm Tier-0 and Tier-1 tools still respond.
5. Measure TTA.

**Pass criteria:**

- TTA ≤ 10 minutes by Tier-1 SOC.
- Tier-2 disable confirmed by direct probe (do not trust configuration alone).
- Tier-0 and Tier-1 continue serving business workload.
- The agent fails gracefully when a Tier-2 tool is unavailable (returns "I can't perform that action right now" rather than silently producing wrong output).

**Common failure:** the tool tiering exists in the privilege matrix CSV but isn't wired into the agent's runtime tool registry. Test that disabling the row actually disables the tool, not just the documentation.

### M4 Full Disable Drill

**Purpose:** Confirm the agent can be taken offline cleanly with evidence preservation intact.

**Test design:**

1. Activate M4 against a staging copy (M4 in production is usually too disruptive for routine testing, but it should be tested at least annually).
2. Confirm active sessions terminate, not just new sessions.
3. **Before** any credential rotation, confirm the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) is captured: prompts (A), tool calls (B), retrieval (C), memory (D), configuration (E), identity logs (F).
4. **Then** rotate credentials, clean corpora, and prepare for M5.

**Pass criteria:**

- TTA ≤ 10 minutes by Tier-1 SOC.
- Evidence Set A–F captured within 60 minutes of declaration, before any state-mutating recovery actions.
- Token rotation does not precede scope capture (this is the most common evidence-destruction failure in AI IR).

**Common failure:** the runbook says "rotate credentials" before "snapshot identity scopes." Drill the opposite order until it's reflex.

### M5 Controlled Re-Enable Drill

**Purpose:** Confirm staged recovery actually validates each step before advancing.

**Test design:**

1. After an M4 drill, run the M5 sequence end-to-end.
2. Step 1: re-enable in M1 only. Confirm logs flow.
3. Step 2: validate retrieval and tool policies against the hardened configuration.
4. Step 3: replay the incident scenario in a sandbox. Confirm the fix holds.
5. Step 4: re-enable Tier-0 (read-only) tools first, then Tier-1 (bounded writes), incrementally with monitoring.
6. Step 5: return to M0 Observe only after all of the above passes.

**Pass criteria:**

- CISO or designated Incident Commander approves the M5 sequence start. The original agent owner alone is **never** sufficient.
- Each stage produces a documented "go/no-go" decision before advancing.
- A failed sandbox replay sends the team back to hardening, not forward to production.

## Evidence Priorities

Testing produces evidence. That evidence is your audit defense. Capture it deliberately.

For each drill, record:

| Field | Where it goes |
|---|---|
| **Date and agent** | [AI-BOM](../templates/README-ai-bom.md) `kill_switches.mX.tested_at` |
| **Measured TTA** | AI-BOM `kill_switches.mX.tta_measured` |
| **Approver chain exercised** | Drill log + runbook |
| **Probes used to verify mode in effect** | Test plan + drill log |
| **Friction observed** | Hardening backlog (per [Playbook 18](18-post-incident-hardening.md)) |
| **Gap if pass criteria missed** | Incident-style after-action review |

The AI-BOM is the audit-facing system of record. If a regulator or auditor asks *"when did you last test M3 on the sales-triage copilot?"*, you point to the `tested_at` field. If the field is empty or older than 90 days, the answer is *"we don't currently have M3 on that agent,"* full stop.

**Cross-reference for auditors:**

- NIST AI RMF MANAGE 2.4: *"Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems."* Tested drills are how you prove "in place and applied."
- NIST CSF 2.0 RS.MA-04: incident escalation. The ≤ 10 minute TTA is your measured escalation criterion for M1 through M4.
- OWASP Agentic Top 10 ASI02 (Tool Misuse) and ASI08 (Cascading Failures): testing M3 directly defends against both.

## Recovery Sequence

When a drill exposes a gap (and the first three drills always will), treat it like a real incident.

1. **Stop the rollout.** If the agent isn't yet in production, hold deployment until the gap closes. If it's already in production, decide whether to leave it active or step down to a lower-risk mode while the gap is fixed.
2. **Document the gap as a finding.** Use the same format as an incident after-action: what failed, why, what the fix is, who owns it, by when.
3. **Fix the gap.** Common fixes: wire the tool registry to the privilege matrix, separate approver and owner roles, add automated probes to verify mode in effect, scope token rotation after evidence capture.
4. **Re-drill within 30 days.** A fix that hasn't been re-drilled is theoretical. Repeat the test that exposed the gap, plus the next mode up the ladder.
5. **Update the AI-BOM.** Reset the `tested_at` clock. Note any change in tool tiering, approver chain, or evidence capture procedure.

## Post-Incident Hardening

Tabletop discipline becomes a hardening program when three things happen:

1. **Drills run on a fixed cadence**, not on calendar-permitting basis. Quarterly is the floor for production agents handling Tier-2 actions. Monthly is appropriate for agents with broad SaaS write access (CRM, ERP, code repo, financial systems).
2. **Drill results enter the [Board-Ready Scorecard](24-board-ready-scorecard.md).** The Containment domain's GREEN/AMBER/RED status flows directly from the most recent drill. Skipped drills convert GREEN to AMBER. Failed drills convert AMBER to RED.
3. **Failed drills produce hardening backlog items**, not memos. The 5-business-day Hardening SLA from [Playbook 18](18-post-incident-hardening.md) applies. A gap that's been "documented" for 60 days without code change is operationally identical to no documentation at all.

The quarterly cadence isn't ceremonial. It's the smallest interval that catches drift from agent reconfiguration, tool registry changes, retrieval corpus updates, and approver role turnover. Anything longer than 90 days is enough time for any of those four variables to move without your test plan noticing.

## Common Pitfalls

| Pitfall | Why it happens | What it costs |
|---|---|---|
| **Tabletop theater** | The drill is read aloud in a conference room without anyone actually flipping a switch or measuring TTA. | The runbook gets signed off without the capability being verified. |
| **Agent owner approves their own M2 calls** | Convenient for the engineering team. | Two-person rule fails on contact. Approver bias is the same risk M2 is designed to prevent. |
| **Token rotation before scope capture in M4 drill** | Sysadmin reflex from traditional IR. | The Evidence Set A–F is destroyed before it's captured. The drill teaches the wrong reflex. |
| **M3 drilled by disabling tools at the documentation layer, not the runtime layer** | The privilege matrix CSV is edited but the agent's actual tool registry isn't refreshed. | The agent keeps calling the "disabled" tool in production, and nobody notices. |
| **Drill cadence drifts past 90 days** | Engineering pressure, holiday calendar, reorg. | The capability is no longer current per the Maturity Roadmap. You drop from Level 2 (Containable) to Level 1 (Aware) by definition. |
| **Failed drills produce a memo, not a code change** | Easier to write a paragraph than to refactor a tool wrapper. | Hardening backlog grows but production posture doesn't. The next drill fails the same way. |

## Related

Distributed as separate packages:

- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). Full M0 through M5 mode specifications and TTA targets that this playbook tests against.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A–F evidence types that M4 drills must preserve before any state-mutating recovery.
- **AI-BOM template:** [`templates/README-ai-bom.md`](../templates/README-ai-bom.md). The `kill_switches` section is the system of record for drill dates and measured TTA.
- **Agent Privilege Matrix:** [`templates/README-privilege-matrix.md`](../templates/README-privilege-matrix.md). The M3 drill validates that this matrix is wired into the runtime, not just the documentation.
- **Playbook 04 (Tool Design Is Containment):** [`04-tool-design-is-containment.md`](04-tool-design-is-containment.md). Without pre-tiered tools, the M3 drill has nothing to test. Run PB04 first if your privilege matrix isn't current.
- **Playbook 18 (Post-Incident Hardening):** [`18-post-incident-hardening.md`](18-post-incident-hardening.md). Failed drills enter PB18's 5-business-day hardening SLA.
- **Playbook 24 (Board-Ready Scorecard):** [`24-board-ready-scorecard.md`](24-board-ready-scorecard.md). Drill results map directly to the Containment domain status.
- **Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). The 90-day rule for testing currency lives here.

## The Question to Carry Forward

If the regulator asked tomorrow *"when did your team last activate M3 on your highest-risk production agent, who approved it, and how long did it take?"*, do you have a date, a name, and a number? If any of the three is missing, this playbook is your work plan. Schedule the drill. Run it this quarter. Then schedule the next one before you leave the room.

---
*Source: AI IR Overlay newsletter, Issue #14, "Testing for Agent Failure Modes," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
