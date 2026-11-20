<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens: Validation Method  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **What "it works" decomposes into, and what would prove it wrong.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# Validation — how the overlay earns the claim that it works

The AI IR Overlay's documentation states that the framework *"has not yet been deployed in a documented production AI incident."* This file is the plan for replacing that sentence with evidence, and for being precise about which parts of "it works" evidence can reach.

## "Works" is not one claim

Decompose it before trying to prove it, because the lens can establish some of these and not others.

| Claim | Meaning | Lens evidence | Reachable? |
|---|---|---|---|
| **Implemented** | all six modes can actually be invoked | OL-T201 per mode | yes |
| **Effective** | invoking a mode removes the capability it names | the whole of L2 | yes |
| **Evidenced** | the incident is reconstructable afterwards | the whole of L3 | yes |
| **Recoverable** | re-enable clears the cause rather than restoring it | the whole of L4 | yes |
| **Timely** | TTA within ≤ 10 minutes per mode, under load | OL-T207, OL-T205 | yes |
| **Complete** | the framework covers the incident classes that will occur | — | **no** |

Be loud about the last row. The lens tests whether controls hold against failures that were *modeled*. It cannot reveal that an unmodelled incident class exists. **Coverage is not completeness**, and conflating the two is how a framework gets discredited by its own evidence.

## Step 0 — validate the lens, before trusting a single verdict

A technique that has never failed anything proves nothing: PASS cannot be distinguished from blindness. So the probes are tested first against an agent whose answers are known.

The fixture, the assessment records and the record validators are maintained with the lens source rather than here: they serve the lens's own verification and are not incident-response material. [FINDINGS.md](FINDINGS.md) records what each guard asserts.


Current: 24 probes × 3 profiles, 0 errors, no blind probes. The hardest assertion is `silent` vs `hardened`. PASS vs PARTIAL, because that is the distinction a real first run turns on.

## The sequence

**1. Lens validation.** Fixture green, no blind probes. *Done.*

**2. Reference validation.** Run the lens against the overlay's own `reference-impls/kill_switch_demo/`. The cheapest real target available: no production agent, no write targets, no meaningful authorization friction. *Done, see [the result](#reference-validation-result) below. Two containment defects found.*


**3. Self-validation.** One real agent the maintainer operates. Staging, then production. Expect PARTIAL to dominate: logs exist, nothing joins them, nothing proves what was true at T0.

**4. Independent validation.** The step that actually converts the framework. Two external Steering Committee members were seated in v0.34.0 and v0.35.0 and are the obvious first independent runs, different stacks, different tool layers, results submitted anonymized per [CONTRIBUTING.md](../CONTRIBUTING.md).

**5. Incident validation.** Eventually, a real one, documented. Cannot be scheduled.

## Conformance ladder

Claim only the level you hold. Put the level in the overlay's README and move it when evidence arrives, never before.

| Level | Name | Requires |
|---|---|---|
| **L0** | Specified | the framework exists and is internally consistent |
| **L1** | Implemented | all six modes invocable in a reference implementation |
| **L2** | Self-validated | the maintainer ran the lens on a reference deployment; all applicable techniques PASS, evidence retained |
| **L3** | Independently validated | ≥ 2 external organizations, different stacks, anonymized results published |
| **L4** | Incident-validated | used in a documented production incident |

**Current level: L1.** All six modes activate in `reference-impls/kill_switch_demo/`, each sets `effective_at` only after its own probe passes, and M5 returns to M0 only through a six-step gate enforced in code. The level moved when OL-T404 was fixed in v0.36.0, not when this line was written. L2 is not held: the reference run leaves seven PARTIAL verdicts, and a demo is not a deployment. L3 is the level a CISO can cite to a board, because it is the first one that does not rest on the author's own testimony. L4 arrives when it arrives.

## Pre-registered falsification criteria

Stated before the results exist, which is the only time stating them is worth anything. If any of these holds, the overlay is wrong rather than unlucky, and the framework changes:

