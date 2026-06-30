<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 15: Records, Retention, and Proving What Happened        -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The proof-discipline playbook. The framework's [Minimum Evidence Set](../evidence/minimum-evidence-set.md) specifies what to capture and the 60-minute export discipline; PB15 specifies how to keep that evidence defensibly across the regulatory, legal, and business-trust windows where the hardest post-incident conversations happen. Two-tier retention, chain-of-custody discipline, incident-triggered legal hold, tamper-evident integrity, and the empirical reconstructability test that proves the framework's evidence claims at 30, 60, and 90 days.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 15: Records, Retention, and Proving What Happened

> *AI incidents need more than technical fixes; they need proof. Three weeks after the incident closes, the question is rarely "did the team respond correctly?"; it is "can you prove what the agent accessed and what it sent where?" The hardest post-incident conversations are the ones where the security team executed flawlessly during the first 60 minutes and then lost the evidence to short retention windows, vendor TTLs, payload truncation, or a cleanup that ran 72 hours after the incident closed. This playbook is the records discipline that turns the framework's evidence taxonomy into a defensible proof chain that survives the regulatory, legal, and business-trust review window.*

## Premise

The framework's [Minimum Evidence Set](../evidence/minimum-evidence-set.md) defines six evidence types (A through F) and a 60-minute export discipline. Two playbooks deepen specific types: [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md) is the Type C deep-dive (retrieval traces and the seven-component pipeline), and [Playbook 09 (Output Leakage)](09-output-leakage.md) is the Type F deep-dive (the output distribution map). PB15 is the **lifecycle deep-dive**: how every evidence type is captured, retained, protected, exported, and ultimately disposed of with defensibility intact across the entire post-incident window.

This makes PB15 operationally distinct from the rest of the framework's playbooks in four ways:

| Aspect | Standard AI incident playbook | Records and retention discipline |
|---|---|---|
| Time horizon | First 60 minutes through the 5-business-day hardening SLA per [Playbook 18](18-post-incident-hardening.md) | 30 days, 90 days, 1 year, 3 years, and beyond, depending on regulatory and contractual obligation |
| Primary risk | Failure to contain or detect the original incident | Failure to prove what happened when the question is asked weeks or months later |
| Surface symptom | Active behavior shift, alarm, or business impact | A regulator's letter, a customer's contract clause, a legal hold notice, a board question on a quarterly review |
| Detection latency for failure | Minutes to hours | Weeks to years, often surfacing only when the evidence is needed and discovered missing |

Evidence loss is not a single failure mode. It is a category of failure modes that compounds quietly across the post-incident window:

- **Vendor TTL expiry.** Model provider prompt-and-response logs (Type A) often default to 24-to-72-hour retention. If the export-within-60-minutes discipline is not enforced, Type A is gone before the 5-business-day hardening review per [Playbook 18](18-post-incident-hardening.md) begins.
- **Payload truncation.** Many telemetry pipelines truncate event payloads at 32 KB or smaller to control storage cost. A truncated tool-call ledger entry (Type B) preserves the fact that the call happened but not the parameters that determine whether the call was harmful, in scope, or anomalous.
- **Index turnover.** Vector indices and corpus stores typically retain only the current version; rebuilds erase the prior version unless explicit versioning discipline per [Playbook 03](03-rag-knowledge-base-forensics.md) is in place. Type C evidence (retrieval traces against the corpus version at incident time) becomes unrecoverable.
- **Configuration drift.** Without the change-pipeline event ledger per [Playbook 22 (Model and Policy Drift)](22-model-policy-drift.md), Type E (Configuration Snapshot) becomes a single-point-in-time artifact rather than a time series. The "what was the prompt 17 days ago?" question becomes unanswerable.
- **Storage tier shifts.** Many logging platforms move data from hot to warm to cold storage on automated schedules; the warm tier may be days, the cold tier may not be queryable at all. Evidence is technically retained but not accessible within the post-incident-investigation timeframe.
- **Sensitive-data redaction.** Payload-class evidence (prompts, responses, retrieval content, tool-call parameters) often contains regulated data; redaction policies applied without forensic awareness can destroy the evidence at the same time they protect the data.

Most evidence loss is small and operationally invisible. Some evidence loss is large and produces unprovable incidents when the proof is needed. The proof discipline's job is to make all retention failures detectable through periodic reconstructability tests rather than through the post-incident discovery that the evidence is already gone.

The biggest operational problem with evidence retention is not the cost of storage; it is the cost of unprovable incidents. An unprovable AI incident produces the worst possible regulatory posture (the customer cannot answer the regulator's question), the worst possible customer-trust posture (the customer cannot answer the affected user's question), and the worst possible internal posture (the executive question "how do we know this will not happen again?" cannot be defensibly answered). This playbook's job is to make proof load-bearing rather than incidental.

