# Changelog

All notable changes to the AI IR Overlay framework live here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/spec/v2.0.0.html).

During the `v0.x` series, each substantive content drop ships as its own MINOR release. `v1.0.0` arrives once the framework core is stable, the remaining playbooks are live, and a Steering Committee is in place.

## [Unreleased]

### Planned

- Remaining playbooks: 05, 09, 15, 16, 17, 19, 21, 22, 23
- Additional crosswalks: CIS Controls, SOC 2, HIPAA, and a companion NIST SP 800-61 r3 ↔ AI IR Overlay crosswalk (referenced from `crosswalks/nist-csf-2.md`)
- Printable Board Scorecard template (`templates/board-scorecard.md`)
- Steering Committee announcement (cuts `v1.0.0`)

## [0.14.1] · 2026-06-28 · Calibration Pass + Reference Validator

### Added

- `scripts/validate.py`: Python 3 reference validator that runs every AI-BOM YAML and Privilege Matrix CSV in `templates/` against the JSON Schemas in `schemas/`. Validates clean against the worked examples shipped with the framework. Supports a `--schemas-dir` flag and accepts arbitrary file paths so adopters can drop the script into their own CI.
- `.github/workflows/validate-templates.yml`: GitHub Actions workflow that runs `scripts/validate.py` on every pull request and push to `main` touching `templates/`, `schemas/`, or the script itself. Demonstrates the schemas as live CI artifacts rather than static documentation.

### Changed

- `README.md` Provenance section reworded to remove the "field-tested" claim. The framework has not yet been deployed in a documented production AI incident; adopters who use it in a real incident are now invited to submit anonymized case studies via GitHub Discussions.
- `README.md` reading order extended to item 11 (reference validator).
- `GOVERNANCE.md` restructured to separate **current governance (v0.x)** from **future governance (v1.0.0 and beyond)**. The Steering Committee, Working Group Leads, certification program, and `CONTRIBUTORS.md` are now explicitly labeled as not-yet-established, conditional on v1.0.0 readiness and community adoption.
- `CHANGELOG.md` "Why now" sections for `v0.12.0` and `v0.13.0` rewritten to remove unverifiable reviewer-attribution language. References to "SEC enforcement counsel, EU AI Act regulator, plaintiff's expert, and CISO reviewers" are replaced with the maintainer's own analysis based on the cited statutory and standards sources. The "dominant 2026 production deployment pattern" market-claim phrasing is softened to "a common 2026 deployment pattern" given the absence of supporting analyst data.
- `CONTENT_MAP.md` adds a Reference implementations section.

### Why now

The v0.14.0 ship brought the framework to a coherent baseline (schemas + crosswalks + 14 playbooks). A hostile-critic review identified a calibration gap: the framework's positioning (governance scaffolding for a multi-party project, "field-tested" claim, unverifiable reviewer attribution) exceeded the project's actual scale (single-maintainer pre-1.0 synthesis with no documented production deployments). v0.14.1 closes that gap so the framework's presentation matches its real state, and ships a working reference validator so the schemas can be cited as live CI artifacts rather than static specifications.

## [0.14.0] · 2026-06-28 · Schemas Directory: Machine-Readable Contracts

### Added

- `schemas/ai-bom.schema.json`: JSON Schema 2020-12 for the AI Bill of Materials. Encodes the [`templates/ai-bom.yaml`](templates/ai-bom.yaml) contract as a machine-validatable artifact. Enforces the T0/T1/T2 risk-tier vocabulary (aligned with the Privilege Matrix), the 10-minute Kill-Switch Mode TTA bound, the 60-minute Evidence Set bound, and the conditional CI rule that write tools must declare `write_targets`. The `$id` resolves to `https://aiir.jacobideji.com/schemas/ai-bom.schema.json` for adopter CI pipelines.