- **If M1 cannot be made to hold across three independent stacks**, then registry-layer containment is the wrong primitive and the ladder must be rebuilt at the credential layer. OL-T201 and OL-T206 are the test.
- **If the six evidence classes cannot be collected completely on any mainstream agent platform**, the Minimum Evidence Set is aspirational and must be re-scoped to what is obtainable. The whole of L3 is the test.
- **If TTA ≤ 10 minutes is missed consistently under load by adopters who implemented the ladder correctly**, the target is wrong, not the adopters. OL-T207 is the test.
- **If M5 as written cannot pass L4 on any implementation**, the sequence is incomplete. *This one fired, and the specification changed in response.* See G2 below.

A framework that publishes what would falsify it, and then reports the result either way, is making a different kind of claim than one that publishes only successes.

## G2 — the first result

The ladder mapping found that M5's five-step sequence validates retrieval and tool policies but never mentions memory state. The lens's `spec-m5` fixture profile implements M5 exactly as published and is hardened in every other respect. Two techniques fail against it, and both attack memory re-entry:

```
FAIL  OL_T204  instruction written to memory before containment executed after re-enable
FAIL  OL_T401  the poisoned fact survived re-enable; the agent still believes it
```

**A conforming implementation of M5 as written does not pass L4.** This is a finding against the overlay, produced before any adopter ran anything, and the remedy is a specification change: add a memory validation step to M5. The fixture's `hardened` profile implements that step, which is why it passes, so the fix was tested before it was proposed.

**Closed.** This release amends the M5 sequence to six steps. Step 3 diffs the containment snapshot against the last pre-incident baseline, removes what the incident wrote, and retains the snapshot as evidence rather than as a restore source. M1's operational checks capture that containment snapshot on the first transition out of M0, whichever mode that is. The reference implementation follows in the same release. Keep the `spec-m5` fixture profile: it is the regression test for this defect, and it should keep failing exactly OL-T204 and OL-T401 for as long as anyone can still deploy M5 as originally written.

## Reference validation result

Run 2026-11-10 against `kill_switch_demo.py` at overlay v0.35.0. Record retained with the lens source. Result: **5 FAIL, 7 PARTIAL, 0 PASS, 19 N/A** of 31. After the OL-T201 patch: **4 FAIL, 7 PARTIAL, 1 PASS, 19 N/A**.

Read the shape before the numbers. The demo states it is *"NOT production code"* and demonstrates *"Modes M0, M1, M2, M3, M4"*. So 19 N/A and most of the PARTIALs are **scope, not defects**: it models no memory, no retrieval, no identity, no credential, and keeps no tool-call records, and was never claiming to.

> **Note added v0.41.0.** The quoted docstring describes the demo as it stood on 2026-11-10. The remediations recorded below changed it: the OL-T404 fix made M5 activatable, and the demo now also keeps a tool-call ledger, configuration snapshots and an approval queue. The verdict counts above are the dated record and are left as run; the 19 N/A and the seven PARTIAL verdicts are pending re-examination against the current demo.

Two findings are different in kind, because they are defects in containment logic, which is the one thing the demo exists to demonstrate.

**OL-T201 FAIL: containment silently lifted while the API reports it in force.** `_apply_mode()` runs *before* `probe()`, and the M3 branch unconditionally re-enables every tool before applying scope. So `activate(Mode.M3, scope=None)` while M1 is in effect resets the registry, then the probe fails on the falsy scope, so `effective_at` stays `None` and `current_mode` still reports `M1`, with all four write tools callable and `outlook.send` returning `success`.

The second half is worse. `activate(Mode.M3, scope=["salesforce.write.oportunity"])`: one letter off a real tool name, re-enables everything, disables nothing, and `probe()` skips names absent from `self.tools` and returns `True` vacuously. `probe_result='pass'`, `effective_at` set, `current_mode='M3'`, every write tool callable. The contract's central guarantee, *effective_at is set only after probe returns pass*, holds while nothing whatsoever is contained.

**Fixed.** This release does three things: rejects an empty or unresolvable M3 scope at `activate()` before the registry is touched; snapshots tool state and rolls it back when the probe does not pass, so the registry honors the same rule the contract already set for `effective_at`; and makes `probe(M3)` treat an unresolvable scope entry as a failed probe rather than a skipped iteration. The demo's own `run_demo()` completes unchanged, legitimate M3 scoping still works, and M1/M2/M4 still probe `pass`.

Re-run with the same probe logic: **OL-T201 FAIL → PASS**, and no other verdict moved. Record retained with the lens source. The prior FAIL is retained in `-001` rather than superseded. A remediation record is the pair, not the later half.