**Mental Model clauses engaged:** *Remembers* (primary, because retention is fundamentally a memory discipline applied to evidence rather than to the agent's operational memory); *Acts* (Type B and Type F evidence carry the action history); *Retrieves* (Type C evidence carries the retrieval history); *Changes* (Type E evidence and the change-pipeline event ledger carry the configuration time series).

**Use this playbook when:** designing or reviewing the customer's AI evidence retention standard · pre-positioning the customer's organization for an audit or regulator review · responding to a legal hold notice that includes AI-system scope · scoping the customer's Six Metrics ([PB13](13-six-metrics.md)) Metric 3 (Time-to-Evidence) baseline · running the quarterly Reconstructability Test from this playbook · responding to a customer or regulator request that asks the customer to "prove exactly what the agent accessed and where it sent it" · scoping evidence collection for a [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) investigation that requires HR/Legal-grade evidence handling · scoping evidence collection for a [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) retrospective that depends on evidence captured weeks earlier · scoping evidence collection for a [Playbook 22 (Drift)](22-model-policy-drift.md) change-event forensics analysis that depends on configuration snapshots from before the change window.

## First-Hour Actions

PB15 is unusual in the framework because its First-Hour Actions are typically **pre-incident** rather than during-incident: the first hour of an evidence-retention failure is most often the first hour of the audit or legal review that surfaced the failure, not the first hour of an AI incident. This section addresses both cases.

### Case A: During an active AI incident, the records discipline is invoked alongside the operational playbook

The First-Hour Actions of the operational playbook (PB01, PB03, PB06, PB07, PB08, PB09, PB10, PB12, PB21, PB22) are unchanged. PB15's during-incident discipline is the evidence-side checklist that runs in parallel.

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Confirm the legal hold trigger criteria.** If the surfaced incident has any of the following characteristics, the customer's legal hold mechanism activates immediately on the affected evidence stores: customer data touched, regulated data touched, external recipient affected, financial action involved, suspected insider misuse per [Playbook 12](12-insider-threat-3.md), or vendor-managed agent under shared-responsibility scope per [Playbook 10](10-vendor-copilots.md). The legal hold extends the default retention window to the customer's legal-hold standard (typically the duration of the matter plus a documented post-matter window). | Incident Commander + Legal |
| 10–30 | **Pull Type A (Prompt and Response Record) immediately.** Vendor TTLs on prompt-and-response logs are the framework's most fragile evidence type; the export window may be as short as 24 hours. Pull within the first 30 minutes regardless of whether the rest of the response sequence has begun. Apply the [Evidence Export Script Contract](../schemas/evidence-export.spec.md) integrity manifest at export time. | Detection engineer + Evidence custodian |
| 30–45 | **Verify the chain-of-custody discipline is active.** Every access to the evidence store from this moment forward is access-logged with actor identity, timestamp, query, and access purpose. Evidence is treated as restricted-access from the moment the incident is declared. The access log itself enters the evidence chain as Type B for the evidence store. | Evidence custodian + Detection engineer |
| 45–55 | **Confirm payload-tier retention extension where applicable.** Customers whose default retention separates metadata from payload (per the Two-Tier Retention Standard below) must verify that the payload tier is held under the incident scope. The default payload window (often 7 to 30 days) is shorter than the customer's incident-investigation cycle; the legal hold or incident-triggered extension is what preserves payload-class evidence past its default. | Platform engineer + Legal |
| 55–60 | **Convene the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) if the incident has touched customer data, regulated data, external recipients, or financial actions.** PB15's role in this convening is to certify that the evidence required to defend the customer's materiality determination is preserved under the legal hold. | Incident Commander + Legal |

### Case B: An audit, regulator review, or legal hold notice has surfaced an evidence-retention question that does not have an active AI incident attached

The first hour is investigative rather than containment-driven. The discipline is to confirm the question that needs an answer and the evidence that supports the answer before any reconstruction begins.