- `schemas/privilege-matrix.schema.json`: JSON Schema for a single Privilege Matrix CSV row. Encodes the three CI rules from [Playbook 04 (Tool Design Is Containment)](playbooks/04-tool-design-is-containment.md) as conditional schema constraints: T2 rows must carry `approval_required=yes`; T2 rows must carry a non-empty `reversible` value that is not `n/a`; every write row must declare non-empty `write_targets`. CSV consumers convert each row to a JSON object and validate against this schema as the runtime equivalent of the playbook's pre-incident review.

- `schemas/credential-event.schema.json`: JSON Schema for a single credential-event log entry. Operationalizes the upstream contract specified in [Playbook 07 (Secrets and Tokens)](playbooks/07-secrets-and-tokens.md) Boundary 3 (Telemetry) and consumed by [Playbook 11 (Monitoring)](playbooks/11-monitoring-detection.md) Family 3 (capability-based signals). Specifies nine required fields including `agent_id` (joins to the AI-BOM), `prior_scopes` and `new_scopes` (deterministic scope-diff computation), `actor`, `justification`, and `ticket_id` (audit-trail discipline). The `event_type` enum splits PB07's prose `scope_change` category into `scope_expansion` and `scope_reduction` for detection clarity. Semantic constraint: revocation events must end with empty `new_scopes`.

- `schemas/kill-switch-api.md`: the runtime contract for Mode M0 through M5 activation. RFC 2119 conformance language (29 MUST, 6 SHOULD, 1 MAY) specifies the four API surfaces (Activate, Status, Deactivate, Probe) and the six per-mode contracts. Documents the four M3 containment variants (M3-RAG, M3-Delegation Cap, M3-Workflow, M3-Vendor) and the M4 corpus-scoped and Agent-suspended-for-user variants introduced across PB03, PB06, PB10, and PB12. TTA is measured as the elapsed time between `Activate.requested_at` and `Activate.effective_at` (the drill-measured definition from [`framework/01`](framework/01-minimum-viable-overlay.md) Measurement Scope). Eight-test conformance suite included for adopter validation.

- `schemas/evidence-export.spec.md`: the contract for the Type A through F evidence export script referenced in [Minimum Evidence Set](evidence/minimum-evidence-set.md) and [Playbook 13 Metric 3](playbooks/13-six-metrics.md). RFC 2119 conformance language (34 MUST, 7 SHOULD, 3 MAY) specifies pre-staged access (the script cannot ask for credentials at incident time), parallel-export discipline (the 60-minute drill-measured bound is parallelism-dependent), telemetry emission (four events feeding PB13 Metric 3), and the export bundle's manifest, integrity hash, and chain-of-custody attestation requirements. Eight-test conformance suite included for adopter validation.

### Changed

- `CONTENT_MAP.md`: new "Schemas" section added between Templates and the Drafted but unshipped notes. Lists all five schemas with their repository locations and `v0.14.0` shipped status.

- `README.md`: reading order extended to include the new schemas directory. The schemas are the machine-readable contracts adopters consume in CI to validate their AI-BOM, Privilege Matrix, and credential-event logs against the framework's normative rules.

### Why now

The framework's prior releases ship the playbooks (the narrative discipline) and the templates (the human-readable starting points). The schemas directory ships the **machine-readable contracts** that connect adopter CI pipelines to the framework's normative rules. Before v0.14.0, an adopter editing their AI-BOM YAML or Privilege Matrix CSV had no automated way to verify the file still satisfied the framework's CI rules. The risk-tier vocabulary could drift from T0/T1/T2 to "low/medium/high". A T2 row could ship to production without `approval_required=yes`. A write tool could ship without declared `write_targets`. The schemas close that gap: the same CI rules that appear as English prose in the playbooks now appear as JSON Schema conditional constraints that any modern validator can enforce.

The two markdown specs (`kill-switch-api.md` and `evidence-export.spec.md`) close a parallel gap on the runtime side. Before v0.14.0, the Kill-Switch Mode M0 through M5 ladder was specified by behavior and TTA target, but not by API surface. Adopters building their own kill-switch automation had to derive the API from the playbooks. PB10's vendor copilots showed why the API surface needed formal specification: vendor-provided granular containment must be testable against a common contract. The Kill-Switch API spec and the Evidence Export Script spec together formalize the runtime contracts that PB13 Metric 2 (Time-to-Safe-Mode) and PB13 Metric 3 (Time-to-Evidence) implicitly measure against.

