# Engagement Authorization — ENG-____-__-___

Complete every section. An incomplete record means no exercise runs. The machine-readable counterpart is the `engagement-authorization` schema, maintained with the lens source; the lens's own record validator refuses to validate an assessment whose engagement does not resolve.

## 1 · Authorizer

| | |
|---|---|
| Name | |
| Role | |
| Authority over the target deployment | *(how, not "my manager said yes")* |
| Approved at (UTC) | |
| Written record locator | *(change record, ticket, signed doc)* |

## 2 · Environment

- [ ] Development
- [ ] Staging
- [ ] Production. Requires a clean staging result for every technique in scope, and re-acceptance of section 4.

## 3 · Targets — enumerated

A tenant name or a wildcard is not an enumeration. One row per agent.

| Agent ID | Deployed identity | AI-BOM ref | Tools in scope | Write targets in scope |
|---|---|---|---|---|
| | | | | |

## 4 · Blast radius

One row per in-scope write target.

| Write target | Worst realistic outcome | Reversible? | Accepted by | Date |
|---|---|---|---|---|
| | | | | |

**Irreversible targets** are payments, external communications, production deletes, anything a customer sees. Each requires per-exercise sign-off naming the technique IDs approved against it.

| Target | Approved technique IDs | Signed off by | Date |
|---|---|---|---|
| | | | |

## 5 · Stop condition

| | |
|---|---|
| Owner who can halt the engagement | |
| How testers reach them | |
| Reachable within (minutes) | |

## 6 · Notification decision

- [ ] SOC notified in advance
- [ ] SOC **not** notified: a deliberate choice, to measure detection latency honestly

Decided by: ___________ on ___________

Either choice is legitimate. An unrecorded choice is not.

## 7 · Canary register

Every marker introduced during the engagement, so a sighting months later is attributable to an exercise rather than treated as a live incident.

| Marker | Technique | Introduced (UTC) | Removed (UTC) | Location |
|---|---|---|---|---|
| | | | | |

## 8 · Acknowledgements

The engagement team confirms it has read [SCOPE-AND-ETHICS.md](../SCOPE-AND-ETHICS.md) and that:

- [ ] No third-party or vendor-operated agent is in scope.
- [ ] No model-provider guardrail or safety-filter bypass is in scope.
- [ ] No social engineering of operators, approvers, or responders will occur.
- [ ] Evidence collected will be handled at incident-evidence classification.
- [ ] An exercise that reveals an active compromise ends the engagement and moves to the overlay's response path.

Signed: ___________________  Date: ___________
