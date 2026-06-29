<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 21: Shadow AI (From Shadow IT to Shadow Agents)          -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The discovery playbook. Shadow AI is Shadow IT with write capabilities, deep system integration, and authorized-looking actions that bypass standard detection. The response is discovery and governance, not punitive shutdown that destroys evidence and pushes the next agent further underground.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 21: Shadow AI (From Shadow IT to Shadow Agents)

> *In a typical 2026 enterprise, the AI agents the security team knows about are a fraction of the agents actually running. The rest sit in product teams, marketing operations, finance automation, customer success workflows, and individual employee tooling. They were built or adopted to solve real business problems. Their creators did not intend to evade governance; they used the path of least friction. They are operating today, with credentials, against systems of record, often with write capabilities the security team has not inventoried. This is Shadow AI, and the response framework must change to address it before the next incident reveals which shadow agent was load-bearing.*

## Premise

Shadow IT (the use of unsanctioned software or cloud services to bypass slow or restrictive IT processes) has been a known governance gap for two decades. The discipline around it (network traffic analysis, SaaS spend review, identity provider audit, periodic discovery scans) is mature. Most security organizations have a Shadow IT discovery cadence.

Shadow AI is the next evolution of the same gap, with three properties that make it operationally different from classical Shadow IT:

| Aspect | Shadow IT | Shadow AI |
|---|---|---|
| Typical access | Read-only (file sharing, note-taking, lightweight productivity SaaS) | Read and **write** (CRM updates, email send, ticket close, code commit, cloud action) |
| Integration depth | Application-level (employee opens the app, employee uses the app) | Action-level (the agent acts through OAuth grants and service accounts that the employee no longer mediates per action) |
| Visibility | Application traffic visible to network monitoring; SaaS spend visible to finance | Often invisible: the agent runs as a service identity, makes authorized API calls, performs business-shaped actions that look indistinguishable from normal automation |
| Risk profile | Data exfiltration (employee uploads file to unauthorized cloud) | Data integrity, confidentiality, trust, and operational stability (agent modifies records, sends external communications, makes financial decisions) |

Shadow Agents emerge from organizational momentum and innovation, not malice. A marketing team writes a customer-research summarizer because the official path takes six weeks. A sales operations team automates lead enrichment because their existing tools cannot reach the relevant data. A product team builds an internal support copilot to reduce ticket volume. None of these are bad-faith actions. All of them now run with credentials against systems of record. None of them appear in the security team's [AI-BOM](../templates/ai-bom.yaml).

The biggest operational problem with shadow agents is not what they do. It is that they operate **without the inventory entry that lets the security team scope or contain anything when something goes wrong**. The first time the security team finds out about a shadow agent is often during the incident the shadow agent caused, at which point response is reconstruction rather than execution. This playbook addresses the discipline that gets the security team ahead of that moment.