The schemas are not a new framework chapter. They are the machine-readable encoding of contracts that already exist in the narrative framework. The shipping discipline is the same as the rest of the repository: the schemas trace back to the playbooks that specify their rules, the playbooks trace back to the newsletter issues, and the newsletter issues trace back to the operational practice. Adopters now have CI-ready artifacts they can drop into their existing validation pipelines without writing custom validators against framework prose.

## [0.13.0] · 2026-06-28 · Playbook 10: Vendor Copilots and Mutual Responsibility

### Added

- `playbooks/10-vendor-copilots.md`: the vendor-copilot playbook. Operationalizes the customer's response when the agent is managed by the vendor. Reframes "shared responsibility" from procurement slogan to testable operational capability through three disciplines: vendor copilots must be deployed behind a customer-controlled identity boundary, contracted with explicit evidence and containment SLAs, and rehearsed quarterly through the Vendor Evidence Drill. Introduces the M3-Vendor containment variant for vendor-controlled granular containment. Specifies the customer-first containment principle (customer-controllable containment activates immediately; vendor escalation runs in parallel, not first), the independent-verification rule for evidence (never trust only vendor logs; correlate with customer-side IdP and target-system audit), and the four-boundary hardening framework (contract, identity, evidence, communication). Ten common pitfalls including untested shared responsibility, vendor-side containment treated as the only option, contract retention shorter than the customer's regulatory window, and OAuth scopes broader than business need.

### Changed

- `CONTENT_MAP.md`: Issue 10 status promoted from drafted to shipped at `v0.13.0`.

- `README.md`: playbook reading order updated to thirteen → fourteen shipped playbooks; PB10 added to the Operations arc bucket as the vendor-and-supply-chain entry.

### Why now

PB10 closes one of the two largest gaps the maintainer identified in the framework's coverage of 2026 production deployment patterns. Vendor copilots (Microsoft 365 Copilot, Salesforce Einstein, ServiceNow Now Assist, Google Workspace Gemini, GitHub Copilot, and the embedded copilots increasingly built into CRM, ERP, and ticketing platforms) are a common 2026 deployment pattern for AI agents in regulated enterprises. The framework's existing playbooks assumed customer-managed agents; PB10 ships the operational discipline for the case where the customer is responsible to the regulator but the vendor controls the agent's operational levers.

PB10's defensive thesis (deploy behind customer-controlled identity boundary, contract for testable evidence and containment SLAs, rehearse quarterly through the Vendor Evidence Drill) is the framework's first formal supply-chain response playbook. It maps directly to OWASP Agentic Top 10 ASI04 (Agentic Supply Chain Compromise), NIST CSF 2.0 GV.SC (supply chain risk management), and the EU AI Act provider/deployer distinction. Customers acting as deployers of vendor-provided AI systems can now point at a specific operational playbook when responding to regulator inquiry or auditor question about vendor copilot incident readiness.

The Materiality and Disclosure integration (from v0.12.0) extends naturally to vendor-copilot incidents: vendor incidents nearly always cross the convening threshold because external recipients (the vendor and downstream customers) are touched. PB10 makes that convening call explicit in its First-Hour Actions section.

## [0.12.0] · 2026-06-28 · Playbook 06 + Materiality and Disclosure

### Added

- `playbooks/06-prompt-injection-workflow.md`: the workflow-injection playbook. Reframes prompt injection from a chat-UI risk to a workflow attack: harmful instructions hidden inside the everyday content the agent already reads (tickets, emails, web pages, ingested documents). Introduces the M3-Workflow containment variant that pauses content-channel ingestion while preserving the agent's other capabilities. Specifies the source-artifact preservation discipline (the quarantine sequence that preserves the attack ticket or document as primary evidence), the architectural-defense pattern (untrusted content never directly triggers Tier-2 tools), and the four-boundary hardening framework (tool architecture, content trust labeling, approval gates, detection). Ten common pitfalls including the prompt-engineering theatrical fix, output-only detection that misses the retrieval vector, and vendor copilots assumed to handle injection internally.

