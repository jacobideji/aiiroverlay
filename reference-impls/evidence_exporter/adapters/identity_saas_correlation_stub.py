"""
Type F: Identity and SaaS Audit-Log Correlation adapter (STUB).

Spec field requirements (per schemas/evidence-export.spec.md line 95):
  {timestamp, identity_principal, target_system, action, target_object,
   target_object_class, source_ip, correlation_id}

Format: JSON Lines, one file per downstream SaaS system the agent has scopes
for. The script MUST correlate correlation_id across systems where the
agent's tool call produced traceable downstream actions.

Per spec: vendor copilot Type F splits between customer-side and vendor-side
captures; MUST mark vendor-side with vendor name in source_system.

In production this connects to the customer's IdP (Okta, Entra) and to the
downstream SaaS audit logs (Salesforce, M365, ServiceNow, GitHub, cloud
control plane).
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type F records in the spec's canonical format."""
    return [
        {
            "timestamp": "2026-06-29T14:14:04.211Z",
            "identity_principal": "sales-triage-copilot-svc-account",
            "target_system": "salesforce",
            "action": "opportunity.update",
            "target_object": "0061a000ABC123",
            "target_object_class": "salesforce.opportunity",
            "source_ip": "10.42.7.18",
            "correlation_id": "trace-xyz-002",
        },
        {
            "timestamp": "2026-06-29T14:14:05.103Z",
            "identity_principal": "sales-triage-copilot-svc-account",
            "target_system": "okta",
            "action": "session.token_used",
            "target_object": "session-token-abc-001",
            "target_object_class": "okta.session",
            "source_ip": "10.42.7.18",
            "correlation_id": "trace-xyz-002",
        },
        {
            "timestamp": "2026-06-29T14:18:20.448Z",
            "identity_principal": "sales-triage-copilot-svc-account",
            "target_system": "microsoft365",
            "action": "outlook.send.attempted",
            "target_object": "external@vendor.example.net",
            "target_object_class": "m365.email.external_recipient",
            "source_ip": "10.42.7.18",
            "correlation_id": "trace-xyz-004",
        },
    ]
