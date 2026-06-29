<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 02: Evidence Lives in New Places                         -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The foundational concepts playbook. Three realities of AI evidence: the actor is a workflow, not a workstation; the payload can be language, not malware; evidence is fragile. The framework's entire evidence discipline (the Minimum Evidence Set A-F, the Capture Order, the Two-Tier Retention Standard, the Reconstructability Test) is the practical operationalization of these three realities. Read this playbook first if AI IR is new to you. Re-read it after any incident response whose evidence chain failed.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 02: Evidence Lives in New Places

> *Traditional incident response assumes the crime scene is the endpoint, the network packet capture, the SIEM correlation. AI incidents do not fit that crime scene. The agent acts through legitimate service identities, the harmful instruction may be plain English embedded in a customer email, and the evidence that proves what happened is held in prompt logs, tool-call ledgers, retrieval traces, memory snapshots, configuration histories, and downstream SaaS audit records across at least four different systems. The most common AI IR failure is not the original incident; it is the response team disabling integrations, rotating tokens, redeploying agents, and cleaning corpora before anyone has asked "what exactly did the agent access and what exactly did it do?" By the time the question gets asked, the proof is gone. This playbook establishes the three foundational realities of AI evidence that the rest of the framework operationalizes.*

## Premise

This is the framework's **foundational concepts playbook**. Other playbooks specify operational disciplines (what to do during an incident, how to contain, how to recover); PB02 specifies the **mental shifts** that make those disciplines applicable to AI in the first place. The playbook sits at the start of the framework's reading order alongside [Playbook 01 (The Agent Is a Privileged Identity)](01-agent-as-privileged-identity.md); both are foundational and both are referenced explicitly by every operational playbook.

The structural difference between PB02 and the response-oriented playbooks: PB02's First-Hour Actions are not the operational response to an incident class; they are the **first-hour reflexes** that any AI incident response depends on, regardless of which response playbook the team is running. PB02's Containment Options are not a kill-switch mode selection; they are the **discipline of containment that preserves evidence rather than destroying it**. PB02's Recovery Sequence is not staged tool re-enablement; it is the **return to disciplined IR practice** after an incident has tested the team's evidence-preservation reflexes.

The discipline this playbook establishes is foundational because the entire framework rests on it:

| Framework artifact | PB02 reality it operationalizes |
|---|---|
| [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md), the A-F evidence taxonomy | "The actor is a workflow, not a workstation" plus "the payload can be language, not malware"; both produce evidence types EDR and network forensics cannot capture |
| The Capture Order (Stabilize → Snapshot → Capture) | "Evidence is fragile"; the order exists because routine response actions destroy state in a specific predictable sequence |
| [Playbook 15 (Records, Retention)](15-records-retention.md), the lifecycle discipline | "Evidence is fragile"; the discipline exists because default retention defaults destroy AI evidence faster than the customer's investigation window |
| [Playbook 23 (Logging and Privacy)](23-logging-privacy.md), the multi-stakeholder governance | "The payload can be language"; payload-class evidence carries regulated content, and the multi-stakeholder discipline exists because the evidence and the privacy risk are the same artifact |
| [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md), the Type C deep-dive | "The payload can be language"; poisoned retrieval content is the harmful instruction, and without retrieval traces the input vector is unprovable |
| [Playbook 11 (Monitoring)](11-monitoring-detection.md), the three signal families | "The actor is a workflow, not a workstation"; the signals to detect are action-based, context-based, and capability-based, not endpoint-based |
| [Playbook 22 (Drift)](22-model-policy-drift.md), the change-event forensics | "Evidence is fragile"; drift-investigation depends on pre-change and post-change configuration snapshots that default retention erases |

If the response team has not internalized these three realities, the framework's operational disciplines do not produce defensible outcomes regardless of how thoroughly they are documented. PB02 makes the realities explicit and named so the team can apply them under pressure.

**Mental Model clauses engaged:** all four. The Acts clause depends on Reality 1 (the actor is a workflow); the Remembers and Retrieves clauses depend on Reality 2 (the payload can be language); the Changes clause depends on Reality 3 (evidence is fragile).

**Use this playbook when:** onboarding a new responder to the on-call rotation as part of the [Playbook 16 (Training)](16-training-your-team.md) Curriculum-of-Six prerequisite reading · briefing a senior leader or board member on why AI IR is operationally distinct from traditional IR · responding to "why are we treating AI incidents differently?" from a security team, audit function, or stakeholder · designing the customer's AI IR program from scratch and needing the conceptual foundation that justifies the framework's operational disciplines · running a post-incident retrospective whose findings reveal that the response team did not preserve evidence the way the framework specifies (the corrective is to re-anchor the team on the Three Realities, not just to update the runbook) · reviewing the framework against a new AI deployment pattern (vendor copilot per [Playbook 10](10-vendor-copilots.md), shadow agent per [Playbook 21](21-shadow-ai.md), drift per [Playbook 22](22-model-policy-drift.md)) and verifying that the Three Realities still apply to the new pattern.

## First-Hour Actions

