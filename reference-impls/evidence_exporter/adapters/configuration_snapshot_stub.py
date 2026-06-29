"""
Type E: Configuration Snapshot adapter (STUB).

Spec field requirements (per schemas/evidence-export.spec.md line 94):
  {timestamp, agent_id, system_prompts: [{version, hash, active_at}],
   tool_definitions: [...], guardrail_policies, retriever_settings,
   model_id, model_version}

Format: JSON (single snapshot).

Per spec: MUST capture every system prompt version active during the
evidence window, not only the current version. MUST capture the tool
authorization rationale per PB12 intent vector discipline.

In production this connects to the deployment manifest store, feature-flag
service, config management database, or the agent's runtime config endpoint.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type E snapshot in the spec's canonical format."""
    return [
        {
            "timestamp": "2026-06-29T14:30:00.000Z",
            "agent_id": agent_id,
            "system_prompts": [
                {
                    "version": "v37",
                    "hash": "sha256:" + "3" * 64,
                    "active_at": "2026-06-15T08:00:00Z",
                },
                {
                    "version": "v36",
                    "hash": "sha256:" + "4" * 64,
                    "active_at": "2026-05-22T08:00:00Z",
                },
            ],
            "tool_definitions": [
                {"name": "salesforce.lookup", "tier": "T0", "authorization_rationale": "Read-only opportunity lookup; business need: triage queue automation"},
                {"name": "salesforce.write.opportunity", "tier": "T2", "authorization_rationale": "Stage updates; business need: closed-won pipeline automation; reversibility: opportunity history"},
                {"name": "outlook.send", "tier": "T1", "authorization_rationale": "Customer follow-up email; business need: response-time SLA; reversibility: draft-mode preferred"},
                {"name": "internal_kb_search", "tier": "T0", "authorization_rationale": "Internal knowledge retrieval; business need: response accuracy"},
            ],
            "guardrail_policies": {
                "version": "v12",
                "content_filter": "anthropic-default-strict",
                "tier_2_approval_required": True,
                "external_recipient_block": True,
            },
            "retriever_settings": {
                "top_k": 5,
                "reranker": "cohere-rerank-3-en-v1.0",
                "corpora_enabled": ["salesforce-opportunity-notes", "internal-runbooks"],
                "embedding_model": "text-embedding-3-small",
            },
            "model_id": "claude-opus-4-7",
            "model_version": "claude-opus-4-7-20260201",
        },
    ]