**Mental Model clauses engaged:** *Acts* (primary, since shadow agents typically have write capabilities); *Retrieves* (the shadow agent's retrieval scope is part of the inventory gap); *Remembers* (conditional, if the agent has persistent memory the inventory must capture it); *Changes* (the shadow agent's update cadence and deployment path may sit outside the customer's normal change management).

**Use this playbook when:** a previously-undocumented AI agent is discovered in production · a connector audit, OAuth grant review, or SaaS audit log surfaces an AI tool the security team did not authorize · network traffic analysis or DNS logs show unrecognized calls to AI or LLM providers · an IdP login report shows a service account performing AI-mediated actions · a SaaS audit log shows automated writes that do not trace to a documented agent · a team member voluntarily discloses an agent they built · [Playbook 11 (Monitoring)](11-monitoring-detection.md) capability-family signals fire on an unrecognized agent identity · an incident investigation per [Playbook 01](01-agent-as-privileged-identity.md) reveals an unsanctioned agent in the blast radius.

## First-Hour Actions

The first hour of a Shadow AI discovery has one job that distinguishes it from other incident classes: **discovery is not yet an incident**. The unsanctioned agent may have caused harm, or it may be running cleanly with poor governance. The response sequence is the same in either case, but the framing matters: the goal is to bring the agent into governance, not to punish its creator. Revoking access before snapshotting is the most common response failure in this incident class. It destroys evidence and creates the harsh-response reputation that drives the next shadow agent further underground.

### The 60-minute Shadow AI triage

| Minute | Action | Owner |
|---|---|---|
| 0–5 | **Confirm the discovery is actually a shadow agent.** Check against the [AI-BOM](../templates/ai-bom.yaml) inventory and the documented agent roster. A documented agent the responder did not recognize is a documentation gap, not a shadow agent. Proceed only if the agent is genuinely undocumented. | Incident Commander |
| 5–20 | **Snapshot identity, credentials, and access before any revocation.** Document the runtime location (vendor-hosted, customer-hosted, employee-personal-account), the credentials in use (user OAuth grant, service account, shared token, API key), the connectors enabled (each downstream system the agent can reach), the write targets per connector, and the data scope (which corpora, which records, which classifications). This is the **Shadow AI Discovery Snapshot** and is the load-bearing evidence artifact for the rest of the response. | Identity team + Detection engineer |
| 20–35 | **Initiate safe mode without destroying the agent's runtime.** Where the agent can be modified directly (the customer or a known team built it, the runtime is accessible), shift to [Mode M1 Read-Only](../kill-switches/overview.md) by stripping write tools, or to [Mode M2 Approvals Required](../kill-switches/overview.md) by routing every action through human approval. Where the agent's runtime cannot be modified by the security team (a vendor-hosted tool the employee subscribed to directly, an employee-personal-account-hosted agent), shift to **identity-level containment**: revoke the agent's OAuth grants to sensitive systems, disable the service account at the IdP, restrict network egress for the runtime, or block the agent's access to critical datasets at the data-store level. The choice depends on what the security team controls. | Platform engineer or IdP administrator |
| 35–50 | **Engage the agent's creator or operator directly.** Most shadow agents have a known owner inside the organization; identify them and bring them into the response bridge. The owner has the runtime context the security team needs (the prompt, the deployment platform, the user it was built for, the business problem it solves). The owner is also the person who decides whether the agent migrates, redesigns, or retires. Excluding the owner produces incomplete response. | Incident Commander + agent owner |
| 50–55 | **Walk the [Six Triage Questions](../triage/six-questions.md) with one extension.** Q1 (tools), Q2 (write targets), Q3 (identity), Q4 (memory), Q5 (safe mode), Q6 (evidence plan) follow standard discipline. Add a seventh: *what business problem does this agent exist to solve, and what is the legitimate path to solve it under governance?* The answer determines whether the agent migrates, redesigns, or retires. | Incident Commander + agent owner |
| 55–60 | **Convene the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) if the shadow agent has touched customer data, regulated data, external recipients, or financial actions.** Shadow agent discovery often surfaces materiality questions that have been latent for weeks or months. The convening protocol applies regardless of containment mode, because the disclosure window may have started before the agent was discovered. | Incident Commander |

**Discipline:** the Shadow AI Discovery Snapshot is the chain-of-custody anchor for a shadow agent response. Without it, the response is operating on inference about what the agent could do; with it, the response can scope the actual blast radius. The instinct to revoke OAuth grants or disable the service account before snapshotting is the most damaging shortcut in this playbook. Snapshot first; revoke second.

**Critical rule:** preserve the agent's runtime, its access state, and its recent activity logs **before** any access change. Where the agent's logs are stored externally to the security team's visibility (a vendor tool the employee subscribed to, a personal-account-hosted runtime), capture what is reachable now; the next access revocation may eliminate the security team's ability to reach those logs.

## Containment Options

Shadow AI containment combines the framework's [Kill-Switch Modes](../kill-switches/overview.md) with **identity-level containment** discipline that is specific to scenarios where the security team does not control the agent's runtime directly. The choice depends on whether the agent is modifiable in place.