| Minute | Action | Owner |
|---|---|---|
| 0–15 | **Confirm the scope and the question.** Document the auditor or regulator's specific request: which agent, which time window, which type of evidence (A through F or specific subsets), which downstream system, which user identity, which corpus, which configuration version. Vague requests produce vague reconstructions; the request scope determines the reconstruction's success criterion. | Legal + Incident Commander |
| 15–35 | **Inventory what the customer has for the requested scope.** Query each evidence-store path that should hold each Type A through F for the agent and time window. Note the gaps (missing types, truncated payloads, expired retention, inaccessible cold-tier data, missing configuration snapshots). The gap inventory is the load-bearing input for the rest of the response. | Evidence custodian + Platform engineer |
| 35–50 | **Apply legal hold to everything still in retention** for the requested scope. The hold prevents subsequent storage-tier transitions, redaction passes, or scheduled deletions from removing evidence that is still recoverable. Hold first; reconstruct second. | Legal + Platform engineer |
| 50–60 | **Run the partial Reconstructability Test against the available evidence** before promising the auditor or regulator a complete answer. If the available evidence does not support a complete reconstruction, the customer's response to the requester names the gap explicitly rather than producing a partial reconstruction that hides the gap. The gap itself is a reportable finding in the customer's records discipline. | Evidence custodian + Legal |

**Discipline:** evidence loss is most often a slow leak rather than a single failure. The First-Hour Actions of PB15 are about catching the leak at the moment the evidence becomes operationally important, not about preventing the leak (which is the Post-Incident Hardening discipline). The instinct to start reconstructing before applying legal hold is the most damaging shortcut in this playbook. Hold first; reconstruct second.

**Critical rule:** the chain-of-custody discipline applies to the evidence store, not just to the original AI system. Every access to the evidence store from the moment an incident is declared (Case A) or an external request lands (Case B) is itself an event that enters the evidence chain. An evidence store without access logging cannot produce a defensible chain of custody regardless of how well the underlying evidence was captured.

**Post-quantum migration note (v0.33.0):** the framework's current tamper-evidence anchor uses SHA-256 (per [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md) and the reference implementation at [`reference-impls/evidence_exporter/`](../reference-impls/evidence_exporter/)). SHA-256 is defensible at v0.33.0 (no known quantum attack reduces second-preimage security materially) but is not a long-horizon choice. As NIST PQC standards mature (FIPS 203/204/205 for ML-KEM/ML-DSA/SLH-DSA and successors) and tamper-evidence anchoring graduates from hash-only to signed-manifest with PQC signatures, the framework's PB15 retention discipline will need to specify the migration path. v1.1 candidate: NIST PQC algorithm options for evidence-manifest signing (CRYSTALS-Dilithium / ML-DSA as a starting point) and the migration discipline that preserves backward verifiability of pre-migration evidence (see [`CHANGELOG.md`](../CHANGELOG.md) `[Unreleased]` v1.1 backlog).

## Containment Options

PB15 does not introduce a new kill-switch variant because retention is a discipline, not a containment surface. The framework's existing [Kill-Switch Modes](../kill-switches/overview.md) apply unchanged to the operational containment of the underlying incident. PB15's containment-equivalent discipline is the **retention-class containment**: the actions that prevent further evidence loss while the operational containment proceeds.

### Retention-class containment

| Action | Use when | What changes |
|---|---|---|
| **Legal hold activation on the evidence store** | Any incident with regulatory, legal, or customer-trust scope | All scheduled retention transitions (warm-to-cold, cold-to-delete, automated redaction) are suspended on the affected evidence. The hold typically applies to all evidence types for the affected agent across the incident window plus a buffer (commonly 30 to 90 days before and after) |
| **Access-restriction tightening on the evidence store** | An incident with insider-threat scope per [Playbook 12](12-insider-threat-3.md), or with regulator-review scope where access-log integrity is load-bearing | The evidence store is moved to a restricted-access configuration; access requires explicit IC or Legal authorization; every access is logged with actor, timestamp, query, and access purpose |
| **Storage-tier promotion** | An incident where the relevant evidence has already moved to cold storage and is operationally inaccessible during the investigation window | The relevant cold-tier data is promoted back to warm or hot for the duration of the investigation; the cost is documented as part of the incident's operational cost |
| **Vendor-side hold request** | An incident involving a vendor-managed AI platform per [Playbook 10](10-vendor-copilots.md) where the customer's contract includes evidence-preservation SLA support | The customer submits the evidence-preservation request to the vendor under the contracted SLA; the vendor's response (acknowledgment, preservation confirmation, extended retention window) is logged in the customer's evidence chain |
| **Payload-tier hold for redaction-eligible evidence** | An incident where the default redaction policy would remove payload-class evidence before the investigation completes | The redaction pipeline is paused for the affected evidence subset; the pause is documented with the explicit risk-acceptance that payload-class evidence is being retained under elevated sensitivity |
| **Cross-system correlation hold** | An incident requiring Type F (Identity and SaaS Audit-Log Correlation) where the downstream SaaS audit-log retention is shorter than the customer's investigation cycle | The customer requests extended retention from the affected SaaS providers under the customer's enterprise agreement or under explicit ticketed request; the extension is logged with the SaaS provider's confirmation |

