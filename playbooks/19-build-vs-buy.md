<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 19: Build vs Buy for Agent Controls                      -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The procurement-time playbook. The platform decision determines what incident response is possible. Buying for features that look good in demos and discovering during an incident that the platform cannot move to read-only mode, cannot export the evidence, or cannot trace a tool call to a SaaS audit log is the single most expensive procurement failure in 2026 AI deployments.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 19: Build vs Buy for Agent Controls

> *Procurement is the upstream decision that determines what every downstream incident response playbook in this framework is able to execute. Buy a platform that supports the [MVO conformance criteria](../framework/01-minimum-viable-overlay.md) and the response disciplines in PB01, PB03, PB06, PB09, PB10, PB11, and PB18 become executable. Buy a platform that does not, and the framework's controls turn into commitments the platform cannot honor. The Build vs Buy decision is therefore not a vendor-selection question; it is an incident-readiness question.*

## Premise

Procurement of AI agent platforms in 2026 is dominated by feature-driven evaluation: which platform has the best reasoning model, which has the smoothest integration with enterprise SaaS, which has the most impressive demos, which has the strongest brand. Each of those evaluation axes addresses what the platform can do in normal operation. None of them addresses what the platform can do during an incident, when the relevant questions become operationally narrow: can we stop it, can we prove what happened, and can we recover safely.

The framework's response-side playbooks (PB01 keystone response, PB03 RAG forensics, PB06 workflow injection, PB09 output leakage, PB10 vendor copilots, PB11 monitoring, PB18 post-incident hardening) all assume the underlying platform can do specific things: activate read-only mode in under 10 minutes, export prompt and tool-call logs within 60 minutes, correlate tool calls to SaaS audit records with traceable identifiers, configure data retention to match the customer's regulatory window, restrict retrieval to specific corpora, and produce the evidence set the customer's General Counsel may need for the [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) call. If the platform cannot do these things, the response playbooks cannot do these things either.

This playbook addresses the procurement-time discipline that makes the response playbooks executable. It specifies the **eight critical procurement questions** that distinguish incident-capable platforms from feature-impressive ones, the **60-minute Proof of Readiness Test** that operationalizes the questions, the **Build vs Buy Decision Matrix** that names which capabilities are typically appropriate to buy and which are typically appropriate to build, and the **post-procurement hardening** discipline that converts the readiness test's findings into contractual commitments before the platform reaches production.

**Mental Model clauses engaged:** *Acts* (the platform's containment capability), *Retrieves* (the platform's retrieval governance), *Remembers* (the platform's memory configuration), *Changes* (the platform's change-control discipline). All four clauses inform what the procurement evaluation must verify.

**Use this playbook when:** procuring a new AI agent platform · drafting an RFP or vendor evaluation for an AI deployment · evaluating an existing AI platform's incident-readiness posture against this framework · preparing for a vendor pitch meeting where the customer needs to know what to ask · running an annual platform review or contract-renewal evaluation · choosing the governed path for a discovered shadow agent per [Playbook 21](21-shadow-ai.md)'s migrate decision · responding to procurement's request for security input on an AI tool the business has already selected · building the customer's internal "approved AI platforms" list.

## First-Hour Actions

The first hour of an AI platform evaluation has one job: **run the Proof of Readiness Test against the candidate platform**. If the test surfaces gaps, the procurement decision is informed by evidence rather than by vendor assurance. If the test cannot be run because the platform does not yet have a trial environment, that is itself a procurement signal.

### The 60-minute Proof of Readiness Test

The test is a four-step operational drill executed against the candidate platform in its trial or evaluation environment. Each step is timed; each produces a documented artifact. The test substitutes empirical evidence for vendor demonstration.

