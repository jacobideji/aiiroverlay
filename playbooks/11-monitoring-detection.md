<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 11: Monitoring That Truly Detects Agent Incidents            -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                  -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0. See LICENSE file in this package.                -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The detection playbook. EDR misses authorized misuse. The signal moved. Three signal families that catch what your SIEM does not.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 11: Monitoring That Truly Detects Agent Incidents

> *Endpoint Detection and Response was optimized for malware, anomalous process trees, and lateral movement. None of those exist in an AI agent incident. The signal moved. Detection has to follow it.*

## Premise

Twenty-five years of SIEM engineering taught security teams how to detect humans behaving badly. AI agents do not behave like humans. They act through valid credentials, sanctioned APIs, and authorized OAuth grants. They generate process trees the orchestrator already expected. They make lateral writes the runtime is built to make. From the endpoint's perspective, an AI agent incident looks like normal operation. From the SIEM's perspective, it looks like a service account doing the work it was provisioned to do. **The most common failure mode in AI-augmented environments is authorized misuse that traditional tools cannot flag.**

This is the detection playbook in the AI IR Overlay series. Where [Playbook 07](07-secrets-and-tokens.md) specifies the credential-event log schema and [Playbook 14](14-testing-for-agent-failure-modes.md) drills the response, this playbook closes the loop: it specifies the signals your monitoring stack must produce so that the response playbooks have something to respond to. Without it, the framework assumes someone notices something. With it, the framework specifies what to notice and how.

The signal moved from the endpoint to three places: **what the agent does** (actions), **what it consumes** (retrievals), and **what it is** (capabilities). Each of these surfaces a distinct signal family that a properly instrumented monitoring stack can detect. None of the three are routinely watched by SIEMs configured for human-actor detection. All three can be detected with the telemetry the framework's other playbooks already specify (PB07 credential-event logs, PB04 tool-call ledgers, PB03 retrieval traces).

**Mental Model clauses engaged:** *Acts* (primary). Detection is fundamentally about what the agent did, attempted, or could have done. *Retrieves* (secondary), because retrieval anomalies are the earliest signal of context poisoning. *Changes* (secondary), because detection rules are software discipline. A rule that has not been re-tuned in 90 days is decaying without telling you.

**Use this playbook when:** building the AI agent monitoring layer of an existing SOC, responding to an audit finding about missing continuous monitoring, deploying a new agent to production and wiring its first detection rules, after a near-miss incident exposed a blind spot, or when [Playbook 13 (Six Metrics)](13-six-metrics.md) Metric 2 (Containment TTA) regresses and the cause turns out to be late detection.

## What EDR misses (and what to put in its place)

Before specifying the signals, it helps to be explicit about what the legacy tooling does not catch.

| EDR was built to detect | Agent incidents actually look like |
|---|---|
| Malware execution | Tool calls via legitimate function-calling APIs |
| Anomalous process trees | Workflow orchestrator processes (Temporal, Airflow, n8n) running as expected |
| Lateral movement | Cross-system writes via authorized OAuth grants |
| Credential theft and reuse | The agent **is** the credential, used as designed |
| Unusual network egress | Standard API egress to vendor SaaS endpoints the agent normally hits |
| Privilege escalation events | The agent already has the privileges; misuse looks like use |

The detection signal moved. The next sections specify where it moved to.

## The Three Signal Families

### Family 1: Tool-Call Anomalies (action-based signals)

The agent equivalent of "command execution." The minimum signal set:

- **Sudden spikes in tool-call volume**, defined as >3 standard deviations above the 7-day rolling mean for that specific tool on that specific agent
- **First-time use of a high-risk tool**, where "high-risk" means [Privilege Matrix](../templates/agent-privilege-matrix.csv) Tier-2
- **Tool usage outside the expected business-hours window** for the agent's documented operating context
- **Repeated retries or failures**, often the visible shape of probing for a weakness
- **Bulk actions affecting many records or recipients in one execution window** (the runaway email-blast pattern)

### Family 2: Retrieval Anomalies (influence-based signals)

The RAG layer is the silent attack surface. The minimum signal set:

- **Retrieval dominance**: a single high-authority document accounts for >40% of an agent's retrieval results within a 24-hour window
- **Repeated retrievals of recently edited documents**, indicating that a freshly modified knowledge source is dominating context
- **Retrievals from novel or unexpected corpus sources** the agent has not historically used
- **High-frequency access to sensitive data repositories** the agent's business need does not require

[Playbook 03 (RAG / Knowledge-Base Forensics)](03-rag-knowledge-base-forensics.md) consumes these signals as the trigger for its 90-minute Freeze-the-World sequence.

### Family 3: Identity and Grant Anomalies (capability-based signals)

