<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 03 — RAG / Knowledge-Base Forensics                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The forensic-depth playbook. In RAG incidents, the model is just the messenger. The attack is in the context. Freeze, snapshot, and trace before you clean.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 03: RAG / Knowledge-Base Forensics

> *In retrieval-augmented incidents, the model produces what the retrieval gave it. The investigation isn't "what did the model do wrong?" It's "what did the retrieval layer feed the model, and how did that content arrive?"*

## Premise

Most discussion of AI agent risk focuses on the model: its prompts, its outputs, its safety behavior. But in production deployments where Retrieval-Augmented Generation (RAG) drives the agent's knowledge of the world, **the model is often just the messenger**. The attack is in the **context** the model received. A poisoned document, a manipulated source, a newly created high-influence file, or an embedding that places malicious content at the top of every search.

The RAG layer is simultaneously the **production environment** and the **crime scene**. Every minute that passes after an incident is suspected (without freezing knowledge sources, snapshotting the vector index, and exporting retrieval traces) is a minute of evidence destroyed by routine operations: nightly re-indexing, scheduled crawls, document updates, embedding model upgrades. By the time the response team understands the question, the artifacts that would answer it have been overwritten.

This is the forensic-depth playbook in the AI IR Overlay series. Where [Playbook 01](01-agent-as-privileged-identity.md) covers general response and [Playbook 04](04-tool-design-is-containment.md) covers tool-layer preparation, **Playbook 03 covers what to do when the suspected attack path is the RAG pipeline itself**. The seven-component chain from source systems through ingestion, embedding, vector storage, retrieval, prompt assembly, and output. Each component is a potential failure surface. Each one requires a distinct forensic discipline.

**Mental Model clause engaged:** *if it can retrieve, protect it as a production system.* The corollary: *if it can retrieve, forensicate it as a production system.* RAG forensics isn't separate from corpus governance. It's corpus governance under incident pressure.

**Use this playbook when:** an agent's outputs reference unexpected documents · a retrieval-dominance alert fires per [Playbook 18](18-post-incident-hardening.md) · users report agent responses that cite policies the organization doesn't have · a high-impact agent decision can't be traced back to its source document · a knowledge base administrator detects unexplained document changes · a vector index shows unexplained ranking shifts.

## First-Hour Actions

The first hour of a RAG-class incident has one job: **freeze the world without breaking the business**. Every other forensic action depends on getting this right.

### The Freeze-the-World Sequence (90-minute target)

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Stabilize the agent.** Activate [Kill-Switch M1 (Read-Only)](../kill-switches/overview.md) if not already engaged. The agent can still serve but can't write while retrieval forensics proceeds. | Tier-1 SOC |
| 10–25 | **Freeze knowledge sources.** Lock writes to corpora the agent retrieves from, OR shift the agent to a frozen read-only snapshot of the current index. **Pause all ingestion, crawls, and ETL into the affected corpus.** | Platform engineering + corpus owner |
| 25–45 | **Snapshot retrieval reality.** Export the **full vector index** (all embeddings, metadata, document IDs, version stamps, ingestion timestamps). Export the **last 7 days of retrieval traces** (queries, returned doc IDs, similarity scores, top-k rank). | RAG platform engineer |
| 45–70 | **Export source-system audit logs.** For each upstream system feeding the corpus (SharePoint, Confluence, Google Drive, ticketing, code repos, internal sites), pull change-history logs covering the incident window plus 7 days. | Identity / SaaS owners (parallel) |
| 70–85 | **Validate containment.** Confirm that ingestion is paused, writes are locked, the snapshot is intact, and the agent is operating from the frozen view. Document evidence that the freeze held. | Incident Commander |
| 85–90 | **Open the investigation log.** Record the freeze timeline, who locked what, what was exported, and the timestamp at which the index was snapshotted. | Incident Commander |

**Critical:** if any of these steps slips, evidence is degraded and the rest of the playbook is reconstructing from incomplete records. The 90-minute target is **aggressive on purpose**. Most organizations discover during this drill that ingestion is automated and harder to pause than they thought, that vector index export isn't pre-approved, or that source-system audit logs require manual ticket requests. **Those discoveries are themselves findings** for [Post-Incident Hardening](18-post-incident-hardening.md).

## Containment Options

For RAG-class incidents, containment maps to [Kill-Switch Modes](../kill-switches/overview.md) somewhat differently from PB01's general response model. The corpus itself becomes a containment surface, not just the agent's tools.

