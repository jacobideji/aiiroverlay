<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 22: Model and Policy Drift                               -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The change-event forensics playbook. Drift is the incident class that starts inside the system, looks like an external attack from the outside, and gets misdiagnosed when change-window evidence is not preserved. The response is treating every material AI change as a candidate incident with snapshot, canary replay, and layered rollback, not treating every change as routine production tuning.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 22: Model and Policy Drift

> *AI applications are always evolving. Models are retrained or upgraded by vendors. System prompts and instruction sets get edited. Policies, safety filters, and moderation layers are tuned. Retrieval parameters shift. Tool schemas change. Index pipelines rebuild. Memory and context windows widen. Each change is intended to improve the system. Each change can also produce a behavior shift the operator did not predict: tool invocation frequency increases, retrieval surfaces different documents for identical queries, sensitive-data boundaries relax, previously-consistent refusals disappear. The drift is rarely advertised. The data leak, the runaway automation, or the spurious external-attack signature shows up first. This playbook is the change-event forensics discipline that lets the response distinguish a real attack from a regression introduced by the customer's own release pipeline.*

## Premise

Traditional incident response assumes the question is *what got in?* Drift incidents flip that assumption: the change came in through the deployment pipeline that the customer's own team operates, often with full audit trail, often signed off as routine. The behavior the customer is now seeing is the system doing exactly what it was told to do; the problem is that the new instruction is not the instruction the security team or the business owner thought they were giving.

This makes drift operationally distinct from the rest of the framework's incident classes in four ways:

| Aspect | Standard AI incident | Drift incident |
|---|---|---|
| Origin | External adversary, compromised supply-chain element, insider misuse | Customer's own change pipeline (model upgrade, prompt edit, policy tune, retriever parameter, index rebuild) |
| Audit trail at time of detection | Usually adversarial or absent | Usually present, often signed-off as routine |
| Surface symptoms | Often match a known threat-model shape (prompt-injection patterns, credential abuse, retrieval poisoning) | Look like a regression, a new attack, or a quality issue depending on which component changed and what the operator expects |
| Time-to-detection | Hours to days, sometimes weeks | Often weeks (post-release performance shift), and sometimes the change-event forensics is the only way to identify the cause |

Drift is not a single attack vector. It is a category of failure modes that can manifest as:

- **Increased tool-invocation frequency**, where the agent has decided some action is now appropriate that previously was rare. This can produce excess external email, excess CRM writes, or excess code commits without the kind of pattern a malicious-actor scenario would produce.
- **Altered retrieval results for identical queries**, where a corpus index rebuild, an embedding-model change, or a top-k parameter shift has changed which documents reach the agent. This can produce silent confidentiality failures per [Playbook 09 (Output Leakage)](09-output-leakage.md) when newly-reachable documents contain sensitive content, or silent quality failures when previously-reachable documents are no longer surfaced.
- **Relaxed enforcement of sensitive-data boundaries**, where a moderation-layer tune, a safety-filter version change, or a system-prompt edit has loosened a refusal pattern. The agent now responds to requests it previously declined.
- **Loss of previously-consistent refusal patterns**, where the same prompts that triggered safety responses last week produce policy-aligned responses this week. This is the symptom most likely to be mistaken for an adversarial bypass; it is often a routine vendor model update.
- **Tool-schema or connector behavior changes**, where a downstream API has changed and the agent's plan succeeds in unexpected ways. The agent's tool call returns successfully but the downstream action is different from what the previous schema produced.

Most drift is small and operationally invisible. Some drift is small and produces compounding harm over weeks. A small number of drift events are immediate and material. The response framework's job is to make all three detectable within a defensible window and traceable to a specific change for safe rollback.

The biggest operational problem with drift is not the drift itself; it is the misdiagnosis cost when the change-window evidence has not been preserved. A drift incident that gets investigated as an external attack burns response capacity, escalates falsely, sometimes triggers disclosure protocols inappropriately, and ultimately fails to identify the actual cause because the change-window evidence has expired. This playbook's job is to make change-window evidence load-bearing rather than incidental.

**Mental Model clauses engaged:** *Changes* (primary, because drift is fundamentally a change-management incident class); *Acts* (when drift produces increased tool invocation or new write patterns); *Retrieves* (when drift originates in the retrieval layer per the corpus rebuild or top-k tune cases); *Remembers* (when memory or context-window changes shift cross-session behavior).

