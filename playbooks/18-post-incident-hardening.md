<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 18 — Post-Incident Hardening                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The closure playbook. Every incident produces lessons. This playbook turns those lessons into permanent guardrails within five business days.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 18: Post-Incident Hardening

> *Good post-incident hardening doesn't slow the business. It prevents the repeat failure that would. The measure is simple: would a recurrence of the triggering prompt be contained by the controls you shipped after the incident?*

## Premise

Post-incident analysis is routine in cybersecurity and IT, but AI incidents bring a particular failure mode. Most organizations close them out with **prompt updates, user reminders, or vendor notifications**. These interventions feel decisive in the moment, but they address symptoms rather than systemic risk. Prompts get rewritten. The next prompt-injection variant bypasses the rewrite. The same incident recurs three months later with a slightly different vector.

This playbook is the **closure playbook** for the AI IR Overlay series. It runs after [Playbook 01 (response)](01-agent-as-privileged-identity.md) has contained an incident and after the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) has been captured. Its purpose is to convert the lessons of that incident into **structural controls**. Not commentary in the post-mortem document, but enforced code, configuration, and policy changes that hold up under future pressure.

The discipline that makes this work is the **five-business-day post-incident hardening SLA**. Every incident must produce at least one meaningful, tested control improvement within five business days of closure, supported by pre-incident and post-incident metric data showing the change reduced risk. No exceptions. The SLA is enforced by the CISO or designated Incident Commander, not by the agent owner.

**Use this playbook when:** an incident has reached M5 Controlled Re-Enable, the [Six Triage Questions](../triage/six-questions.md) have been answered and logged, the A–F evidence set has been captured, and the team is moving from response into closure.

**Mental Model clause engaged:** *if it can change, manage it as software, with rollback and auditability.* Hardening changes are software deployments. They get versioned, reviewed, deployed, and monitored. Not added as bullet points to a runbook nobody reads.

## First-Hour Actions

Hardening starts within one hour of incident closure, not weeks later. The first hour is about **scoping the fix list**, not building it.

| Minute | Action |
|---|---|
| 0–10 | Open a clean **Fix List** document. Reference the [decision log](01-agent-as-privileged-identity.md) and the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) capture. |
| 10–25 | List every candidate control discovered during the incident. Include ones that *would not* have prevented this incident but *should* exist anyway. Do not filter yet. |
| 25–40 | For each candidate, classify by impact: **(B)** reduces blast radius · **(E)** improves evidence · **(R)** prevents recurrence · **(V)** validates recovery. |
| 40–50 | Select **3 to 5 high-impact controls** for immediate implementation. The rest go into a backlog reviewed quarterly with the [Maturity Roadmap](../framework/03-maturity-roadmap.md). |
| 50–60 | Assign **owner + deadline + acceptance criteria** for each of the 3–5 selected controls. Deadline = **5 business days** from incident closure. |

That's the entire first hour. The fix list at the end of it should fit on one page. If it doesn't, you're confusing *hardening priorities* with a *backlog grooming session*. Separate the two.

**Critical:** every selected control must be **measurable**. *"Tighten the email tool"* isn't a hardening control. It's a wish. *"Convert email tool from `send` to `draft` for any external recipient; CI rejects calls to `send.external` without two-person approval"* is a hardening control. Specificity is what makes the 5-day SLA enforceable.

**Materiality verification:** before the Fix List ships, the Incident Commander confirms the [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) determination was captured in the decision log. If the determination is missing, incomplete, or undocumented, hardening is **paused** until General Counsel re-convenes and the determination is documented. The 5-business-day SLA does not run if the materiality record is incomplete.

## Containment Options

Hardening's containment value is **preventive**. It makes the next incident's [Kill-Switch Modes](../kill-switches/overview.md) faster, more surgical, and more reliable. Without hardening, every incident requires the same heroics. With disciplined hardening, the same scenario class becomes a routine M3 (Tool Tiering) operation instead of an M4 (Full Disable).

The hardening dividend per Kill-Switch Mode:

| Kill-Switch Mode | Hardening that makes it faster next time |
|---|---|
| **M1 Read-Only** | Pre-defined `read_write` flag on every tool ([Privilege Matrix](../templates/agent-privilege-matrix.csv)). M1 becomes a config flip, not a code change. |
| **M2 Approvals Required** | Approval-gate infrastructure already wired for Tier 2 tools. M2 becomes enabling a flag, not building a workflow under pressure. |
| **M3 Tool Tiering** | Every tool already tiered per [Playbook 04](04-tool-design-is-containment.md). M3 becomes a CSV filter, not a forensic exercise. |
| **M4 Full Disable** | Snapshot procedures rehearsed in micro drills. M4 captures evidence in <10 min instead of <60. |
| **M5 Controlled Re-Enable** | Tier-ordered re-enablement runbook validated post-incident. M5 follows a checklist, not a debate. |

