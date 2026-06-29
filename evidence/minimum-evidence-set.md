<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Minimum AI Evidence Set                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Six evidence types (A–F) plus capture order. Exportable in 60 minutes.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Minimum AI Evidence Set

> When the actor is an authorized agent, the question is not just *"what was compromised?"* but also *"what was trusted, what was retrieved, and what actions were taken in our name?"*

In AI incidents, evidence is fragile. The most common AI IR failure comes from well-meaning teams who disable integrations, rotate tokens, update prompts, and redeploy, and only then ask *"what exactly did it access?"* By then, the proof is gone.

This document defines the **minimum** evidence set every team must be able to capture, in what order, and within what time budget.

---

## The Capture Order (do not skip)

### Step 1: Stabilize Without Rewriting Reality

Use staged containment (Kill-Switch Modes M1 to M4) to stop damage **without destroying state**. The objective is to halt harm while keeping systems intact long enough to capture evidence.

### Step 2: Snapshot Identity and Capabilities

**Before** rotating credentials or making config changes, document:

- Agent identity (service account, OAuth grant, impersonation)
- Permissions held at incident time
- Enabled tools and write targets
- Current configuration (prompts, tools, policies, retriever settings)

### Step 3: Capture the Minimum AI Evidence Set

The six evidence types below. **Only then** rotate credentials, clean corpora, or redeploy.

---

## The Six Evidence Types (A–F)

### A. Prompt and Response Record

The user prompts, system prompts, and model outputs for the incident window.

**Where it lives:** model provider logs, API gateway logs, application logs.

**Capture format:** structured JSON with timestamps, user identity, session ID.

**Retention concern:** model provider TTLs are often short (24 to 72 hours). Pull immediately.

### B. Tool-Call Ledger (Action Log)

Attempted **and** successful tool calls, with parameters and results.

**Where it lives:** application middleware, function-calling logs, SaaS audit logs (target side).

**Critical detail:** capture *attempted* calls, not just successful. Denied calls are evidence of intent.

### C. Retrieval Traces (RAG / Knowledge-Base)

What the agent retrieved, from which corpus, at which version, with what scores.

**Where it lives:** vector store query logs, RAG framework traces, knowledge-base access logs.

**Why it matters:** poisoned context produces poisoned output. Without retrieval traces, you cannot prove the input vector.

See [RAG / Knowledge-Base Forensics (Playbook 03)](../playbooks/03-rag-knowledge-base-forensics.md) for the 90-minute freeze-the-world sequence and the seven-component pipeline forensics (C1 through C7).

### D. Memory Snapshot (if enabled)

The agent's persistent context as of incident time.

**Where it lives:** memory backend (Redis, vector DB, app DB), agent framework state.

**Scope question:** is memory per-user or shared? Memory bleed between users is its own incident class.

### E. Configuration Snapshot

The full agent configuration at incident time:

- System prompts (every version active in the window)
- Tool definitions and authorizations
- Policies and guardrails
- Retriever settings (corpus list, top-k, filters)
- Model version and parameters

**Where it lives:** config management system, deployment manifests, feature flags.

**Why it matters:** "what was the prompt?" is the most-asked post-incident question. Without a versioned snapshot, the answer is a guess.

### F. Identity and SaaS Audit-Log Correlation

The downstream evidence. What the agent did in target systems, attributed to the agent's identity.

**Where it lives:** IdP logs (Okta, Entra), SaaS audit logs (Salesforce, M365, ServiceNow), cloud CloudTrail/Activity logs.

**Why it matters:** confirms the blast radius and supports regulator/customer notification.

---

## Operational Requirements

To claim conformance with the Minimum Evidence Set:

- [ ] All six types (A–F) can be **exported within 60 minutes** of incident declaration
- [ ] The export procedure conforms to the [Evidence Export Script Contract](../schemas/evidence-export.spec.md): pre-staged access, parallel-export discipline, manifest and integrity hash, chain-of-custody attestation
- [ ] Owners and access paths for each type are pre-documented
- [ ] Pre-approved emergency access exists (no waiting on a ticket)
- [ ] Logs A and B are retained for a minimum window matching your IR plan (typically 90 days)
- [ ] Configuration snapshots (E) are versioned with every change in production

---

## Common Pitfalls

| Pitfall | Consequence |
|---|---|
| Rotating credentials before capturing scopes (B, F) | Cannot prove what the agent could do |
| Updating prompts before exporting previous state (E) | Cannot prove what the agent was told |
| Cleaning knowledge bases before preserving versioned content (C) | Cannot prove the input vector |
| Relying on screenshots instead of structured exports | Inadmissible in regulator or legal proceedings |
| Trusting model-provider retention defaults | Lose A within 72 hours |

---

## Related

- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md) (staged containment that preserves evidence)
- **RAG / Knowledge-Base Forensics** (Playbook 03): [`playbooks/03-rag-knowledge-base-forensics.md`](../playbooks/03-rag-knowledge-base-forensics.md) (Type C deep dive)
- **Evidence Export Script Contract:** [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md) (the runtime contract that operationalizes the 60-minute export requirement; telemetry events feed [Playbook 13 Metric 3](../playbooks/13-six-metrics.md))
- **Records, Retention, and Proving What Happened** (Playbook 15): forthcoming. See [CHANGELOG.md](../CHANGELOG.md) and [CONTENT_MAP.md](../CONTENT_MAP.md) for status.
- **Multi-Stakeholder Logging and Privacy** (Playbook 23): forthcoming. See [CHANGELOG.md](../CHANGELOG.md) and [CONTENT_MAP.md](../CONTENT_MAP.md) for status.

---

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