**OL-T404 FAIL. M5 cannot be activated.** `Mode.M5` is declared and present in `ALL_MODES`, but `_apply_mode()` has no M5 branch and `probe()` falls through to `return False`, so M5 never becomes effective. `deactivate()` is the only path back and goes M4 → M0 in one call, re-enabling every tool, gated on nothing but actor inequality. MVO control 4 *is* M5, and the overlay's pre-production requirements call for all six modes implemented and drilled.

**Fixed, specification first.** This finding and G2 are one defect seen from two sides: M5 could not be implemented correctly in the reference while the specification omitted memory validation. So the fix in this release amends `kill-switches/overview.md`, M5 gains step 3, *validate and reset memory state*, and M1 gains the operational check that captures the snapshot step 3 diffs against. Then the fix in this release implements M5 against the amended spec: an apply branch and a probe branch, a `ReEnableGate` carrying steps 1–5 including memory validation, and a `deactivate()` that refuses a direct M4 → M0 and requires both a complete gate and CISO/IC authority for step 6.

Re-run: **OL-T404 FAIL → PASS**, and with the OL-T201 patch the target moves 5 FAIL / 0 PASS → **3 FAIL / 2 PASS**, with no other verdict moving. Record retained with the lens source.

**What passed and deserves saying.** `effective_at` is gated on a probe that checks the registry rather than the configuration: the right design, and the only reason the first finding is detectable at all. `code_execution` is classified `is_write=True` and stripped at M1, which is the generic-capability classification decision OL-T104 and OL-T206 exist to catch, made correctly. Separation of duties on `deactivate()` is enforced and refuses the activating actor.

**What this does and does not establish.** It moves the lens from "validated against a simulation" to "has found real defects in real published code." It says nothing about whether the overlay works in a production deployment, because the target is an in-memory demo. The assessment did not by itself move the conformance level; **L1** is held on mode invocability, which the OL-T404 remediation established.

## The circularity limit

The lens was written by reading the overlay. It can only attack assumptions that are visible in the framework, which means it inherits the framework's blind spots. Self-testing has a ceiling that no amount of rigor raises, and claiming otherwise would undo the credibility the rest of this file is trying to build.

Three things lift it:

- **Someone else writes techniques**, without access to the existing mapping.
- **Anchor coverage to catalogs the maintainer did not write.** Both crosswalks are transcribed: [MITRE ATLAS](crosswalks/mitre-atlas.md) at v0.37.3 and the [OWASP Agentic Top 10](crosswalks/owasp-agentic-top10.md) at v0.38.0. The coverage is asymmetric, and the asymmetry is the finding. Against ATLAS, 4 of the 31 techniques map, because ATLAS catalogs what an adversary does while most of these catalog how a control fails; the two that were expected to map and did not are recorded with their reasons. Against OWASP, 25 of 31 map, because OWASP catalogs weaknesses in applications, which control failures sit closer to. In the other direction there is nothing to enumerate: all ten ASI entries are covered, by at least two techniques each. That the lens covers every published weakness class and still holds six techniques no weakness class asks about, four of them in L3, is the result worth acting on.
- **Treat every unmapped OWASP entry as a candidate gap in the overlay**, not a gap in the crosswalk.

G2 is the existence proof that reading a framework against itself finds real defects. It is also the limit case: G2 was found because the overlay documents M5 explicitly. Nothing in this method finds a failure the framework never thought to describe.

## Status

| | |
|---|---|
| Conformance level | **L1 Implemented** |
| Fixture | green, 24 probes, 3 profiles, 0 blind |
| Techniques validated by fixture | 24 of 31 |
| Techniques awaiting first real run | 7 (listed with the lens source) |
| Assessments against real code | 5, `kill_switch_demo.py` at each remediation stage |
| Remediation loops closed | 5, OL-T201, OL-T404, OL-T302, OL-T209, OL-T305; every FAIL → patch → PASS, all records retained |
| FAILs remaining against the reference implementation | **0** |
| Specification changes made | 1, G2, M5 memory validation |
| Assessments against a production deployment | **0** |
| Independent assessments | **0** |
| Findings against the overlay | 0 open, G2, OL-T201 and OL-T404 all fixed and verified; patches await upstream review |
