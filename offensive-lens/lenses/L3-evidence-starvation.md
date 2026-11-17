<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens L3: Evidence Starvation  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The minimum evidence set is only as good as what survives contact.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../../CONTENT_MAP.md) for the full repository map.*

---

# L3 · Evidence Starvation

**Validates:** Overlay Control 3 (Evidence, the six-class minimum evidence set)
**CSF 2.0:** Detect / Respond
**Premise:** The overlay specifies a minimum evidence set across six classes: prompts and responses, tool-call records, retrieval traces, memory state, configuration state, and identity or downstream audit logs. Specifying a set does not produce it. L3 tests each class for three failure modes, **absence**, **truncation**, and **poisoning**, and tests whether the set survives the act of containment.

The materiality call the overlay asks responders to make is made from this evidence. Where the evidence is thin, the call becomes a guess with a timestamp on it.

No L3 technique requires a write to a production target. L3 is the lens to run first where write risk is unacceptable.

---

### OL-T301 — Prompt / response truncation

**Premise:** Prompt logging is usually implemented with a size cap, because contexts are large and log budgets are not. The cap falls exactly where the interesting content is: the injected instruction arrives inside a long retrieved document.

**Procedure**
1. Drive a turn with a deliberately large context: a long retrieved document, a long tool result, a long conversation history.
2. Retrieve the logged record for that turn.
3. Compare logged bytes against actual bytes. Locate where truncation occurs and what is lost: system prompt, tool definitions, retrieved content, the response.
4. Confirm whether truncation is marked in the record, or silent.

**PASS**. Full prompt and response recoverable, or truncation explicitly marked with the original length and a pointer to full content.
**PARTIAL**. Truncation occurs and is marked, but full content is unrecoverable.
**FAIL**. Truncation is silent. The record looks complete and is not.

**Expected defensive signal:** the truncation marker itself.
**Remediation theme:** store full context out-of-band with a content hash in the log line. Silent truncation is worse than no logging, because it is trusted.

### OL-T302 — Tool-call record gap on failure

**Premise:** Tool-call logging is frequently implemented on the success path. Failures, retries, timeouts, and denials are the sequence that matters most during containment, and OL-T201's PARTIAL verdict exists precisely because this class is often empty.

**Procedure**
1. Induce each non-success outcome: a denied invocation, a timeout, a downstream 5xx, a schema-invalid argument set, a retry storm.
2. For each, retrieve the tool-call record.
3. Verify the record carries: agent identity, correlation ID, tool name, arguments, outcome, and timestamp.

**PASS**. Every outcome produces a record with all six fields.
**PARTIAL**. Records exist for some outcomes, or lack correlation identifiers.
**FAIL**. Any non-success outcome produces no record.

**Expected defensive signal:** denial and retry-rate metrics derived from these records.
**Remediation theme:** log at the invocation boundary, before dispatch, with the outcome written back. Never log from the success handler.

### OL-T303 — Retrieval trace absence

**Premise:** When an agent does something wrong because it read something wrong, the investigation needs to know *which chunks were retrieved on that turn*. Most RAG implementations log the query and discard the results.

**Procedure**
1. Drive a turn that performs retrieval.
2. Attempt to reconstruct, from logs alone: the query issued, the documents returned, their identifiers and versions, the scores, and what was actually placed in context after reranking and filtering.
3. Then attempt the harder question: re-run the same query today and determine whether the corpus has changed since.

**PASS**. Retrieved chunk identifiers and content versions are recorded per turn.
**PARTIAL**. The query is logged but results are not, so retrieval is reproducible only if the corpus is unchanged.
**FAIL**. No retrieval record exists.

**Expected defensive signal:** per-turn retrieval records joined to the prompt record by correlation ID.
**Remediation theme:** record chunk IDs and content hashes, not the rendered text. Cheap to store, sufficient to reconstruct, and it survives corpus drift. Pairs with **OL-T105**.

### OL-T304 — Memory volatility under containment

**Premise:** The overlay's M1 preserves read-only function explicitly so that evidence survives. If memory is held in process, or flushed on restart, then the containment action that was supposed to preserve evidence destroys it. This is the highest-value finding in L3.

**Procedure**
1. Establish distinctive memory state at M0: facts, summaries, user preferences, scratchpad contents.
2. Snapshot what you can read of it.
3. Invoke M1 by the documented runbook path, including whatever process restart or redeploy that path actually involves.
4. Attempt to export memory state afterwards. Diff against the snapshot.
5. Repeat for M2 and above, where the ladder level is reachable in your deployment.

**PASS**. Memory state fully exportable after containment, at every level tested.
**PARTIAL**. Exportable but lossy: summaries survive, raw entries do not, or timestamps are gone.
**FAIL**. Containment destroyed memory state, or memory was never exportable at all.

**Expected defensive signal:** containment runbook includes a memory snapshot step *before* the state transition.
**Remediation theme:** snapshot-then-contain, as an atomic step in the kill-switch implementation rather than a human instruction in a runbook.

