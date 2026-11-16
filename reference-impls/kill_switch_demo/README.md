# Kill-Switch Demo — Reference Implementation

A minimal Python implementation of the [Kill-Switch API contract](../../schemas/kill-switch-api.md) showing Modes M0 through M5 against a synthetic in-memory agent tool registry.

## Run the demo

```bash
cd reference-impls/kill_switch_demo
python3 kill_switch_demo.py

# or with verbose output:
python3 kill_switch_demo.py --verbose
```

Expected demonstration:
1. Initial state in M0 (Observe)
2. Activate M1 (Read-Only); test that writes are denied and reads pass
3. Demonstrate separation-of-duties on deactivation (same actor blocked)
4. Activate M3 (Tool Tiering) scoped to specific tools; test that scoped tools are disabled while unscoped tools keep working. (Approval-gating is M2 semantics; M3 disables.)
5. Escalate to M4 (Full Disable); test that all tools are denied
6. Demonstrate M5 (Controlled Re-Enable): direct M4 to M0 refused, M5 activated read-only, premature return refused on an incomplete gate, insufficient approver authority refused, then the gated return to M0
7. Demonstrate M2 (Approvals Required) with a working approver: a held call, agent self-approval refused, an approver denial that does not execute, an approver release that does, and queue metrics
8. Print the configuration evidence: registry snapshots that reconstruct what was callable at a past moment
9. Print the tool-call evidence: every invocation recorded with its outcome, mode and activation link
10. Print full activation history

## File layout

```
kill_switch_demo/
├── README.md                  (this file)
└── kill_switch_demo.py        (the demo script)
```

## What this demonstrates

| Contract element | Where in the code |
|---|---|
| Activate API with required inputs (mode, agent_id, actor, reason, ticket_id, optional scope) | `KillSwitchAPI.activate()` |
| Activate output (activation_id, requested_at, acknowledged_at, effective_at) | `Activation` dataclass |
| `effective_at` set ONLY after probe returns pass | `KillSwitchAPI.activate()` line near end |
| Status API returns current_mode, activated_at, last_probed_at, probe_result | `KillSwitchAPI.status()` |
| Deactivate API with separation-of-duties enforcement | `KillSwitchAPI.deactivate()` |
| Probe API verifies mode is in effect with evidence | `KillSwitchAPI.probe()` |
| Per-mode effects: M1 (read-only), M2 (approvals), M3 (scoped tiering), M4 (full disable), M5 (staged read-only) | `KillSwitchAPI._apply_mode()` |
| M3 scope parameter (specific tool list), rejected at activate() if empty or unresolvable | `KillSwitchAPI.activate()`, `_apply_mode()` M3 branch |
| Activation is atomic: the registry is rolled back when the probe does not pass | `KillSwitchAPI.activate()` |
| M5 staged recovery gate, steps 1-5 of `kill-switches/overview.md` | `ReEnableGate` |
| M5 step 6 enforced: gate complete AND approver holds CISO/IC authority | `KillSwitchAPI.deactivate()` |
| M4 exit criteria: no direct return to M0, must route through M5 | `KillSwitchAPI.deactivate()` |
| Tool-call evidence: record opened before dispatch, outcome written back | `ToolCall`, `Tool.call()`, `KillSwitchAPI._open_tool_call()` |
| Denials and queued calls recorded, not only successes | `KillSwitchAPI.tool_calls(outcome=...)` |
| M2 approvals actionable: one decision per held call, no bulk approve | `KillSwitchAPI.approve()` / `deny()` |
| Approver has authority to deny, and the agent cannot approve itself | `KillSwitchAPI._decide()` |
| Per-item approval audit and queue metrics | `ToolCall.decision*`, `KillSwitchAPI.approval_metrics()` |
| Configuration state versioned; past registry reconstructable | `ConfigSnapshot`, `KillSwitchAPI.configuration_at()` |

## Adapting for production

The demo is structured so adopters can fork and wire it up to real agent runtimes:

| Demo component | Replace with |
|---|---|
| `KillSwitchAPI.tools` (in-memory dict) | LangGraph tool registry, Bedrock Agents action group, vendor copilot tool-management API |
| `_apply_mode()` per-mode logic | Vendor-specific tool-toggle calls (LangGraph runtime reconfiguration, Bedrock UpdateAgent, Copilot Studio policy change) |
| `Activation` history (in-memory list) | Database-backed audit table; entries are evidence per PB07 + PB15 |
| `approval_queue` (in-memory dict) | A real approval workflow with notification, timeout and escalation. A queue nobody is paged for is unstaffed, which M2's operational checks forbid |
| `configuration_history` (in-memory list) | Versioned configuration store. These are the configuration-state records of the Minimum Evidence Set |
| `tool_call_history` (in-memory list) | SIEM or audit pipeline. These are the tool-call records of the Minimum Evidence Set; without them a containment verdict cannot be evidenced from the system's own logs |
| `_now()` timestamp helper | Use the customer's authoritative time source if your environment has clock-skew sensitivity |
| Separation-of-duties check | Replace inline `if active.actor == actor` with IdP-side authorization (Okta workflows, Azure PIM) |

The probe discipline (verifying with evidence, not just configuration) is the contract element that requires the most care. In production, M1's probe should attempt a write through the agent and verify denial; the demo's in-memory check is illustrative but not equivalent.

## What this does NOT demonstrate

- M3 variants (M3-RAG, M3-Workflow, M3-Output, M3-Vendor, M3-Delegation Cap, M3-Drift); the demo shows the canonical M3 only. The variants are documented in [`kill-switches/overview.md`](../../kill-switches/overview.md) and each requires a vendor-specific implementation (corpus disablement for M3-RAG, content-channel pause for M3-Workflow, etc.)
- M5 (Controlled Re-Enable); the demo's `deactivate()` returns to M0 directly. Real M5 implementation is multi-step per the [MVO-4 Controlled Re-Enable](../../framework/01-minimum-viable-overlay.md#4-controlled-re-enable-staged-validated-recovery) discipline
- Persistence across restarts; the demo state is in-memory
- Approval workflow integration; M2's "requires_approval" flag is a marker, not a real approval queue

## Dependencies

Python 3.10+ standard library only.

## License

Apache 2.0. See `../../LICENSE`.
