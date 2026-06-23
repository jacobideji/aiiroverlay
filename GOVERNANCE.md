# Governance

The AI IR Overlay™ is open, vendor-neutral, and Apache 2.0 licensed. This document defines how decisions are made.

## Roles

### Founder / Lead Maintainer

- **Jacob Ideji** — founder, original author of the framework, current Lead Maintainer.
- Holds tie-breaking authority during the `v0.x` series.
- Owns the trademark and certification mark (see [LICENSE](LICENSE)).

### Steering Committee (target: 5 seats)

- Convened upon `v1.0.0` release.
- Composition target:
  - 2 sitting CISOs (one Fortune 500, one mid-market or public sector)
  - 1 academic or research representative
  - 1 regulator-adjacent voice (ex-NIST, ex-CISA, or equivalent international body)
  - 1 international representative (EU, UK, APAC, or Africa)
- 2-year staggered terms; reappointment by Committee vote.

### Working Group Leads

- One per crosswalk (NIST AI RMF, NIST CSF 2.0, EU AI Act, ISO/IEC 42001, OWASP Top 10 Agentic).
- Empowered to merge PRs within scope.

### Contributors

- Anyone via Pull Request. Substantive contributors are credited in release notes and (once it exists) in `CONTRIBUTORS.md`.

## Decision-making

### v0.x (current series)

- Lead Maintainer decides.
- 5-day public comment window for changes to the `framework/` directory or the six-question card.
- All other content (playbooks, crosswalks, templates) applies "lazy consensus": silence after 5 days of public visibility counts as approval.

### v1.0 onward

- Steering Committee operates by **lazy consensus** with a 5-day comment window.
- Breaking changes — anything that invalidates conformance claims — require:
  - A written RFC in `rfcs/`
  - 30-day public comment
  - 2/3 Committee approval
  - A major version bump

## Release cadence

| Cadence | Type | Approver |
|---|---|---|
| Per content drop (v0.x) | MINOR (`0.x.0`) | Lead Maintainer |
| As warranted | PATCH (`0.x.y`) | Lead Maintainer |
| Quarterly (v1.x+) | MINOR (`1.x.0`) | Lead Maintainer |
| As warranted (v1.x+) | PATCH (`1.x.y`) | Working Group Lead |
| ~Annual (v1.x+) | MAJOR (`x.0.0`) | Steering Committee |

Major versions are justified only by external-ecosystem shifts (e.g., a future NIST AI Agent Interoperability Profile, an EU AI Act Article 26 update, an OWASP Agentic Top 10 revision).

## Trademark and certification

- **AI IR Overlay™** — word mark, held by the Lead Maintainer.
- **AI IR Overlay Certified™** — certification mark; commercial use requires a license.
- Free use for: education, advocacy, academic citation, conformant non-commercial implementations.
- The certification program (Conformant Implementations and Certified Practitioner) is governed by a separate document: `certification/charter.md` (forthcoming with `v1.0.0`).

## Conflict of interest

- Steering Committee members must disclose vendor employment and material stock holdings.
- Members must recuse from votes that materially benefit their employer.
- A public conflict-of-interest register is published quarterly.

## Code of Conduct

The project adopts the **Contributor Covenant v2.1**. See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Security disclosures

For vulnerabilities, see [`SECURITY.md`](SECURITY.md) for the private reporting path.

## Amendments

This document may be amended by:

- `v0.x`: Lead Maintainer decision, 14-day public comment window.
- `v1.0+`: Steering Committee 2/3 vote, 30-day public comment window.

<!-- Last revised: 2026-06-23 -->
