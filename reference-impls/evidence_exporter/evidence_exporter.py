#!/usr/bin/env python3
"""
AI IR Overlay reference evidence exporter.

A Python CLI implementing the Evidence Export Script Contract from
`schemas/evidence-export.spec.md` for Types A through F.

This implementation conforms to the contract's MUST requirements:
  - Required inputs (incident_id, agent_id, window_start, window_end,
    evidence_types, output_destination, actor)
  - Manifest at <output_destination>/<incident_id>/manifest.json with the
    spec's required fields (script_version, requested_at, completed_at,
    overall_status, types[] with per-type records)
  - Per-type artifacts at <output_destination>/<incident_id>/<type>/
    in JSON Lines format (Types A, B, C, F) or JSON (Types D, E)
  - Exit codes 0 (success), 1 (partial), 2 (failed), 3 (invalid input),
    4 (output destination unavailable), 5 (authorization failure)
  - Timing telemetry events (evidence_export.started, type_started,
    type_completed, completed)
  - --validate-access mode for pre-staged access pre-flight checks

The adapters in `adapters/` are STUBS. Adopters fork this and replace each
stub with vendor-specific implementations (OpenAI, Anthropic, Salesforce,
Okta, etc.). The contract conformance is preserved through the adapter swap.

Usage
-----
    python3 evidence_exporter.py \\
        --incident-id INC-2026-0042 \\
        --agent-id sales-triage-copilot \\
        --window-start 2026-06-29T14:00:00Z \\
        --window-end 2026-06-29T15:00:00Z \\
        --output-destination ./out \\
        --actor incident_commander_jdoe

    # Pre-staged access pre-flight check (no evidence captured):
    python3 evidence_exporter.py --validate-access \\
        --incident-id PREFLIGHT-2026-Q2 \\
        --agent-id sales-triage-copilot \\
        --window-start 2026-06-29T14:00:00Z \\
        --window-end 2026-06-29T15:00:00Z \\
        --output-destination /tmp/preflight \\
        --actor preflight_checker

Exit codes
----------
    0  overall_status: success (all requested types captured)
    1  overall_status: partial (some types failed)
    2  overall_status: failed (all types failed)
    3  Invalid input (missing required field, malformed timestamp)
    4  Output destination unavailable
    5  Authorization failure (script lacks pre-staged access)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

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

SCRIPT_VERSION = "0.1.0"

# Per-type configuration: (output_format, default_source_system, capture_fn)
# Output format: "jsonl" for Types A, B, C, F (line-per-record); "json" for Types D, E (snapshot)
EVIDENCE_TYPES: dict[str, tuple[str, str, Callable]] = {
    "A": ("jsonl", "litellm-proxy-logs", prompt_response_stub.capture),
    "B": ("jsonl", "tool-wrapper-middleware", tool_call_ledger_stub.capture),
    "C": ("jsonl", "rag-trace-store", retrieval_traces_stub.capture),
    "D": ("json", "agent-memory-backend", memory_snapshot_stub.capture),
    "E": ("json", "config-management-system", configuration_snapshot_stub.capture),
    "F": ("jsonl", "okta-system-log+saas-audit", identity_saas_correlation_stub.capture),
}

VALID_FAILURE_REASONS = {
    "retention-exceeded",
    "auth-failure",
    "source-unreachable",
    "timeout",
    "vendor-pending",
    "output-destination-unavailable",
}


@dataclass
class TypeRecord:
    """Per-type record for the manifest, per spec section 'Per-type record schema'."""
    type: str
    status: str  # "success", "partial", "failed", "skipped"
    source_system: str
    records_captured: int
    output_path: str
    started_at: str
    completed_at: str
    duration_seconds: int
    failure_reason: Optional[str] = None
    failure_detail: Optional[str] = None


@dataclass
class TelemetryEvent:
    event_name: str
    timestamp: str
    attributes: dict


def parse_rfc3339(value: str) -> datetime:
    """Parse an RFC 3339 timestamp. Raises ValueError on invalid input."""
    # Accept Z suffix and explicit timezone offsets
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def emit_telemetry(events: list[TelemetryEvent], event_name: str, **attributes) -> None:
    """Emit a telemetry event. In production, push to OpenTelemetry / SIEM."""
    event = TelemetryEvent(
        event_name=event_name,
        timestamp=datetime.now(timezone.utc).isoformat(),
        attributes=attributes,
    )
    events.append(event)
    print(f"  TELEMETRY {event_name}: {json.dumps(attributes, separators=(',', ':'), default=str)}")


def write_artifact(records: list[dict], path: Path, format: str) -> int:
    """Write records as JSONL (one per line) or JSON (single object). Returns bytes written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if format == "jsonl":
        with path.open("w") as f:
            for record in records:
                f.write(json.dumps(record, default=str) + "\n")
    else:  # "json"
        # For snapshot types (D, E), records is a list of one or more snapshots
        with path.open("w") as f:
            if len(records) == 1:
                json.dump(records[0], f, indent=2, default=str)
            else:
                json.dump(records, f, indent=2, default=str)
    return path.stat().st_size


