<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 10: Vendor Copilots and Mutual Responsibility                 -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                   -->
<!--  https://jacobideji.com                                                 -->
<!--  License: Apache 2.0. See LICENSE file in this package.                 -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The vendor copilot playbook. The vendor manages the agent. The customer is held accountable for what it does. Shared responsibility only works when evidence, containment, and support are actually shared.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 10: Vendor Copilots and Mutual Responsibility

> *Vendor copilots automate work, access sensitive data, and take actions in the customer's name. When something goes wrong, the customer answers the regulator, the press, and the board. The vendor is one phone call away. "Shared responsibility" without testable, contracted readiness is a procurement slogan, not an operational control.*

## Premise

Microsoft 365 Copilot, Salesforce Einstein, ServiceNow Now Assist, Google Workspace Gemini, GitHub Copilot, Workday Vendor Direct, the embedded copilots inside CRM and ERP and ticketing platforms: every major enterprise SaaS now ships an AI copilot, and every adoption produces the same operational gap. The vendor manages the agent's prompts, model, retrieval, memory, and tools. The customer is responsible to the regulator, the auditor, the board, and the customer's own customers for what the agent does inside the customer's tenant. The accountability does not shift even though the operational levers do.

Four practical realities define vendor-copilot incident response:

**Visibility gaps.** The agent's actions inside the vendor's infrastructure are invisible to the customer's SOC unless the vendor exposes them through documented APIs or scheduled exports. Most vendors expose a partial view: high-level activity summaries without the parameter-level detail that an investigation needs. The customer's monitoring (SIEM, DLP, UEBA) sees the downstream effect of agent actions in target systems, not the agent's reasoning or retrieval path that produced them.

**Evidence dispersion.** Prompts, tool-call ledgers, retrieval traces, memory snapshots, and configuration history live with the vendor in proprietary formats. The customer can pull what the vendor exposes, when the vendor exposes it, with the retention window the vendor allows. The Minimum Evidence Set the customer's IR program is built around (A through F) becomes a request to a vendor support queue rather than an export the customer's runbook can execute.

**Ambiguous control.** Traditional SaaS gives the customer admin controls: disable a user, change a permission, modify a configuration. Vendor copilots vary widely. Some expose granular feature flags. Many expose only license-level disable and user-level access toggles. Few expose the rapid scope-shrink controls that incident response requires. The customer's Tier-1 SOC, trained to activate Kill-Switch Modes M1 through M4 within 10 minutes, finds that for vendor copilots the operational equivalent is "open a vendor support ticket and wait."

**Shared responsibility means shared clarity, and procurement often skipped the clarity step.** Master Service Agreements and Data Processing Agreements signed at onboarding rarely specify evidence export SLAs, named escalation contacts, retention floors, or containment cooperation timelines. The shared-responsibility model becomes one-sided in practice: the customer is responsible for outcomes, the vendor is responsible only for what the contract specified. The gap between the two is where real incidents happen.

The defensive thesis of this playbook is direct: **vendor copilots must be deployed behind a customer-controlled identity boundary, contracted with explicit evidence and containment SLAs, and rehearsed quarterly through a vendor evidence drill that proves the readiness in fact rather than on paper.** Without those three disciplines, the framework's response, evidence, and recovery commitments cannot be honored when the underlying agent lives at a vendor.

**Mental Model clauses engaged:** *Acts* (primary; the vendor's agent acts in the customer's name through customer-authorized scopes), *Retrieves* (secondary; vendor agents retrieve customer data the customer has not directly authorized for that purpose), and *Remembers* (conditional; many vendor copilots retain conversation or context state with limited customer visibility into what is retained and for how long).

**Use this playbook when:** a vendor copilot acts in ways the customer did not intend; a customer-facing system shows an agent action with no obvious customer-side authorization; a regulator inquires about a vendor agent's behavior in the customer's tenant; output-leakage detection per [Playbook 11 (Monitoring)](11-monitoring-detection.md) fires on vendor-copilot activity; pre-deployment review of a vendor copilot identifies missing evidence-export or containment capabilities; quarterly vendor evidence drill exposes a readiness gap; or a vendor announces an incident that may have affected the customer's tenant.

## First-Hour Actions

