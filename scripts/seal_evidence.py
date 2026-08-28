#!/usr/bin/env python3
"""Create a deterministic recursive SHA-256 seal for new FPM evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

from check_evidence import is_transient, sha256_file, validate_ai_provenance


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = (ROOT / "LAB" / "EVIDENCE").resolve()
SEAL_INDEX = ROOT / "LAB" / "EVIDENCE-SEALS.jsonl"


def inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def collect(directory: Path) -> tuple[list[tuple[str, str, int]], list[str]]:
    entries: list[tuple[str, str, int]] = []
    errors: list[str] = []
    for path in sorted(directory.rglob("*")):
        name = path.relative_to(directory).as_posix()
        if name == "SHA256SUMS.txt":
            continue
        if path.is_symlink():
            errors.append(f"symlink forbidden: {name}")
            continue
        if path.is_file():
            if is_transient(name):
                errors.append(f"transient artifact forbidden: {name}")
                continue
            before = path.stat()
            digest = sha256_file(path)
            after = path.stat()
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (
                after.st_size, after.st_mtime_ns, after.st_ino
            ):
                errors.append(f"file changed while hashing: {name}")
                continue
            entries.append((name, digest, after.st_size))
    return entries, errors


def validate_required_metadata(directory: Path) -> list[str]:
    errors: list[str] = []
    provenance = directory / "AI-PROVENANCE.json"
    if not provenance.is_file():
        errors.append("AI-PROVENANCE.json is required")
    else:
        errors.extend(validate_ai_provenance(provenance))
    manifest = directory / "EVIDENCE-MANIFEST.json"
    if not manifest.is_file():
        errors.append("EVIDENCE-MANIFEST.json is required")
    else:
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"EVIDENCE-MANIFEST.json invalid: {exc}")
        else:
            required = {"schema_version", "mission_id", "title", "operational_state",
                        "created_at", "resources", "access", "rights", "retention"}
            if not isinstance(payload, dict):
                errors.append("EVIDENCE-MANIFEST.json root must be an object")
            else:
                for key in sorted(required - payload.keys()):
                    errors.append(f"EVIDENCE-MANIFEST.json missing {key}")
    return errors


def seal(directory: Path, index: Path = SEAL_INDEX, make_read_only: bool = True,
         evidence_root: Path = EVIDENCE_ROOT) -> dict[str, object]:
    directory = directory.resolve()
    evidence_root = evidence_root.resolve()
    if not inside(directory, evidence_root) or directory.parent != evidence_root:
        raise ValueError("target must be one direct child of LAB/EVIDENCE")
    if not directory.is_dir():
        raise ValueError("target is not a directory")
    manifest = directory / "SHA256SUMS.txt"
    if manifest.exists():
        raise FileExistsError("SHA256SUMS.txt already exists; seals are never overwritten")
    errors = validate_required_metadata(directory)
    entries, collection_errors = collect(directory)
    errors.extend(collection_errors)
    if not entries:
        errors.append("empty evidence directory")
    if errors:
        raise ValueError("; ".join(errors))

    content = "".join(f"{digest}  {name}\n" for name, digest, _ in entries)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(manifest, flags, 0o444)
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    manifest_digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    try:
        directory_label = directory.relative_to(ROOT).as_posix()
    except ValueError:
        directory_label = directory.relative_to(evidence_root).as_posix()
    receipt = {
        "schema_version": 1,
        "sealed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "directory": directory_label,
        "files": len(entries),
        "bytes": sum(size for _, _, size in entries),
        "manifest_sha256": manifest_digest,
    }
    index.parent.mkdir(parents=True, exist_ok=True)
    with index.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
        stream.flush()
        os.fsync(stream.fileno())

    protection_errors: list[str] = []
    if make_read_only:
        for path in [p for p in directory.rglob("*") if p.is_file() and not p.is_symlink()]:
            try:
                path.chmod(path.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            except OSError as exc:
                protection_errors.append(f"{path.name}: {exc}")
    receipt["protection"] = "APPLIED" if not protection_errors else "FAILED_DECLARED"
    receipt["protection_errors"] = protection_errors
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--index", type=Path, default=SEAL_INDEX)
    parser.add_argument("--evidence-root", type=Path, default=EVIDENCE_ROOT)
    parser.add_argument("--no-read-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        receipt = seal(args.directory, args.index, not args.no_read_only, args.evidence_root)
    except (OSError, ValueError) as exc:
        print(f"seal refused: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
