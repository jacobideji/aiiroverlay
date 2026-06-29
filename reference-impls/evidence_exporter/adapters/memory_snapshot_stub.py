"""
Type D: Memory Snapshot adapter (STUB).

Spec field requirements (per schemas/evidence-export.spec.md line 93):
  {timestamp, scope, memory_store_id, contents_summary, retention_remaining}

Format: JSON (single snapshot or array of snapshots, one per scope).

Per spec: if memory is disabled (memory.enabled: false in the AI-BOM),
the script MUST emit status: skipped with no failure_reason. Return empty
list here to signal that.

In production this connects to the agent memory backend (Redis, vector DB,
application database) and produces a snapshot of persistent context at
incident time.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type D snapshot in the spec's canonical format.

    Returns empty list when memory is disabled, signaling status: skipped.
    """
    # In production, check the AI-BOM's memory.enabled field for this agent.
    # The stub returns a per-user snapshot to demonstrate the shape.
    return [
        {
            "timestamp": "2026-06-29T14:30:00.000Z",
            "scope": "per_user",
            "memory_store_id": "redis-prod-cluster-01",
            "contents_summary": (
                "12 entries for user-customer-success-alice over the last 30 days. "
                "Content classes: customer-pii (4 entries), case-context (5 entries), "
                "general (3 entries). Full content redacted per PB23 Three-Layer Logging Model; "
                "content hashes available on request under elevated access discipline."
            ),
            "retention_remaining": "29 days for default-tier entries; 6 days for content-class-flagged-pii",
        },
    ]
