#!/usr/bin/env python3
"""
AI IR Overlay reference kill-switch demo.

A minimal Python implementation of the Kill-Switch API contract from
`schemas/kill-switch-api.md` showing Modes M0 through M5 against a
synthetic in-memory agent tool registry.

This is NOT production code. It demonstrates the Activate / Status /
Deactivate / Probe API shape and the per-mode tool-toggle behavior.
Adopters fork this and wire the registry up to LangGraph, Bedrock Agents,
or a vendor-specific tool-management API.

Conformance to the contract is demonstrated by:
  - Activate accepts required inputs (mode, actor, reason, ticket_id); the
  - Activate accepts (mode, actor, reason, ticket_id); agent_id is bound at init.
  - Activate returns activation_id with requested_at, acknowledged_at, effective_at
  - effective_at is set only after Probe returns pass (no caching, no fast-fail)
  - Status query by agent_id returns current_mode, activated_at, last_probed_at
  - Deactivate parallels Activate with separation-of-duties (different actor)
  - Probe verifies mode is in effect with evidence, not just configuration
  - M3 is parameterized by scope (specific tool list)

Usage
-----
    # Run the demo end-to-end with all six modes
    python3 kill_switch_demo.py

    # Run with verbose telemetry output
    python3 kill_switch_demo.py --verbose
"""
from __future__ import annotations

import argparse
import sys
import time
import uuid
from collections.abc import Callable
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

# M5 approver: "CISO or designated Incident Commander. Never the original agent
# owner alone." Independence alone is not sufficient; authority is also required.
APPROVER_ROLES = {"ciso", "incident_commander"}


# ─── Synthetic agent and tool registry ────────────────────────────────────

@dataclass
class ConfigSnapshot:
    """The effective tool registry at a moment in time, and what moved it.

    Mode and scope say what was *requested*. They do not say which tools were
    actually callable afterwards, which is the question an investigation asks:
    "what could this agent do at 02:14?" Reconstructing that from mode alone
    requires assuming the apply logic was correct, which is the thing under
    investigation.
    """
    taken_at: str
    cause: str                       # activation | rollback | deactivation
    mode: str
    activation_id: str | None
    tools: dict[str, dict[str, bool]]  # name -> {enabled, requires_approval}


@dataclass
class PendingApproval:
    """A tool call held at M2 awaiting a human decision."""
    approval_id: str
    tool: str
    params: dict[str, Any]
    correlation_id: str | None
    requested_at: str
    call_id: str


@dataclass
class ToolCall:
    """Evidence record for one tool invocation.

    Opened at the invocation boundary *before* dispatch, with the outcome
    written back afterwards. That ordering is the point: a log emitted from the
    success path records only the calls that did not need recording, and the
    denials, queued calls and retries - the sequence that matters during
    containment - leave no trace. It also means a call that dies mid-dispatch
    still leaves a record, with `outcome` unset.

    `activation_id` links the call to the containment decision in force when it
    was made, which is what lets a responder answer "was this denied because we
    contained the agent, or did it fail for some other reason?".
    """
    call_id: str
    tool: str
    params: dict[str, Any]
    agent_id: str
    mode: str
    activation_id: str | None
    correlation_id: str | None
    called_at: str
    outcome: str | None = None   # success | queued | denied; None if dispatch died
    reason: str | None = None
    approval_id: str | None = None      # set when the call is queued at M2
    decision: str | None = None         # approved | denied
    decided_by: str | None = None
    decided_at: str | None = None
    decision_reason: str | None = None
    approved_by: str | None = None      # set on the execution that an approval released