The first hour of a vendor-copilot incident has one challenge that distinguishes it from incidents in customer-managed agents: **you do not own the operational levers, so the response runs on two tracks simultaneously**. The customer-controllable track activates immediately. The vendor-controllable track depends on the contract and the named escalation contact. Both tracks must run in parallel from minute zero.

### The 60-minute vendor-copilot triage

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Activate customer-side containment.** Disable user access to the vendor copilot at the customer's identity provider. Revoke OAuth grants. Block network egress to the vendor copilot API if customer-controllable containment is too slow. The objective is to stop further agent actions inside the customer's tenant within 10 minutes regardless of what the vendor does next. | Tier-1 SOC + IdP team |
| 10–20 | **Open the named vendor escalation.** Reference the contracted SLA in the first message. Provide: incident summary, affected tenant, suspected agent action, customer-side evidence captured, requested vendor actions, requested evidence export. If no named escalation exists, log the gap as a critical [Playbook 18](18-post-incident-hardening.md) hardening item before escalating through generic vendor support. | Incident Commander |
| 20–30 | **Walk the [Six Triage Questions](../triage/six-questions.md) with one adaptation.** Q1 (tools), Q2 (write targets), Q3 (identity), Q4 (memory) require vendor cooperation for full answers. Document customer-side partial answers and the vendor-side gaps as a structured request to the escalation contact. The gap itself is evidence of the readiness state. | Incident Commander |
| 30–45 | **Snapshot customer-side evidence.** IdP authentication logs, OAuth grant history, downstream SaaS audit logs in target systems (CRM, ERP, ticketing, email, code repos), DLP/SIEM correlations, gateway or proxy logs if the vendor copilot is fronted by customer infrastructure. The customer-side evidence is the independent-verification anchor; it does not depend on the vendor's cooperation. | Detection engineer |
| 45–55 | **Issue the vendor evidence export request.** Request the full Minimum Evidence Set (Types A through F) per the contracted SLA. Specify retention extension: the customer's regulatory clock may exceed the vendor's default retention window. The export request and the legal hold notice are separate documents; both go in writing. | Incident Commander + General Counsel |
| 55–60 | **Convene the [Materiality and Disclosure call](../framework/04-materiality-and-disclosure.md)** if the vendor copilot reached external recipients (customer messages, partner systems, public output), if regulated data was touched, or if the customer's regulator has jurisdiction over the affected agent action. Vendor-copilot incidents nearly always cross the call threshold because the vendor copilot operates against the customer's brand and identity. | Incident Commander |

**Discipline:** the customer-side track does not wait for the vendor. Customer-controlled IdP disablement and OAuth revocation are the customer's containment of last resort. They are slower than dedicated agent kill-switches in customer-managed agents, but they are immediate compared to vendor-side response. The 10-minute customer-side containment target is achievable for every vendor copilot the customer deploys; if it is not, the deployment is not production-ready per [Playbook 04 (Tool Design)](04-tool-design-is-containment.md) discipline.

**Critical rule:** evidence requests to the vendor are written, not verbal. The exchange becomes part of the case file. Regulators reviewing the incident reconstruct the timeline from documents, not phone calls.

## Containment Options

Containment for a vendor-copilot incident splits along the customer/vendor responsibility boundary. The framework's six [Kill-Switch Modes](../kill-switches/overview.md) apply with explicit annotation of who can activate each.

### Mode mapping for vendor-copilot incidents

