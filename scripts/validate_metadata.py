#!/usr/bin/env python3
"""Dependency-free semantic validation for FPM manifests and run receipts."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import re
import sys


SHA = re.compile(r"^[0-9a-f]{64}$")
ROLES = {"INPUT", "SOURCE", "RAW", "DERIVED", "LOG", "CODE", "BINARY", "FIGURE_TARGET", "METADATA"}
RETENTION = {"PRESERVE", "REGENERABLE", "TRANSIENT", "EXTERNAL", "RESTRICTED"}


def date_time(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_manifest(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["root must be an object"]
    required = {"schema_version", "mission_id", "title", "operational_state", "created_at",
                "resources", "access", "rights", "retention"}
    errors = [f"missing {item}" for item in sorted(required - payload.keys())]
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not date_time(payload.get("created_at")):
        errors.append("created_at must be RFC 3339")
    if payload.get("retention") not in RETENTION:
        errors.append("invalid retention")
    resources = payload.get("resources")
    if not isinstance(resources, list):
        errors.append("resources must be an array")
        return errors
    seen: set[str] = set()
    for index, resource in enumerate(resources):
        prefix = f"resources[{index}]"
        if not isinstance(resource, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in ("path", "role", "media_type", "bytes", "sha256", "generated_by"):
            if key not in resource:
                errors.append(f"{prefix} missing {key}")
        name = resource.get("path")
        if isinstance(name, str):
            parts = PurePosixPath(name)
            if parts.is_absolute() or ".." in parts.parts:
                errors.append(f"{prefix} unsafe path")
            if name in seen:
                errors.append(f"{prefix} duplicate path")
            seen.add(name)
        if resource.get("role") not in ROLES:
            errors.append(f"{prefix} invalid role")
        if not isinstance(resource.get("bytes"), int) or resource.get("bytes", -1) < 0:
            errors.append(f"{prefix} invalid bytes")
        if not isinstance(resource.get("sha256"), str) or not SHA.fullmatch(resource.get("sha256", "")):
            errors.append(f"{prefix} invalid sha256")
    expected = payload.get("expected_outputs", [])
    if not isinstance(expected, list):
        errors.append("expected_outputs must be an array")
    else:
        for index, item in enumerate(expected):
            if not isinstance(item, dict) or item.get("status") not in {"PRODUCED", "ABSENT"}:
                errors.append(f"expected_outputs[{index}] invalid status")
            elif item.get("status") == "ABSENT" and not item.get("reason"):
                errors.append(f"expected_outputs[{index}] absent without reason")
    return errors


def validate_receipt(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["root must be an object"]
    required = {"schema_version", "mission_id", "run_id", "command", "cwd", "started_at",
                "finished_at", "duration_seconds", "exit_code", "timeout_seconds", "state",
                "environment", "parameters", "determinism", "inputs", "outputs", "executor"}
    errors = [f"missing {item}" for item in sorted(required - payload.keys())]
    state = payload.get("state")
    if state not in {"RUNNING", "COMPLETE", "FAILED", "INTERRUPTED"}:
        errors.append("invalid state")
    if not isinstance(payload.get("command"), list) or not payload.get("command"):
        errors.append("command must be a non-empty array")
    if not date_time(payload.get("started_at")):
        errors.append("started_at must be RFC 3339")
    if state != "RUNNING" and not date_time(payload.get("finished_at")):
        errors.append("finished_at required for final state")
    duration = payload.get("duration_seconds")
    if state != "RUNNING" and (not isinstance(duration, (int, float)) or duration < 0):
        errors.append("non-negative duration required for final state")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("manifest", "receipt"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    errors = validate_manifest(payload) if args.kind == "manifest" else validate_receipt(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.path} validates as {args.kind}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

