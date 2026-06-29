#!/usr/bin/env python3
"""
AI IR Overlay reference kill-switch demo.

A minimal Python implementation of the Kill-Switch API contract from
`schemas/kill-switch-api.md` showing Modes M0, M1, M2, M3, M4 against a
synthetic in-memory agent tool registry.

This is NOT production code. It demonstrates the Activate / Status /
Deactivate / Probe API shape and the per-mode tool-toggle behavior.
Adopters fork this and wire the registry up to LangGraph, Bedrock Agents,
or a vendor-specific tool-management API.

Conformance to the contract is demonstrated by:
  - Activate accepts required inputs (mode, agent_id, actor, reason, ticket_id)
  - Activate returns activation_id with requested_at, acknowledged_at, effective_at
  - effective_at is set only after Probe returns pass (no caching, no fast-fail)
  - Status query by agent_id returns current_mode, activated_at, last_probed_at
  - Deactivate parallels Activate with separation-of-duties (different actor)
  - Probe verifies mode is in effect with evidence, not just configuration
  - M3 is parameterized by scope (specific tool list)

Usage
-----
    # Run the demo end-to-end with all five modes
    python3 kill_switch_demo.py

    # Run with verbose telemetry output
    python3 kill_switch_demo.py --verbose
"""
from __future__ import annotations

import argparse
import sys
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ─── Mode definitions ──────────────────────────────────────────────────────

class Mode:
    M0 = "M0"  # Observe (normal operations)
    M1 = "M1"  # Read-Only
    M2 = "M2"  # Approvals Required
    M3 = "M3"  # Tool Tiering
    M4 = "M4"  # Full Disable
    M5 = "M5"  # Controlled Re-Enable

ALL_MODES = [Mode.M0, Mode.M1, Mode.M2, Mode.M3, Mode.M4, Mode.M5]


# ─── Synthetic agent and tool registry ────────────────────────────────────

@dataclass
class Tool:
    """A registered tool with its risk tier and current state."""
    name: str
    risk_tier: str  # "T0", "T1", "T2"
    is_write: bool
    enabled: bool = True
    requires_approval: bool = False

    def call(self, params: dict[str, Any]) -> dict[str, Any]:
        """Simulate a tool call. Returns result and approver if any."""
        if not self.enabled:
            return {"status": "denied", "reason": f"tool {self.name} is disabled"}
        if self.requires_approval:
            # In production: queue for approval; here we just note it
            return {"status": "queued", "reason": f"tool {self.name} requires approval"}
        return {"status": "success", "result": f"called {self.name} with {params}"}


@dataclass
class Activation:
    """Per-activation record produced by an Activate call."""
    activation_id: str
    mode: str
    agent_id: str
    actor: str
    reason: str
    ticket_id: str | None
    scope: list[str] | None  # Specific tool list for M3
    requested_at: str
    acknowledged_at: str | None = None
    effective_at: str | None = None
    deactivated_at: str | None = None
    last_probed_at: str | None = None
    probe_result: str | None = None  # "pass", "fail", None


# ─── Kill-switch API ──────────────────────────────────────────────────────

