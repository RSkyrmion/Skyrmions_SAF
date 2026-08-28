#!/usr/bin/env python3
"""Validate FPM tabular files against compact, reusable schemas."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "scripts" / "schemas"
NULLS = {"", "NA", "N/A", "NULL", "null", "."}


def convert(value: str, field: dict[str, object]) -> object:
    if value in NULLS:
        if field.get("nullable"):
            return None
        raise ValueError("null in non-nullable field")
    kind = field["type"]
    if kind == "integer":
        parsed: object = int(value)
    elif kind == "number":
        parsed = float(value)
        if field.get("finite") and not math.isfinite(parsed):
            raise ValueError("non-finite number")
    else:
        parsed = value
    enum = field.get("enum")
    if enum is not None and parsed not in enum:
        raise ValueError(f"value {parsed!r} outside enum")
    if isinstance(parsed, (int, float)) and parsed is not None:
        if "minimum" in field and parsed < field["minimum"]:
            raise ValueError(f"value {parsed} below minimum")
        if "maximum" in field and parsed > field["maximum"]:
            raise ValueError(f"value {parsed} above maximum")
    return parsed


def validate(path: Path, schema_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [str(exc)]
    fields = schema.get("fields", [])
    if not fields:
        return ["schema has no fields"]
    schema_header: str | None = None
    units_header: list[str] | None = None
    rows: list[tuple[int, list[str]]] = []
    delimiter = schema.get("delimiter", "whitespace")
    for line_number, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            payload = stripped[1:].strip()
            if payload.lower().startswith("schema:"):
                schema_header = payload.split(":", 1)[1].strip()
            elif payload.lower().startswith("units:"):
                units_header = payload.split(":", 1)[1].strip().split()
            continue
        if delimiter == "tab":
            values = raw.rstrip("\n").split("\t")
        elif delimiter == "comma":
            values = [item.strip() for item in raw.split(",")]
        else:
            values = stripped.split()
        rows.append((line_number, values))
    if schema_header != schema.get("name"):
        errors.append(f"schema header must be {schema.get('name')!r}")
    expected_units = [str(field.get("unit", "1")) for field in fields]
    if units_header != expected_units:
        errors.append(f"units header mismatch: expected {' '.join(expected_units)}")
    if not rows:
        errors.append("table has no data rows")
        return errors
    columns: list[list[object]] = [[] for _ in fields]
    for line_number, values in rows:
        if len(values) != len(fields):
            errors.append(f"line {line_number}: expected {len(fields)} columns, got {len(values)}")
            continue
        for index, (value, field) in enumerate(zip(values, fields)):
            try:
                columns[index].append(convert(value, field))
            except (TypeError, ValueError) as exc:
                errors.append(f"line {line_number}, {field.get('name')}: {exc}")
    for index, field in enumerate(fields):
        if field.get("monotonic") == "strict" and len(columns[index]) > 1:
            values = [value for value in columns[index] if value is not None]
            if any(right <= left for left, right in zip(values, values[1:])):
                errors.append(f"field {field.get('name')} is not strictly monotonic")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--schema", required=True)
    args = parser.parse_args(argv)
    schema_path = Path(args.schema)
    if not schema_path.exists():
        schema_path = SCHEMAS / f"{args.schema}.schema.json"
    errors = validate(args.path, schema_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.path} validates as {schema_path.stem.replace('.schema', '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