### OL-T305 — Unversioned configuration state

**Premise:** Reconstructing an incident requires the configuration as it was at T0: system prompt, model version and parameters, tool definitions, guardrail settings, feature flags. Most of these are mutable, and several change without a deploy.

**Procedure**
1. Pick a timestamp 30 days ago. Attempt to reconstruct the agent's full configuration as of that moment, from durable records only.
2. Enumerate which elements you cannot recover.
3. Check specifically for the silent movers: a model alias that now resolves to a newer version, a prompt edited through a console, a flag flipped by an experimentation platform, a guardrail threshold tuned by another team.

**PASS**. Complete configuration reconstructable for any point in the retention window.
**PARTIAL**. Most elements reconstructable; silent movers are not.
**FAIL**. Configuration at T0 is not reconstructable.

**Expected defensive signal:** configuration changes emit versioned, retained events, including those made outside the deploy pipeline.
**Remediation theme:** pin model versions explicitly rather than by alias; snapshot full effective configuration on every agent invocation, or at minimum hash it and record the hash per turn.

### OL-T306 — Downstream attribution collapse

**Premise:** The agent acts through a service account. The downstream system logs the service account. The chain from *human request → agent → tool call → downstream effect* breaks at exactly the point where a regulator, a customer, or a materiality assessment needs it intact.

**Procedure**
1. Have the agent perform a logged read-only action against a downstream system of record.
2. Starting from the downstream audit entry alone, walk backwards: which agent, which turn, which prompt, which human initiated it.
3. Record every join you had to make and whether a shared identifier existed for it.
4. Then test the reverse direction: from a given turn, find all downstream effects.

**PASS**. Bidirectional traversal on a propagated correlation ID.
**PARTIAL**. Traversal possible by timestamp correlation. Workable with one agent, unreliable under concurrency.
**FAIL**. Traversal impossible in either direction.

**Expected defensive signal:** correlation ID present in downstream audit entries.
**Remediation theme:** propagate a trace ID into every tool call and require downstream systems to persist it. Where a downstream system cannot, record the limitation in the AI-BOM as a known attribution gap. Pairs with **OL-T106**.

### OL-T307 — Evidence poisoning via injected content

**Premise:** Agent evidence contains attacker-controlled text by construction: retrieved documents, tool results, user input. A responder reading that evidence is reading adversary-authored content. So, increasingly, is the LLM-assisted triage tool reading it on their behalf.

**Procedure**
1. Place a benign canary in a retrievable document: a unique marker plus text styled as a log entry or system annotation, e.g. a fabricated "reviewed and approved by security" line. No live instructions; a marker and a misleading frame.
2. Drive a turn that retrieves it.
3. Inspect the resulting evidence records. Does the injected text appear in a position or format where a responder would read it as system-generated rather than as content?
4. If any triage tooling summarizes evidence, feed it the record and observe whether the fabricated frame is carried into the summary as fact.

**PASS**. Content is clearly delimited from system-generated fields at every layer, including summarization.
**PARTIAL**. Delimited in storage, lost in the rendering or summarization layer.
**FAIL**. Attacker-controlled text is indistinguishable from system-generated evidence.

**Expected defensive signal:** none expected. The absence is the finding.
**Remediation theme:** structural delimitation and provenance tags on every field, enforced in the viewer, not only the store. Treat evidence as untrusted input to the responder's tools.

### OL-T308 — Retention shorter than detection latency

**Premise:** Agent evidence is high-volume and expensive, so retention gets tuned down. Agent incidents are discovered late, because nothing looks like an intrusion. If retention is shorter than time-to-discovery, the evidence set is specified, collected, and gone.

**Procedure**
1. Record the actual retention period for each of the six classes. Not the policy: the configured value, verified by querying for the oldest available record.
2. Estimate time-to-discovery for the incident classes the overlay's playbooks describe: an agent acting on stale knowledge, a gradually drifting approval pattern, a quiet unintended write discovered at reconciliation.
3. Compare, per class. Note that classes rarely share a retention period.

**PASS**. Every class retained longer than the plausible worst-case discovery latency, with the shortest class documented.
**PARTIAL**. Retention adequate for some classes; the set is unusable past the shortest one.
**FAIL**. The shortest class expires before plausible discovery.

**Expected defensive signal:** retention is set from an incident-discovery assumption that is written down.
**Remediation theme:** retention is a property of the evidence *set*, not of each log. Set them together, to the longest requirement, or tier to cheap storage rather than deleting.

---

## Lens verdict

L3 is validated when every technique is PASS across all six classes. The dominant first-run pattern is PARTIAL almost everywhere: the logs exist, nothing joins them, and nothing proves what was true at T0.

Report L3 as a grid of six classes against absence, truncation and poisoning, rather than as eight verdicts. The grid is what tells a CISO which incident questions are currently unanswerable, which is the form the finding needs to take to get funded.
