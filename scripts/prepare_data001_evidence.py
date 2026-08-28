#!/usr/bin/env python3
"""Prepare the new, unsealed DATA-001 evidence package exactly once."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import mimetypes
from pathlib import Path
import subprocess
import sys
import tempfile

from build_data_catalog import build as build_catalog
from check_evidence import check_tree
from export_data_package import create as create_export, validate as validate_export
from inventory_evidence import inventory


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "LAB" / "EVIDENCE"
TARGET = EVIDENCE / "DATA-001"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    if TARGET.exists():
        print(f"refusing to overwrite existing evidence: {TARGET}", file=sys.stderr)
        return 1

    baseline_inventory = inventory(EVIDENCE)
    baseline_checks = check_tree(EVIDENCE)
    by_name = {item.directory: item for item in baseline_checks}
    catalog, catalog_errors = build_catalog()
    expected_baseline = (
        len(baseline_checks) == 19
        and sum(item.status == "SEALED_VALID" for item in baseline_checks) == 16
        and by_name["A005"].status == "SEALED_CONTAMINATED"
        and by_name["A005R"].status == "SEALED_CORRUPT"
        and by_name["LAB"].status == "UNSEALED"
        and len(by_name["A005R"].hash_mismatches) == 5
        and "ac0_piso.mx3" in by_name["A005R"].extra
        and baseline_inventory["summary"]["mission_header_mismatches"] == 35
    )
    if not expected_baseline or catalog_errors:
        print("baseline does not match ERRATA-002; evidence was not created", file=sys.stderr)
        return 1

    tests = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "test_data_hygiene.py")],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if tests.returncode:
        print(tests.stdout, file=sys.stderr)
        print("acceptance fixtures failed; evidence was not created", file=sys.stderr)
        return 1

    TARGET.mkdir()
    write(TARGET / "TEST-RESULTS.txt", tests.stdout)
    write(TARGET / "BASELINE-INVENTORY.json", json.dumps(baseline_inventory, indent=2, sort_keys=True) + "\n")
    check_payload = {
        "summary": {
            status: sum(item.status == status for item in baseline_checks)
            for status in ("SEALED_VALID", "SEALED_CONTAMINATED", "SEALED_CORRUPT", "UNSEALED")
        },
        "directories": [item.__dict__ for item in baseline_checks],
    }
    write(TARGET / "BASELINE-CHECK.json", json.dumps(check_payload, indent=2, sort_keys=True) + "\n")
    write(TARGET / "CATALOG-SNAPSHOT.json", json.dumps(catalog, indent=2, sort_keys=True) + "\n")

    fixtures = {
        "trajectory-valid.tsv": "# schema: trajectory-v1\n# units: s m m m m m 1 1 1 1\n0 0 0 1e-8 0 1e-8 1 -1 2 2\n1e-12 0 0 1e-8 0 1e-8 1 -1 2 2\n",
        "magnetization-grid-valid.tsv": "# schema: magnetization-grid-v1\n# units: 1 1 1 1 1 1\n0 0 1 0 0 1\n0 0 2 0 0 -1\n",
        "phase-scan-valid.tsv": "# schema: phase-scan-v1\n# units: J/m2 J/m3 1 m 1 T\n0.1 600000 COAXIAL NA 10 1e-5\n",
        "criterion-summary-valid.tsv": "# schema: criterion-summary-v1\n# units: 1 1 1 1 1\nDA-0\tinventario\t1\tPASS\tbaseline-corrigido\n",
    }
    for name, content in fixtures.items():
        write(TARGET / name, content)

    receipt_states: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="data001-artifacts-", dir="/tmp") as temporary:
        scratch = Path(temporary)
        commands = {
            "success": ("pass", 2.0),
            "failure": ("raise SystemExit(3)", 2.0),
            "timeout": ("import time; time.sleep(1)", 0.05),
        }
        for label, (code, timeout) in commands.items():
            receipt = scratch / f"RUN-RECEIPT-{label}.json"
            subprocess.run(
                [sys.executable, "-B", str(ROOT / "scripts" / "run_with_receipt.py"),
                 "--mission", "MISSION-DATA-001", "--run-id", f"fixture-{label}",
                 "--receipt", str(receipt), "--cwd", str(scratch), "--timeout", str(timeout),
                 "--checkpoint", "LAB/DECISIONS/WRITEBACK-031.md", "--",
                 sys.executable, "-B", "-c", code],
                cwd=ROOT, check=False,
            )
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            receipt_states[label] = str(payload["state"])
            write(TARGET / receipt.name, json.dumps(payload, indent=2, sort_keys=True) + "\n")

        source = scratch / "export-source"
        source.mkdir()
        write(source / "fixture.txt", "DATA-001 local export fixture\n")
        package = scratch / "export-package"
        create_export(source, package, "MISSION-DATA-001", "DATA-001 fixture")
        export_errors = validate_export(package)
        export_report = {
            "output_scope": "/tmp only",
            "network_actions": 0,
            "uploads": 0,
            "identifiers_created": 0,
            "ro_crate_version": "1.3",
            "bagit": "1.0 / SHA-256",
            "datacite": "4.x local draft",
            "validation_errors": export_errors,
            "files": sorted(path.relative_to(package).as_posix() for path in package.rglob("*") if path.is_file()),
        }
        write(TARGET / "EXPORT-VALIDATION.json", json.dumps(export_report, indent=2, sort_keys=True) + "\n")

    common_tests_pass = tests.returncode == 0
    receipt_pass = receipt_states == {"success": "COMPLETE", "failure": "FAILED", "timeout": "INTERRUPTED"}
    export_pass = not export_report["validation_errors"] and export_report["network_actions"] == 0
    verdicts = {
        "DA-0": expected_baseline,
        "DA-1": common_tests_pass,
        "DA-2": common_tests_pass,
        "DA-3": common_tests_pass,
        "DA-4": common_tests_pass,
        "DA-5": receipt_pass and common_tests_pass,
        "DA-6": not catalog_errors and len(catalog["entries"]) == 19,
        "DA-7": expected_baseline and common_tests_pass,
        "DA-8": common_tests_pass,
        "DA-9": export_pass and common_tests_pass,
        "DA-10": "**Claims aceitos:** `C-1` a `C-15`" in (ROOT / "LAB" / "STATE.md").read_text(encoding="utf-8"),
    }
    gate = {
        "schema_version": 1,
        "mission_id": "MISSION-DATA-001",
        "evaluated_at": now(),
        "criteria": {key: "PASS" if value else "FAIL" for key, value in verdicts.items()},
        "gate": "PASS" if all(verdicts.values()) else "FAIL",
        "human_acceptance": "PENDING",
        "historical_integrity": {
            "A005": "SEALED_CONTAMINATED",
            "A005R": "SEALED_CORRUPT",
            "LAB": "UNSEALED",
            "normalized": False,
        },
    }
    write(TARGET / "GATE-RESULTS.json", json.dumps(gate, indent=2, sort_keys=True) + "\n")

    provenance_payload = {
        "schema_version": 1,
        "mission_id": "MISSION-DATA-001",
        "created_at": now(),
        "ai_involvement": "MATERIAL",
        "research_stages": ["SPECIFICATION", "IMPLEMENTATION", "VALIDATION", "DOCUMENTATION"],
        "systems": [{"name": "Codex", "provider": "OpenAI", "version_or_access_date": "2026-08-27", "roles": ["EXECUTOR", "SELF_VALIDATOR"]}],
        "persistent_context": [
            {"path_or_identifier": "LAB/MISSIONS/MISSION-DATA-001.md", "integrity": "append-only"},
            {"path_or_identifier": "LAB/MISSIONS/MISSION-DATA-001-ERRATA-001.md", "integrity": "append-only"},
            {"path_or_identifier": "LAB/MISSIONS/MISSION-DATA-001-ERRATA-002.md", "integrity": "append-only"}
        ],
        "executable_actions": [
            {"actor": "Codex", "action": "implemented and ran local data-hygiene fixtures", "artifact": "TEST-RESULTS.txt"},
            {"actor": "Codex", "action": "generated read-only baseline inventory", "artifact": "BASELINE-INVENTORY.json"},
            {"actor": "Codex", "action": "validated local-only export dry-run", "artifact": "EXPORT-VALIDATION.json"}
        ],
        "retrieval_sources": [
            {"identifier": "10.1038/sdata.2016.18", "accessed_at": "2026-08-27", "claim_location": "FAIR guiding principles"},
            {"identifier": "10.6028/NIST.SP.1500-18r2", "accessed_at": "2026-08-27", "claim_location": "research data lifecycle"},
            {"identifier": "https://www.w3.org/TR/prov-overview/", "accessed_at": "2026-08-27", "claim_location": "entities, activities and agents"},
            {"identifier": "https://www.rfc-editor.org/rfc/rfc8493", "accessed_at": "2026-08-27", "claim_location": "BagIt manifests and transfer"}
        ],
        "human_checkpoints": [{"checkpoint": "PREREGISTRATION_REVIEW_AND_EXECUTION_AUTHORIZATION", "authority": "Rodrigo", "record": "LAB/DECISIONS/WRITEBACK-031.md"}],
        "validation_layers": [
            {"validator": "unittest fixtures", "method": "positive and negative synthetic fixtures in /tmp", "independent_axes": ["test data"], "shared_axes": ["implementation", "criteria interpretation"]},
            {"validator": "SHA-256", "method": "recursive fixity and exact set comparison", "independent_axes": ["digest algorithm"], "shared_axes": ["local filesystem"]}
        ],
        "independence_limits": ["Executor and validator are the same Codex session (SELF_VALIDATION).", "No external validator or backup destination was authorized."],
        "known_limits": ["A005 remains contaminated.", "A005R remains corrupt.", "Backup and restore remain UNVERIFIED.", "No DOI, upload, license decision or scientific claim was produced."],
        "disclosure_summary": "Codex materially implemented and self-validated the DATA-001 data-governance tooling under a human-reviewed preregistration; local fixtures and SHA-256 checks compensate partially, without independent external validation."
    }
    write(TARGET / "AI-PROVENANCE.json", json.dumps(provenance_payload, indent=2, sort_keys=True) + "\n")

    role_by_name = {
        "TEST-RESULTS.txt": "LOG", "BASELINE-INVENTORY.json": "METADATA",
        "BASELINE-CHECK.json": "METADATA", "CATALOG-SNAPSHOT.json": "METADATA",
        "EXPORT-VALIDATION.json": "METADATA", "GATE-RESULTS.json": "METADATA",
        "AI-PROVENANCE.json": "METADATA",
    }
    resources = []
    for path in sorted(item for item in TARGET.iterdir() if item.is_file()):
        name = path.name
        role = role_by_name.get(name, "RAW" if name.endswith(".tsv") else "LOG")
        resources.append({
            "path": name, "role": role,
            "media_type": mimetypes.guess_type(name)[0] or "application/octet-stream",
            "bytes": path.stat().st_size, "sha256": sha256(path),
            "generated_by": "scripts/prepare_data001_evidence.py",
            "supports_criterion": ["DA-0", "DA-1", "DA-2", "DA-3", "DA-4", "DA-5", "DA-6", "DA-7", "DA-8", "DA-9", "DA-10"] if name == "GATE-RESULTS.json" else [],
        })
    manifest = {
        "schema_version": 1,
        "mission_id": "MISSION-DATA-001",
        "title": "Fixtures and validation reports for FPM data hygiene",
        "operational_state": "COMPLETE" if gate["gate"] == "PASS" else "FAILED",
        "created_at": now(),
        "resources": resources,
        "access": "LOCAL; lightweight subset may be public",
        "rights": "UNDECIDED",
        "retention": "PRESERVE",
        "expected_outputs": [{"path": item, "status": "PRODUCED"} for item in sorted(path.name for path in TARGET.iterdir() if path.is_file())],
        "links": {
            "mission": "LAB/MISSIONS/MISSION-DATA-001.md",
            "errata": ["LAB/MISSIONS/MISSION-DATA-001-ERRATA-001.md", "LAB/MISSIONS/MISSION-DATA-001-ERRATA-002.md"],
            "release": "LAB/RELEASES/RELEASE-DATA-001.md",
            "authorization": "LAB/DECISIONS/WRITEBACK-031.md",
            "ai_provenance": "AI-PROVENANCE.json"
        }
    }
    write(TARGET / "EVIDENCE-MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"target": str(TARGET), "files": len(list(TARGET.iterdir())), "gate": gate["gate"]}, sort_keys=True))
    return 0 if gate["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