### Mode mapping for Shadow AI

| Mode | Use when | What changes |
|---|---|---|
| **M0 Observe (after discovery)** | The discovered agent is operating cleanly, the snapshot is complete, the owner is engaged, and the migration path is short | Full logging continues; the agent enters the AI-BOM as a transitional entry; standard monitoring per [Playbook 11](11-monitoring-detection.md) covers it until governed integration completes |
| **M1 Read-Only** | The agent is customer-modifiable (built in-house or in a runtime the security team controls) and the harm vector is unclear | Strip write tools from the agent's tool set; the agent continues to serve reads while investigation and migration proceed |
| **M2 Approvals Required** | The agent is customer-modifiable and business need requires continued operation | Every tool call routes to a human approver before execution; the approver sees the proposed action and the destination |
| **M3 Tool Tiering** | The agent's tools have been classified into T0/T1/T2 tiers (per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md)) during the discovery snapshot | Disable Tier-2 tools immediately; keep T0/T1 tools live for continued business value during the migration window |
| **Identity-level containment** (Shadow-AI-specific) | The agent's runtime is not directly modifiable by the security team (vendor tool, employee-personal-account-hosted, no-code platform without admin access) | Revoke OAuth grants to sensitive systems at the customer's IdP; disable the agent's service account or shared token at the IdP; restrict network egress for the runtime IP range; block the agent's access at the data-store layer (corpus permissions, API gateway rules). Each revocation is logged with the reason and the access being removed |
| **M4 Full Disable** | The shadow agent is actively causing harm (sending external emails, modifying customer records inappropriately, exfiltrating data) | Hard stop via identity-level containment plus, where possible, runtime termination by the owner. Snapshot first per the First-Hour Actions sequence, then revoke |

### Identity-level containment specifics

When the security team cannot modify the agent's runtime directly, the containment surface shifts to the identity provider, the data store, and the network egress controls the security team does own. The sequence:

1. **OAuth grant revocation.** Identify every OAuth grant the agent uses (in the customer's IdP, in the third-party SaaS's connected-apps list, in the data store's API connections). Revoke the grants for sensitive scopes first (write scopes on systems of record, read scopes on regulated data classes). Read-only scopes on non-sensitive data can be revoked second.
2. **Service account or shared token deactivation.** If the agent runs as a service account managed by the customer's IdP, disable the account. If it runs on a shared token issued from the customer's identity store, rotate or revoke the token. The disabling captures a final timestamp of legitimate access for the audit trail.
3. **Network egress restriction.** Where the agent's runtime is in a customer-controlled network (employee VPN, BYOD with corporate gateway), block egress to the relevant AI provider or to the sensitive downstream systems. This is the right control when the agent itself cannot be modified but the network path is the customer's.
4. **Data-store-level block.** Where the agent reads from customer-controlled data stores (vector indices, document repositories, databases), revoke the agent's access at the data store rather than at the agent. This is the surgical control when the customer cannot revoke the agent's overall credentials without breaking other legitimate work.

The four layers are complementary, not exclusive. A response may use OAuth revocation for one connector, network egress restriction for another, and data-store-level blocks for a third, depending on which layer the customer has authoritative control over for that specific path.

## Evidence Priorities

The Shadow AI evidence set extends the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A-F with explicit emphasis on the **Shadow AI Discovery Snapshot** as the agent-inventory equivalent of Type E (Configuration Snapshot) for shadow agents that may have no other formal configuration record.

### Evidence priorities ranked for Shadow AI

| Code | Evidence Type | Priority | Why it matters |
|---|---|---|---|
| **B** | Tool-Call Ledger | **Critical** | The agent's action history is the primary record of what it actually did. For shadow agents, the ledger may be incomplete (the agent's runtime may not log to a customer-accessible store). Capture what is available immediately; the next access revocation may close the window. |
| **F** | Identity and SaaS Audit-Log Correlation | **Critical** | The downstream record of where the agent's actions reached customer-controlled systems. Even when the agent's own logs are unavailable, the downstream SaaS audit logs (Salesforce, M365, ticketing, code repos, cloud control plane) record what the agent did once its actions reached the customer's systems. This is the load-bearing record when the agent is itself opaque. |
| **E** | Configuration Snapshot (extended: **Shadow AI Discovery Snapshot**) | **Critical** | The shadow agent is not yet in the AI-BOM. The discovery snapshot is the configuration artifact: agent name and owner, runtime location, identity and credentials, connectors and write targets, retrieval scope, memory configuration, deployment platform, business purpose. The snapshot is what allows the rest of the framework's controls to operate on this agent going forward. |
| **C** | Retrieval Traces | High if the agent is RAG-based | Without the retrieval trace, the response cannot determine what data the agent saw. For shadow agents that lack retrieval logging, capture the connector list as a proxy and note the logging gap as a finding. |
| **A** | Prompt and Response Record | High if accessible | Often the most difficult to capture for shadow agents. If the agent runs on a vendor tool the employee subscribed to (a ChatGPT Plus account, a Claude Pro account, a no-code agent platform), the customer may not have access to the prompt and response history. Capture what the owner can produce; document the gap. |
| **D** | Memory Snapshot | High if the agent has persistent memory | Particularly important for vendor-hosted agents where memory may persist across sessions and across employees. The snapshot captures the data the agent has accumulated outside the customer's normal data governance. |