These six containment actions are complementary, not exclusive. A complex incident may use legal hold for the customer's own evidence store, access-restriction tightening for an insider-threat scope, vendor-side hold request for a vendor-managed agent, payload-tier hold for redaction-eligible evidence, and cross-system correlation hold for the downstream SaaS audit logs, all in parallel.

## Evidence Priorities

PB15 extends the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A through F with a structured **Retention Tier** classification that calibrates retention windows by evidence class, integrity criticality, and regulatory exposure. The classification is the lifecycle equivalent of the Privilege Matrix's T0/T1/T2 tool tiering: a pre-positioned discipline that determines how each evidence type is treated when the incident hits.

### The Two-Tier Retention Standard

Every evidence type has two retention horizons: a **metadata horizon** that captures the existence, identity, timestamp, version, and destination of each event, and a **payload horizon** that captures the full content of the event (prompt body, response body, tool-call parameters, retrieved document content, configuration content). The two horizons typically differ by an order of magnitude.

| Evidence Type | Metadata retention (recommended baseline) | Payload retention (recommended baseline) | Notes |
|---|---|---|---|
| **A** Prompt and Response Record | 1 year (timestamps, model identifier, session ID, user identity, response length, content category) | 30 to 90 days (prompt body and response body) | Vendor TTL is the constraint; some vendors do not retain payload at all and the customer must capture at the API gateway |
| **B** Tool-Call Ledger | 1 to 3 years (timestamps, tool identifier, target system, success or denied, identity, correlation ID) | 90 to 180 days (parameters and results) | Denied calls are retained as part of the metadata tier indefinitely (they are evidence of intent regardless of whether they succeeded) |
| **C** Retrieval Traces | 1 year (timestamps, corpus identifier, query identifier, document identifiers, version pins, similarity scores) | 90 days (retrieved document content and full query text) | See [PB03 RAG Forensics](03-rag-knowledge-base-forensics.md) for corpus-version retention specifics; the corpus index itself must be retained at the metadata tier for at least the document-level retention window |
| **D** Memory Snapshot | 1 year (timestamps, memory backend identifier, scope class, retention class, entry counts) | 30 to 90 days (memory entry content) | Per-user memory may carry regulated-data exposure that shortens the payload retention; shared memory may require longer retention for cross-session forensics |
| **E** Configuration Snapshot | 7 years (timestamps, change identifier, approver identity, change category, version diff hash) | 1 to 3 years (full configuration content) | Configuration evidence supports the longest-horizon questions ("what was the agent told to do in March of last year?"); metadata retention typically matches the customer's records-retention standard for change management |
| **F** Identity and SaaS Audit-Log Correlation | 3 to 7 years (timestamps, identity, action class, target system, correlation ID) | 90 to 180 days (full event detail including downstream action parameters and results) | Downstream SaaS retention typically determines the binding constraint; the customer must verify per-provider retention before claiming framework conformance |

The two-tier pattern's discipline: **metadata is cheap to retain and load-bearing for reconstructability**; **payload is expensive to retain and load-bearing for content-level proof**. The customer's payload retention is calibrated against the customer's expected incident-investigation cycle (typically 30 to 90 days post-incident), not against worst-case regulatory horizons. Incident-triggered legal hold is the mechanism that extends payload retention past the default for events that require it.

### The legal-hold extension mechanism

When the customer's incident-declaration or external request triggers legal hold, the affected evidence transitions from default retention to hold-class retention. The mechanism:

1. **Hold scope identification.** The hold names the agent, the time window, the evidence types, and the access scope. A hold that is overscoped retains data beyond the legal need (a privacy risk); a hold that is underscoped misses evidence (a forensic risk). The scope is documented at hold activation.
2. **Hold-class retention duration.** The hold typically persists for the duration of the legal or regulatory matter plus a documented post-matter window (commonly 90 to 365 days). The hold's end date is recorded at activation with the matter's expected closure and is reviewed quarterly.
3. **Hold notification.** The hold is logged in the customer's evidence chain; affected stakeholders (platform engineering, evidence custodian, legal, IC) are notified; the hold's status is queryable by the legal team without requiring per-event drill-down.
4. **Hold release.** When the matter closes and the post-matter window elapses, the hold is released and the affected evidence returns to the default retention schedule. Release is a documented event with the matter closure citation and the release approver.

### Reconstructability evidence: the empirical test

PB15 introduces the **Reconstructability Test** as the empirical validation that the framework's evidence claims are true at 30, 60, and 90 days from a given incident. The test is run quarterly per the [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) cadence and produces a measurable result that flows into [Playbook 13 (Six Metrics)](13-six-metrics.md) Metric 3 (Time-to-Evidence).

