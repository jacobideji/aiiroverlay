<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 24 — Board-Ready Scorecard                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The executive-layer playbook. Translates technical IR readiness into board-level posture across four domains: Containment, Evidence, Governance, Recovery.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Playbook 24: Board-Ready Scorecard

> *Executives don't need to become AI engineers. They need clear, practical evidence that the organization can stop, verify, scope, and recover from agent-driven incidents using concrete data, not assurances.*

## Premise

Boards and executive teams haven't changed their questions about cybersecurity in twenty years: *How fast can we stop harm? What was the scope? What is the customer impact? Can our decisions withstand regulatory scrutiny? Can we recover cleanly?* AI agents change the **sources of information** that answer those questions, but they don't change the questions themselves.

The disconnect between technical and executive teams in AI incident response isn't a knowledge gap. It's a **language gap**. Technical teams monitor tool-call ledgers, retrieval-dominance alerts, and prompt-injection patterns. Executives need to know whether the answers to their five enduring questions are *yes, today, with evidence*.

This is the executive-layer playbook in the AI IR Overlay series. It runs after [Playbook 04 (Tool Design)](04-tool-design-is-containment.md), [Playbook 01 (Response)](01-agent-as-privileged-identity.md), and [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) have built the technical machinery. It converts that machinery into **a four-domain scorecard** that fits on one page, gets used quarterly, and updates the board on whether the organization is **board-ready or only documentation-ready**.

**Use this playbook when:** preparing a quarterly board update on AI risk posture, briefing a risk committee, responding to a regulator inquiry about AI incident-response capability, or self-assessing readiness before an audit. Use it during an active incident when the board needs **a concise, defensible status snapshot** rather than a technical bridge call.

**Mental Model clause engaged:** *if it can act, govern it as a privileged identity.* The scorecard makes that clause auditable at the executive level. Not as a slogan, but as four measurable capabilities the board can verify quarterly.

## First-Hour Actions

During an active incident, the board doesn't need a 60-page playbook. They need a **one-page snapshot delivered within the first hour**. The Executive Incident Snapshot template below is the deliverable.

| Minute | Action |
|---|---|
| 0–15 | Pull the agent's current scorecard from the last quarterly review. This is your **baseline**. |
| 15–30 | Mark each domain (Containment · Evidence · Governance · Recovery) as **GREEN** (holding), **AMBER** (under stress), or **RED** (failed) based on the live incident. |
| 30–45 | Capture **what the board can defensibly say** in each domain. One sentence each, derived from evidence already captured per [PB 01](01-agent-as-privileged-identity.md). |
| 45–55 | Identify the **top two risks** in plain language. No jargon. No model names. No tool stack details. |
| 55–60 | Send the Executive Incident Snapshot (template below) to the board chair, CISO, General Counsel, and Communications lead. |

**Critical:** if the snapshot relies on opinion rather than evidence captured per [Minimum Evidence Set](../evidence/minimum-evidence-set.md), the board is being asked to validate *plans*, not *capabilities*. The scorecard's quarterly discipline exists to prevent that. If you can't complete the snapshot from evidence, the **most important board update is that finding itself**.

## Containment Options

The Containment domain of the scorecard answers one question: **can the organization halt harmful agent activity in under 10 minutes without shutting down the business?**

### Containment Scorecard Items (Domain A)

| # | Question | Pass criteria |
|---|---|---|
| **A1** | Can agent actions be rapidly paused or forced into read-only mode? | M1 Read-Only activatable in ≤ 10 min by Tier-1 SOC, **tested in the last quarter** |
| **A2** | Is there an approvals mode for high-risk operations? | M2 Approvals Required pre-wired for Tier 2 tools per [Privilege Matrix](../templates/agent-privilege-matrix.csv); approval queue staffed |
| **A3** | Are emergency stoppage procedures (M4 Full Disable) tested quarterly? | Tabletop or live drill within last 90 days · time-to-disable measured, not assumed |

**Operational mapping:** these three items operationalize [Kill-Switch Modes](../kill-switches/overview.md) M1, M2, and M4 specifically. The scorecard doesn't invent new capabilities. It audits whether the existing framework's capabilities are *real* (tested in the last quarter) or *theoretical* (documented but unverified).

**Common GREEN-AMBER trap:** a GREEN rating means modes were *tested* in the last quarter under realistic conditions, not just *implemented* in code. Implementation without exercise is AMBER. Implementation without testing is RED.

## Evidence Priorities

The Evidence domain answers: **if a customer, regulator, or board member asks "what exactly happened?", can we answer with proof rather than opinion?**

### Evidence Scorecard Items (Domain B)