| Mode | RAG-specific application |
|---|---|
| **M0 Observe** | Normal operation; retrieval-dominance alerting active (per PB18 hardening) |
| **M1 Read-Only** | Agent can retrieve and respond but can't trigger write tools. **Doesn't stop the corpus from updating.** |
| **M2 Approvals Required** | High-impact agent actions require human approval. Useful when the corpus is uncertain but operations can't pause. |
| **M3 Tool Tiering** | Disable downstream Tier 2 actions that depend on retrieval. Useful when context integrity is suspected but read access is needed. |
| **M3-RAG** | **Disable retrieval against the suspect corpus while preserving retrieval against unaffected corpora.** Agent operates with reduced knowledge but no exposure to poisoned content. |
| **M4 Full Disable** | Hard stop on the agent. **Doesn't freeze the corpus.** Corpus freeze is a separate action. |
| **M5 Controlled Re-Enable** | Includes corpus revalidation as a gate before retrieval re-enables |

**The corpus-freeze decision is independent of the agent-mode decision.** You can run an agent in M0 Observe while the corpus is frozen for forensics, or run an agent in M4 Full Disable while leaving the corpus unfrozen because the corpus isn't the suspected attack path. Confusing these two decisions wastes time and degrades evidence.

## Evidence Priorities

For RAG-class incidents, **Type C (Retrieval Traces) is the load-bearing evidence type**. Most teams discover it's insufficiently instrumented when they need it most.

### Type C-extended for RAG