| Minute | Action | Owner | Artifact produced |
|---|---|---|---|
| 0–10 | **Activate read-only mode.** Through the platform's documented procedure (admin console, API, configuration flag), put a representative agent into a state where it can serve read queries but cannot execute write tool calls or send external communications. Capture the actual elapsed time from the moment the decision is made to the moment the read-only state is in effect. If the platform requires a vendor support ticket to activate this mode, the test stops; the platform fails the readiness bar. | Platform engineer (customer-side) | Read-only mode activation log with timestamps |
| 10–25 | **Export tool-call and retrieval logs for the past hour.** Through the platform's documented procedure (admin export, API call, log download), retrieve the agent's actions from the last 60 minutes including prompt and response records, tool-call ledger with parameters and results, retrieval traces with document IDs and version stamps, and configuration state at the time of action. Capture the actual elapsed time and the completeness of the export against the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A-F. | Detection engineer (customer-side) | Evidence export bundle with completeness checklist |
| 25–45 | **Identify the most-frequently-retrieved document.** Using the retrieval traces exported in the previous step, determine which corpus document the agent retrieved most often in the past hour, with version stamps and similarity scores. This is the C1 sub-type from [Playbook 03 Type C extended](03-rag-knowledge-base-forensics.md). If the platform's retrieval logging does not surface this, the platform cannot support PB03 forensics. | RAG / Platform engineer (customer-side) | Top-retrieved-document report with provenance |
| 45–55 | **Produce a one-page executive update from the exported evidence.** Following the [Playbook 24 Executive Incident Snapshot Template](24-board-ready-scorecard.md), summarize what the agent did in the past hour, what it accessed, where its outputs reached, and which evidence types are missing or incomplete. The update is the artifact the customer's CISO would hand the General Counsel during a real incident. | Incident Commander (customer-side) | One-page executive update |
| 55–60 | **Document the gaps and the timing.** What did the platform do well? What was missing? What took longer than the framework's drill-measured targets (10 min TTA, 60 min evidence export per [framework/01](../framework/01-minimum-viable-overlay.md))? Each gap is a procurement finding that becomes a contractual requirement, a build-side commitment, or a deal-breaker. | Incident Commander | Gap register with procurement implications |

**Discipline:** the Proof of Readiness Test is the **operational substitute for vendor demonstration**. A platform that performs well in a vendor's demo but fails the 60-minute test is a platform that will fail during a real incident. The test's value is not in the success criteria; it is in the failure modes the test surfaces. Platforms that fail one or more steps may still be procurement candidates, but the gaps become either contractual remediation items, customer-side build commitments, or explicit risk-acceptance decisions documented for the board.

**Critical rule:** **Do not run the Proof of Readiness Test in production.** Use a trial environment, a sandbox tenant, or a non-production agent. The test is destructive to normal operation by design (read-only mode interrupts the agent's writes; full evidence export may stress the platform's API quotas). If the vendor cannot provide a non-production environment for the test, the absence of that environment is itself a finding.

## Build vs Buy Decision Matrix

Containment of procurement risk maps to a decision matrix that names which capabilities are typically appropriate to buy from a vendor platform, which are typically appropriate to build in-house, and which require a hybrid approach.

### Decision matrix by capability class

