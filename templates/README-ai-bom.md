<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Template — AI Bill of Materials (AI-BOM)                          -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji              -->
<!--  https://jacobideji.com                                             -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package           -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **Machine-readable inventory schema. One YAML file per AI agent.**
>
> *Part of the AI IR Overlay™ framework. See [CONTENT_MAP.md](../CONTENT_MAP.md) for the full repository map.*

---

# AI Bill of Materials (AI-BOM)

A YAML schema for describing every AI agent in production. **The AI-BOM is the inventory layer (MVO-1) of the [Minimum Viable Overlay](../framework/01-minimum-viable-overlay.md).** Without it, responders cannot scope an incident in real time.

## What this package contains

| File | Purpose |
|---|---|
| `ai-bom.yaml` | The schema, fully filled in with a worked example (`sales-triage-copilot`) |
| `LICENSE` | Apache 2.0 + trademark notice |
| `CITATION.cff` | Machine-readable citation metadata |

## What goes in an AI-BOM

The schema captures, **per agent**:

| Section | What it documents |
|---|---|
| `agent` | Name, business owner, technical owner, environment, deployment dates |
| `identity` | Service account, OAuth grant, scopes, rotation cadence |
| `model` | Provider, model ID, version pinning, fallback model |
| `tools` | Every enabled tool with risk tier (`T0`/`T1`/`T2`), read vs. write, write targets |
| `retrieval` | Each corpus, URI, sensitivity, refresh cadence |
| `memory` | Scope (off / per-user / shared), retention, sensitivity, PII handling |
| `guardrails` | Active policies (prompt-injection detection, PII redaction, rate limits) |
| `logging` | What's logged, retention windows |
| `kill_switches` | Implementation status + last-tested date for each mode M1 to M4 |
| `evidence_export` | Where the runbook lives, tested export time |
| `compliance_tags` | SOC 2, ISO/IEC 42001:2023, EU AI Act applicability |
| `incidents_history` | Tabletop and real incident log |

## How to use

### Quickstart

1. Copy `ai-bom.yaml` to your repo as one file per agent, e.g.:

   ```text
   .ai-bom/
     sales-triage-copilot.yaml
     support-copilot.yaml
     devops-agent.yaml
   ```

2. Replace the worked-example values with your agent's actual configuration.

3. Treat each file as **production configuration.** Version it, review it, and require an updated AI-BOM on every agent change.

### Operational requirement

The AI IR Overlay sets a hard target: **the AI-BOM must be exportable in under 5 minutes during an active incident.** A wiki page that takes 30 minutes to find is not an inventory.

### CI integration

Validate every AI-BOM file against the JSON Schema [`schemas/ai-bom.schema.json`](../schemas/ai-bom.schema.json) (JSON Schema 2020-12). The schema enforces the `T0`/`T1`/`T2` risk-tier vocabulary, the 10-minute Kill-Switch Mode TTA upper bound, the 60-minute Evidence Set export upper bound, the conditional rule that write tools must declare `write_targets`, and the **maturity-target-conditional kill-switch implementation rule** (Level 2 Containable and above requires all four kill-switch modes implemented=true).

The framework's reference validator at [`scripts/validate.py`](../scripts/validate.py) performs both schema validation and **operational-currency staleness checks**:

- `last_reviewed` field must be within 7 days for MVO-1 Inventory conformance
- `kill_switches.mX.tested_at` must be within 90 days for the claimed `maturity_target` (level_2_containable and above)

Staleness findings are reported as WARNINGs by default. Run with `--strict` to escalate them to errors (exit code 1) for CI enforcement.

Any JSON Schema validator (`ajv`, `jsonschema`, `check-jsonschema`) validates YAML inputs after a YAML-to-JSON conversion step. The framework's [`scripts/validate.py`](../scripts/validate.py) (Python 3.10+, jsonschema, pyyaml) is the reference implementation.

### Maturity-level progression

The `kill_switches.maturity_target` field controls which Kill-Switch Modes must be implemented:

| `maturity_target` | Kill-switch implementation requirement | Use when |
|---|---|---|
| `level_1_aware` | Modes may have `implemented: false` and null `tested_at` / `tta_minutes` | Initial adoption; only the AI-BOM inventory is required at this level. |
| `level_2_containable` | All four modes (M1-M4) must have `implemented: true` and `tested_at` within 90 days | Production-ready customers who have tabletop-tested kill-switch activation per [Playbook 14](../playbooks/14-testing-for-agent-failure-modes.md). |
| `level_3_provable` | Level 2 + 60-minute Evidence Set export tested within 90 days | Customers who have completed the [Reconstructability Test](../playbooks/15-records-retention.md) at the framework's measurement standard. |
| `level_4_resilient` | Level 3 + measured Six Metrics trending over rolling 90 days | Customers operating the framework's [Six Metrics](../playbooks/13-six-metrics.md) discipline. |

The framework's discipline is **honest self-assessment**: customers below Level 2 should declare `level_1_aware` explicitly rather than leave the field blank or claim Level 2 conformance they cannot defend. See [`framework/03-maturity-roadmap.md`](../framework/03-maturity-roadmap.md) for the full level definitions.

### Default behavior when `maturity_target` is omitted

The framework's discipline is **deliberate opt-in**, not silent permissiveness. However, real-world adoption sometimes lands AI-BOM files in the customer's environment without the `maturity_target` field set (legacy AI-BOMs predating the v0.26.0 schema; copy-paste errors; partial migration from earlier framework versions). The framework's `kill_switches` schema requires the `maturity_target` field per the v0.26.0 enforcement (see the `kill_switches.maturity_target` property in [`schemas/ai-bom.schema.json`](../schemas/ai-bom.schema.json)), so a file missing the field **fails schema validation** rather than silently defaulting.

If the field is missing, the validator's error message names the field explicitly: `"'maturity_target' is a required property"`. The customer's CI integration catches this at validation time, not at incident time.

**Adopter recommendation:** when starting AI-BOM adoption, set `maturity_target: "level_1_aware"` explicitly in every AI-BOM, even when the customer's actual operating posture is below Level 1 (no inventory yet). The explicit declaration signals to subsequent reviewers (auditors, regulators, internal governance) that the customer's posture is intentional rather than aspirational. As the customer's posture matures, the field's value is bumped to `level_2_containable`, then `level_3_provable`, then `level_4_resilient` per the [Maturity Roadmap](../framework/03-maturity-roadmap.md).

**No default is provided** because the framework's position is that maturity claims must be explicit and defensible. A blank field that silently defaults would create the kind of false confidence the framework's discipline is designed to prevent.

### Mapping to other inventories

If you maintain a CMDB or SBOM:

| Their term | AI-BOM equivalent |
|---|---|
| Service | `agent.name` |
| Owner | `agent.business_owner` + `agent.technical_owner` |
| Component | each entry in `tools[]`, `retrieval.corpora[]` |
| Dependency | `model.provider` + `model.model_id` |

## License

Apache 2.0. Free to use, fork, adapt, and ship in your products. The word mark **AI IR Overlay™** is protected. See `LICENSE` for terms.

## Related

- [`framework/01-minimum-viable-overlay.md`](../framework/01-minimum-viable-overlay.md): describes the four MVO controls. Inventory is the first.
- [`schemas/ai-bom.schema.json`](../schemas/ai-bom.schema.json): the JSON Schema 2020-12 contract for CI validation, including the conditional rule that write tools must declare `write_targets`.
- [`templates/agent-privilege-matrix.csv`](agent-privilege-matrix.csv) ([README](README-privilege-matrix.md)): the companion CSV mapping tools to risk tiers.
- [`kill-switches/overview.md`](../kill-switches/overview.md): the six modes referenced by the `kill_switches` section.
- [Playbook 01: The Agent Is a Privileged Identity](../playbooks/01-agent-as-privileged-identity.md): the response playbook that uses the inventory.

## Cite

```text
Ideji, J. (2026). AI Bill of Materials (AI-BOM) template. AI IR Overlay framework.
https://jacobideji.com
```