**The test:**

1. **Select a synthetic or real past incident** from at least 30 days prior. The test target is a specific agent, a specific time window, and a specific reconstruction question (e.g., *"prove what documents the customer-support copilot retrieved on 2026-04-12 between 14:00 and 15:00 UTC for user X"*).
2. **Attempt the reconstruction** using the customer's normal evidence-export procedure. The 60-minute export discipline applies; if the export takes longer, that is a measurable finding.
3. **Score the reconstruction completeness** against the six evidence types: which were present, which were partial, which were missing, which were technically present but inaccessible (cold-tier, redacted, truncated). The scoring is recorded for the quarterly retrospective.
4. **Identify the failure modes** for any missing or partial evidence. Each failure mode enters the [PB18 Post-Incident Hardening](18-post-incident-hardening.md) backlog as a 5-business-day SLA item.

**Operational requirement:** the Reconstructability Test must produce a complete reconstruction (all six evidence types capturable for the test target) at the 30-day horizon and a metadata-complete reconstruction at the 90-day horizon. A customer who cannot complete the Reconstructability Test at 30 days does not satisfy the framework's evidence-retention conformance criterion, regardless of how the original 60-minute export discipline performs.

## Recovery Sequence

PB15 recovery is not an incident-closure activity. It is the periodic restoration of the evidence-retention posture after an event has consumed or strained the customer's evidence-storage capacity, retention budget, or chain-of-custody integrity. Three paths exist, and the choice depends on what the prior event consumed.

### Path 1: Restore default retention after legal hold release

The most common recovery path. The incident or external request has closed, the legal hold has been released, and the affected evidence returns to the default retention schedule.

1. **Confirm matter closure.** The matter's documented closure citation is on file with the customer's legal team; the post-matter hold window has elapsed.
2. **Release the hold.** The retention-management system releases the affected evidence from hold-class retention. The release is logged with the matter citation, the release approver, and the release timestamp.
3. **Resume default retention transitions.** Affected evidence resumes its scheduled warm-to-cold and cold-to-delete transitions per the default schedule.
4. **Update the evidence chain.** The hold's full history (activation, scope, duration, release) is preserved in the customer's evidence-chain log as part of the customer's records-retention standard for the legal-hold mechanism itself.

### Path 2: Restore evidence-store capacity after a major-incident retention surge

An incident has produced a multi-week period of elevated retention (legal hold on multiple agents, payload-tier extension, storage-tier promotion). The evidence store's operating cost has materially elevated; the customer's records discipline now needs to identify which retention is still legally required and which can be released.

1. **Inventory the held evidence.** Document each hold's scope, matter citation, expected duration, and current storage-tier placement.
2. **Identify hold candidates for release.** Holds with closed matters and elapsed post-matter windows are release candidates. Holds with open matters but evidence subsets that no longer require active retention (e.g., metadata-tier retention is sufficient because payload-tier proof has already been produced) are partial-release candidates.
3. **Execute partial or full release** per the legal team's authorization. Each release is logged.
4. **Re-baseline the evidence-store capacity.** The post-release storage footprint is the new operating baseline; if the new baseline still exceeds the customer's planned capacity, the records discipline produces a finding for the customer's records-retention standard review.

### Path 3: Rebuild chain-of-custody integrity after a custody breach

A custody breach has occurred. Examples: unauthorized access to the evidence store, an access-log gap, evidence modification by an unauthorized actor, evidence loss through an operational error. The recovery sequence:

1. **Document the breach.** The breach itself enters the evidence chain with the breach scope, the affected evidence subset, the timeline, and the contributing factors.
2. **Restore from backup where possible.** Evidence stores must have a backup-and-restore discipline that supports this recovery path; the restore returns the affected subset to its pre-breach state.
3. **Re-establish chain integrity.** The restored evidence is re-hashed; the integrity manifest is regenerated; the chain-of-custody log is updated to reflect the restore as a new chain entry with the breach citation and the restore approver.
4. **Engage Legal for materiality determination.** A custody breach on evidence that supports a regulatory or legal matter may itself be a reportable event; the materiality determination is made by Legal in consultation with the IC.
5. **Treat the breach as a [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) candidate if the breach scope suggests deliberate action.** Unauthorized evidence access is among the highest-risk insider scenarios because it directly defeats the framework's proof discipline.

**Approver for recovery actions:** Legal, in consultation with the IC and the Evidence custodian. Platform engineering and detection engineering execute the recovery steps but do not authorize the release of held evidence or the closure of a custody breach. The discipline is the same as the four-eyes principle for high-impact actions in [Playbook 04 (Tool Design)](04-tool-design-is-containment.md): a single role does not have unilateral authority over evidence release.

