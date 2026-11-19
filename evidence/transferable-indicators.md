<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Transferable Indicator Set                                                            -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Six indicator classes (TI-1–TI-6) derived from the evidence you already hold. What can leave your organization, and what must not.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Transferable Indicator Set

> The [Minimum Evidence Set](minimum-evidence-set.md) answers *what happened here*. This file answers *what can I tell anyone else*, which is a different question with a different answer.

## Premise

An agent incident is rarely confined to one organization. A poisoned document sits in a vendor's knowledge base that forty customers index. An injection string that works against one orchestrator works against the next one built on the same framework. A compromised tool definition ships to everyone who installed it.

Yet nothing in this framework, through v0.38.0, said what an organization could hand to a peer, an ISAC, or a vendor's security team. The six evidence types are scoped to the responding organization: they are what you capture to reconstruct your own incident and defend your own materiality call. None of them is shareable as captured, because every one of them contains either regulated content or details specific to your deployment.

A **transferable indicator** is the part of an evidence artifact that survives both tests: it is specific enough that another organization can match against it, and stripped enough that sharing it discloses nothing it should not.

This set is distinct from two things the framework already names. It is not the **Indicators** field in [Playbook 08](../playbooks/08-multi-agent-blast-radius.md), which lists internal detection signals for multi-agent threat patterns, nor the three **signal families** in [Playbook 11](../playbooks/11-monitoring-detection.md), which are what your own monitoring watches. Those face inward. These face outward.

## The derivation rule

Every transferable indicator is derived, never authored:

1. **It comes from a named evidence type.** If no evidence type produces it, it is not an indicator, it is a theory.
2. **It is reduced per [Playbook 23](../playbooks/23-logging-privacy.md).** Payload-tier content does not leave. Where the payload *is* the indicator, the hash leaves and the content stays, which is the standard discipline for sensitive indicators and is why the [Evidence Export Script Contract](../schemas/evidence-export.spec.md) already emits a `sha256_hash` per artifact.
3. **It carries external labels.** The [ATLAS](../offensive-lens/crosswalks/mitre-atlas.md) technique and [OWASP ASI](../crosswalks/owasp-agentic-top-10.md) entry it evidences, so the receiver can route it without translation.
4. **It names the lens technique that proves you could produce it.** An indicator class you cannot generate is a gap in your instrumentation, not an absence of adversary activity.

## The Six Indicator Classes (TI-1–TI-6)

### TI-1 Injection content

**Derived from:** Type A Prompt and Response Record, field `user_prompt`; for indirect injection, the document body reached via Type C `documents_retrieved[].doc_id` and `version`.

**Transferable:** the SHA-256 of the normalized injection string, the normalization method, the delivery channel, and the structural shape, for example an imperative instruction embedded in a document styled as a system annotation.

**Stays behind:** the string itself when it contains user or customer content. `user_prompt` is payload-tier under PB23 and does not leave on the strength of an incident alone.

**Labels:** ASI01 Agent Goal Hijack · `AML.T0071` False RAG Entry Injection for the indirect case, `AML.T0094` Delay Execution of LLM Instructions where the instruction was held for a later turn.

**Lens gate:** [OL-T301](../offensive-lens/lenses/L3-evidence-starvation.md) Prompt / response truncation. If your Type A record truncates, the injection may be the part that was dropped, and you cannot produce this class at all.

### TI-2 Poisoned corpus document identity

**Derived from:** Type C Retrieval Traces, fields `corpus_id` and `documents_retrieved[].doc_id` with `version`.

**Transferable:** the corpus identifier where it is a shared or vendor-supplied corpus, the document identifier, the document version, and the SHA-256 of the document content. For a public or vendor corpus, these are the most directly actionable indicator the framework produces, because the receiver can check their own index for the same document.

**Stays behind:** the document body if it carries customer content, and `query`, which is a user utterance and payload-tier.

**Labels:** ASI04 Agentic Supply Chain Vulnerabilities and ASI06 Memory & Context Poisoning · `AML.T0070` RAG Poisoning.

**Lens gate:** [OL-T303](../offensive-lens/lenses/L3-evidence-starvation.md) Retrieval trace absence, and [OL-T105](../offensive-lens/lenses/L1-inventory-drift.md) Retrieval-corpus drift for whether `version` means anything.

### TI-3 Memory entry

**Derived from:** Type D Memory Snapshot, field `contents_summary`.

**Transferable:** the SHA-256 of the entry, its scope as `per-user` or `shared`, whether it was imperative or declarative, and the turn offset between the write and the first execution. That offset is the operationally useful number: it tells a receiver how far back their own retention has to reach.

**Stays behind:** the entry text whenever memory scope is per-user, which makes it personal data in most regimes.

**Labels:** ASI06 Memory & Context Poisoning · `AML.T0080.000` Memory, specializing `AML.T0080` AI Agent Context Poisoning.

**Lens gate:** [OL-T304](../offensive-lens/lenses/L3-evidence-starvation.md) Memory volatility under containment. If memory does not survive the transition to a safe mode, this class does not exist for you, and [OL-T401](../offensive-lens/lenses/L4-recovery-reentry.md) is then also unanswerable.

### TI-4 Tool-call signature

**Derived from:** Type B Tool-Call Ledger, fields `tool_name`, `result_status`, `denied_reason`, and the ordered sequence across lines.

**Transferable:** the ordered tool-name sequence that effected or attempted the harm, the parameter *shape* rather than its values, and the denied-then-succeeded pattern where one exists. Denied calls are included because the Minimum Evidence Set already treats them as evidence of intent, and a denial sequence is often more portable than a success: it describes what the adversary tried against a control, not what your particular deployment allowed.

