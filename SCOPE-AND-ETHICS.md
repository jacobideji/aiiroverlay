<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens: Scope and Rules of Engagement  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **A gate, not a formality. Authorization precedes every exercise.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Scope and Rules of Engagement

This document is a gate. If you cannot satisfy every item in the Authorization Gate below, do not run any exercise in this repository.

## Authorization Gate

Before the first exercise, all five must be true and recorded in [templates/engagement-authorization.md](templates/engagement-authorization.md):

1. **Named authorizer.** A person with authority over the target agent's deployment has approved this engagement in writing. The authorizer must own the system, not manage the testers.
2. **Enumerated targets.** Every agent identity, tool, write target, and data source in scope is listed by name. "All agents in the staging tenant" is not an enumeration.
3. **Blast-radius statement.** For each in-scope write target, the worst realistic outcome of an exercise is written down and accepted. Exercises that touch irreversible write targets (payments, external communications, production deletes) require per-exercise sign-off.
4. **Stop condition.** A named person can halt the engagement, and the testers know how to reach them within minutes.
5. **Notification decision.** Whether the SOC is told in advance is recorded either way. Running unannounced is a legitimate choice for L3. It is the only honest way to measure detection latency, but it is a *decision*, made in advance, by the authorizer.

## In scope

- AI agents your organization **deploys and operates**, under its own oversight.
- The control plane your organization owns: tool registries, kill switches, logging pipelines, memory stores, retrieval corpora, agent identity and scope grants.
- Non-production environments first. An exercise moves to production only after it has produced a clean result in staging and the blast-radius statement has been re-accepted.

## Out of scope

This repository does not cover, and must not be used for:

- **Third-party agents.** Agents operated by vendors, partners, or platforms. Their controls are not yours to test, and the AI-BOM for them is not yours to validate.
- **Model providers.** Jailbreaking, guardrail evasion, or safety-filter bypass against a foundation model as such. The lens tests *your* containment, not the provider's alignment.
- **Agents handling live third-party data** where an exercise could expose, alter, or exfiltrate another party's records.
- **Humans.** No social engineering of operators, approvers, or responders. L4's self-approval technique (OL-T405) tests whether the *workflow* permits self-approval; it does not test whether a person can be talked into it.

## Technique posture

Techniques in this repository are specified as **procedures with pass criteria**, at the altitude of MITRE ATT&CK or the OWASP testing guide. They state what to attempt, what result proves the control held, and what defensive signal should have fired.

They deliberately do not ship working payloads, prompt-injection strings tuned to specific models, or exploit code. Two reasons, in order:

1. A payload is a point-in-time artifact and makes a poor control test. "Did write capability leave the agent?" is answerable with a benign, auditable write; it does not need an injection to be meaningful.
2. The audience is an incident-response and governance audience. The deliverable is a defensible finding, not a demonstration.

Where an exercise genuinely requires adversarial input (OL-T307 and OL-T401/402 involve content the agent treats as instructions), use a **benign canary**: a uniquely identifiable, harmless marker whose appearance proves the path, and whose presence in logs is unambiguous. Canary construction is covered per-technique.

## Data handling

- Evidence collected during an exercise is incident evidence. Hold it to the same classification, retention, and access controls as real incident evidence.
- Exercise records will contain agent prompts and tool payloads, which routinely contain customer data and secrets. Redact before the record leaves the engagement team, and record that redaction happened.
- Canary markers must be unique per exercise and logged, so a canary surfacing six months later is attributable to an exercise rather than treated as a live incident.

## Disclosure

Findings about your own deployment are yours. If an exercise surfaces a defect in a **third-party product** such as an agent framework, a logging pipeline or a kill-switch implementation. That is a vulnerability disclosure, not an exercise finding. Route it through the vendor's disclosure process and out of the engagement report.

## Standing down

Halt immediately, notify the stop-condition owner, and preserve all evidence if an exercise:

- produces an effect on an out-of-scope system;
- produces an irreversible write that was not in the blast-radius statement;
- cannot be distinguished from a real incident by the responders;
- reveals an active compromise. An exercise that finds a real intruder is over. Switch to the overlay's response path (`RESPONSE-START.md`) and treat the exercise evidence as incident evidence.
