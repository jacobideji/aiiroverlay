<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens: Technique Matrix  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **31 techniques across four lenses, mapped to the controls they test.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Offensive Lens Matrix

31 techniques, four lenses, each mapped to the overlay control it validates.

**Legend**, *Control*: overlay MVO control (1 Inventory · 2 Safe Modes · 3 Evidence · 4 Controlled Re-enable). *CSF*: NIST CSF 2.0 function, the axis NIST SP 800-61 r3 is organized on. *Write risk*: whether running the technique can produce a write to a real target, and therefore needs per-exercise sign-off per [SCOPE-AND-ETHICS.md](SCOPE-AND-ETHICS.md#authorization-gate).

Playbook IDs are filled only where the overlay's own `kill-switches/overview.md` or a playbook's stated scope gives direct evidence. Remaining `TODO` cells await authoritative IDs from the mapping, see [`crosswalks/overlay-mapping.md`](crosswalks/overlay-mapping.md#playbook-mapping). Do not fill them from memory.

## L1 · Inventory Drift

Premise: the AI-BOM is a declaration; the runtime is the truth.

| ID | Technique | Control | CSF | Overlay playbook | Write risk |
|---|---|---|---|---|---|
| OL-T101 | Undeclared tool reachability | 1 | ID | PB01 | no |
| OL-T102 | Effective-scope inflation | 1 | ID | PB01 | no |
| OL-T103 | Shadow agent deployment | 1 | ID | PB21 | no |
| OL-T104 | Transitive write path via read-only tool | 1 | ID | PB04 | **yes** |
| OL-T105 | Retrieval-corpus drift | 1 | ID | PB03 | no |
| OL-T106 | Agent identity aliasing | 1 | ID | PB01 | no |
| OL-T107 | Stale AI-BOM freshness | 1 | GV / ID | TODO | no |

## L2 · Containment Bypass

Premise: a ladder mode is a claim about capability removal. Test whether capability left. Covers M1 (OL-T201/202/204/206/207), M2 (OL-T208/209), M3 and its variants (OL-T210, with OL-T104/206), and M4 (OL-T205/207).

| ID | Technique | Control | CSF | Overlay playbook | Write risk |
|---|---|---|---|---|---|
| OL-T201 | Write-path residue after M1 | 2 | RS | PB04 | **yes** |
| OL-T202 | In-flight action completion | 2 | RS | TODO | **yes** |
| OL-T203 | Multi-agent containment relay | 2 | RS | PB08 | **yes** |
| OL-T204 | Memory-mediated deferred write | 2 | RS | TODO | **yes** |
| OL-T205 | Kill-switch control-plane dependency | 2 | RS / PR | TODO | no |
| OL-T206 | Containment-aware rerouting | 2 | RS | TODO | **yes** |
| OL-T207 | Containment application race | 2 | RS | PB13 | **yes** |
| OL-T208 | Approval-path bypass | 2 | RS | PB04 | **yes** |
| OL-T209 | Approval integrity under load | 2 | RS | PB04 | **yes** |
| OL-T210 | Output-channel containment residue | 2 | RS | PB09 | **yes** |

## L3 · Evidence Starvation

Premise: the minimum evidence set is only as good as what survives contact.

| ID | Technique | Control | CSF | Overlay playbook | Write risk |
|---|---|---|---|---|---|
| OL-T301 | Prompt / response truncation | 3 | DE | PB02 | no |
| OL-T302 | Tool-call record gap on failure | 3 | DE | PB02 | no |
| OL-T303 | Retrieval trace absence | 3 | DE | PB03 | no |
| OL-T304 | Memory volatility under containment | 3 | RS | PB02 | no |
| OL-T305 | Unversioned configuration state | 3 | ID / DE | PB22 | no |
| OL-T306 | Downstream attribution collapse | 3 | DE | PB01 | no |
| OL-T307 | Evidence poisoning via injected content | 3 | DE / RS | TODO | no |
| OL-T308 | Retention shorter than detection latency | 3 | DE / GV | PB15 | no |

## L4 · Recovery Re-entry

Premise: re-enable restores capability. Does it also restore the foothold?

| ID | Technique | Control | CSF | Overlay playbook | Write risk |
|---|---|---|---|---|---|
| OL-T401 | Poisoned memory survives re-enable | 4 | RC | TODO | **yes** |
| OL-T402 | Poisoned corpus survives re-enable | 4 | RC | PB03 | **yes** |
| OL-T403 | Credential re-grant and rotation sequence | 4 | RC / PR | PB07 | no |
| OL-T404 | Re-enable without regression gate | 4 | RC | PB18 | no |
| OL-T405 | Self-approved re-enable | 4 | GV / RC | TODO | no |
| OL-T406 | Rollback to vulnerable configuration | 4 | RC | PB22 | no |

## Coverage of the six evidence classes

L3 is specified so that every class the overlay requires has at least one technique attacking it. If the overlay's evidence set changes, this table is the check that L3 still covers it.

| Evidence class | Primary technique | Secondary |
|---|---|---|
| Prompts / responses | OL-T301 | OL-T307 |
| Tool-call records | OL-T302 | OL-T202, OL-T207 |
| Retrieval traces | OL-T303 | OL-T105, OL-T402 |
| Memory state | OL-T304 | OL-T204, OL-T401 |
| Configuration state | OL-T305 | OL-T406 |
| Identity / downstream audit | OL-T306 | OL-T102, OL-T106, OL-T403 |

OL-T403 is also an evidence technique in one of its two directions: rotating credentials before snapshotting scope destroys the identity evidence class outright.

## Selection guidance

Run the first pass ([START-HERE.md](START-HERE.md)) before selecting from this matrix. After it:

- **L1 FAIL** → run all of L1 before anything else. Inventory scopes every other exercise.
- **Single-agent deployment** → OL-T203 is N/A. Document it; revisit when a second agent ships.
- **No memory / stateless agent** → OL-T204, OL-T304, OL-T401 are N/A. Verify the claim against the runtime, not the architecture diagram; "stateless" is frequently a design-time statement.
- **No M2 implementation** → OL-T208 and OL-T209 are N/A, but record that the ladder is incomplete rather than that the techniques do not apply. The overlay requires all six modes before production.
- **No output-channel tools** (the agent cannot send externally) → OL-T210 is N/A.
- **Irreversible write targets in scope** → defer every **yes** in the write-risk column until a canary write target exists that is observable and safe to write.