| # | Question | Pass criteria |
|---|---|---|
| **B1** | Are agent activity logs and retrieval traces exportable within 60 minutes? | Full [Minimum Evidence Set A–F](../evidence/minimum-evidence-set.md) exported within 60-minute SLA; tested in last quarter |
| **B2** | Is the evidence chain-of-custody maintained and auditable? | Type A and B logs stored in tamper-evident systems; access restricted and audited |
| **B3** | Can the full sequence of agent actions be reconstructed on demand? | Type B (tool-call ledger) captures **attempted** calls (not just successful); Type E (config snapshot) versioned; Type F correlates downstream SaaS audit logs |

**Operational mapping:** these items audit whether the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) is truly **operational at the 60-minute SLA**. The scorecard converts that SLA from an aspirational document into a board-verifiable capability.

**The "proof under pressure" test:** if the evidence export procedure has never been executed under timing pressure, the team has *documentation*, not *capability*. RED until exercised.

## Post-Incident Hardening

This section is where Playbook 24 differs from the other playbooks. For the scorecard, **the hardening is the quarterly cadence itself**. A scorecard that's reviewed once and filed is a documentation artifact. A scorecard that drives quarterly commitments is a governance engine.

### Governance Scorecard Items (Domain C)

| # | Question | Pass criteria |
|---|---|---|
| **C1** | Are agent permissions tiered and minimally scoped? | T0/T1/T2 per [Privilege Matrix](../templates/agent-privilege-matrix.csv); CI rejects T2 tools without `approval_required: yes` |
| **C2** | Can write targets be limited dynamically during an incident? | M3 Tool Tiering operational; CSV-filterable in seconds, not minutes |

### The Quarterly Cadence (Hardening as Governance)

| Cadence | Action | Owner |
|---|---|---|
| **Every quarter** | Run the 10-item scorecard on the **top 3–5 production agents** with privileged access | CISO + agent business owners |
| **Every quarter** | Identify the **top two gaps** per agent | CISO |
| **Every quarter** | Commit to closing **at least one gap per agent per quarter** | CISO + agent business owners + engineering |
| **Every board meeting** | Use the Executive Incident Snapshot template to update the risk committee | CISO |
| **Every annual board cycle** | Aggregate scorecards into trend lines; map to [Maturity Roadmap](../framework/03-maturity-roadmap.md) levels | CISO + Board chair |

### Scoring Guidance

For each agent, count the GAPS across the 10 scorecard items:

| Gaps | Posture | Board narrative |
|---|---|---|
| **0–3** | Strong baseline | "Containment, evidence, governance, and recovery capabilities are operational and tested." |
| **4–6** | Exposed | "We have documented procedures but unverified capabilities. Targeted remediation underway." |
| **7+** | Urgent remediation required | "The agent is operating without board-ready IR posture. Recommend pausing new privileges until baseline is achieved." |

The scoring is **deliberately blunt**. Boards don't need nuance. They need *can-we-or-can't-we*.

## Recovery Sequence

The Recovery domain answers: **after containment, can we restore service in a way that prevents recurrence and survives later regulatory review?**

### Recovery Scorecard Items (Domain D)

| # | Question | Pass criteria |
|---|---|---|
| **D1** | Is there a staged process to restore agent access post-incident? | [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) procedure documented; M5 sequence validated in last quarter |
| **D2** | Are validation steps in place to prevent recurrence before re-enablement? | Replay test per [PB 18](18-post-incident-hardening.md): *would a recurrence of the triggering prompt be contained by the controls shipped after the incident?* |

**Operational mapping:** the validation gate (D2) is the [Playbook 18](18-post-incident-hardening.md) recurrence-containment test. If the team can demonstrate that the replay test was executed and the answer was *yes*, recovery is defensible. If not, the recovery is theater.

## The Executive Incident Snapshot Template

Use this template for **active-incident board updates** and for **quarterly posture briefings**. It's intentionally short. One page, no jargon, no model names.

```text
EXECUTIVE INCIDENT SNAPSHOT: AI Agent IR Posture

Top agents in scope: [List 3–5 production agents with privileged access]

Containment readiness:
  - Time-to-read-only:        [actual, last tested DATE]
  - Approvals mode status:    [operational / unverified / not implemented]
  - M4 emergency stoppage:    [last drilled DATE; time-to-disable VALUE]

Evidence readiness:
  - 60-minute evidence export: [achieved / partial / not capable, last tested DATE]
  - Chain-of-custody:          [audited / unaudited]
  - Action sequence reconstruction: [demonstrated / not demonstrated]

Governance boundaries:
  - Tool tiering:              [T0/T1/T2 enforced / partial / absent]
  - Dynamic write-target limits: [M3 operational / theoretical]

Recovery readiness:
  - Staged re-enable procedure: [documented + drilled / documented only / undocumented]
  - Replay test pass rate:      [last 3 incidents]

Top two risks (plain language):
  1. [One sentence each]
  2. [One sentence each]

Quarterly improvements shipped (1-3 bullets):
  - [What changed; what measurable risk was reduced]

Next quarter commitments (with owners + deadlines):
  - [Specific gap close; assigned owner; date]
```