- `framework/04-materiality-and-disclosure.md`: the Materiality and Disclosure annex. Establishes the convening protocol (CISO + General Counsel + Incident Commander) triggered at Kill-Switch Mode M3 or higher, the four-question walkthrough that decides whether a regulatory disclosure clock has started, and the three outcomes (not material, material, determination cannot be made yet). Cites SEC Item 1.05 (4-business-day clock), EU AI Act Article 26(7) (15-day reporting), NY DFS 23 NYCRR Part 500.17(c) (72-hour notification), and HIPAA 45 CFR §164.408. Frames materiality determination as procedural discipline, not legal authority.

- README "Scope" section: declares the framework operationalizes deployer obligations under EU AI Act Article 3. Lists four explicit out-of-scope categories (provider obligations, GPAI provider obligations, prohibited practices, conformity assessment). Names vendor copilots as in-scope for the deployer (customer side).

- `framework/01` "Measurement Scope" section: distinguishes drill-measured SLA targets (5-minute inventory, 10-minute Mode M1-M5, 60-minute Evidence Set) from live-incident timing. Live timing is tracked under PB13 Metric 2 and 3. Live-incident timing variability is expected and tracked, not a conformance failure.

### Changed

- `kill-switches/overview.md`: TTA definition expanded with drill-measured qualifier. Targets define readiness; live measurement reveals operational reality. A live TTA above target enters PB18 hardening, not a conformance failure.

- `playbooks/01-agent-as-privileged-identity.md`: First-Hour Actions section adds the Materiality and Disclosure trigger. When Question 5 lands on Mode M3 or higher (or the named trigger conditions in framework/04 apply), the Incident Commander convenes the materiality call within one hour.

- `playbooks/18-post-incident-hardening.md`: First-Hour Actions section adds the Materiality verification callout. Before the Fix List ships, the Incident Commander confirms the materiality determination was captured in the decision log. If missing or incomplete, hardening pauses and the 5-business-day SLA does not run.

- `playbooks/24-board-ready-scorecard.md`: adds C3 scorecard item (materiality determination documented for every incident reaching Mode M3 or higher). Scoring guidance bumps from 10 to 11 items; thresholds adjust proportionally (0-3 strong, 4-7 exposed, 8+ urgent).

- Framework metadata refresh and cross-document consistency closure: CITATION.cff bumped to v0.11.0; SECURITY.md Supported Versions table refreshed; CONTRIBUTING.md style guide updated; PB13 Metric 2/3 carry TTSM/TTE canonical aliases reconciling with PB18 and PB20; PB14 recovery sequence reconciled with kill-switches/overview.md M5 order; PB24 body section order rearranged to match the declared A-B-C-D domain flow; PR.AT-01 row added to the NIST CSF 2.0 crosswalk to support PB12's citation; concentrated Tier-2 rule defined inline in PB08; README playbook reading order restructured into the CONTENT_MAP arc; kill-switches Mode Variants subsection added to catalog M3-RAG, M3-Delegation Cap, M4 corpus-scoped, and Agent-suspended-for-user variants.

### Why now

PB06 closes one of the largest gaps the maintainer identified in the framework's previous releases. Indirect prompt injection in workflow form (harmful instructions hidden in tickets, emails, web pages, and ingested documents the agent reads as part of normal operation) is a distinct attack surface from the chat-UI form that earlier framework releases addressed in passing. PB06 ships the architectural-defense framing (untrusted content never directly triggers Tier-2 tools) as an alternative to the prompt-engineering posture common in published competing frameworks.

The Materiality and Disclosure block addresses a gap the maintainer's review of SEC Item 1.05, EU AI Act Article 26/73, NY DFS Part 500, and HIPAA §164.408 surfaced: prior framework releases shipped containment and evidence machinery but did not specify the convening protocol that determines whether a regulatory disclosure clock has started. The four-file chain (framework/04 authority, PB01 trigger, PB18 verification, PB24 governance signal) operationalizes the discipline across the response arc.

