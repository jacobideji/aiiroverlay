# Changelog

All notable changes to the AI IR Overlay™ framework are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

During the `v0.x` series, each substantive content drop ships as its own MINOR
release. `v1.0.0` is cut as the stable release once the framework core, the
remaining playbooks, and the Steering Committee are in place.

## [Unreleased]

### Planned

- Remaining playbooks (Playbooks 02, 05–12, 15–17, 19–23) under MINOR releases
- Additional crosswalks (CIS Controls, SOC 2, HIPAA)
- Steering Committee announcement (`v1.0.0`)

## [0.6.0] — 2026-06-23 — Measurement Release

### Added

- Operational guidance for measuring AI incident-response posture and surfacing readiness signals across the four MVO controls.

## [0.5.0] — 2026-06-20 — Playbook 24: Board-Ready Scorecard

### Added

- `playbooks/24-board-ready-scorecard.md` — executive-layer artifact that translates technical IR machinery into board-verifiable posture across four domains (Containment, Evidence, Governance, Recovery) with GREEN / AMBER / RED ratings.

## [0.4.0] — 2026-06-19 — Playbook 18: Post-Incident Hardening

### Added

- `playbooks/18-post-incident-hardening.md` — closes the IR temporal arc by operationalizing post-incident lessons into guardrails within a five-business-day SLA.

## [0.3.0] — 2026-06-18 — Playbook 04: Tool Design Is Containment

### Added

- `playbooks/04-tool-design-is-containment.md` — pre-incident preparation playbook operationalizing tool-layer tiering (Tier 0 / 1 / 2) and the five-control containment model.

## [0.2.0] — 2026-06-18 — Playbook 01: The Agent Is a Privileged Identity

### Added

- `playbooks/01-agent-as-privileged-identity.md` — first practitioner playbook, orchestrating framework components for privileged-identity-class scenarios. Establishes the lens every subsequent playbook builds on.

## [0.1.5] — 2026-06-17 — Crosswalk Expansion

### Added

- `crosswalks/nist-csf-2.md` — NIST CSF 2.0 mapping (functions: Govern, Identify, Protect, Detect, Respond, Recover).
- `crosswalks/owasp-agentic-top-10.md` — OWASP Agentic Top 10 2026 (ASI01–ASI10) mapping.

### Changed

- Improved citation accuracy across all referenced standards.

## [0.1.4] — 2026-06-17 — Content Accuracy Polish

### Changed

- Updated NIST reference from SP 800-61 r2 to **r3** (April 2025), reflecting the CSF 2.0 Community Profile restructure.
- Disambiguated OWASP **Top 10 for LLM Applications (2025.1)** from OWASP **Top 10 for Agentic Applications 2026** throughout.

## [0.1.3] — 2026-06-17 — Cosmetic Polish

### Changed

- Trivial consistency fixes (formatting, link punctuation, heading casing). No framework substance changes.

## [0.1.2] — 2026-06-17 — OSS Conventions

### Added

- `CITATION.cff` — citation file format for academic and regulatory referencing.
- `SECURITY.md` — vulnerability disclosure policy and trademark misuse channel.
- `CONTRIBUTING.md` — contribution paths, PR process, style guide.
- `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1.

## [0.1.1] — 2026-06-17 — License & Lint Fixes

### Added

- Apache 2.0 LICENSE with appended trademark notice for the `AI IR Overlay™` and `AI IR Overlay Certified™` word marks.

### Fixed

- Markdown linting corrections across the framework, triage, kill-switches, and evidence directories.

## [0.1.0] — Foundation

The founding release. Establishes the thesis, the framework core, the triage discipline, the containment ladder, and the evidence taxonomy. No playbooks ship in this release — Playbook 01 ships next in `v0.2.0`.

### Added — Framework Core

- `framework/00-overview.md` — Why an overlay, not a replacement
- `framework/01-minimum-viable-overlay.md` — The four MVO controls
- `framework/02-mental-model.md` — The four-sentence model

### Added — Triage

- `triage/six-questions.md` — The first-15-minutes discipline
- `triage/six-questions-card.md` — Printable one-page card

### Added — Containment

- `kill-switches/overview.md` — The six-mode ladder (M0–M5) with TTA targets

### Added — Evidence

- `evidence/minimum-evidence-set.md` — Evidence types A–F + capture order

### Added — Templates

- `templates/ai-bom.yaml` — Machine-readable AI Bill of Materials
- `templates/agent-privilege-matrix.csv` — Tier 0/1/2 example mapping

[Unreleased]: https://github.com/jacobideji/aiiroverlay/compare/v0.6.0...HEAD
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