### Shadow-AI-specific captures

In addition to A through F:

- **The agent's deployment manifest** (if any): the code, configuration, or no-code-platform definition that constitutes the agent. For shadow agents this often does not exist in a customer-controlled location; capture whatever the owner can produce.
- **The agent's change history**: who modified it, when, with what intent. Most shadow agents have undocumented change history; the response identifies this as a finding rather than recovering it.
- **The agent's dependency graph**: every external service, model provider, data store, and tool the agent invokes. The graph is the supply-chain artifact for shadow agents, analogous to [Playbook 10's](10-vendor-copilots.md) vendor-copilot inventory.
- **The agent's user base**: the human users the agent serves or operates on behalf of, the customers the agent's outputs reach, and the systems the agent's actions affect. This is the human-mediated scope that disciplined inventory normally captures pre-deployment.

**Operational requirement:** the full Shadow AI Discovery Snapshot must be capturable within **60 minutes** of discovery. The downstream Type F audit logs are typically capturable within the same window; the agent's own logs may not be. Where the agent's logs are not capturable in 60 minutes, document the logging gap as a finding for the post-incident hardening.

### CIA+T Impact Assessment for Shadow AI discoveries

Shadow AI discovery is unusual among incident classes because **the discovery itself is not yet an incident**: the shadow agent may be operating cleanly with poor governance. The CIA+T impact framing from [Playbook 05 (Executive Decision-Making)](05-executive-decision-making.md) is applied retrospectively to the shadow agent's operating history, not just to a current event. The assessment determines whether the discovery is a governance finding (no CIA+T impact identified) or an incident (CIA+T impact identified, possibly latent for weeks or months).

| Dimension | Shadow-AI question | What to capture |
|---|---|---|
| **Confidentiality** | What regulated or sensitive data has the shadow agent accessed over its operating life? Has the agent's retrieval scope included corpora the security team has not authorized? | The Discovery Snapshot's retrieval scope; cross-reference with the customer's data-classification inventory; identify per-corpus access without documented business need |
| **Integrity** | What records has the shadow agent created or modified in systems of record? Are those records correct, or has the agent's lack of governance produced data-quality issues that the business has been absorbing as routine error? | The Discovery Snapshot's write-target list; SaaS audit logs (Type F) for shadow-agent write history; the business owner's assessment of record-quality impact |
| **Availability** | Has the shadow agent's containment response disrupted the workflow it serves? For vendor-hosted or personal-account-hosted shadow agents where identity-level containment is the only option, what business processes depend on this agent? | The containment-mode timeline; the affected business owner's operational impact statement; the migrate-vs-redesign-vs-retire path implication |
| **Trust** | Has the shadow agent produced customer-facing or external-recipient impact during its operating life? Did the agent send emails, post tickets, generate customer-facing recommendations, or modify customer-visible records? | The agent's user base inventory; the affected-customer count; the visibility classification; **the most important Shadow AI Trust assessment is the regulatory-disclosure framing**: if the shadow agent touched regulated data over its lifetime, the disclosure window may have started months before discovery |

