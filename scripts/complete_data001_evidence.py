#!/usr/bin/env python3
"""Append the DATA-001 R1 evaluation without rewriting the preserved failed attempt."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import mimetypes
from pathlib import Path
import subprocess
import sys

from build_data_catalog import build as build_catalog
from check_evidence import check_tree
from inventory_evidence import inventory


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "LAB" / "EVIDENCE"
TARGET = EVIDENCE / "DATA-001"
NEW_NAMES = {
    "TEST-RESULTS-R1.txt", "CURRENT-INVENTORY-R1.json", "CURRENT-CHECK-R1.json",
    "CATALOG-SNAPSHOT-R1.json", "GATE-RESULTS-R1.json", "AI-PROVENANCE-ADDENDUM-001.json",
    "EVIDENCE-MANIFEST-ADDENDUM-001.json",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot_preexisting() -> dict[str, str]:
    return {
        path.relative_to(EVIDENCE).as_posix(): sha256(path)
        for path in sorted(EVIDENCE.rglob("*"))
        if path.is_file() and not path.is_symlink() and TARGET not in path.parents
    }


def write_new(name: str, content: str) -> Path:
    path = TARGET / name
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def main() -> int:
    if not TARGET.is_dir() or (TARGET / "SHA256SUMS.txt").exists():
        print("DATA-001 must exist and remain unsealed for R1", file=sys.stderr)
        return 1
    collisions = sorted(name for name in NEW_NAMES if (TARGET / name).exists())
    if collisions:
        print(f"refusing to overwrite R1 files: {', '.join(collisions)}", file=sys.stderr)
        return 1

    before = snapshot_preexisting()
    current_inventory = inventory(EVIDENCE)
    checks = check_tree(EVIDENCE)
    by_name = {item.directory: item for item in checks}
    expected_current = (
        len(checks) == 21
        and sum(item.status == "SEALED_VALID" for item in checks) == 15
        and sum(item.status == "SEALED_CONTAMINATED" for item in checks) == 2
        and sum(item.status == "SEALED_CORRUPT" for item in checks) == 2
        and sum(item.status == "UNSEALED" for item in checks) == 2
        and by_name["A003"].status == "SEALED_CONTAMINATED"
        and by_name["A005"].status == "SEALED_CONTAMINATED"
        and by_name["A005R"].status == "SEALED_CORRUPT"
        and by_name["A005R2"].status == "SEALED_CORRUPT"
        and by_name["DATA-001"].status == "UNSEALED"
        and by_name["LAB"].status == "UNSEALED"
        and len(by_name["A005R"].hash_mismatches) == 5
        and "ac0_piso.mx3" in by_name["A005R"].extra
        and current_inventory["summary"]["mission_header_mismatches"] == 35
    )
    if not expected_current:
        print("resume baseline changed again; R1 files were not created", file=sys.stderr)
        return 1

    tests = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "test_data_hygiene.py")],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    after = snapshot_preexisting()
    unchanged = before == after
    catalog, catalog_errors = build_catalog()
    state_text = (ROOT / "LAB" / "STATE.md").read_text(encoding="utf-8")

    check_payload = {
        "summary": {
            status: sum(item.status == status for item in checks)
            for status in ("SEALED_VALID", "SEALED_CONTAMINATED", "SEALED_CORRUPT", "UNSEALED")
        },
        "directories": [item.__dict__ for item in checks],
    }
    write_new("TEST-RESULTS-R1.txt", tests.stdout)
    write_new("CURRENT-INVENTORY-R1.json", json.dumps(current_inventory, indent=2, sort_keys=True) + "\n")
    write_new("CURRENT-CHECK-R1.json", json.dumps(check_payload, indent=2, sort_keys=True) + "\n")
    write_new("CATALOG-SNAPSHOT-R1.json", json.dumps(catalog, indent=2, sort_keys=True) + "\n")

    test_pass = tests.returncode == 0
    criteria = {
        "DA-0": expected_current,
        "DA-1": test_pass,
        "DA-2": test_pass,
        "DA-3": test_pass,
        "DA-4": test_pass,
        "DA-5": test_pass,
        "DA-6": not catalog_errors and len(catalog["entries"]) == 21,
        "DA-7": unchanged,
        "DA-8": test_pass,
        "DA-9": test_pass,
        "DA-10": "**Claims aceitos:** `C-1` a `C-15`" in state_text and "C-16" not in state_text,
    }
    gate = {
        "schema_version": 1,
        "mission_id": "MISSION-DATA-001",
        "revision": "R1",
        "evaluated_at": now(),
        "supersedes_for_gate": "GATE-RESULTS.json",
        "correction_reason": "DA-10 textual matcher did not account for Markdown markup; claims were unchanged.",
        "criteria": {key: "PASS" if value else "FAIL" for key, value in criteria.items()},
        "gate": "PASS" if all(criteria.values()) else "FAIL",
        "human_acceptance": "PENDING",
        "preexisting_evidence_unchanged_during_r1": unchanged,
        "concurrent_drift_preserved": ["A003/__pycache__/ovf.cpython-311.pyc", "A005R/RUN-LOG.txt", "A005R2/"],
        "historical_integrity": {
            "A003": "SEALED_CONTAMINATED", "A005": "SEALED_CONTAMINATED",
            "A005R": "SEALED_CORRUPT", "A005R2": "SEALED_CORRUPT", "LAB": "UNSEALED",
            "normalized": False,
        },
    }
    gate_path = write_new("GATE-RESULTS-R1.json", json.dumps(gate, indent=2, sort_keys=True) + "\n")

    provenance = {
        "schema_version": 1,
        "mission_id": "MISSION-DATA-001",
        "created_at": now(),
        "ai_involvement": "MATERIAL",
        "research_stages": ["RESUMPTION", "VALIDATION", "DOCUMENTATION"],
        "systems": [{"name": "Codex", "provider": "OpenAI", "version_or_access_date": "2026-08-28", "roles": ["EXECUTOR", "SELF_VALIDATOR"]}],
        "persistent_context": [{"path_or_identifier": "LAB/MISSIONS/MISSION-DATA-001-ADDENDUM-001.md", "integrity": "append-only"}],
        "executable_actions": [{"actor": "Codex", "action": "repeated gate after correcting only the DA-10 textual matcher", "artifact": gate_path.name}],
        "retrieval_sources": [],
        "human_checkpoints": [{"checkpoint": "RESUME_AUTHORIZED_WORK", "authority": "Rodrigo", "record": "LAB/DECISIONS/WRITEBACK-033.md"}],
        "validation_layers": [{"validator": "unittest fixtures and before/after SHA snapshot", "method": "self-validation in /tmp plus immutable preexisting evidence comparison", "independent_axes": ["synthetic fixtures", "SHA-256"], "shared_axes": ["implementation", "criteria interpretation"]}],
        "independence_limits": ["Same Codex executor and validator; no external validation."],
        "known_limits": ["Concurrent filesystem drift occurred between the original snapshot and resumption.", "A005R2 has no authorization record located by DATA-001.", "Historical contamination/corruption remains untouched."],
        "disclosure_summary": "Codex resumed DATA-001, preserved its first failed gate, documented concurrent filesystem drift, and repeated the corrected gate with before/after SHA protection."
    }
    provenance_path = write_new("AI-PROVENANCE-ADDENDUM-001.json", json.dumps(provenance, indent=2, sort_keys=True) + "\n")

    new_payloads = [
        TARGET / "TEST-RESULTS-R1.txt", TARGET / "CURRENT-INVENTORY-R1.json",
        TARGET / "CURRENT-CHECK-R1.json", TARGET / "CATALOG-SNAPSHOT-R1.json",
        gate_path, provenance_path,
    ]
    resources = [{
        "path": path.name,
        "role": "LOG" if path.suffix == ".txt" else "METADATA",
        "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "generated_by": "scripts/complete_data001_evidence.py",
        "supports_criterion": sorted(criteria) if path == gate_path else [],
    } for path in new_payloads]
    manifest_addendum = {
        "schema_version": 1,
        "mission_id": "MISSION-DATA-001",
        "title": "R1 append-only correction and resumption snapshot",
        "operational_state": "COMPLETE" if gate["gate"] == "PASS" else "FAILED",
        "created_at": now(),
        "supersedes": {"document": "EVIDENCE-MANIFEST.json", "scope": ["operational_state", "gate_pointer"]},
        "resources": resources,
        "access": "LOCAL; lightweight subset may be public",
        "rights": "UNDECIDED",
        "retention": "PRESERVE",
        "expected_outputs": [{"path": path.name, "status": "PRODUCED"} for path in new_payloads],
        "links": {
            "mission_addendum": "LAB/MISSIONS/MISSION-DATA-001-ADDENDUM-001.md",
            "technical_record": "LAB/DECISIONS/WRITEBACK-033.md",
            "gate": "GATE-RESULTS-R1.json",
            "ai_provenance": "AI-PROVENANCE-ADDENDUM-001.json"
        }
    }
    write_new("EVIDENCE-MANIFEST-ADDENDUM-001.json", json.dumps(manifest_addendum, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"gate": gate["gate"], "criteria": gate["criteria"], "preexisting_unchanged": unchanged}, sort_keys=True))
    return 0 if gate["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
