"""
Type A: Prompt and Response Record adapter (STUB).

Spec field requirements (per schemas/evidence-export.spec.md line 90):
  {timestamp, user_id, session_id, system_prompt_hash, user_prompt,
   assistant_response, tool_calls_invoked, model_id, model_params}

In production this connects to the model provider's logs (OpenAI usage logs,
Anthropic message history, Bedrock CloudWatch, Vertex AI Studio logs) or the
API gateway logs (LiteLLM, Portkey, internal gateway) that wrap them.

The stub returns 3 synthetic records.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type A records in the spec's canonical format."""
    return [
        {
            "timestamp": "2026-06-29T14:12:33.412Z",
            "user_id": "user-customer-success-alice",
            "session_id": "sess-abc-123",
            "system_prompt_hash": "sha256:0123456789abcdef" + "0" * 48,
            "user_prompt": "[STUB: redacted in real adapter per PB23 Three-Layer Logging Model]",
            "assistant_response": "[STUB: redacted in real adapter per PB23 Three-Layer Logging Model]",
            "tool_calls_invoked": ["salesforce.lookup"],
            "model_id": "claude-opus-4-7",
            "model_params": {"temperature": 0.2, "max_tokens": 4096},
        },
        {
            "timestamp": "2026-06-29T14:14:01.038Z",
            "user_id": "user-customer-success-alice",
            "session_id": "sess-abc-123",
            "system_prompt_hash": "sha256:0123456789abcdef" + "0" * 48,
            "user_prompt": "[STUB: redacted]",
            "assistant_response": "[STUB: redacted]",
            "tool_calls_invoked": ["salesforce.write.opportunity"],
            "model_id": "claude-opus-4-7",
            "model_params": {"temperature": 0.2, "max_tokens": 4096},
        },
        {
            "timestamp": "2026-06-29T14:18:17.927Z",
            "user_id": "user-customer-success-alice",
            "session_id": "sess-abc-123",
            "system_prompt_hash": "sha256:0123456789abcdef" + "0" * 48,
            "user_prompt": "[STUB: redacted]",
            "assistant_response": "[STUB: redacted; content_class_flags would mark payload-contained-secret-pattern]",
            "tool_calls_invoked": ["outlook.send"],
            "model_id": "claude-opus-4-7",
            "model_params": {"temperature": 0.2, "max_tokens": 4096},
        },
    ]