## Common Pitfalls

These are the highest-frequency failure modes when translating technical IR readiness to board-level posture.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Briefing with technical jargon** | CISO defaults to engineering vocabulary | Board can't challenge or verify; defaults to trust without evidence |
| **Confusing documentation with capability** | Implementation gets credit; testing doesn't | Scorecard shows GREEN; the actual incident shows RED |
| **Scoring on opinion, not evidence** | Quarterly review is rushed; evidence isn't attached to scores | Board signs off on a posture the organization can't demonstrate |
| **Annual review only** | "We'll roll it into the annual audit" | 12 months of drift; scorecard becomes obsolete before it's read |
| **No gap-closure commitment per quarter** | Scoring without action | Board sees the same gaps year after year; loses confidence |
| **Aggregating across agents into one score** | "Our overall AI posture is GREEN" | Hides the high-risk agent inside the company average |
| **Top-two-risks list is technical** | *"Prompt injection in the sales copilot"* | Board can't act on it; risk doesn't register at the leadership layer |
| **Quarterly improvements list is vague** | *"Improved tool design"* | Can't be audited; loses board credibility over time |
| **Scoreboard becomes "security theater"** | Posture reported optimistically to protect reputation | Incident exposes the gap; board surprise becomes board distrust |
| **No tie to risk committee agenda** | Scorecard lives in a Confluence page | Reviews skipped; capability decays without ever appearing on a meeting agenda |

## Key Metrics for Board-Ready Posture

These three metrics are the **floor** for any organization claiming board-ready AI IR posture. If the organization can't demonstrate all three with current evidence, the claim of board-readiness is aspirational, not actual.

| Metric | Target | What it proves |
|---|---|---|
| **Time-to-read-only / approvals** | < 10 minutes | The organization can halt harm without shutting down the business |
| **Time-to-minimum-evidence-export** | < 60 minutes | The organization can demonstrate scope under regulatory or board pressure |
| **Time-to-output-distribution clarity** | Demonstrable | The organization can answer "who saw the agent's output, and where did it go?" with evidence rather than guess |

The third metric is often the underprepared one. Tool-call ledgers and retrieval traces tell the story up to the agent's output. **Downstream distribution** (who received the email, who acted on the recommendation, which customer was affected) requires correlation across SaaS, CRM, communications, and analytics systems. The organization that hasn't yet rehearsed this correlation will discover the gap during an incident, not before.

## Related

Distributed as separate packages or files within the framework:

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md) (the four MVO controls this scorecard audits)
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md) (the four-clause foundation the board narrative rests on)
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md) (the scorecard's annual trend maps to maturity levels)
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md) (Modes M1, M2, M3, M4 underpin the Containment + Governance scorecard items)
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md) (A–F types underpin the Evidence scorecard items)
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml) (the inventory the scorecard runs against)
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv) (the tier discipline the Governance domain audits)
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)) (the response playbook the scorecard's Containment + Evidence domains validate)
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)) (the pre-incident discipline the Governance domain measures)
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)) (the metric framework the scorecard's four domains derive from)
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)) (the quarterly hardening cadence the scorecard governs)
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.4, GOVERN 1.6, GOVERN 3.2, MANAGE 4.2)
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports GV.OV-01, GV.OV-02, GV.RR-02, ID.IM-01, RC.CO-03)
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses governance dimensions of ASI03 Identity & Privilege Abuse and ASI09 Human-Agent Trust Exploitation)

## The Question to Carry Forward

If you do nothing else after reading this playbook, answer this one question for your most advanced production AI agent, and then answer it **for your board**, in plain language, with concrete evidence:

> *If your most advanced AI agent caused harm for 30 minutes, could you demonstrate to leadership today, using concrete evidence rather than opinion, how you would stop it, verify what occurred, define the scope, and restore operations safely?*

If yes, with evidence: the organization is **board-ready**.
If yes, with plans: the organization is **documentation-ready**. The next incident will expose the gap.
If no: the scorecard's quarterly cadence exists to close that distance, one gap at a time, over the next four quarters.

That's the test. That's the discipline. That's how AI risk stops being an abstract concern and becomes a tangible, evolving strength the board can defend.

---

*Source: AI IR Overlay newsletter, Issue #24, "Translating AI Agent Risk into Executive Clarity: A Board-Ready Scorecard for Incident Readiness," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