**Use this playbook when:** a recent model upgrade, prompt edit, policy tune, retriever change, index rebuild, tool-schema change, or memory configuration change has been deployed and behavior has shifted · the agent's behavior has changed and the security team is being asked whether it is an attack · [Playbook 11 (Monitoring)](11-monitoring-detection.md) detection-signal volumes for the agent have shifted significantly in either direction in the past 24 to 72 hours · a vendor has announced a model version change for an agent the customer depends on · the [PB14 Drift Canary pack](14-testing-for-agent-failure-modes.md) produces a fail or a significant boundary delta against a known baseline · [Playbook 13 (Six Metrics)](13-six-metrics.md) values for the agent shift outside their tolerance band without an obvious incident · downstream business owners report that *"the AI changed"* without a corresponding security or operational event · investigation under [Playbook 01](01-agent-as-privileged-identity.md) traces the surfaced behavior to a configuration delta rather than an external trigger.

## First-Hour Actions

The first hour of a drift response has one job that distinguishes it from other incident classes: **establish whether the surfaced behavior is drift, an attack, or both, before any cleanup begins**. The instinct to roll back the last release before snapshotting the current state is the most damaging shortcut in this playbook. The rollback is in scope; the rollback is not the first step. The order of operations is the entire response.

### The 60-minute drift triage

| Minute | Action | Owner |
|---|---|---|
| 0–5 | **Confirm the surfaced behavior is unexpected, not just unfamiliar.** Compare against the documented operating envelope for the agent (the AI-BOM entry, the most recent canary baseline, the [Six Metrics tolerance band](13-six-metrics.md)). A behavior that is new to the responder but inside the documented envelope is a documentation gap, not a drift incident. Proceed only if the behavior is genuinely outside the documented envelope. | Incident Commander |
| 5–20 | **Snapshot the current post-change state before any rollback.** Capture the agent's current configuration: system prompt and instruction set as deployed, policy and moderation configuration, retriever parameters (top-k, recency weighting, embedding model version, reranker configuration), tool schemas and connector definitions, memory configuration, context window setting, model identifier and version pin. This is the **Post-Change Configuration Snapshot** and is the load-bearing evidence artifact for the rest of the response. The snapshot is captured even when the team intends to roll back within the next 30 minutes, because the post-change state is the artifact that proves what was deployed when the behavior shift was observed. | Platform engineer + Detection engineer |
| 20–35 | **Define the change window.** Identify the deployment events in the relevant systems (CI/CD pipeline, vendor dashboard, configuration management database, policy management system, retriever admin console) that occurred between the last known-good behavior baseline and the surfaced behavior shift. Record the *who*, the *what*, and the *when* for each change candidate. The change window is the time bound for the rollback and the evidence-collection scope. | Platform engineer + Change management owner |
| 35–50 | **Stabilize behavior without destroying state.** Where the agent's behavior is causing measurable harm (data exposure, runaway tool invocation, broken business workflow), shift to [Mode M1 Read-Only](../kill-switches/overview.md) by stripping write tools, or to [Mode M3 Tool Tiering](../kill-switches/overview.md) by disabling the specific tools showing the drift, or to the new **M3-Drift variant** by rolling back the specific component (model version, prompt, policy, retriever parameters) that the change-window evidence identifies as the most likely source. The mode choice depends on the surfaced behavior and the change-window analysis; the discipline is to contain before rollback completes. | Incident Commander + Platform engineer |
| 50–55 | **Walk the [Six Triage Questions](../triage/six-questions.md) with one extension.** Q1 (tools), Q2 (write targets), Q3 (identity), Q4 (memory), Q5 (safe mode), Q6 (evidence plan) follow standard discipline. Add a seventh: *what specifically changed in the deployment pipeline between the last known-good baseline and now, and which of those changes is most likely the source of the behavior shift?* The answer determines the rollback order in the Recovery Sequence. | Incident Commander + Platform engineer |
| 55–60 | **Convene the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) if drift has touched customer data, regulated data, external recipients, or financial actions.** Drift incidents often have a tail of latent exposure that started when the change shipped, which may be days or weeks before detection. The convening protocol applies regardless of containment mode, because the disclosure window may have started before the drift was observed. | Incident Commander |

**Discipline:** the Post-Change Configuration Snapshot is the chain-of-custody anchor for a drift response. Without it, the post-incident analysis cannot prove what configuration produced the observed behavior. The instinct to roll back first and document later is the most damaging shortcut in this playbook. Snapshot first; roll back second.

**Critical rule:** preserve the change-pipeline logs, the deployment timestamps, the approver identities, and the per-change configuration deltas for every candidate change in the window. Where the change pipeline retains these for less than 30 days, capture what is reachable now; the next rollback or pipeline cleanup may eliminate the security team's ability to reach those logs.