The Scope declaration and the Measurement Scope qualifier are the framework's first formal defensive language additions. They bound the framework's claims to a specific regulatory role (deployer obligations) and a specific measurement context (drill-measured targets, not live-incident performance). Both are the load-bearing language a publicly-traded adopter needs in their 10-K to defensibly cite framework conformance.

The metadata and cross-document consistency work brings the framework to a coherent v0.12.0 baseline. Twelve releases of patches, ghost references, stale version anchors, and contradictory cross-doc citations are reconciled.

## [0.11.0] · 2026-06-28 · Playbook 12: Insider Threat 3.0 (AI-Driven Misuse)

### Added

- `playbooks/12-insider-threat-3.md`: the AI-driven insider misuse playbook. Covers two scenarios that prior insider threat generations conflate or miss: the human-with-agent insider (a user with legitimate access uses an AI agent to compile or exfiltrate at scale) and the agent-as-insider (the AI agent itself drifts or is compromised, operating against organizational intent). Specifies the capability vs intent vs impact investigator triad, HR and Legal joint engagement from minute zero, the intent vector as a load-bearing AI-BOM artifact, the intent-realignment gate in recovery, and the soft cap / hard cap discipline for bulk-summarize attacks. Ten common pitfalls including conflating capability with intent, suspending the user before HR/Legal concurrence, and UEBA models tuned for humans missing agent-mediated actions.

### Changed

- `framework/02-mental-model.md` Related section: the Insider Threat 3.0 (Playbook 12) reference upgraded from "forthcoming" to a direct link. **All forthcoming references in the framework's foundational chapters are now closed.**

### Why now

PB12 closes the last remaining forthcoming reference in the framework's foundational chapters (the Mental Model's Related section). After this release, a reader following the foundational arc (README → Mental Model → Maturity Roadmap → MVO) hits zero unfinished references. The framework's foundational narrative reads as complete.

PB12 also completes the rogue-agent coverage arc. [Playbook 11](playbooks/11-monitoring-detection.md) covers detection of capability-family signals that suggest rogue behavior; PB12 covers the response and investigation when those signals fire. The two playbooks form a matched detection-response pair, the same upstream-downstream pattern PB07 → PB11 → PB08 established.

PB12's "Insider Threat 3.0" framing positions the framework ahead of the analyst category formation. Insider Threat 1.0 (humans with credentials, DLP era) and Insider Threat 2.0 (humans with anomalous behavior, UEBA era) are addressed by mature programs. The 3.0 generation, where AI agents mediate or constitute the insider action, is the rising 2026 CISO concern. PB12 ships the operational playbook before the category solidifies.

## [0.10.0] · 2026-06-26 · Playbook 08: Multi-Agent Systems Multiply Blast Radius

### Added

- `playbooks/08-multi-agent-blast-radius.md`: the multi-agent playbook. Specifies the multiplicative blast-radius thesis (one compromised agent's output becomes every downstream agent's input), the orchestrator-first containment sequence, the agent-dependency graph as an AI-BOM artifact, structured handoff contracts between agents, bounded delegation at 2 hops, trace IDs as the across-agents evidence requirement, the 5-to-30-second cascade propagation window and sub-60-second containment latency, the four-boundary hardening framework (topology documentation, inter-agent contracts, bounded delegation, telemetry), and ten common multi-agent pitfalls.

### Changed

- OWASP Agentic Top 10 crosswalk Status section updated. All 10 ASI categories now have substantive playbook coverage with direct references. ASI07 (Insecure Inter-Agent Communication) and ASI08 (Cascading Agent Failures) detailed mappings updated to reference Playbook 08 as the operational layer.

### Why now

PB08 closes the last remaining OWASP Top 10 for Agentic Applications category. With this release, the framework has substantive playbook coverage of **all 10 OWASP ASI categories AND all 6 NIST CSF 2.0 functions**. Combined with the v0.9.0 CSF DETECT closure, v0.10.0 reaches the v1.0.0-ready standards posture.

