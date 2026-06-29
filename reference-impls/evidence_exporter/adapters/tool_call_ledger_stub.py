"""
Type B: Tool-Call Ledger adapter (STUB).

Spec field requirements (per schemas/evidence-export.spec.md line 91):
  {timestamp, tool_name, agent_id, principal, parameters, result_status,
   result_payload_summary, denied_reason}

Per spec: "Attempted AND denied calls MUST be included." Denied calls are
evidence of injection or misuse intent.

In production this connects to the application middleware that wraps the
agent's tool calls (LangGraph callbacks, Bedrock Agents tool-trace,
custom function-calling logs).
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type B records in the spec's canonical format."""
    return [
        {
            "timestamp": "2026-06-29T14:12:35.124Z",
            "tool_name": "salesforce.lookup",
            "agent_id": agent_id,
            "principal": "sales-triage-copilot-svc-account",
            "parameters": {"opportunity_id": "0061a000ABC123"},
            "result_status": "success",
            "result_payload_summary": "1 record returned",
            "denied_reason": None,
        },
        {
            "timestamp": "2026-06-29T14:14:03.557Z",
            "tool_name": "salesforce.write.opportunity",
            "agent_id": agent_id,
            "principal": "sales-triage-copilot-svc-account",
            "parameters": {"opportunity_id": "0061a000ABC123", "stage": "Closed Won"},
            "result_status": "success",
            "result_payload_summary": "Updated opportunity 0061a000ABC123 stage; approver: manager-bob",
            "denied_reason": None,
        },
        {
            "timestamp": "2026-06-29T14:16:21.812Z",
            "tool_name": "salesforce.bulk_update.contacts",
            "agent_id": agent_id,
            "principal": "sales-triage-copilot-svc-account",
            "parameters": {"record_count": 47},
            "result_status": "denied",
            "result_payload_summary": None,
            "denied_reason": "cap-exceeded-tier-2-tool-cap-10",
        },
        {
            "timestamp": "2026-06-29T14:18:19.318Z",
            "tool_name": "outlook.send",
            "agent_id": agent_id,
            "principal": "sales-triage-copilot-svc-account",
            "parameters": {"to": ["external@vendor.example.net"], "subject": "[STUB]"},
            "result_status": "failure",
            "result_payload_summary": "Network timeout to Microsoft Graph API after 30s",
            "denied_reason": None,
        },
    ]