The Trust dimension is the framework's recognition that Shadow AI discoveries often surface **latent regulatory exposure** that has been accumulating before discovery. A shadow customer-support copilot that has been operating for 6 months and has touched 8,000 customer records produces a different materiality determination than the discovery itself implies. The CIA+T framing in the [Executive Decision Packet](05-executive-decision-making.md) is the artifact that translates the discovery into the customer's regulatory disclosure posture; the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md) per the canonical convening trigger from framework/04 is triggered whenever the CIA+T assessment surfaces customer-data, external-recipient, or regulated-data conditions, regardless of containment mode.

## Recovery Sequence

Shadow AI recovery is not incident closure. It is migration to governance. Three paths exist for each discovered shadow agent, and the choice is made by the agent's owner, the security team, and (where business need is material) the business owner of the affected function.

### Path 1: Migrate

The shadow agent's business value is established, the architecture is recoverable, and the agent can be brought into the customer's standard AI governance with reasonable effort. Migration steps:

1. **AI-BOM entry.** The agent is added to the customer's [AI-BOM](../templates/ai-bom.yaml) with full identity, tooling, write targets, retrieval scope, memory configuration, and ownership. The migration is not complete until the AI-BOM entry validates against [`schemas/ai-bom.schema.json`](../schemas/ai-bom.schema.json) via the reference validator.
2. **Privilege Matrix entry.** The agent's tools are tier-classified per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) and added to [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). T2 tools acquire approval-required gates; T1 tools acquire caps and allowlists; T0 tools remain unrestricted.
3. **Identity migration.** The agent's runtime identity is migrated from whatever it currently uses (often a personal OAuth grant or a shared token) to a customer-managed service account with documented scopes and rotation cadence per [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md).
4. **Logging migration.** The agent's prompts, tool calls, retrieval traces, and outputs are routed to the customer's standard logging infrastructure with retention windows matching the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) operational requirements.
5. **Kill-Switch implementation.** Modes M1, M2, M3, and M4 are implemented for the migrated agent per [Kill-Switch Modes](../kill-switches/overview.md) and tested in a tabletop within the 90-day rolling window per [framework/03 Maturity Roadmap](../framework/03-maturity-roadmap.md).
6. **Conformance validation.** The migrated agent satisfies the [MVO Conformance Criteria](../framework/01-minimum-viable-overlay.md) before it returns to full operation.

### Path 2: Redesign

The shadow agent's business value is established but its current architecture cannot be brought into governance without fundamental change. Common cases: the agent uses prompt-engineering shortcuts where architectural controls are required (per [Playbook 06](06-prompt-injection-workflow.md) and [Playbook 04](04-tool-design-is-containment.md)); the agent has memory or retrieval scope that cannot be safely reduced; the agent runs on a platform that does not support the logging or containment the framework requires. Redesign steps:

1. **Document the business need.** The redesign starts from the problem the agent solves, not the agent's existing implementation. Engage the function owner and the security team to define the requirements.
2. **Architect the replacement.** Design the replacement against the framework's standards from the start: AI-BOM-ready, tier-classifiable tools, identity-managed credentials, logging-aware, kill-switch-capable.
3. **Migrate users with continuity planning.** The shadow agent continues to operate in a constrained safe mode (M1 Read-Only typically) until the replacement is operational; users are migrated with documented handoff.
4. **Retire the original.** Once users have migrated, the shadow agent's identity, credentials, and runtime are decommissioned with proper data retention and audit-log preservation.

