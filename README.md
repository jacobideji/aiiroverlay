<!-- ────────────────────────────────────────────────────────────────── -->
<!--  AI IR Overlay — Framework Overview                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Why an overlay, not a replacement. The thesis.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# The AI IR Overlay — Framework Overview

> Establishing the minimum standard for safe and effective operations of AI agents in production.

## Why an overlay, not a replacement

Traditional incident response, as described in NIST SP 800-61 Revision 2, addresses unauthorized access vectors including malware, exploits, credential theft, and lateral movement. The use of AI agents introduces new types of failure modes.

AI incidents often manifest through authorized channels:

* Legitimate identities, such as service accounts or delegated OAuth grants, may perform unintended actions.
* Legitimate APIs, including tool calls to email, CRM, and ERP, may operate within allowed parameters but still cause harm.
* Legitimate sources, such as retrieval layers, may pull from trusted but outdated or inappropriate knowledge.
* Legitimate workflows, including automations that follow policy as written, may still result in harmful outcomes.

After authorization, the focus shifts from identifying the actor to determining what resources were accessed and what actions were performed. Key evidence is now found in prompts, tool calls, retrieval traces, and configuration state, rather than on endpoints.

## What stays the same


The core mechanics of effective incident response remain unchanged:

- Clear command and control
- Evidence-first discipline
- Rapid containment with minimal disruption
- Scoping using *confirmed* versus *suspected* terminology
- Recovery via controlled, staged re-enablement
- Defensible decision logs

AI does not change the core principles of effective incident response, but it does reshape the operational environment.

## The Overlay model

The AI IR Overlay adds four agent-aware controls — the **Minimum Viable Overlay (MVO)** — on top of your existing IR program:

```
┌─────────────────────────────────────────────────────────┐
│                NIST 800-61 IR Lifecycle                 │
│  Preparation → Detection → Containment → Eradication →  │
│              Recovery → Post-Incident                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              AI IR Overlay — MVO Controls               │
│                                                         │
│  1. INVENTORY     — Agents · Identities · Tools ·       │
│                     Write Targets                       │
│  2. SAFE MODES    — Kill-Switch Ladder (Modes 0–5)      │
│  3. EVIDENCE      — Minimum AI Evidence Set (A–F)       │
│  4. CONTROLLED    — Staged, validated re-enablement     │
│     RE-ENABLE                                           │
└─────────────────────────────────────────────────────────┘
```

## Reading order

The framework ships as separate packages. Read them in this order:

1. **The Minimum Viable Overlay** — the four controls in detail (`framework-01-minimum-viable-overlay`)
2. **The Mental Model** — four sentences that govern every decision (`framework-02-mental-model`)
3. **The Maturity Roadmap** — where your program is, and how to advance it (`framework-03-maturity-roadmap`)
4. **The Six Triage Questions** — first-hour discipline (`triage-six-questions`)
5. **Kill-Switch Modes** — containment ladder (`kill-switches-modes`)
6. **Minimum Evidence Set** — what to preserve, and in what order (`evidence-minimum-set`)

## Provenance

Jacob Ideji developed and tested the AI IR Overlay through the *AI IR Overlay* LinkedIn newsletter series (Issues 1–24, 2025–2026). Each issue aligns with a playbook in the framework.

## Related work

- NIST SP 800-61 r2 — Computer Security Incident Handling Guide
- NIST AI Risk Management Framework (AI RMF 1.0)
- OWASP Top 10 for LLM and Agentic Applications
- ISO/IEC 42001:2023 — Artificial Intelligence Management System
- EU AI Act (Regulation 2024/1689) — Article 26 obligations for deployers
- MITRE ATLAS — Adversarial Threat Landscape for AI Systems
