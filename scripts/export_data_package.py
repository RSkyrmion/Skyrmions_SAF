#!/usr/bin/env python3
"""Create and validate local-only RO-Crate, BagIt and DataCite draft exports."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_output(path: Path) -> bool:
    try:
        path.resolve().relative_to(Path("/tmp").resolve())
        return True
    except ValueError:
        return False


def tag_manifest(root: Path) -> str:
    names = ["bag-info.txt", "bagit.txt", "manifest-sha256.txt", "ro-crate-metadata.json", "datacite-draft.json"]
    return "".join(f"{sha256(root / name)}  {name}\n" for name in names)


def create(source: Path, output: Path, mission_id: str, title: str) -> None:
    if not safe_output(output):
        raise ValueError("export output must be inside /tmp")
    if output.exists():
        raise FileExistsError("output already exists")
    if not source.is_dir():
        raise ValueError("source must be a directory")
    data = output / "data"
    shutil.copytree(source, data, symlinks=False)
    payload_files = sorted(path for path in data.rglob("*") if path.is_file())
    output.mkdir(parents=True, exist_ok=True)
    (output / "bagit.txt").write_text("BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n", encoding="utf-8")
    (output / "bag-info.txt").write_text(
        f"Source-Organization: SAF-Skyrmion FPM\nExternal-Identifier: {mission_id}\n"
        f"Bagging-Date: {datetime.now(timezone.utc).date().isoformat()}\nPayload-Oxum: "
        f"{sum(path.stat().st_size for path in payload_files)}.{len(payload_files)}\n", encoding="utf-8")
    (output / "manifest-sha256.txt").write_text(
        "".join(f"{sha256(path)}  {path.relative_to(output).as_posix()}\n" for path in payload_files), encoding="utf-8")
    graph: list[dict[str, object]] = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork", "about": {"@id": "./"}, "conformsTo": {"@id": "https://w3id.org/ro/crate/1.3"}},
        {"@id": "./", "@type": "Dataset", "name": title, "identifier": mission_id,
         "hasPart": [{"@id": path.relative_to(output).as_posix()} for path in payload_files]},
    ]
    graph.extend({"@id": path.relative_to(output).as_posix(), "@type": "File",
                  "contentSize": path.stat().st_size, "sha256": sha256(path)} for path in payload_files)
    (output / "ro-crate-metadata.json").write_text(
        json.dumps({"@context": "https://w3id.org/ro/crate/1.3/context", "@graph": graph}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    datacite = {
        "schemaVersion": "http://datacite.org/schema/kernel-4",
        "state": "DRAFT_LOCAL_ONLY",
        "identifiers": [],
        "creators": [{"name": "UNDECIDED"}],
        "titles": [{"title": title}],
        "publisher": "UNDECIDED",
        "publicationYear": datetime.now(timezone.utc).year,
        "types": {"resourceTypeGeneral": "Dataset"},
        "version": "DATA-001-draft",
        "rightsList": [{"rights": "UNDECIDED"}],
        "relatedIdentifiers": [{"relatedIdentifier": mission_id, "relatedIdentifierType": "Other", "relationType": "IsDocumentedBy"}],
    }
    (output / "datacite-draft.json").write_text(json.dumps(datacite, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "tagmanifest-sha256.txt").write_text(tag_manifest(output), encoding="utf-8")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    required = {"bagit.txt", "bag-info.txt", "manifest-sha256.txt", "tagmanifest-sha256.txt", "ro-crate-metadata.json", "datacite-draft.json"}
    missing = sorted(name for name in required if not (root / name).is_file())
    errors.extend(f"missing {name}" for name in missing)
    for manifest_name in ("manifest-sha256.txt", "tagmanifest-sha256.txt"):
        path = root / manifest_name
        if not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                expected, name = line.split("  ", 1)
                candidate = root / name
            except ValueError:
                errors.append(f"{manifest_name}:{line_number} malformed")
                continue
            if not candidate.is_file() or sha256(candidate) != expected:
                errors.append(f"{manifest_name}:{line_number} hash mismatch")
    try:
        crate = json.loads((root / "ro-crate-metadata.json").read_text(encoding="utf-8"))
        if crate.get("@context") != "https://w3id.org/ro/crate/1.3/context" or not crate.get("@graph"):
            errors.append("invalid RO-Crate 1.3 metadata")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid RO-Crate JSON: {exc}")
    try:
        datacite = json.loads((root / "datacite-draft.json").read_text(encoding="utf-8"))
        if datacite.get("state") != "DRAFT_LOCAL_ONLY" or datacite.get("identifiers"):
            errors.append("DataCite draft must remain local and identifier-free")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid DataCite JSON: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    create_parser = sub.add_parser("create")
    create_parser.add_argument("source", type=Path)
    create_parser.add_argument("output", type=Path)
    create_parser.add_argument("--mission", required=True)
    create_parser.add_argument("--title", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "create":
            create(args.source, args.output, args.mission, args.title)
            target = args.output
        else:
            target = args.output
        errors = validate(target)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: local package validates at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

