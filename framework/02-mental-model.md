<!-- ────────────────────────────────────────────────────────────────── -->
<!--  The Mental Model                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Four sentences. Memorize them. They govern every AI IR decision.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# The Mental Model

Four sentences. Memorize them. They govern every AI IR decision.

> **If it can act, govern it as a privileged identity.**
> **If it can remember, treat it as a data store.**
> **If it can retrieve, protect it as a production system.**
> **If it can change, manage it as software, with rollback and auditability.**

---

## Why these four

Each clause maps a capability of modern AI agents to a discipline your security team **already knows how to do**. The overlay does not introduce new disciplines; it reassigns existing ones to a new class of system.

### 1. *If it can act, govern it as a privileged identity*

When an agent can send email, modify records, approve workflows, or trigger automations, its permissions define organizational blast radius. The mature discipline for managing privileged identities (least privilege, just-in-time elevation, MFA-equivalent gating, session logging, kill switches) applies directly.

**Implication:** treat every agent's tool list as a privileged-access grant. Review it in your PAM cadence.

### 2. *If it can remember, treat it as a data store*

Agent memory holds user context, intermediate reasoning, prior actions, and sometimes regulated data. The mature discipline for data stores (classification, retention, encryption, access logging, deletion) applies.

**Implication:** memory is in scope for SOC 2, HIPAA, GDPR, and PCI assessments. Plan for it before the auditor asks.

### 3. *If it can retrieve, protect it as a production system*

The retrieval layer (RAG, knowledge bases, connectors) is *part of the agent*. Poisoned context produces poisoned actions. The mature discipline for production systems (change control, vulnerability management, integrity verification) applies to corpora.

**Implication:** corpus updates are change-control events. Track them in CMDB.

### 4. *If it can change, manage it as software, with rollback and auditability*

Prompts, tool definitions, policies, and model versions all change in production. The mature discipline for software (versioning, rollback, code review, deployment gates, audit) applies.

**Implication:** "prompt updated" is a deployment. Treat it like one.

---

## Using the model in triage

When an AI incident is declared, walk the four sentences in order. Each one points to a different team and a different evidence source:

| Clause | Owning team | Where evidence lives |
|---|---|---|
| Acts | Identity / PAM | Audit logs, tool-call ledger |
| Remembers | Data / Privacy | Memory snapshots, vector store |
| Retrieves | Platform / DevOps | RAG traces, corpus versions |
| Changes | App Sec / SRE | Config snapshots, deployment log |

If you cannot identify the owning team for each clause **before** an incident, you do not have a complete AI IR program.

---

## Related

- **The Six Triage Questions:** [`triage/six-questions.md`](../triage/six-questions.md). The first-hour discipline that operationalizes the four clauses.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A–F evidence taxonomy each clause maps onto.
- **The Agent Is a Privileged Identity** ([Playbook 01](../playbooks/01-agent-as-privileged-identity.md)). The keystone playbook. The Mental Model's *"if it can act, govern it as a privileged identity"* clause is the lens PB01 operationalizes for every response sequence.
- **Tool Design Is Containment** ([Playbook 04](../playbooks/04-tool-design-is-containment.md)). The pre-incident discipline that makes the Acts clause operational. The tool layer is where governance becomes containment.
- **Insider Threat 3.0** ([Playbook 12](../playbooks/12-insider-threat-3.md)). The AI-driven insider misuse playbook. Covers the human-with-agent and agent-as-insider scenarios; the capability vs intent vs impact investigator triad; HR and Legal joint engagement from minute zero; intent vector documentation; and soft cap / hard cap discipline for bulk-summarize attacks.

---

*Source: AI IR Overlay newsletter and framework synthesis, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
