# Evidence Exporter — Reference Implementation (Contract-Conformant)

A Python CLI implementing the [Evidence Export Script Contract](../../schemas/evidence-export.spec.md) for Types A through F. Conforms to the contract's MUST requirements: JSONL format for record-stream types (A, B, C, F), JSON for snapshot types (D, E), manifest at `<output_destination>/<incident_id>/manifest.json` with the spec's required fields, per-type artifacts at `<output_destination>/<incident_id>/<type>/`, exit codes 0-5, and `--validate-access` pre-flight mode.

**Note on v0.28.0:** The v0.26.0 initial release of this implementation had material contract deviations (wrong format, wrong field names, wrong manifest schema, missing exit codes). v0.28.0 rewrites the implementation to conform. If you forked the v0.26.0 version, please diff against this version.

## Run the demo

```bash
cd reference-impls/evidence_exporter
python3 evidence_exporter.py \
    --incident-id INC-2026-0042 \
    --agent-id sales-triage-copilot \
    --window-start 2026-06-29T14:00:00Z \
    --window-end 2026-06-29T15:00:00Z \
    --evidence-types A,B,C,D,E,F \
    --output-destination ./out \
    --actor incident_commander_jdoe

# Pre-staged access pre-flight (no evidence captured):
python3 evidence_exporter.py --validate-access \
    --incident-id PREFLIGHT-Q2 \
    --agent-id sales-triage-copilot \
    --window-start 2026-06-29T14:00:00Z \
    --window-end 2026-06-29T15:00:00Z \
    --output-destination ./preflight \
    --actor preflight_checker
```

Expected output (capture mode):
- `./out/INC-2026-0042/manifest.json`: per the spec's required fields (script_version, requested_at, completed_at, overall_status, types[])
- `./out/INC-2026-0042/A/records.jsonl`: Type A in JSON Lines (one record per line)
- `./out/INC-2026-0042/B/records.jsonl`: Type B in JSON Lines
- `./out/INC-2026-0042/C/records.jsonl`: Type C in JSON Lines
- `./out/INC-2026-0042/D/records.json`: Type D snapshot (single JSON object)
- `./out/INC-2026-0042/E/records.json`: Type E snapshot (single JSON object)
- `./out/INC-2026-0042/F/records.jsonl`: Type F in JSON Lines
- `./out/INC-2026-0042/telemetry.jsonl`: telemetry events (started, type_started, type_completed, completed)

Exit codes per spec:
- `0` overall_status success (all requested types captured)
- `1` overall_status partial (some types failed)
- `2` overall_status failed (all types failed)
- `3` Invalid input (missing required field, malformed timestamp)
- `4` Output destination unavailable
- `5` Authorization failure

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