## Containment Options

Drift containment combines the framework's [Kill-Switch Modes](../kill-switches/overview.md) with a new **M3-Drift** variant that scopes containment to the specific component identified by the change-window analysis. The choice depends on whether the drift source has been identified and whether the harm vector justifies broader containment.

### Mode mapping for Drift

| Mode | Use when | What changes |
|---|---|---|
| **M0 Observe (continued monitoring)** | The behavior shift is inside the documented operating envelope after canary replay validates the new state, the change-window evidence is preserved, and no harm vector is identified | Full logging continues; the agent's AI-BOM entry is updated to record the new baseline; the Drift Canary pack is updated to include the new boundary if appropriate |
| **M1 Read-Only** | The drift source has not been identified and the agent has write capabilities that may be amplifying the harm | Strip write tools from the agent's tool set; the agent continues to serve reads while change-window analysis and rollback proceed |
| **M2 Approvals Required** | The drift is identified but business need requires continued operation while validation runs | Every tool call routes to a human approver before execution; the approver sees the proposed action and the destination |
| **M3 Tool Tiering** | The drift is producing excess invocations of a specific tool class or excess writes to a specific destination class | Disable the affected tools or destination categories; keep unaffected tools live for continued business value during the analysis window |
| **M3-Drift** (this playbook) | The change-window analysis has identified a specific component as the most likely drift source, and that component can be reverted without disabling the agent's other capabilities | Roll back the identified component (model version pin, system prompt version, policy configuration version, retriever parameters, tool schema, memory configuration) to the last known-good state while preserving the agent's other capabilities. Validate behavior against the Drift Canary pack after rollback. If the canary passes, the agent returns to M0 with the rolled-back component in place. If the canary fails or partially fails, escalate to M3 Tool Tiering or M4 Full Disable while the drift source is investigated further. |
| **M4 Full Disable** | Drift is producing immediate material harm, the source has not been identified after 30 minutes of change-window analysis, or rollback of the identified candidate has not restored expected behavior | Hard stop while change-window forensics complete. Snapshot first per the First-Hour Actions sequence, then disable |

### The M3-Drift discipline

M3-Drift is the surgical variant of M3 Tool Tiering for the case where the cause of the behavior shift is a specific changed component rather than a specific risky tool. The discipline:

1. **Identify the most-likely-source component** from the change-window analysis. Score candidates by recency (how recently was the change deployed relative to the behavior shift), by component-class plausibility (does the component class plausibly produce the surfaced symptom, e.g., a retriever change is a more plausible source for retrieval-pattern drift than a tool-schema change), and by change-magnitude (a model version upgrade has a larger plausible behavior surface than a single prompt-line edit).
2. **Revert the identified component to the last known-good state** while preserving the agent's other capabilities. For model version drift, this is a version pin or model-ID rollback. For prompt drift, this is a system-prompt or instruction-set revert. For policy drift, this is a moderation-configuration revert. For retriever drift, this is a parameter or embedding-model revert. For tool-schema drift, this is a connector or schema revert. For memory drift, this is a memory-configuration revert.
3. **Validate against the Drift Canary pack** after the rollback. The canary is the empirical test that the rolled-back state produces expected behavior; without the canary, the rollback's effect is asserted rather than measured.
4. **If the canary passes, return to M0** with the rolled-back component in place and the post-change configuration logged as a failed-validation candidate for the post-incident hardening. If the canary fails, the rollback either missed the source or the source is multi-component; escalate to M3 Tool Tiering (broader containment) while continuing the change-window analysis.

The M3-Drift variant is the structural parallel to the existing M3 variants: M3-RAG scopes to the retrieval layer; M3-Delegation Cap scopes to inter-agent delegation depth; M3-Workflow scopes to a content channel feeding the agent; M3-Vendor scopes to a vendor-managed deployment; M3-Output scopes to a specific output channel or destination class. M3-Drift scopes to a specific recently-changed component while pre-change state is restored.

## Evidence Priorities

The Drift evidence set extends the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A-F with explicit emphasis on the **Post-Change Configuration Snapshot** and the **change-pipeline event ledger** as the time-axis artifacts that drift response requires beyond the standard incident-class evidence.

### Evidence priorities ranked for Drift