PB08 also extends the upstream-downstream contract pattern established by PB07 → PB11. Multi-agent topologies inherit the credential-event log schema from PB07 (each agent is a separate identity, no permission inheritance) and consume PB11 detection rules for inter-agent traffic anomalies.

## [0.9.0] · 2026-06-25 · Playbook 11: Monitoring That Truly Detects Agent Incidents

### Added

- `playbooks/11-monitoring-detection.md`: the detection playbook. EDR was built for malware, anomalous process trees, and lateral movement. AI agents act through authorized channels and look like normal operation to the SIEM. PB11 specifies the three signal families (action-based, influence-based, capability-based) that catch what traditional monitoring misses, the 60-minute first-rule drill, the detection-to-containment latency requirement (under 60 seconds), and the four-boundary hardening framework (signal sources, rule logic, latency and routing, procedure).

### Changed

- NIST CSF 2.0 crosswalk Status section updated. The DETECT function (DE.CM continuous monitoring) deferral is closed. All six CSF 2.0 functions now have substantive playbook coverage.
- `playbooks/07-secrets-and-tokens.md` Related section: PB11 reference upgraded from "forthcoming" to a direct link. The hardening section's identity-attribution requirement is now backed by a live downstream consumer.

### Why now

PB11 closes the last remaining NIST CSF 2.0 deferral. With this release, the framework has substantive playbook coverage of all six CSF 2.0 functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER). PB11 also consumes the credential-event log schema specified in [Playbook 07](playbooks/07-secrets-and-tokens.md), honoring the upstream-downstream contract PB07 established. The framework's IR loop (identify, protect, detect, respond, recover, improve) is now operationally complete.

PB11 covers OWASP ASI06 (Memory & Context Poisoning detection), ASI08 (Cascading Agent Failures early detection), and ASI10 (Rogue Agent drift detection).

## [0.8.0] · 2026-06-24 · Playbook 07: Secrets and Tokens in an Agent World

### Added

- `playbooks/07-secrets-and-tokens.md`: the credential-discipline playbook. Covers three credential classes (service-account secrets, delegated OAuth grants, user-impersonation tokens), the 60-minute snapshot-narrow-rotate-validate sequence, the scope-shrink rule, the break-glass procedure for credential-only containment without taking the agent offline, four-boundary hardening (lifecycle, scope, telemetry, procedure), and ten common credential pitfalls observed across engagements.

### Why now

PB07 closes the largest implicit gap in the live framework. Every shipped playbook references token rotation (PB01 names it as "the single most common evidence-destruction failure in AI IR"), yet no playbook specified the agent-specific PAM cadence, rotation discipline, OAuth grant lifecycle, or break-glass procedure. PB07 fills the gap. It also closes the NIST CSF 2.0 PR.AA-05 standards gap that was explicitly documented as deferred in the CSF crosswalk Status section.

PB07 directly extends [Playbook 01](playbooks/01-agent-as-privileged-identity.md)'s privileged-identity lens with the credential-management operational discipline that lens implies. PB11 (Monitoring, forthcoming) will consume the credential-event log this playbook specifies.

## [0.7.0] · 2026-06-24 · Playbook 20: AI IR Maturity Roadmap (Operating View)

### Added

- `playbooks/20-maturity-roadmap.md`: the operating view of the Maturity Roadmap. Covers the four-quarter cadence (weekly, monthly, quarterly, annual), the level-to-containment realism mapping, the 30-minute single-agent reality check, the four-quarter improvement loop, and the ten operating pitfalls that turn a maturity program into documentation theater.
- Maturity Roadmap framework view (`framework/03-maturity-roadmap.md`) now points readers at PB20 for execution. The two prior "forthcoming" notes are removed.
- CONTENT_MAP.md Issue 20 row updated to show the operating view as shipped.

### Why now

