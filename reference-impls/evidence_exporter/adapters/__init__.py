# Stub adapters for the six evidence types.
# Replace each stub with vendor-specific implementations in production.

from . import (
    prompt_response_stub,
    tool_call_ledger_stub,
    retrieval_traces_stub,
    memory_snapshot_stub,
    configuration_snapshot_stub,
    identity_saas_correlation_stub,
)

__all__ = [
    "prompt_response_stub",
    "tool_call_ledger_stub",
    "retrieval_traces_stub",
    "memory_snapshot_stub",
    "configuration_snapshot_stub",
    "identity_saas_correlation_stub",
]
