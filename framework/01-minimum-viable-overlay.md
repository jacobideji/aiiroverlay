<!-- ────────────────────────────────────────────────────────────────── -->
<!--  The Minimum Viable Overlay (MVO)                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Four controls. Each small. Together: the minimum standard.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# The Minimum Viable Overlay (MVO) — Four Essential Controls

The MVO is the smallest set of controls that converts an AI deployment from *unreadiness* to *defensibility*. Adopt all four to claim minimum-standard conformance.

These four controls are referenced throughout the framework as **MVO-1 (Inventory)**, **MVO-2 (Safe Modes)**, **MVO-3 (Minimum Evidence Set)**, and **MVO-4 (Controlled Re-Enable)**.

---

## 1. Inventory

**Question answered:** *What can the agent do, and where can it write?*

A comprehensive inventory of every AI agent in production. Without it, responders cannot scope an incident in real time, and well-meaning containment either over-reacts or under-reacts.

For each agent, the inventory must capture:

| Field | Example |
|---|---|
| **Agent name + business owner** | "Sales Triage Copilot · owner: VP Sales Ops" |
| **Execution identity** | Service account, delegated OAuth, user impersonation, shared token |
| **Enabled tools and connectors** | Outlook send, Salesforce write, internal RAG, code execution |
| **Write targets** | CRM records, email recipients, ticket systems, code repos, cloud actions |
| **Retrieval corpora** | SharePoint folder X, Confluence space Y, vector store Z |
| **Access controls on corpora** | Read scope, sensitivity classification, refresh cadence |
| **Memory configuration** | Off / per-user / shared / TTL |

**Operational requirement:** the inventory must be **exportable in under 5 minutes** during an active incident. A wiki page that takes 30 minutes to find is not an inventory.

> **Mental model:** if you cannot answer *"what can this agent do?"* in one sentence, you cannot contain its incident in one hour.

See the **AI Bill of Materials (AI-BOM)** template — distributed as the `template-ai-bom` package.

---

## 2. Safe Modes — Rapid Activation and Tiered Containment

**Question answered:** *Can we stop harm in under 10 minutes without killing the business?*

A binary on/off switch is rarely appropriate in production. The Overlay defines six **Kill-Switch Modes** that escalate in severity:

| Mode | Name | Use when |
|---|---|---|
| **M0** | Observe | Normal operations |
| **M1** | Read-Only | Suspicious behavior; low/moderate business impact |
| **M2** | Approvals Required | Agent must keep operating; actions need a two-person rule |
| **M3** | Tool Tiering | Targeted: disable high-risk tools, keep low-risk |
| **M4** | Full Disable | Active harm or confirmed compromise |
| **M5** | Controlled Re-Enable | Containment validated; staged recovery |

**Operational requirements:**

- Modes M1–M4 must be activatable within **10 minutes** by Tier-1 SOC
- Mode M5 requires CISO or designated incident commander approval
- Each mode must be tested in a tabletop **before** the first production deployment

See the **Kill-Switch Modes** full specification — distributed as the `kill-switches-modes` package.

---

## 3. Minimum AI Evidence Set

**Question answered:** *Can we prove what happened in 60 minutes?*

In AI incidents, evidence is fragile. Rotating tokens, redeploying agents, or cleaning knowledge bases without snapshots will destroy proof of scope. The Overlay defines a minimum set of six evidence types that must be preservable on demand:

| Code | Evidence Type |
|---|---|
| **A** | Prompt and response record for the incident window |
| **B** | Tool-call ledger (attempted and successful calls, parameters, results) |
| **C** | Retrieval traces (documents, sources, timestamps) |
| **D** | Memory snapshot (if memory is enabled) |
| **E** | Configuration snapshot (prompts, tool definitions, policies, retriever settings) |
| **F** | Identity and SaaS audit-log correlation |

**Operational requirement:** the team must be able to **export the full set within 60 minutes** of incident declaration, using documented procedures and pre-approved access paths.

> **The rush-to-contain trap:** the most common AI IR failure comes from well-meaning teams who disable integrations, rotate tokens, update prompts, and redeploy — and only then ask "what exactly did it access?" Evidence-first discipline is the single biggest predictor of defensible response.

See the **Minimum Evidence Set** full specification — distributed as the `evidence-minimum-set` package.

---

## 4. Controlled Re-Enable — Staged, Validated Recovery

**Question answered:** *Can we recover in stages without restarting the incident?*

Recovery is not binary. Systems are restored in stages, each with validation:

1. **Restore read-only access first** — re-enable the agent in observe mode
2. **Validate retrieval and tool policies** — confirm fixes hold post-incident
3. **Replay the incident scenario in a safe harness** — sandbox the original trigger
4. **Re-enable tools incrementally** — monitor for regression or drift after each
5. **Return to full operation** — only after the above passes

This stepwise approach prevents the most common recovery failure: re-enabling everything at once and re-triggering the same incident.

---

## Conformance: Claiming Minimum Standard

An AI deployment conforms to the AI IR Overlay Minimum Standard when:

- [ ] **Inventory** exists, is current within 7 days, and is exportable in under 5 minutes
- [ ] **Safe Modes** M1, M2, M3, M4 are implemented and tabletop-tested in the last 90 days
- [ ] **Minimum Evidence Set** A–F is exportable within 60 minutes
- [ ] **Controlled Re-Enable** procedure exists and is documented in the runbook

Document conformance using the **Board-Ready Scorecard** — distributed as the `playbook-24` package.