PB20 completes the measurement and discipline triad with [Playbook 13 (Six Metrics)](playbooks/13-six-metrics.md) and [Playbook 14 (Testing for Agent Failure Modes)](playbooks/14-testing-for-agent-failure-modes.md). Together these three carry the Level 4 (Resilient) maturity claim from aspiration to operating reality.

## [0.6.2] · 2026-06-23 · Structural Cleanup

Documentation accuracy and navigation polish. No framework substance changes.

### Fixed

- Misrouted link in `playbooks/01-agent-as-privileged-identity.md` line 111. The "Playbook 18" reference now resolves to the actual playbook (was pointing to the CSF 2.0 crosswalk by mistake).
- "Minimum Viable Overlay" link in `templates/README-ai-bom.md` repointed from `jacobideji.com` to the in-repo file.

### Changed

- 46 backtick-package-slug references across 12 files converted to relative file paths. Closes the residue from the original "ships as separate packages" distribution model.
- 5 forthcoming-playbook references (PB12, PB15, PB20, PB23) rewritten as "forthcoming, see CHANGELOG" notes instead of citing them as live packages.
- Evidence-letter notation normalized to A–F (en dash) across the repo. 12 outliers (A to F, A-F hyphen, A through F) all aligned.

### Added

- New "RAG-specific containment" note in `kill-switches/overview.md` Mode 3, pointing to Playbook 03 for the freeze-the-world sequence.
- Inbound links added for the previously underwoven playbooks: PB13 now referenced from PB18, PB24, and the Maturity Roadmap Level 4 row. PB03 now referenced from kill-switches Mode 3, evidence Type C, and OWASP ASI06.
- Printable triage card now linked from `triage/six-questions.md`.

## [0.6.1] · 2026-06-23 · Documentation Polish

Accuracy and OSS-convention round. No framework substance changes.

### Fixed

- `SECURITY.md` Supported Versions table bumped from `v0.1.x` to `v0.6.x`. The version table was stale and didn't reflect the actual current release.
- `CODE_OF_CONDUCT.md` enforcement section: "at via" template artifact replaced with "via".
- `README.md` "widely-understood" hyphenation corrected to "widely understood" (predicate adjective).
- `README.md` reading order items 1 through 6 converted from package slugs to real relative file paths.

### Added

- `README.md` now carries License, Latest Release, and Standards badges.
- `README.md` Acronyms list now includes TTE (Time-to-Evidence) and TTSM (Time-to-Safe-Mode).
- `CHANGELOG.md` (this file): Keep-a-Changelog format covering all 11 releases.
- `GOVERNANCE.md`: roles, decision-making, release cadence, trademark.
- `CONTENT_MAP.md`: newsletter issue to repo destination map with arc-based ship order.

### Changed

- Repo-wide humanization pass: em-dash density reduced from 1.0 to 7.6 per 100 words (worst-case) down to 0.08 per 100 words across the whole repo. Style guide target is 0.5.

## [0.6.0] · 2026-06-23 · Measurement Release

### Added

- Operational guidance for measuring AI incident response posture across the four MVO controls.
- `playbooks/13-six-metrics.md`: the six metrics that turn maturity from an adjective into a number.
- `playbooks/14-testing-for-agent-failure-modes.md`: how to test Kill-Switch modes M1 through M4 before you need them.
- `playbooks/03-rag-knowledge-base-forensics.md`: the freeze-the-world sequence for RAG and knowledge-base incidents.

## [0.5.0] · 2026-06-20 · Playbook 24: Board-Ready Scorecard

### Added

- `playbooks/24-board-ready-scorecard.md`: executive-layer artifact. Translates the technical IR machinery into a four-domain board view (Containment, Evidence, Governance, Recovery) with GREEN, AMBER, and RED ratings.

## [0.4.0] · 2026-06-19 · Playbook 18: Post-Incident Hardening

### Added

- `playbooks/18-post-incident-hardening.md`: closes the response arc. Turns post-incident lessons into permanent guardrails within five business days.

## [0.3.0] · 2026-06-18 · Playbook 04: Tool Design Is Containment