## Post-Incident Hardening

PB15 hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert AI evidence retention from a storage-policy question into a continuous proof discipline.

### Boundary 1: The Two-Tier Retention Standard codified

- **The customer's records-retention standard documents the metadata and payload retention windows for each of the six evidence types** (A through F) with the rationale, the regulatory and contractual basis, and the default versus extended retention pathways. The standard is published, reviewed annually, and signed off by Legal and the CISO.
- **The retention windows are implementable by the customer's evidence-storage infrastructure** with documented mechanisms for the metadata-versus-payload separation, the default schedule, and the legal-hold extension. A standard that the infrastructure cannot implement is a finding rather than a control.
- **The retention schedule is automated** with no human-in-the-loop required for the default transitions. Manual retention is incompatible with the framework's scale assumptions; manual exceptions exist for the hold mechanism but not for the default schedule.
- **The retention standard is queryable by audit and regulator review** without requiring the customer to engage platform engineering for each request. The standard's published form is the answer to the auditor's question about retention practice.

### Boundary 2: Chain of custody and tamper-evidence

- **Every access to the evidence store is logged** with actor identity, timestamp, query, and access purpose. The access log is itself evidence (Type B for the evidence store) and is retained at the evidence-store-equivalent metadata tier.
- **Every captured evidence artifact has an integrity hash** computed at capture time and included in the [Evidence Export Script Contract](../schemas/evidence-export.spec.md) manifest. The hash is the tamper-evidence anchor; subsequent access can verify that the captured evidence has not been modified.
- **Evidence-store access requires authentication and authorization at the framework's standard discipline** per [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md): no shared service accounts; explicit per-role authorization; rotation cadence documented; access logging end-to-end. The evidence store is itself a Tier-T2 asset and is governed accordingly per the Privilege Matrix discipline.
- **Custody breaches are themselves an incident class** per the Recovery Sequence Path 3 above; the customer's monitoring discipline per [Playbook 11 (Monitoring)](11-monitoring-detection.md) covers the evidence store as a primary surface.

### Boundary 3: The Reconstructability Test cadence

- **The Reconstructability Test runs quarterly** per the [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) cadence. Each quarter selects a synthetic or real past incident, runs the 60-minute export against the present-day evidence store, and scores the reconstruction completeness against the six evidence types.
- **The test target progresses across quarters** to cover the full evidence-type matrix and the full retention-horizon matrix. A quarter might test Type A and Type C at 30 days; the next quarter Type B and Type F at 60 days; the next quarter Type D and Type E at 90 days. The progression ensures that no evidence type and no retention horizon goes untested across the calendar year.
- **The test's failure findings enter the [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) 5-business-day SLA backlog.** A failed reconstructability test is not a retrospective curiosity; it is an actionable finding.
- **The test's success findings update the customer's evidence-conformance posture** per [Playbook 24 (Board-Ready Scorecard)](24-board-ready-scorecard.md) Evidence-domain signals. A consistently-green reconstructability test is a board-defensible indicator that the framework's evidence claims are empirically validated.

### Boundary 4: Disposal discipline

- **Disposal is itself a discipline.** Evidence that has reached the end of its retention window is disposed of through a documented procedure that produces a disposal log entry; the disposal log itself enters the customer's records discipline as part of the chain-of-custody artifact.
- **Disposal is not deletion.** For some regulatory regimes, the disposal of evidence requires cryptographic destruction (key rotation, secure overwrite, hardware destruction) rather than logical deletion. The customer's records discipline names the appropriate disposal method per evidence class.
- **Disposal failure (evidence retained past its disposal date without legal hold) is its own finding.** Customers commonly retain evidence past its disposal date because the disposal mechanism is not automated; the retained evidence is a privacy and storage-cost finding for the records discipline retrospective.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to disposal findings. Disposal-discipline gaps do not wait for the next quarterly review.

## Common Pitfalls