| Mode | Customer-controllable | Vendor-controllable | What changes |
|---|---|---|---|
| **M0 Observe** | Logging at IdP, target SaaS audit, gateway proxy | Vendor's internal activity monitoring | Customer correlates downstream effects; vendor monitors prompt and tool layers |
| **M1 Read-Only** | Strip write scopes on OAuth grants to vendor copilot | Vendor configures copilot to read-only operating mode | Customer-side change is immediate; vendor-side change depends on copilot configurability |
| **M2 Approvals Required** | Vendor-dependent (most vendor copilots lack customer-controlled approval gates) | Vendor toggles human-approval mode for the copilot's Tier-2 actions | Largely vendor-side; customer cannot impose approval gates the vendor copilot does not natively support |
| **M3 Tool Tiering** | Customer disables OAuth scopes (revoke `mail.send`, keep `mail.read`) | Vendor disables specific tool integrations inside the copilot | Hybrid: customer-side scope revocation is faster but coarser; vendor-side tool tiering is more precise but slower |
| **M3-Vendor (variant)** | Customer cannot directly activate | Vendor support team disables a specific tool, integration, or data source | Documented sub-variant of M3 for vendor-controlled granular containment. Acceptable only when contracted SLA for vendor activation is faster than the customer's overall TTA target. |
| **M4 Full Disable (customer-side)** | Customer disables the vendor copilot at the IdP, revokes all OAuth grants, blocks egress | Vendor service continues unchanged for other tenants | Stops agent actions inside the customer's tenant. Does not stop the vendor from retaining customer data per their retention policy. |
| **M4 Full Disable (vendor-side)** | Customer cannot directly activate | Vendor suspends the copilot for the customer's tenant per contract | Full vendor-side shutdown. Requires named escalation contact and contracted SLA to be meaningful. |
| **M5 Controlled Re-Enable** | Customer re-establishes OAuth grants in stages | Vendor confirms the underlying issue is resolved and customer re-grants access | Recovery is a joint sequence: vendor confirms remediation, customer re-grants scopes, monitoring validates each stage |

### The customer-first containment principle

Customer-controllable containment activates first, always. Waiting for the vendor's named escalation to respond before stripping OAuth scopes converts a 10-minute customer-side containment into a multi-hour vendor-side containment. The vendor's response, however cooperative, is bounded by their internal SLAs, time zones, and ticket queues. The customer's identity provider is bounded only by the customer's own automation.

| Containment classification | Default response |
|---|---|
| **Customer-controllable available** | Activate customer-side containment immediately. Open vendor escalation in parallel. Do not wait. |
| **Customer-controllable insufficient** (e.g., the harmful action originates from vendor-controlled retrieval) | Activate customer-side containment for partial scope reduction. Vendor escalation becomes the critical path. Document the customer-side limit. |
| **Customer-controllable absent** | Deployment was not production-ready. Activate the only available container (IdP user disable at minimum). Treat the gap as an immediate [Playbook 18](18-post-incident-hardening.md) hardening item with contract renegotiation as the proposed resolution. |

## Evidence Priorities

The vendor-copilot evidence set extends the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A through F with explicit split between customer-side sources (which the customer controls) and vendor-side sources (which require vendor cooperation). The independent-verification rule applies throughout: customer-side evidence must be sufficient to validate the vendor's account of the incident.

### Evidence priorities ranked for vendor-copilot incidents

| Code | Evidence Type | Customer-side source | Vendor-side source | Priority |
|---|---|---|---|---|
| **F** | Identity and SaaS Audit-Log Correlation | IdP authentication, target SaaS audit (Salesforce, M365, ServiceNow, etc.), CloudTrail or equivalent for cloud-attributed actions | Vendor session logs, vendor identity attribution records | **Critical**: the downstream evidence that does not depend on vendor cooperation |
| **B** | Tool-Call Ledger | Limited customer-side visibility unless gateway-fronted | Vendor function-call logs in proprietary format | **Critical**: required to reconstruct what the agent attempted |
| **A** | Prompt and Response Record | Limited customer-side; some vendors expose to customer admin console | Vendor's full prompt and output history | **Critical**: required to understand intent and to bound the model-layer dimension of the incident |
| **C** | Retrieval Traces | Customer-side connector logs (partial) | Vendor RAG framework traces, retrieval store logs | High: required if customer data corpora were the injection or context-poisoning vector |
| **E** | Configuration Snapshot | Customer admin console at the time of incident | Vendor copilot configuration, feature flags, policy state | High: the agent's effective configuration at the incident is the technical baseline for the investigation |
| **D** | Memory Snapshot | (typically not customer-visible) | Vendor memory store, conversation-state retention | High if the copilot retains cross-session memory and the customer's investigation requires it |

### Vendor-specific captures

In addition to A through F:

- **The vendor evidence export request and response chain.** The written request, the vendor's acknowledgment, the export delivery, and any negotiation about scope or format. This document chain is the audit trail for vendor cooperation, separate from the technical evidence.
- **The vendor's incident notification.** If the vendor disclosed an incident affecting the customer's tenant, the notification itself, the timing, and any updates. Capture per the contract's notification requirements.
- **Vendor SLA performance.** Time to escalation acknowledgment, time to evidence export, time to vendor-side containment. These metrics feed [Playbook 18](18-post-incident-hardening.md) hardening and contract renegotiation.
- **Customer-side independent verification.** Where vendor logs claim the agent did X, what does the customer-side audit log of the target system show? Discrepancies between vendor claims and customer-side evidence are findings; they are not resolved by accepting the vendor's account.

**Operational requirement:** the full vendor-copilot evidence set must be exportable within the contracted vendor SLA, with customer-side evidence (Types F partial, plus IdP and gateway logs) exportable within **60 minutes** independent of vendor cooperation. The contracted vendor SLA must be tested quarterly through the vendor evidence drill described below. If the contracted SLA exceeds the customer's regulatory disclosure window, the SLA itself is a [Playbook 18](18-post-incident-hardening.md) hardening item that requires contract amendment.

### The Vendor Evidence Drill

The single highest-leverage preparation for vendor-copilot incident response. Run quarterly per [Playbook 14: Testing for Agent Failure Modes](14-testing-for-agent-failure-modes.md) cadence.

1. **Select a vendor copilot** with access to sensitive workflows (email, CRM, ticketing, code, financial systems). Rotate through all deployed vendor copilots over four quarters.
2. **Schedule a one-hour test window.** Notify the customer's stakeholders and the vendor's named escalation contact. Treat it as a real evidence-export rehearsal, not a synthetic test.
3. **Request the full evidence set** for a defined two-hour window in the recent past. Record: request timestamp, vendor acknowledgment timestamp, evidence delivery timestamp, completeness score.
4. **Review the data quality.** Verify the fields the framework requires are present: user attribution, timestamps, source identifiers, action parameters, retrieval references, configuration state. Identify missing fields against the customer's incident-response requirements.
5. **Run the correlation check.** Compare the vendor's evidence to customer-side IdP logs, target-system SaaS audit, DLP, and SIEM for the same window. Discrepancies between vendor claims and customer-side evidence are findings.
6. **Document and debrief.** Summarize the drill: what the SLA was, what the actual delivery was, what gaps exist between contract and capability. Escalate gaps to the vendor in writing. Update [Playbook 18](18-post-incident-hardening.md) backlog with hardening items. Schedule the next quarter's drill before leaving the room.

This drill produces a more honest picture of vendor-copilot readiness than any procurement checklist. Most customers discover during the first drill that their contracted SLA assumes evidence is available that the vendor cannot actually deliver within the SLA window.

## Recovery Sequence

Vendor-copilot recovery follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **two vendor-specific gates** added.

1. **Confirm customer-side containment is solid.** Before re-enabling, verify the IdP disable and OAuth revocation actually stopped the agent's access. Test by attempting an agent action through a controlled account; expect a clean failure.
2. **Receive vendor confirmation of remediation** (*vendor-specific gate*). The vendor must confirm in writing what was fixed, when, and how it was validated on the vendor side. Verbal confirmation is not sufficient. The confirmation enters the case file.
3. **Validate the vendor's account against independent customer-side evidence** (*vendor-specific gate*). The vendor says the agent's behavior was caused by X and was fixed by Y. Does the customer-side audit log of the target systems support that account? If yes, proceed to step 4. If no, the recovery is paused; the discrepancy is investigated.
4. **Re-enable the vendor copilot in customer-side read-only first.** Re-grant only read-scope OAuth tokens initially. Confirm the copilot functions in observe mode and that customer-side logs flow.
5. **Validate the customer's monitoring before re-granting write scopes.** Confirm the [Playbook 11 (Monitoring)](11-monitoring-detection.md) detection rules for vendor-copilot activity are firing on the recovered traffic. Confirm anomaly thresholds are tightened to mean + 2σ for the post-incident observation window.
6. **Re-grant Tier-1 write scopes incrementally.** Bounded writes first (drafts, internal updates). Monitor for 24 to 72 hours.
7. **Re-grant Tier-2 write scopes one at a time** with [Approvals (M2)](../kill-switches/overview.md) where the vendor supports it. Each Tier-2 re-grant is a separate decision with a separate approver and a separate monitoring window.
8. **Return to M0 Observe** only after the vendor copilot has carried production traffic for 72 hours without anomaly. Lower the [Playbook 11](11-monitoring-detection.md) detection threshold to baseline after 14 days of clean operation.
9. **Update the contract** if the incident revealed an SLA gap. Faster evidence export, named escalation expansion, retention floor increase, or specific containment cooperation timelines all become contract amendment candidates. Contract update is part of recovery, not a follow-up project.

