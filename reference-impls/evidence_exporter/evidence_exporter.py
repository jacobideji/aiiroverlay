#!/usr/bin/env python3
"""
AI IR Overlay reference evidence exporter.

A minimal Python CLI implementing the Evidence Export Script Contract from
`schemas/evidence-export.spec.md` for Types A through F.

This is NOT production code. It is a skeleton that demonstrates the
contract's manifest discipline, parallel-export pattern, integrity hashing,
and telemetry event emission. Adopters fork this and replace the stub
adapters with vendor-specific implementations (OpenAI, Anthropic, Salesforce,
Okta, etc.).

Conformance to the contract is demonstrated by:
  - Required inputs accepted (incident_id, agent_id, window_start, window_end,
    evidence_types, output_destination, actor)
  - Manifest produced in the contract's specified shape
  - Per-type artifacts produced with required JSON fields
  - Exit codes match the contract (0 success, 1 partial, 2 failure)
  - Telemetry events emitted in the canonical format

Usage
-----
    python3 evidence_exporter.py \\
        --incident-id INC-2026-0042 \\
        --agent-id sales-triage-copilot \\
        --window-start 2026-06-29T14:00:00Z \\
        --window-end 2026-06-29T15:00:00Z \\
        --evidence-types A,B,C,D,E,F \\
        --output-destination ./out/INC-2026-0042 \\
        --actor incident_commander_jdoe

    python3 evidence_exporter.py --help

Exit codes
----------
    0  All requested evidence types exported successfully
    1  Partial export (some types failed); manifest documents failures
    2  Unrecoverable error (invalid inputs, output destination unwritable)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

# Import stub adapters (replace with vendor-specific implementations in production)
sys.path.insert(0, str(Path(__file__).parent))
from adapters import (
    prompt_response_stub,
    tool_call_ledger_stub,
    retrieval_traces_stub,
    memory_snapshot_stub,
    configuration_snapshot_stub,
    identity_saas_correlation_stub,
)

EVIDENCE_TYPES = {
    "A": ("prompt_response", prompt_response_stub.capture),
    "B": ("tool_call_ledger", tool_call_ledger_stub.capture),
    "C": ("retrieval_traces", retrieval_traces_stub.capture),
    "D": ("memory_snapshot", memory_snapshot_stub.capture),
    "E": ("configuration_snapshot", configuration_snapshot_stub.capture),
    "F": ("identity_saas_correlation", identity_saas_correlation_stub.capture),
}


@dataclass
class CaptureResult:
    type_code: str
    type_name: str
    status: str  # "success", "partial", "failure"
    artifact_path: str | None
    bytes_captured: int
    record_count: int
    duration_ms: int
    error_message: str | None = None
    integrity_hash_sha256: str | None = None


@dataclass
class TelemetryEvent:
    event_id: str
    event_type: str  # "evidence_export.started", "evidence_export.type.completed", etc.
    timestamp: str
    incident_id: str
    agent_id: str
    actor: str
    payload: dict = field(default_factory=dict)


def compute_sha256(path: Path) -> str:
    """Compute SHA-256 of a file for the manifest integrity anchor."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def emit_telemetry(events: list[TelemetryEvent], event_type: str, **payload) -> TelemetryEvent:
    """Emit a telemetry event and append to the event list."""
    event = TelemetryEvent(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        timestamp=datetime.now(timezone.utc).isoformat(),
        incident_id=payload.pop("incident_id", ""),
        agent_id=payload.pop("agent_id", ""),
        actor=payload.pop("actor", ""),
        payload=payload,
    )
    events.append(event)
    # In production, also push to SIEM / observability platform
    print(f"  TELEMETRY: {event.event_type} at {event.timestamp}")
    return event


def capture_one_type(
    type_code: str,
    type_name: str,
    capture_fn: Callable,
    incident_id: str,
    agent_id: str,
    window_start: str,
    window_end: str,
    output_dir: Path,
    actor: str,
) -> CaptureResult:
    """Run a single evidence-type capture and produce a CaptureResult."""
    started_at = datetime.now(timezone.utc)
    try:
        # The stub adapters produce a dict of evidence records
        records = capture_fn(
            agent_id=agent_id,
            window_start=window_start,
            window_end=window_end,
            incident_id=incident_id,
        )

        artifact_path = output_dir / f"type_{type_code}_{type_name}.json"
        with artifact_path.open("w") as f:
            json.dump(
                {
                    "type_code": type_code,
                    "type_name": type_name,
                    "incident_id": incident_id,
                    "agent_id": agent_id,
                    "window_start": window_start,
                    "window_end": window_end,
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                    "captured_by": actor,
                    "record_count": len(records),
                    "records": records,
                },
                f,
                indent=2,
                default=str,
            )

        integrity = compute_sha256(artifact_path)
        size = artifact_path.stat().st_size
        duration_ms = int((datetime.now(timezone.utc) - started_at).total_seconds() * 1000)

        return CaptureResult(
            type_code=type_code,
            type_name=type_name,
            status="success",
            artifact_path=str(artifact_path),
            bytes_captured=size,
            record_count=len(records),
            duration_ms=duration_ms,
            integrity_hash_sha256=integrity,
        )

    except Exception as e:
        duration_ms = int((datetime.now(timezone.utc) - started_at).total_seconds() * 1000)
        return CaptureResult(
            type_code=type_code,
            type_name=type_name,
            status="failure",
            artifact_path=None,
            bytes_captured=0,
            record_count=0,
            duration_ms=duration_ms,
            error_message=str(e),
        )