PB02's First-Hour Actions are the **first-hour reflexes** that apply to every AI incident response, regardless of which scenario-specific playbook is running. They are the foundational behaviors that operationalize the Three Realities under operational pressure.

| Minute | Action | Reality engaged |
|---|---|---|
| 0–5 | **Recognize you are responding to an AI-mediated event.** The first reflex is to name the event class: an authorized agent has done something, or has been instructed to do something, or has accessed something, that requires response. Naming the event correctly is the precondition for applying the framework's discipline; misnaming it as a traditional intrusion produces the wrong response sequence | Reality 1: the actor is a workflow |
| 5–15 | **Apply the snapshot-before-rotate reflex.** Before disabling integrations, rotating tokens, updating prompts, or redeploying, snapshot the current state per the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Capture Order. This single reflex is the single largest determinant of whether the incident is investigable in 30 days or operationally invisible | Reality 3: evidence is fragile |
| 15–30 | **Recognize where the evidence is.** Evidence for AI incidents is not on the endpoint or in the network capture; it is in: prompt-and-response logs (Type A) at the model provider or API gateway; tool-call ledgers (Type B) at the application middleware; retrieval traces (Type C) at the vector store or RAG framework; memory snapshots (Type D) at the agent's memory backend; configuration snapshots (Type E) at the deployment pipeline or feature flags; identity and SaaS audit-log correlation (Type F) at the IdP and downstream SaaS audit logs. Naming the evidence locations explicitly is the precondition for the [Evidence Owner](16-training-your-team.md) role's parallel-export discipline | Reality 1 + Reality 2: the actor is a workflow + the payload can be language |
| 30–45 | **Apply the language-as-payload lens.** Read the prompt body, the retrieved content, the agent's response, and the tool-call parameters for the harmful instruction or the unintended action. The payload is not necessarily malicious code; it may be a customer email that contained an injected instruction, a poisoned document in the corpus, a prompt that loosened a refusal boundary, or a tool-call parameter that escalated scope. The payload is plain text that produced harmful action | Reality 2: the payload can be language |
| 45–55 | **Apply the workflow-as-actor lens.** Read the agent's privilege scope, the tool tiering per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md), the identity per [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md), and the write targets per the [Agent Privilege Matrix](../templates/agent-privilege-matrix.csv). The agent is a privileged identity acting through authorized channels; the response scope is determined by what the workflow could do, not by what got compromised | Reality 1: the actor is a workflow |
| 55–60 | **Apply the snapshot-second discipline.** Only after the evidence is preserved do credential rotations, prompt updates, corpus cleanings, or redeployments occur. The discipline is documented in the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Capture Order Step 1 to Step 3; the operational specification lives in [Playbook 15 (Records, Retention)](15-records-retention.md) and [Playbook 23 (Logging and Privacy)](23-logging-privacy.md). The reflex is foundational; the operational discipline is documented elsewhere | Reality 3: evidence is fragile |

**Discipline:** the First-Hour Actions of PB02 are reflexes, not scenario-specific procedures. The reflexes apply regardless of which scenario-specific playbook the team is actually running. The team that has internalized PB02 will apply these reflexes automatically; the team that has not will produce response sequences that defeat the framework's discipline even when the team is following the right scenario playbook on paper.

**Critical rule:** the foundational reflex is **snapshot before rotate**. Every other framework discipline depends on it. A team that snapshots first preserves the optionality to investigate later; a team that rotates first has committed to an investigation conducted on inference.

## The Three Realities of AI Evidence

These are the named principles. Every framework playbook references them, often implicitly. PB02 makes them explicit.

### Reality 1: The Actor Is a Workflow, Not a Workstation

In traditional IR, the actor is a process running on a workstation, a foothold on a server, a session established through a compromised credential. The evidence lives at the endpoint and on the network. EDR catches the binary; the SIEM correlates the lateral movement.

In AI IR, the actor is an **authorized workflow** running under a service identity, calling **legitimate APIs** with **valid OAuth grants** to perform **business-shaped actions** that look indistinguishable from normal automation. The evidence does not live at the endpoint, because the endpoint executed exactly the same kind of API call yesterday under exactly the same identity. The evidence lives in **what the workflow chose to do** and **what authorized the workflow to make that choice**.

This shift produces five operational consequences:

1. **EDR does not detect AI incidents.** Every endpoint signal the EDR would normally flag is absent because the agent is doing authorized work. Detection lives in [Playbook 11 (Monitoring)](11-monitoring-detection.md)'s three signal families (action-based, context-based, capability-based), which observe the workflow's behavior rather than the endpoint's state.
2. **Network forensics does not characterize AI incidents.** The agent's network traffic is API calls to model providers, vector stores, and downstream SaaS systems. The packet capture shows authorized API calls; what made them harmful is in the application layer, not the transport.
3. **Identity-as-actor framing is foundational.** [Playbook 01 (The Agent Is a Privileged Identity)](01-agent-as-privileged-identity.md) is the keystone playbook precisely because the agent's identity is the only stable scoping artifact when every other endpoint-side signal is absent.
4. **Inventory becomes load-bearing.** The customer cannot scope the incident if the customer cannot answer "what agent did this, what tools did it have, what identity did it use, what corpora did it access", and that answer lives in the [AI-BOM](../templates/ai-bom.yaml), not in the asset inventory the EDR feeds.
5. **Downstream audit logs become primary evidence.** [Minimum Evidence Set Type F](../evidence/minimum-evidence-set.md) (Identity and SaaS Audit-Log Correlation) is the load-bearing evidence type for proving what the workflow actually did in the customer's downstream systems.