**Stays behind:** `parameters` values and `result_payload_summary`, both of which carry business data.

**Labels:** ASI02 Tool Misuse and Exploitation and ASI05 Unexpected Code Execution · `AML.T0053` AI Agent Tool Invocation.

**Lens gate:** [OL-T302](../offensive-lens/lenses/L3-evidence-starvation.md) Tool-call record gap on failure. A ledger that records only successes cannot produce the denial sequence, which is the half of this class that transfers best.

### TI-5 Grant and scope delta

**Derived from:** Type F Identity and SaaS Audit-Log Correlation, field `identity_principal`; and Type E Configuration Snapshot, fields `tool_definitions` and `system_prompts[].hash`.

**Transferable:** the scope or permission set before and after, expressed in the provider's own vocabulary such as an OAuth scope string, the grant mechanism, and whether the change fell inside an approved change window. Scope strings are provider-defined and therefore portable: another organization using the same SaaS can check for the same grant.

**Stays behind:** the principal identifier itself, and any tenant-specific object identifier.

**Labels:** ASI03 Identity and Privilege Abuse · `AML.T0083` Credentials from AI Agent Configuration.

**Lens gate:** [OL-T305](../offensive-lens/lenses/L3-evidence-starvation.md) Unversioned configuration state. Without versioned configuration there is no *before*, and a delta with one side missing is not an indicator.

### TI-6 Agent provenance as seen downstream

**Derived from:** Type F, fields `target_system`, `action`, `target_object_class`, and `correlation_id`.

**Transferable:** how the agent presented itself to the downstream system, whether the downstream record attributes the action to the agent or to a human, and the class of object acted on rather than the object. This is the indicator that tells a peer whether their own downstream logs would even show an agent at work.

**Stays behind:** `source_ip`, `target_object`, and `correlation_id`, which is specific to your export.

**Labels:** ASI03 Identity and Privilege Abuse and ASI10 Rogue Agents · `AML.T0073` Impersonation.

**Lens gate:** [OL-T306](../offensive-lens/lenses/L3-evidence-starvation.md) Downstream attribution collapse. If the receiving system records a human principal where an agent acted, this class is unproducible and the incident is unattributable in both organizations.

## The retention gate on all six

[OL-T308](../offensive-lens/lenses/L3-evidence-starvation.md) Retention shorter than detection latency applies to every class above. An indicator you could have derived from an artifact that has already aged out is not a sharing failure, it is a retention failure, and the two have different owners: see [Playbook 15](../playbooks/15-records-retention.md).

This is the single most common reason an organization has nothing to contribute. The agent incident is detected at day 40 and the Type A retention window was 30 days.

## What this set is not

- **It is not a sharing protocol.** No TLP marking, STIX shape or MISP object is specified here. That is deliberate: the taxonomy has to be settled before the serialization, and specifying a wire format for indicator classes nobody has yet produced would be specifying the easy half.
- **It is not an attribution aid.** None of these classes identifies an actor. Per [Playbook 17](../playbooks/17-communication-techniques.md), attribution to external actors without evidence is a forbidden phrase in this framework's incident communications, and nothing here changes that.
- **It is not a conformance requirement.** An organization at Maturity Level 3 that shares nothing is still at Level 3. Producing transferable indicators is a contribution to others, and the framework does not grade you on it.

## Where it sits in the response arc

Deriving indicators is a **Closure** activity, after the materiality call and alongside [Playbook 18](../playbooks/18-post-incident-hardening.md)'s hardening list. It is the last thing you do with the evidence, and it is the first thing another organization's **Detection** layer consumes: a received TI-2 becomes a corpus check, a received TI-4 becomes a [Playbook 11](../playbooks/11-monitoring-detection.md) Family 1 rule.

That is the whole point of the set. Your Closure is somebody else's Preparation.

## Related

- **[Minimum AI Evidence Set](minimum-evidence-set.md)**: the six evidence types every class above is derived from, and the capture order that determines whether they exist.
- **[Evidence Export Script Contract](../schemas/evidence-export.spec.md)**: the field names cited throughout, and the manifest whose `sha256_hash` is the mechanism behind every hash-only indicator here.
- **[Playbook 23: AI Logging and Privacy](../playbooks/23-logging-privacy.md)**: the payload-tier and metadata-tier split, and the data-minimization filter that decides what stays behind.
- **[Playbook 15: Records and Retention](../playbooks/15-records-retention.md)**: the retention windows that determine whether an indicator still exists to derive.
- **[Playbook 11: Monitoring That Truly Detects Agent Incidents](../playbooks/11-monitoring-detection.md)**: the three signal families, which are the inward-facing counterpart and the consumer of indicators received from others.
- **[Playbook 18: Post-Incident Hardening](../playbooks/18-post-incident-hardening.md)**: the Closure step this derivation belongs to.
- **[Offensive Lens](../offensive-lens/README.md)**: the L3 lens, whose techniques are the gates on all six classes. Of the six techniques that v0.38.0 found had no OWASP counterpart, four — OL-T301, OL-T302, OL-T303 and OL-T308 — are the gates named above. The lens's evidence-starvation axis has no weakness class to answer to because it does not describe a weakness; it describes whether you can say anything useful afterwards.

---

*Source: AI IR Overlay framework synthesis, by Jacob Ideji. Introduced in v0.39.0 to close the cross-victim gap: the framework specified what to capture and what to prove, and not what to pass on.*
<https://www.linkedin.com/in/jacobideji/>
