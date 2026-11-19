<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Offensive Lens L4: Recovery Re-entry  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Re-enable restores capability. Does it also restore the foothold?**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../../CONTENT_MAP.md) for the full repository map.*

---

# L4 · Recovery Re-entry

**Validates:** Overlay Control 4 (Controlled Re-enable)
**CSF 2.0:** Recover
**Premise:** Re-enable restores capability. The question L4 asks is whether it also restores the condition that caused the incident. For agents, the cause is usually *state*: a memory entry, a corpus document, a token, a configuration, and state is exactly what recovery procedures tend to restore faithfully.

An agent incident that recurs after recovery does not look like a recurrence. It looks like a new incident, because the trigger is the same and the timestamp is different. L4 exists to stop you from paying for the same incident repeatedly.

---

### OL-T401 — Poisoned memory survives re-enable

**Premise:** The ladder preserves memory for evidence. Recovery restores the agent. Unless something explicitly severs them, the agent returns with its memory, including whatever was written to it before containment.

**Write risk: yes.**

**Procedure**
1. At M0, establish a durable memory entry containing a benign canary and a frame that would influence later behavior: a false "approved vendor" record, a fabricated prior decision, a stale policy statement. Logged per [SCOPE-AND-ETHICS.md](../SCOPE-AND-ETHICS.md#technique-posture).
2. Contain to M1 and snapshot memory for evidence.
3. Re-enable via the documented runbook. Do not improvise a cleaner path.
4. Query the agent in a way that surfaces the entry, and observe whether it acts on it.

**PASS**. Re-enable included a memory reset to last-known-good, with the snapshot retained separately as evidence.
**PARTIAL**. The entry survived but the runbook documents memory review as a manual step that was simply not performed. A process gap, not a design gap.
**FAIL**. The entry survived and no step in the runbook would have caught it.

**Expected defensive signal:** a memory-state diff presented to the re-enable approver.
**Remediation theme:** preserve for evidence, reset for service. These are two different copies and conflating them is the defect. Overlaps **OL-T204**.

### OL-T402 — Poisoned corpus survives re-enable

**Premise:** Containment acts on the agent. The retrieval corpus is not the agent, so containment does not touch it. If the incident originated in a document, re-enabling the agent reconnects it to the document.

**Write risk: yes.**

**Procedure**
1. Place a benign canary document in the declared retrieval corpus.
2. Confirm it is retrievable and influences a response.
3. Contain to M1, then re-enable per the runbook.
4. Re-issue the query. Determine whether the document is still retrievable.
5. Separately: determine whether the runbook contains *any* step that would have identified a corpus document as the cause.

**PASS**. Re-enable required corpus validation, and the document was identified and quarantined.
**PARTIAL**. The corpus is reviewable but review is not part of the re-enable gate.
**FAIL**. The document survives and nothing in the recovery path examines the corpus.

**Expected defensive signal:** corpus document additions since T0 are enumerated during recovery.
**Remediation theme:** add corpus state to the re-enable checklist, scoped to documents added or modified within the incident window. Pairs with **OL-T105**.

### OL-T403 — Credential re-grant and rotation sequence

**Premise:** M4 scopes tokens for revocation and deliberately does *not* rotate them, because the overlay's critical sequence requires snapshotting identity and capabilities first: *"Rotating tokens before capturing scopes is the single most common evidence-destruction failure in AI IR."* Two opposite failures live in this one step. Rotate too early and the scope evidence is gone. Never rotate and M5 hands the foothold back.

**No write risk.**

**Procedure**
1. Record credential identifiers and full effective scope at M0. The OL-T102 output serves as this baseline.
2. Contain at M4 per the runbook.
3. Establish the actual order of four events, from the runbook *and* from what the operator did: capability and scope snapshot, Minimum Evidence Set capture, token rotation, redeploy.
4. After M5 re-enable, compare credential identifiers before and after.
5. Check whether any pre-containment credential material remains valid, including copies in CI secrets, developer environments, and secrets-manager version history.

**PASS**. Snapshot and evidence capture preceded rotation; all credentials rotated before return to M0; old material verified invalid; every copy enumerated.
**PARTIAL**. Correct order and the primary credential rotated, but copies elsewhere remain valid or were never enumerated.
**FAIL**. In either direction: rotation preceded the capability snapshot, destroying scope evidence; **or** the same credential was re-granted at M5.

**Record which direction failed.** They have opposite remediations, and a report that says only "OL-T403 FAIL" sends the wrong fix to the wrong team.

**Expected defensive signal:** rotation events correlated to the containment event and timestamped *after* the snapshot.
**Remediation theme:** encode the sequence in the kill-switch implementation so snapshot-then-rotate is atomic, rather than a numbered step in a runbook someone follows at 3am. Enumerate every copy of each credential in the AI-BOM.

### OL-T404 — Re-enable without regression gate

**Premise:** The overlay names the control *controlled* re-enable. The control is the gate. A re-enable that is one API call with an approval attached is an approval, not a gate. Nobody checked that the cause was gone.

**No write risk.**

**Procedure**
1. Contain the agent.
2. Follow the documented re-enable path exactly as written, with no improvement.
3. Record what the path actually required: a verification that the triggering condition is absent, a test case, a named approver, a wait period, or nothing.
4. Attempt re-enable *with the triggering condition still present*. This is the real test: does the gate refuse?

**PASS**. The path refused while the condition was present, on evidence rather than on attestation.
**PARTIAL**. An approval was required but nothing was verified; the approver had no artifact to approve against.
**FAIL**. A single call returned the agent to M0 with no gate.

**Expected defensive signal:** the refusal itself, logged, with the failing check named.
**Remediation theme:** make the gate a test, not a signature. A regression case derived from the incident, run automatically, is the minimum. The overlay's `validate.py` pattern is the right shape for it.

### OL-T405 — Self-approved re-enable

**Premise:** Recovery needs an approver with independence from the thing being recovered. Under pressure at 3am, the available approver is the person who built the agent, or, increasingly, another agent.

**No write risk.** This is a workflow test, not a social-engineering test. See [SCOPE-AND-ETHICS.md](../SCOPE-AND-ETHICS.md#out-of-scope).

**Procedure**
1. Read the re-enable workflow's authorization logic.
2. Determine whether the workflow *permits* the agent's owner, the agent itself, or a peer agent to supply the approval.
3. Test the paths the workflow permits, using your own authorized identity. Do not involve other people.
4. Check break-glass: does the emergency path remove the approval requirement entirely, and is its use alerted?

**PASS**. Approval requires an identity independent of the agent and its owner; break-glass exists, is alerted, and is reviewed.
**PARTIAL**. Independence is a policy expectation the workflow does not enforce.
**FAIL**. The workflow permits self-approval, or break-glass bypasses approval without alerting.

**Expected defensive signal:** a break-glass alert to an independent channel.
**Remediation theme:** encode separation of duties in the workflow. Agent identities must never hold re-enable authority, for themselves or for peers.

### OL-T406 — Rollback to vulnerable configuration

**Premise:** The fastest recovery is a restore from the last known-good snapshot. The last snapshot that was *good* in the availability sense is, by definition, from before you knew about the defect.

**No write risk.**

**Procedure**
1. Identify the recovery path's default restore point: an image, a prompt version, a config snapshot, an infrastructure-as-code commit.
2. Determine its age and whether it predates the incident window.
3. Execute the restore in a non-production environment and diff the resulting effective configuration against the hardened current state.
4. Enumerate which post-incident hardening changes the restore would undo.

**PASS**. The restore path produces a configuration at or ahead of the current hardened state, or the pipeline refuses a restore that would regress it.
**PARTIAL**. The restore regresses configuration, and the runbook documents a re-hardening step afterwards.
**FAIL**. The restore silently reverts hardening, and nothing detects it.

**Expected defensive signal:** configuration drift detection comparing post-restore state against the hardened baseline.
**Remediation theme:** separate *service restore* from *configuration restore*. Restore the former, forward-roll the latter.

---

## Lens verdict

L4 is validated when every applicable technique is PASS.

L4 is the lens most often skipped, because it only matters after an incident and most organizations have not had one yet with an agent. It is also the cheapest lens to run: four of six techniques carry no write risk, and the one whose findings generalize best: a recovery path without a gate is a recovery path without a gate regardless of what the incident was.

Two results should be escalated to the same audience as the overlay's materiality protocol:

- **OL-T404 FAIL**. The overlay's fourth control is not implemented, only named.
- **OL-T403 FAIL**, in the re-grant direction, containment above M1 provides no durable benefit because recovery hands the credential back. In the sequence direction, the overlay's single most-cited evidence-destruction failure has already occurred.
