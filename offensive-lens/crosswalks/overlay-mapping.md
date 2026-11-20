<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens Crosswalk: Overlay Controls  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Every mode, every variant, and the technique that tests it.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../../CONTENT_MAP.md) for the full repository map.*

---

# Crosswalk — Offensive Lens → AI IR Overlay

This is the **single file to update** when the overlay's `MATRIX.md` or `kill-switches/overview.md` changes. Nothing else in this repository references overlay playbook IDs or ladder semantics.

Mapped against the overlay's [`kill-switches/overview.md`](../../kill-switches/overview.md) in this repository, at whatever release this file ships in. It names no overlay version, because it cannot then fall behind one.

## Control mapping

| Overlay MVO control | Lens | What the lens falsifies |
|---|---|---|
| 1 · Inventory (AI-BOM) | [L1](../lenses/L1-inventory-drift.md) | That the AI-BOM describes runtime capability |
| 2 · Safe Modes (M0–M5) | [L2](../lenses/L2-containment-bypass.md) | That a ladder mode removes the capability it names |
| 3 · Evidence (six classes) | [L3](../lenses/L3-evidence-starvation.md) | That the evidence set exists, is complete, and survives containment |
| 4 · Controlled Re-enable (M5) | [L4](../lenses/L4-recovery-reentry.md) | That recovery clears the cause rather than restoring it |

## Ladder mapping

The overlay defines six modes with a drill-measured **Time-To-Activate (TTA) target of ≤ 10 minutes for M1 through M4**, measured from incident-commander order to mode in effect. Every row below inherits that target; OL-T207 measures it.

| Mode | Overlay name and assertion | Techniques that test it |
|---|---|---|
| **M0** | *Observe.* Tool calls logged with parameters and outcomes; prompt/response logged for the retention window; identity correlation in SaaS audit logs. | OL-T301, OL-T302, OL-T303, OL-T305, OL-T306, OL-T308. M0's requirements **are** the L3 evidence baseline. A deployment failing L3 is not at M0. |
| **M1** | *Read-Only.* All write tools stripped from the tool set; read and query tools remain. Checks: write tools confirmed disabled, test query confirms reads function, logging continues at M0 fidelity. | OL-T201 (primary), OL-T202, OL-T203, OL-T204, OL-T206, OL-T207; OL-T104 (whether the preserved read-only set is actually inert); OL-T304 (whether M0 logging fidelity really continues) |
| **M2** | *Approvals Required.* Every tool call queued for human approval. Checks: queue is staffed, approval latency acceptable, approver has authority to deny. | OL-T208 (primary, paths that bypass the queue), OL-T209 (staffing, latency, and authority to deny under load), OL-T206 (agent routes around the queue), OL-T202 (actions already dispatched), OL-T207 (queue latency vs. action rate) |
| **M3** | *Tool Tiering.* Specific high-risk tools disabled, lower-risk retained. Checks: tier definitions pre-documented in the Agent Privilege Matrix, disabled tools confirmed unreachable, remaining tools confirmed operational. | OL-T104 (tier classification defect), OL-T206 (generic-capability tools defeat tiering), OL-T102 (privilege matrix vs. effective scope) |
| **M4** | *Full Disable.* Agent offline, active sessions terminated, tokens **scoped for revocation but not yet rotated**. Critical sequence: snapshot identity and capabilities *before* token rotation; capture the Minimum Evidence Set *before* redeployment. | OL-T304 (session termination destroying memory evidence), OL-T403 (sequence discipline, see note), OL-T205 (availability when it matters), OL-T202, OL-T207 |
| **M5** | *Controlled Re-Enable.* Six staged steps: re-enable at M1 → validate retrieval and tool policies → validate and reset memory state → replay the incident in a safe harness → re-enable tools incrementally → return to M0. Approver is CISO or IC, **never the original agent owner alone**. | OL-T404 (step 4, the replay gate), OL-T405 (approver independence), OL-T402 + OL-T105 (step 2, corpora versions confirmed clean), OL-T406 + OL-T201 (step 5, incremental re-enable), OL-T403 (step after M4 rotation), OL-T401 + OL-T204 (step 3, memory validation; **see gap G2**, closed) |

### M3 variants

The overlay documents scenario-scoped variants of M3. A variant narrows an existing mode; it does not add a mode. Each one is a distinct containment claim and therefore a distinct test.

