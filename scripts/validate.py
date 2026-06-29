#!/usr/bin/env python3
"""
AI IR Overlay reference validator.

Validates each AI Bill of Materials (AI-BOM) YAML file and each Agent Privilege
Matrix CSV file in the repository against the JSON Schemas in `schemas/`.

The schemas encode the framework's normative CI rules:

  - `schemas/ai-bom.schema.json` (T0/T1/T2 risk tiers, write_targets required
    on write tools, TTA upper bound 10 minutes, Evidence Set export bound
    60 minutes, etc.)
  - `schemas/privilege-matrix.schema.json` (T2 rows require approval, T2 rows
    require non-empty reversible, write rows require non-empty write_targets)

Usage
-----
    # Validate every AI-BOM (*.yaml) under templates/ or a custom path:
    python3 scripts/validate.py

    # Validate specific files:
    python3 scripts/validate.py templates/ai-bom.yaml templates/agent-privilege-matrix.csv

    # Use schemas from a specific directory (default: repo `schemas/`):
    python3 scripts/validate.py --schemas-dir schemas/

Exit codes
----------
    0  All input files validate clean.
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


def load_schema(schemas_dir: Path, name: str) -> dict:
    path = schemas_dir / name
    if not path.exists():
        raise FileNotFoundError(f"schema not found: {path}")
    with path.open() as f:
        return json.load(f)


def validate_ai_bom(path: Path, schema: dict) -> list[str]:
    with path.open() as f:
        instance = yaml.safe_load(f)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"  at {list(e.absolute_path)}: {e.message}"
        for e in validator.iter_errors(instance)
    ]


def validate_privilege_matrix(path: Path, schema: dict) -> list[str]:
    with path.open() as f:
        rows = list(csv.DictReader(f))
    validator = jsonschema.Draft202012Validator(schema)
    errors: list[str] = []
    for i, row in enumerate(rows, start=2):  # row 1 is header
        for e in validator.iter_errors(row):
            errors.append(f"  line {i} ({row.get('tool_name', '?')}): {e.message}")
    return errors


def validate_file(path: Path, schemas_dir: Path) -> tuple[bool, list[str]]:
    """Returns (ok, error_messages)."""
    if not path.exists():
        return False, [f"  file not found: {path}"]

    if path.suffix == ".yaml" or path.suffix == ".yml":
        schema = load_schema(schemas_dir, "ai-bom.schema.json")
        errors = validate_ai_bom(path, schema)
    elif path.suffix == ".csv":
        schema = load_schema(schemas_dir, "privilege-matrix.schema.json")
        errors = validate_privilege_matrix(path, schema)
    else:
        return False, [f"  unsupported file type: {path.suffix} (expected .yaml, .yml, or .csv)"]

    return (len(errors) == 0), errors


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
    args = parser.parse_args(argv)

    targets = args.files if args.files else DEFAULT_TARGETS

    if not args.schemas_dir.exists():
        print(f"error: schemas directory not found: {args.schemas_dir}", file=sys.stderr)
        return 2

    print(f"AI IR Overlay validator. Schemas from {args.schemas_dir}")
    print()

    all_ok = True
    for target in targets:
        rel = target.relative_to(REPO_ROOT) if REPO_ROOT in target.parents or target == REPO_ROOT else target
        ok, errors = validate_file(target, args.schemas_dir)
        if ok:
            print(f"OK    {rel}")
        else:
            all_ok = False
            print(f"FAIL  {rel}")
            for e in errors:
                print(e)

    print()
    if all_ok:
        print("All files validate clean.")
        return 0
    print("Validation failed. See errors above.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