def run_export(args) -> int:
    output_dir = Path(args.output_destination)
    output_dir.mkdir(parents=True, exist_ok=True)

    telemetry: list[TelemetryEvent] = []
    emit_telemetry(
        telemetry,
        "evidence_export.started",
        incident_id=args.incident_id,
        agent_id=args.agent_id,
        actor=args.actor,
        evidence_types=args.evidence_types,
        window_start=args.window_start,
        window_end=args.window_end,
    )

    # Parse requested types (default: all six)
    requested = args.evidence_types.split(",") if args.evidence_types else list(EVIDENCE_TYPES.keys())
    requested = [t.strip().upper() for t in requested]
    invalid = [t for t in requested if t not in EVIDENCE_TYPES]
    if invalid:
        print(f"error: invalid evidence types: {invalid}. Valid: A,B,C,D,E,F", file=sys.stderr)
        return 2

    # Parallel export: run all requested types concurrently per the contract
    results: list[CaptureResult] = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(
                capture_one_type,
                code,
                EVIDENCE_TYPES[code][0],
                EVIDENCE_TYPES[code][1],
                args.incident_id,
                args.agent_id,
                args.window_start,
                args.window_end,
                output_dir,
                args.actor,
            ): code
            for code in requested
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            emit_telemetry(
                telemetry,
                "evidence_export.type.completed",
                incident_id=args.incident_id,
                agent_id=args.agent_id,
                actor=args.actor,
                type_code=result.type_code,
                status=result.status,
                bytes_captured=result.bytes_captured,
                record_count=result.record_count,
                duration_ms=result.duration_ms,
            )

    # Build the manifest per the contract's specified shape
    manifest = {
        "manifest_version": "1.0",
        "incident_id": args.incident_id,
        "agent_id": args.agent_id,
        "window_start": args.window_start,
        "window_end": args.window_end,
        "actor": args.actor,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "evidence_types_requested": requested,
        "results": [asdict(r) for r in sorted(results, key=lambda r: r.type_code)],
        "chain_of_custody_attestation": {
            "actor": args.actor,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "statement": (
                "I attest that this evidence export was performed under documented "
                "incident response authority. The integrity hashes recorded in this "
                "manifest are computed against the artifact files at capture time."
            ),
        },
    }

    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w") as f:
        json.dump(manifest, f, indent=2)

    # Write telemetry events
    telemetry_path = output_dir / "telemetry.jsonl"
    with telemetry_path.open("w") as f:
        for event in telemetry:
            f.write(json.dumps(asdict(event)) + "\n")

    # Summarize and determine exit code
    success_count = sum(1 for r in results if r.status == "success")
    failure_count = sum(1 for r in results if r.status == "failure")

    print()
    print(f"Evidence export complete: {success_count}/{len(results)} types captured.")
    print(f"  Manifest:  {manifest_path}")
    print(f"  Telemetry: {telemetry_path}")
    for r in sorted(results, key=lambda r: r.type_code):
        status_icon = "✓" if r.status == "success" else "✗"
        print(f"  {status_icon} Type {r.type_code} ({r.type_name}): {r.status} ({r.bytes_captured} bytes, {r.duration_ms} ms)")
        if r.error_message:
            print(f"    error: {r.error_message}")

    emit_telemetry(
        telemetry,
        "evidence_export.completed",
        incident_id=args.incident_id,
        agent_id=args.agent_id,
        actor=args.actor,
        success_count=success_count,
        failure_count=failure_count,
        total_duration_ms=sum(r.duration_ms for r in results),
    )

    if failure_count == 0:
        return 0
    if success_count > 0:
        return 1  # Partial success
    return 2  # All failed


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--incident-id", required=True, help="Customer-assigned incident identifier")
    parser.add_argument("--agent-id", required=True, help="AI-BOM agent_id of the affected agent")
    parser.add_argument("--window-start", required=True, help="ISO-8601 UTC start of the incident window")
    parser.add_argument("--window-end", required=True, help="ISO-8601 UTC end of the incident window")
    parser.add_argument(
        "--evidence-types",
        default="A,B,C,D,E,F",
        help="Comma-separated subset of A,B,C,D,E,F (default: all six)",
    )
    parser.add_argument(
        "--output-destination",
        required=True,
        help="Directory to write manifest and per-type artifacts",
    )
    parser.add_argument(
        "--actor",
        required=True,
        help="Identity of the responder executing the export (for chain-of-custody)",
    )
    args = parser.parse_args(argv)

    return run_export(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
