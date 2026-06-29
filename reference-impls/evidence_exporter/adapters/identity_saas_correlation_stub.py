"""
Type F: Identity and SaaS Audit-Log Correlation adapter (STUB).

In production this connects to the customer's IdP (Okta, Entra) and to the
downstream SaaS audit logs (Salesforce, M365, ServiceNow, GitHub, cloud
control plane). For output-leakage incidents per PB09, this is where the
output distribution map is composed.

The stub returns synthetic correlation records.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    return [
        {
            "record_id": f"{incident_id}-f-001",
            "timestamp": "2026-06-29T14:14:04Z",
            "actor_identity": "sales-triage-copilot-svc-account",
            "actor_type": "service_account",
            "downstream_system": "salesforce",
            "action": "opportunity.update",
            "target_record": "0061a000ABC123",
            "result": "success",
            "correlation_id": "trace-xyz-002",
        },
        {
            "record_id": f"{incident_id}-f-002",
            "timestamp": "2026-06-29T14:14:05Z",
            "actor_identity": "sales-triage-copilot-svc-account",
            "actor_type": "service_account",
            "downstream_system": "okta",
            "action": "session.token_used",
            "target_record": "session-token-abc-001",
            "result": "success",
            "correlation_id": "trace-xyz-002",
        },
        {
            "record_id": f"{incident_id}-f-003",
            "timestamp": "2026-06-29T14:18:20Z",
            "actor_identity": "sales-triage-copilot-svc-account",
            "actor_type": "service_account",
            "downstream_system": "microsoft365",
            "action": "outlook.send.attempted",
            "target_record": "external@vendor.example.net",
            "result": "failure_network_timeout",
            "correlation_id": "trace-xyz-004",
            "note": "External recipient; per PB09 Output Distribution Map this would enter the output-leakage scoping if the send had succeeded",
        },
    ]
