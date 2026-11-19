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

**Status: transcribed from ATLAS v5.6.0**, `mitre-atlas/atlas-data` release `v2026.10`. ATLAS technique IDs are transcribed from the live matrix, which is versioned and revised, and never filled from memory. Re-check the cells against the current matrix before citing them.

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
| OL-T204 | Persistence · Defense Evasion | `AML.T0080.000` Memory, specializing `AML.T0080` AI Agent Context Poisoning · `AML.T0094` Delay Execution of LLM Instructions | High | Memory-mediated persistence. ATLAS describes T0080.000 as manipulating LLM memory to persist changes into future sessions, which is this technique's premise; T0094 covers instructions held for a future event to bypass a control, which is the deferred write itself. |
| OL-T206 | — | — | n/a | Containment-aware rerouting has no adversary-technique counterpart: the premise is an agent trying alternatives out of competence, with no adversary in the loop. `AML.T0053` AI Agent Tool Invocation is the nearest neighbour and is not equivalent, being an adversary using agent tools rather than an agent searching around containment. |
| OL-T307 | Defense Evasion | `AML.T0071` False RAG Entry Injection · `AML.T0067` LLM Trusted Output Components Manipulation | High · Medium | Adversary-authored content in the evidence path. T0071 is content the model treats as a retrieved document, which is what this technique plants. T0067 is Medium rather than High: it manipulates output to appear trustworthy to the *user*, while this technique targets the *responder* reading evidence. |
| OL-T401 | Persistence | `AML.T0080.000` Memory, specializing `AML.T0080` AI Agent Context Poisoning | High | Persistence through recovery. ATLAS persists memory changes into future sessions; this technique asks whether re-enable severs them. |
| OL-T402 | Persistence | `AML.T0070` RAG Poisoning | High | Corpus persistence through recovery. ATLAS contaminates a future thread through indexed content; this technique asks whether re-enable leaves it indexed. |
| OL-T403 | — | — | n/a | The credential rotation sequence is a recovery-sequence defect, not an adversary technique, and ATLAS carries no valid-account persistence entry. `AML.T0055` Unsecured Credentials and `AML.T0083` Credentials from AI Agent Configuration are the techniques that benefit when the sequence is wrong. |
| all others | — | — | n/a | control defects with no adversary-technique counterpart |

Record the ATLAS matrix version used, alongside the overlay version, in the assessment record's `scope_note`. For the mapping above that is `ATLAS v5.6.0 / atlas-data v2026.10`.

Four of the six techniques this crosswalk expected to map do map. Two do not, and are recorded as unmapped rather than forced: OL-T206 describes agent behaviour that needs no adversary, and OL-T403 describes a defect in the responder's own sequence. That outcome is the crosswalk working as specified.