The agent's risk profile shifts the instant its permissions change. This signal family directly consumes the credential-event log schema specified in [Playbook 07: Secrets and Tokens](07-secrets-and-tokens.md). The minimum signal set:

- **Scope expansions** on any agent identity, especially mid-incident
- **New OAuth grants issued** to the agent's principal
- **New tool integrations added** to the AI-BOM `tools` section
- **Modifications to allowlists or approval policies** in the [Privilege Matrix](../templates/agent-privilege-matrix.csv)
- **Creation of new service identities** for agent use
- **Refresh-token issuance velocity changes**, which often precede credential abuse

Together these three families produce **fifteen baseline signals**. Most AI deployments today watch zero of them.

## First-Hour Actions

You do not need a full SIEM rewrite to begin. The first hour is about producing one credible detection rule, validated against historical telemetry, on one agent, and wiring it to a containment action.

### The 60-minute first-rule drill

| Minute | Action | Owner |
|---|---|---|
| 0–10 | Pick **one** production AI agent with Tier-2 tool access. Pull its [AI-BOM](../templates/ai-bom.yaml). Identify the single tool with the highest business impact if misused. | Detection engineer |
| 10–25 | Pick **one** signal from the three families above for that tool. Tool-call volume spike is the easiest to start with. Pull 7 days of historical tool-call telemetry. Compute the mean and standard deviation. Set the alert threshold at mean + 3σ. | Detection engineer |
| 25–40 | **Dry-run the rule against the last 30 days of telemetry.** Record how many times the rule would have fired. Investigate every hit. If the rule would have fired more than once per week without a real incident, the threshold is too low or the signal is wrong. Re-tune. | Detection engineer + agent owner |
| 40–50 | **Wire the rule to an automated containment action.** A volume-spike rule that does not trip the agent into [Mode M2 Approvals](../kill-switches/overview.md) or [Mode M1 Read-Only](../kill-switches/overview.md) within 60 seconds of firing is a notification, not a control. | SOC tooling lead |
| 50–55 | **Document the rule** in the AI-BOM `guardrails` section: signal source, threshold, fire-to-containment latency, owner, last calibration date. | Detection engineer |
| 55–60 | **Schedule the rule's first calibration review** for 30 days from today. Pre-commit the date. A detection rule that has not been re-calibrated in 90 days is decaying. | Detection engineer + Incident Commander |

That is the entire first hour. One agent. One signal. One automated containment wire. One calibration review on the calendar. Do **not** scale to additional rules until the first one has been calibrated at least once. Most teams fail by stacking rules before they tune the first one.

## Containment Options

Detection without automatic containment is a notification. The framework requires every detection rule to be wired to a containment action. The mapping uses the framework's standard six-mode ladder.

### Detection trigger to Kill-Switch Mode mapping

| Detection signal | Kill-Switch Mode triggered | Latency requirement |
|---|---|---|
| Tool-call volume spike (3σ above 7-day mean) on a Tier-2 tool | **M2 Approvals Required** | < 60 seconds |
| First-time use of a Tier-2 tool by an agent | **M2 Approvals Required** | < 60 seconds |
| Retrieval dominance (>40% from single document over 24h) | **M1 Read-Only** | < 60 seconds |
| Retrieval from novel corpus source | **M1 Read-Only** plus alert | < 60 seconds |
| New OAuth grant issued to agent principal | **M3 Tool Tiering** (disable affected scope class) | < 60 seconds |
| Scope expansion on agent identity outside approved change window | **M4 Full Disable**, requires [Playbook 07](07-secrets-and-tokens.md) snapshot-before-revocation sequence | < 60 seconds, snapshot before any rotation |
| Multiple signals fire simultaneously across two or more families | **M4 Full Disable**, immediate Incident Commander page | < 60 seconds |
| Single signal fires but business impact is unverified | **M2 Approvals Required**, page Tier-1 SOC | < 60 seconds |

> **The 60-second containment rule:** every signal that fires must produce a containment action within 60 seconds. Not a Slack message. Not an email. A mode change at the agent layer. If the latency is longer than 60 seconds, the rule is theatrical, not operational. This is the credential-discipline equivalent of [Playbook 14](14-testing-for-agent-failure-modes.md)'s "tabletop theater" pitfall applied to monitoring.

### When detection alone is the right answer

Some signals warrant observation rather than containment. These are detection-only by design and feed forensics rather than containment:

- Identity-attribution gaps in tool-call logs (a logging defect, not an attack)
- Refresh-token velocity changes within expected ranges
- Retrieval frequency changes during known business events (quarterly close, product launch)

Catalog these in the AI-BOM as detection-only rules with the rationale recorded. The catalog itself is auditable evidence that you did not silently downgrade containment.

## Evidence Priorities

For monitoring-driven incidents, **the detection event itself is the earliest piece of evidence**. Every detection rule that fires must persist its full context, not just the alert payload.

