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
| `tools` | Every enabled tool with risk tier (0/1/2), read vs. write, write targets |
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

Add a CI step that:

- Parses every `*.yaml` in your AI-BOM directory
- Fails the build if any required field is missing or stale (older than 7 days for `last_reviewed`)
- Asserts that each `kill_switches.mX.tested_at` is within the last 90 days

The schema is intentionally flat enough to validate with `yq` or any YAML schema validator.

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
- [`templates/agent-privilege-matrix.csv`](agent-privilege-matrix.csv) ([README](README-privilege-matrix.md)): the companion CSV mapping tools to risk tiers.
- [`kill-switches/overview.md`](../kill-switches/overview.md): the six modes referenced by the `kill_switches` section.
- [Playbook 01: The Agent Is a Privileged Identity](../playbooks/01-agent-as-privileged-identity.md): the response playbook that uses the inventory.

## Cite

```text
Ideji, J. (2026). AI Bill of Materials (AI-BOM) template. AI IR Overlay framework.
https://jacobideji.com
```