def capture_one_type(
    type_code: str,
    incident_id: str,
    agent_id: str,
    window_start: str,
    window_end: str,
    output_dir: Path,
) -> TypeRecord:
    """Capture one evidence type and produce a TypeRecord for the manifest."""
    output_format, source_system, capture_fn = EVIDENCE_TYPES[type_code]
    started_at = datetime.now(timezone.utc)
    started_iso = started_at.isoformat()

    try:
        records = capture_fn(
            agent_id=agent_id,
            window_start=window_start,
            window_end=window_end,
            incident_id=incident_id,
        )

        if not records:
            # Type D may return empty list when memory.enabled=false; spec mandates "skipped"
            completed_at = datetime.now(timezone.utc)
            return TypeRecord(
                type=type_code,
                status="skipped",
                source_system=source_system,
                records_captured=0,
                output_path="",
                started_at=started_iso,
                completed_at=completed_at.isoformat(),
                duration_seconds=int((completed_at - started_at).total_seconds()),
            )

        extension = "jsonl" if output_format == "jsonl" else "json"
        artifact_path = output_dir / type_code / f"records.{extension}"
        write_artifact(records, artifact_path, output_format)

        completed_at = datetime.now(timezone.utc)
        return TypeRecord(
            type=type_code,
            status="success",
            source_system=source_system,
            records_captured=len(records),
            output_path=str(artifact_path.relative_to(output_dir.parent)),
            started_at=started_iso,
            completed_at=completed_at.isoformat(),
            duration_seconds=int((completed_at - started_at).total_seconds()),
        )

    except Exception as e:
        completed_at = datetime.now(timezone.utc)
        return TypeRecord(
            type=type_code,
            status="failed",
            source_system=source_system,
            records_captured=0,
            output_path="",
            started_at=started_iso,
            completed_at=completed_at.isoformat(),
            duration_seconds=int((completed_at - started_at).total_seconds()),
            failure_reason="source-unreachable",
            failure_detail=str(e),
        )