| Variant | Source playbook | Techniques |
|---|---|---|
| **M3-RAG**, retrieval cut to the suspect corpus | PB03 RAG / Knowledge-Base Forensics | OL-T402, OL-T105, OL-T303 |
| **M3-Delegation Cap**, delegation depth capped | PB08 Multi-Agent Blast Radius | OL-T203 |
| **M3-Workflow**, ingestion paused on the affected channel | PB06 Prompt Injection as a Workflow Threat | OL-T307 |
| **M3-Output**, output channel or destination class disabled | PB09 Leakage Without a Breach | OL-T210 |
| **M3-Drift**, recently-changed component rolled back | PB22 Model and Policy Drift | OL-T305, OL-T406 |
| **M3-Vendor**, containment executed vendor-side | PB10 Vendor Copilots | **out of scope by design**, [SCOPE-AND-ETHICS.md](../SCOPE-AND-ETHICS.md#out-of-scope) excludes vendor-operated agents. The customer-controllable half (identity boundary, data scope) is testable via OL-T102 and OL-T403. |
| **M4 (corpus-scoped)** | PB12 Insider Threat 3.0 | OL-T402, OL-T105 |
| **Agent suspended for user** | PB12 Insider Threat 3.0 | OL-T106, OL-T306 |

## Why L1 runs first: the Six Triage Questions

PB01 directs responders to walk the Six Triage Questions in order on the initial bridge call, and four of the six are answered **from the AI-BOM**. L1 measures whether those answers are true.

| # | Triage question | Answer source | Technique that falsifies it |
|---|---|---|---|
| 1 | What tools can the agent call? | AI-BOM `tools` | OL-T101 |
| 2 | What systems can it write to? | AI-BOM `tools[].write_targets` | OL-T104 |
| 3 | What identity does it run as? | AI-BOM `identity` | OL-T102, OL-T106 |
| 4 | Does it have memory? What is the scope? | AI-BOM `memory` | OL-T304, OL-T204 |
| 5 | What is the least disruptive safe mode? | Kill-Switch Modes | the whole of L2 |

An L1 failure is therefore not a documentation defect. It means the **first hour of a real incident produces wrong answers to the first four triage questions**, and the containment decision in question 5 is scoped against them. That is the argument for running L1 before anything else, and it is the overlay's own argument.

## Conformance instrumentation

The overlay's pre-production requirements state that all six modes must be *implemented*, *tested in a tabletop drill*, and that **"TTA targets are met in measurement (not promised)."** The Offensive Lens is the instrument for that sentence.

| Pre-production requirement | Lens evidence |
|---|---|
| All six modes implemented in code/config | OL-T201 per mode; a mode that cannot be invoked is not implemented |
| All six modes tested in a tabletop drill | a lens assessment covering M1–M5 **is** the drill, with evidence attached |
| TTA targets met in measurement, not promised | OL-T207 (measured latency under load) and OL-T205 (latency under dependency failure) |
| Runbook documents who pulls which lever, with backup approvers | OL-T205 (named-individual dependency), OL-T405 (approver independence) |

An agent that passes L1–L4 has a defensible answer to all four. That is the claim this repository exists to make testable.

## Playbook mapping

The overlay's 24 playbooks, from its repository tree. Mappings rest on one of two bases: the overlay's own kill-switch document and playbook titles, or a reading of the playbook's procedure for the step a technique's failure would invalidate. The eight rows added at v0.42.0, and three techniques added to rows that already existed, come from the second.

| Playbook | Techniques | Basis |
|---|---|---|
| PB01 Agent as Privileged Identity | OL-T101, OL-T102, OL-T106, OL-T306, OL-T403 | identity and scope are L1's subject; OL-T101 tests the AI-BOM tool list this playbook owns, and OL-T306 is the same identity problem seen from the evidence side |
| PB02 Evidence Lives in New Places | all of L3 | the six evidence classes |
| PB03 RAG / Knowledge-Base Forensics | OL-T105, OL-T303, OL-T402 | M3-RAG variant owner |
| PB04 Tool Design Is Containment | OL-T101, OL-T104, OL-T201, OL-T206, OL-T208, OL-T209 | cited by M3 tier definitions; PB04's controls include approval gates, and a write path that never consulted the registry is a tool-design defect |
| PB06 Prompt Injection as a Workflow Threat | OL-T307 | M3-Workflow variant owner |
| PB08 Multi-Agent Blast Radius | OL-T203 | M3-Delegation Cap variant owner |
| PB09 Leakage Without a Breach | OL-T210 | M3-Output variant owner |
| PB10 Vendor Copilots | out of scope | M3-Vendor variant owner |
| PB12 Insider Threat 3.0 | OL-T106, OL-T306, OL-T402 | M4 corpus- and user-scoped variants |
| PB13 Six Metrics | OL-T207, OL-T308 | Metric 2 is live TTA |
| PB14 Testing for Agent Failure Modes | the entire lens | nearest existing playbook to this repository |
| PB15 Records Retention | OL-T308 | retention vs. discovery latency |
| PB18 Post-Incident Hardening | the re-run loop below | hardening cycle owner |
| PB20 Maturity Roadmap | lens verdicts as maturity evidence | |
| PB21 Shadow AI | OL-T103 | unregistered deployments |
| PB22 Model and Policy Drift | OL-T305, OL-T406 | M3-Drift variant owner |
| PB05 Executive Decision-Making | OL-T209, OL-T303, OL-T307 | the Approval Receipt cannot render provenance the approver can act on, and packet claims tagged *Confirmed* rest on evidence |
| PB07 Secrets and Tokens | OL-T102, OL-T205, OL-T401, OL-T403, OL-T405 | the snapshot-before-rotation sequence, the scope-shrink rule, break-glass independence, and the approver this playbook names |
| PB11 Monitoring That Truly Detects | OL-T102, OL-T107, OL-T302, OL-T303 | one technique per signal family, plus the rule-calibration decay the drill schedules |
| PB16 Training Your Team | OL-T201, OL-T207 | Core Move 1 is *verify activation* against a measured TTSM; the drill scores both |
| PB17 Communication Techniques | OL-T301, OL-T306, OL-T307 | the Three-Status Taxonomy and the impact statement are built from evidence a responder reads |
| PB19 Build vs Buy | OL-T201, OL-T303, OL-T305, OL-T306 | the Proof of Readiness Test is these four techniques run against a candidate platform |
| PB23 AI Logging and Privacy | OL-T301, OL-T306, OL-T308 | Layer 2's full payload, Layer 1's correlation tokens, and the tier retention horizons |
| PB24 Board-Ready Scorecard | OL-T201, OL-T209, OL-T302 | scorecard items A1, A2 and B3 are capability claims these techniques falsify |

The rule: for each playbook, identify the technique whose failure would invalidate that playbook's *procedure*, not the playbook on the same topic, the one that would be wrong. A technique mapping to no playbook is a gap in the overlay; a playbook with no technique is a gap in the lens. Record both rather than forcing a mapping.

Applying it leaves every playbook carrying at least one technique, and two techniques carrying no playbook of their own: **OL-T202** (in-flight action completion) and **OL-T204** (memory-mediated deferred write). Both turn on the interval between dispatch and effect, OL-T202 at the tool layer and OL-T204 across a containment boundary, and no playbook's procedure has a step that interval would break. PB14 covers them as it covers the whole lens, which is not the same as a playbook whose procedure they test. They are recorded here rather than forced onto the nearest playbook on the same topic, and they are the two cells `MATRIX.md` still carries as `TODO`.

## Gaps found by this mapping

Gaps in both directions are the most valuable output of this crosswalk. Three were found, and all three are now closed.

**G1. M2 Approvals Required was under-tested. Closed in 0.3.0** by OL-T208 (approval-path bypass) and OL-T209 (approval integrity under load). The latter targets M2's three operational checks directly: queue staffed, latency acceptable, approver has authority to deny.

**G2. M5's sequence validated corpora but not memory. Closed in overlay 0.36.0.** The published five-step sequence confirmed retrieval and tool policies and corpora versions, and no step addressed memory state, so OL-T401 tested a re-entry path the overlay's own recovery sequence left open. It was a finding against the specification rather than against any deployment, and the remedy was a specification change. M5 is now six steps, with step 3 validating memory against a pre-incident baseline and removing what the incident wrote. M1 gained the operational check that captures that baseline. PB01, PB14 and PB18 restate the sequence in full and carry the step as well.

**G3. M3-Output had no technique. Closed in 0.3.0** by OL-T210, which tests the destination rather than the tool name. The distinction the variant's definition turns on.

**OL-T403 sequence assertion. Closed in 0.3.0.** The overlay states that rotating tokens before capturing scopes is "the single most common evidence-destruction failure in AI IR," and M4 deliberately scopes tokens for revocation *without* rotating. OL-T403 now fails in **either** direction, rotation before snapshot, or re-grant at M5, and requires the report to name which, because the two have opposite remediations.

**No gap found by this mapping is still open.** G2 was the last of them, and it was a gap in the overlay rather than in the lens, which is the direction this crosswalk exists to catch.

## Feedback path

Findings produced here are inputs to PB18's hardening cycle, reached without an incident:

```
Offensive Lens finding (FAIL/PARTIAL)
  → overlay playbook or ladder deficiency
    → hardening change (PB18)
      → re-run the technique
        → PASS recorded, prior FAIL retained alongside
```

That last step is what the overlay currently cannot show. A re-run PASS with its prior FAIL retained is a validation record: the closest available substitute for a documented production incident, and arguably the better artifact because the conditions were controlled and repeatable.

It also satisfies M5 step 4 directly: *"replay the incident scenario in a safe harness; confirm fix holds."* A lens technique is a replayable harness by construction.