### Path 3: Retire

The shadow agent's business value does not justify the governance overhead, or the business function it serves can be addressed by existing sanctioned tooling, or the risk-benefit analysis favors elimination. Retirement steps:

1. **Communicate the decision.** The owner and affected users are informed; the alternative path is documented.
2. **Preserve the evidence baseline.** The Shadow AI Discovery Snapshot, the activity history, and any incident-relevant evidence are preserved in the customer's standard evidence retention store before the agent is decommissioned.
3. **Revoke credentials and disable runtime.** Following the identity-level containment sequence in Containment Options above, with the addition of permanent revocation rather than temporary suspension.
4. **Document the retirement.** The agent's case file enters the customer's [Playbook 18 Post-Incident Hardening](18-post-incident-hardening.md) backlog as a closed item with the discovery, containment, and retirement record preserved.

**Approver for path selection:** CISO or designated Incident Commander, in consultation with the function's business owner. The agent's creator does not unilaterally choose retirement (which may be self-protective) or migration (which may underweight risk).

## Post-Incident Hardening

Shadow AI hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert Shadow AI from a recurring surprise into a managed lifecycle.

### Boundary 1: Discovery (continuous, not one-time)

- **Network traffic and DNS monitoring** for known AI and LLM provider endpoints. The signal is presence of outbound calls to AI providers the security team has not authorized for a given runtime or identity. Detection rule lives in [Playbook 11](11-monitoring-detection.md) Family 1 (action-based signals).
- **IdP audit log review** for OAuth grants to AI tools. Most IdPs surface OAuth-grant lists; the security team reviews new grants in a documented cadence (weekly or daily depending on organizational risk appetite).
- **SaaS audit log review** for automated writes that do not trace to a documented agent. Salesforce, M365, ServiceNow, Jira, GitHub, and similar systems all log the originating identity; writes from unrecognized identities are the signal.
- **Voluntary disclosure channel.** A documented intake path (email alias, Slack channel, intake form) where teams can disclose shadow agents without punitive consequences. This is the highest-leverage discovery channel because the team building the agent knows it exists; the channel exists or does not exist as a customer-cultural artifact.
- **Quarterly discovery audit.** A documented audit cadence per [Playbook 14 (Testing for Agent Failure Modes)](14-testing-for-agent-failure-modes.md) that runs all four channels above and produces a roster of discovered shadow agents for the quarter.

### Boundary 2: Identity (24-hour intake standard)

- **Within 24 hours of discovery, every shadow agent has an intake record** with: owner identity and team; runtime location and platform; identity and scope of access; tools and write targets; minimum viable logs available; safe mode plan; classification by capability (read-only, write-capable, system-of-record). The 24-hour standard is the Shadow Agent Intake Standard from this playbook.
- **The intake record migrates into the AI-BOM as a transitional entry** with `status: shadow_under_governance` or equivalent annotation. The transitional entry validates against [`schemas/ai-bom.schema.json`](../schemas/ai-bom.schema.json) on a best-effort basis (some fields may be empty pending migration).
- **The shadow agent's identity is mapped to a customer-managed identity within 30 days.** Service accounts replace shared tokens; managed OAuth grants replace personal grants; documented scopes replace wildcard authorizations.

### Boundary 3: Governed integration path

- **A low-friction, documented integration path** exists for teams that want to deploy an AI agent under governance. The path should be measurably faster than building a shadow agent and bypassing governance. If the official path takes six weeks and the shadow path takes a day, the discovery boundary will be overwhelmed by new shadow agents regardless of detection investment.
- **The integration path includes:** a templated AI-BOM that the team fills out; a templated Privilege Matrix; an identity-issuance procedure with documented turnaround time; a logging pipeline the team plugs into; pre-approved tool wrappers for common operations (email send, CRM write, ticket update, code commit) with appropriate tiering already applied.
- **The integration path is reviewed quarterly** for friction. If the discovery boundary keeps surfacing the same teams building the same types of shadow agents, the integration path has a usability gap that the discovery boundary alone cannot solve.

