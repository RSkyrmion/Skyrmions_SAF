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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
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
