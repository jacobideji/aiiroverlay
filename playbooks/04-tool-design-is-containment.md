<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 04 — Tool Design Is Containment                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The pre-incident playbook. Design your tool layer before you need it — because in production, the tool layer IS your containment boundary.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Playbook 04 — Tool Design Is Containment

> *Safe prompts help the agent behave. Safe tools prevent irreversible impact. In an agent-powered system, the tool layer is not plumbing — it is the containment boundary.*

## Premise

Most AI agent incidents are not the result of compromise in the traditional sense. They are the result of an agent executing **the wrong sequence of perfectly valid actions, at machine speed, simply because those actions were available**. Emailing the wrong customer list. Updating the wrong vendor record. Closing the wrong tickets. Pushing changes to the wrong repo. Opening the wrong firewall rule.

Each of those actions can be performed by an authorized service identity, logged as a legitimate API call, and pass every endpoint-security check you have. Prompt guardrails do not stop them. Model retraining does not stop them. Only one thing stops them — **the absence of the tool that performs the action, or the gating around it**.

This is the foundational pre-incident playbook in the AI IR Overlay series. Where Playbook 01 covers what to do when an incident is happening, Playbook 04 covers **the work that determines whether the response in Playbook 01 will be surgical or catastrophic**. The single most leveraged decision in AI IR is *not made under pressure during an incident*. It is made on a quiet Tuesday when you decide which tools your agent can call, with what scope, with what controls.

**Mental Model clause engaged:** *if it can act, govern it as a privileged identity.* The tool list IS the agent's privilege grant. Review it in your PAM cadence.

**Use this playbook when:** you are designing a new agent for production, reviewing an existing agent before its next deployment, building an [Agent Privilege Matrix](../templates/agent-privilege-matrix.csv) for the first time, or operationalizing M3 Tool Tiering in your [Kill-Switch Modes](../kill-switches/overview.md) runbook.

## First-Hour Actions

If you start this work today, the highest-leverage first hour is **not** a full tool audit. It is a single-question scoping exercise on your highest-risk production agent.

**The 60-minute drill:**

| Minute | Action |
|---|---|
| 0–10 | Pick **one** production agent. Pull its current tool list — by enumeration, not memory. |
| 10–25 | For each tool, ask: *if this tool ran with the wrong parameters for 10 minutes, what is the worst defensible outcome?* Record the answer in plain English. |
| 25–35 | Sort the tools into Tier 0 / Tier 1 / Tier 2 (definitions below). If you cannot decide between T1 and T2, default to T2. |
| 35–45 | Identify the **single most dangerous tool** the agent can call. (For most teams, it is *send external email*, *write to ERP*, *deploy code*, or *change cloud config*.) |
| 45–60 | Pick **one** control to add to that tool **this week**: an allowlist, a cap, an approval gate, or a draft/preview layer. One tool. One upgrade. Measurable risk reduction. |

That is the first-hour version of this playbook. Do it for one agent, ship the upgrade, and move to the next. Tool design is a **practice**, not a project.

## Containment Options

Tool design directly enables [Kill-Switch Mode M3 (Tool Tiering)](../kill-switches/overview.md). Without pre-tiered tools, M3 is not a real mode — it is a theoretical option that cannot be executed in 10 minutes under pressure.

### The Tool-Tiering Model

The single most important deliverable of this playbook is a tiered view of every tool your agent can call. The model:

| Tier | Risk class | Examples | Default control |
|---|---|---|---|
| **T0** | Read-only, low risk | Search KB · summarize ticket · read policy · retrieve status · query records | Allowed by default |
| **T1** | Bounded writes, moderate risk | Draft (do not send) email · update internal ticket fields · create tasks · soft-delete | Allowed + caps + allowlists |
| **T2** | Systems of record, high risk | Send external email · update CRM/ERP · push code · change cloud config · perform financial / security / identity actions | Approvals required (or disabled until explicitly needed) |

Capture this in the [Agent Privilege Matrix template](../templates/agent-privilege-matrix.csv). The `risk_tier` column is the operational handle for M3 containment: when an incident requires Tool Tiering, you filter the CSV by tier and disable T2 in seconds.

### The Five Controls (apply per-tool)