| Capability | Typical recommendation | Why |
|---|---|---|
| **Foundation model and inference infrastructure** | Buy | Capital-intensive, capability-evolving, undifferentiated for most adopters; commercial providers (OpenAI, Anthropic, Google, AWS Bedrock, Azure OpenAI, etc.) reach scale and capability the customer cannot match. |
| **Standard logging pipelines and structured storage** | Buy | Mature SaaS category (Datadog, Splunk, Elastic, OpenTelemetry collectors). Building introduces operational cost without competitive advantage. |
| **Identity provider and OAuth grant management** | Buy | Existing IdP investment already covers this; AI agents inherit the identity discipline from the IdP. Building introduces credential-management gaps the IdP already solves. |
| **Policy engine for approvals and allowlists** | Buy | OPA, Cedar, vendor-native policy engines all reach maturity that custom approval logic cannot match. Building introduces enforcement gaps. |
| **Connector security and credential or token management** | Buy | Vault, AWS Secrets Manager, vendor-native credential stores all solve this. Building introduces rotation, audit, and recovery gaps. |
| **Baseline monitoring and anomaly detection** | Buy (with custom rules) | SIEM and observability platforms already address the infrastructure layer; customer-built detection rules sit on top of the bought platform. |
| **Business-specific workflow logic** | Build | The agent's value lives in the customer's specific workflow. Vendor "AI for [vertical]" platforms typically fail to fit precise business need. |
| **Domain-specific retrieval and filtering rules** | Build | The customer's knowledge base, sensitivity classifications, and access policies are customer-specific. Vendor retrieval frameworks provide the substrate; the rules are built by the customer. |
| **Enterprise-specific approval workflows** | Build (on bought policy engine) | The policy engine is bought; the workflow definitions (who approves what, under what conditions, with what escalation) are built by the customer. |
| **Custom regression test suites ("golden prompt" suites)** | Build | The test prompts that verify the agent behaves correctly for the customer's specific use case cannot come from a vendor. Build per [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md). |
| **Output-layer DLP rules** | Build (on bought DLP engine) | The DLP engine is typically bought; the channel-aware rules (per [Playbook 09](09-output-leakage.md) Boundary 2) are built by the customer because they depend on customer-specific destination classifications. |
| **Materiality determination protocol** | Build | The convening protocol, the four-question walkthrough, and the regulatory mapping all depend on the customer's jurisdictions and operating context. The [framework/04 (Materiality and Disclosure)](../framework/04-materiality-and-disclosure.md) annex provides the template; the customer builds the operationalization. |

### Hybrid decision principle