| Code | Evidence Type | Priority | Why it matters |
|---|---|---|---|
| **E** | Configuration Snapshot (extended: **Post-Change** and **Pre-Change** snapshots) | **Critical** | The two-snapshot pattern is what makes drift forensics possible. The Post-Change snapshot captures the state that produced the observed behavior; the Pre-Change snapshot is the reference point from the last known-good baseline. The diff between the two is the evidence that drives the rollback decision. Without one or both snapshots, the response is reconstructing what changed from after-the-fact deployment records, which is materially less reliable. |
| **B** | Tool-Call Ledger | **Critical** | Drift symptoms often manifest as changed tool-call patterns (frequency, target, parameters). The pre-drift baseline tool-call ledger and the post-drift ledger together produce the behavior-shift evidence that quantifies the drift's operational impact. Without the comparison window, the response is asserting that behavior changed rather than measuring it. |
| **A** | Prompt and Response Record | **High** | The behavior-shift artifact. The same prompts that produced expected responses in the pre-drift baseline should produce the same responses in the rolled-back state; deviation is the drift's surface signature. The Drift Canary pack (see Post-Incident Hardening) is the curated prompt set that operationalizes this evidence type for drift specifically. |
| **C** | Retrieval Traces | **High if the agent is RAG-based** | Drift in the retrieval layer (corpus rebuild, embedding-model change, top-k parameter shift, reranker change) is one of the most common drift surfaces in 2026 production agents. The pre-drift retrieval trace and the post-drift retrieval trace for the same query reveal which documents shifted into or out of the agent's reachable context. |
| **D** | Memory Snapshot | **High if memory or context-window configuration changed** | Memory or context-window drift is among the most operationally subtle drift surfaces because the change affects only multi-turn or cross-session behavior. The memory snapshot pre- and post-drift is the only evidence that quantifies the actual cross-session bleed produced by the change. |
| **F** | Identity and SaaS Audit-Log Correlation | **High** | The downstream record of what the drift produced in customer-controlled systems. Even when the agent's own logs are noisy or incomplete, the SaaS audit logs record what reached the downstream systems (Salesforce, M365, ticketing, code repos, cloud control plane). Drift that produced excess writes, new tool calls, or unexpected destinations is reconstructable from the downstream audit trail. |

### Drift-specific captures

In addition to A through F:

- **The change-pipeline event ledger** for the change window: every deployment event in the relevant systems (CI/CD pipeline, vendor model-version-change notifications, configuration management database, policy management system, retriever admin console, index pipeline jobs, memory store administrative actions) with timestamps, change-IDs, approver identities, and per-change configuration deltas. This is the time-axis equivalent of Type B for the customer's own change pipeline; it is what makes the rollback decision a forensic decision rather than a guess.
- **The Drift Canary baseline result set** captured immediately before the change window began. The canary baseline is the empirical reference; the post-drift canary run is the comparison. The two together quantify the drift surface.
- **The Six Metrics values** ([Playbook 13](13-six-metrics.md)) for the agent across the change window. The metrics that move (Time-to-Activate, Time-to-Safe-Mode, Time-to-Evidence, the AI-BOM currency metric, the M3 readiness metric, the M5 controlled re-enable metric) localize the drift impact to specific operational capabilities.
- **The model and policy version chain** for the affected agent: not just the current version but the deployment sequence over the past 90 days. The chain converts an isolated drift event into a time series that often reveals slow drift accumulation rather than a single triggering change.

**Operational requirement:** the full Drift Evidence Capture must complete within **90 minutes** of the surfaced behavior shift confirmation. The Post-Change Configuration Snapshot and the change-pipeline event ledger are the two artifacts the response cannot recover later; they must be captured before any rollback. The pre-change snapshot and the baseline canary results are pre-positioned per the Post-Incident Hardening discipline, not captured during the incident response itself.

## Recovery Sequence

Drift recovery is the controlled, validated return to a known-good baseline. The sequence is layered because drift sources are often unclear at the start of the response, and an undisciplined rollback can introduce new drift while attempting to undo the original drift. Five steps, in order.

### Step 1: Stabilize behavior

Before the rollback sequence begins, the agent is in M1 Read-Only, M2 Approvals Required, M3 Tool Tiering, M3-Drift, or M4 Full Disable per the Containment Options analysis. Stabilization is the precondition for safe rollback; an agent that continues to write during the rollback window may produce a partial-state inconsistency where some downstream systems reflect the pre-rollback behavior and others reflect the post-rollback behavior.

### Step 2: Validate the change-window evidence

The Post-Change Configuration Snapshot is in evidence; the Pre-Change Configuration Snapshot from the last known-good baseline is retrieved from the customer's configuration store; the change-pipeline event ledger for the change window is captured. The Incident Commander confirms that the rollback target is the actual last known-good state, not an arbitrary recent state. The check is non-trivial: a customer with weekly releases over a 90-day drift accumulation may need to roll back to a baseline that is older than the most recent operational reference point.

