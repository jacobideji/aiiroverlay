# Changelog

All notable changes to the AI IR Overlay framework live here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/spec/v2.0.0.html).

During the `v0.x` series, each substantive content drop ships as its own MINOR release. `v1.0.0` arrives once the framework core is stable, the remaining playbooks are live, and a Steering Committee is in place.

## [Unreleased]

### Planned

- Remaining playbooks: 05, 06, 08, 09, 10, 12, 15, 16, 17, 19, 21, 22, 23
- Additional crosswalks: CIS Controls, SOC 2, HIPAA
- Printable Board Scorecard template (`templates/board-scorecard.md`)
- Steering Committee announcement (cuts `v1.0.0`)

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

- `framework/00-overview.md`: why an overlay, not a replacement.
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

[Unreleased]: https://github.com/jacobideji/aiiroverlay/compare/v0.9.0...HEAD
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
