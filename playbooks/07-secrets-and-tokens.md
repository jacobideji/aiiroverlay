<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Playbook 07: Secrets and Tokens in an Agent World                     -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji                  -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0. See LICENSE file in this package.                -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The credential-discipline playbook. Rotate scopes, not just keys. Capture before rotation. Build the credential lifecycle the framework already assumes.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Playbook 07: Secrets and Tokens in an Agent World

> *Rotating credentials without shrinking scopes is not response. It is refreshing the same blast radius with a different token.*

## Premise

Credential rotation is a standard incident response move: revoke, replace, recover. With AI agents in production, that reflex is dangerously incomplete. AI agents operate under **service identities** with **broad delegated access**, **OAuth grants spanning multiple SaaS tenants**, and **long-lived tokens** sitting in runtime environments. Rotating tokens without first documenting the prior scopes destroys evidence. Rotating tokens without **shrinking scopes** simultaneously fails to reduce risk. Tomorrow's token holds the same dangerous permissions that yesterday's token did. You have refreshed the keys to the same blast radius.

This is the credential-discipline playbook in the AI IR Overlay series. Where [Playbook 01](01-agent-as-privileged-identity.md) establishes that an AI agent with tool access is a privileged identity, this playbook answers the operational follow-up: *how do you actually manage that privileged identity's credentials, and in what order do you operate when the credential is suspect?* The framework's most-cited failure mode lives at the intersection: rotating tokens before snapshotting scopes is the single most common evidence-destruction failure in AI IR. Every shipped playbook references that failure. This is the playbook that prevents it.

Agent credentials come in three classes, each with its own discipline. **Service-account secrets** (long-lived, broadly scoped, often shared) behave like traditional service identities. **Delegated OAuth grants** (issued on behalf of a user, scoped per-resource, with refresh tokens) behave more like federated access. **User-impersonation tokens** (the agent acts *as* a specific user) inherit the user's full blast radius for the impersonation window. Each requires different rotation discipline. Conflating them is the failure mode most CISOs walk into.

**Mental Model clauses engaged:** *Acts* (primary). Every credential is a privileged-access grant, and rotation discipline is the privileged-access management cadence applied to the agent. *Remembers* (secondary), because credentials cached in memory or session state become a separate attack surface. *Changes* (secondary), because rotation is software discipline. Credential rotation that breaks the agent is a deployment failure, not an unavoidable cost.

**Use this playbook when:** an agent's credential is suspected of compromise, an agent's tokens are scheduled for routine rotation, a new agent is being deployed to production, a vendor SDK upgrade changes the agent's OAuth scopes, a credential-event log shows unexpected refresh activity, or a quarterly Privileged Access Management review reaches the agent identities in the AI-BOM.

## First-Hour Actions

The order matters. Reversing step 1 and step 3 below is the failure mode every prior playbook warns against. The 60-minute drill exists to make the order reflexive before you need it.

### The 60-minute four-step sequence

| Minute | Action | Owner |
|---|---|---|
| 0–10 | **Snapshot identity and capabilities before any rotation.** Pull the agent's [AI-BOM](../templates/ai-bom.yaml) `identity` section. If missing fields, write them now. Capture: principal, identity type (service account, delegated OAuth, impersonation), all current scopes, refresh-token lifetime, rotation cadence, downstream API keys, secrets-manager paths. The output is a single time-stamped artifact, not a series of screenshots. | Incident Commander |
| 10–25 | **Narrow privileges immediately.** Before any rotation, reduce the blast radius. Remove write scopes the agent does not need right now. Disable high-risk tool integrations. Enforce approvals on Tier-2 actions per the [Privilege Matrix](../templates/agent-privilege-matrix.csv). This buys time. The business keeps running. The investigation gets clean state. | Agent business owner + Tier-1 SOC |
| 25–45 | **Rotate credentials with documentation.** Now rotate: the agent's primary token, its downstream API keys, all delegated access. Every change goes into a credential-event log with the field set: `who, what, when, prior_scope, new_scope, reason, ticket_id`. The audit trail is the deliverable, not the rotation. | Identity / PAM team |
| 45–55 | **Validate before re-enabling at full scope.** Re-enable in [Mode M1 Read-Only](../kill-switches/overview.md) first. Confirm logs flow with the new identity correctly attributed. Add approvals for Tier-2. Only then restore writes incrementally. | Incident Commander + Agent owner |
| 55–60 | **Update the AI-BOM.** The agent's `identity` section, `kill_switches.tested_at` fields, and `incidents_history` entry must reflect the new credential state within 7 days. If the AI-BOM is not refreshed within 7 days of a credential change, the agent regresses per the Maturity Roadmap operating guidance in [Playbook 20](20-maturity-roadmap.md). | Agent owner |