**Approver:** CISO or designated Incident Commander, with General Counsel signing off on the contract-amendment dimension if any. The vendor relationship owner alone is not sufficient. Implementation bias is heightened by the procurement relationship; the recovery decision needs independent containment oversight.

## Post-Incident Hardening

Vendor-copilot hardening organizes around four boundaries. Each has an owner, an artifact, and a measurable acceptance criterion. The four boundaries together convert the "shared responsibility" slogan into a contractually and operationally enforceable discipline.

### Boundary 1: Contract

- **Evidence export SLA** is contractually specified: maximum time from request to delivery, format guarantee (structured JSON or equivalent), completeness commitment, retention floor that exceeds the customer's regulatory window.
- **Named escalation contacts** are specific individuals or dedicated teams with documented coverage hours, not a generic customer support address. The escalation path is documented at contract level so a procurement turnover does not lose it.
- **Containment cooperation timeline** is contractually specified: maximum time for the vendor to activate vendor-side M3-Vendor or M4 containment per customer request, with separate timelines for business hours and after-hours.
- **Incident notification** requires the vendor to notify the customer of incidents affecting the customer's tenant within a contractually defined window (typically 24 hours), with required content: what happened, what was affected, remediation status.
- **Legal hold and retention extension** procedures are contractually specified so the customer can extend vendor retention beyond default during an investigation without per-incident negotiation.

### Boundary 2: Identity

- **The vendor copilot operates under customer-controlled identity.** Every action attributable to the vendor agent traces to a customer-managed OAuth grant or service identity. The vendor does not control the identity authorization.
- **OAuth scopes are minimized to the documented business need.** Wildcard or all-tenant scopes are containment-class findings; they are removed before production deployment.
- **Customer-side scope revocation is rehearsed and timed.** The customer's [Playbook 07 (Secrets and Tokens)](07-secrets-and-tokens.md) credential discipline applies to vendor copilots; the customer can revoke an OAuth grant within the snapshot-narrow-rotate-validate sequence's four-step rhythm.
- **Network-layer containment is available as a last resort.** Egress to vendor copilot API endpoints can be blocked at the customer's network edge if IdP and OAuth disablement do not propagate fast enough.

### Boundary 3: Evidence

- **Customer-side independent verification exists for every vendor-copilot deployment.** The customer's IdP, target-system SaaS audit, DLP, SIEM, and (where applicable) gateway logs are configured to capture the downstream effect of agent actions. The customer's evidence is not dependent on vendor cooperation.
- **The vendor evidence drill runs quarterly** per [Playbook 14](14-testing-for-agent-failure-modes.md). Drill results enter the customer's [Six Metrics](13-six-metrics.md) Metric 3 (Evidence Export Time) trend with the vendor SLA as the data source.
- **Vendor evidence format is normalized to a customer-side schema** where vendor APIs allow it. The normalization layer is the customer's responsibility; it preserves the audit chain when the vendor changes their export format.
- **Retention is contracted and tested.** The customer's IR plan retention windows for prompts (Type A), tool calls (Type B), and configuration (Type E) are honored by the vendor SLA. Where the vendor's default retention is shorter, the contract specifies the extension procedure.

### Boundary 4: Communication

- **Vendor incident notification triggers customer's [Materiality and Disclosure](../framework/04-materiality-and-disclosure.md) call.** A vendor-disclosed incident affecting the customer's tenant is treated as if the customer's own agent had triggered the incident: the convening protocol applies.
- **Customer's regulator disclosure timing is not paused by vendor cooperation timing.** The 4-business-day SEC clock (Form 8-K Item 1.05), the 72-hour NY DFS clock (23 NYCRR Part 500.17(a)), the EU AI Act Article 26 deployer notification obligation, and the downstream Article 73 provider reporting clock (15 days default; 2 days for death or serious harm) all run from the customer's own determination point, not from vendor evidence delivery. The customer's General Counsel decides what to disclose with what evidence; vendor evidence delivery is a parallel track.
- **Customer's external communications use customer's facts, not vendor's account.** Communications to customers, partners, and the press cite customer-side evidence. Vendor-side claims are referenced only after independent verification.
- **The 5-business-day hardening SLA** from [Playbook 18: Post-Incident Hardening](18-post-incident-hardening.md) applies to vendor-copilot findings. Hardening items that require contract amendment are scheduled within the SLA even if the amendment itself takes longer.