### Step 3: Layered rollback

The rollback is sequential, starting with the lowest-blast-radius components and proceeding to higher-blast-radius components. The canonical layer order:

1. **Tool policies and connector configurations.** Tier classifications, allowlists, approval rules, write-target restrictions. These are the components closest to the agent's action surface and the easiest to roll back without rebuilding state.
2. **Retriever parameters and reranker settings.** Top-k, recency weighting, similarity thresholds, reranker model. These affect which documents reach the agent's context but do not require corpus or index changes.
3. **System prompt and instruction-set version.** The agent's stated mission, role, and behavioral constraints. Rolling back the system prompt is a low-cost reversion that often resolves drift originating in a prompt edit.
4. **Policy and moderation configuration.** Safety filter version, moderation thresholds, refusal pattern configuration. Often deployed independently of the system prompt but produces overlapping behavior effects.
5. **Memory and context-window configuration.** Memory scope, retention, context window size. Rolling back memory or context configuration may require care if the agent has accumulated memory under the post-change configuration that does not transfer cleanly to the pre-change configuration.
6. **Tool schemas and connector definitions.** If a downstream API has changed and the customer's connector definition has been updated to match, the rollback may need coordination with the connector owner.
7. **Retrieval index and corpus version.** Corpus refreshes are deployment events; rolling back to a prior corpus version is feasible only if the customer's index pipeline preserves prior versions. Where index rollback is not feasible, the rollback discipline shifts to retriever-parameter constraints that approximate the prior reachability.
8. **Model version pin.** The highest-blast-radius rollback. Where the change is a vendor model version change, the rollback may require coordinating with the vendor (vendor pinning or model-ID downgrade). Vendor-managed agents per [Playbook 10 (Vendor Copilots)](10-vendor-copilots.md) follow the M3-Vendor discipline for this layer.

Each layer's rollback is followed by an immediate canary replay (Step 4) before proceeding to the next layer. The discipline is to identify the smallest rollback set that restores expected behavior; a multi-layer rollback that succeeds in restoring behavior but cannot localize the drift source has not produced a defensible post-incident-hardening artifact.

### Step 4: Canary replay between layers

After each layer's rollback, the [Drift Canary pack](14-testing-for-agent-failure-modes.md) runs against the agent in its current state. The canary measures:

- **Refusal-pattern boundaries** that were known to hold in the pre-change baseline. Drift that loosened refusals shows as canary fails for these probes.
- **Retrieval-pattern boundaries** that were known to hold for sensitive corpora. Drift that surfaced new documents shows as canary fails for these probes.
- **Tool-invocation patterns** for benign and high-risk action requests. Drift that loosened tool invocation shows as canary fails for these probes.
- **Workflow-completion patterns** for representative business tasks. Drift that broke task completion shows as canary fails for these probes.

The canary's result determines whether the rollback proceeds (canary fails at the current layer; continue rolling back additional layers), pauses (canary partially passes; investigate the partial pass before continuing), or completes (canary fully passes at the current layer; the rollback's last layer is the drift source).

### Step 5: Controlled re-enable

After the canary passes at the rolled-back state, the agent re-enters M0 per the [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) discipline. The re-enable sequence:

1. **Update the AI-BOM** with the rolled-back configuration as the current operating baseline. Record the drift event with its change-window evidence, the identified source, and the rollback layer that resolved it.
2. **Update the Drift Canary pack** to include the boundary that the drift event surfaced as the closure for that boundary's coverage gap.
3. **Communicate the resolution** to the agent's downstream business owners, the change-pipeline owner (so the failed change candidate enters the customer's change-management retrospective), and the [Playbook 18 Post-Incident Hardening](18-post-incident-hardening.md) backlog for the 5-business-day SLA review.
4. **Re-enable write capabilities incrementally**, starting with the lowest-blast-radius write tools, with monitoring per [Playbook 11](11-monitoring-detection.md) covering the re-enable window.

