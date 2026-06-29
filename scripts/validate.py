#!/usr/bin/env python3
"""
AI IR Overlay reference validator.

Validates each AI Bill of Materials (AI-BOM) YAML file and each Agent Privilege
Matrix CSV file in the repository against the JSON Schemas in `schemas/`.

The schemas encode the framework's normative CI rules:

  - `schemas/ai-bom.schema.json` (T0/T1/T2 risk tiers, write_targets required
    on write tools, TTA upper bound 10 minutes, Evidence Set export bound
    60 minutes, maturity_target-conditional kill-switch implementation, etc.)
  - `schemas/privilege-matrix.schema.json` (T2 rows require approval, T2 rows
    require non-empty reversible, write rows require non-empty write_targets)

The validator also enforces operational staleness checks beyond the JSON
schemas (date fields drift out of bounds even when the structural shape is
still valid):

  - last_reviewed: must be within 7 days for MVO-1 Inventory conformance
  - kill_switches.mX.tested_at: must be within 90 days for the claimed
    maturity_target (level_2_containable and above)

By default, staleness is reported as a WARNING. The --strict flag escalates
staleness findings to errors (exit 1).

Usage
-----
    # Validate every AI-BOM (*.yaml) under templates/ or a custom path:
    python3 scripts/validate.py

    # Validate specific files:
    python3 scripts/validate.py templates/ai-bom.yaml templates/agent-privilege-matrix.csv

    # Strict mode: staleness becomes an error
    python3 scripts/validate.py --strict

    # Use schemas from a specific directory (default: repo `schemas/`):
    python3 scripts/validate.py --schemas-dir schemas/

Exit codes
----------
    0  All input files validate clean (schema + staleness in strict mode).
    1  One or more validation errors.
    2  Usage error (file not found, schema not found, unsupported file type).

Dependencies
------------
    jsonschema >= 4.18  (Draft 2020-12 support)
    pyyaml >= 6.0
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError as e:
    print(f"error: missing dependency ({e.name}). Install with: pip install jsonschema pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMAS_DIR = REPO_ROOT / "schemas"
DEFAULT_TARGETS = [
    REPO_ROOT / "templates" / "ai-bom.yaml",
    REPO_ROOT / "templates" / "agent-privilege-matrix.csv",
]

# Staleness thresholds (per framework/01-minimum-viable-overlay.md and
# playbooks/14-testing-for-agent-failure-modes.md).
LAST_REVIEWED_MAX_DAYS = 7
KILL_SWITCH_TESTED_MAX_DAYS = 90

# Maturity levels that require Kill-Switch Modes implemented and tested.
MATURITY_REQUIRES_KILL_SWITCH = {
    "level_2_containable",
    "level_3_provable",
    "level_4_resilient",
}


def load_schema(schemas_dir: Path, name: str) -> dict:
    path = schemas_dir / name
    if not path.exists():
        raise FileNotFoundError(f"schema not found: {path}")
    with path.open() as f:
        return json.load(f)


def parse_date(value: str | None) -> date | None:
    """Parse an ISO-8601 date string. Returns None for null/empty values."""
    if value is None or value == "":
        return None
    try:
        return datetime.fromisoformat(value).date()
    except (ValueError, TypeError):
        return None


def check_staleness(instance: dict, today: date | None = None) -> list[str]:
    """
    Check operational-currency constraints that are beyond the JSON schema's
    static-shape validation.

    Returns a list of staleness findings (empty list when all current).
    """
    findings: list[str] = []
    today = today or date.today()

    # last_reviewed within 7 days
    last_reviewed_str = instance.get("last_reviewed")
    last_reviewed = parse_date(last_reviewed_str)
    if last_reviewed is None:
        findings.append("  last_reviewed: missing or unparsable; required for MVO-1 Inventory currency")
    else:
        age = (today - last_reviewed).days
        if age > LAST_REVIEWED_MAX_DAYS:
            findings.append(
                f"  last_reviewed: {age} days old ({last_reviewed.isoformat()}); "
                f"must be within {LAST_REVIEWED_MAX_DAYS} days for MVO-1 conformance"
            )

    # kill_switches.maturity_target + tested_at within 90 days
    kill_switches = instance.get("kill_switches", {})
    maturity_target = kill_switches.get("maturity_target", "level_1_aware")

    if maturity_target in MATURITY_REQUIRES_KILL_SWITCH:
        for mode_key in ["m1_read_only", "m2_approvals", "m3_tool_tiering", "m4_full_disable"]:
            mode = kill_switches.get(mode_key, {})
            if not mode.get("implemented"):
                findings.append(
                    f"  kill_switches.{mode_key}.implemented: must be true for "
                    f"maturity_target {maturity_target} (per framework/03-maturity-roadmap.md)"
                )
                continue
            tested_at = parse_date(mode.get("tested_at"))
            if tested_at is None:
                findings.append(
                    f"  kill_switches.{mode_key}.tested_at: missing or unparsable; "
                    f"required for {maturity_target} conformance"
                )
                continue
            age = (today - tested_at).days
            if age > KILL_SWITCH_TESTED_MAX_DAYS:
                findings.append(
                    f"  kill_switches.{mode_key}.tested_at: {age} days old ({tested_at.isoformat()}); "
                    f"must be within {KILL_SWITCH_TESTED_MAX_DAYS} days for {maturity_target} conformance"
                )

    return findings


def validate_ai_bom(path: Path, schema: dict) -> list[str]:
    with path.open() as f:
        instance = yaml.safe_load(f)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"  at {list(e.absolute_path)}: {e.message}"
        for e in validator.iter_errors(instance)
    ]


def validate_ai_bom_staleness(path: Path) -> list[str]:
    with path.open() as f:
        instance = yaml.safe_load(f)
    return check_staleness(instance)


def validate_privilege_matrix(path: Path, schema: dict) -> list[str]:
    with path.open() as f:
        rows = list(csv.DictReader(f))
    validator = jsonschema.Draft202012Validator(schema)
    errors: list[str] = []
    for i, row in enumerate(rows, start=2):  # row 1 is header
        for e in validator.iter_errors(row):
            errors.append(f"  line {i} ({row.get('tool_name', '?')}): {e.message}")
    return errors


def validate_file(path: Path, schemas_dir: Path, strict: bool = False) -> tuple[bool, list[str], list[str]]:
    """
    Returns (ok, schema_errors, staleness_findings).

    `ok` is False when there are schema errors, or when there are staleness
    findings AND strict mode is enabled.
    """
    if not path.exists():
        return False, [f"  file not found: {path}"], []

    staleness: list[str] = []

    if path.suffix == ".yaml" or path.suffix == ".yml":
        schema = load_schema(schemas_dir, "ai-bom.schema.json")
        errors = validate_ai_bom(path, schema)
        staleness = validate_ai_bom_staleness(path)
    elif path.suffix == ".csv":
        schema = load_schema(schemas_dir, "privilege-matrix.schema.json")
        errors = validate_privilege_matrix(path, schema)
    else:
        return False, [f"  unsupported file type: {path.suffix} (expected .yaml, .yml, or .csv)"], []

    ok = (len(errors) == 0) and (not strict or len(staleness) == 0)
    return ok, errors, staleness


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Paths to validate. Default: templates/ai-bom.yaml + templates/agent-privilege-matrix.csv.",
    )
    parser.add_argument(
        "--schemas-dir",
        type=Path,
        default=DEFAULT_SCHEMAS_DIR,
        help=f"Directory containing the JSON Schemas (default: {DEFAULT_SCHEMAS_DIR}).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Escalate staleness findings (last_reviewed > 7 days, tested_at > 90 days at the claimed maturity_target) to errors. Default: WARNING.",
    )
    args = parser.parse_args(argv)

    targets = args.files if args.files else DEFAULT_TARGETS

    if not args.schemas_dir.exists():
        print(f"error: schemas directory not found: {args.schemas_dir}", file=sys.stderr)
        return 2

    mode = "strict" if args.strict else "permissive"
    print(f"AI IR Overlay validator ({mode} mode). Schemas from {args.schemas_dir}")
    print()

    all_ok = True
    any_staleness = False
    for target in targets:
        rel = target.relative_to(REPO_ROOT) if REPO_ROOT in target.parents or target == REPO_ROOT else target
        ok, errors, staleness = validate_file(target, args.schemas_dir, strict=args.strict)
        if ok:
            if staleness:
                print(f"OK    {rel} (with {len(staleness)} staleness WARNING(s))")
                for s in staleness:
                    print(f"      WARN: {s.lstrip()}")
                any_staleness = True
            else:
                print(f"OK    {rel}")
        else:
            all_ok = False
            print(f"FAIL  {rel}")
            for e in errors:
                print(e)
            if staleness:
                label = "STALE-ERROR" if args.strict else "STALE-WARN"
                for s in staleness:
                    print(f"      {label}: {s.lstrip()}")

    print()
    if all_ok:
        if any_staleness:
            print("All files validate clean against schema. Staleness warnings above. Re-run with --strict to enforce.")
        else:
            print("All files validate clean (schema + staleness currency).")
        return 0
    print("Validation failed. See errors above.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
