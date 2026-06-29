<!-- ────────────────────────────────────────────────────────────────── -->
<!--  AI IR Overlay — Quickstart                                        -->
<!--  Part of the AI IR Overlay™ framework, by Jacob Ideji              -->
<!--  https://jacobideji.com                                            -->
<!--  License: Apache 2.0. See LICENSE file in this package.            -->
<!-- ────────────────────────────────────────────────────────────────── -->

# Quickstart: Adopt the AI IR Overlay in 30 days

> *A 30-day adoption path for one production AI agent. Each day's work fits in one hour. Day 30 produces a defensible Level 2 (Containable) maturity claim per [framework/03-maturity-roadmap.md](framework/03-maturity-roadmap.md).*

This quickstart is the operational entry point to the framework. It assumes you are a security engineer or CISO with one production AI agent that has tool access. You have not yet adopted the framework. You are reading this on Monday morning. Each step is concrete enough that you can run it.

For the conceptual reading order, see [README.md](README.md#reading-order). For the per-newsletter mapping, see [CONTENT_MAP.md](CONTENT_MAP.md).

## Pick the right agent first

This 30-day path is calibrated for **one agent**. Pick the agent whose blast radius would be highest if it misbehaved. The right candidate has at least one of:

- Tool-call access to systems of record (CRM, ERP, identity provider, code repo, cloud control plane)
- Ability to send external-facing communication (email, ticketing, chat to customers or partners)
- Memory enabled across users or sessions
- Retrieval against any corpus that contains regulated data, customer data, or pricing data

If you have a fleet of agents, run this path on the highest-impact agent first. Repeat for the next agent only after Day 30 closes on the first.

## Day 1: Build the AI-BOM

**Goal:** produce one AI Bill of Materials YAML file per agent in production.

**What to do (60 minutes):**

1. Copy [`templates/ai-bom.yaml`](templates/ai-bom.yaml) to your repo as `.ai-bom/<agent-name>.yaml`.
2. Replace every worked-example value with your agent's actual configuration. Pay close attention to:
   - `identity.principal` (the actual service account or OAuth grant)
   - `identity.scopes` (what your IdP says, not what the agent's prompt claims)
   - `tools[]` (every tool, including ones the prompt restricts but the wrapper still exposes)
   - `tools[].write_targets` (every downstream system the tool can affect)
   - `memory.scope` and `memory.retention_days`
3. Run [`scripts/validate.py`](scripts/validate.py) to confirm the file conforms to [`schemas/ai-bom.schema.json`](schemas/ai-bom.schema.json).

**Done when:** the validator returns `OK` on your agent's AI-BOM. You now have MVO-1 (Inventory) for this agent.

**Conformance link:** see [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md) Control 1.

## Day 7: Tier the agent's tools

**Goal:** produce the Agent Privilege Matrix CSV row-by-row for this agent.

**What to do (60 minutes):**

1. Copy [`templates/agent-privilege-matrix.csv`](templates/agent-privilege-matrix.csv) as `.ai-bom/<agent-name>-privileges.csv`.
2. Enumerate every tool from the AI-BOM as a row. For each:
   - Assign `risk_tier` as `T0` (read-only or low risk), `T1` (bounded writes), or `T2` (systems of record). If you cannot decide between T1 and T2, default to T2 per [Playbook 04](playbooks/04-tool-design-is-containment.md).
   - Set `approval_required = yes` on every T2 row (CI rule).
   - Set `reversible` to a real undo mechanism for every T2 row (CI rule); `n/a` is not acceptable.
   - Set `write_targets` to a non-empty string on every write row (CI rule).
3. Run [`scripts/validate.py`](scripts/validate.py) on the CSV to confirm conformance to [`schemas/privilege-matrix.schema.json`](schemas/privilege-matrix.schema.json).

**Done when:** the validator returns `OK` on the CSV. You can now execute Kill-Switch Mode M3 (Tool Tiering) by filtering this CSV.

**Conformance link:** [`framework/01-minimum-viable-overlay.md`](framework/01-minimum-viable-overlay.md) Control 1; [Playbook 04](playbooks/04-tool-design-is-containment.md).

## Day 14: Tabletop M1 through M4

**Goal:** activate Kill-Switch Modes M1, M2, M3, M4 in a tabletop and prove each is implementable.

**What to do (60 minutes):**

1. Pull up [`kill-switches/overview.md`](kill-switches/overview.md) and read the M0-M5 ladder + Mode Variants table.
2. Walk a synthetic scenario. The agent's most-dangerous tool (from the Day 7 matrix) just executed an unauthorized action. Walk:
   - **Activate M1 (Read-Only).** Confirm the agent's write tools are unreachable in production. Capture timing.
   - **Activate M2 (Approvals Required).** Confirm the approval queue routes correctly. Capture timing.
   - **Activate M3 (Tool Tiering).** Disable every T2 row from the Day 7 matrix. Confirm T0 and T1 still function. Capture timing.
   - **Activate M4 (Full Disable).** Confirm the agent is offline AND that you snapshotted identity scopes BEFORE token rotation. Capture timing.
3. Record each Time-to-Activate (TTA) value in the AI-BOM `kill_switches.mX.tta_minutes` field.

**Done when:** all four TTA values are below 10 minutes (the framework's drill-measured target per [`framework/01`](framework/01-minimum-viable-overlay.md#measurement-scope)). If any exceeds 10 minutes, that mode is a hardening item for the next cycle.

**Conformance link:** [`kill-switches/overview.md`](kill-switches/overview.md); [Playbook 14](playbooks/14-testing-for-agent-failure-modes.md).

## Day 21: Drill the 60-minute evidence export

**Goal:** prove the Minimum Evidence Set (Types A through F) is exportable within 60 minutes.

**What to do (60 minutes):**

1. Read [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md) and [`schemas/evidence-export.spec.md`](schemas/evidence-export.spec.md).
2. Pick a 1-hour window from the past 24 hours. Treat that window as the incident window.
3. Export each Type:
   - **A:** Prompt/response logs from your model provider or API gateway (note: provider TTLs are often 24-72 hours; this is why the drill exists).
   - **B:** Tool-call ledger from application middleware. Include attempted-but-denied calls.
   - **C:** Retrieval traces (document IDs, chunks, similarity scores) from your RAG/KB framework.
   - **D:** Memory snapshot (if memory is enabled per the AI-BOM).
   - **E:** Configuration snapshot (system prompt version, tool definitions, retriever settings).
   - **F:** Identity and SaaS audit-log correlation (IdP logs + downstream SaaS audit logs).
4. Time the full export end-to-end. Record `evidence_export.tested_export_minutes` in the AI-BOM.

**Done when:** all six Types exported in under 60 minutes. If any Type's data is unrecoverable (e.g., model-provider TTL already expired), that gap is a hardening item.

**Conformance link:** [`evidence/minimum-evidence-set.md`](evidence/minimum-evidence-set.md); [Playbook 13 Metric 3](playbooks/13-six-metrics.md).

## Day 30: Claim Level 2 (Containable) maturity

**Goal:** produce a defensible Level 2 (Containable) claim for this agent.

**What to do (30 minutes):**

1. Open [`framework/03-maturity-roadmap.md`](framework/03-maturity-roadmap.md) and confirm the Level 2 criteria:
   - MVO-1 Inventory exists and is current within 7 days ✓ (Day 1)
   - MVO-2 Safe Modes M1-M4 are implemented and tabletop-tested within the last 90 days ✓ (Day 14)
2. If your evidence export drill (Day 21) also passed, you have a Level 3 (Provable) claim for this agent. Note that in the AI-BOM `incidents_history` block as a `tabletop` entry.
3. Document the claim in your audit-trail wherever your organization tracks security posture (CMDB, GRC tool, board-ready scorecard per [Playbook 24](playbooks/24-board-ready-scorecard.md)).

**Done when:** the agent has a documented Level 2 (or Level 3) maturity claim, dated within the last 90 days, with evidence attached.

## After Day 30

Pick the next-highest-blast-radius agent. Run this 30-day path on that agent. Repeat until every production AI agent has at least a Level 2 maturity claim.

For ongoing operations:

- **Quarterly:** re-run Day 14 tabletops to keep the 90-day rolling window valid.
- **Quarterly:** re-run Day 21 evidence drills.
- **Per agent change:** update the AI-BOM and re-run [`scripts/validate.py`](scripts/validate.py). The [GitHub Action](.github/workflows/validate-templates.yml) runs this automatically on every PR if you keep the AI-BOMs in your repo.
- **Per incident:** activate the appropriate playbook from the [reading-order index](README.md#reading-order). [Playbook 01](playbooks/01-agent-as-privileged-identity.md) is the keystone for any agent-class incident.

## When you hit a wall

This 30-day path assumes the framework's controls map cleanly onto your agent platform. Some platforms (especially vendor copilots; see [Playbook 10](playbooks/10-vendor-copilots.md)) don't expose every control surface the framework assumes. When you hit a gap:

- File an [Issue](https://github.com/jacobideji/aiiroverlay/issues) describing what didn't map.
- Or open a [Discussion](https://github.com/jacobideji/aiiroverlay/discussions) for a longer-form conversation.

The framework gets better when adopters surface these gaps.

## Worked example

For a full end-to-end walkthrough of an incident response using this framework, see [`examples/incident-walkthrough.md`](examples/incident-walkthrough.md).

---

*Source: AI IR Overlay framework, by Jacob Ideji.*
<https://www.linkedin.com/in/jacobideji/>