Every tool in your matrix should be evaluated against five control dimensions:

1. **Control what can be done** — split read vs. write. No `do-everything` endpoints. Tier the result.
2. **Control where it can be done** — allowlists for domains, tenants, repos, record types. Restrict write scope to narrow objects and fields.
3. **Control how much can be done** — caps per agent run (records, emails, updates). Rate limits and burst controls.
4. **Control irreversibility** — prefer `draft` over `send`. Diff previews before applying. Undo paths (revert logs, soft deletes, staging-first).
5. **Control accountability** — log tool calls with parameters AND results. Capture approver identity and rationale for Tier 2 actions. Maintain an incident decision log.

A tool that passes all five is **agent-safe**. A tool that fails any of them is a future incident waiting for the right (wrong) sequence of valid actions.

## Evidence Priorities

Good tool design is not just preventive — it is **evidentiary**. The five controls above directly shape what the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) can prove during an incident.

| Tool-design control | Evidence type strengthened | Why |
|---|---|---|
| Log tool calls with parameters + results | **Type B (Tool-Call Ledger)** | The ledger is only as good as the logging; tool-call observability is a tool-design choice |
| Capture approver identity + rationale (T2) | **Type B + Type F** | Approver records correlate with SaaS audit logs; both become defensible records |
| Diff previews before apply | **Type B** | The diff is the proof of *what was about to happen* — critical for proving harm avoided |
| Allowlists | **Type B + Type F** | Denied attempts show up in the ledger and downstream logs as **evidence of intent** |
| Caps per run | **Type B** | Cap-triggered halts are evidence the control held |

A tool that emits structured logs with parameters, results, approver identity, and outcome is a tool that survives forensic review. A tool that emits only `success / failure` is a tool that destroys evidence by omission.

**Operational requirement:** every Tier 2 tool must produce structured logs sufficient to reconstruct *who approved, when, with what parameters, with what result* — within the [60-minute evidence export window](../evidence/minimum-evidence-set.md).

## Recovery Sequence

Tool design also shapes **recovery speed**. The [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) sequence depends on incremental tool re-enablement; without tiering, you can only re-enable everything at once — and that is the most common recovery failure.

After containment, recovery proceeds in tier order:

1. **Re-enable T0 (read-only) first.** The agent functions; business workflows that depend on retrieval and lookup resume.
2. **Verify logging and policy enforcement.** Confirm that the tools you re-enabled are emitting the structured logs your evidence set requires.
3. **Re-enable T1 (bounded writes) with caps tightened.** Lower the per-run cap to half its pre-incident value for the first 24–72 hours. Monitor.
4. **Re-enable T2 (systems of record) one tool at a time, with approvals.** Do not batch-enable T2. Each one is a separate decision with a separate approver and a separate monitoring window.
5. **Return to baseline caps.** Only after monitoring thresholds confirm normal behavior over a documented observation window.

If your tools are not pre-tiered, this sequence collapses into a single binary decision — and the cost of getting it wrong is re-triggering the original incident.

## Post-Incident Hardening

After an incident, tool design is where the **lessons get written into the codebase**, not into the runbook. A runbook entry that says *"be more careful with the email tool"* will be ignored. A code change that splits the email tool into `draft` and `send` cannot be ignored — the agent literally cannot send anymore without going through the new gate.

The hardening checklist:

| Action | Outcome |
|---|---|
| Add the implicated tool to the Privilege Matrix if missing | Closes the inventory gap |
| Promote the tool's tier if its blast radius was underestimated | Tightens future containment |
| Split the tool if it was a "god tool" (multi-verb or multi-object) | Narrows future blast radius |
| Add an allowlist if the wrong target was reached | Prevents the same scope error |
| Add a cap if a runaway happened | Bounds future runaway |
| Add a diff preview if the action was irreversible | Creates an undo path |
| Add structured logging if the evidence was insufficient | Strengthens future Type B captures |
| Update the AI-BOM `tools` section with the new control | Future responders see the new state |
| Schedule a tabletop within 30 days using the same scenario | Verifies the hardening holds |

This is what *"transforming lessons learned into guardrails"* looks like in tool-layer terms.

## Common Pitfalls

