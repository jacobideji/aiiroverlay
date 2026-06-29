"""
Type D: Memory Snapshot adapter (STUB).

In production this connects to the agent memory backend (Redis, Postgres,
vector DB, agent-framework state store). For agents with memory disabled,
returns an empty list (a documented null result is part of the manifest).

The stub returns a snapshot of synthetic per-user memory entries.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    return [
        {
            "record_id": f"{incident_id}-d-001",
            "memory_backend": "redis-prod-cluster-01",
            "memory_scope": "per_user",
            "user_identity": "user-customer-success-alice",
            "snapshot_at": "2026-06-29T14:30:00Z",
            "entry_count": 12,
            "retention_window_days": 30,
            "entries": [
                {
                    "entry_id": "mem-001",
                    "created_at": "2026-06-29T13:45:00Z",
                    "content_hash": "sha256:" + "1" * 64,
                    "content": "[STUB: redacted in real adapter per PB23 Three-Layer Logging Model]",
                    "content_class_flags": [],
                },
                {
                    "entry_id": "mem-002",
                    "created_at": "2026-06-29T14:00:00Z",
                    "content_hash": "sha256:" + "2" * 64,
                    "content": "[STUB: redacted]",
                    "content_class_flags": ["payload-contained-customer-pii"],
                },
            ],
        },
    ]