**Approver for full re-enable:** CISO or designated Incident Commander, in consultation with the change-pipeline owner. The platform engineer who deployed the original change does not unilaterally approve the rolled-back state (which may produce the appearance of bypassing change-management discipline) or the failed-change retrospective (which may underweight the drift's operational cost).

## Post-Incident Hardening

Drift hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert AI change-management from a release-pipeline question into a continuous incident-response discipline.

### Boundary 1: Change control treated as release management

- **Every model upgrade, system-prompt edit, policy tune, retriever parameter change, tool-schema update, index pipeline rebuild, and memory configuration change requires a formal change request** with documented intent, scope, expected behavior delta, rollback plan, and approver identity. The change request is the pre-event artifact that the change-window analysis depends on.
- **The change-request standard distinguishes routine, minor, and major changes** with proportional review depth. A vendor model version upgrade and an index pipeline rebuild are major changes regardless of how small the diff appears at the policy or configuration layer; a wording fix on a system prompt is a minor change. The standard prevents major changes from sliding through as routine releases.
- **The change-request log is queryable by date range** so the change-window analysis in the First-Hour Actions can complete in 15 minutes rather than 60. A change-request system that does not support fast time-range queries does not satisfy the discipline.
- **Vendor-managed agents per [Playbook 10](10-vendor-copilots.md) require vendor change-notification SLAs** in the customer's contract. Vendor model version upgrades that arrive without advance notice are themselves a contractual finding for the customer-vendor relationship, regardless of the drift impact.

### Boundary 2: Versioning, snapshotting, and pre-change state preservation

- **The pre-change configuration is captured automatically** by the change pipeline before each deployment. The pre-change snapshot is stored with retention that covers the customer's expected drift-detection window (90 days is a reasonable starting point; longer for regulated environments where post-incident discovery may extend further).
- **The pre-change snapshot is locatable from the change request** so the rollback discipline does not require manual reconstruction. The snapshot's stored location is a field on the change request itself.
- **Every component class has a versioning standard:** system prompts and instruction sets in version control with tags; policy and moderation configuration in version control with tags; retriever parameters in declarative configuration with version pinning; tool schemas in version control; memory configuration in declarative configuration; index and corpus versions retained with content-addressable identifiers per [Playbook 03 (RAG Forensics)](03-rag-knowledge-base-forensics.md); model version pins documented in the AI-BOM. The standard prevents the "I do not know which version we were running last Tuesday" failure mode that defeats drift forensics.
- **The retention window for change-pipeline logs matches the customer's regulatory and operational disclosure windows.** A 30-day change log retention is incompatible with a 90-day drift-detection cycle.

### Boundary 3: The Drift Canary pack

- **A curated set of prompts and test cases that probe sensitive boundaries, workflow triggers, refusal logic, retrieval-pattern boundaries, tool-invocation patterns, and workflow completion** is maintained as the agent's empirical drift-detection baseline. The canary pack is owned per agent (or per agent class for fleets) and updated as part of the Post-Incident Hardening discipline after each drift event.
- **The canary runs automatically against every change** that touches the agent's configuration, prompt, policy, retriever, tools, memory, or model. The pipeline does not advance the change without a canary pass; canary fail blocks deployment by default and requires explicit override (with sign-off and risk-acceptance) to proceed.
- **The canary runs on a quarterly cadence regardless of change activity** per the [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) testing discipline. The quarterly run catches drift that crosses the per-change threshold individually but accumulates across changes.
- **The canary's boundary coverage is reviewed after each incident** for completeness. A drift event that the canary did not catch is a canary coverage gap; the boundary that the drift exposed is added to the canary as a closure for that gap. This is the operational closure rule for the canary pack: every incident either confirms the canary's coverage or expands it.

### Boundary 4: Detection, monitoring, and drift-class signals

- **PB11 (Monitoring) Family 1 (action-based signals)** extended to detect tool-invocation-frequency shifts outside the documented tolerance band. The signal is a frequency-class delta rather than a specific tool call; drift surfaces in aggregate behavior rather than individual events.
- **PB11 Family 2 (context-based signals)** extended to detect retrieval-pattern shifts: which documents are surfaced for benchmark queries, which corpora are reachable, which embedding distances are inside or outside the previously-observed envelope.
- **PB11 Family 3 (capability-based signals)** extended to detect refusal-pattern shifts: which prompts now produce policy-aligned responses that previously produced refusals, and vice versa. Refusal-pattern shifts are a leading indicator of drift in policy or moderation configuration.
- **PB13 (Six Metrics)** values reviewed weekly for tolerance-band excursions. A metric that drifts outside its tolerance band is a drift indicator independent of any specific incident.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to drift findings. Each drift event produces canary additions, change-control retrospective items, and PB11 signal extensions that enter the 5-business-day SLA closure window.

## Common Pitfalls

These are the highest-frequency failure modes in drift response. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Rolling back before snapshotting the post-change state** | Standard IR reflex (restore service) applied to a change-event scenario | Post-incident analysis cannot prove what configuration produced the observed behavior; the drift source is identified by inference rather than evidence; the change-management retrospective is incomplete |
| **Treating drift as an external attack and escalating accordingly** | Behavior shift symptoms often match known threat-model shapes (relaxed refusals look like prompt-injection bypass, increased writes look like credential abuse, retrieval shifts look like corpus poisoning) | Response capacity burns on attack investigation; disclosure protocols may be triggered inappropriately; the actual cause (a routine release the customer's own team deployed) is identified late or not at all |
| **Treating drift as routine production tuning and skipping forensics** | The opposite reflex: dismissing the behavior shift as expected variation | The drift source is not localized; subsequent drift events compound; the customer's change-management process never gets the feedback loop the retrospective produces |
| **No pre-change configuration snapshot** | Change pipeline captures the post-change state but not the pre-change baseline | Rollback discipline degrades from "restore from snapshot" to "reconstruct from memory plus partial deployment logs"; drift forensics become unreliable beyond the most recent change |
| **No change-pipeline event ledger or retention shorter than the drift-detection window** | The change-pipeline owner optimizes for storage cost rather than forensic readiness | Drift that accumulates over weeks or months cannot be traced to specific change events; the rollback becomes a guess at which baseline is appropriate |
| **No Drift Canary pack** | Canary discipline is treated as a pre-production testing concern (PB14) rather than a continuous-monitoring concern | Drift detection depends on downstream business owners noticing behavior shifts, which is the slowest possible detection channel and produces detection latency measured in weeks |
| **Canary pack that does not get updated after incidents** | The closure rule for canary coverage is not enforced | The same drift class recurs because the canary still does not probe the boundary that the previous incident exposed |
| **Canary pack that blocks the pipeline by default but with override that gets used routinely** | Override discipline degrades because canary fails are treated as deployment friction rather than safety signal | The canary becomes ceremonial; deployments proceed past canary fails; the canary's coverage becomes inversely correlated with the drift's impact |
| **Rollback at the wrong layer** | The change-window analysis identifies the wrong candidate as the source; rollback at that layer does not restore expected behavior | The response continues to roll back additional layers and may overcorrect, producing new drift while attempting to undo the original drift |
| **Vendor model version change without notification** | The customer's contract with the vendor does not include change-notification SLAs | Drift surfaces with no warning; the customer's change-window analysis identifies no candidate from the customer's own change pipeline; the response stalls until the vendor's release notes are correlated externally |
| **No version pinning at the model layer** | The customer's deployment uses the vendor's "latest" model identifier rather than a pinned version | Every vendor model update is a silent deployment in the customer's environment; the change pipeline shows no event but the behavior shifts; drift response is reduced to canary-driven rollback because version pinning is not available |
| **Memory or context-window changes deployed without canary coverage** | Memory and context-window changes are treated as configuration tuning rather than architectural changes | Cross-session behavior drift is identified only by downstream business owners reporting that "the agent forgot things" or "the agent remembers things it should not"; canary coverage was missing |
| **Confusing drift with insider threat or external attack** | Surface similarity in symptoms (unexpected agent behavior, possible policy bypass, possible data exposure) | Investigation defaults to [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) or [Playbook 01 (Privileged Identity)](01-agent-as-privileged-identity.md) discipline when the actual scenario is a change-event regression; HR and Legal may be engaged inappropriately; the change-pipeline owner is not engaged when they are the principal source |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-4 Controlled Re-Enable is the discipline the layered rollback in this playbook operationalizes for change-event scenarios; MVO-1 Inventory's AI-BOM is the artifact the post-rollback state updates.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clause 4 (Changes) is the load-bearing clause for this playbook: AI changes are software releases, with deployment discipline, rollback plans, and version control as preconditions for safe operation.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Drift Canary discipline is a Level 3 (Provable) capability; weekly Six Metrics review and quarterly canary cadence are Level 4 (Resilient) capabilities.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). Drift incidents that surface latent regulatory-data exposure trigger the convening protocol; the disclosure window may have started weeks before the drift was observed if the change accumulated.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The full M0-M5 ladder applies to drift response. **M3-Drift** is the new variant introduced by this playbook: M3 Tool Tiering scoped to the specific recently-changed component identified by change-window analysis while pre-change state is restored.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The Post-Change and Pre-Change Configuration Snapshots are Type E extensions; the change-pipeline event ledger is the time-axis equivalent of Type B for the customer's own change pipeline.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The model version pin, prompt version, policy version, retriever parameters, tool schemas, memory configuration, and last-known-good baseline are AI-BOM fields. Drift response updates the AI-BOM with the rolled-back state as the new operating baseline.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). Tool schemas reference the Privilege Matrix; a tool-schema drift event may require Privilege Matrix updates as part of the post-rollback discipline.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook that drift response builds on; drift events that affect identity scopes flow back through PB01's discipline.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). Retrieval-layer drift (corpus rebuild, embedding-model change, top-k tune) shares the 90-minute Freeze-the-World sequence and the seven-component pipeline forensics; PB22 operates on the time axis and PB03 operates on the corpus axis.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). Tool-schema drift response uses the T0/T1/T2 tiering discipline; the post-rollback Privilege Matrix update closes the change loop.
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). Drift that produces silent confidentiality failures (corpus rebuild that surfaces previously-unreachable sensitive documents, policy tune that relaxes refusals) flows through PB09's response discipline once the drift cause is identified.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). Vendor-managed agents face vendor-driven drift (vendor model version changes) that the customer cannot pin against without contractual support. PB10's contracting discipline includes vendor change-notification SLAs that drift response depends on.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The detection rules that surface drift live here; PB22's change-event forensics depend on PB11's instrumentation. PB22 extends PB11 with explicit drift-class signals: tool-invocation-frequency shifts, retrieval-pattern shifts, refusal-pattern shifts.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). Six Metrics values are reviewed weekly for tolerance-band excursions; drift indicators surface in the metrics independent of any single incident. The Six Metrics are the leading indicator for drift detection at the operating-program level.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The Drift Canary pack lives in PB14's testing discipline as the empirical drift baseline; PB22's response sequence runs the canary between rollback layers. PB14 and PB22 together form the **pre-production-testing / continuous-monitoring pair** for drift: PB14 catches drift before deployment; PB22 catches drift after deployment with rollback discipline.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to drift findings; each drift event produces canary additions, change-control retrospective items, and PB11 signal extensions that enter the hardening backlog.
- **Playbook 21: Shadow AI** ([`playbooks/21-shadow-ai.md`](21-shadow-ai.md)). Shadow agents typically lack any of the four hardening boundaries this playbook defines (no formal change control, no pre-change snapshots, no canary pack, no drift-class detection signals). Discovered shadow agents that migrate to governance acquire PB22's discipline as part of the migration; shadow agents that do not migrate are durably at higher drift risk.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). Drift Canary readiness, change-pipeline event-ledger retention, and the post-rollback discipline are Recovery and Governance domain signals. Drift events resolved within the canonical sequence, drift events resolved at the rollback layer with the smallest blast radius, and drift events surfaced by the canary versus by downstream business owners are board-defensible posture indicators.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports MANAGE 4.1 post-deployment monitoring, MANAGE 4.2 continual improvement integrated with change management, MEASURE 2.7 security and resilience evaluation, MEASURE 4.2 trustworthiness over time).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook is the direct operational response for **ID.RA** risk assessment of change events and **PR.PS** platform security configuration management applied to AI agents; supports DE.CM continuous monitoring on the drift-detection dimension, RS.MA incident management for change-event regressions, RC.RP recovery sequence for layered rollback).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses the change-event vector for **ASI06 Memory & Context Poisoning** when memory or retrieval changes produce drift, and **ASI10 Rogue Agents** when drift is the dominant 2026 form of rogue-agent emergence: unintentional drift accumulation rather than reward hacking or goal collusion).