| Code | Evidence Type | Priority for monitoring incidents | What detection contributes |
|---|---|---|---|
| **B** | Tool-Call Ledger | **Critical** | The spike or anomaly itself. The baseline window for comparison. The denied calls (probing). |
| **C** | Retrieval Traces | **Critical** for any influence-family signal | Document IDs, retrieval scores, corpus versions at detection time. |
| **F** | Identity and SaaS Audit-Log Correlation | **Critical** for any capability-family signal | Grant history, OAuth consent log, identity provisioning log at detection time. |
| **E** | Configuration Snapshot | **Critical** for all monitoring incidents | The detection rule itself: threshold, signal source, calibration date, fire-to-containment latency. Without this, you cannot later defend why the rule fired or did not fire. |
| **A** | Prompt and Response Record | High if the signal coincides with a prompt-injection vector | Prompt logs at detection time correlate the action signal back to its origin. |
| **D** | Memory Snapshot | High if memory is `scope: shared` and a capability anomaly fires | A shared memory poisoning often precedes scope abuse. |

**Operational requirement:** the detection rule's payload, the agent's state at detection time, and the containment action taken must be exportable as a single artifact within **10 minutes** of the alert firing. This export is the earliest piece of the A–F evidence set and must be preserved alongside the later captures.

### Credential-event log expectations

The credential-event log schema specified by [Playbook 07](07-secrets-and-tokens.md) is the upstream contract this playbook depends on:

```
agent_id, principal, event_type, prior_scopes, new_scopes,
timestamp, actor, justification, ticket_id
```

If this log is not emitting, Family 3 (capability-based signals) cannot be detected. PB11 cannot ship in a meaningful operational way until PB07's hardening section's identity-attribution requirement is met. The two playbooks are an upstream-downstream pair.

## Recovery Sequence

For monitoring incidents, recovery means returning the agent to operation **and** validating the detection rule itself. Detection rules are software. They regress.

1. **Validate the detection rule fired correctly.** Was this a true positive? The post-incident triage answers three questions: did the signal fire, did the containment action execute within 60 seconds, did the human triage path see the alert with sufficient context.
2. **Re-tune thresholds based on the incident.** False positives waste capacity. Missed signals cost everything. Document the threshold change and the rationale. Update the AI-BOM `guardrails` section.
3. **Add a new signal if the incident revealed a blind spot.** A real incident is the cheapest detection-engineering input you will get. Mine it.
4. **Re-enable the agent in [Mode M1 Read-Only](../kill-switches/overview.md)** under tightened monitoring thresholds for the first 14 days post-incident. Lower the alert threshold to mean + 2σ for that period. Return to 3σ only after 14 days of clean operation.
5. **Tabletop the same scenario within 30 days** per [Playbook 14](14-testing-for-agent-failure-modes.md). Confirm the new or re-tuned rule still fires and the containment action still executes within 60 seconds.
6. **Update the [Maturity Roadmap](20-maturity-roadmap.md) Level claim** for the affected agent if necessary. A monitoring gap exposed during a real incident is a regression event. Acknowledge it on the next Board Scorecard cycle.

**Approver for re-enablement:** CISO or designated Incident Commander. The detection engineer who tuned the rule is **not** sufficient. Implementation bias is the same risk PB07 warns about for credential rotation.

## Post-Incident Hardening

Monitoring discipline becomes a hardening program when four boundaries each have their own ownership and cadence.

### Boundary 1: Signal sources

- **Every signal family has at least one rule live in production.** Action, Influence, Capability. If any family is empty, the agent is missing a detection dimension.
- **Every Tier-2 tool has a baseline established and a volume-spike rule wired** within the first quarter of the agent's production deployment. Quarterly rollout cadence: one Tier-2 tool's baseline per month.
- **Credential-event log is consumed.** Identity attribution is in tool-call logs. Family 3 signals can fire. The PB07 contract is honored.

### Boundary 2: Rule logic

- **Thresholds are calibrated against historical telemetry**, not vendor defaults. A vendor-default threshold is a wish.
- **Rules are reviewed quarterly.** A rule older than 90 days without re-tuning is decaying.
- **False-positive feedback loop is documented.** When the SOC dismisses an alert, the dismissal reason updates the rule's calibration data.

### Boundary 3: Latency and routing

- **Detection-to-containment latency is < 60 seconds.** Measured. Not promised. Track per rule.
- **Alerts route to a paging system, not an inbox.** PagerDuty, Slack incident channel with auto-page, or the SOC's primary alert tool. Email-only routing is the framework's "alerts without a stop button" pitfall.
- **The Incident Commander gets the same alert the SOC analyst gets.** No layered escalation chain for high-severity signals. The IC owns the response from minute zero.

