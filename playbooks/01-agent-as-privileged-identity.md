<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 01 — The Agent Is a Privileged Identity                                                       -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The foundational playbook. If an agent can act, respond like you would to a privileged-identity incident.**
>
> *This file is one self-contained piece of the AI IR Overlay™ framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Playbook 01: The Agent Is a Privileged Identity

> *Every AI agent with tool access is a privileged identity in disguise. Respond to it like one, before, during, and after the incident.*

## Premise

Traditional incidents start with compromised endpoints, malware, or stolen credentials. Agent incidents often start somewhere else: **instruction hijack** (prompt injection), **context poisoning** (RAG / knowledge-base corruption), or **excessive agency** (over-permissioned tools). In all three classes, the most consequential variable is the same: *what the agent can do and where it can write*.

This playbook is the foundational one in the AI IR Overlay series because the privileged-identity lens is the **mental shift** that every subsequent playbook builds on. If your team can absorb this clause from the [Mental Model](../framework/02-mental-model.md):

> **If it can act, govern it as a privileged identity.**

Then the rest of the framework's machinery (Inventory, Safe Modes, Evidence Set, Controlled Re-Enable) snaps into place. If your team can't, you'll respond to an AI incident as if it were a software bug or a model-behavior question. You'll destroy evidence and over- or under-contain before you understand the blast radius.

**Use this playbook when:** an AI agent with tool access exhibits unintended behavior, an external researcher reports suspected prompt injection, retrieval traces show suspicious sources, or a downstream system (CRM, email, ticketing) shows actions the business didn't authorize.

**Mental Model clauses engaged:** *Acts* (primary), *Remembers* (if memory is enabled), *Retrieves* (if RAG/KB is implicated), *Changes* (if a recent config change preceded the incident).

## First-Hour Actions

Walk the [Six Triage Questions](../triage/six-questions.md) **in order** on the initial bridge call. Don't skip ahead. Each question scopes the next.

| # | Question | What it scopes | Where the answer lives |
|---|---|---|---|
| 1 | What tools can the agent call? | Action surface | AI-BOM `tools` section ([AI-BOM template](../templates/ai-bom.yaml)) |
| 2 | What systems can it write to? | Blast radius | AI-BOM `tools[].write_targets` |
| 3 | What identity does it run as? | Attribution chain | AI-BOM `identity` section |
| 4 | Does it have memory? What is the scope? | Cross-session risk | AI-BOM `memory` section |
| 5 | What is the least disruptive safe mode? | Containment decision | [Kill-Switch Modes](../kill-switches/overview.md) |
| 6 | What is your evidence plan before you rotate keys? | Preservation | [Minimum Evidence Set](../evidence/minimum-evidence-set.md) |

**Discipline:** if any answer takes more than 60 seconds to produce, you have an *inventory problem*, not an incident problem. The inventory gap is itself a finding. Document it in the decision log. Don't slow the bridge call to fix it.

**Decision log:** open it on minute zero. Capture the **time**, **the question**, **the answer** (with confidence), and **the action taken**. This becomes the chronology if regulators, customers, or the board ask later.

## Containment Options

Containment for a privileged-identity-class incident is **never** binary in production. The framework's [Kill-Switch Modes](../kill-switches/overview.md) provide a graduated ladder. The table below selects the right mode based on **confidence × impact**.

| Confidence the agent is compromised / misbehaving | Business impact of full disable | Recommended starting mode | Why |
|---|---|---|---|
| Low (suspicious, unclear) | Any | **M1 Read-Only** | Stop writes without stopping business; preserves state for forensics |
| Medium | High (customer-facing, revenue-critical) | **M2 Approvals Required** | Two-person rule keeps service running with control |
| Medium-to-high (specific tool implicated) | Any | **M3 Tool Tiering** | Disable the specific tool(s); leave the rest |
| High (active harm, confirmed compromise) | Any | **M4 Full Disable** | Hard stop, but capture evidence **before** rotating tokens |