**The asymmetry to internalize:** hardening done badly costs hours of meeting time and produces a Confluence page. Hardening done well costs the same hours and produces a code-enforced control that makes the next incident shorter, cheaper, and more defensible.

## Evidence Priorities

Hardening shapes evidence in two directions. It **improves the captures** the next incident will produce, and it **closes the gaps** the current incident exposed.

For each evidence type in the [Minimum Evidence Set](../evidence/minimum-evidence-set.md), evaluate whether the just-closed incident's capture met the 60-minute SLA. Where it didn't, ship a hardening fix:

| Evidence Type | If it failed to capture, ship this hardening |
|---|---|
| **A** Prompt / Response Record | Extend model-provider log TTL or pull logs to an internal store with ≥90-day retention |
| **B** Tool-Call Ledger | Instrument *attempted* calls (not just successful); structured logging with parameters AND results |
| **C** Retrieval Traces | Add corpus-version + document-ID logging to RAG framework; expose query traces |
| **D** Memory Snapshot | Implement memory-export endpoint; document the export procedure in the runbook |
| **E** Configuration Snapshot | Move prompt + policy + retriever config under version control with diff history |
| **F** Identity + SaaS Audit Correlation | Document the audit-log pull procedure per target system; pre-approve emergency access |

**Operational requirement (post-hardening):** the next incident's evidence export must complete within **45 minutes**. That's 25% faster than the framework's 60-minute baseline. The hardening dividend is measurable speedup, not just better documentation.

### Retrieval-specific hardening (often the gap that surprises)

The retrieval layer is the most under-hardened part of most AI deployments. Specific hardening items:

- **Retrieval-dominance alert:** trigger when a single document accounts for >40% of an agent's retrieval results within a 24-hour window. High-authority documents are the highest-leverage poisoning vectors.
- **Sensitive corpora isolation by role:** policy documents, security playbooks, and financial procedures should never be retrieved by agents whose business purpose doesn't require them.
- **Treat the knowledge base as production infrastructure.** Corpus updates are change-control events, tracked in CMDB, with rollback paths.

## Recovery Sequence

Hardening isn't a separate phase from recovery. It's the **validation gate** between Mode M5 and the return to M0 Observe. An agent that re-enters production without hardening hasn't actually completed recovery. It has only resumed operations under the same conditions that produced the incident.

The recovery sequence with hardening built in:

1. **Re-enable in Read-Only (M1).** Confirm the agent functions, logs flow.
2. **Validate retrieval and tool policies.** Then deploy the first hardening fix (typically a Tier 2 tool downgrade or allowlist tightening).
3. **Replay the incident scenario in a safe harness.** Verify the new hardening control would have prevented it. **If it wouldn't, the hardening is insufficient.**
4. **Re-enable tools incrementally.** Monitor the new hardening control under live traffic for the first 24–72 hours.
5. **Return to M0 Observe.** Only after the hardening control has been live, monitored, and demonstrated to hold across the post-incident observation window.

The replay step (3) is the hardening **acceptance test**. If a recurrence of the triggering prompt wouldn't be contained by the new control, the recovery isn't complete. Go back to the fix list.

## Post-Incident Hardening

This is the playbook's core section, organized as the **Tiered Hardening Framework**. Four boundary categories that together cover the full surface where AI incidents originate.

### Boundary 1: Tool Controls (Containment)

The single most leveraged hardening category. Operationalizes [Playbook 04 (Tool Design Is Containment)](04-tool-design-is-containment.md):

- **Tier tools by criticality.** T0 (read-only) · T1 (bounded writes) · T2 (systems of record). Capture in the [Agent Privilege Matrix](../templates/agent-privilege-matrix.csv).
- **Require approvals for Tier 2 operations.** And *log the approver identity + rationale*.
- **Enforce allowlists.** Domains, tenants, repos, record types, user groups. **Enforcement lives in the tool wrapper, not the system prompt.**
- **Implement operational caps.** Maximum recipients, maximum record updates, rate limits, burst controls.
- **Ensure reversibility.** `draft` instead of `send`, staging instead of production, soft-delete instead of hard-delete, diff preview before apply.

### Boundary 2: Retrieval Controls (Provenance)

The under-hardened boundary in most deployments:

- **Retrieval-dominance alerting.** Alert when a single high-authority document dominates retrieval results.
- **Sensitive corpora isolation by user role.** Agents only retrieve from corpora their business purpose requires.
- **Corpus change control.** Corpus updates are versioned, tracked in CMDB, with rollback paths.
- **KB-as-production.** Apply production change-management discipline to the knowledge base itself.

### Boundary 3: Evidence Controls (Provability)

What turns the next incident into a defensible chronology rather than a guess:

- **Tool-call logs record parameters AND results.** Every call, including failures and denials.
- **Retrieval traces capture document ID + version** at retrieval time.
- **Configuration snapshots are versioned.** Prompts, tool definitions, policies, retriever settings.
- **Evidence access is restricted and audited.** Who looked at what, when.
- **Export procedures are tested regularly.** The first time you discover your export procedure has friction shouldn't be during an active incident.

