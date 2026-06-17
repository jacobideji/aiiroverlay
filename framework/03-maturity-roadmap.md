<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Maturity Roadmap (framework view)                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The four-level maturity model.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# The AI IR Maturity Roadmap

> Four levels. One question at each: *can you do this, on demand, under pressure?*

This is the **framework view** of maturity — the model used to assess and benchmark organizations. The **operating** view, with cadences, drills, and pitfalls, is distributed as the `playbook-20` package.

## The Four Levels

```text
                       ┌──────────────────────────────┐
                       │   Level 4  RESILIENT         │
                       │   Continuous improvement     │
                       │   "We get better every Q"    │
                       └──────────────▲───────────────┘
                                      │
                       ┌──────────────────────────────┐
                       │   Level 3  PROVABLE          │
                       │   Evidence under pressure    │
                       │   "Here is what happened"    │
                       └──────────────▲───────────────┘
                                      │
                       ┌──────────────────────────────┐
                       │   Level 2  CONTAINABLE       │
                       │   Stop harm without stopping │
                       │   "We're already contained"  │
                       └──────────────▲───────────────┘
                                      │
                       ┌──────────────────────────────┐
                       │   Level 1  AWARE             │
                       │   Inventory of agents/tools  │
                       │   "We know what we run"      │
                       └──────────────────────────────┘
```

## Level Definitions

| Level | One-sentence definition | Test |
|---|---|---|
| **1 — Aware** | The organization has basic visibility into its AI assets. | Can you produce a current inventory of every agent → identity → tool → write target in under 5 minutes? |
| **2 — Containable** | Harm can be contained without a complete shutdown. | Can Tier-1 SOC activate Modes M1–M4 within 10 minutes, in production, without escalation? |
| **3 — Provable** | The organization can demonstrate scope under time pressure. | Can the team export the Minimum Evidence Set within 60 minutes for any agent? |
| **4 — Resilient** | Continuous improvement with measured recovery. | Are the Six Metrics (see the `playbook-13` package) trending in the right direction over rolling 90 days? |

## Mapping the Levels to Framework Controls

| Level | Required controls (see the `framework-01-minimum-viable-overlay` package) |
|---|---|
| **1 — Aware** | MVO-1 Inventory (current) |
| **2 — Containable** | MVO-1 + MVO-2 Safe Modes (M1–M4 implemented & tested) |
| **3 — Provable** | Level 2 + MVO-3 Minimum Evidence Set (A–F exportable in 60 min) |
| **4 — Resilient** | Level 3 + MVO-4 Controlled Re-Enable + quarterly tabletops + measured metrics |

## The Honest Self-Assessment

A common failure mode is over-claiming. The Overlay's stance:

> If a capability has never been tested in the **last 90 days**, you do not have it.

Apply this rule to every level:

- Level 2 means M1–M4 *tested in production* within 90 days, not "documented in the runbook."
- Level 3 means the Minimum Evidence Set was *actually exported* within 60 minutes within 90 days.
- Level 4 means tabletops happened and metrics moved.

Most organizations who claim Level 3 are honestly at Level 1.

## Why This Matters for the Board

| Board question | Level required to answer "yes" |
|---|---|
| Do we know which AI we run? | Level 1 |
| Can we stop harm fast? | Level 2 |
| Can we tell the regulator what happened? | Level 3 |
| Are we measurably getting better? | Level 4 |

The board scorecard (distributed as the `playbook-24` package) maps directly to these.

## Operating the Roadmap

The operating cadence, drill design, and common pitfalls are detailed in the `playbook-20` package. Start there for execution.

---

*Source: AI IR Overlay newsletter, Issue #20 — "AI IR Maturity Roadmap," by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
