# Security Policy

## Scope

This repository contains the **AI IR Overlay™** framework: documentation, templates, and reference materials for AI agent incident response. It is **not** a runtime system or executable software.

The security boundary of this repository covers:

- The integrity of the framework content itself (preventing tampered guidance that could mislead adopters)
- Sensitive data accidentally included in templates or documentation
- Misuse of the `AI IR Overlay™` and `AI IR Overlay Certified™` word marks
- Vulnerabilities in any reference implementations added in future releases

For incidents in **your** AI agent environments, the framework itself is the guide. Start with the [Six Triage Questions](triage/six-questions.md).

## Supported Versions

| Version | Supported with security fixes |
|---|---|
| Latest minor release (`v0.6.x`) | ✅ |
| Previous minor (`v0.5.x`) | ✅ Critical fixes only |
| Older tags (`≤ v0.4.x`) | ❌ Upgrade to latest |
| Pre-release / unreleased commits | ❌ |

## Reporting a Vulnerability

**Please do not open a public GitHub Issue for security reports.** Use one of the private channels below.

### Preferred channel: GitHub Security Advisory

Open a private advisory:
**[github.com/jacobideji/aiiroverlay/security/advisories/new](https://github.com/jacobideji/aiiroverlay/security/advisories/new)**

This is the fastest path. It gives you a private collaboration thread with the maintainer and lets us coordinate a fix and disclosure.

### Alternative: direct contact

If a security advisory isn't possible, contact the maintainer through [jacobideji.com](https://jacobideji.com).

### What to include

- A short description of the issue
- Steps to reproduce (if a script, template, or rendering is involved)
- The version or commit SHA you observed it on
- Whether you have discussed this with anyone else
- Your suggested CVSS severity, if you have one

### What to expect from us

- **Acknowledgment within 5 business days**
- **Initial assessment within 14 days**
- Fix targeted for the next regular release, or an off-cycle patch for critical issues
- Credit to the reporter in the release notes (unless you prefer to remain anonymous)
- Coordinated public disclosure once a fix is available

## Responsible Disclosure

We follow a coordinated disclosure model. Please give us a reasonable window (typically **30 days** from acknowledgment for non-critical issues, **faster for critical**) before any public disclosure.

If you intend to publish research or a CVE, let us know your target date and we will work to meet it.

## Out of Scope

- Generic discussions of AI agent risk that do not identify a specific vulnerability in this repository
- Theoretical attacks on AI systems described **by** the framework (these are the subject of the framework, not vulnerabilities of it)
- Issues in upstream dependencies of any tooling (`markdownlint-cli2`, `pyyaml`, etc.). Report those to their respective maintainers.

## Trademark and Brand Misuse

If you believe someone is misusing the **AI IR Overlay™** or **AI IR Overlay Certified™** word marks (for example, claiming "certification" status without authorization, or running a paid program under the name), please report it via [jacobideji.com](https://jacobideji.com) rather than the security advisory channel.