### Added

- `playbooks/04-tool-design-is-containment.md`: pre-incident playbook. Covers tool tiering (Tiers 0, 1, and 2) and the five-control containment model that makes Mode M3 surgical.

## [0.2.0] · 2026-06-18 · Playbook 01: The Agent Is a Privileged Identity

### Added

- `playbooks/01-agent-as-privileged-identity.md`: the first practitioner playbook. Sets the privileged-identity lens that every later playbook builds on.

## [0.1.5] · 2026-06-17 · Crosswalk Expansion

### Added

- `crosswalks/nist-csf-2.md`: NIST CSF 2.0 mapping across the six functions (Govern, Identify, Protect, Detect, Respond, Recover).
- `crosswalks/owasp-agentic-top-10.md`: OWASP Agentic Top 10 2026 (ASI01 through ASI10) mapping.

### Changed

- Citation accuracy improved across every referenced standard.

## [0.1.4] · 2026-06-17 · Content Accuracy Polish

### Changed

- Updated NIST reference from SP 800-61 r2 to r3 (April 2025), reflecting the CSF 2.0 Community Profile restructure.
- Disambiguated OWASP Top 10 for LLM Applications (2025.1) from OWASP Top 10 for Agentic Applications 2026 throughout.

## [0.1.3] · 2026-06-17 · Cosmetic Polish

### Changed

- Trivial consistency fixes (formatting, link punctuation, heading casing). No framework substance changed.

## [0.1.2] · 2026-06-17 · OSS Conventions

### Added

- `CITATION.cff`: citation file format for academic and regulatory referencing.
- `SECURITY.md`: vulnerability disclosure policy and trademark misuse channel.
- `CONTRIBUTING.md`: contribution paths, PR process, style guide.
- `CODE_OF_CONDUCT.md`: Contributor Covenant v2.1.

## [0.1.1] · 2026-06-17 · License and Lint Fixes

### Added

- Apache 2.0 LICENSE with appended trademark notice for the AI IR Overlay and AI IR Overlay Certified word marks.

### Fixed

- Markdown lint corrections across the framework, triage, kill-switches, and evidence directories.

## [0.1.0] · Foundation

The founding release. Establishes the thesis, the framework core, the triage discipline, the containment ladder, and the evidence taxonomy. No playbooks in this release. Playbook 01 ships next, in `v0.2.0`.

### Added: Framework Core

- `framework/00-overview.md`: why an overlay, not a replacement. *(Content absorbed into README.md during v0.6.x cleanup.)*
- `framework/01-minimum-viable-overlay.md`: the four MVO controls.
- `framework/02-mental-model.md`: the four-sentence model.

### Added: Triage

- `triage/six-questions.md`: the first-15-minutes discipline.
- `triage/six-questions-card.md`: printable one-page card.

### Added: Containment

- `kill-switches/overview.md`: the six-mode ladder (M0 through M5) with TTA targets.

### Added: Evidence

- `evidence/minimum-evidence-set.md`: evidence types A–F plus capture order.

### Added: Templates

- `templates/ai-bom.yaml`: machine-readable AI Bill of Materials.
- `templates/agent-privilege-matrix.csv`: Tier 0, 1, and 2 example mapping.

[Unreleased]: https://github.com/jacobideji/aiiroverlay/compare/v0.14.1...HEAD
[0.14.1]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.14.1
[0.14.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.14.0
[0.13.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.13.0
[0.12.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.12.0
[0.11.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.11.0
[0.10.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.10.0
[0.9.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.9.0
[0.8.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.8.0
[0.7.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.7.0
[0.6.2]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.6.2
[0.6.1]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.6.1
[0.6.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.6.0
[0.5.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.5.0
[0.4.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.4.0
[0.3.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.3.0
[0.2.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.2.0
[0.1.5]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.5
[0.1.4]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.4
[0.1.3]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.3
[0.1.2]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.2
[0.1.1]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.1
[0.1.0]: https://github.com/jacobideji/aiiroverlay/releases/tag/v0.1.0
