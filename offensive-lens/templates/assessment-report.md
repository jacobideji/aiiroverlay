# Offensive Lens Assessment — <agent or estate>

| | |
|---|---|
| Assessment ID | |
| Engagement ID | ENG-____-__-___ |
| Assessed | |
| Lens version | 0.3.0 |
| Overlay version assessed against | v____ |
| Environment | |
| Scope note | |

> Verdicts are not portable across overlay versions that change the ladder or the evidence set. Record the overlay version or the report expires silently.

## 1 · Verdict summary

| Lens | Control validated | Verdict | Techniques run | PASS | PARTIAL | FAIL | N/A |
|---|---|---|---|---|---|---|---|
| L1 Inventory Drift | 1 · Inventory | | | | | | |
| L2 Containment Bypass | 2 · Safe Modes | | | | | | |
| L3 Evidence Starvation | 3 · Evidence | | | | | | |
| L4 Recovery Re-entry | 4 · Controlled Re-enable | | | | | | |

A lens is **VALIDATED** only when every applicable technique is PASS.

## 2 · What this means for incident response

Written for the person who will make the materiality call, not for the engineer who will fix it. Answer directly:

- Which incident questions can we currently answer with evidence?
- Which can we not answer at all?
- If the ladder were invoked today, what would still be able to write?
- If we recovered today, what would come back with the agent?

## 3 · Findings

One subsection per finding. Mirror the `finding` schema, maintained with the lens source.

### <OL-Txxx> — <technique name> · <VERDICT>

| | |
|---|---|
| Lens / control | |
| Severity | |
| Defensive signal | fired / late / absent / unattributable |
| Write occurred | |
| Overlay playbook | |

**Observed**: what happened, factually, with no interpretation.

**Evidence**: class, locator, redaction status, hash.

**Why it matters**. The incident question this makes unanswerable, or the write path it leaves open.

**Remediation**: the control change, not the symptom fix.

## 4 · The six-class evidence grid

Report L3 as a grid, not as a verdict list. This table is what tells a CISO which incident questions are unanswerable today.

| Evidence class | Present | Complete | Survives containment | Attributable | Retention vs. discovery latency |
|---|---|---|---|---|---|
| Prompts / responses | | | | | |
| Tool-call records | | | | | |
| Retrieval traces | | | | | |
| Memory state | | | | | |
| Configuration state | | | | | |
| Identity / downstream audit | | | | | |

## 5 · Residual blast radius

From OL-T207. State it as a number, because the runbook should.

| | |
|---|---|
| Agent sustained action rate | |
| Measured containment latency (under load) | |
| Residual actions before containment is effective | |
| Runbook's claimed figure | |

## 6 · Remediation priority

| # | Finding | Control change | Owner | Target date | Re-run technique |
|---|---|---|---|---|---|
| 1 | | | | | |

Every row ends with a re-run. A remediation without a re-run is an intention.

## 7 · Canary disposition

| Marker | Introduced | Removed | Confirmed absent from retrieval / memory / write targets |
|---|---|---|---|
| | | | |

## 8 · Limitations

State plainly what was not tested and why: techniques deferred on write risk, N/A techniques and their rationale, environments out of scope, and whether staging is representative of production. A reader who cannot see the boundary of the assessment will assume it has none.
