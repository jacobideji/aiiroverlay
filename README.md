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
Å
---

# The AI IR Overlay — Framework Overview

> We set basic requirements to ensure AI agents work safely and effectively in real-world use.

## Why an overlay, not a replacement

Traditional incident response, as described in NIST SP 800-61 r2, focused on threats like malware, exploits, stolen credentials, and lateral movement. With AI agents, the types of failures we face differ, including incorrect outputs, unsafe actions, and loss of control.

AI incidents often manifest through *authorized* channels:

* Legitimate identities, such as service accounts or delegated OAuth grants, can sometimes carry out actions that were not intended.
* Legitimate APIs, including tool calls to email, CRM, and ERP systems, may work within approved limits but can still cause harm.
* Legitimate sources, such as retrieval layers, might pull information from trusted but outdated or unsuitable knowledge bases.
* Legitimate workflows, including automations that follow policy as written, can still lead to harmful results.

Once the actor is authorized, the focus changes from asking *"who got in?"* to *"what could they access and what did they do?"* At this stage, the most useful evidence comes from prompts, tool calls, retrieval traces, and configuration state, rather than only checking endpoints.

## What stays the same

The main steps for effective incident response have stayed the same:

- Keep command and control clear
- Focus on evidence first
- Contain issues quickly while causing as little disruption as possible
- Use 'confirmed' and 'suspected' carefully when describing the scope
- Recover systems in a controlled, step-by-step way
- Keep clear records of decisions

AI does not change the basic rules of effective international relations. Instead, it shifts the landscape.

## The Overlay model

The AI IR Overlay introduces four agent-aware controls, called the **Minimum Viable Overlay (MVO)**, to your current IR program:

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

The AI IR Overlay was developed and tested through the *AI IR Overlay* LinkedIn newsletter series (Issues 1–24, 2025–2026) by Jacob Ideji. Each issue corresponds to a playbook in the full framework.

## Related work

- NIST SP 800-61 r2 — Computer Security Incident Handling Guide
- NIST AI Risk Management Framework (AI RMF 1.0)
- OWASP Top 10 for LLM and Agentic Applications
- ISO/IEC 42001:2023 — Artificial Intelligence Management System
- EU AI Act (Regulation 2024/1689) — Article 26 obligations for deployers
- MITRE ATLAS — Adversarial Threat Landscape for AI Systems
