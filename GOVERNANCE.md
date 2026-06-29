# Governance

The AI IR Overlay is open, vendor-neutral, and Apache 2.0 licensed. This document defines how decisions get made today and how governance will change as the project matures.

## Project status

This is a **single-maintainer, pre-1.0 project**. Current scale:

- **Lead Maintainer:** Jacob Ideji (founder, original author, current sole contributor)
- **External contributors:** none yet
- **Steering Committee, Working Group Leads, certification program:** **not yet established.** All multi-party governance structures described below under "Future governance (v1.0.0 and beyond)" are aspirational and will be convened only if v1.0.0 readiness criteria are met and community adoption justifies the structure.

The framework's roadmap to v1.0.0 is documented in [CHANGELOG.md](CHANGELOG.md) `[Unreleased]` and [CONTENT_MAP.md](CONTENT_MAP.md).

## Current governance (v0.x)

### Roles

- **Lead Maintainer (Jacob Ideji):** founder, original author, current sole decision-maker. Owns the trademark and certification mark (see [LICENSE](LICENSE)). Holds final authority during the `v0.x` series.
- **Contributors:** anyone, via Pull Request. Substantive contributors are credited in release notes. A `CONTRIBUTORS.md` file will be created once external contributors exist.

### Decision-making

- Lead Maintainer decides.
- Changes to the `framework/` directory or the six-question card get a 5-day public comment window.
- Everything else (playbooks, crosswalks, templates, schemas) runs on lazy consensus: silence after 5 days of public visibility counts as approval.

### Release cadence

| Cadence | Type | Approver |
|---|---|---|
| Per content drop (v0.x) | MINOR (`0.x.0`) | Lead Maintainer |
| As warranted | PATCH (`0.x.y`) | Lead Maintainer |

### Amendments to this document

During `v0.x`: Lead Maintainer decides after a 14-day public comment window.

## Future governance (v1.0.0 and beyond)

The following structures will be convened **only if** the project reaches v1.0.0 with sustained external community engagement. None of these structures exist today.

### Planned: Steering Committee (target: 5 seats)

- Would be convened at `v1.0.0`.
- Composition target:
  - 2 sitting CISOs (one Fortune 500, one mid-market or public sector)
  - 1 academic or research representative
  - 1 regulator-adjacent voice (former NIST, former CISA, or equivalent abroad)
  - 1 international representative (EU, UK, APAC, or Africa)
- 2-year staggered terms. Reappointment by Committee vote.
- A public conflict-of-interest register would be published quarterly. Members would disclose vendor employment and material stock holdings, and recuse from votes that materially benefit their employer.

### Planned: Working Group Leads

- Would be appointed one per crosswalk (NIST AI RMF, NIST CSF 2.0, EU AI Act, ISO/IEC 42001, OWASP Top 10 Agentic) once contributors emerge to lead each.
- Would be authorized to merge PRs within scope.

### Planned: Decision-making at v1.0.0 and beyond

- Steering Committee would operate by lazy consensus with a 5-day comment window.
- Breaking changes (anything that invalidates a conformance claim) would require:
  - A written RFC in `rfcs/`
  - A 30-day public comment window
  - Two-thirds Committee approval
  - A major version bump

### Planned: Release cadence at v1.0.0 and beyond

| Cadence | Type | Approver |
|---|---|---|
| Quarterly | MINOR (`1.x.0`) | Lead Maintainer |
| As warranted | PATCH (`1.x.y`) | Working Group Lead |
| Roughly annual | MAJOR (`x.0.0`) | Steering Committee |

Major versions would only be justified by external-ecosystem shifts. Examples: a future NIST AI Agent Interoperability Profile, an EU AI Act Article 26 update, an OWASP Agentic Top 10 revision.

### Planned: Certification program

The `AI IR Overlay Certified™` mark exists as a defensive registration to reserve the framework's brand. **The certification program itself does not yet exist.** When the program is built (target: with `v1.0.0`), it will be documented in a separate charter at `certification/charter.md` and will cover:

- Conformant Implementations
- Certified Practitioner

Until then, the mark is reserved for the maintainer's future use; no third party is currently authorized to claim certification under it.

### Planned: Amendments at v1.0.0 and beyond

From `v1.0` onward: Steering Committee two-thirds vote after a 30-day public comment window.

## Trademark

- **AI IR Overlay™**: unregistered word mark held by the Lead Maintainer.
- **AI IR Overlay Certified™**: unregistered word mark held by the Lead Maintainer, reserved for the future certification program.
- Free use covers education, advocacy, academic citation, and conformant non-commercial implementations.
- Commercial use requires contact via [jacobideji.com](https://jacobideji.com).

## Code of Conduct

This project adopts the **Contributor Covenant v2.1**. See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Security disclosures

For vulnerabilities, follow the private reporting path in [`SECURITY.md`](SECURITY.md).

<!-- Last revised: 2026-06-28 -->