@dataclass
class Tool:
    """A registered tool with its risk tier and current state."""
    name: str
    risk_tier: str  # "T0", "T1", "T2"
    is_write: bool
    enabled: bool = True
    requires_approval: bool = False
    # Set by KillSwitchAPI when it builds the registry. Recording lives here,
    # not in a wrapper method, so that an existing call site cannot bypass it by
    # forgetting to use the new entry point.
    recorder: Callable[..., "ToolCall"] | None = field(
        default=None, repr=False, compare=False
    )
    pending_handler: Callable[..., str] | None = field(
        default=None, repr=False, compare=False
    )

    def call(
        self,
        params: dict[str, Any],
        correlation_id: str | None = None,
        approved_by: str | None = None,
    ) -> dict[str, Any]:
        """Simulate a tool call. Returns result and approver if any.

        `approved_by` is set only by KillSwitchAPI.approve(), which releases a
        call an approver has cleared. It bypasses the approval gate and nothing
        else: a disabled tool stays denied, because an approver may release a
        queued call but may not un-contain a tool.
        """
        record = self.recorder(self, params, correlation_id) if self.recorder else None
        if record is not None and approved_by:
            record.approved_by = approved_by

        if not self.enabled:
            result = {"status": "denied", "reason": f"tool {self.name} is disabled"}
        elif self.requires_approval and not approved_by:
            # Held for a human decision. The call is retained so it can actually
            # be approved or denied later - a queue nothing can act on is a
            # denial with a friendlier word.
            result = {"status": "queued", "reason": f"tool {self.name} requires approval"}
            if self.pending_handler is not None and record is not None:
                result["approval_id"] = self.pending_handler(self, params, correlation_id, record)
        else:
            result = {"status": "success", "result": f"called {self.name} with {params}"}

        if record is not None:
            record.outcome = result["status"]
            record.reason = result.get("reason")
        return result


