#!/usr/bin/env python3
"""Create a read-only recursive inventory of the local FPM evidence tree."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

from check_evidence import check_tree, sha256_file


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "LAB" / "EVIDENCE"


def inventory(evidence: Path) -> dict[str, object]:
    records: list[dict[str, object]] = []
    extensions: Counter[str] = Counter()
    by_hash: dict[str, list[str]] = defaultdict(list)
    header_mismatches: list[dict[str, str]] = []
    symlinks: list[str] = []
    for path in sorted(evidence.rglob("*")):
        relative = path.relative_to(evidence).as_posix()
        if path.is_symlink():
            symlinks.append(relative)
            records.append({"path": relative, "type": "symlink", "target": str(path.readlink())})
        elif path.is_dir():
            records.append({"path": relative, "type": "directory"})
        elif path.is_file():
            digest = sha256_file(path)
            size = path.stat().st_size
            suffix = path.suffix.lower() or "[none]"
            extensions[suffix] += 1
            by_hash[digest].append(relative)
            records.append({"path": relative, "type": "file", "bytes": size, "sha256": digest})
            if path.suffix.lower() == ".dat":
                try:
                    first = path.open("r", encoding="utf-8", errors="replace").readline().strip()
                except OSError:
                    first = ""
                mission_dir = relative.split("/", 1)[0]
                if "MISSION-E003" in first and mission_dir != "E003":
                    header_mismatches.append({"path": relative, "declared": "MISSION-E003", "directory": mission_dir})
    duplicates = [
        {"sha256": digest, "paths": paths}
        for digest, paths in sorted(by_hash.items()) if len(paths) > 1
    ]
    checks = check_tree(evidence)
    largest = sorted(
        (item for item in records if item["type"] == "file"),
        key=lambda item: int(item["bytes"]), reverse=True,
    )[:20]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "root": str(evidence.resolve()),
        "read_only_operation": True,
        "summary": {
            "top_level_directories": sum(1 for path in evidence.iterdir() if path.is_dir()),
            "sealed_directories": sum(1 for item in checks if item.status.startswith("SEALED_")),
            "sealed_valid": sum(1 for item in checks if item.status == "SEALED_VALID"),
            "sealed_contaminated": sum(1 for item in checks if item.status == "SEALED_CONTAMINATED"),
            "sealed_corrupt": sum(1 for item in checks if item.status == "SEALED_CORRUPT"),
            "unsealed": sum(1 for item in checks if item.status == "UNSEALED"),
            "files": sum(1 for item in records if item["type"] == "file"),
            "bytes": sum(int(item["bytes"]) for item in records if item["type"] == "file"),
            "symlinks": len(symlinks),
            "mission_header_mismatches": len(header_mismatches),
        },
        "coverage": [{"directory": item.directory, "status": item.status,
                      "missing": item.missing, "extra": item.extra,
                      "hash_mismatches": item.hash_mismatches} for item in checks],
        "extension_counts": dict(sorted(extensions.items())),
        "header_mismatches": header_mismatches,
        "duplicates": duplicates,
        "largest_files": largest,
        "symlinks": symlinks,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=EVIDENCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(inventory(args.evidence), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

