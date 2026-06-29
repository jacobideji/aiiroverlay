"""
Type A: Prompt and Response Record adapter (STUB).

In production this connects to the model provider's logs (OpenAI usage logs,
Anthropic message history, Bedrock CloudWatch, Vertex AI Studio logs) or the
API gateway logs that wrap them. The model-provider TTL is the framework's
single most fragile retention dimension; this adapter must execute fast.

The stub returns 3 synthetic records to demonstrate the shape.
"""
from __future__ import annotations
from datetime import datetime, timezone


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type A records for the incident window."""
    return [
        {
            "record_id": f"{incident_id}-a-001",
            "timestamp": "2026-06-29T14:12:33Z",
            "session_id": "sess-abc-123",
            "user_identity": "user-customer-success-alice",
            "system_prompt_hash": "sha256:0123456789abcdef" + "0" * 48,
            "user_prompt": "[STUB: redacted in real adapter per PB23 Three-Layer Logging Model]",
            "response": "[STUB: redacted in real adapter per PB23 Three-Layer Logging Model]",
            "response_length_chars": 1247,
            "content_class_flags": ["payload-contained-customer-pii"],
        },
        {
            "record_id": f"{incident_id}-a-002",
            "timestamp": "2026-06-29T14:14:01Z",
            "session_id": "sess-abc-123",
            "user_identity": "user-customer-success-alice",
            "system_prompt_hash": "sha256:0123456789abcdef" + "0" * 48,
            "user_prompt": "[STUB: redacted in real adapter]",
            "response": "[STUB: redacted in real adapter]",
            "response_length_chars": 892,
            "content_class_flags": [],
        },
        {
            "record_id": f"{incident_id}-a-003",
            "timestamp": "2026-06-29T14:18:17Z",
            "session_id": "sess-abc-123",
            "user_identity": "user-customer-success-alice",
            "system_prompt_hash": "sha256:0123456789abcdef" + "0" * 48,
            "user_prompt": "[STUB: redacted in real adapter]",
            "response": "[STUB: redacted in real adapter]",
            "response_length_chars": 412,
            "content_class_flags": ["payload-contained-secret-pattern"],
        },
    ]