## Common Pitfalls

These are the highest-frequency failure modes specific to vendor-copilot incident response. Each has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **"Shared responsibility" not tested** | Procurement signed the MSA; nobody operationalized it | Customer absorbs accountability when vendor evidence is late or incomplete |
| **No named escalation contact** | Vendor sales relationship treated as the support path | First incident contact lands in generic ticket queue; SLA is meaningless without a contact |
| **No quarterly evidence drill** | Drills feel synthetic; the SLA looks fine on paper | Cannot prove readiness until a real incident proves the gap; gap discovered under pressure |
| **Customer-side containment skipped while waiting for vendor** | IR team assumes vendor will act faster than they will | Multi-hour containment of an incident that customer-side IdP could have stopped in 10 minutes |
| **Vendor's account accepted without independent verification** | Vendor cooperation is reassuring; verification feels adversarial | Discrepancies missed; the customer briefs leadership on a partial picture |
| **Contract retention shorter than customer's regulatory window** | Procurement optimized for cost; legal not consulted on retention | Evidence gone before the customer's investigation can complete |
| **OAuth scopes broader than business need** | Vendor SDK or onboarding wizard requests wildcard scopes by default | Compromise of a Tier-0 read scope opens Tier-2 write scope; blast radius matches the broadest authorized scope |
| **Vendor-side containment treated as the only option** | The IR runbook for vendor copilots is "call the vendor" | TTA is bounded by vendor SLA; customer-side identity containment is unavailable when needed |
| **Vendor incident notification ignored** | Notification looks like a vendor marketing email | Customer's regulator clock starts at vendor notification; ignoring it is a disclosure violation |
| **Vendor copilot evidence assumed to satisfy customer's regulatory requirements** | Customer's compliance team trusted the vendor's compliance posture | Regulators evaluate the customer's program, not the vendor's; vendor's compliance is not customer's compliance |
| **Contractual leverage assumed, not measured** | The hardening framework assumes the customer can negotiate evidence-export SLAs, containment-cooperation timelines, and legal-hold extensions into the vendor MSA | Mid-market customers and customers on standard vendor terms often lack this leverage; vendor responds "out of scope" to the requested clauses |