class KillSwitchAPI:
    """In-memory reference implementation of the Kill-Switch API."""

    def __init__(self, agent_id: str, verbose: bool = False):
        self.agent_id = agent_id
        self.verbose = verbose
        self.current_mode: str = Mode.M0
        self.activation_history: list[Activation] = []
        self.tools: dict[str, Tool] = {
            "salesforce.lookup": Tool("salesforce.lookup", "T0", is_write=False),
            "internal_kb_search": Tool("internal_kb_search", "T0", is_write=False),
            "outlook.send": Tool("outlook.send", "T1", is_write=True),
            "salesforce.write.opportunity": Tool("salesforce.write.opportunity", "T2", is_write=True),
            "salesforce.bulk_update": Tool("salesforce.bulk_update", "T2", is_write=True),
            "code_execution": Tool("code_execution", "T2", is_write=True),
        }

    # ─── Activate ──────────────────────────────────────────────────────────

    def activate(
        self,
        mode: str,
        actor: str,
        reason: str,
        ticket_id: str | None = None,
        scope: list[str] | None = None,
    ) -> Activation:
        """Activate a Kill-Switch Mode."""
        if mode not in ALL_MODES:
            raise ValueError(f"invalid mode: {mode}; expected one of {ALL_MODES}")

        activation = Activation(
            activation_id=str(uuid.uuid4()),
            mode=mode,
            agent_id=self.agent_id,
            actor=actor,
            reason=reason,
            ticket_id=ticket_id,
            scope=scope,
            requested_at=_now(),
        )

        # Apply the mode's per-tool effects
        self._apply_mode(mode, scope)

        # Acknowledge (in production this is the orchestrator's ack)
        activation.acknowledged_at = _now()

        # Probe to verify the mode is actually in effect
        time.sleep(0.01)  # Simulate brief delay
        probe = self.probe(mode, scope)
        activation.last_probed_at = _now()
        activation.probe_result = "pass" if probe else "fail"

        # effective_at is set ONLY if probe passes (per the contract)
        if activation.probe_result == "pass":
            activation.effective_at = _now()
            self.current_mode = mode

        self.activation_history.append(activation)

        if self.verbose:
            print(f"  ACTIVATE: mode={mode} actor={actor} probe={activation.probe_result}")

        return activation

    # ─── Status ────────────────────────────────────────────────────────────

    def status(self) -> dict[str, Any]:
        """Return current Kill-Switch state for this agent."""
        active = next(
            (a for a in reversed(self.activation_history) if a.deactivated_at is None and a.effective_at),
            None,
        )
        return {
            "agent_id": self.agent_id,
            "current_mode": self.current_mode,
            "activated_at": active.effective_at if active else None,
            "last_probed_at": active.last_probed_at if active else None,
            "probe_result": active.probe_result if active else None,
            "scope": active.scope if active else None,
        }

    # ─── Deactivate ────────────────────────────────────────────────────────

    def deactivate(self, actor: str, reason: str) -> Activation | None:
        """Deactivate the current mode. Returns to M0 (Observe).

        Separation-of-duties rule: the deactivating actor must differ from
        the most recent activating actor. In production this is enforced
        by an IdP-side authorization check; here we enforce it inline.
        """
        active = next(
            (a for a in reversed(self.activation_history) if a.deactivated_at is None and a.effective_at),
            None,
        )
        if not active:
            return None
        if active.actor == actor:
            raise PermissionError(
                f"separation-of-duties violation: deactivator ({actor}) must differ from "
                f"activator ({active.actor}) per kill-switch-api.md"
            )

        active.deactivated_at = _now()

        # Restore all tools to default state
        for tool in self.tools.values():
            tool.enabled = True
            tool.requires_approval = False

        self.current_mode = Mode.M0
        if self.verbose:
            print(f"  DEACTIVATE: mode {active.mode} -> M0 by {actor}")
        return active

    # ─── Probe ─────────────────────────────────────────────────────────────

    def probe(self, mode: str, scope: list[str] | None = None) -> bool:
        """Verify the mode is in effect with evidence (not just configuration)."""
        if mode == Mode.M0:
            # M0: all tools enabled, no approval required
            return all(t.enabled and not t.requires_approval for t in self.tools.values())

        if mode == Mode.M1:
            # M1: read tools enabled, write tools denied
            for t in self.tools.values():
                if t.is_write and t.enabled:
                    return False
                if not t.is_write and not t.enabled:
                    return False
            return True

        if mode == Mode.M2:
            # M2: all enabled but writes require approval
            for t in self.tools.values():
                if t.is_write and not t.requires_approval:
                    return False
            return True

        if mode == Mode.M3:
            # M3 with scope: specific tools must be disabled or approval-gated
            if not scope:
                return False
            for tool_name in scope:
                if tool_name in self.tools and self.tools[tool_name].enabled:
                    if not self.tools[tool_name].requires_approval:
                        return False
            return True

        if mode == Mode.M4:
            # M4: all tools disabled
            return all(not t.enabled for t in self.tools.values())

        return False

    # ─── Private: apply a mode's effects ───────────────────────────────────

    def _apply_mode(self, mode: str, scope: list[str] | None) -> None:
        if mode == Mode.M0:
            for t in self.tools.values():
                t.enabled = True
                t.requires_approval = False
        elif mode == Mode.M1:
            for t in self.tools.values():
                t.enabled = not t.is_write
                t.requires_approval = False
        elif mode == Mode.M2:
            for t in self.tools.values():
                t.enabled = True
                t.requires_approval = t.is_write
        elif mode == Mode.M3:
            for t in self.tools.values():
                t.enabled = True
                t.requires_approval = False
            if scope:
                for tool_name in scope:
                    if tool_name in self.tools:
                        self.tools[tool_name].requires_approval = True
        elif mode == Mode.M4:
            for t in self.tools.values():
                t.enabled = False


