#!/usr/bin/env python3
"""Recursive, Git-independent integrity checker for FPM evidence directories."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from typing import Iterable

from validate_metadata import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = ROOT / "LAB" / "EVIDENCE"
BASELINE = ROOT / "scripts" / "ai_provenance_baseline.txt"
HASH_LINE = re.compile(r"^([0-9a-fA-F]{64})  (.+)$")
TRANSIENT_NAMES = {"__pycache__", ".DS_Store"}
TRANSIENT_SUFFIXES = (".pyc", ".pyo", ".tmp", ".swp", ".swo", "~")


@dataclass
class DirectoryResult:
    directory: str
    status: str
    manifest_entries: int = 0
    actual_files: int = 0
    bytes: int = 0
    missing: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)
    hash_mismatches: list[str] = field(default_factory=list)
    unsafe_paths: list[str] = field(default_factory=list)
    duplicate_entries: list[str] = field(default_factory=list)
    symlinks: list[str] = field(default_factory=list)
    transient: list[str] = field(default_factory=list)
    metadata_errors: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return self.status == "SEALED_VALID"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def baseline_names(path: Path = BASELINE) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def is_safe_relative(name: str) -> bool:
    posix = PurePosixPath(name)
    return bool(name) and not posix.is_absolute() and ".." not in posix.parts and "" not in posix.parts


def is_transient(name: str) -> bool:
    path = PurePosixPath(name)
    return any(part in TRANSIENT_NAMES for part in path.parts) or name.endswith(TRANSIENT_SUFFIXES)


def parse_manifest(path: Path) -> tuple[dict[str, str], list[str], list[str], list[str]]:
    entries: dict[str, str] = {}
    invalid: list[str] = []
    unsafe: list[str] = []
    duplicates: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return {}, [f"manifest unreadable: {exc}"], [], []
    for line_number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = HASH_LINE.fullmatch(line)
        if not match:
            invalid.append(f"line {line_number}")
            continue
        digest, name = match.groups()
        if not is_safe_relative(name):
            unsafe.append(name)
            continue
        if name == "SHA256SUMS.txt":
            invalid.append(f"line {line_number}: self reference")
            continue
        if name in entries:
            duplicates.append(name)
            continue
        entries[name] = digest.lower()
    return entries, invalid, unsafe, duplicates


def validate_ai_provenance(path: Path) -> list[str]:
    required = {
        "schema_version", "mission_id", "created_at", "ai_involvement", "research_stages",
        "systems", "persistent_context", "executable_actions", "retrieval_sources",
        "human_checkpoints", "validation_layers", "independence_limits", "known_limits",
        "disclosure_summary",
    }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"AI-PROVENANCE.json invalid: {exc}"]
    if not isinstance(payload, dict):
        return ["AI-PROVENANCE.json root is not an object"]
    errors = [f"AI-PROVENANCE.json missing {key}" for key in sorted(required - payload.keys())]
    if payload.get("schema_version") != 1:
        errors.append("AI-PROVENANCE.json unsupported schema_version")
    return errors


def _actual_files(directory: Path) -> tuple[set[str], list[str], list[str], int]:
    files: set[str] = set()
    symlinks: list[str] = []
    transient: list[str] = []
    total_bytes = 0
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory).as_posix()
        if path.is_symlink():
            symlinks.append(relative)
            files.add(relative)
            continue
        if path.is_file() and relative != "SHA256SUMS.txt":
            files.add(relative)
            total_bytes += path.stat().st_size
            if is_transient(relative):
                transient.append(relative)
    return files, symlinks, transient, total_bytes


def check_directory(directory: Path, baseline: set[str] | None = None) -> DirectoryResult:
    baseline = baseline_names() if baseline is None else baseline
    actual, symlinks, transient, total_bytes = _actual_files(directory)
    result = DirectoryResult(
        directory=directory.name,
        status="UNSEALED",
        actual_files=len(actual),
        bytes=total_bytes,
        symlinks=symlinks,
        transient=transient,
    )
    manifest = directory / "SHA256SUMS.txt"
    if not manifest.is_file():
        if directory.name not in baseline and "AI-PROVENANCE.json" not in actual:
            result.metadata_errors.append("AI-PROVENANCE.json missing in new directory")
        return result

    entries, invalid, unsafe, duplicates = parse_manifest(manifest)
    result.manifest_entries = len(entries)
    result.unsafe_paths = unsafe
    result.duplicate_entries = duplicates
    result.metadata_errors.extend(f"invalid SHA256SUMS: {item}" for item in invalid)
    expected = set(entries)
    result.missing = sorted(expected - actual)
    result.extra = sorted(actual - expected)

    for name in sorted(expected & actual):
        candidate = directory / name
        if candidate.is_symlink() or not candidate.is_file():
            continue
        if sha256_file(candidate) != entries[name]:
            result.hash_mismatches.append(name)

    provenance = directory / "AI-PROVENANCE.json"
    if directory.name not in baseline and not provenance.is_file():
        result.metadata_errors.append("AI-PROVENANCE.json missing in new sealed directory")
    elif provenance.is_file():
        result.metadata_errors.extend(validate_ai_provenance(provenance))
    functional = directory / "EVIDENCE-MANIFEST.json"
    if directory.name not in baseline and not functional.is_file():
        result.metadata_errors.append("EVIDENCE-MANIFEST.json missing in new sealed directory")
    elif functional.is_file():
        try:
            functional_payload = json.loads(functional.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            result.metadata_errors.append(f"EVIDENCE-MANIFEST.json invalid: {exc}")
        else:
            result.metadata_errors.extend(
                f"EVIDENCE-MANIFEST.json: {error}" for error in validate_manifest(functional_payload)
            )

    corrupt = bool(
        result.missing or result.hash_mismatches or result.unsafe_paths or result.duplicate_entries
        or result.symlinks or result.metadata_errors or invalid
    )
    policy_corrupt = any(name in expected for name in transient)
    if corrupt or policy_corrupt:
        result.status = "SEALED_CORRUPT"
    elif result.extra or result.transient:
        result.status = "SEALED_CONTAMINATED"
    else:
        result.status = "SEALED_VALID"
    return result


def check_tree(evidence: Path = DEFAULT_EVIDENCE) -> list[DirectoryResult]:
    baseline = baseline_names()
    if not evidence.is_dir():
        return []
    return [check_directory(path, baseline) for path in sorted(evidence.iterdir()) if path.is_dir()]


def summary(results: Iterable[DirectoryResult]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return counts


def self_test() -> bool:
    with tempfile.TemporaryDirectory(prefix="fpm-evidence-selftest-", dir="/tmp") as temporary:
        directory = Path(temporary) / "FIXTURE"
        directory.mkdir()
        payload = directory / "data.txt"
        payload.write_text("fixture\n", encoding="utf-8")
        digest = sha256_file(payload)
        (directory / "SHA256SUMS.txt").write_text(f"{digest}  data.txt\n", encoding="utf-8")
        clean = check_directory(directory, {"FIXTURE"}).status == "SEALED_VALID"
        nested = directory / "nested"
        nested.mkdir()
        (nested / "extra.txt").write_text("extra\n", encoding="utf-8")
        contaminated = check_directory(directory, {"FIXTURE"}).status == "SEALED_CONTAMINATED"
        payload.write_text("changed\n", encoding="utf-8")
        corrupt = check_directory(directory, {"FIXTURE"}).status == "SEALED_CORRUPT"
        return clean and contaminated and corrupt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", nargs="?", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        passed = self_test()
        print("OK: recursive checker rejects contamination and corruption" if passed else "FAIL: recursive checker self-test")
        return 0 if passed else 1
    evidence = args.evidence.resolve()
    results = check_tree(evidence)
    counts = summary(results)
    if args.as_json:
        print(json.dumps({"root": str(evidence), "summary": counts,
                          "directories": [asdict(item) for item in results]}, indent=2, sort_keys=True))
    else:
        for item in results:
            details = []
            for label in ("missing", "extra", "hash_mismatches", "unsafe_paths",
                          "duplicate_entries", "symlinks", "transient", "metadata_errors"):
                values = getattr(item, label)
                if values:
                    details.append(f"{label}={','.join(values)}")
            suffix = f" ({'; '.join(details)})" if details else ""
            print(f"{item.status:20} {item.directory}{suffix}")
        print("SUMMARY " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    return 0 if results and all(item.clean for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