**Critical sequence (M4 only):**

1. **Snapshot identity and capabilities BEFORE token rotation** (Evidence Step 2, see [Minimum Evidence Set](../evidence/minimum-evidence-set.md)).
2. **Capture the Minimum AI Evidence Set** (A–F) **before redeployment**.
3. **Only then:** rotate credentials, clean corpora, redeploy.

Rotating tokens before capturing scopes is the single most common evidence-destruction failure in AI IR. It's the reason this playbook lists "evidence plan before key rotation" as Triage Question 6.

## Evidence Priorities

For a privileged-identity-class incident, the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) types **A**, **B**, and **F** are load-bearing. Types **C**, **D**, **E** are conditional on the specific attack vector.

| Code | Evidence Type | Priority for this scenario | Why |
|---|---|---|---|
| **A** | Prompt and Response Record | **Critical** | Establishes what the agent was told and how it responded; proof of intent or compromise |
| **B** | Tool-Call Ledger | **Critical** | The action log; **capture attempted calls, not just successful**. Denied calls are evidence of attacker intent. |
| **F** | Identity and SaaS Audit-Log Correlation | **Critical** | Confirms downstream blast radius in target systems; supports regulator/customer notification |
| **C** | Retrieval Traces | High if RAG / KB is suspected vector | Without it, context poisoning is unprovable |
| **D** | Memory Snapshot | High if memory `scope: shared` | Cross-tenant memory bleed is its own incident class |
| **E** | Configuration Snapshot | High if a recent config change preceded the incident | Versioned snapshot answers "what was the prompt?" definitively |

**Retention concern:** model-provider logs (type A) often have 24–72h TTLs. **Pull A immediately**, within the first 15 minutes of the incident. SaaS-side logs (type F) have longer windows but require explicit pull requests. Queue those in parallel with A.

**Operational requirement:** the team must be able to **export the full set within 60 minutes** of incident declaration. If you can't, you don't have a Level 3 (Provable) [Maturity Roadmap](../framework/03-maturity-roadmap.md) capability. Log the gap.

## Recovery Sequence

After eradication, recovery follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **two scenario-specific gates** added:

1. **Re-enable in Read-Only (M1).** Confirm the agent functions and logs flow.
2. **Validate identity and tool policies** (*scenario-specific gate*). Confirm the agent's permissions match the **pre-incident AI-BOM**, not the post-rotation configuration. Drift between intended and actual scope is itself a finding.
3. **Validate retrieval and configuration.** Corpora versions confirmed clean. System prompt matches the approved version.
4. **Replay the incident scenario in a safe harness.** Sandbox the original trigger (the suspicious prompt, the poisoned document, the over-permissioned tool call) and confirm the fix holds.
5. **Re-enable tools incrementally** (*scenario-specific gate*). Start with **lowest-tier tools first** (T0 read-only per the [Privilege Matrix](../templates/agent-privilege-matrix.csv)). Monitor for drift, then T1, then T2 with approvals.
6. **Return to M0 Observe.** Only after monitoring thresholds confirm normal behavior over a documented window (typically 24–72 hours).

**Approver:** CISO or designated Incident Commander. **Never** the original agent owner alone. The owner has implementation bias; the IC has containment bias. The recovery decision needs the IC's lens.

## Post-Incident Hardening

The hardening priorities for a privileged-identity-class incident map directly to existing security disciplines:

| Discipline | Action |
|---|---|
| **PAM** (Privileged Access Management) | Add the agent's identity to your PAM review cadence. Treat the agent's tool list as a privileged-access grant. Review it quarterly. |
| **Tier classification** | Confirm every tool has a `risk_tier` in the [Privilege Matrix](../templates/agent-privilege-matrix.csv). Add **CI checks**: no T2 tool with `approval_required: no`; no T2 tool without `reversible` specified. |
| **AI-BOM update** | Update the agent's [AI-BOM](../templates/ai-bom.yaml) `incidents_history` entry with date, summary, mode activated, duration, outcome. |
| **Kill-Switch tabletop** | Schedule a tabletop within **30 days** to validate the fix and exercise M1–M4 against the same scenario class. |
| **Detection thresholds** | Update monitoring to detect recurrence of the specific attack vector (prompt injection patterns, retrieval anomalies, tool-call rate spikes). |
| **Post-incident comms** | Prepare the recovery communication per [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md). Internal stakeholders, customers, and regulators if scope warrants. |