These are the highest-frequency failure modes in tool design. Each one quietly converts an agent from *helpful* to *blast-radius-on-tap*.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **God Tools** ("update CRM", "manage email", "admin cloud") | Convenience during prototyping; copy-pasted from vendor docs | Unlimited action surface — one wrong instruction becomes many wrong actions at machine speed |
| **No read/write split** | The vendor SDK exposes both in one client; engineers don't separate | Cannot enable T0 without enabling T2; M3 (Tool Tiering) becomes binary |
| **Tier 2 defaulted to no-approval** | Approval workflow not built; deferred to "later" | Approval gate exists only on paper; an incident reveals it was never enforced |
| **Allowlist as policy comment, not code** | Allowlist documented in the system prompt instead of enforced in the tool wrapper | Prompt injection bypasses it; allowlist provides false assurance |
| **No diff preview on irreversible writes** | "We'll add it next sprint" | Recovery from a wrong write becomes manual replay across logs |
| **Cap counts requests, not blast radius** | Cap = "200 calls per run"; one call updates 10,000 records | Cap held; harm still occurred |
| **Logging captures success only** | "Success" branch was instrumented; failures and denials are silent | Type B evidence missing the most important rows (denied attempts = attacker intent) |
| **Tools not in the AI-BOM inventory** | Engineering shipped the tool without updating the manifest | Incident commander does not know the tool exists; cannot scope blast radius |
| **Tier 2 tools without an `approver` identity contract** | Approval is "checked" but not recorded with who, when, why | F (downstream audit) cannot correlate approval with action |
| **Re-using one tool definition across multiple agents with different risk profiles** | DRY engineering reflex | A T1 tool for Agent A is a T2 tool for Agent B; matrix conflicts go unresolved |

## Related

Distributed as separate packages or files within the framework:

- **Agent Privilege Matrix template** — [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv) (the artifact this playbook operationalizes)
- **Privilege Matrix README** — [`templates/README-privilege-matrix.md`](../templates/README-privilege-matrix.md) (column-by-column explanation of the matrix)
- **AI-BOM template** — [`templates/ai-bom.yaml`](../templates/ai-bom.yaml) (the `tools` section is the source of truth for the matrix)
- **The Minimum Viable Overlay** — [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md) (MVO-1 Inventory + MVO-2 Safe Modes both depend on tool-design discipline)
- **The Mental Model** — [`framework/02-mental-model.md`](../framework/02-mental-model.md) (clauses 1 and 4: *if it can act, govern it as a privileged identity* and *if it can change, manage it as software*)
- **Kill-Switch Modes** — [`kill-switches/overview.md`](../kill-switches/overview.md) (M3 Tool Tiering is the mode this playbook prepares you to execute)
- **Minimum Evidence Set** — [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md) (Type B Tool-Call Ledger is shaped by tool-design choices)
- **Playbook 01 — The Agent Is a Privileged Identity** — [`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md) (the response playbook this one prepares you for)
- **NIST AI RMF crosswalk** — [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MAP 4.1, MANAGE 1.3, MANAGE 2.4)
- **NIST CSF 2.0 crosswalk** — [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports ID.AM-05, PR.AA-05, RS.MI-01)
- **OWASP Agentic Top 10 crosswalk** — [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook responds primarily to ASI02 Tool Misuse & Exploitation, ASI03 Identity & Privilege Abuse, ASI05 Unexpected Code Execution)

## The Question to Carry Forward

If you do nothing else after reading this playbook, answer this one question for your highest-risk production agent:

> *If your agent made the wrong decision for 10 minutes, which tool would do the most damage — and what control stands between the agent and that tool right now?*

If you cannot name the tool, you have an **inventory gap** ([MVO-1](../framework/01-minimum-viable-overlay.md)).
If you can name the tool but not the control, you have a **tool-design gap** (this playbook).
If you can name both but the control is unenforced, you have an **enforcement gap** (the next code change).

Pick the gap with the smallest cost-to-close. Close it this week. Move to the next agent.

That is how the tool layer becomes the containment boundary it should already be.

---

*Source: AI IR Overlay newsletter, Issue #4 — "Tool Design Is Containment," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