### Reality 2: The Payload Can Be Language, Not Malware

In traditional IR, the harmful artifact is code. It runs, it persists, it spreads, it exfiltrates. The evidence is the binary, the dropped file, the registry key, the network beacon.

In AI IR, the harmful artifact may be **plain text**. A poisoned document in the corpus per [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md). An injected instruction inside a customer email per [Playbook 06 (Workflow Injection)](06-prompt-injection-workflow.md). A relaxed refusal pattern produced by a prompt edit per [Playbook 22 (Drift)](22-model-policy-drift.md). A tool-call parameter that escalated scope. The evidence is the text itself: the prompt, the response, the retrieved document, the tool-call argument.

This shift produces five operational consequences:

1. **Antivirus and intrusion-detection signatures do not apply.** The "payload" is grammatically correct English (or Spanish, or French, or another language); pattern-matching on signatures produces zero hits on incidents that nonetheless caused material harm.
2. **The prompt-and-response record (Type A) is the primary forensic artifact.** [Minimum Evidence Set Type A](../evidence/minimum-evidence-set.md) is irreplaceable for proving what the agent was told to do and what it produced. Vendor TTLs on Type A logs are the framework's single most fragile retention dimension per [Playbook 15 (Records, Retention)](15-records-retention.md).
3. **Retrieval traces become evidence in their own right.** [Minimum Evidence Set Type C](../evidence/minimum-evidence-set.md) (Retrieval Traces) captures which documents reached the agent's context; the document content is part of the payload, not separate from it. [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md) is the Type C deep-dive.
4. **The output is also payload.** [Playbook 09 (Output Leakage)](09-output-leakage.md) addresses the case where the agent's output (a legitimate response to a legitimate query) carries sensitive content into an inappropriate destination. The output is not "data exfiltration" in the traditional sense; it is authorized communication that happens to carry harmful content.
5. **Logs themselves carry regulated data.** [Playbook 23 (Logging and Privacy)](23-logging-privacy.md) addresses the case that follows from Reality 2: payload-class evidence (prompts, responses, retrieved content, tool parameters) often contains PII, PHI, regulated identifiers, business-confidential content, or credentials. The evidence chain is also a privacy risk; the multi-stakeholder governance discipline exists to reconcile the two.

### Reality 3: Evidence Is Fragile

In traditional IR, evidence is preserved by isolating the endpoint, imaging the disk, and capturing the memory before anything else changes. The discipline is well-rehearsed; the evidence survives the response.

In AI IR, the routine response actions **destroy evidence by default**. Rotating tokens (a sensible containment reflex) destroys the scope record. Updating the system prompt (a sensible drift-correction reflex) destroys Type E configuration evidence. Cleaning the corpus (a sensible poisoning-correction reflex) destroys Type C retrieval evidence. Redeploying the agent (a sensible recovery reflex) destroys the runtime state and may invalidate Type B tool-call correlation identifiers. Disabling the integration (a sensible isolation reflex) may close the customer's access to vendor-held Type A logs entirely.

Every one of those response actions is **operationally correct** in isolation. The reflex they collectively defeat is **snapshot before rotate**. Without that reflex, the customer's incident becomes investigable only on inference rather than on evidence.

This shift produces five operational consequences:

1. **The Capture Order exists because the failure is predictable.** The [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Capture Order Step 1 (Stabilize without rewriting reality) → Step 2 (Snapshot identity and capabilities) → Step 3 (Capture the A-F set) exists because every incident's response team will be tempted to skip to Step 3-equivalents in operational time. The order is named and explicit so the team applies it as discipline rather than relying on judgment under pressure.
2. **The 60-minute export discipline is the load-bearing time budget.** The framework's six-types-in-60-minutes target is calibrated against vendor TTLs that begin to expire as soon as the incident is declared. A team that takes 4 hours to export Type A loses Type A in many vendor configurations.
3. **The Two-Tier Retention Standard exists because default retention is wrong.** [Playbook 15 (Records, Retention)](15-records-retention.md) introduces the metadata-tier and payload-tier discipline because the customer's regulatory and investigation windows do not align with the default retention windows of vendor logs, telemetry pipelines, vector indices, and configuration management systems. Default behavior loses evidence; explicit discipline preserves it.
4. **The Reconstructability Test exists because assertions are insufficient.** [Playbook 15 (Records, Retention)](15-records-retention.md) introduces the quarterly Reconstructability Test because the customer's claim that "we can export the evidence" is only credible when the customer has empirically validated the claim at 30, 60, and 90 days from a target incident.
5. **The chain of custody applies to the evidence store itself.** [Playbook 15 (Records, Retention)](15-records-retention.md) Boundary 2 specifies that every access to the evidence store is itself logged with actor identity, timestamp, query, and access purpose. The fragility extends to the artifacts that prove the original evidence was preserved.

The Three Realities are interconnected. **Reality 1** (the actor is a workflow) determines what evidence types exist. **Reality 2** (the payload can be language) determines what content the evidence contains. **Reality 3** (evidence is fragile) determines how the evidence must be captured, retained, and protected. The framework's operational disciplines flow from these three principles.

## Containment Options

PB02 does not introduce a kill-switch variant. The framework's existing [Kill-Switch Modes](../kill-switches/overview.md) apply unchanged. PB02's containment-equivalent discipline is the **state-preservation containment**: the actions that contain the incident while preserving the evidence that proves its scope.

### State-preservation containment

| Action | Use when | What the Three Realities require |
|---|---|---|
| **Snapshot-first containment** | Any AI incident, by default | Reality 3: evidence is fragile. Snapshot Type A (prompt and response), Type B (tool-call ledger), Type E (configuration) before any token rotation, prompt update, or redeployment. The snapshot is the prerequisite to all other containment actions |
| **Mode M1 (Read-Only) over Mode M4 (Full Disable)** | The harm vector is unclear and the agent has write capabilities that may be amplifying it | Reality 1: the actor is a workflow. Read-Only stops the harmful actions (writes) while preserving the workflow's state and the customer's ability to capture additional evidence as the response proceeds. Full Disable destroys runtime state |
| **Identity-level containment over runtime destruction** | The agent's runtime is not customer-modifiable (vendor copilot, shadow agent, employee-personal-account-hosted) per [Playbook 21 (Shadow AI)](21-shadow-ai.md) | Reality 1: the actor is a workflow. Identity-level containment (OAuth grant revocation, service account disablement, network egress restriction, data-store-level block) contains the workflow's reach without destroying the runtime; runtime destruction may make vendor-held Type A and Type C evidence unreachable |
| **Corpus version preservation before any corpus cleanup** | A retrieval-poisoning incident per [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md) is suspected | Reality 2: the payload can be language. The poisoned document content IS the payload. Cleaning the corpus destroys the evidence of the poisoning instruction; the corpus version snapshot preserves the input vector for investigation |
| **Configuration snapshot before any prompt update or policy tune** | A drift incident per [Playbook 22 (Model and Policy Drift)](22-model-policy-drift.md) is suspected | Reality 3: evidence is fragile. The pre-change configuration is the comparison artifact; updating the prompt to "fix" the drift before snapshotting the pre-change state defeats the change-window forensics |
| **Vendor-side evidence preservation request** | A vendor-managed agent per [Playbook 10 (Vendor Copilots)](10-vendor-copilots.md) is involved | Reality 1 + Reality 3: the actor is a workflow controlled by a vendor; evidence is fragile and held vendor-side. The customer's first containment action includes a vendor-side preservation request under the contracted SLA; failure to request preservation in the first hour may make Type A and Type B evidence unrecoverable when the vendor's TTL expires |

The six actions are complementary. The discipline is to make each containment decision with the Three Realities in mind: which evidence does this containment action preserve, and which does it destroy?

## Evidence Priorities

PB02's evidence discipline is not a new evidence taxonomy; it is the **Three Realities mapped to the existing Minimum Evidence Set A through F**. The mapping makes explicit why each evidence type exists in the framework.

### The A-F Quick Reference

| Code | Evidence Type | Three Realities mapping | Where it lives | Deep-dive |
|---|---|---|---|---|
| **A** | Prompt and Response Record | Reality 2 (payload is language): the harmful instruction and the agent's response are both plain text artifacts | Model provider logs, API gateway logs, application logs. Vendor TTL is the constraint | [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Type A |
| **B** | Tool-Call Ledger | Reality 1 (actor is workflow): the workflow's actions are tool calls; attempted-and-denied calls are evidence of intent | Application middleware, function-calling logs, SaaS audit logs (target side) | [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Type B; [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) tiering context |
| **C** | Retrieval Traces | Reality 2 (payload is language): the retrieved content reaching the agent's context is part of the payload | Vector store query logs, RAG framework traces, knowledge-base access logs | [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md) (the Type C deep-dive) |
| **D** | Memory Snapshot | Reality 1 + Reality 3 (workflow accumulates state; the state is fragile across rotations or cleanups) | Memory backend (Redis, vector DB, app DB), agent framework state | [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Type D; [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) for memory bleed scenarios |
| **E** | Configuration Snapshot | Reality 3 (evidence is fragile): the configuration changes constantly and defaults erase prior versions | Config management system, deployment manifests, feature flags | [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Type E; [Playbook 22 (Model and Policy Drift)](22-model-policy-drift.md) for the change-window forensics |
| **F** | Identity and SaaS Audit-Log Correlation | Reality 1 (actor is workflow): downstream SaaS records the action under the workflow's identity, independent of the agent's own logging | IdP logs (Okta, Entra), SaaS audit logs (Salesforce, M365, ServiceNow), cloud control plane logs | [Playbook 09 (Output Leakage)](09-output-leakage.md) (the Type F deep-dive: the output distribution map) |

### Operationalization

The Three Realities and the A-F taxonomy together produce the framework's operational machinery:

| Operational artifact | Realities-and-types mapping |
|---|---|
| **The 60-minute export discipline** | Realities 1+2+3 together: all six types must be exportable in parallel because all six are time-sensitive (vendor TTLs, payload truncation, index turnover, storage-tier transitions) |
| **The Two-Tier Retention Standard** per [Playbook 15](15-records-retention.md) | Reality 3 specifically: metadata-tier and payload-tier separation calibrates retention to each evidence type's regulatory exposure and forensic value |
| **The chain-of-custody discipline** per [Playbook 15](15-records-retention.md) | Reality 3: the evidence store itself is fragile and requires the same custody discipline as the original evidence |
| **The Three-Layer Logging Model** per [Playbook 23 (Logging and Privacy)](23-logging-privacy.md) | Realities 1+2 together: the workflow produces actions that are evidence and content that is regulated; the layered model calibrates capture to forensic and privacy posture simultaneously |
| **The Reconstructability Test** per [Playbook 15](15-records-retention.md) | Reality 3: assertions about evidence preservation are only credible when empirically validated at 30, 60, and 90 days |

**Operational requirement:** every responder reads PB02 during the [Playbook 16 (Training)](16-training-your-team.md) onboarding sequence before progressing to the Curriculum-of-Six. The Three Realities are the conceptual prerequisite for the Curriculum-of-Six; teaching the moves without the realities produces responders who can execute the operational sequence but cannot recognize when the sequence is the wrong sequence for the surfaced scenario.

## Recovery Sequence

PB02 recovery is not the operational recovery of a specific incident; it is the **conceptual recovery** of the response team's evidence-discipline after an incident has tested or strained it. Three paths exist, calibrated to which kind of strain the incident produced.

### Path 1: Recovery from an evidence-loss event

An incident response has produced evidence loss: a token rotated before scopes were captured, a prompt updated before the prior configuration was snapshotted, a corpus cleaned before the poisoned version was preserved. The recovery is conceptual and operational together:

1. **Run the post-incident competence review** per [Playbook 16 (Training)](16-training-your-team.md) Case C. Distinguish the substrate gaps (the responder could not access the snapshot tool) from the conceptual gaps (the responder did not internalize the snapshot-before-rotate reflex).
2. **Re-anchor the team on the Three Realities.** A conceptual gap is closed not by adding more runbook detail but by re-teaching the foundational principle that produces the reflex. The team-level recovery is to articulate which Reality the failed action violated and to commit to applying it next time.
3. **Run a [Playbook 16 (Training)](16-training-your-team.md) micro-drill within 5 business days** that exercises the specific snapshot-before-rotate reflex that failed in the real incident.
4. **Update the [Playbook 18 (Post-Incident Hardening)](18-post-incident-hardening.md) backlog** with the specific runbook clarifications, access fixes, or training additions that close the gap durably.

### Path 2: Recovery from a "this was traditional IR" misframing

An incident response has been conducted as if the incident were a traditional intrusion: EDR triage, network forensics, endpoint isolation. The framework's AI-specific evidence types were not captured because the response team did not recognize the event as an AI incident. The recovery:

1. **Document the misframing explicitly.** What signals were misread, what evidence types were not captured, what the actual incident class turned out to be.
2. **Re-anchor on Reality 1.** The signal that "the actor is a workflow, not a workstation" is the first reflex that prevents the misframing. The team's recovery is to internalize the recognition shift.
3. **Update the team's intake discipline.** When an event is reported, the first triage question becomes "is this an AI agent doing something?" The question routes the response to the framework rather than to the traditional-IR playbook.
4. **Run a cross-scenario drill** that includes both a traditional intrusion and an AI-mediated event; the drill validates that the team can distinguish the two and route correctly.

### Path 3: Recovery from a "the AI did it" framing

An incident response has produced communication artifacts that anthropomorphize the agent: "the AI hallucinated", "the model decided to", "the agent went rogue". The framing defeats Reality 1's accountability lens (the actor is a workflow under the customer's permissions) and undermines the customer's [Playbook 17 (Communication Techniques)](17-communication-techniques.md) Responsible Reframing discipline.

1. **Document the framings that were issued.** Which messages used anthropomorphizing language, which audiences received them, what the corrective is.
2. **Re-anchor on Reality 1 again** specifically through the accountability lens: the workflow operated under the customer's permissions and access; the customer is the accountable party. The agent is a tool, not an actor.
3. **Apply [Playbook 17 (Communication Techniques)](17-communication-techniques.md) Responsible Reframing** to subsequent messages and to the public-record corrections.
4. **Update the team's communication training** to reinforce the reframing reflex; the customer's [Playbook 16 (Training)](16-training-your-team.md) drills include the reframing pass as a recurring exercise.

**Approver for recovery actions:** Training lead, in consultation with the Incident Commander and the CISO. The conceptual recovery is owned at the IR-program level rather than the individual-responder level; the discipline applies to the team's shared mental model rather than to a single responder's performance.

## Post-Incident Hardening

PB02 hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert the Three Realities from documented principles into operational reflexes the team applies automatically.

### Boundary 1: PB02 in the onboarding curriculum

- **Every new responder reads PB02 before progressing to the [Playbook 16 (Training)](16-training-your-team.md) Curriculum-of-Six.** PB02 is the conceptual prerequisite; the Curriculum-of-Six is the operational application. A responder who learns the operational moves without internalizing the Three Realities will apply the moves in the wrong situations.
- **The onboarding sequence includes an explicit "name the Three Realities" check.** The new responder can articulate Reality 1, Reality 2, and Reality 3 and give an example of each before completing onboarding.
- **The onboarding sequence is documented as part of the customer's training discipline** per the [Playbook 16 (Training)](16-training-your-team.md) onboarding artifact.
- **The PB02 reading is tracked in the team's records discipline** per [Playbook 15 (Records, Retention)](15-records-retention.md); training-discipline evidence supports the customer's PB24 board scorecard claims.

### Boundary 2: The Three Realities as drill-evaluation criteria

- **Every [Playbook 16 (Training)](16-training-your-team.md) monthly micro-drill is evaluated against the Three Realities.** Each drill produces a Realities-application score: did the responder recognize the workflow-as-actor framing (Reality 1)? Did they capture the language-as-payload evidence (Reality 2)? Did they apply the snapshot-before-rotate reflex (Reality 3)?
- **Drill failures are categorized by Reality.** A drill that fails on Reality 3 (the responder rotated before snapshotting) is a different finding from one that fails on Reality 1 (the responder treated the event as a traditional intrusion). The corrective is calibrated to the failure type.
- **The Realities-application score enters the customer's Six Metrics baseline** per [Playbook 13](13-six-metrics.md); a sustained Reality-application deficit is a training-discipline finding rather than an individual-performance finding.

### Boundary 3: The Three Realities applied to framework reviews

- **Every quarterly framework review applies the Three Realities** to new deployment patterns the customer has adopted (new vendor copilots, new shadow-agent classes, new agent-platform integrations). The discipline is to ask: does Reality 1 apply here? Does Reality 2? Does Reality 3? Where the Realities do not fully apply, the customer documents the deviation and the compensating control.
- **The framework review is owned by the customer's [Playbook 20 (Maturity Roadmap)](20-maturity-roadmap.md) maturity owner** and reported on the customer's PB24 board scorecard.
- **Deviations are documented** with the rationale and the compensating control; an undocumented deviation is a finding.

### Boundary 4: The Three Realities applied to communication discipline

- **The [Playbook 17 (Communication Techniques)](17-communication-techniques.md) Responsible Reframing discipline is anchored to Reality 1.** The customer's communication training names the reframing reflex (agent → workflow, model → automation, decided → executed) as the explicit operationalization of Reality 1's accountability lens.
- **Every external communication is reviewed for anthropomorphic framings** before issuance. The review is a five-minute pass on the draft message; the absence of the review is a process finding.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to PB02 findings. Conceptual-discipline gaps do not wait for the next quarterly retrospective.

## Common Pitfalls

These are the conceptual misframings that PB02 exists to correct. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **"This is a traditional intrusion"** | The team's IR training is calibrated to traditional intrusions; the surfaced behavior is mapped to the closest traditional pattern | The framework's AI-specific evidence types (A, B, C, D, E, F) are not captured; the response is conducted on inference; the post-incident retrospective cannot reconstruct what happened |
| **"The AI did it"** | The agent is described as the actor; the workflow framing is absent from the communication | The customer's accountability posture is undermined; the Responsible Reframing discipline from PB17 is defeated; the regulator's expected framing is contradicted |
| **"The payload would have triggered EDR"** | The team assumes endpoint-detection signatures cover the threat | The harmful instruction is plain English in a customer email or a corpus document; no endpoint signature exists; the incident proceeds without detection until downstream impact surfaces |
| **"Let me rotate tokens first, then we'll figure out scope"** | The instinct under containment pressure is to act; the snapshot-before-rotate reflex has not been internalized | The scope record is destroyed; subsequent investigation operates on inference; the customer cannot answer regulator or customer questions about what the agent could access |
| **"We'll just retrain the model" or "redeploy the agent"** | The remediation reflex skips the evidence-capture step | Type E (Configuration Snapshot) for the pre-incident state is destroyed; the change-event forensics from [Playbook 22](22-model-policy-drift.md) cannot identify the trigger; the same incident recurs |
| **"Clean the corpus first"** | The instinct to remove the poisoned document outweighs the discipline of preserving its version | Type C (Retrieval Traces) for the poisoning event is unrecoverable; the customer cannot prove what the agent read and when |
| **"The model provider logs everything for us"** | The team assumes vendor retention is sufficient | Vendor TTLs on Type A are 24 to 72 hours; the customer's investigation cycle is days to weeks; the load-bearing evidence expires before the investigation begins |
| **"The evidence is somewhere; we'll find it when we need it"** | The customer has not run a Reconstructability Test per [Playbook 15](15-records-retention.md) | The first time the customer attempts to reconstruct a 30-day-old incident is during an audit or regulator review; gaps surface at the worst possible moment |
| **"The agent's response was fine; the problem was elsewhere"** | The team treats the agent's output as separate from the payload chain | [Playbook 09 (Output Leakage)](09-output-leakage.md) addresses this exact misframing: the output is part of the payload chain, and authorized outputs can carry sensitive content to inappropriate destinations |
| **"This is a privacy issue, not a security issue"** | The team treats payload-class evidence (PII, PHI, regulated identifiers in logs) as out-of-scope for the security response | The multi-stakeholder coordination from [Playbook 23 (Logging and Privacy)](23-logging-privacy.md) is bypassed; the evidence chain becomes a privacy finding alongside the security incident |
| **"Configuration changes are routine, not events"** | The change-pipeline ledger discipline from [Playbook 22 (Model and Policy Drift)](22-model-policy-drift.md) is not internalized | Drift incidents are misdiagnosed as external attacks or dismissed as routine production variation; the change-window forensics fail because the configuration snapshots do not exist |
| **"Snapshot the screenshot"** | The team produces visual evidence rather than structured exports | Screenshots are not admissible in regulator or legal proceedings; the structured evidence (JSON-formatted A through F) is what the customer's records discipline preserves |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). PB02 establishes the conceptual realities that the four MVO controls (Inventory, Safe Modes, Evidence, Re-Enable) operationalize. The MVO is the operational specification; PB02 is the conceptual foundation.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). The four-clause Mental Model (Acts, Remembers, Retrieves, Changes) is the AI-behavior framing; PB02's Three Realities are the AI-evidence framing. The two are complementary: the Mental Model determines how to govern the agent; PB02 determines how to investigate the agent.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Internalizing the Three Realities is a Level 1 (Aware) capability; applying them in monthly drills is a Level 2 (Containable) capability; passing the framework's time budgets while applying them is a Level 3 (Provable) capability.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). The materiality determination depends on defensible evidence; PB02 establishes the foundational discipline that produces the evidence the materiality call requires.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M0 through M5 ladder is the operational containment surface; PB02's state-preservation containment is the discipline that applies the modes without destroying evidence.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The A through F taxonomy and the Capture Order are the canonical operational specification for PB02's Three Realities. PB02 is the conceptual companion; the Minimum Evidence Set is the operational implementation. Together they form the **concepts-and-operations pair** for the framework's evidence discipline.
- **Evidence Export Script Contract:** [`schemas/evidence-export.spec.md`](../schemas/evidence-export.spec.md). The contract that operationalizes the 60-minute export discipline that Reality 3 (evidence is fragile) requires.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The AI-BOM is the operational substrate for Reality 1 (the actor is a workflow): without the inventory, the response cannot identify the workflow, its identity, its tools, its corpora, or its write targets.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The Privilege Matrix is the tool-tiering substrate for Reality 1: the workflow's actions are tool calls, and the matrix specifies the operational meaning of each tool tier.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone response playbook; PB02 and PB01 are the framework's **two foundational playbooks**. PB02 establishes the conceptual realities; PB01 establishes the operational identity lens.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). The Type C deep-dive; PB03 is Reality 2 (the payload can be language) operationalized for retrieval-poisoning incidents.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The T0/T1/T2 tool tiering is Reality 1 (the actor is a workflow) operationalized for the response's tool-tier-based containment.
- **Playbook 06: Rethinking Prompt Injection as a Workflow Threat** ([`playbooks/06-prompt-injection-workflow.md`](06-prompt-injection-workflow.md)). PB06 is Reality 2 (the payload can be language) operationalized for the workflow-injection input class.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). Credential discipline applies to both the agent's identity (Reality 1) and the evidence store (Reality 3).
- **Playbook 08: Multi-Agent Systems Multiply Blast Radius** ([`playbooks/08-multi-agent-blast-radius.md`](08-multi-agent-blast-radius.md)). Multi-agent scenarios extend Reality 1 (the actor is a workflow) to a workflow-of-workflows scope.
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). The Type F deep-dive; PB09 is Reality 2 (the payload can be language) operationalized for the output-side distribution analysis.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). Vendor copilots extend Reality 1 (the actor is a workflow) to a vendor-controlled-workflow scope and Reality 3 (evidence is fragile) to vendor-held-evidence retention.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The three signal families (action-based, context-based, capability-based) are Reality 1 (the actor is a workflow) operationalized for the detection layer.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). Insider-threat investigations require Reality 3 (evidence is fragile) discipline at the highest standard; the chain of custody is the load-bearing artifact.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). The Six Metrics include Time-to-Evidence (Metric 3) which is Reality 3 (evidence is fragile) operationalized as a measured outcome.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). Pre-production testing validates the substrate that Reality 3 requires (snapshot mechanisms, export pipelines, retention configurations).
- **Playbook 15: Records, Retention, and Proving What Happened** ([`playbooks/15-records-retention.md`](15-records-retention.md)). PB15 is Reality 3 (evidence is fragile) operationalized as a lifecycle discipline. The Two-Tier Retention Standard, the chain-of-custody discipline, the tamper-evidence anchor, and the Reconstructability Test all flow from Reality 3.
- **Playbook 16: Training Your Team for AI Incidents** ([`playbooks/16-training-your-team.md`](16-training-your-team.md)). PB16's onboarding sequence includes PB02 as the conceptual prerequisite; PB16's monthly drills evaluate Three-Realities application as part of the drill scoring. PB02 and PB16 together form the **concepts-and-training pair**: PB02 establishes the realities; PB16 trains the team to apply them.
- **Playbook 17: Communication Techniques for AI-Involved IR** ([`playbooks/17-communication-techniques.md`](17-communication-techniques.md)). The Responsible Reframing discipline is Reality 1 (the actor is a workflow) operationalized for the communication track. The reframing pattern (agent → workflow, model → automation, decided → executed) names Reality 1 in the message text.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to PB02 findings (conceptual misframings, Three-Realities application failures, communication-reframing gaps).
- **Playbook 19: Build vs Buy for Agent Controls** ([`playbooks/19-build-vs-buy.md`](19-build-vs-buy.md)). The Proof of Readiness Test validates the platform's support for the operational disciplines that the Three Realities require: can the platform produce Type A, Type B, Type C, Type E evidence in the customer's investigation window? PB19's eight critical procurement questions are Realities-driven.
- **Playbook 20: AI IR Maturity Roadmap** ([`playbooks/20-maturity-roadmap.md`](20-maturity-roadmap.md)). The level progression depends on PB02's conceptual foundation; an organization that has not internalized the Three Realities cannot achieve Level 2 capability regardless of how much operational machinery exists.
- **Playbook 21: Shadow AI** ([`playbooks/21-shadow-ai.md`](21-shadow-ai.md)). Shadow AI extends Reality 1 (the actor is a workflow) to undocumented workflows; the Discovery Snapshot is Reality 3 (evidence is fragile) operationalized for the discovery moment.
- **Playbook 22: Model and Policy Drift** ([`playbooks/22-model-policy-drift.md`](22-model-policy-drift.md)). Drift is Reality 3 (evidence is fragile) operationalized for the change-event forensics; the change-pipeline event ledger is the time-axis equivalent of Type B for the customer's own change pipeline.
- **Playbook 23: AI Logging and Privacy in a Multi-Stakeholder World** ([`playbooks/23-logging-privacy.md`](23-logging-privacy.md)). PB23 is the multi-stakeholder governance discipline that follows from Reality 2 (the payload can be language): payload-class evidence carries regulated content, and the privacy posture and the forensic posture are the same artifact.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). The board's Governance and Evidence domain signals depend on the customer's PB02 discipline; consistently strong PB02 application is a board-defensible posture indicator.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (PB02's Three Realities support the conceptual framing for MAP 1.1 intended-use documentation, MEASURE 2.7 security and resilience evaluation, and MANAGE 4.1 post-deployment monitoring).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (PB02 supports the CSF 2.0 functions' AI-specific application: the Three Realities are the conceptual basis for why IDENTIFY, PROTECT, DETECT, RESPOND, and RECOVER operate differently for AI agents than for traditional systems).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (PB02's Realities map across all 10 ASI categories: Reality 1 underlies ASI02 Tool Misuse, ASI03 Identity Abuse, ASI07 Inter-Agent Communication; Reality 2 underlies ASI01 Goal Hijack, ASI06 Memory Poisoning, ASI09 Trust Exploitation; Reality 3 underlies the evidence-preservation discipline required to respond to any ASI category).

## The Question to Carry Forward

If a security analyst on your team encountered an AI-mediated event tomorrow morning, would they recognize it as an AI incident rather than a traditional intrusion? Would they snapshot the agent's identity, configuration, and tool-call history before rotating credentials or updating the prompt? Would they recognize that the harmful payload might be plain English in a customer email rather than a malicious binary? Would they capture Type A through Type F evidence in 60 minutes rather than improvising the export from scratch? Would they communicate the incident as "an authorized automation behaved incorrectly under investigation" rather than "the AI hallucinated"?

The honest answer is the gap. If any of those answers is *"only the senior responder would"* or *"maybe, depending on the scenario"*, the conceptual foundation is not yet operational. PB02 is the discipline that closes the gap; reading it once is not enough. The Three Realities become operational when the team applies them reflexively rather than reaches for them under deliberation.

Evidence lives in new places. The team that has internalized PB02 will look in those places automatically. The team that has not will look on the endpoint, find nothing, and spend the next two weeks reconstructing what happened from partial logs while the regulator and the customer wait for an answer. The framework's job is to make the difference between **the team that knows where to look** and **the team that does not** an empirical question rather than a hopeful one. When the Three Realities are operational, every other framework discipline becomes executable.

---

*Source: AI IR Overlay newsletter, Issue #2, "Evidence Lives in New Places," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