The decision matrix above is a starting point, not a prescription. Most organizations end up with **a buy for the platform substrate and a build for the customer-specific layer on top**: buy the foundation model and the inference infrastructure, build the workflow logic and the approval workflows; buy the logging pipeline, build the customer-specific detection rules; buy the policy engine, build the policy definitions. The exact split is customer-specific; what matters is that each capability has an explicit owner (the vendor, the customer's platform team, or a clearly-named hybrid responsibility) and that the response playbooks can execute against the resulting stack.

The **misallocation** to watch for is buying the customer-specific layer (workflow logic, approval workflows, detection rules) under the assumption that a vendor's "out of the box" feature covers it. The vendor's out-of-the-box version is typically built for the median customer, which is not the customer; the response playbooks then cannot rely on the discipline the vendor's version implies.

## Evidence Requirements: What the Platform Must Produce

The candidate platform's evidence capability is the single highest-leverage procurement criterion. The [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A-F is the standard. The Proof of Readiness Test measures the platform's actual evidence capability against the standard. The gap register captures what the platform cannot produce; the procurement decision treats those gaps as either contractual obligations the vendor must close, customer-side build commitments, or explicit risk-acceptance.

### Evidence capability requirements ranked

| Code | Evidence Type | Platform must support | Buy-vs-build implication if absent |
|---|---|---|---|
| **A** | Prompt and Response Record | Exportable prompt and response logs for any agent, any time window, with timestamps and session identifiers, retained for at least the customer's regulatory retention window | If absent: the platform fails the basic readiness bar; build a wrapper to capture prompts and responses before they reach the platform's opaque pipeline, or do not procure |
| **B** | Tool-Call Ledger | Exportable tool-call records with parameters, results, approver identity for gated calls, and **correlation identifiers that join to downstream SaaS audit logs** | The correlation-identifier requirement is the most-missed feature in 2026 platforms. If absent: build a wrapper layer that injects correlation identifiers, or accept the limit that the customer cannot reconstruct the full action chain |
| **C** | Retrieval Traces | Exportable retrieval traces with document identifiers, chunk identifiers, version stamps, similarity scores, top-k position, and retriever configuration at retrieval time | If absent: the platform cannot support PB03 forensics; build a retrieval-logging proxy or do not procure for any RAG-dependent agent |
| **D** | Memory Snapshot | Exportable memory state with scope (off, per-user, shared), retention, classification, and content at any point in time | If absent: the platform cannot support memory-bleed investigation; either disable memory (acceptable for many agents) or build a memory-export wrapper |
| **E** | Configuration Snapshot | Exportable configuration history with all changes versioned and timestamped, including system prompts, tool definitions, retriever settings, model versions, and guardrail policies | If absent: the platform cannot prove what the agent was configured to do at a given point in time; build a configuration-versioning layer or do not procure |
| **F** | Identity and SaaS Audit-Log Correlation | The platform's actions surface in downstream SaaS audit logs with the correlation identifiers from B | Customer-side correlation is feasible without platform support if the platform's identity is documented in the customer's IdP; the gap is harder to close if the platform uses opaque service accounts |

### Operational requirement

The candidate platform's evidence capability must be exportable **within 60 minutes**, per the framework's drill-measured target in [framework/01 Measurement Scope](../framework/01-minimum-viable-overlay.md#measurement-scope). The Proof of Readiness Test measures this directly. If the platform's evidence export takes longer than 60 minutes, the gap is either contractually fixable (vendor SLA) or build-side fixable (customer wraps the export); if neither is feasible, the platform fails the readiness bar.

## Procurement Decision Sequence

Procurement progression follows a sequence with explicit decision gates at each step. The sequence is the framework's adaptation of the [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) discipline applied to vendor onboarding rather than incident recovery.

### Gate 1: Initial requirements with the eight critical procurement questions

Before any vendor demonstration or RFP response, the customer's evaluation team documents which of the eight critical procurement questions the platform must answer affirmatively. The questions are the framework's distillation of the response playbooks' platform dependencies.

1. **Tool gating.** Does the platform provide tool-level allowlists, per-tool caps, action reversibility primitives (draft mode, preview mode, soft delete), and per-tool approval workflows? (Required for [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) and [Kill-Switch Mode M3](../kill-switches/overview.md).)
2. **Exportable comprehensive logging.** Are logs of tool calls, data retrievals, prompts, and outputs comprehensive, structured, and exportable? (Required for [Minimum Evidence Set](../evidence/minimum-evidence-set.md) Types A, B, C.)
3. **Configurable data retention.** Is retention configurable per agent, per data class, and adaptable to the customer's legal-hold and regulatory requirements? (Required for [Playbook 15 (Records and Retention)](15-records-retention.md) when it ships, and for [framework/04 Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) discipline.)
4. **Correlation identifiers.** Can individual tool calls be correlated to downstream SaaS audit records using documented identifiers? (Required for Evidence Type F.)
5. **Robust identity management.** Does the platform support customer-managed service accounts, scoped OAuth grants, environment separation (dev / staging / production), and credential rotation per [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md)?
6. **Retrieval-augmented generation governance.** Does the platform support corpus-level provenance, document-level trust labeling, retrieval-policy change controls, and the seven-component pipeline state capture per [Playbook 03 Type C extended](03-rag-knowledge-base-forensics.md)?
7. **Escalation contacts and incident SLAs.** Are named escalation contacts, documented incident notification timelines, evidence-export SLAs, and containment-cooperation timelines defined in the platform's contract (or available for customer-driven contracting)? (Required for [Playbook 10 (Vendor Copilots)](10-vendor-copilots.md) when the platform is vendor-hosted.)
8. **Build vs Buy clarity.** For each of the seven questions above, does the platform answer "yes" out of the box, or does the customer need to build on top? (Determines whether procurement is the right path or whether the build-side investment exceeds the buy-side savings.)

A platform that cannot answer one of the first seven questions affirmatively (with documented evidence, not vendor assurance) is a platform with a known gap. The eighth question informs whether the gap is procurable, buildable, or a deal-breaker.

### Gate 2: Proof of Readiness Test against the candidate platform

The 60-minute test described above. The test's outcome is the empirical record that supplements (and sometimes contradicts) the vendor's marketing materials and demo. The test must be repeatable; if a different customer engineer cannot reproduce the same results from the same starting state, the platform has a consistency gap.

### Gate 3: Contract and SLA terms

For platforms that pass Gates 1 and 2, the contract must lock in the operational commitments the response playbooks depend on:

- Evidence-export SLA in business hours and after hours, with named maximum delivery time and completeness commitment per [Playbook 10 Boundary 1](10-vendor-copilots.md).
- Named escalation contacts for the customer's incident-response use, with documented coverage hours and backup contacts.
- Containment-cooperation timeline (maximum time for vendor to assist with [M3-Vendor or M4 containment](../kill-switches/overview.md) per customer request).
- Incident notification timeline (vendor's maximum time to notify the customer of incidents affecting the customer's tenant).
- Legal hold and retention extension procedures (so the customer can extend vendor retention beyond default during an investigation).
- Data residency, data classification, and data-processor commitments aligned with the customer's regulatory jurisdiction.

If the vendor cannot include these in the contract, the gap moves to either customer-side build commitments or to documented [PB10 Boundary 1 risk acceptance with C4 scorecard tracking](24-board-ready-scorecard.md) when the customer chooses to deploy without contractual coverage.

### Gate 4: Operational integration and continued validation

After procurement, the platform's continued conformance to the framework's standards is validated:

- Quarterly Proof of Readiness Test re-runs per [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) cadence. The test is the platform's MVO-conformance maintenance discipline.
- Vendor's quarterly evidence drill (the [Playbook 10 Vendor Evidence Drill](10-vendor-copilots.md)) is scheduled and executed.
- The platform's release notes are reviewed against the customer's [Playbook 22 Model and Policy Drift](22-model-policy-drift.md) discipline when it ships; until then, monitor for vendor-side configuration changes that affect the agent's behavior.
- The [Playbook 24 Board Scorecard](24-board-ready-scorecard.md) Governance domain item C4 tracks any platform-level gaps that the customer accepted as risk during procurement.

## Post-Procurement Hardening

Hardening after a procurement decision converts the readiness test's findings and the contract's commitments into permanent operational discipline. The four boundaries below mirror the four-boundary pattern of [Playbook 06](06-prompt-injection-workflow.md) and [Playbook 09](09-output-leakage.md), adapted for procurement.

### Boundary 1: Capability gap closure (build or contract)

- Every gap from the Proof of Readiness Test is tracked as a closure item with an owner and target date. The owner is the customer's platform team (for build-side gaps) or the vendor (for contractually-committed gaps).
- Build-side gaps are tracked in the customer's standard engineering backlog; vendor-side gaps are tracked against the contract's SLA with documented escalation if missed.
- The 5-business-day [Playbook 18 hardening SLA](18-post-incident-hardening.md) does not apply to procurement gaps (procurement gaps are pre-incident, not post-incident); the closure timeline is procurement-specific and typically runs against the contract's effective date and the agent's go-live timeline.

### Boundary 2: Operational instrumentation

- The platform's logging, monitoring, and evidence-export procedures are integrated into the customer's standard infrastructure: SIEM, observability, IR runbook, [Playbook 11 (Monitoring)](11-monitoring-detection.md) signal families.
- The Six Metrics from [Playbook 13](13-six-metrics.md) are instrumented against the platform: Metric 2 (TTA) and Metric 4 (Drill Currency) require platform-level test execution; Metric 3 (Evidence Export Time) is measured during the quarterly Proof of Readiness re-run.
- The agent or agents deployed on the platform are added to the [AI-BOM](../templates/ai-bom.yaml) with full identity, tooling, write targets, and configuration before go-live.

### Boundary 3: Build-side discipline

- For every build-side commitment (customer-built workflow logic, customer-built approval workflows, customer-built DLP rules, etc.), the customer's engineering process applies: code review, CI test coverage per [Playbook 14](14-testing-for-agent-failure-modes.md), versioning, deployment gates.
- Build-side artifacts that the response playbooks depend on (the customer's golden-prompt test suite, the customer's DLP rule set, the customer's correlation-identifier wrapper) are first-class repository citizens, not engineering-team side projects.
- Build-side gaps to the framework's MVO conformance criteria are explicit: if the build-side commitment is "we will add memory-export logging in Q3", the gap is tracked in the [Playbook 24 Board Scorecard C4 risk-acceptance discipline](24-board-ready-scorecard.md) until Q3 closure.

### Boundary 4: Continued vendor relationship

- The vendor's quarterly business reviews include the framework's incident-readiness metrics, not just feature roadmap.
- The vendor's release notes are reviewed for changes that could affect the agent's [Playbook 22 (Model and Policy Drift)](22-model-policy-drift.md) detection thresholds when PB22 ships; until then, vendor-side platform changes are tracked as change-management events.
- The vendor's escalation contacts are tested annually (a non-incident-driven contact verification: confirm the contact still works at the vendor, confirm the customer's named contact list with the vendor, confirm the SLA still reads as written).
- Contract renewals include a re-run of the Proof of Readiness Test and a re-evaluation of any risk-accepted gaps that were tracked in the C4 scorecard during the prior contract period.

## Common Pitfalls

These are the highest-frequency failure modes in AI platform procurement. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Feature-driven procurement** | Vendor demos optimize for the "wow" moment; procurement teams optimize for capability checklists | Platform that looks impressive in evaluation but cannot move to read-only mode during an incident; the response playbooks' commitments cannot be honored |
| **Demo-driven evaluation without Proof of Readiness Test** | The Proof of Readiness Test is more effort than a demo; vendors offer demos by default | The vendor controls the evaluation surface; the customer never sees the platform under the operational pressure that matters |
| **Skipping audit log requirements until after purchase** | Audit logging is treated as an implementation detail rather than a procurement criterion | Audit log gaps surface during the first incident; remediation is contractual, slow, and expensive |
| **No correlation ID requirement in the RFP** | The correlation-identifier requirement is the most-missed feature in 2026 platforms; few RFPs name it explicitly | Tool calls cannot be joined to SaaS audit logs; Evidence Type F is incomplete; investigation operates on inference rather than evidence |
| **Vendor SLA accepted without testing** | SLAs are written; the customer assumes they will work | First incident reveals the SLA's actual operational meaning: response timing measured from when the vendor's support team receives the ticket, not from when the customer reports the incident |
| **Build vs Buy decision made by procurement alone, without IR input** | Procurement is the contracting team; IR sees the platform after deployment | Build vs Buy decision is made on cost and feature criteria; the IR team inherits a platform that cannot support the framework's response disciplines |
| **Ignoring data retention configurability** | Default retention seems sufficient until a 12-month legal hold lands | The platform's data is gone before the investigation can complete; the case file is incomplete by the time General Counsel needs it |
| **Memory scope assumed safe by default** | Memory features are demonstrated as productivity capability; scope is rarely emphasized | Memory-bleed across users surfaces during the first incident in a multi-user agent; the platform's memory configuration is not what the customer assumed |
| **Multi-agent traceability assumed available** | The platform demonstrates single-agent capability; multi-agent topologies are added later | When the customer scales to multi-agent per [Playbook 08](08-multi-agent-blast-radius.md), the cross-agent trace identifiers do not exist; cascade investigation cannot reconstruct the agent-to-agent handoff chain |
| **No proof-of-readiness re-run cadence after procurement** | The platform's readiness is verified once at procurement and never re-tested | Platform updates, vendor-side configuration changes, and the customer's own usage drift produce readiness gaps that are only discovered during the next incident |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). The MVO conformance criteria are the procurement-time benchmark; this playbook converts those criteria into procurement questions and the Proof of Readiness Test.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). All four clauses (Acts, Remembers, Retrieves, Changes) inform the procurement evaluation; the platform's capability against each clause is a procurement criterion.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). The platform's Level 2 (Containable) and Level 3 (Provable) capability is what procurement is buying; the Proof of Readiness Test is the empirical evidence that the platform reaches the claimed level.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). The platform's evidence capability must support the convening protocol's four-question walkthrough; specifically, Type F downstream correlation is what allows the disclosure determination to be made on evidence rather than inference.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The platform must support Mode M1 through M4 activation; Mode M3 variants (M3-RAG, M3-Workflow, M3-Output, M3-Vendor) require additional platform-specific capabilities documented in the relevant source playbooks.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The platform must support Type A through Type F evidence export within 60 minutes; the Proof of Readiness Test verifies this empirically.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). Every agent deployed on the procured platform populates an AI-BOM entry per the schemas; the platform must support the metadata the schema requires.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The platform's tool-tiering capability (Tier 0, 1, 2 per [Playbook 04](04-tool-design-is-containment.md)) is a procurement criterion.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone response playbook the procured platform must support.
- **Playbook 03: RAG / Knowledge-Base Forensics** ([`playbooks/03-rag-knowledge-base-forensics.md`](03-rag-knowledge-base-forensics.md)). The seven-component pipeline state capture is a platform capability that procurement must verify.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The tier model is the build-side discipline; the platform's tool-gating primitives are the buy-side capability that supports it.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). The platform must support customer-managed service accounts and scoped OAuth grants; the procurement evaluation verifies this.
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). The platform's output-layer DLP capability and channel-classification primitives are procurement criteria.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). The special case of pure-buy with no build option; the four-boundary hardening discipline applies to every vendor-managed AI platform.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The three signal families require platform-level instrumentation; procurement verifies the platform exposes the signals.
- **Playbook 13: The Six Metrics** ([`playbooks/13-six-metrics.md`](13-six-metrics.md)). The metrics' data sources are the procured platform's logs; procurement validates the platform produces what the metrics require.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The Proof of Readiness Test joins the PB14 test discipline as the platform's MVO-conformance maintenance check.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). Procurement gaps that surface during an incident enter the hardening backlog; the 5-business-day SLA applies to hardening, not to procurement-time gaps.
- **Playbook 21: Shadow AI** ([`playbooks/21-shadow-ai.md`](21-shadow-ai.md)). The migrate decision in PB21's three-path framework is a Build vs Buy decision; this playbook informs the choice for the discovered shadow agent's governed path.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). Procurement-time gaps that the customer accepts as risk are tracked in scorecard item C4 until closure; the Executive Incident Snapshot Template is produced from the procured platform's evidence export.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.4 risk-management process design, MAP 4.1 third-party data and software risks, MANAGE 1.3 risk response prioritization).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports GV.SC supply-chain risk management, GV.RR roles and responsibilities, ID.AM-04 inventories of services provided by suppliers).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the procurement-time discipline that closes the precondition gap behind ASI04 Agentic Supply Chain Compromise; the framework's response to ASI04 lives in PB10, but the procurement decision is upstream of that response).

## The Question to Carry Forward

If you discovered a serious AI incident in your organization today, could your procured platform prove what happened? Or could it only shut down the agents? The honest answer reveals whether the procurement decision optimized for normal operation or for the moment that determines whether the response playbooks in this framework are executable or aspirational.

If the answer is *"it can shut down, but evidence export takes a vendor ticket"*, PB19 is the work plan. Run the Proof of Readiness Test on the platform this week. Identify the gaps. Convert each gap to either a contract amendment, a customer-side build commitment, or a documented risk-acceptance with PB24 C4 tracking. Schedule the quarterly re-run cadence so the platform's readiness does not drift. Then evaluate the next platform candidate against the same standard.

A platform that works in a real incident is safer than one that looks good in a demo. Procurement is the discipline that decides which kind of platform the customer's agents will run on.

---

*Source: AI IR Overlay newsletter, Issue #19, "Build vs Buy for Agent Controls," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