### Boundary 4: Human Controls (Training and Communication)

The boundary that determines whether the technical controls actually get exercised:

- **Micro drills measure Time-to-Safe-Mode (TTSM) and Time-to-Evidence (TTE).** Quarterly per agent, results trended.
- **Standardized messaging templates.** Internal, customer, regulator. Templates approved in advance, not drafted under pressure.
- **Disciplined decision logging.** Every decision during an incident gets logged with timestamp, decider, and rationale. Templates make this mechanical.

### What does NOT count as hardening

A short list of common closure activities that do **not** qualify as hardening under this playbook:

- Updating the system prompt without an enforced policy backing it
- Sending an internal email reminder about safe use
- Filing a vendor ticket and waiting for their response
- Adding language to the system prompt that the agent might ignore
- Holding a tabletop without measurable acceptance criteria

These can be useful in their own right, but they're **not the 5-day SLA deliverable**. The SLA deliverable is a code, config, or policy change with measurable risk reduction.

## Common Pitfalls

These are the highest-frequency failure modes when post-incident hardening goes wrong.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Quick-fix dependence** | Time pressure; closure happens before the fix list is built | Same incident recurs in 3–6 months with a slight variant |
| **Prompt-only changes** | Prompt is the easiest surface to change; nobody has to coordinate with engineering | Next prompt injection bypasses the rewrite; risk unchanged |
| **No 5-day SLA** | "We'll get to it next sprint" | Hardening backlog grows; lesson loses urgency; pattern repeats |
| **Owner is the agent owner alone** | The owner of the agent owns the fix | Implementation bias. Owner naturally selects the cheapest fix, not the most-protective. |
| **Fix list with >5 items** | Capturing every idea instead of prioritizing | Nothing ships; team treats hardening as a discussion topic |
| **No measurable acceptance criteria** | *"Tighten the email tool"* | Owner ships something; nobody can prove it works; debate happens at next incident |
| **No replay test in M5** | Recovery goes straight from M5 staged re-enable to M0 Observe | Hardening control is shipped but never validated against the original trigger |
| **Retrieval boundary skipped** | RAG / KB is considered "data," not "infrastructure" | Same context-poisoning vector recurs with a slightly different document |
| **Evidence gaps not addressed** | Evidence capture was painful but worked; closure happens before fix is shipped | Next incident has the same capture friction; same 60-minute risk |
| **No metric tracking** | Hardening seen as one-time | Can't demonstrate trend improvement; [Maturity Roadmap](../framework/03-maturity-roadmap.md) Level 4 (Resilient) unreachable |

## Iterating the Hardening Practice

The playbook applies to individual incidents, but its **discipline** applies to the hardening practice itself. Every quarter, review:

- **How many hardening controls were shipped on time vs late?** Time-to-control trend.
- **Which controls actually held under subsequent incidents?** Pre/post efficacy metric.
- **How many incidents resulted in zero hardening?** This number should be zero.
- **Are TTSM and TTE trending in the right direction over rolling 90 days?** If not, the hardening is cosmetic.

These four data points are the [Maturity Roadmap](../framework/03-maturity-roadmap.md) Level 4 (Resilient) criteria for this playbook. TTSM and TTE are defined in [Playbook 13: The Six Metrics](13-six-metrics.md), along with how to capture them and how to read their trend lines. Without that discipline, the framework's promise of "continuous improvement" is a slogan, not a practice.

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md) (MVO-4 Controlled Re-Enable is the recovery gate this playbook fills)
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md) (clauses 2, 3, and 4: memory, retrieval, change disciplines)
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md) (Level 4 Resilient = measured improvement, this playbook's discipline)
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md) (each mode benefits from prior hardening)
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md) (gaps surfaced in capture become hardening priorities)
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml) (`incidents_history` records each hardening cycle)
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv) (the artifact most hardening cycles update)
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)) (the response that produces the lessons this playbook hardens)
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)) (the pre-incident discipline this playbook reinforces post-incident)
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)) (Metric 5 measures hardening SLA compliance; TTSM and TTE definitions live there)
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MANAGE 4.2, MANAGE 4.3)
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports ID.IM-01, ID.IM-02, RC.RP-04, RC.CO-03, GV.OV-01)
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses recurrence prevention for ASI02, ASI06, ASI08)

## The Question to Carry Forward

If you do nothing else after reading this playbook, answer this one question at your next incident closure:

> *Would a recurrence of the triggering prompt, exact same words, exact same context, be contained by the controls you shipped in the five business days after this incident?*

If yes, the hardening is real.
If no, the hardening is theater. The next recurrence is on the schedule. You just don't know which week.

That's the test. That's the discipline. That's what turns lessons learned into permanent guardrails.

---

*Source: AI IR Overlay newsletter, Issue #18, "Post-Incident Hardening in AI Incident Response," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