### Boundary 4: Detection extended to shadow patterns

- **PB11 Family 3 (capability-based signals)** extended to detect unrecognized agent identities performing AI-mediated actions: capability lookups to LLM providers, retrieval calls to vector stores, tool calls to known agent tooling endpoints from identities not in the AI-BOM.
- **Anomalous-identity monitoring** at the SaaS audit log layer: writes from identities that are not in the customer's documented agent inventory; OAuth grants that do not have a documented business case in the customer's change-management system.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to all four boundaries. Shadow AI findings do not wait for the next quarterly review.

## Common Pitfalls

These are the highest-frequency failure modes in Shadow AI response. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Revoking access before snapshotting the discovery state** | Standard IR reflex applied to a discovery scenario | Discovery snapshot is incomplete; the agent's capability and access cannot be fully characterized; the migration vs retirement decision is made on partial information |
| **Treating shadow AI discovery as employee misconduct** | The instinct that the creator was hiding the agent | Punitive response drives the next shadow agent further underground; the discovery boundary becomes less effective over time; the disclosure channel loses credibility |
| **Assuming low risk because the agent "just reads"** | Read-only mental model carried over from Shadow IT | Read-only agents still leak data through outputs per [Playbook 09](09-output-leakage.md); read scope on regulated data is its own risk class regardless of write capability |
| **No identity-level containment fallback when tool-level isn't available** | Containment runbook assumes the agent's runtime is customer-modifiable | Vendor-hosted shadow agents and personal-account shadow agents become uncontainable; the response is "we asked the employee to stop using it" with no audit trail |
| **No 24-hour intake standard** | Discovery results sit in the IR team's tracker but never enter the AI-BOM | The same agent is rediscovered in the next quarterly audit; inventory churn rather than inventory growth |
| **Punitive response that drives the next shadow agent underground** | Cultural pattern: security as enforcement rather than enablement | Subsequent shadow agents are built with deliberate evasion (personal devices, personal accounts, residential ISPs) rather than convenience evasion |
| **Confusing shadow AI with insider threat** | Surface similarity (unauthorized agent, unauthorized actions) | Investigation defaults to [Playbook 12 (Insider Threat 3.0)](12-insider-threat-3.md) discipline (HR and Legal at minute zero) when the actual scenario is a governance gap. Wrong stakeholders are engaged; the agent owner is treated as a suspect rather than a partner |
| **Discovery only via incident** | No proactive discovery boundary; shadow agents surface only when something breaks | First-time discovery has the smallest possible information surface and the largest possible blast radius; response is always reconstruction |
| **No governed integration path** | The shadow-AI problem is treated as a discovery problem rather than a friction problem | Teams continue building shadow agents because they have no legitimate option; the discovery boundary becomes a treadmill |
| **Documentation gap on memory and retrieval scope** | The intake form captures tools and identity but not the data scope the agent has accumulated | The agent migrates to governance with hidden memory bleed across users or hidden access to sensitive retrieval corpora; the migration looks complete but does not address the highest-impact risks |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 Inventory is the discipline this playbook converts shadow agents into; the Shadow Agent Intake Standard is the operational specification for bringing newly-discovered agents into MVO-1 conformance.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clause 1 (Acts) is the load-bearing discipline because shadow agents typically have write capabilities. Clause 4 (Changes) governs the shadow agent's deployment and change-control gap.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Shadow AI discovery is a Level 1 (Aware) capability. The 24-hour intake standard and the governed integration path are Level 2 (Containable) and Level 3 (Provable) capabilities respectively.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). Shadow agent discoveries that surface latent regulatory-data exposure trigger the convening protocol even when the agent has been operating without observable harm.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The full M0-M5 ladder applies to migrated shadow agents. Identity-level containment is the fallback discipline when tool-level kill-switches are not available because the runtime is not customer-modifiable.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). The Shadow AI Discovery Snapshot is a Type E (Configuration Snapshot) extension for agents that have no prior formal configuration record.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The artifact every migrated shadow agent must populate. The transitional entry pattern with `status: shadow_under_governance` annotation supports the intake-before-completion discipline.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). Every migrated shadow agent's tools are tier-classified into this matrix as part of the migration path.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook the shadow agent migration ultimately produces conformance with.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The pre-incident discipline that classifies the migrated agent's tools; without it the migrated agent has only nominal governance.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). The credential-discipline playbook the migrated agent's identity migration must satisfy.
- **Playbook 09: Leakage Without a Breach** ([`playbooks/09-output-leakage.md`](09-output-leakage.md)). Shadow agents that have been operating without output-layer DLP are particularly likely to have produced latent output-leakage incidents; the discovery snapshot should specifically check whether output-leakage has occurred.
- **Playbook 10: Vendor Copilots and Mutual Responsibility** ([`playbooks/10-vendor-copilots.md`](10-vendor-copilots.md)). Vendor-hosted shadow agents combine this playbook's discovery discipline with PB10's vendor-side containment constraints. Identity-level containment is the shared fallback for both.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The detection rules that surface unrecognized agent identities live here; PB21's discovery boundary depends on PB11's instrumentation.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). Shadow AI and Insider Threat 3.0 can look similar at the surface; the distinguishing question is intent. Most shadow AI is governance gap (no malicious intent), most Insider Threat 3.0 involves established intent concerns. The investigative discipline differs accordingly.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The quarterly discovery audit cadence lives in PB14's testing discipline.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day hardening SLA applies to discovery findings; each shadow agent migration or retirement produces hardening items.
- **Playbook 24: Board-Ready Scorecard** ([`playbooks/24-board-ready-scorecard.md`](24-board-ready-scorecard.md)). Shadow AI inventory currency and discovery cadence are Governance domain signals. The number of shadow agents discovered per quarter, the number migrated within 30 days, and the trend over time are board-defensible posture indicators.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.6 inventory mechanisms, MAP 1.1 intended-use documentation, MANAGE 1.3 risk response prioritization).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook is the direct operational response for **ID.AM** asset management gaps applied to AI agents; supports GV.OC organizational context, GV.RR roles and responsibilities, ID.AM-01 inventories of hardware, ID.AM-02 inventories of software and services, ID.AM-04 inventories of supplier services).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook addresses the inventory-gap precondition that makes ASI03 Identity & Privilege Abuse and ASI04 Agentic Supply Chain Compromise harder to detect and contain).

## The Question to Carry Forward

If you discovered a shadow AI agent in your organization tomorrow morning, could you move it to safe mode within 10 minutes? Could you export its activity and access history within an hour? Could you bring it into your AI-BOM within 24 hours with full identity, tooling, write targets, and retrieval scope? Could you migrate it to a customer-managed identity within 30 days? Could you decide whether to migrate, redesign, or retire by the end of the week, with the agent's owner as a partner rather than a suspect?

The honest answer is the gap. If any of those answers is *"not yet"* or *"only if the agent is in our existing runtime"*, the discovery boundary, the intake standard, the identity-level containment fallback, or the governed integration path is the corresponding hardening priority.

Shadow agents come from organizational momentum and innovation. The response framework's job is not to suppress that momentum, because the momentum is the source of the legitimate AI value the business will need. The job is to make the difference between **shadow AI** and **governed AI** the difference between a one-day intake into a clear path and a six-week proposal into a closed door. When the legitimate path is faster than the shadow path, the discovery boundary becomes a governance boundary rather than an arms race.

---

*Source: AI IR Overlay newsletter, Issue #21, "The Evolution from Shadow IT to Shadow AI," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