**Discipline:** if step 3 happens before step 1 is complete, the evidence is degraded. Document the gap. Do not slow the rotation to fix it, but capture the gap as a [Post-Incident Hardening](18-post-incident-hardening.md) item with the 5-business-day SLA.

**Critical sequence rule:** snapshot scopes **before** revocation. After the token is revoked, the SaaS-side audit logs may rotate out of the window where you can correlate. Reading scopes from a revoked OAuth grant is sometimes possible, sometimes not, depending on the identity provider. Capture first. Always.

## Containment Options

Containment for a credential-class incident is **never** binary. The framework's [Kill-Switch Modes](../kill-switches/overview.md) apply with credential-discipline adaptations.

### Mode mapping for credential-class incidents

| Mode | Use when | Credential-specific action |
|---|---|---|
| **M0 Observe** | Routine credential operations | Log every credential lifecycle event (issuance, refresh, revocation) with full identity attribution |
| **M1 Read-Only** | Token is suspect but the agent's read activity is needed for business continuity | Strip write scopes from the active token. Refresh-token issuance disabled. New refreshes blocked. Reads continue. |
| **M2 Approvals Required** | Token must continue serving the business while the investigation narrows scope | Tier-2 tool calls queued for human approval. Approver identity captured alongside the agent identity in the audit log. |
| **M3 Tool Tiering** | Specific scopes are confirmed as the harm vector (typical case: a vendor SDK upgrade silently broadened scopes) | Disable the affected scope class at the identity layer. The agent's other scopes continue. M3 is more surgical at the credential layer than at the tool layer in this scenario. |
| **M4 Full Disable** | Confirmed token compromise with active misuse | Hard stop. **Snapshot scopes BEFORE revocation.** Capture the [Minimum Evidence Set](../evidence/minimum-evidence-set.md) A–F. Only then revoke the token, rotate downstream keys, and prepare fresh identity issuance. |
| **M5 Controlled Re-Enable** | Containment validated, ready to restore | Issue new identity with **narrower** scopes than the prior identity. The rule: if the prior token had write access to five systems, the new one writes to two. Justify the third, fourth, and fifth in writing before adding them back. |

> **The scope-shrink rule:** every credential rotation produces a credential with narrower scopes than the one it replaces, unless the agent owner can justify the prior scope set against current business need. Rotation without justification of the prior scope set is the credential discipline equivalent of "tabletop theater" from [Playbook 14](14-testing-for-agent-failure-modes.md).

### The credential break-glass procedure

For incidents where the credential must be rotated **without** taking the agent fully offline (typical case: customer-facing copilot with revenue impact), pre-position a break-glass procedure:

1. **Issue a parallel credential** with M1 Read-Only scopes from a separate identity pool. The break-glass identity is pre-provisioned, never used in normal operation, and audited at least quarterly.
2. **Switch the agent to the break-glass credential.** The agent operates at reduced scope while the compromised credential is investigated and rotated.
3. **Rotate the original credential** with the full four-step sequence.
4. **Switch the agent back** to the rotated original credential. The break-glass returns to standby.
5. **Document the switch events** in the AI-BOM `incidents_history` with timing.

A break-glass procedure that requires the same credentials being rotated is not a break-glass procedure. Drill it quarterly.

## Evidence Priorities

For credential-class incidents, **Type E (Configuration Snapshot)** and **Type F (Identity and SaaS Audit-Log Correlation)** are load-bearing. Type B (Tool-Call Ledger) is critical for attribution. Types A, C, D are conditional on the specific attack vector.