## The Question to Carry Forward

If your model, prompt, policy, retriever, tool schema, memory configuration, or index pipeline changed overnight, could you identify the change and restore expected behavior by the end of the day? Could you snapshot the post-change state before any rollback? Could you locate the pre-change configuration from your change-management system in under 30 minutes? Could you query the change-pipeline event ledger by date range for the past 90 days? Could you run a curated canary pack against the agent and quantify the drift surface before any cleanup begins? Could you roll back layer by layer with canary validation between each layer?

The honest answer is the gap. If any of those answers is *"not yet"* or *"only for the most recent change"*, the change-control discipline, the snapshot retention, the canary pack, or the layered-rollback sequence is the corresponding hardening priority.

Not every incident comes from an outside threat. Many start with well-meaning changes inside AI systems, deployed through the customer's own pipeline, signed off as routine. The response framework's job is not to suppress AI change velocity, because the velocity is the source of the legitimate AI value the business will need. The job is to make the difference between **a routine change** and **a drift event** the difference between a green canary and a red canary, identified at the deployment boundary rather than weeks later through downstream business reports. When the change pipeline produces canary results that the security team trusts, the drift surface becomes a managed lifecycle rather than a recurring surprise.

---

*Source: AI IR Overlay newsletter, Issue #22, "Managing Model and Policy Drift in AI Systems: A Forensic Approach to Change Events," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