> **When contractual leverage is limited:** the Boundary 1 (Contract) hardening items assume meaningful customer negotiating power. Customers without that leverage (typically mid-market organizations on standard vendor terms, or any customer whose vendor renewal is months away) should treat the Boundary 1 items as **target state at the next contract renewal cycle** and lean harder on the items the customer controls unilaterally: Boundary 2 (Identity) restricting vendor agent OAuth scopes at the customer's IdP, Boundary 3 (Evidence) extending customer-side audit-log retention beyond default, Boundary 4 (Communication) hardening internal escalation paths. The quarterly Vendor Evidence Drill in this lower-leverage variant runs as an **internal-only drill** simulating vendor cooperation failures, until contractual provisions exist to drill against the real vendor.

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md). MVO-1 Inventory extends to documenting every vendor copilot the customer deploys with the same fidelity as customer-managed agents.
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md). Clause 1 (Acts) applies to vendor agents acting in the customer's name. The customer's PAM cadence covers vendor copilot identities.
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md). Vendor copilot maturity tracks customer-side containment readiness and quarterly evidence drill currency.
- **Materiality and Disclosure:** [`framework/04-materiality-and-disclosure.md`](../framework/04-materiality-and-disclosure.md). Vendor-copilot incidents nearly always cross the convening threshold; the convening protocol applies regardless of whether the harmful action originated customer-side or vendor-side.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). The M3-Vendor variant introduced in this playbook documents vendor-controllable granular containment as an extension of M3 Tool Tiering.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). Type F (Identity and SaaS Audit-Log Correlation) is the load-bearing customer-side evidence type for vendor-copilot incidents.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). Every vendor copilot has its own AI-BOM entry with the `identity` section documenting the customer-controlled OAuth grants and the `tools` section documenting the vendor-managed tool list.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The tier discipline applies to vendor-copilot tools through OAuth scope mapping.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The keystone playbook applies to vendor agents; the customer responds to the agent regardless of who manages its model and tooling.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The tier discipline drives OAuth scope minimization for vendor copilots.
- **Playbook 06: Rethinking Prompt Injection as a Workflow Threat** ([`playbooks/06-prompt-injection-workflow.md`](06-prompt-injection-workflow.md)). Vendor copilots that consume customer-supplied content are a workflow-injection target; the architectural defense applies even when the agent is vendor-managed.
- **Playbook 07: Secrets and Tokens** ([`playbooks/07-secrets-and-tokens.md`](07-secrets-and-tokens.md)). Customer-side OAuth grant management is the vendor-copilot equivalent of the credential lifecycle discipline.
- **Playbook 08: Multi-Agent Systems Multiply Blast Radius** ([`playbooks/08-multi-agent-blast-radius.md`](08-multi-agent-blast-radius.md)). Vendor copilots that delegate to other vendor agents inherit the multi-agent cascade discipline.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). Customer-side detection rules for vendor copilots fire on downstream-effect signals because the customer cannot see the agent's internals.
- **Playbook 12: Insider Threat 3.0** ([`playbooks/12-insider-threat-3.md`](12-insider-threat-3.md)). A vendor copilot used by a customer's employee for misuse is the vendor-mediated variant of Insider Threat 3.0; the HR and Legal coordination still applies.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA applies to vendor-copilot hardening, including contract-amendment items that fit within the SLA.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.4 risk-management process documentation including third-party AI, GOVERN 1.6 inventory mechanisms extending to vendor copilots, MAP 4.1 third-party technology and legal risk mapping, MANAGE 2.4 deactivation mechanisms including customer-controllable containment).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports ID.AM-04 inventories of services provided by suppliers, GV.SC supply chain risk management, PR.AA-05 access policies on vendor-managed AI identities, RS.MA-02 incident triage extended to vendor incidents).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the direct operational response for ASI04 Agentic Supply Chain Compromise; also covers customer-side response to ASI03 Identity & Privilege Abuse when the implicated identity is a vendor copilot's OAuth grant).
- **EU AI Act Article 26 (deployer obligations):** the customer is the deployer of a vendor copilot. Vendor is the provider. Article 26(5) requires the customer to keep automatically generated logs for at least 6 months (where the logs are under the customer's control). Article 26 also requires the customer, upon identifying a serious incident, to inform the provider (vendor), distributor, and the relevant market surveillance authority without undue delay, regardless of vendor cooperation status. The provider's separate Article 73 obligation to report the incident to market surveillance authorities (15 days default, 2 days for death or serious harm, 10 days for widespread infringement) runs from the provider's awareness, which the customer's notification triggers.
- **ISO/IEC 42001:2023 Clause 8 (Operation):** vendor copilot deployment falls under the customer's AI management system operations. Clause 8.1 operational planning and control extends to vendor-managed agents the customer relies on.

## The Question to Carry Forward

If a vendor copilot acting in your customer-facing CRM today produced an output that reached an external recipient or touched regulated data, could your team prove what the agent did using customer-side evidence alone within 60 minutes, brief the General Counsel on the materiality determination using facts rather than vendor assurances, and demonstrate that customer-side containment activated within 10 minutes regardless of vendor cooperation timing? Answer the question for the one vendor copilot that has the most sensitive scope. The answer reveals whether the customer's vendor-copilot readiness is real or contracted on paper.

If the answer is improvised, PB10 is the work plan. Run a vendor evidence drill on the highest-scope copilot this quarter. Audit the named escalation contact and the contracted SLA against the customer's regulatory clocks this month. Renegotiate one contract clause that the drill exposed as insufficient this year. Then move to the next vendor copilot in the inventory.

That is how vendor-copilot readiness moves from procurement slogan to operational capability. One vendor, one drill, one contracted SLA at a time, on a cadence that holds.

---

*Source: AI IR Overlay newsletter, Issue #10, "Vendor Copilots and Mutual Responsibility," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
