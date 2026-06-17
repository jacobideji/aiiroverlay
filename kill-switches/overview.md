<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Kill-Switch Modes (M0-M5)                                                              -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji                 -->
<!--  https://jacobideji.com                                                -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package              -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Containment is not one switch. Six modes with TTA targets.**
>
> *This file is one self-contained piece of the AI IR Overlay framework.
> Cross-references to other pieces point to other packages in the same set,
> which you can obtain at [jacobideji.com](https://jacobideji.com).*

---

# Kill-Switch Modes — The Containment Ladder

> The "kill switch" is not one switch. It is six modes that escalate from passive observation to full disable, and back.

Binary on/off is rarely appropriate in production. The Overlay defines **six modes** so containment can be calibrated to confidence, impact, and business need.

---

## The Modes at a Glance

| Mode | Name | Use when | TTA target | Approver |
|---|---|---|---|---|
| **M0** | Observe | Normal operations | n/a | Owner |
| **M1** | Read-Only | Suspicious behavior; low/moderate impact | **≤ 10 min** | Tier-1 SOC |
| **M2** | Approvals Required | Agent must keep operating; actions need two-person rule | **≤ 10 min** | Tier-1 SOC |
| **M3** | Tool Tiering | Targeted containment — disable high-risk tools only | **≤ 10 min** | Tier-1 SOC |
| **M4** | Full Disable | Active harm, confirmed misuse, or evidence of compromise | **≤ 10 min** | Tier-1 SOC |
| **M5** | Controlled Re-Enable | Containment validated; staged recovery | n/a | CISO / IC |

> **TTA** = Time-To-Activate. Measured from incident-commander order to mode in effect.

---

## Mode 0 — Observe (Baseline)

**Purpose:** Normal operations with logging.

**Requirements:**

- Tool calls logged with parameters and outcomes
- Prompt/response logged for the configured retention window
- Identity correlation in SaaS audit logs

**Exit criteria:** Incident declared → step up to M1 (or further) based on confidence.

---

## Mode 1 — Read-Only (Preferred First Containment)

**Purpose:** Stop writes without stopping the business.

**What changes:** All write tools are stripped from the agent's tool set. Read and query tools remain.

**Use when:**

- Suspicious behavior with unclear scope
- Business impact appears low to moderate
- You need time to investigate without triggering customer-visible failures

**Operational checks:**

- [ ] All write tools confirmed disabled in production config
- [ ] Test query confirms reads still function
- [ ] Logging continues at M0 fidelity

**Exit criteria:** Investigation confirms benign (return to M0), confirms harm (step up to M3/M4), or requires continued operation with control (step to M2).

---

## Mode 2 — Approvals Required (Two-Person Rule)

**Purpose:** Continue operation, but no action without a human approver.

**What changes:** Every tool call is queued for human approval before execution.

**Use when:**

- Agent must continue for business continuity
- Risk of automated action is unacceptable
- Cost of full disable is higher than approval latency

**Operational checks:**

- [ ] Approval queue is staffed
- [ ] Average approval latency is acceptable for business need
- [ ] Approver has authority to deny

**Exit criteria:** Risk reduced (return to M1 or M0), or containment must escalate (M3/M4).

---

## Mode 3 — Tool Tiering

**Purpose:** Selectively contain — disable high-risk tools, keep low-risk.

**What changes:** Specific tools (external email send, code deploy, financial actions) are disabled. Lower-risk tools (internal search, status lookup) remain.

**Use when:**

- The harm vector is known and isolated to specific tools
- Business needs require continued operation of unaffected tools
- Full disable would cause unacceptable disruption

**Operational checks:**

- [ ] Tier definitions are pre-documented (see the `template-agent-privilege-matrix` package)
- [ ] Disabled tools confirmed unreachable in production
- [ ] Remaining tools confirmed operational

**Exit criteria:** Vector contained (step down to M1/M2), or scope expands (M4).

---

## Mode 4 — Full Disable

**Purpose:** Hard stop.

**What changes:** Agent is taken offline. Active sessions are terminated. Tokens are scoped for revocation (not yet rotated — see Evidence Plan).

**Use when:**

- Active harm is occurring
- Compromise is confirmed
- Containment under M1–M3 has failed

**Operational checks (critical sequence):**

- [ ] **Snapshot identity and capabilities BEFORE token rotation** (see Step 2 of the `evidence-minimum-set` package)
- [ ] **Capture the Minimum AI Evidence Set BEFORE redeployment**
- [ ] Only then: rotate credentials, clean corpora, redeploy

> Rotating tokens before capturing scopes is the single most common evidence-destruction failure in AI IR.

**Exit criteria:** Eradication complete → M5 controlled re-enable.

---

## Mode 5 — Controlled Re-Enable (Recovery)

**Purpose:** Restore operation in stages, with validation at each step.

**Sequence:**

1. **Re-enable in Read-Only (M1)** — confirm the agent functions and logs flow
2. **Validate retrieval and tool policies** — corpora versions confirmed clean
3. **Replay the incident scenario in a safe harness** — confirm fix holds
4. **Re-enable tools incrementally** — start with low-risk, monitor for drift
5. **Return to M0 Observe** — only after all of the above

**Approver:** CISO or designated Incident Commander. **Never** the original agent owner alone.

**Operational checks:**

- [ ] Post-incident hardening complete (see the `playbook-18` package)
- [ ] Monitoring thresholds updated to detect recurrence
- [ ] Tabletop scheduled within 30 days to validate the fix

---

## Pre-Production Requirements

Before ANY agent reaches production:

- [ ] All six modes have been **implemented** in code/config
- [ ] All six modes have been **tested** in a tabletop drill
- [ ] **TTA targets are met** in measurement (not promised)
- [ ] Runbook documents who pulls which lever, with backup approvers

If any of the above is "not yet," the agent is not production-ready.

---

## Related

Distributed as separate packages:

- **The Six Triage Questions** — `triage-six-questions`
- **Minimum Evidence Set** — `evidence-minimum-set`
- **Tool Design Is Containment** (Playbook 04) — `playbook-04`
- **Testing for Agent Failure Modes** (Playbook 14) — `playbook-14`
