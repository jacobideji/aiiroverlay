# Governance

The AI IR Overlay is open, vendor-neutral, and Apache 2.0 licensed. This document defines how decisions get made.

## Roles

### Founder and Lead Maintainer

- **Jacob Ideji**: founder, original author of the framework, and current Lead Maintainer.
- Holds tie-breaking authority during the `v0.x` series.
- Owns the trademark and certification mark. See [LICENSE](LICENSE).

### Steering Committee (target: 5 seats)

- Convened at `v1.0.0`.
- Composition target:
  - 2 sitting CISOs (one Fortune 500, one mid-market or public sector)
  - 1 academic or research representative
  - 1 regulator-adjacent voice (former NIST, former CISA, or equivalent abroad)
  - 1 international representative (EU, UK, APAC, or Africa)
- 2-year staggered terms. Reappointment by Committee vote.

### Working Group Leads

- One per crosswalk: NIST AI RMF, NIST CSF 2.0, EU AI Act, ISO/IEC 42001, OWASP Top 10 Agentic.
- Authorized to merge PRs within scope.

### Contributors

- Anyone, via Pull Request. Substantive contributors get credit in release notes and (once it exists) in `CONTRIBUTORS.md`.

## Decision-making

### v0.x (current series)

- Lead Maintainer decides.
- Changes to the `framework/` directory or the six-question card get a 5-day public comment window.
- Everything else (playbooks, crosswalks, templates) runs on lazy consensus: silence after 5 days of public visibility counts as approval.

### v1.0 onward

- Steering Committee operates by lazy consensus with a 5-day comment window.
- Breaking changes (anything that invalidates a conformance claim) require all of the following:
  - A written RFC in `rfcs/`
  - A 30-day public comment window
  - Two-thirds Committee approval
  - A major version bump

## Release cadence

| Cadence | Type | Approver |
|---|---|---|
| Per content drop (v0.x) | MINOR (`0.x.0`) | Lead Maintainer |
| As warranted | PATCH (`0.x.y`) | Lead Maintainer |
| Quarterly (v1.x and later) | MINOR (`1.x.0`) | Lead Maintainer |
| As warranted (v1.x and later) | PATCH (`1.x.y`) | Working Group Lead |
| Roughly annual (v1.x and later) | MAJOR (`x.0.0`) | Steering Committee |

Major versions are only justified by external-ecosystem shifts. Examples: a future NIST AI Agent Interoperability Profile, an EU AI Act Article 26 update, an OWASP Agentic Top 10 revision.

## Trademark and certification

- **AI IR Overlay™**: word mark, held by the Lead Maintainer.
- **AI IR Overlay Certified™**: certification mark. Commercial use requires a license.
- Free use covers education, advocacy, academic citation, and conformant non-commercial implementations.
- The certification program (Conformant Implementations and Certified Practitioner) gets a separate governance document at `certification/charter.md`, forthcoming with `v1.0.0`.

## Conflict of interest

- Steering Committee members must disclose vendor employment and material stock holdings.
- Members recuse from votes that materially benefit their employer.
- A public conflict-of-interest register is published quarterly.

## Code of Conduct

This project adopts the **Contributor Covenant v2.1**. See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Security disclosures

For vulnerabilities, follow the private reporting path in [`SECURITY.md`](SECURITY.md).

## Amendments

- During `v0.x`: Lead Maintainer decides after a 14-day public comment window.
- From `v1.0` onward: Steering Committee two-thirds vote after a 30-day public comment window.

<!-- Last revised: 2026-06-23 -->
