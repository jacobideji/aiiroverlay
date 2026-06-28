# Contributing to the AI IR Overlay™ Framework

Thanks for considering a contribution. The AI IR Overlay is a **practitioner-driven framework**. Field experience is the most valuable contribution you can make.

## Highest-velocity contribution paths

These are where new contributors create the most value:

1. **Playbooks** for AI agent incident scenarios not yet covered (voice agents, coding agents, multi-tenant SaaS copilots, healthcare clinical decision support, financial trading-floor copilots, citizen-facing chatbots)
2. **Crosswalks** mapping AI IR Overlay controls to other frameworks (CIS Controls, SOC 2, HIPAA, FedRAMP, Singapore CSA, UK AISI guidance, Japan METI AI guidelines, ENISA)
3. **Reference implementations** in your stack (LangChain, LangGraph, Semantic Kernel, AWS Bedrock Agents, Azure AI Foundry, Vertex AI Agent Builder, Anthropic SDK)
4. **Translations** of the six-question card
5. **Real-incident case studies** (anonymized) that strengthen specific playbooks

## How to contribute

### Issues

Open an Issue for:

- **Bug reports**: broken link, factual error, conflicting guidance, lint warning
- **Playbook proposals**: describe the scenario and why a separate playbook is warranted
- **Crosswalk requests**: name the target framework and your intended use

For open-ended questions, use **[Discussions](https://github.com/jacobideji/aiiroverlay/discussions)** instead of Issues.

### Pull Requests

1. **Fork** the repository
2. Create a feature branch from `main` (e.g., `playbook/voice-agent-deepfake`)
3. Make changes with **clear conventional commit messages** (`feat:`, `fix:`, `docs:`, `style:`, `chore:`)
4. Open a PR linking to the originating Issue or Discussion
5. **Lazy consensus applies** for non-framework changes. Silence after 5 days of public visibility counts as approval.

## Standards by contribution type

### Framework-core changes (`framework/`, `triage/`, `kill-switches/`, `evidence/`)

- Require **Lead Maintainer review**
- Must preserve compatibility with the current MVO conformance claims (see [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md))
- Must update the README's reading-order if the structure changes
- Must update `CHANGELOG.md` under `[Unreleased]`

### Playbooks (`playbooks/`)

- Follow the **playbook template**. Every playbook has these sections: Premise, First-Hour Actions, Containment Options, Evidence Priorities, Recovery Sequence, Post-Incident Hardening, Common Pitfalls, Related, The Question to Carry Forward. Each playbook closes with a source-citation footer linking back to the originating newsletter issue.
- Must include a **source citation** if adapted from existing material
- Must reference the Mental Model clause(s) the scenario engages
- Must cross-reference relevant framework pieces using the *"see the `X-package` package"* pattern (so the playbook reads correctly standalone)

### Crosswalks (`crosswalks/`)

- Provide a **two-column mapping** (AI IR Overlay ↔ target framework)
- Include "gap" notes for AI IR Overlay controls **not** present in the target. These are the value-adds your crosswalk surfaces.

### Reference implementations (when added)

- **Working code with tests**
- **Document supported runtime / framework versions** explicitly
- **Apache 2.0 license header** required in every source file
- Use parameterized config (e.g., `AIIROVERLAY_VAULT_DIR` pattern). Never hardcode paths or credentials.

## Style guide

- **Plain English.** Avoid jargon when a plain word works.
- **Active voice.** "The agent sends an email" beats "An email is sent by the agent."
- **US spelling.** We're not ideological, just consistent.
- **No vendor pitches.** Use brand-neutral language ("vector database" not "Pinecone," "CRM" not "Salesforce," unless the specific vendor's behavior is the point).
- **Cite normative references by document number** (NIST SP 800-61 r3, ISO/IEC 42001:2023, EU AI Act Reg 2024/1689).
- **Em-dash budget.** Aim for under 0.5 em-dashes per 100 words. Prefer periods, colons, or parentheses for readability. Em-dashes are fine when sparingly used for emphasis. They're not a brand signature.
- **Contractions are fine** in playbook prose (don't, won't, it's, I've). Use them for natural practitioner voice.
- **First-person is fine** when sharing direct experience.
- **No filler.** *Very, really, actually, basically.* Cut on sight.

## Source attribution

If you adapt material from the **AI IR Overlay** LinkedIn newsletter or any other published source, preserve the citation in the file footer:

```text
*Source: AI IR Overlay newsletter, Issue #N (YYYY-MM-DD), by Jacob Ideji.*
*https://www.linkedin.com/in/jacobideji/*
```

This is part of how the framework remains academically citable.

## Recognition

Substantive contributors are credited in release notes. Once a `CONTRIBUTORS.md` exists, your name lands there too.

## Code of Conduct

This project follows the **[Contributor Covenant 2.1](CODE_OF_CONDUCT.md)**. By contributing, you agree to abide by it.

## Security disclosures

For vulnerabilities, **do not** open a public Issue. See **[SECURITY.md](SECURITY.md)** for the private reporting path.

## Trademark notice

The **AI IR Overlay™** and **AI IR Overlay Certified™** word marks are protected. See `LICENSE`. Contributing code or content under Apache 2.0 does not grant rights to use the word marks commercially.

---
*Questions? Open a [Discussion](https://github.com/jacobideji/aiiroverlay/discussions), or reach the maintainer at [jacobideji.com](https://jacobideji.com).*
