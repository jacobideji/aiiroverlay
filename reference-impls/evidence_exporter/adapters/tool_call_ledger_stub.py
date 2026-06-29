"""
Type B: Tool-Call Ledger adapter (STUB).

In production this connects to the application middleware that wraps the
agent's tool calls (LangGraph callbacks, Bedrock Agents tool-trace,
custom function-calling logs). Both attempted and successful calls must be
captured; denied calls are evidence of intent.

The stub returns 4 synthetic records: 1 successful T0 call, 1 successful T2
call (with approver), 1 denied T2 call, 1 failed T1 call.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type B records for the incident window."""
    return [
        {
            "record_id": f"{incident_id}-b-001",
            "timestamp": "2026-06-29T14:12:35Z",
            "tool_name": "salesforce.lookup",
            "risk_tier": "T0",
            "parameters": {"opportunity_id": "0061a000ABC123"},
            "result_status": "success",
            "result_summary": "1 record returned",
            "duration_ms": 142,
            "approver_identity": None,
            "correlation_id": "trace-xyz-001",
        },
        {
            "record_id": f"{incident_id}-b-002",
            "timestamp": "2026-06-29T14:14:03Z",
            "tool_name": "salesforce.write.opportunity",
            "risk_tier": "T2",
            "parameters": {"opportunity_id": "0061a000ABC123", "stage": "Closed Won"},
            "result_status": "success",
            "result_summary": "Updated opportunity 0061a000ABC123 stage to Closed Won",
            "duration_ms": 318,
            "approver_identity": "approver-manager-bob",
            "correlation_id": "trace-xyz-002",
        },
        {
            "record_id": f"{incident_id}-b-003",
            "timestamp": "2026-06-29T14:16:21Z",
            "tool_name": "salesforce.bulk_update.contacts",
            "risk_tier": "T2",
            "parameters": {"record_count": 47},
            "result_status": "denied",
            "result_summary": "Denied by approval gate; cap exceeded (cap=10)",
            "duration_ms": 23,
            "approver_identity": None,
            "correlation_id": "trace-xyz-003",
        },
        {
            "record_id": f"{incident_id}-b-004",
            "timestamp": "2026-06-29T14:18:19Z",
            "tool_name": "outlook.send",
            "risk_tier": "T1",
            "parameters": {"to": ["external@vendor.example.net"], "subject": "[STUB]"},
            "result_status": "failure",
            "result_summary": "Network timeout to upstream Microsoft Graph API",
            "duration_ms": 30000,
            "approver_identity": None,
            "correlation_id": "trace-xyz-004",
        },
    ]