These are the highest-frequency failure modes in evidence retention. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **No payload export within the vendor TTL window** | The team focused on containment and treated evidence capture as an after-hours task | Type A (prompt and response) is gone within 24 to 72 hours; the most-asked post-incident question ("what was the agent told to do?") becomes unanswerable |
| **Payload truncation in the telemetry pipeline** | The telemetry platform's default event-size cap was never reviewed for AI evidence applicability | Type B (tool calls) retains the fact of the call but not the parameters; the post-incident reconstruction can confirm "the agent did something" but not "the agent did this specific thing" |
| **No two-tier retention separation** | The retention policy treats metadata and payload as a single class | The customer pays for payload-class retention to satisfy metadata-class horizons, or under-retains metadata because the payload cost is prohibitive; the tradeoff is reached implicitly rather than by design |
| **No incident-triggered legal hold** | The hold mechanism exists for traditional-IT scope but has not been extended to AI evidence | Default retention schedules continue to run during the investigation; evidence the customer needs in 60 days is gone by 30 |
| **No chain-of-custody discipline on the evidence store** | Evidence storage is treated as a passive archive rather than an active forensic asset | Custody breaches go undetected; access logs are absent or unreliable; the evidence's defensibility in a regulator or legal proceeding is compromised |
| **No tamper-evidence on captured artifacts** | The export script captures content but not integrity hashes | A subsequent claim that the evidence was modified after capture cannot be defended; the integrity question is unanswerable |
| **No Reconstructability Test cadence** | The framework's evidence claims are asserted but not empirically validated | The first time the customer attempts a 30-day reconstruction is during an audit, regulator review, or post-incident retrospective; gaps surface at the moment they are most damaging |
| **Configuration changes not versioned** | Prompt and policy edits are treated as production tuning rather than evidence-producing events | Type E (Configuration Snapshot) becomes a point-in-time artifact rather than a time series; per [Playbook 22 (Drift)](22-model-policy-drift.md) the change-window analysis becomes a reconstruction from memory rather than a forensic export |
| **Redaction policies applied without forensic awareness** | The privacy-redaction pipeline is calibrated for production data rather than for evidence | Payload-class evidence is redacted before the investigation begins; the redaction itself becomes a finding because it destroys evidence at the same time it protects data |
| **Storage-tier transitions during the investigation window** | Evidence migrates from warm to cold to inaccessible during an active investigation | The 60-minute export discipline still produces a successful export technically, but the export retrieves cold-tier data after a multi-hour latency that defeats the operational requirement |
| **Vendor TTL not contracted for AI evidence types** | The vendor's default retention was accepted without review during procurement | Per [Playbook 19 (Build vs Buy)](19-build-vs-buy.md), the customer's evidence claims are bounded by the vendor's retention defaults; framework conformance is not achievable without contractual extension |
| **Cross-system correlation gap** | Type F (Identity and SaaS Audit-Log Correlation) depends on per-provider audit-log retention that the customer does not control | Downstream SaaS retention shorter than the customer's investigation cycle produces a partial-reconstruction outcome; the customer's records discipline includes per-provider retention validation but is often skipped |
| **Disposal discipline absent** | Evidence that should have been disposed of is retained indefinitely | The customer carries privacy and storage-cost exposure that the records-retention standard does not authorize; the retained evidence is itself a finding |
| **No clarity on what to retain past hold release** | The customer's records discipline does not specify whether evidence that supported a closed matter is retained at metadata or payload tier post-release | The default behavior is to retain everything indefinitely (privacy risk) or to delete everything immediately (forensic risk); neither is the disciplined outcome |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-3 Minimum Evidence Set is the discipline this playbook deepens; PB15 is the lifecycle deep-dive on the A-F evidence taxonomy.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clause 2 (Remembers) is the load-bearing clause for this playbook: evidence is data, and the retention discipline applies the same data-store rigor that the framework applies to agent memory.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Two-Tier Retention Standard codification is a Level 2 (Containable) capability; the Reconstructability Test cadence is a Level 3 (Provable) capability; the quarterly evidence-conformance retrospective is a Level 4 (Resilient) capability.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). Evidence preservation is the load-bearing precondition for the materiality determination; without defensible evidence, the customer cannot defend the materiality call regardless of how the call was made.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The full M0-M5 ladder applies unchanged to the operational containment of the underlying incident. PB15's retention-class containment (legal hold, access-restriction tightening, storage-tier promotion, vendor-side hold request, payload-tier hold, cross-system correlation hold) operates in parallel on the evidence store rather than on the agent.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The six-type taxonomy and the 60-minute export discipline; PB15 is the lifecycle deep-dive that operationalizes the taxonomy across the full retention horizon. The Two-Tier Retention Standard, the legal-hold extension mechanism, the chain-of-custody discipline, the tamper-evidence anchor, and the Reconstructability Test are the artifacts PB15 contributes to the framework's evidence discipline.
- **Evidence Export Script Contract:** [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md). The integrity manifest and chain-of-custody attestation specified in the export contract are the operational implementation of PB15's tamper-evidence discipline.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The retention class and the legal-hold scope for each agent's evidence types are AI-BOM fields; the AI-BOM is queryable to determine which agents are in which retention class at any time.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). Evidence-store access is itself a Tier-T2 privilege (per the discipline this playbook establishes); the evidence store's access controls are codified in the Privilege Matrix the same way agent tool access is codified.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook that establishes the privileged-identity lens; PB15 applies the same lens to the evidence store itself.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). The Type C deep-dive (retrieval traces and the seven-component pipeline). PB15 deepens the lifecycle discipline for Type C: corpus version retention, retrieval trace metadata-versus-payload separation, embedding-model version preservation across index rebuilds.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). The evidence store's access discipline follows PB07's credential discipline: no shared service accounts; per-role authorization; documented rotation cadence; end-to-end access logging. The evidence store is a Tier-T2 asset and is governed accordingly.
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). The Type F deep-dive (the output distribution map). PB15 deepens the lifecycle discipline for Type F: per-provider audit-log retention validation, cross-system correlation hold, the destination-class scoping principle applied to evidence retention as well as to incident scope.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). Vendor-managed agents face vendor-driven retention defaults that the customer cannot extend without contractual support. PB10's contracting discipline includes evidence-preservation SLA support that PB15's retention discipline depends on.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). Insider-threat investigations carry the highest chain-of-custody bar in the framework. PB15's access-restriction tightening and the custody-breach Recovery Sequence Path 3 are the evidence-side discipline that PB12 investigations depend on.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). Metric 3 (Time-to-Evidence) is the metric PB15 operationalizes; the Reconstructability Test produces the measurable value that flows into Metric 3 on the customer's quarterly review.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The Reconstructability Test cadence lives in PB14's testing discipline as the quarterly evidence-lifecycle validation; PB15 specifies the test's content, scoring, and follow-through.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to PB15 findings (failed Reconstructability Tests, identified retention gaps, custody breaches, vendor-side retention shortfalls).
- **Playbook 19: Build vs Buy for Agent Controls** ([`playbooks/19-build-vs-buy.md`](19-build-vs-buy.md)). The Proof of Readiness Test includes evidence-export validation; PB19's eight critical procurement questions include configurable retention. PB15 is the post-procurement records discipline that operationalizes the retention capability PB19 validates at procurement time.
- **Playbook 22: Model and Policy Drift** ([`playbooks/22-model-policy-drift.md`](22-model-policy-drift.md)). The change-pipeline event ledger and the Post-Change Configuration Snapshot are the time-axis extensions to Type E that PB15's retention discipline applies; the Two-Tier Retention Standard's payload retention for configuration is calibrated against PB22's typical drift-investigation horizon.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). The Reconstructability Test pass rate, the legal-hold inventory, and the custody-breach incidence are Evidence and Governance domain signals; PB15's reconstructability claim is the board-defensible posture indicator that supports the customer's evidence-conformance claim.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MEASURE 2.7 security and resilience evaluation through documented evidence preservation, MANAGE 4.1 post-deployment monitoring with mechanisms for capturing evidence, and MANAGE 4.3 incident communication that depends on defensible evidence).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook is the direct operational response for **RS.AN-06** action recording with integrity and provenance, **RS.AN-07** incident data and metadata collection with integrity and provenance, and **PR.DS-01** data-at-rest protection applied to the evidence store itself).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses the evidence-preservation precondition that every ASI category's response depends on; without defensible retention, the response disciplines for ASI01 through ASI10 produce findings that cannot be defended in a regulator or legal review).

