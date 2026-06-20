<!-- ────────────────────────────────────────────────────────────────── -->
<!--  Template — Agent Privilege Matrix                                  -->
<!--  Part of the AI IR Overlay™ framework — by Jacob Ideji              -->
<!--  https://jacobideji.com                                             -->
<!--  License: Apache 2.0  ·  See LICENSE file in this package           -->
<!-- ────────────────────────────────────────────────────────────────── -->

> **CSV mapping each agent's tools to Tier 0/1/2 with risk and reversibility.**
>
> *This is one self-contained piece of the AI IR Overlay™ framework.
> Get the rest at [jacobideji.com](https://jacobideji.com).*

---

# Agent Privilege Matrix

A spreadsheet-friendly CSV for tiering every tool an AI agent can call. The matrix makes **Kill-Switch Mode M3 (Tool Tiering)** actionable: when an incident hits, you can target containment instead of taking the agent fully offline.

## What this package contains

| File | Purpose |
|---|---|
| `agent-privilege-matrix.csv` | The template, pre-filled with worked examples for three agents |
| `LICENSE` | Apache 2.0 + trademark notice |
| `CITATION.cff` | Machine-readable citation metadata |

## The tier model

| Tier | Risk | Examples | Default control |
|---|---|---|---|
| **T0** | Read-only | Search KB, query records, retrieve status | Allowed by default |
| **T1** | Bounded writes | Draft (not send) email, update internal ticket fields, create tasks | Allowed + caps + allowlists |
| **T2** | Systems of record | Send external email, update CRM/ERP, deploy code, change cloud config, financial actions | Approvals required (or disabled until needed) |

## CSV columns

| Column | What it captures |
|---|---|
| `agent_name` | Which agent this tool belongs to |
| `tool_name` | Stable identifier (matches your tool registry) |
| `tool_category` | `saas_read`, `saas_write`, `communication`, `vcs_write`, `infra_write`, etc. |
| `risk_tier` | `T0`, `T1`, or `T2` |
| `read_write` | `read` or `write` (separates passive lookup from active change) |
| `scope` | Scope string (e.g., `mail.send`, `salesforce.write.opportunities`) |
| `write_targets` | The downstream system + object touched (e.g., `Salesforce.Opportunity`) |
| `allowlist` | Domain/tenant/repo restriction, or blank if unrestricted |
| `cap_per_run` | Maximum invocations per agent execution; `unlimited` for low-risk |
| `approval_required` | `yes` for T2 by default, `no` for T0/T1 |
| `reversible` | How a misstep is undone (`draft mode`, `revert log`, `staging`, etc.) |
| `notes` | Free-text caveats |

## How to use

### Quickstart

1. Open `agent-privilege-matrix.csv` in your spreadsheet tool or import into your tool-registry CI.
2. Replace the worked-example rows with your own agents and tools.
3. Default Tier-2 to `approval_required = yes`. Only relax for a specific cell when business need justifies it.

### Operational use during an incident

When **Kill-Switch Mode M3 (Tool Tiering)** is activated:

1. Filter the CSV to the affected agent's rows
2. Disable every `risk_tier = T2` tool first
3. Leave `T0` (read-only) and `T1` (bounded-writes) live so the business keeps running
4. Document which tools were disabled in the decision log

This converts containment from a binary "kill the agent" decision to a surgical one.

### Validation in CI

Add a CI check that asserts:

- No `risk_tier = T2` row has `approval_required = no`
- No `risk_tier = T2` row has empty `reversible`
- Every row has a non-empty `write_targets` if `read_write = write`

### Import to Sheets / Excel / Airtable

The CSV is plain UTF-8 with standard delimiters. Drop it into any spreadsheet tool. For Airtable, the columns map cleanly to single-line text + single-select fields.

## License

Apache 2.0. Free to use, fork, adapt, and ship in your products. The word mark **AI IR Overlay™** is protected. See `LICENSE` for terms.

## Related packages

- `kill-switches-modes`: the six containment modes. Mode 3 (Tool Tiering) uses this matrix.
- `template-ai-bom`: the per-agent inventory YAML that references these tools.
- `playbook-04`: "Tool Design Is Containment" (the playbook that introduces the tier model).

## Cite

```text
Ideji, J. (2026). Agent Privilege Matrix template. AI IR Overlay framework.
https://jacobideji.com
```
