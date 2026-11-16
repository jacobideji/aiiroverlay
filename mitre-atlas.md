<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens Crosswalk: MITRE ATLAS  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Partial by nature. ATLAS catalogs adversary technique, the lens catalogs control failure.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../../CONTENT_MAP.md) for the full repository map.*

---

# Crosswalk — Offensive Lens → MITRE ATLAS

**Status: unfilled, deliberately.** ATLAS technique IDs must be transcribed from the live matrix, which is versioned and revised. Do not fill these cells from memory.

## Why this crosswalk exists

ATLAS is the recognized vocabulary for adversarial behavior against AI systems. An Offensive Lens report that speaks ATLAS can be read by a threat-intel team without translation, and lens findings can be lined up against real observed adversary behavior rather than against a framework's own assumptions.

## Why the mapping is partial by nature

ATLAS catalogs what an adversary does to an AI system. The Offensive Lens catalogs how a response control fails. These are adjacent, not congruent:

- Most L1 and L3 techniques will have **no ATLAS counterpart**. "The AI-BOM is stale" and "retention is shorter than detection latency" are control defects, not adversary techniques. Leave them unmapped.
- L2 and L4 techniques map more readily, because bypassing containment and surviving recovery are things adversaries actually do: the ATT&CK-side concepts to look for are defense evasion and persistence.
- Where a lens technique maps cleanly to an ATLAS technique, the lens exercise becomes an **ATLAS-aligned detection test**: run it, then ask whether detection engineering covers that ATLAS ID. That is the highest-value use of this table.

## Table

| Technique | ATLAS tactic | ATLAS technique ID | Confidence | Notes |
|---|---|---|---|---|
| OL-T204 | TODO | TODO | | memory-mediated persistence |
| OL-T206 | TODO | TODO | | evasion by capability rerouting |
| OL-T307 | TODO | TODO | | adversary-authored content in the evidence path |
| OL-T401 | TODO | TODO | | persistence through recovery |
| OL-T402 | TODO | TODO | | corpus persistence through recovery |
| OL-T403 | TODO | TODO | | valid-credential persistence |
| all others | — | — | n/a | control defects with no adversary-technique counterpart |

Record the ATLAS matrix version used, alongside the overlay version, in the assessment record's `scope_note`.