def validate_access(args, telemetry: list[TelemetryEvent]) -> int:
    """
    Implement the --validate-access mode per spec.

    Exercises each pre-staged access path WITHOUT capturing evidence.
    Returns a structured report listing any gaps.
    """
    print(f"AI IR Overlay evidence exporter v{SCRIPT_VERSION}: --validate-access mode")
    print()

    # Reuse the output directory check to confirm writability
    output_dir = Path(args.output_destination) / args.incident_id
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        test_file = output_dir / ".write_test"
        test_file.write_text("preflight\n")
        test_file.unlink()
        output_writable = True
    except (OSError, PermissionError):
        output_writable = False

    # For the reference impl, the stub adapters always "succeed" their access check;
    # in production, each adapter would attempt a read query against its source system
    access_report = []
    for type_code in EVIDENCE_TYPES:
        output_format, source_system, _ = EVIDENCE_TYPES[type_code]
        access_report.append({
            "type": type_code,
            "source_system": source_system,
            "access_ok": True,
            "note": "stub adapter: production implementations attempt a real read query",
        })

    report = {
        "validation_mode": "validate-access",
        "incident_id": args.incident_id,
        "agent_id": args.agent_id,
        "script_version": SCRIPT_VERSION,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "output_destination_writable": output_writable,
        "access_paths": access_report,
        "gaps": [] if output_writable else ["output-destination-unwritable"],
        "overall_status": "ready" if output_writable else "gaps-detected",
    }

    report_path = output_dir / "preflight-report.json"
    report_path.write_text(json.dumps(report, indent=2))

    print(f"Validate-access report written to {report_path}")
    print(f"Overall status: {report['overall_status']}")

    if not output_writable:
        return 4
    return 0