The base [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Type C captures *what the agent retrieved*. For RAG forensics, expand Type C to capture **the seven-component pipeline state at the time of retrieval**:

| Sub-type | What it captures | Why |
|---|---|---|
| **C1: Source system state** | Document ID, last-modified timestamp, author, last-modifier from SharePoint / Confluence / Drive / tickets / repos | Establishes who introduced the document and when |
| **C2: Ingestion state** | Connector ID, crawl timestamp, ETL pipeline version, chunking rule version | Identifies which ingestion path delivered the document |
| **C3: Embedding state** | Embedding model version + parameters at the time the document was vectorized | Embedding upgrades change rankings. The question "why did this document outrank?" depends on the embedding version. |
| **C4: Index state** | Vector index version, document chunks present, metadata, version timestamps | The index at retrieval time vs. now |
| **C5: Retriever state** | top-k value, filters applied, reranking model + version, recency boost coefficients | Identical query + different retriever settings = different results |
| **C6: Prompt assembly state** | Template version, max-context budget, document ordering rules, citation injection rules | How the retrieved content actually reached the model |
| **C7: Output + downstream actions** | Agent response text, tool calls triggered by retrieval, downstream system actions, recipient list | The blast radius of the poisoned context |

A team that can export all 7 sub-types within the 60-minute SLA has a **defensible chronology**. A team that captures only C1 and C4 has a **partial story** that won't survive regulator scrutiny.

### The Provenance Test

For each agent output reviewed in the investigation, you must be able to answer all three questions with timestamped evidence:

1. **What document(s) influenced this output?** Citation by doc ID and version.
2. **When did that document enter the knowledge base?** Ingestion timestamp.
3. **Who authored or modified it?** Source-system audit trail.

If the answer to any of these is "we don't have that data," the incident response is operating on **inference**, not evidence. The [PB 18 hardening](18-post-incident-hardening.md) priority for the next cycle is fixing that gap.

## Recovery Sequence

Recovery from a RAG-class incident follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **two RAG-specific gates**.

### Gate 1: Source restoration before index rebuild

Do not rebuild the vector index from the existing source systems if those source systems contained the malicious content. **Restore the sources first.**

1. Identify the **last known-good state** of each affected corpus (typically the last point before the suspect document(s) were introduced).
2. Restore source documents to that known-good state from version control or backups.
3. Re-validate access controls. The original document insertion may have used compromised credentials. Rotate before rebuild.
4. Re-validate ingestion connector configurations. The malicious content may have arrived via a connector misconfiguration that's still in place.

### Gate 2: Staged index rebuild with monitoring

1. **Rebuild the index from the restored sources** in a staging environment first.
2. **Replay representative agent queries** against the new index in staging. Verify the harmful retrieval pattern no longer reproduces.
3. **Validate the recurrence-containment test** per [PB 18](18-post-incident-hardening.md): would the original triggering query return the same harmful document now? If yes, the hardening is insufficient.
4. **Promote the rebuilt index to production** only after staging validation.
5. **Re-enable retrieval against the corpus in M1 Read-Only** for the first 24–72 hours. Monitor for retrieval-dominance recurrence.
6. **Return to M0** only after the observation window confirms normal retrieval behavior.

**Document-influence monitoring:** for at least 30 days post-recovery, track the **top 10 most-retrieved documents per agent per day**. Any document that suddenly enters the top 10 without a known business cause is a candidate for review.

## Post-Incident Hardening

The RAG-specific hardening priorities from this playbook complement [Playbook 18](18-post-incident-hardening.md)'s general Tiered Hardening Framework. These are the items that close the gaps RAG forensics typically exposes.

### Retrieval Provenance

| Hardening | Why |
|---|---|
| Every retrieved chunk carries `doc_id + version + ingestion_timestamp` in the trace | Enables Type C-extended capture without manual correlation |
| Every agent output stored in tickets/CRM includes a "Sources Used" footer with doc IDs and versions | Provenance survives outside the agent's own logs |
| Tier 2 actions (per [Privilege Matrix](../templates/agent-privilege-matrix.csv)) require **explicit citations** to source documents in the action's record | "The agent did this because of document X version Y" becomes part of the audit chain |
| Retrieval-dominance alerts (per [PB 18](18-post-incident-hardening.md)) trigger at >40% from a single document over 24h | Detects context-poisoning patterns before they cause measurable harm |

### Source-System Discipline

| Hardening | Why |
|---|---|
| Knowledge sources treated as production infrastructure: change control, rollback paths, audit logging | KB updates are deployment events, not data updates |
| Sensitive corpora isolated by user role | An agent for sales doesn't retrieve from finance policy corpus |
| Ingestion connectors versioned and reviewed | Misconfigured connectors are a re-introduction vector |
| Document promotion to high-authority status requires explicit approval | "Trusted" status is granted, not assumed |

### Forensic Readiness

| Hardening | Why |
|---|---|
| Vector index export procedure pre-approved + tested quarterly | The first time you discover the export procedure is broken shouldn't be during the incident |
| Source-system audit log access pre-approved (no waiting on ticketing during incident) | Forensic clock starts at incident detection, not at log access approval |
| Retrieval trace retention ≥ 30 days | Most RAG incidents are detected days after the triggering query |
| Embedding model version history retained | Re-ranking forensics requires the embedding version that was active at retrieval time |

## Common Pitfalls

These are the highest-frequency failure modes in RAG-class incident response. Each one quietly degrades evidence or extends the incident.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Cleaning the knowledge base before snapshotting** | "Remove the bad document fast" reflex | Evidence destroyed; can't prove the document existed, when, or who introduced it |
| **Treating retrieval traces as logs (delete after 7 days)** | RAG framework defaults are short | Incident detected day 14 has no evidence from day 0 |
| **Rebuilding the index from the same compromised sources** | Skipped Gate 1 (source restoration) | The same poisoned content re-enters the rebuilt index |
| **Pausing ingestion late** | Ingestion is automated and out of sight | More malicious content enters during the response window |
| **No `doc_id + version` in retrieval traces** | Traces capture similarity scores but not document identity | Can't trace from agent output back to source document |
| **Source-system audit logs not pulled in parallel** | Sequential investigation; SaaS log requests take hours | Source-system audit window expires before the request returns |
| **No "Sources Used" footer on agent outputs** | Provenance lives only in agent logs | Downstream evidence (ticket text, CRM notes, email) has no traceable chain |
| **Embedding model upgraded post-incident before forensics** | "We were going to upgrade anyway" | The embedding version that ranked the malicious document at the top is now lost |
| **Vector index export untested before incident** | Procedure exists in runbook only | Discovery during incident: export breaks at 10GB; index is 200GB |
| **Sensitive corpora not isolated by role** | DRY principle applied to data | Agent for one team retrieves from another team's confidential corpus |

## Related

Distributed as separate packages or files within the framework:

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md) (MVO-3 Evidence Set + MVO-4 Controlled Re-Enable underpin this playbook)
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md) (clause 3: *if it can retrieve, protect it as a production system*)
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md) (Level 3 Provable requires Type C-extended capability)
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md) (Modes M1, M3-RAG, M5 are RAG-specific in this playbook)
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md) (Type C is the load-bearing evidence type for this playbook)
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml) (the `retrieval` section is the source of truth for corpora the agent retrieves from)
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)) (general response playbook this RAG-specific playbook extends)
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)) (the discipline that makes M3-RAG executable)
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)) (where the gaps surfaced in this playbook become quarterly hardening commitments)
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)) (the Evidence domain B3 action-sequence reconstruction depends on this playbook's Type C-extended capability)
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MAP 2.3, MEASURE 2.7, MANAGE 4.1)
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports PR.DS-01, DE.AE-03, RS.AN-03, RS.AN-07)
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the **direct operational response** to ASI06 Memory & Context Poisoning)

## The Question to Carry Forward

If you do nothing else after reading this playbook, answer these two questions for your highest-impact production agent, and be honest about whether the answers come from evidence or inference:

> *If your knowledge base were poisoned today, could your team freeze ingestion, export retrieval traces, and identify the "high-influence" document within 60 minutes?*
>
> *Could you show the exact document version behind your agent's last high-impact decision, right now?*

If the first answer is no, your forensic readiness is incomplete. The response to the next RAG incident will be reconstruction, not investigation.
If the second answer is no, your agent's outputs are operating on **trust without provenance**. The next regulator, auditor, or customer inquiry will expose the gap before you discover it.

In a RAG-driven system, the model can only be as honest as the retrieval that feeds it. The first job of the response team is to **freeze the world**. The second job is to **prove what the world contained**. Everything else is reconstruction.

---

*Source: AI IR Overlay newsletter, Issue #3, "RAG / Knowledge Base Forensics: When Context Becomes the Attack Path," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