**Done when:** the [Maturity Roadmap](../framework/03-maturity-roadmap.md)'s Level 4 (Resilient) criteria for this agent are met. Drill happened, metrics moved, AI-BOM updated.

## Common Pitfalls

These are the highest-frequency failure modes in this scenario class. Each one destroys evidence or expands the incident.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Rotating tokens before capturing scopes** | "Stop the bleeding" reflex from traditional IR | Can't prove what the agent could do. Scope becomes a guess. |
| **Updating the system prompt before exporting type E** | Owner wants to "fix it now" | Can't prove what the agent was told. Defensibility collapses. |
| **Cleaning the knowledge base before preserving versioned content** | Operations team treats corpus as logs | Can't prove the input vector for context-poisoning class incidents |
| **Going straight to M4 (Full Disable) on low-confidence reports** | Over-correction; "when in doubt, kill" | Business impact larger than necessary; destroys forensic state |
| **Going straight to M0 (Observe) on confirmed compromise** | Owner resists containment for revenue reasons | Active harm continues during forensic delay |
| **Skipping the Triage Six** | Bridge call jumps to root-cause discussion before scoping | Containment decisions made without blast-radius data |
| **Trusting model-provider retention defaults** | Assumption that "the logs are there" | Type A evidence lost within 72 hours |
| **Relying on screenshots instead of structured exports** | Convenience under pressure | Inadmissible in regulator or legal proceedings |
| **Re-enabling tools all at once after M5** | "We're past the incident, just turn it back on" | Re-triggers the same incident; M5 staged sequence skipped |
| **No post-incident AI-BOM update** | Incident closure is treated as finished | Next responder has the pre-incident inventory; the lesson is lost |

## Related

Distributed as separate packages or files within the framework:

- **The Six Triage Questions:** [`triage/six-questions.md`](../triage/six-questions.md) (the first-hour discipline this playbook orchestrates)
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md) (full mode specifications and TTA targets)
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md) (A–F types, capture order, retention requirements)
- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md) (the four controls, including MVO-4 Controlled Re-Enable)
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md) (the four-clause foundation, especially *if it can act, govern it as a privileged identity*)
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml) (the inventory schema this playbook's first-hour questions resolve against)
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv) (the tool-tier matrix that makes M3 Tool Tiering surgical)
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MANAGE 1.3, 2.3, 2.4, 4.1)
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports RS.MA-01, RS.MA-04, RS.MI-01, RS.MI-02)
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook responds primarily to ASI01 Agent Goal Hijack, ASI02 Tool Misuse, ASI03 Identity & Privilege Abuse, ASI05 Unexpected Code Execution)

## The Question to Carry Forward

If you're deploying agents today, here is the question to put in front of leadership:

> *Do your agents have write access in production, and do you have a tested safe mode you can activate in under 10 minutes?*

If the answer to the first half is *yes* and the answer to the second half is *no, or untested*, this playbook is the work plan. Build the inventory ([AI-BOM template](../templates/ai-bom.yaml)). Tier the tools ([Privilege Matrix](../templates/agent-privilege-matrix.csv)). Tabletop the modes ([Kill-Switch Modes](../kill-switches/overview.md)). Document the evidence path ([Minimum Evidence Set](../evidence/minimum-evidence-set.md)). Then test it before you need it.

---

*Source: AI IR Overlay newsletter, Issue #1, "The Agent Is a Privileged Identity," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