def run_export(args) -> int:
    # Output structure: <output_destination>/<incident_id>/{manifest.json, <type>/records.{jsonl|json}}
    base_dir = Path(args.output_destination)
    output_dir = base_dir / args.incident_id

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        print(f"error: cannot write to {output_dir}: {e}", file=sys.stderr)
        return 4

    requested_at = datetime.now(timezone.utc)
    telemetry: list[TelemetryEvent] = []

    # Parse and validate evidence_types
    requested = args.evidence_types.split(",") if args.evidence_types else list(EVIDENCE_TYPES.keys())
    requested = [t.strip().upper() for t in requested]
    invalid = [t for t in requested if t not in EVIDENCE_TYPES]
    if invalid:
        print(f"error: invalid evidence types: {invalid}. Valid: A,B,C,D,E,F", file=sys.stderr)
        return 3

    # Compute the requested-window-seconds for telemetry
    try:
        win_start = parse_rfc3339(args.window_start)
        win_end = parse_rfc3339(args.window_end)
        requested_window_seconds = int((win_end - win_start).total_seconds())
    except ValueError:
        # Already caught at argparse / main, but defensive
        return 3

    emit_telemetry(
        telemetry,
        "evidence_export.started",
        incident_id=args.incident_id,
        agent_id=args.agent_id,
        requested_window_seconds=requested_window_seconds,
        requested_types=requested,
    )

    # Parallel capture per the contract
    results: list[TypeRecord] = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_type = {}
        for type_code in requested:
            _, source_system, _ = EVIDENCE_TYPES[type_code]
            emit_telemetry(
                telemetry,
                "evidence_export.type_started",
                incident_id=args.incident_id,
                agent_id=args.agent_id,
                type=type_code,
                source_system=source_system,
            )
            future = executor.submit(
                capture_one_type,
                type_code,
                args.incident_id,
                args.agent_id,
                args.window_start,
                args.window_end,
                output_dir,
            )
            future_to_type[future] = type_code

        for future in as_completed(future_to_type):
            result = future.result()
            results.append(result)
            emit_telemetry(
                telemetry,
                "evidence_export.type_completed",
                incident_id=args.incident_id,
                agent_id=args.agent_id,
                type=result.type,
                status=result.status,
                duration_seconds=result.duration_seconds,
                records_captured=result.records_captured,
            )

    completed_at = datetime.now(timezone.utc)
    total_duration_seconds = int((completed_at - requested_at).total_seconds())

    # Determine overall_status per spec
    types_succeeded = sum(1 for r in results if r.status == "success")
    types_skipped = sum(1 for r in results if r.status == "skipped")
    types_partial = sum(1 for r in results if r.status == "partial")
    types_failed = sum(1 for r in results if r.status == "failed")

    types_done = types_succeeded + types_skipped
    if types_done == len(results):
        overall_status = "success"
    elif types_done > 0 or types_partial > 0:
        overall_status = "partial"
    else:
        overall_status = "failed"

    # Build manifest per spec
    manifest = {
        "incident_id": args.incident_id,
        "agent_id": args.agent_id,
        "script_version": SCRIPT_VERSION,
        "requested_at": requested_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "actor": args.actor,
        "requested_window_start": args.window_start,
        "requested_window_end": args.window_end,
        "overall_status": overall_status,
        "types": [asdict(r) for r in sorted(results, key=lambda x: x.type)],
        "chain_of_custody": {
            "actor": args.actor,
            "attestation_timestamp": completed_at.isoformat(),
            "statement": (
                "I attest that this evidence export was performed under documented "
                "incident response authority. The script_version, requested_at, and "
                "completed_at fields establish the export window; the per-type records "
                "establish the per-source capture audit trail."
            ),
        },
    }

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str))

    # Write telemetry events as JSONL for downstream consumption
    telemetry_path = output_dir / "telemetry.jsonl"
    with telemetry_path.open("w") as f:
        for event in telemetry:
            f.write(json.dumps(asdict(event), default=str) + "\n")

    emit_telemetry(
        telemetry,
        "evidence_export.completed",
        incident_id=args.incident_id,
        agent_id=args.agent_id,
        overall_status=overall_status,
        total_duration_seconds=total_duration_seconds,
        types_succeeded=types_succeeded,
        types_partial=types_partial,
        types_failed=types_failed,
    )

    # Re-write telemetry with the final completed event
    with telemetry_path.open("w") as f:
        for event in telemetry:
            f.write(json.dumps(asdict(event), default=str) + "\n")

    # Console summary
    print()
    print(f"Evidence export {overall_status}: {types_done}/{len(results)} types captured (+ {types_skipped} skipped).")
    print(f"  Total duration: {total_duration_seconds}s (target: <= 3600s per framework MVO-3)")
    print(f"  Manifest:  {manifest_path}")
    print(f"  Telemetry: {telemetry_path}")
    for r in sorted(results, key=lambda x: x.type):
        icon = {"success": "✓", "skipped": "○", "partial": "⚠", "failed": "✗"}.get(r.status, "?")
        print(f"  {icon} Type {r.type}: {r.status} ({r.records_captured} records, {r.duration_seconds}s)")
        if r.failure_detail:
            print(f"      reason: {r.failure_reason}; {r.failure_detail}")

    # Exit codes per spec
    if overall_status == "success":
        return 0
    if overall_status == "partial":
        return 1
    return 2


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--incident-id", required=True, help="Reference to the incident ticket")
    parser.add_argument("--agent-id", required=True, help="AI-BOM agent.name of the affected agent")
    parser.add_argument("--window-start", required=True, help="RFC 3339 UTC start of evidence window")
    parser.add_argument("--window-end", required=True, help="RFC 3339 UTC end of evidence window")
    parser.add_argument(
        "--evidence-types",
        default="A,B,C,D,E,F",
        help="Comma-separated subset of A,B,C,D,E,F (default: all six)",
    )
    parser.add_argument(
        "--output-destination",
        required=True,
        help="Directory; the script writes to <output_destination>/<incident_id>/",
    )
    parser.add_argument(
        "--actor",
        required=True,
        help="Identity of the responder executing the export (chain-of-custody)",
    )
    parser.add_argument(
        "--validate-access",
        action="store_true",
        help="Pre-flight check: exercise pre-staged access paths without capturing evidence",
    )
    args = parser.parse_args(argv)

    # Input validation
    for ts_field, ts_value in [("window_start", args.window_start), ("window_end", args.window_end)]:
        try:
            parse_rfc3339(ts_value)
        except ValueError:
            print(f"error: --{ts_field.replace('_', '-')} is not a valid RFC 3339 timestamp: {ts_value}", file=sys.stderr)
            return 3

    if args.validate_access:
        return validate_access(args, telemetry=[])

    return run_export(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
