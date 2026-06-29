# Evidence Exporter — Reference Implementation

A minimal Python CLI implementing the [Evidence Export Script Contract](../../schemas/evidence-export.spec.md) for Types A through F.

## Run the demo

```bash
cd reference-impls/evidence_exporter
python3 evidence_exporter.py \
    --incident-id INC-2026-0042 \
    --agent-id sales-triage-copilot \
    --window-start 2026-06-29T14:00:00Z \
    --window-end 2026-06-29T15:00:00Z \
    --evidence-types A,B,C,D,E,F \
    --output-destination ./out/INC-2026-0042 \
    --actor incident_commander_jdoe
```

Expected output:
- `./out/INC-2026-0042/manifest.json`: the chain-of-custody anchor
- `./out/INC-2026-0042/type_A_prompt_response.json` (and Type B through F)
- `./out/INC-2026-0042/telemetry.jsonl`: per-event observability stream
- Exit code 0 on success, 1 on partial, 2 on failure

## File layout

```
evidence_exporter/
├── README.md                       (this file)
├── evidence_exporter.py            (the CLI entry point)
└── adapters/
    ├── __init__.py
    ├── prompt_response_stub.py            (Type A)
    ├── tool_call_ledger_stub.py           (Type B)
    ├── retrieval_traces_stub.py           (Type C)
    ├── memory_snapshot_stub.py            (Type D)
    ├── configuration_snapshot_stub.py     (Type E)
    └── identity_saas_correlation_stub.py  (Type F)
```

## What this demonstrates

| Contract element | Where in the code |
|---|---|
| Required CLI inputs | `evidence_exporter.py:main()` argparse |
| Parallel-export discipline | `evidence_exporter.py:run_export()` ThreadPoolExecutor |
| Per-type artifacts with required JSON fields | each `adapters/*_stub.py` |
| Manifest with integrity hashes (SHA-256 per artifact) | `evidence_exporter.py:compute_sha256()` + manifest assembly |
| Chain-of-custody attestation | manifest section in `run_export()` |
| Telemetry events for Metric 3 (Time-to-Evidence) | `evidence_exporter.py:emit_telemetry()` |
| Exit codes (0 success, 1 partial, 2 failure) | `run_export()` return value |

## Adapting for production

Replace each `adapters/*_stub.py` with a vendor-specific implementation:

| Stub | Replace with |
|---|---|
| `prompt_response_stub.py` | OpenAI usage API, Anthropic message history pull, Bedrock CloudWatch query, or API gateway log fetch |
| `tool_call_ledger_stub.py` | LangGraph callback aggregator, Bedrock Agents tool-trace pull, custom function-calling log query |
| `retrieval_traces_stub.py` | Vector store query log pull (Pinecone, Weaviate, Qdrant, pgvector), LangChain trace store |
| `memory_snapshot_stub.py` | Redis SCAN over memory keys, Postgres SELECT, agent-framework state export |
| `configuration_snapshot_stub.py` | Deployment manifest fetch, feature-flag service snapshot, config management database export |
| `identity_saas_correlation_stub.py` | Okta API correlated with Salesforce/M365/ServiceNow audit log queries by correlation ID |

The contract conformance (manifest shape, exit codes, telemetry event format) is preserved through the adapter swap.

## Dependencies

Python 3.10+ standard library only. No pip installs required.

## License

Apache 2.0. The word mark **AI IR Overlay™** is protected. See `../../LICENSE`.
