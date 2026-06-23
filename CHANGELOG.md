# Changelog

All notable changes to the AI IR Overlay framework live here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/spec/v2.0.0.html).

During the `v0.x` series, each substantive content drop ships as its own MINOR release. `v1.0.0` arrives once the framework core is stable, the remaining playbooks are live, and a Steering Committee is in place.

## [Unreleased]

### Planned

- Remaining playbooks: 05 through 12, 15 through 17, and 19 through 23
- Additional crosswalks: CIS Controls, SOC 2, HIPAA
- Steering Committee announcement (cuts `v1.0.0`)

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
