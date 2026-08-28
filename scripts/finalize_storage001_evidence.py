#!/usr/bin/env python3
"""Create the functional manifest for completed STORAGE-001 evidence before sealing."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import mimetypes
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "LAB" / "EVIDENCE" / "STORAGE-001"
OUTPUT = TARGET / "EVIDENCE-MANIFEST.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def role(path: Path) -> str:
    name = path.name
    if name == "AI-PROVENANCE.json" or "MANIFEST" in name or "MATRIX" in name or name in {
        "BASELINE-INVENTORY.json", "PACKAGE-INDEX.json", "COPY-AUDIT.json",
        "DEACCESSION-CANDIDATES.json", "GATE-RESULTS.json",
    }:
        return "METADATA"
    if "RESULTS" in name or "RECEIPT" in path.parts:
        return "LOG"
    return "METADATA"


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit("EVIDENCE-MANIFEST.json already exists")
    resources = []
    for path in sorted(p for p in TARGET.rglob("*") if p.is_file()):
        relative = path.relative_to(TARGET).as_posix()
        resources.append({
            "path": relative,
            "role": role(path),
            "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "generated_by": "scripts/run_storage001.py" if path.name != "AI-PROVENANCE.json" else "Codex before execution",
            "supports_criterion": ["SC-0", "SC-1", "SC-2", "SC-3", "SC-4", "SC-5", "SC-6", "SC-7", "SC-8", "SC-9"] if path.name == "GATE-RESULTS.json" else [],
        })
    manifest = {
        "schema_version": 1,
        "mission_id": "MISSION-STORAGE-001",
        "title": "Non-destructive storage appraisal, temporary cold packages and restoration evidence",
        "operational_state": "COLD_COPY_ONLY",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "resources": resources,
        "access": "LOCAL; volumetric packages and restored tree are temporary under /tmp/fpm-storage-001-20260828",
        "rights": "UNDECIDED",
        "retention": "PRESERVE",
        "expected_outputs": [{"path": row["path"], "status": "PRODUCED"} for row in resources],
        "links": {
            "mission": "LAB/MISSIONS/MISSION-STORAGE-001.md",
            "authorization": "LAB/DECISIONS/WRITEBACK-038.md",
            "ai_provenance": "AI-PROVENANCE.json",
            "release": "LAB/RELEASES/RELEASE-STORAGE-001.md"
        },
        "limits": [
            "SC-4 UNEVALUATED because packaging and validation share the same Codex lineage",
            "SC-6 UNEVALUATED because no second failure-independent copy was authorized",
            "ST-6 and every removal remain not authorized",
            "temporary packages are not a preservation destination"
        ]
    }
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(OUTPUT, flags, 0o444)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