## The Question to Carry Forward

If a customer or regulator asked next month, *"prove exactly what the agent accessed and where it sent it"*, would you have the evidence, or would it already be gone? Could you produce the prompt-and-response record from 30 days ago? Could you reconstruct the retrieval trace for a specific query at the corpus version in effect on that day? Could you correlate the tool-call ledger entries with the downstream SaaS audit logs for the affected user identity? Could you produce the configuration snapshot from before the most recent prompt edit and prove the integrity of that snapshot through a cryptographic chain rather than an assertion?

The honest answer is the gap. If any of those answers is *"only for last week"* or *"not yet for that specific reconstruction question"*, the Two-Tier Retention Standard, the legal-hold extension mechanism, the chain-of-custody discipline, or the quarterly Reconstructability Test is the corresponding hardening priority.

AI incidents need more than technical fixes; they need proof. The hardest post-incident conversations are not about the response itself; they are about the trust the response can defend in front of a regulator, a customer, or a board reviewing the customer's posture. The framework's job is to make the difference between **a defensible incident** and **an unprovable one** the difference between a passing Reconstructability Test and a failing one, identified quarterly through the framework's testing discipline rather than during the regulator's response window. When the evidence chain produces results the customer trusts, the proof discipline becomes the foundation of the customer's AI risk posture rather than the gap that surfaces when the question is asked.

---

*Source: AI IR Overlay newsletter, Issue #15, "Records, Retention, and Proving What Happened," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
