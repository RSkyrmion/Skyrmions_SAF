#!/usr/bin/env python3
"""Acceptance fixtures for MISSION-DATA-001 (all mutation confined to /tmp)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from build_data_catalog import build as build_catalog, validate_public_snapshot  # noqa: E402
from check_evidence import check_directory, check_tree  # noqa: E402
from export_data_package import create as create_export, validate as validate_export  # noqa: E402
from seal_evidence import seal  # noqa: E402
from validate_metadata import validate_manifest, validate_receipt  # noqa: E402
from validate_tabular import validate as validate_table  # noqa: E402


def provenance() -> dict[str, object]:
    return {
        "schema_version": 1,
        "mission_id": "MISSION-FIXTURE",
        "created_at": "2026-08-27T00:00:00Z",
        "ai_involvement": "MATERIAL",
        "research_stages": ["VALIDATION"],
        "systems": [{"name": "test", "provider": "local", "version_or_access_date": "2026-08-27", "roles": ["VALIDATOR"]}],
        "persistent_context": [], "executable_actions": [], "retrieval_sources": [],
        "human_checkpoints": [], "validation_layers": [], "independence_limits": [],
        "known_limits": [], "disclosure_summary": "Synthetic local fixture."
    }


def functional_manifest() -> dict[str, object]:
    return {
        "schema_version": 1, "mission_id": "MISSION-FIXTURE", "title": "fixture",
        "operational_state": "COMPLETE", "created_at": "2026-08-27T00:00:00Z",
        "resources": [{"path": "data.txt", "role": "RAW", "media_type": "text/plain",
                       "bytes": 2, "sha256": hashlib.sha256(b"x\n").hexdigest(),
                       "generated_by": "fixture"}],
        "access": "LOCAL", "rights": "UNDECIDED", "retention": "PRESERVE",
        "expected_outputs": [{"path": "data.txt", "status": "PRODUCED"}],
    }


def make_unsealed(root: Path, name: str = "FIXTURE") -> Path:
    directory = root / name
    directory.mkdir(parents=True)
    (directory / "data.txt").write_text("x\n", encoding="utf-8")
    (directory / "AI-PROVENANCE.json").write_text(json.dumps(provenance()) + "\n", encoding="utf-8")
    (directory / "EVIDENCE-MANIFEST.json").write_text(json.dumps(functional_manifest()) + "\n", encoding="utf-8")
    return directory


def manual_seal(directory: Path) -> None:
    lines = []
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        name = path.relative_to(directory).as_posix()
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {name}\n")
    (directory / "SHA256SUMS.txt").write_text("".join(lines), encoding="utf-8")


class EvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="data001-", dir="/tmp")
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def clean(self, name: str = "FIXTURE") -> Path:
        directory = make_unsealed(self.root, name)
        manual_seal(directory)
        self.assertEqual(check_directory(directory, set()).status, "SEALED_VALID")
        return directory

    def test_recursive_clean_and_extra_nested(self) -> None:
        directory = self.clean()
        (directory / "nested").mkdir()
        (directory / "nested" / "extra.txt").write_text("extra\n", encoding="utf-8")
        result = check_directory(directory, set())
        self.assertEqual(result.status, "SEALED_CONTAMINATED")
        self.assertEqual(result.extra, ["nested/extra.txt"])

    def test_missing_and_byte_change(self) -> None:
        missing = self.clean("MISSING")
        (missing / "data.txt").unlink()
        self.assertEqual(check_directory(missing, set()).missing, ["data.txt"])
        changed = self.clean("CHANGED")
        (changed / "data.txt").write_text("y\n", encoding="utf-8")
        self.assertEqual(check_directory(changed, set()).hash_mismatches, ["data.txt"])

    def test_duplicate_unsafe_symlink_and_transient(self) -> None:
        duplicate = self.clean("DUP")
        line = (duplicate / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()[0]
        with (duplicate / "SHA256SUMS.txt").open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
        self.assertTrue(check_directory(duplicate, set()).duplicate_entries)
        unsafe = self.clean("UNSAFE")
        with (unsafe / "SHA256SUMS.txt").open("a", encoding="utf-8") as stream:
            stream.write("0" * 64 + "  ../escape\n")
        self.assertEqual(check_directory(unsafe, set()).unsafe_paths, ["../escape"])
        linked = self.clean("LINK")
        (linked / "alias").symlink_to("data.txt")
        self.assertEqual(check_directory(linked, set()).status, "SEALED_CORRUPT")
        transient = self.clean("CACHE")
        (transient / "__pycache__").mkdir()
        (transient / "__pycache__" / "x.pyc").write_bytes(b"cache")
        self.assertEqual(check_directory(transient, set()).status, "SEALED_CONTAMINATED")

    def test_sealer_is_deterministic_and_never_overwrites(self) -> None:
        evidence = self.root / "evidence"
        directory = make_unsealed(evidence)
        index = self.root / "seals.jsonl"
        receipt = seal(directory, index=index, make_read_only=False, evidence_root=evidence)
        self.assertEqual(receipt["files"], 3)
        self.assertEqual(check_directory(directory, set()).status, "SEALED_VALID")
        with self.assertRaises(FileExistsError):
            seal(directory, index=index, make_read_only=False, evidence_root=evidence)

    def test_real_tree_preserves_known_failures(self) -> None:
        by_name = {item.directory: item for item in check_tree(ROOT / "LAB" / "EVIDENCE")}
        self.assertEqual(by_name["A005"].status, "SEALED_CONTAMINATED")
        self.assertIn("__pycache__/ovf.cpython-311.pyc", by_name["A005"].extra)
        self.assertEqual(by_name["A005R"].status, "SEALED_CORRUPT")
        self.assertEqual(len(by_name["A005R"].hash_mismatches), 5)
        self.assertIn("ac0_piso.mx3", by_name["A005R"].extra)
        self.assertEqual(by_name["LAB"].status, "UNSEALED")
        self.assertEqual(by_name["A003"].status, "SEALED_CONTAMINATED")
        self.assertIn("__pycache__/ovf.cpython-311.pyc", by_name["A003"].extra)
        self.assertEqual(by_name["A005R2"].status, "SEALED_VALID")
        self.assertFalse(by_name["A005R2"].metadata_errors)
        if "DATA-001" in by_name:
            self.assertIn(by_name["DATA-001"].status, {"UNSEALED", "SEALED_VALID"})
        self.assertTrue(all(item.status == "SEALED_VALID" for name, item in by_name.items()
                            if name not in {"A003", "A005", "A005R", "DATA-001", "LAB"}))


class SchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="data001-schema-", dir="/tmp")
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def validate_text(self, schema: str, text: str) -> list[str]:
        path = self.root / f"{schema}.txt"
        path.write_text(text, encoding="utf-8")
        return validate_table(path, SCRIPTS / "schemas" / f"{schema}.schema.json")

    def test_four_valid_table_families(self) -> None:
        cases = {
            "trajectory-v1": "# schema: trajectory-v1\n# units: s m m m m m 1 1 1 1\n0 0 0 1 0 1 1 -1 2 2\n1e-12 0 0 1 0 1 1 -1 2 2\n",
            "magnetization-grid-v1": "# schema: magnetization-grid-v1\n# units: 1 1 1 1 1 1\n0 0 1 0 0 1\n0 0 2 0 0 -1\n",
            "phase-scan-v1": "# schema: phase-scan-v1\n# units: J/m2 J/m3 1 m 1 T\n0.1 600000 COAXIAL NA 10 1e-5\n",
            "criterion-summary-v1": "# schema: criterion-summary-v1\n# units: 1 1 1 1 1\nDA-1\tcompletude\t1\tPASS\tfixture-local\n",
        }
        for schema, text in cases.items():
            with self.subTest(schema=schema):
                self.assertEqual(self.validate_text(schema, text), [])

    def test_invalid_column_unit_nan_and_monotonicity(self) -> None:
        base = "# schema: trajectory-v1\n# units: s m m m m m 1 1 1 1\n"
        self.assertTrue(self.validate_text("trajectory-v1", base + "0 0\n"))
        wrong_units = "# schema: trajectory-v1\n# units: ns m m m m m 1 1 1 1\n0 0 0 1 0 1 1 -1 2 2\n"
        self.assertTrue(self.validate_text("trajectory-v1", wrong_units))
        self.assertTrue(self.validate_text("trajectory-v1", base + "0 0 0 1 0 NaN 1 -1 2 2\n"))
        self.assertTrue(self.validate_text("trajectory-v1", base + "1 0 0 1 0 1 1 -1 2 2\n0 0 0 1 0 1 1 -1 2 2\n"))

    def test_manifest_semantics(self) -> None:
        valid = functional_manifest()
        self.assertEqual(validate_manifest(valid), [])
        missing = dict(valid)
        missing.pop("rights")
        self.assertTrue(validate_manifest(missing))
        bad_role = json.loads(json.dumps(valid))
        bad_role["resources"][0]["role"] = "CLAIM"
        self.assertTrue(validate_manifest(bad_role))
        absent = dict(valid)
        absent["expected_outputs"] = [{"path": "x", "status": "ABSENT"}]
        self.assertTrue(validate_manifest(absent))


class ReceiptExportCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="data001-run-", dir="/tmp")
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_receipt(self, label: str, code: str, timeout: float = 2) -> tuple[int, dict[str, object]]:
        receipt = self.root / f"{label}.json"
        command = [sys.executable, "-B", str(SCRIPTS / "run_with_receipt.py"),
                   "--mission", "MISSION-FIXTURE", "--run-id", label,
                   "--receipt", str(receipt), "--cwd", str(self.root),
                   "--timeout", str(timeout), "--", sys.executable, "-B", "-c", code]
        completed = subprocess.run(command, check=False)
        return completed.returncode, json.loads(receipt.read_text(encoding="utf-8"))

    def test_receipts_for_success_error_timeout(self) -> None:
        ok_code, ok = self.run_receipt("ok", "pass")
        fail_code, failed = self.run_receipt("fail", "raise SystemExit(3)")
        timeout_code, interrupted = self.run_receipt("timeout", "import time; time.sleep(1)", .05)
        self.assertEqual((ok_code, ok["state"]), (0, "COMPLETE"))
        self.assertEqual((fail_code, failed["state"]), (3, "FAILED"))
        self.assertEqual((timeout_code, interrupted["state"]), (124, "INTERRUPTED"))
        self.assertEqual(validate_receipt(ok), [])
        self.assertEqual(validate_receipt(failed), [])
        self.assertEqual(validate_receipt(interrupted), [])

    def test_local_export_and_no_identifier(self) -> None:
        source = self.root / "source"
        source.mkdir()
        (source / "fixture.txt").write_text("fixture\n", encoding="utf-8")
        output = self.root / "package"
        create_export(source, output, "MISSION-FIXTURE", "Fixture")
        self.assertEqual(validate_export(output), [])
        datacite = json.loads((output / "datacite-draft.json").read_text(encoding="utf-8"))
        self.assertEqual(datacite["identifiers"], [])
        self.assertEqual(datacite["state"], "DRAFT_LOCAL_ONLY")

    def test_catalog_links_and_no_silent_promotion(self) -> None:
        catalog, errors = build_catalog()
        self.assertEqual(errors, [])
        entries = {item["mission_id"]: item for item in catalog["entries"]}
        self.assertEqual(entries["MISSION-A005"]["seal_status"], "SEALED_CONTAMINATED")
        self.assertEqual(entries["MISSION-A005R"]["seal_status"], "SEALED_CORRUPT")
        for item in catalog["entries"]:
            for claim in item["claims"]:
                if claim["relation"] == "ACCEPTED":
                    self.assertTrue((ROOT / claim["authority"]).is_file())

    def test_public_catalog_without_omitted_payloads(self) -> None:
        count, errors = validate_public_snapshot()
        self.assertEqual(errors, [])
        self.assertEqual(count, len(check_tree(ROOT / "LAB" / "EVIDENCE")))

    def test_integrations_use_recursive_rule(self) -> None:
        hook = (ROOT / ".claude" / "hooks" / "verify-evidence.sh").read_text(encoding="utf-8")
        repository = (SCRIPTS / "check_repository.py").read_text(encoding="utf-8")
        self.assertIn("check_evidence.py", hook)
        self.assertIn("check_evidence.py", repository)


if __name__ == "__main__":
    unittest.main(verbosity=2)