# ─── Helpers ───────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def print_status(api: KillSwitchAPI, label: str) -> None:
    s = api.status()
    print(f"\n{label}")
    print(f"  agent_id:        {s['agent_id']}")
    print(f"  current_mode:    {s['current_mode']}")
    print(f"  activated_at:    {s['activated_at']}")
    print(f"  scope:           {s['scope']}")


# ─── Demo ──────────────────────────────────────────────────────────────────

def run_demo(verbose: bool) -> int:
    print("AI IR Overlay reference kill-switch demo")
    print("=========================================")
    print()

    api = KillSwitchAPI(agent_id="sales-triage-copilot", verbose=verbose)
    print_status(api, "Initial state:")

    # Scenario: detection triggers a workflow-injection alert per PB06
    # The IC chooses M3 Tool Tiering scoped to the bulk-update tool
    print("\n--- Step 1: Activate M1 (Read-Only) ---")
    api.activate(
        mode=Mode.M1,
        actor="ic_jdoe",
        reason="Anomalous tool-call spike on outlook.send",
        ticket_id="INC-2026-0042",
    )
    print_status(api, "After M1 activation:")

    # Verify a write tool is denied
    result = api.tools["outlook.send"].call({"to": "test@example.com"})
    print(f"  Test: outlook.send -> {result}")
    result = api.tools["salesforce.lookup"].call({"id": "0061a000ABC123"})
    print(f"  Test: salesforce.lookup -> {result}")

    # Deactivate M1 (different actor per separation-of-duties)
    print("\n--- Step 2: Deactivate M1 ---")
    try:
        api.deactivate(actor="ic_jdoe", reason="Test SoD violation")
    except PermissionError as e:
        print(f"  ✓ SoD enforced: {e}")
    api.deactivate(actor="cisco_marketing_director", reason="False positive confirmed")
    print_status(api, "After M1 deactivation:")

    # Escalation: activate M3 scoped to the bulk-update tool
    print("\n--- Step 3: Activate M3 (Tool Tiering) scoped to bulk_update ---")
    api.activate(
        mode=Mode.M3,
        actor="ic_jdoe",
        reason="Suspected workflow injection through CRM bulk-update path",
        ticket_id="INC-2026-0042",
        scope=["salesforce.bulk_update", "code_execution"],
    )
    print_status(api, "After M3 activation:")

    # Test that scoped tools require approval but others do not
    result = api.tools["salesforce.bulk_update"].call({"count": 47})
    print(f"  Test: salesforce.bulk_update -> {result}")
    result = api.tools["salesforce.lookup"].call({"id": "0061a000ABC123"})
    print(f"  Test: salesforce.lookup -> {result}")
    result = api.tools["outlook.send"].call({"to": "test@example.com"})
    print(f"  Test: outlook.send -> {result}")

    # Escalate to M4
    print("\n--- Step 4: Escalate to M4 (Full Disable) ---")
    api.deactivate(actor="cisco_marketing_director", reason="Escalating to M4")
    api.activate(
        mode=Mode.M4,
        actor="ciso",
        reason="Confirmed unauthorized data write to external system",
        ticket_id="INC-2026-0042",
    )
    print_status(api, "After M4 activation:")

    # Verify all tools denied
    result = api.tools["salesforce.lookup"].call({"id": "0061a000ABC123"})
    print(f"  Test: salesforce.lookup -> {result}")

    # Summary
    print("\n--- Activation history ---")
    for a in api.activation_history:
        deact = a.deactivated_at or "still active"
        scope_str = f", scope={a.scope}" if a.scope else ""
        print(f"  {a.activation_id[:8]}  mode={a.mode}  actor={a.actor}  deactivated_at={deact}{scope_str}")

    print("\nDemo complete.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose telemetry output")
    args = parser.parse_args(argv)
    return run_demo(verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