### Boundary 4: Procedure

- **Detection drills run quarterly** alongside the [Playbook 14](14-testing-for-agent-failure-modes.md) Kill-Switch drills. Confirm rules fire, latency holds, containment executes.
- **The 5-business-day hardening SLA** from [Playbook 18](18-post-incident-hardening.md) applies to monitoring gaps exposed in real incidents.

## Common Pitfalls

These are the highest-frequency failure modes specific to AI agent monitoring. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Relying on EDR for agent visibility** | "We have a SIEM. We're covered." | Authorized misuse is invisible until external impact (a customer complaint, a SaaS audit log review, a regulator notice). |
| **Alerts without automatic containment** | The detection engineer ships the rule. The containment wiring is "next sprint." | Agent keeps acting during the 5-to-15-minute human triage window. Five-minute incidents become hour-long incidents. |
| **Static thresholds** | The rule was tuned once at deployment. | Agent behavior evolves. Rules go stale silently. The first signal that the rule is decayed is missing the next real incident. |
| **No baseline before deploying the rule** | "We need monitoring now. We can tune later." | Cannot distinguish "spike" from "Tuesday morning." Either alert floods or detection silence. |
| **Monitoring tool calls but not identity events** | The credential-event log (PB07) is not wired into the detection pipeline. | Capability-family signals never fire. The most dangerous attack class (scope expansion) is invisible. |
| **Per-agent rules instead of per-tool rules** | The agent is the entity. The tool is a detail. | When an agent is reconfigured (new tool added, scope expanded), every rule has to be re-tuned. Per-tool rules survive agent changes. |
| **Detection rules not in version control** | The SIEM has its own UI. Why source-control it. | A drifted rule is silent until incident. Version control with the AI-BOM is the only audit-defensible record. |
| **Alert fatigue from over-tuned action-family signals** | First-week false positives are not investigated; the SOC starts dismissing all alerts on the agent. | Real incident gets dismissed. The "we have monitoring" claim turns into "we ignore monitoring." |
| **Latency measured at the SIEM, not at the containment action** | The SIEM fires in 5 seconds; the containment runbook takes 12 minutes. | The framework's < 60-second rule is met on paper, violated in practice. Measure end-to-end. |
| **One detection engineer owns all the rules** | Specialist hire. Specialist responsibility. | When that engineer leaves or rotates, every rule becomes orphaned. Distribute ownership per agent or per tool. |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 Inventory drives signal coverage; MVO-3 Evidence Set is what detection events become.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clauses 1, 3, and 4 (Acts, Retrieves, Changes) shape the three signal families.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Level 4 (Resilient) requires monitoring trend lines, not just rule presence.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The modes detection triggers into. The 60-second latency requirement is enforced here.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). Detection events are Type B precursors and Type E artifacts.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The `guardrails` and `logging` sections document the rules and their calibration.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). Tier-2 tools are the priority targets for the first detection rule on every agent.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The response playbook detection events trigger.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). Retrieval-family signals are PB03's triggering events.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The tier discipline that prioritizes which tools get baselines first.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). The credential-event log schema this playbook consumes. Upstream contract.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). Metric 2 (Containment TTA) regression is often a detection-latency problem.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The drill discipline that validates detection rules fire and contain within 60 seconds.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA that monitoring-gap closures inherit.
- **Playbook 20: Maturity Roadmap (Operating View)** ([`playbooks/20-maturity-roadmap.md`](20-maturity-roadmap.md)). Monitoring discipline freshness drives the Level 3 to Level 4 transition.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MEASURE 2.7, MEASURE 4.2, MANAGE 4.1).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports DE.CM-01, DE.CM-09, DE.AE-02, DE.AE-03, DE.AE-06, RS.MA-02).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the direct operational response for ASI06 Memory & Context Poisoning detection, ASI08 Cascading Agent Failures early detection, and ASI10 Rogue Agent drift detection).

## The Question to Carry Forward

If your most privileged AI agent's behavior changed at 3 AM on a Saturday, would your SIEM tell you, would the alert reach the on-call engineer with enough context to triage in under 10 minutes, and would the agent already be in [Mode M1 Read-Only](../kill-switches/overview.md) by the time the engineer answered the page? Answer the question for the one agent that scares you most. The answer reveals whether the framework's monitoring discipline is real or aspirational.

If the answer is no to any of the three, PB11 is the work plan. Pick one signal from one family. Tune it against 30 days of telemetry. Wire it to an automated containment action with a 60-second latency budget. Drill it within 30 days. Then move to the next signal.

That is how monitoring moves from documented to demonstrated. One agent, one signal, one wired containment, on a cadence that holds.

---

*Source: AI IR Overlay newsletter, Issue #11, "Monitoring That Truly Detects Agent Incidents," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
