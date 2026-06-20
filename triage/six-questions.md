<!-- ────────────────────────────────────────────────────────────────── -->
<!--  The Six Triage Questions                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The first-15-minutes discipline. Asked in order by the incident commander.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# The Six Triage Questions

> Use these on your initial bridge call. If you can answer all six in 15 minutes, you are already ahead of most teams.

When an AI agent incident is suspected, the first-hour decisions determine whether you contain harm or destroy evidence. These six questions are designed to be asked **in order** by the incident commander.

---

## 1. What tools can the agent call?

List enabled tools and integrations. Separate **read** from **write**.

- Read tools (search, lookup, retrieve)
- Write tools (send, create, update, delete, execute)
- External vs. internal (does it touch outside parties or customers?)

> If the answer takes more than 60 seconds to produce, you have an inventory problem, not an incident problem.

## 2. What systems can it write to?

Enumerate every system where action can be observed by a customer, partner, regulator, auditor, or board:

- Email (internal / external)
- CRM (Salesforce, HubSpot, Dynamics)
- Ticketing (ServiceNow, Jira, Zendesk)
- Cloud (AWS, Azure, GCP actions)
- ERP (SAP, Oracle, NetSuite)
- Code repository (commits, PRs, deploys)
- Anything that **changes records** or **triggers workflows**.

## 3. What identity does it run as?

- Service account
- Delegated OAuth grant (on behalf of which user?)
- User impersonation
- Shared token

The identity determines what audit logs to pull and which downstream systems will attribute the action.

## 4. Does it have memory? What is the scope?

- Is memory enabled?
- Is it **per-user** or **shared across users/teams**?
- What is the retention window?
- Is sensitive data classified before being stored in memory?

Memory scope determines blast radius across tenants and users.

## 5. What is the least disruptive safe mode?

Before you reach for the off switch, walk the **Kill-Switch Modes** (see the `kill-switches-modes` package):

- Can you move to **Read-Only (M1)**?
- Can you require **Approvals (M2)**?
- Can you **disable only high-risk tools (M3)**?
- Is **Full Disable (M4)** actually required?

The wrong choice here costs revenue. The wrong choice on the other side destroys evidence.

## 6. What is your evidence plan before you rotate keys?

Capture **prompt/response logs**, **tool-call logs**, and **configuration state** *before* rotating credentials, redeploying, or cleaning corpora.

See the **Minimum Evidence Set**, distributed as the `evidence-minimum-set` package.

---

## Printable Card

A single-page printable version of these six questions, designed to live on a SOC wall, is distributed as the **`triage-six-questions-card`** package.

## Related

Distributed as separate packages:

- **Kill-Switch Modes:** `kill-switches-modes`
- **Minimum Evidence Set:** `evidence-minimum-set`
- **Playbook 01: The Agent Is a Privileged Identity:** `playbook-01`

---

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
