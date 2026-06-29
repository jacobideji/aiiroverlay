"""
Type E: Configuration Snapshot adapter (STUB).

In production this connects to the deployment manifest store, feature-flag
service, config management database, or the agent's runtime configuration
endpoint. Captures the system prompt, tool definitions, policies, retriever
settings, model version pin, memory configuration.

The stub returns a snapshot of synthetic configuration.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    return [
        {
            "record_id": f"{incident_id}-e-001",
            "snapshot_at": "2026-06-29T14:30:00Z",
            "snapshot_type": "post_change",
            "agent_id": agent_id,
            "model_provider": "anthropic",
            "model_id": "claude-opus-4-7",
            "model_version_pinned": True,
            "system_prompt_version": "v37",
            "system_prompt_hash": "sha256:" + "3" * 64,
            "policy_version": "v12",
            "tools_enabled": [
                {"name": "salesforce.lookup", "tier": "T0"},
                {"name": "salesforce.write.opportunity", "tier": "T2"},
                {"name": "outlook.send", "tier": "T1"},
                {"name": "internal_kb_search", "tier": "T0"},
            ],
            "retriever_config": {
                "top_k": 5,
                "reranker": "cohere-rerank-3",
                "corpora_enabled": ["salesforce-opportunity-notes", "internal-runbooks"],
            },
            "memory_config": {
                "enabled": True,
                "scope": "per_user",
                "retention_days": 30,
            },
            "kill_switch_state": "M0",
        },
    ]