| Code | Evidence Type | Priority for this scenario | Why |
|---|---|---|---|
| **E** | Configuration Snapshot | **Critical** | The agent's scope set, OAuth consent records, allowlists, and rotation policy at incident time. Without this, you cannot prove what the token could do. |
| **F** | Identity and SaaS Audit-Log Correlation | **Critical** | What the identity actually did across CRM, ERP, email, code repositories, and cloud platforms. The downstream blast radius. |
| **B** | Tool-Call Ledger | **Critical** | Captures attempted calls (denied = evidence of intent) and successful calls with identity attribution. The 24-hour window prior to detection often contains the earliest anomaly. |
| **A** | Prompt and Response Record | High if the compromise vector is prompt injection that elevated the agent's effective scope | Required to prove the agent was instructed to misuse its credentials, distinct from the credentials being directly compromised. |
| **C** | Retrieval Traces | High if a retrieval source delivered a poisoned credential reference | Less common but real: a corpus document leaks a hard-coded token the agent then uses. |
| **D** | Memory Snapshot | High if the credential was cached in agent memory | Memory may carry credential state across sessions if memory `scope: shared`. |

### Credential-specific captures

In addition to the A–F set, capture for credential incidents:

- **OAuth consent records and refresh-token issuance history** from the identity provider (Okta, Entra, Auth0, or the agent's IdP)
- **Secrets-manager access log** (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault). Who pulled which secret, when, from which workload identity.
- **Downstream API rate-limit and quota counters** for the agent's target SaaS systems. Quota anomalies are often the earliest credential-misuse signal.
- **Refresh-token chain history** for delegated OAuth grants. A refresh token that bootstrapped multiple access tokens leaves a chain that's auditable at the IdP layer.

**Retention concern:** identity-provider audit logs often have shorter retention windows than tool-call logs (30–90 days at the IdP versus 180+ days at the application). Pull IdP logs immediately, in parallel with the four-step sequence. Queue the request at minute 25, not minute 55.

**Operational requirement:** the full A–F set plus the credential-specific captures must be exportable within **60 minutes** of incident declaration. If you cannot, you are operating at Maturity Roadmap Level 2 at best for this incident class. Log the gap. See [Playbook 20: Maturity Roadmap (Operating View)](20-maturity-roadmap.md).

## Recovery Sequence

Recovery follows [MVO-4 Controlled Re-Enable](../framework/01-minimum-viable-overlay.md) with **three credential-specific gates** layered in.

1. **Re-enable the agent in Read-Only (M1) on the new credential.** Confirm the agent functions. Confirm logs flow with the new identity correctly attributed across IdP, application, and SaaS audit trails. Identity attribution is the validation, not the agent's response quality.
2. **Validate scope minimization** (*credential-specific gate*). Confirm the new credential's scope set is **narrower** than the pre-incident scope set, or that any retained scope is documented with current business need. Drift between the prior scope set and the new one is itself a finding.
3. **Validate the credential-event log.** Confirm credential lifecycle events (issuance, refresh, revocation) are emitting to the SIEM with the field set the framework expects. If the log was not emitting before the incident, this is a hardening item, not a recovery blocker, but it must be tracked.
4. **Re-enable Tier-1 tools incrementally** with caps at half the pre-incident value for the first 24 to 72 hours. Monitor.
5. **Re-enable Tier-2 tools one at a time** with approvals (M2). Each Tier-2 re-enablement is a separate decision with a separate approver and a separate monitoring window. Do not batch-enable.
6. **Validate the credential break-glass procedure** (*credential-specific gate*). Drill the switch to break-glass and back at least once before declaring recovery complete. A break-glass that was not exercised during recovery is theoretical.
7. **Return to M0 Observe** only after the new credential has carried production traffic for a documented observation window (typically 24 to 72 hours) without anomaly.

**Approver:** CISO or designated Incident Commander. **Never** the agent owner alone, **never** the engineer who set up the credential originally. The original engineer has implementation bias.

## Post-Incident Hardening

Credential discipline is one of the highest-leverage hardening categories because the controls are mature (PAM has been a discipline for 25 years) but the AI-agent translation is recent. Every hardening item below has a measurable acceptance criterion.

### Boundary 1: Credential lifecycle

- **Pre-document rotation cadence per identity in the AI-BOM.** Tier-0 tools: 90 days. Tier-1 tools: 60 days. Tier-2 tools: 30 days. Break-glass identities: never used in normal operation, rotated quarterly regardless.
- **Shorten refresh-token lifetimes.** Replace year-long refresh tokens with hours-long where the IdP supports it.
- **Implement just-in-time credential issuance** for sensitive integrations. The agent requests a credential when it needs one, returns it when finished. The credential's lifetime is the operation, not the calendar.

### Boundary 2: Scope discipline

- **Separate identities per tool tier.** One service identity for Tier-0 reads, a different identity for Tier-1 bounded writes, a third for Tier-2 systems of record. Compromise of one does not compromise the others.
- **Tighten OAuth scopes to the smallest set the business need supports.** Most vendor SDKs request broader scopes than the integration requires by default. Pin the scopes per integration in the AI-BOM.
- **Review scope creep quarterly** in the same review where the [AI-BOM is refreshed](20-maturity-roadmap.md). A scope added six months ago for a project that was deprioritized is a scope that no longer has business justification.

### Boundary 3: Telemetry

- **Credential lifecycle events emit to the SIEM.** Issuance, refresh, revocation, scope change. Field set: `agent_id, principal, event_type, prior_scopes, new_scopes, timestamp, actor, justification, ticket_id`.
- **Identity attribution in tool-call logs.** Every tool call carries the principal that authorized it. Without this, [Playbook 11: Monitoring](11-monitoring-detection.md) cannot correlate credential events to tool actions.
- **Downstream quota and rate-limit telemetry.** SaaS-side API quotas often signal credential misuse before application-side detection catches it. Wire them into the same SIEM as credential lifecycle events.

### Boundary 4: Procedure

- **Break-glass procedure exists, is documented, and is drilled quarterly.** The drill output is the credential-event log showing the switch and switch-back, with timing.
- **The 5-business-day hardening SLA** from [Playbook 18](18-post-incident-hardening.md) applies. Credential gaps surfaced in this playbook do not wait for the next quarter to close.

## Common Pitfalls

These are the highest-frequency failure modes specific to credential discipline for AI agents. Each one has been observed often enough to name as a pattern.

| Pitfall | Why it happens | Consequence |
|---|---|---|
| **Rotate first, document scopes later** | "Stop the bleeding" reflex from traditional IR | Cannot prove what the prior token could do. Scope becomes a guess. |
| **Rotate with identical scopes** | The rotation runbook says "issue replacement token"; nobody questions the scope set | Same blast radius, fresh token. False security. The next incident proves it. |
| **One service identity for all tool tiers** | Convenient. Procurement-friendly. One vendor relationship to manage. | Compromise of a Tier-0 read scope leaks Tier-2 write access. The blast radius is the highest-tier scope on the identity. |
| **Long-lived tokens with broad scopes** | The IdP supports year-long refresh; nobody narrows it | A single credential leak compromises the environment for months. Detection is harder. Rotation under pressure is riskier. |
| **OAuth scopes baked into vendor SDK with no narrowing** | The SDK requests the maximum scopes the vendor supports by default | The agent has scopes it never uses. A future code change activates those scopes silently. |
| **Skipping the AI-BOM update after credential rotation** | The rotation closed the incident; "next sprint" handles the inventory | Inventory drifts from reality. The next incident scope is a guess. Maturity claim drifts to Level 1 by definition. |
| **Break-glass procedure that requires the same credentials being rotated** | Bootstrapping problem nobody surfaces until they need it | When the rotation fails or the IdP itself is suspect, there is no path back. Manual ticket-based recovery becomes the failure mode. |
| **Hard-coded service-account secrets in deployment manifests** | Convenient for the engineering team; "we'll move to secrets manager next sprint" | A Git history breach leaks the credential. The credential outlives the engineer who set it up. |
| **No identity attribution in tool-call logs** | The logging schema was designed for human users; the agent identity field was an afterthought | Cannot correlate credential events to tool actions. The investigation operates on inference, not evidence. |
| **No credential-event log at all** | The IdP has audit logs; the assumption is those are sufficient | They are not. IdP logs miss application-side credential operations (cache hits, refresh failures, secrets-manager pulls). Without an application-side log, the picture is partial. |

## Related

- **The Minimum Viable Overlay:** [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md) (MVO-1 Inventory `identity` section is this playbook's primary artifact).
- **The Mental Model:** [`framework/02-mental-model.md`](../framework/02-mental-model.md) (clause 1: *if it can act, govern it as a privileged identity*).
- **The Maturity Roadmap:** [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md) and the operating view in [Playbook 20](20-maturity-roadmap.md). Credential discipline freshness drives the Level 1 claim.
- **Kill-Switch Modes:** [`kill-switches/overview.md`](../kill-switches/overview.md). M4 Full Disable requires the scope-snapshot before revocation. M5 Re-Enable validates scope minimization.
- **Minimum Evidence Set:** [`evidence/minimum-evidence-set.md`](../evidence/minimum-evidence-set.md). Types E (configuration), F (identity correlation), and B (tool-call ledger with identity attribution) are load-bearing for credential incidents.
- **AI-BOM template:** [`templates/ai-bom.yaml`](../templates/ai-bom.yaml). The `identity` section is the primary source of truth for credential discipline. The `incidents_history` records the rotation chain.
- **Agent Privilege Matrix:** [`templates/agent-privilege-matrix.csv`](../templates/agent-privilege-matrix.csv). The tier discipline this playbook applies to credential scope.
- **Playbook 01: The Agent Is a Privileged Identity** ([`playbooks/01-agent-as-privileged-identity.md`](01-agent-as-privileged-identity.md)). The lens this playbook operationalizes.
- **Playbook 04: Tool Design Is Containment** ([`playbooks/04-tool-design-is-containment.md`](04-tool-design-is-containment.md)). The tier model that makes scope shrinking possible.
- **Playbook 14: Testing for Agent Failure Modes** ([`playbooks/14-testing-for-agent-failure-modes.md`](14-testing-for-agent-failure-modes.md)). The M4 drill discipline that exercises this playbook's snapshot-before-rotation sequence.
- **Playbook 18: Post-Incident Hardening** ([`playbooks/18-post-incident-hardening.md`](18-post-incident-hardening.md)). The 5-business-day SLA credential-gap closure inherits.
- **Playbook 20: Maturity Roadmap (Operating View)** ([`playbooks/20-maturity-roadmap.md`](20-maturity-roadmap.md)). The cadence that holds credential discipline honest over time.
- **Playbook 11: Monitoring That Truly Detects Agent Incidents** ([`playbooks/11-monitoring-detection.md`](11-monitoring-detection.md)). The detection rules that consume this playbook's credential-event log. The three signal families (action, influence, capability) include the capability-based family that directly fires on credential lifecycle events.
- **NIST AI RMF crosswalk:** [`crosswalks/nist-ai-rmf.md`](../crosswalks/nist-ai-rmf.md) (this playbook supports GOVERN 1.6, MAP 4.1, MANAGE 1.3).
- **NIST CSF 2.0 crosswalk:** [`crosswalks/nist-csf-2.md`](../crosswalks/nist-csf-2.md) (this playbook supports PR.AA-01, PR.AA-05, ID.AM-04).
- **OWASP Agentic Top 10 crosswalk:** [`crosswalks/owasp-agentic-top-10.md`](../crosswalks/owasp-agentic-top-10.md) (this playbook is the direct operational response to ASI03 Identity & Privilege Abuse and ASI04 Agentic Supply Chain Compromise).

## The Question to Carry Forward

If your most privileged AI agent had its credentials rotated for an unrelated reason today, would your incident-response process still work, or does it depend on a token that should not exist? Answer it for the one agent that scares you most. The answer reveals whether the framework's discipline is real or assumed.

If the answer is "it depends on the current token," PB07 is the work plan. Snapshot the scopes. Narrow the privileges. Rotate with documentation. Validate before re-enabling at full scope. Then make the snapshot-narrow-rotate-validate sequence the muscle memory your team has, not the diagram in the runbook.

That is how credential discipline moves from documented to demonstrated. One agent, one rotation, one shrunk scope at a time, on a cadence that holds.

---

*Source: AI IR Overlay newsletter, Issue #7, "Secrets and Tokens in an Agent World," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