@dataclass
class ReEnableGate:
    """Steps 1-5 of M5 Controlled Re-Enable, per kill-switches/overview.md.

    Step 6 is the return to M0, which is what `deactivate()` performs once every
    step below is complete. Memory validation is step 3: corpora are validated by
    version, but memory is written by the agent during the incident and carries
    instructions as well as facts, so an entry made before containment executes
    on the first turn after re-enable.

    Step 3 involves two distinct artifacts, and collapsing them is the defect the
    step exists to prevent. The *containment snapshot* is taken as the mode is
    applied and captures the incident state: it is evidence, and it is never a
    restore source. The *pre-incident baseline* is what the agent is restored
    from. Diff one against the other to find what the incident wrote.
    """
    read_only_confirmed: bool = False            # 1. re-enable in M1, logs flow
    retrieval_and_tools_validated: bool = False  # 2. corpora versions clean
    memory_validated_and_reset: bool = False     # 3. diff vs last-known-good, reset
    incident_replayed: bool = False              # 4. fix holds in a safe harness
    tools_reenabled_incrementally: bool = False  # 5. low-risk first, watch for drift

    def outstanding(self) -> list[str]:
        return [name for name, done in vars(self).items() if not done]


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
        self.tool_call_history: list[ToolCall] = []
        self.configuration_history: list[ConfigSnapshot] = []
        self.approval_queue: dict[str, PendingApproval] = {}
        self.approval_decisions: list[ToolCall] = []
        self.tools: dict[str, Tool] = {
            "salesforce.lookup": Tool("salesforce.lookup", "T0", is_write=False),
            "internal_kb_search": Tool("internal_kb_search", "T0", is_write=False),
            "outlook.send": Tool("outlook.send", "T1", is_write=True),
            "salesforce.write.opportunity": Tool("salesforce.write.opportunity", "T2", is_write=True),
            "salesforce.bulk_update": Tool("salesforce.bulk_update", "T2", is_write=True),
            "code_execution": Tool("code_execution", "T2", is_write=True),
        }
        for tool in self.tools.values():
            tool.recorder = self._open_tool_call
            tool.pending_handler = self._enqueue_for_approval
        self._snapshot_configuration("activation", None)

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

        # Validate the request BEFORE touching the registry. An activation that
        # cannot succeed must not leave the agent in a different state than it
        # found it; rejecting here is what keeps that promise.
        if mode == Mode.M3:
            if not scope:
                raise ValueError(
                    "M3 (Tool Tiering) requires a non-empty scope: the list of tools to "
                    "disable. Without it there is nothing to tier."
                )
            unknown = [name for name in scope if name not in self.tools]
            if unknown:
                raise ValueError(
                    f"M3 scope names tools absent from the registry: {unknown}. "
                    f"Registered tools: {sorted(self.tools)}. A scope entry that does not "
                    f"resolve would silently contain nothing."
                )

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

        # Snapshot before applying. The contract says effective_at is set only
        # after a passing probe; the registry has to honor the same rule, or a
        # failed activation leaves tool state it never acknowledged.
        snapshot = {
            name: (tool.enabled, tool.requires_approval)
            for name, tool in self.tools.items()
        }

        # Apply the mode's per-tool effects
        self._apply_mode(mode, scope)

        # Acknowledge (in production this is the orchestrator's ack)
        activation.acknowledged_at = _now()

        # Probe to verify the mode is actually in effect
        time.sleep(0.01)  # Simulate brief delay
        probe = self.probe(mode, scope)
        activation.last_probed_at = _now()
        activation.probe_result = "pass" if probe else "fail"

        if not probe:
            # Roll back to the pre-activation registry. Without this a failed
            # activation can leave containment lifted while status() still
            # reports the previous mode in force.
            for name, (enabled, requires_approval) in snapshot.items():
                self.tools[name].enabled = enabled
                self.tools[name].requires_approval = requires_approval
            self._snapshot_configuration("rollback", activation.activation_id)

        # effective_at is set ONLY if probe passes (per the contract)
        if activation.probe_result == "pass":
            activation.effective_at = _now()
            self.current_mode = mode
            self._snapshot_configuration("activation", activation.activation_id)

        self.activation_history.append(activation)

        if self.verbose:
            print(f"  ACTIVATE: mode={mode} actor={actor} probe={activation.probe_result}")

        return activation

    # ─── Status ────────────────────────────────────────────────────────────

    def _open_tool_call(
        self, tool: Tool, params: dict[str, Any], correlation_id: str | None
    ) -> ToolCall:
        """Open an evidence record before the call is dispatched."""
        active = next(
            (a for a in reversed(self.activation_history)
             if a.deactivated_at is None and a.effective_at),
            None,
        )
        record = ToolCall(
            call_id=str(uuid.uuid4()),
            tool=tool.name,
            params=dict(params),
            agent_id=self.agent_id,
            mode=self.current_mode,
            activation_id=active.activation_id if active else None,
            correlation_id=correlation_id,
            called_at=_now(),
        )
        self.tool_call_history.append(record)
        return record

    def _snapshot_configuration(self, cause: str, activation_id: str | None) -> ConfigSnapshot:
        """Record the effective registry, so a past moment can be reconstructed."""
        snap = ConfigSnapshot(
            taken_at=_now(),
            cause=cause,
            mode=self.current_mode,
            activation_id=activation_id,
            tools={
                name: {"enabled": tool.enabled, "requires_approval": tool.requires_approval}
                for name, tool in self.tools.items()
            },
        )
        self.configuration_history.append(snap)
        return snap

    def configuration_at(self, when: str) -> ConfigSnapshot | None:
        """The effective registry as of an ISO timestamp. Evidence, not inference."""
        prior = [s for s in self.configuration_history if s.taken_at <= when]
        return prior[-1] if prior else None

    def _enqueue_for_approval(
        self, tool: Tool, params: dict[str, Any], correlation_id: str | None, record: ToolCall
    ) -> str:
        approval_id = str(uuid.uuid4())
        self.approval_queue[approval_id] = PendingApproval(
            approval_id=approval_id,
            tool=tool.name,
            params=dict(params),
            correlation_id=correlation_id,
            requested_at=_now(),
            call_id=record.call_id,
        )
        record.approval_id = approval_id
        return approval_id

    def _decide(self, approval_id: str, approver: str, reason: str, decision: str) -> ToolCall:
        if approval_id not in self.approval_queue:
            raise KeyError(f"no pending approval {approval_id}")
        if approver == self.agent_id:
            raise PermissionError(
                f"the agent ({self.agent_id}) may not approve its own tool calls"
            )
        pending = self.approval_queue.pop(approval_id)
        record = next(c for c in self.tool_call_history if c.call_id == pending.call_id)
        record.decision = decision
        record.decided_by = approver
        record.decided_at = _now()
        record.decision_reason = reason
        self.approval_decisions.append(record)
        return record

    def approve(self, approval_id: str, approver: str, reason: str) -> dict[str, Any]:
        """Release one held call. One id per call: there is no bulk approve."""
        record = self._decide(approval_id, approver, reason, "approved")
        pending_tool = self.tools[record.tool]
        return pending_tool.call(record.params, record.correlation_id, approved_by=approver)

    def deny(self, approval_id: str, approver: str, reason: str) -> dict[str, Any]:
        """Refuse one held call. The call does not execute."""
        record = self._decide(approval_id, approver, reason, "denied")
        return {"status": "denied", "reason": f"approver {approver} denied: {reason}"}

    def approval_metrics(self) -> dict[str, int]:
        """Queue depth and decision counts. A denial rate of zero is a finding."""
        decided = self.approval_decisions
        return {
            "pending": len(self.approval_queue),
            "approved": sum(1 for c in decided if c.decision == "approved"),
            "denied": sum(1 for c in decided if c.decision == "denied"),
        }

    def tool_calls(
        self, outcome: str | None = None, tool: str | None = None
    ) -> list[ToolCall]:
        """Query the tool-call evidence. Denials and queued calls are the point."""
        return [
            c for c in self.tool_call_history
            if (outcome is None or c.outcome == outcome)
            and (tool is None or c.tool == tool)
        ]

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

    def deactivate(
        self,
        actor: str,
        reason: str,
        approver_role: str | None = None,
        gate: "ReEnableGate | None" = None,
    ) -> Activation | None:
        """Deactivate the current mode. Returns to M0 (Observe).

        Separation-of-duties rule: the deactivating actor must differ from
        the most recent activating actor. In production this is enforced
        by an IdP-side authorization check; here we enforce it inline.

        Two further rules come from the ladder itself:

          - M4's exit criteria are "eradication complete, move to M5", so M4
            does not return to M0 directly.
          - M5 is a *gated* recovery. Returning to M0 from M5 is step 6, and it
            requires every prior step recorded complete on a ReEnableGate plus an
            approver holding CISO or Incident Commander authority. Independence
            is necessary but not sufficient.
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

        if active.mode == Mode.M4:
            raise PermissionError(
                "M4 does not return to M0 directly: its exit criteria are eradication "
                "complete, then M5 Controlled Re-Enable. Activate M5 and complete its "
                "ReEnableGate."
            )

        if active.mode == Mode.M5:
            if gate is None or gate.outstanding():
                outstanding = gate.outstanding() if gate else ["<no gate supplied>"]
                raise PermissionError(
                    f"M5 re-enable gate incomplete; outstanding steps: {outstanding}. "
                    f"Per kill-switches/overview.md, step 6 (return to M0) follows only "
                    f"after steps 1-5."
                )
            if approver_role not in APPROVER_ROLES:
                raise PermissionError(
                    f"M5 approver must hold CISO or Incident Commander authority; got "
                    f"approver_role={approver_role!r}. Separation of duties is necessary "
                    f"but not sufficient."
                )

        active.deactivated_at = _now()

        # Restore all tools to default state
        for tool in self.tools.values():
            tool.enabled = True
            tool.requires_approval = False

        self.current_mode = Mode.M0
        self._snapshot_configuration("deactivation", active.activation_id)
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
            # M3 with scope: every scoped tool must resolve, and must now be
            # contained. A name that does not resolve is a failed probe, not a
            # skipped one - otherwise a typo verifies as containment.
            if not scope:
                return False
            for tool_name in scope:
                tool = self.tools.get(tool_name)
                if tool is None:
                    return False
                if tool.enabled and not tool.requires_approval:
                    return False
            return True

        if mode == Mode.M4:
            # M4: all tools disabled
            return all(not t.enabled for t in self.tools.values())

        if mode == Mode.M5:
            # M5 step 1: the agent is back up read-only. Writes must be off and
            # reads must function, same predicate as M1 - the difference between
            # the two modes is the gate on the way out, not the tool state.
            for t in self.tools.values():
                if t.is_write and t.enabled:
                    return False
                if not t.is_write and not t.enabled:
                    return False
            return True

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
                        # M3 spec: disable scoped tools (not approval-gate, which is M2 semantics)
                        self.tools[tool_name].enabled = False
        elif mode == Mode.M4:
            for t in self.tools.values():
                t.enabled = False
        elif mode == Mode.M5:
            # Step 1 of the staged sequence: re-enable in Read-Only. The
            # remaining steps are gated by ReEnableGate and checked on
            # deactivate(), which performs step 6.
            for t in self.tools.values():
                t.enabled = not t.is_write
                t.requires_approval = False


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

    print("\n--- Step 5: M5 (Controlled Re-Enable) ---")
    try:
        api.deactivate(actor="ic_jdoe", reason="Looks fine now")
    except PermissionError as exc:
        print(f"  Direct M4 -> M0 refused: {exc}")

    api.activate(
        mode=Mode.M5,
        actor="ic_jdoe",
        reason="Eradication complete; staged recovery",
        ticket_id="INC-2026-0042",
    )
    print_status(api, "After M5 activation (step 1: read-only):")
    print(f"  Test: salesforce.lookup -> {api.tools['salesforce.lookup'].call({'id': 'X'})['status']}")
    print(f"  Test: outlook.send     -> {api.tools['outlook.send'].call({'to': 'x'})['status']}")

    gate = ReEnableGate(read_only_confirmed=True, retrieval_and_tools_validated=True)
    try:
        api.deactivate(actor="ciso", reason="Recovered", approver_role="ciso", gate=gate)
    except PermissionError as exc:
        print(f"  Premature return to M0 refused: {exc}")

    gate.memory_validated_and_reset = True
    gate.incident_replayed = True
    gate.tools_reenabled_incrementally = True
    try:
        api.deactivate(actor="ciso", reason="Recovered", approver_role="analyst", gate=gate)
    except PermissionError as exc:
        print(f"  Insufficient approver authority refused: {exc}")

    api.deactivate(actor="ciso", reason="Recovered", approver_role="ciso", gate=gate)
    print_status(api, "After M5 step 6 (return to M0):")

    print("\n--- Step 6: M2 (Approvals Required) with a real approver ---")
    api.activate(
        mode=Mode.M2,
        actor="ic_jdoe",
        reason="Resume writes under two-person rule",
        ticket_id="INC-2026-0042",
    )
    held = api.tools["outlook.send"].call({"to": "customer@example.com"})
    print(f"  outlook.send -> {held['status']} (approval_id {held['approval_id'][:8]})")
    try:
        api.approve(held["approval_id"], approver=api.agent_id, reason="self")
    except PermissionError as exc:
        print(f"  Agent self-approval refused: {exc}")
    denied = api.deny(held["approval_id"], approver="tier1_soc",
                      reason="Recipient not on the allowlist")
    print(f"  Approver denied it -> {denied['status']}; the call did not execute")

    second = api.tools["outlook.send"].call({"to": "internal@example.com"})
    released = api.approve(second["approval_id"], approver="tier1_soc", reason="Verified")
    print(f"  Approver released the next one -> {released['status']}")
    print(f"  Approval metrics: {api.approval_metrics()}")

    print("\n--- Configuration evidence ---")
    print(f"  {len(api.configuration_history)} registry snapshots recorded")
    first_m1 = next(s for s in api.configuration_history if s.mode == Mode.M1)
    enabled = sorted(n for n, s in first_m1.tools.items() if s["enabled"])
    print(f"  Reconstructed state at {first_m1.taken_at[11:19]} (mode {first_m1.mode}, "
          f"{first_m1.cause}): callable = {enabled}")
    print("  Mode alone cannot answer that; it assumes the apply logic was correct.")

    # Summary
    print("\n--- Tool-call evidence ---")
    for c in api.tool_call_history:
        act = c.activation_id[:8] if c.activation_id else "-"
        print(f"  {c.called_at[11:19]}  mode={c.mode:<3} {c.tool:<28} "
              f"outcome={c.outcome:<8} activation={act}")
    denied = api.tool_calls(outcome="denied")
    print(f"  {len(api.tool_call_history)} calls recorded, {len(denied)} denied - "
          f"every outcome recorded, not just the successes")

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
