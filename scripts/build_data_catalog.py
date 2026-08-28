#!/usr/bin/env python3
"""Build and validate the FPM claim-to-data catalog without promoting claims."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from check_evidence import check_tree


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "LAB" / "EVIDENCE"
METADATA = ROOT / "scripts" / "data_catalog_metadata.json"
OUTPUT = ROOT / "LAB" / "DATA-CATALOG.json"


def release_for(name: str) -> list[str]:
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "LAB" / "RELEASES").glob(f"RELEASE-{name}*.md")
    )


def mission_for(name: str) -> list[str]:
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "LAB" / "MISSIONS").glob(f"MISSION-{name}*.md")
    )


def validate_metadata(metadata: dict[str, object], evidence_names: set[str]) -> list[str]:
    errors: list[str] = []
    entries = metadata.get("entries", {})
    if not isinstance(entries, dict):
        return ["metadata entries must be an object"]
    for name, item in entries.items():
        if name not in evidence_names:
            errors.append(f"metadata points to missing evidence directory: {name}")
        if not isinstance(item, dict):
            errors.append(f"metadata {name} must be an object")
            continue
        for claim in item.get("claims", []):
            authority = ROOT / claim.get("authority", "")
            if not authority.is_file():
                errors.append(f"{name} claim {claim.get('id')} has missing authority")
            if claim.get("relation") == "ACCEPTED" and not str(claim.get("id", "")).startswith("C-"):
                errors.append(f"{name} attempted accepted claim promotion without canonical id")
    return errors


def build() -> tuple[dict[str, object], list[str]]:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    checks = check_tree(EVIDENCE)
    evidence_names = {item.directory for item in checks}
    errors = validate_metadata(metadata, evidence_names)
    curated = metadata["entries"]
    entries: list[dict[str, object]] = []
    for item in checks:
        directory = EVIDENCE / item.directory
        meta = curated.get(item.directory, {})
        entries.append({
            "mission_id": f"MISSION-{item.directory}",
            "evidence_path": directory.relative_to(ROOT).as_posix(),
            "seal_status": item.status,
            "manifest_entries": item.manifest_entries,
            "actual_files": item.actual_files,
            "bytes": item.bytes,
            "gate": meta.get("gate", "NOT_APPLICABLE" if item.status == "UNSEALED" else "UNKNOWN"),
            "claims": meta.get("claims", []),
            "schemas": [],
            "access": "LOCAL_FULL_PUBLIC_LIGHTWEIGHT",
            "retention": meta.get("retention", "UNDECIDED"),
            "missions": mission_for(item.directory),
            "releases": release_for(item.directory),
            "integrity_findings": {
                "missing": item.missing,
                "extra": item.extra,
                "hash_mismatches": item.hash_mismatches,
            },
        })
    source_fingerprint = hashlib.sha256(
        json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ({
        "schema_version": 1,
        "source_fingerprint_sha256": source_fingerprint,
        "authority_note": "Index only; mission, release, writeback and sealed manifest prevail on conflict.",
        "claim_promotion": "FORBIDDEN_WITHOUT_WRITEBACK",
        "entries": entries,
    }, errors)


def validate_public_snapshot() -> tuple[int, list[str]]:
    """Validate the full catalog without requiring deliberately omitted evidence."""
    errors: list[str] = []
    try:
        payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return 0, [f"invalid or missing public catalog: {exc}"]

    entries = payload.get("entries")
    if not isinstance(entries, list):
        return 0, ["public catalog entries must be an array"]
    expected_fingerprint = hashlib.sha256(
        json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if payload.get("source_fingerprint_sha256") != expected_fingerprint:
        errors.append("public catalog source fingerprint mismatch")

    names: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("public catalog entry must be an object")
            continue
        mission_id = entry.get("mission_id", "")
        if not isinstance(mission_id, str) or not mission_id.startswith("MISSION-"):
            errors.append(f"invalid mission id in public catalog: {mission_id!r}")
            continue
        name = mission_id.removeprefix("MISSION-")
        if name in names:
            errors.append(f"duplicate public catalog entry: {name}")
        names.add(name)
        if entry.get("evidence_path") != f"LAB/EVIDENCE/{name}":
            errors.append(f"invalid evidence path in public catalog: {name}")

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    errors.extend(validate_metadata(metadata, names))
    curated_names = set(metadata.get("entries", {}))
    for name in sorted(names - curated_names - {"LAB"}):
        errors.append(f"public catalog entry lacks curated metadata: {name}")
    for item in check_tree(EVIDENCE):
        if item.directory not in names:
            errors.append(f"published evidence directory absent from catalog: {item.directory}")
    return len(entries), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-public", action="store_true")
    args = parser.parse_args()
    if args.check and args.check_public:
        parser.error("--check and --check-public are mutually exclusive")
    if args.check_public:
        count, errors = validate_public_snapshot()
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"OK: {count} public catalog entries validated")
        return 0
    payload, errors = build()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale or missing catalog: {args.output}", file=sys.stderr)
            return 1
    else:
        args.output.write_text(rendered, encoding="utf-8")
    print(f"OK: {len(payload['entries'])} evidence entries cataloged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
