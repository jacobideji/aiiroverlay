<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens: Overview  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **The overlay specifies what to do. The lens tests whether it would work.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# AI IR Overlay — Offensive Lens

**Version 0.37.0** · companion to [AI IR Overlay™](https://github.com/jacobideji/aiiroverlay) v0.35.0 · Apache 2.0

> The overlay specifies what to do when an AI agent incident happens.
> The Offensive Lens tests whether any of it would actually work.

## Why this exists

The overlay's own documentation states plainly that the framework *"has not yet been deployed in a documented production AI incident."* Waiting for one is not a validation strategy. It is the absence of one.

The Offensive Lens is the alternative. It is a structured adversarial exercise program aimed not at the agent, but at **the four controls the overlay installs around the agent**. Each exercise attacks one control's core assumption and produces a pass/partial/fail record with evidence attached.

Run it and you can answer, with artifacts rather than assertions:

- Is the AI-BOM an accurate description of runtime capability, or a stale declaration?
- When you call M1, does write capability actually leave the agent?
- Do all six evidence classes survive the act of containment?
- Does controlled re-enable restore the service without restoring the foothold?

That is the evidence the overlay is currently missing, obtainable without a breach.

## What this is / is not

| This is | This is not |
|---|---|
| A control-validation program for the overlay's four MVO controls | A penetration-testing methodology for AI products |
| Adversarial *exercises* with defined pass criteria | An exploit collection or payload library |
| Run against agents **your organization operates** | Run against third-party or vendor-hosted agents |
| Output: findings mapped to overlay playbooks | Output: access, data, or persistence |

Every exercise assumes you already hold write authority over the target agent. The lens is about whether your *controls* hold, not whether you can get in.

**Read [SCOPE-AND-ETHICS.md](SCOPE-AND-ETHICS.md) before running anything.** Authorization is a gate, not a formality.

## Structure

The lens mirrors the overlay's four Minimum Viable Overlay controls. One lens per control:

| Lens | Attacks overlay control | Core premise | CSF 2.0 function |
|---|---|---|---|
| **[L1, Inventory Drift](lenses/L1-inventory-drift.md)** | 1 · Inventory (AI-BOM) | The AI-BOM is a declaration; the runtime is the truth. Measure the delta. | Identify |
| **[L2, Containment Bypass](lenses/L2-containment-bypass.md)** | 2 · Safe Modes (M0–M5) | A ladder mode is a *claim* about capability removal. Test whether capability left. | Respond |
| **[L3, Evidence Starvation](lenses/L3-evidence-starvation.md)** | 3 · Evidence (six classes) | The minimum evidence set is only as good as what survives contact. | Detect / Respond |
| **[L4, Recovery Re-entry](lenses/L4-recovery-reentry.md)** | 4 · Controlled Re-enable | Re-enable restores capability. Does it also restore the attacker's foothold? | Recover |

31 techniques across the four lenses, covering every mode of the ladder. Full index: **[MATRIX.md](MATRIX.md)**.

## Reading order

1. **[SCOPE-AND-ETHICS.md](SCOPE-AND-ETHICS.md)**, authorization gate and rules of engagement.
2. **[START-HERE.md](START-HERE.md)**: the 90-minute first pass. Four exercises, one per lens, enough to produce a baseline.
3. **[MATRIX.md](MATRIX.md)**: the technique index and its mapping back to overlay controls and standards.
4. **[VALIDATION.md](VALIDATION.md)**. The conformance ladder, and what would prove the framework wrong.
5. **[FINDINGS.md](FINDINGS.md)**: every finding, why it was wrong, what replaced it, and what now stops the correction from becoming wrong again.
6. The lens document for whichever control you have the least confidence in.

## Scoring

Each technique yields one verdict:

- **PASS**: the control held; the attempted bypass produced no effect and the expected defensive signal was observed.
- **PARTIAL**. The control held but the signal was absent, late, or unattributable. The control works and you cannot prove it.
- **FAIL**. The control's premise does not hold in this deployment.
- **N/A**. The technique does not apply (document why; an undocumented N/A is treated as PARTIAL).

A lens is **validated** when every applicable technique is PASS. `PARTIAL` is the most common and most useful result: it is where the overlay is correct on paper and silent in practice.

## Repository layout

```
MATRIX.md                   technique index → overlay control → standards
SCOPE-AND-ETHICS.md         authorization gate, rules of engagement
START-HERE.md               90-minute first pass
lenses/                     L1–L4, technique definitions and procedures
templates/                  engagement authorization, report, finding stub
crosswalks/                 overlay playbooks, OWASP Agentic Top 10, MITRE ATLAS
offensive-lens/          the complete upload: 18 self-contained step folders
dist/                    generated: the component as it lands in the framework repository
VALIDATION.md               conformance ladder and pre-registered falsification criteria
```

## Relationship to the overlay

This repository takes no dependency on overlay code and does not vendor its content. It references overlay controls by number and playbooks by ID. When the overlay's `MATRIX.md` changes, [crosswalks/overlay-mapping.md](crosswalks/overlay-mapping.md) is the single file that needs updating.

Findings produced here are intended to flow back as overlay hardening input: the post-incident hardening path, reached without an incident.

## Status

Pre-release. Conformance level **L1 Implemented** per [VALIDATION.md](VALIDATION.md): all six kill-switch modes are invocable in the overlay's reference implementation, and the fixture is green with 24 of 31 techniques shown to discriminate. No exercise in this repository has been executed against a real deployment by anyone. The `TODO` cells in [MATRIX.md](MATRIX.md) are overlay-playbook mappings awaiting direct evidence, not missing standard IDs: the ATLAS and OWASP crosswalks are transcribed.
