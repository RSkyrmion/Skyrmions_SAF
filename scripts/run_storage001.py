#!/usr/bin/env python3
"""Execute the authorized, non-destructive ST-0..ST-5 storage appraisal."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "LAB" / "EVIDENCE"
TARGET = EVIDENCE / "STORAGE-001"
TEMP = Path("/tmp/fpm-storage-001-20260828")
PACKAGES = TEMP / "packages"
RESTORE = TEMP / "restore"
MISSION_ID = "MISSION-STORAGE-001"

HOLD = {
    "A005R": "SEALED_CORRUPT: five divergent payloads, one extra, and failure context",
    "A003": "SEALED_CONTAMINATED: historical __pycache__ preserved in context",
    "A005": "SEALED_CONTAMINATED: historical __pycache__ preserved in context",
    "LAB": "UNSEALED anomalous nested tree and zero-byte failure record",
}

ANALYSES = {
    "E002": ("analyze.py", "CRITERIOS-RESULTADOS.txt"),
    "E003": ("analyze3.py", "CRITERIOS-RESULTADOS.txt"),
    "E004": ("analyze4.py", "CRITERIOS-RESULTADOS.txt"),
    "E004R": ("analyze4r.py", "CRITERIOS-RESULTADOS.txt"),
    "E005": ("analyze5.py", "CRITERIOS-RESULTADOS.txt"),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_new(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o444)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        if isinstance(payload, str):
            stream.write(payload)
        else:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")


def file_record(path: Path, base: Path) -> dict[str, object]:
    st = path.lstat()
    kind = "symlink" if path.is_symlink() else "file"
    return {
        "path": path.relative_to(base).as_posix(),
        "kind": kind,
        "bytes": st.st_size,
        "sha256": None if kind == "symlink" else sha256(path),
        "symlink_target": os.readlink(path) if kind == "symlink" else None,
        "mode": stat.S_IMODE(st.st_mode),
        "mtime_ns": st.st_mtime_ns,
        "inode": st.st_ino,
    }


def snapshot(names: list[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for name in names:
        directory = EVIDENCE / name
        for path in sorted(directory.rglob("*")):
            if path.is_file() or path.is_symlink():
                records.append(file_record(path, EVIDENCE))
    return records


def stable_view(records: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {key: value for key, value in row.items() if key != "inode"}
        for row in records
    ]


def run(args: list[str], cwd: Path | None = None, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, input=input_bytes, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)


def seal_status(name: str) -> str:
    if name == "A005R":
        return "SEALED_CORRUPT"
    if name in {"A003", "A005"}:
        return "SEALED_CONTAMINATED"
    if name == "LAB":
        return "UNSEALED"
    return "SEALED_VALID"


def load_catalog() -> dict[str, dict[str, object]]:
    payload = json.loads((ROOT / "LAB" / "DATA-CATALOG.json").read_text(encoding="utf-8"))
    result = {}
    for entry in payload["entries"]:
        path = entry.get("evidence_path", "")
        if path.startswith("LAB/EVIDENCE/"):
            result[path.split("/")[-1]] = entry
    return result


def classify(names: list[str], baseline: list[dict[str, object]], catalog: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for item in baseline:
        name = str(item["path"]).split("/", 1)[0]
        entry = catalog.get(name, {})
        claims = entry.get("claims", [])
        suffix = Path(str(item["path"])).suffix.lower()
        basename = Path(str(item["path"])).name
        if name in HOLD:
            epistemic = "FAILURE_RECORD"
            retention = "PERMANENT_HOLD"
            reason = HOLD[name]
        elif name == "A005R2":
            epistemic = "FAILURE_RECORD"
            retention = "COLD_PRESERVE"
            reason = "nonconvergent procedural record; preserved but eligible for lossless cold copy"
        elif claims:
            epistemic = "CLAIM_BEARING"
            retention = "COLD_PRESERVE"
            reason = "catalog links mission to accepted claim(s): " + ",".join(str(c.get("id")) for c in claims)
        elif suffix in {".dat", ".ovf", ".omf", ".ohf"} or basename.startswith("SHA256SUMS"):
            epistemic = "CONTEXT_ONLY"
            retention = "COLD_PRESERVE"
            reason = "raw/checkpoint or integrity material; absence of discard proof resolves to preservation"
        else:
            epistemic = "NON_CLAIM"
            retention = "COLD_PRESERVE"
            reason = "no complete regeneration chain and bit-identical archived-output proof preregistered"
        rows.append({
            **item,
            "mission_directory": name,
            "seal_status": seal_status(name),
            "epistemic_role": epistemic,
            "retention_action": retention,
            "catalog_retention": entry.get("retention", "UNRECORDED"),
            "claims": claims,
            "authority_sources": [
                f"LAB/DATA-CATALOG.json#{name}",
                f"LAB/EVIDENCE/{name}/SHA256SUMS.txt" if (EVIDENCE / name / "SHA256SUMS.txt").exists() else "UNSEALED",
            ],
            "classification_reason": reason,
        })
    return rows


def receipt(run_id: str, command: list[str], cwd: Path, started: str, finished: str,
            duration: float, exit_code: int, inputs: list[dict[str, object]],
            outputs: list[dict[str, object]], state: str = "COMPLETE",
            executor_role: str = "PACKAGER") -> dict[str, object]:
    return {
        "schema_version": 1,
        "mission_id": MISSION_ID,
        "run_id": run_id,
        "command": command,
        "cwd": str(cwd),
        "started_at": started,
        "finished_at": finished,
        "duration_seconds": duration,
        "exit_code": exit_code,
        "timeout_seconds": 0,
        "state": state,
        "environment": {
            "python": sys.version.split()[0],
            "zstd": run(["zstd", "--version"]).stdout.decode(errors="replace").strip(),
            "platform": os.uname().sysname + " " + os.uname().release,
        },
        "parameters": {"compression": "zstd level 1", "archive": "GNU tar pax"},
        "determinism": "source payload identity is deterministic; compressed byte identity is recorded, not assumed across tool versions",
        "inputs": inputs,
        "outputs": outputs,
        "executor": {"kind": "AI", "name": "Codex", "role": executor_role},
    }


def create_package(name: str, source_rows: list[dict[str, object]]) -> tuple[dict[str, object], dict[str, object]]:
    archive = PACKAGES / f"{name}.tar.zst"
    manifest_path = PACKAGES / f"{name}.ARCHIVE-MANIFEST.json"
    command = ["tar", "--sort=name", "--format=posix", "-cf", "-", "-C", str(ROOT), f"LAB/EVIDENCE/{name}", "|", "zstd", "-1", "-T0", "-o", str(archive)]
    started = now()
    before = time.monotonic()
    tar_proc = subprocess.Popen(command[:8], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert tar_proc.stdout is not None
    zstd_proc = subprocess.Popen(command[9:], stdin=tar_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tar_proc.stdout.close()
    zstdout, zstderr = zstd_proc.communicate()
    tstderr = tar_proc.stderr.read() if tar_proc.stderr else b""
    tar_code = tar_proc.wait()
    duration = time.monotonic() - before
    if tar_code != 0 or zstd_proc.returncode != 0:
        raise RuntimeError(f"package {name} failed: tar={tar_code} {tstderr!r}; zstd={zstd_proc.returncode} {zstderr!r} {zstdout!r}")
    finished = now()
    manifest = {
        "schema_version": 1,
        "mission_id": MISSION_ID,
        "source_directory": f"LAB/EVIDENCE/{name}",
        "source_seal_status": seal_status(name),
        "historical_seal_authority": f"LAB/EVIDENCE/{name}/SHA256SUMS.txt",
        "historical_seal_rederived": False,
        "archive_file": archive.name,
        "archive_format": "POSIX pax tar compressed by Zstandard",
        "compression_lossless": True,
        "created_at": finished,
        "command": command,
        "source_file_count": len(source_rows),
        "source_bytes": sum(int(row["bytes"]) for row in source_rows),
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256(archive),
        "payloads": [{key: row[key] for key in ("path", "bytes", "sha256", "mode", "mtime_ns", "kind")} for row in source_rows],
        "temporary_location": str(archive),
        "retention": "TEMPORARY_COLD_COPY",
    }
    write_new(manifest_path, manifest)
    output = {"path": str(archive), "bytes": archive.stat().st_size, "sha256": manifest["archive_sha256"]}
    rec = receipt(f"package-{name}", command, ROOT, started, finished, duration, 0,
                  [{"path": f"LAB/EVIDENCE/{name}", "files": len(source_rows)}], [output])
    return manifest, rec


def archive_members(archive: Path) -> tuple[list[str], list[str]]:
    z = subprocess.Popen(["zstd", "-dc", str(archive)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert z.stdout is not None
    t = subprocess.Popen(["tar", "-tf", "-"], stdin=z.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    z.stdout.close()
    tout, terr = t.communicate()
    zerr = z.stderr.read() if z.stderr else b""
    zcode = z.wait()
    errors = []
    if zcode != 0 or t.returncode != 0:
        errors.append(f"list failure zstd={zcode} tar={t.returncode}: {zerr!r} {terr!r}")
    members = [line for line in tout.decode("utf-8", errors="strict").splitlines() if line]
    for member in members:
        pure = PurePosixPath(member)
        if pure.is_absolute() or ".." in pure.parts:
            errors.append(f"unsafe member: {member}")
    return members, errors


def restore_packages(eligible: list[str], package_index: list[dict[str, object]], baseline_by_path: dict[str, dict[str, object]]) -> dict[str, object]:
    RESTORE.mkdir(parents=True, exist_ok=False)
    details = []
    all_ok = True
    for item in package_index:
        name = str(item["directory"])
        archive = Path(str(item["temporary_archive"]))
        test = run(["zstd", "--test", str(archive)])
        members, member_errors = archive_members(archive)
        expected_prefix = f"LAB/EVIDENCE/{name}"
        prefix_ok = all(m == expected_prefix or m.startswith(expected_prefix + "/") for m in members)
        z = subprocess.Popen(["zstd", "-dc", str(archive)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert z.stdout is not None
        t = subprocess.Popen(["tar", "-xf", "-", "-C", str(RESTORE)], stdin=z.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        z.stdout.close()
        _, terr = t.communicate()
        zerr = z.stderr.read() if z.stderr else b""
        zcode = z.wait()
        restored_dir = RESTORE / "LAB" / "EVIDENCE" / name
        restored_rows = []
        if restored_dir.exists():
            for path in sorted(restored_dir.rglob("*")):
                if path.is_file() or path.is_symlink():
                    restored_rows.append(file_record(path, RESTORE / "LAB" / "EVIDENCE"))
        comparisons = []
        for row in restored_rows:
            source = baseline_by_path.get(str(row["path"]))
            comparisons.append({
                "path": row["path"],
                "source_present": source is not None,
                "bytes_equal": source is not None and row["bytes"] == source["bytes"],
                "sha256_equal": source is not None and row["sha256"] == source["sha256"],
                "mode_equal": source is not None and row["mode"] == source["mode"],
                "mtime_ns_equal": source is not None and row["mtime_ns"] == source["mtime_ns"],
            })
        path_set_equal = {str(row["path"]) for row in restored_rows} == {
            path for path in baseline_by_path if path.startswith(name + "/")
        }
        payload_ok = path_set_equal and all(c["bytes_equal"] and c["sha256_equal"] and c["mode_equal"] and c["mtime_ns_equal"] for c in comparisons)
        seal = run(["sha256sum", "-c", "SHA256SUMS.txt"], cwd=restored_dir)
        ok = test.returncode == 0 and not member_errors and prefix_ok and zcode == 0 and t.returncode == 0 and payload_ok and seal.returncode == 0
        all_ok = all_ok and ok
        details.append({
            "directory": name,
            "zstd_test": "PASS" if test.returncode == 0 else "FAIL",
            "member_safety": "PASS" if not member_errors and prefix_ok else "FAIL",
            "extract_exit": {"zstd": zcode, "tar": t.returncode},
            "path_set_equal": path_set_equal,
            "payload_and_metadata_equal": payload_ok,
            "historical_sha256sums": "PASS" if seal.returncode == 0 else "FAIL",
            "historical_sha256sums_stderr": seal.stderr.decode(errors="replace"),
            "errors": member_errors + ([terr.decode(errors="replace"), zerr.decode(errors="replace")] if zcode or t.returncode else []),
        })
    return {
        "technical_restore": "PASS" if all_ok else "FAIL",
        "lineage_assessment": "SELF_VALIDATION",
        "st_2_verdict": "UNEVALUATED",
        "reason": "PACKAGER and RESTORE_VALIDATOR share the same Codex lineage; technical checks do not promote SC-4",
        "restore_root": str(RESTORE),
        "directories": details,
    }


def analysis_matrix_and_results() -> tuple[list[dict[str, object]], dict[str, object]]:
    matrix = []
    results = []
    all_equal = True
    for name in sorted(ANALYSES):
        script_name, expected_name = ANALYSES[name]
        script = RESTORE / "LAB" / "EVIDENCE" / name / script_name
        expected = RESTORE / "LAB" / "EVIDENCE" / name / expected_name
        command = [sys.executable, "-B", f"LAB/EVIDENCE/{name}/{script_name}"]
        row = {
            "directory": name,
            "analyzer": f"LAB/EVIDENCE/{name}/{script_name}",
            "analyzer_sha256": sha256(script),
            "command": command,
            "cwd": str(RESTORE),
            "inputs": "restored LAB/EVIDENCE tree; cross-mission dependencies retained",
            "designated_output": f"LAB/EVIDENCE/{name}/{expected_name}",
            "expected_sha256": sha256(expected),
            "volatile_exclusions": [],
        }
        matrix.append(row)
        started = now()
        before = time.monotonic()
        proc = run(command, cwd=RESTORE)
        duration = time.monotonic() - before
        observed = hashlib.sha256(proc.stdout).hexdigest()
        equal = proc.returncode == 0 and observed == row["expected_sha256"]
        all_equal = all_equal and equal
        results.append({
            "directory": name,
            "exit_code": proc.returncode,
            "duration_seconds": duration,
            "expected_sha256": row["expected_sha256"],
            "observed_stdout_sha256": observed,
            "bit_identical": equal,
            "stderr": proc.stderr.decode(errors="replace"),
        })
    return matrix, {"verdict": "PASS" if all_equal else "FAIL", "comparison": "SHA-256 exact stdout equality; no tolerance and no volatile exclusions", "results": results}


def main() -> int:
    if not TARGET.is_dir() or sorted(p.name for p in TARGET.iterdir()) != ["AI-PROVENANCE.json"]:
        raise SystemExit("STORAGE-001 must contain only the pre-created AI-PROVENANCE.json")
    TEMP.mkdir(parents=True, exist_ok=False)
    PACKAGES.mkdir()

    source_names = sorted(p.name for p in EVIDENCE.iterdir() if p.is_dir() and p.name != "STORAGE-001")
    if set(HOLD) - set(source_names):
        raise SystemExit("PERMANENT-FAILURE-HOLD target missing")
    eligible = [name for name in source_names if name not in HOLD]
    baseline = snapshot(source_names)
    hold_before = [row for row in baseline if str(row["path"]).split("/", 1)[0] in HOLD]
    baseline_payload = {
        "created_at": now(),
        "source_root": "LAB/EVIDENCE",
        "excluded_new_evidence": "STORAGE-001",
        "directories": source_names,
        "eligible_directories": eligible,
        "file_count": len(baseline),
        "file_bytes": sum(int(row["bytes"]) for row in baseline),
        "files": baseline,
    }
    write_new(TARGET / "BASELINE-INVENTORY.json", baseline_payload)
    hold_payload = {
        "created_at": now(),
        "policy": "PERMANENT-FAILURE-HOLD",
        "operations_forbidden": ["compress", "migrate", "remove", "move", "replace", "normalize", "reseal"],
        "directories": [{"path": f"LAB/EVIDENCE/{name}", "reason": HOLD[name]} for name in HOLD],
        "files": hold_before,
    }
    write_new(TARGET / "PERMANENT-FAILURE-HOLD.json", hold_payload)

    catalog = load_catalog()
    classifications = classify(source_names, baseline, catalog)
    write_new(TARGET / "EPISTEMIC-RETENTION-MATRIX.json", {
        "created_at": now(),
        "rule": "absence of evidence for safe discard resolves to preservation",
        "rows": classifications,
        "counts": {
            "CLAIM_BEARING": sum(r["epistemic_role"] == "CLAIM_BEARING" for r in classifications),
            "FAILURE_RECORD": sum(r["epistemic_role"] == "FAILURE_RECORD" for r in classifications),
            "CONTEXT_ONLY": sum(r["epistemic_role"] == "CONTEXT_ONLY" for r in classifications),
            "NON_CLAIM": sum(r["epistemic_role"] == "NON_CLAIM" for r in classifications),
            "PERMANENT_HOLD": sum(r["retention_action"] == "PERMANENT_HOLD" for r in classifications),
            "COLD_PRESERVE": sum(r["retention_action"] == "COLD_PRESERVE" for r in classifications),
            "REGENERABLE_CANDIDATE": sum(r["retention_action"] == "REGENERABLE_CANDIDATE" for r in classifications),
        },
    })

    by_directory = {name: [row for row in baseline if str(row["path"]).startswith(name + "/")] for name in source_names}
    package_index = []
    for name in eligible:
        manifest, rec = create_package(name, by_directory[name])
        package_index.append({
            "directory": name,
            "seal_status": seal_status(name),
            "source_files": manifest["source_file_count"],
            "source_bytes": manifest["source_bytes"],
            "archive_bytes": manifest["archive_bytes"],
            "archive_sha256": manifest["archive_sha256"],
            "temporary_archive": str(PACKAGES / str(manifest["archive_file"])),
            "temporary_manifest": str(PACKAGES / f"{name}.ARCHIVE-MANIFEST.json"),
            "savings_bytes": int(manifest["source_bytes"]) - int(manifest["archive_bytes"]),
        })
        write_new(TARGET / "ARCHIVE-MANIFESTS" / f"{name}.ARCHIVE-MANIFEST.json", manifest)
        write_new(TARGET / "RUN-RECEIPTS" / f"package-{name}.json", rec)
    write_new(TARGET / "PACKAGE-INDEX.json", {
        "created_at": now(),
        "temporary_root": str(TEMP),
        "packages": package_index,
        "totals": {
            "source_bytes": sum(int(p["source_bytes"]) for p in package_index),
            "archive_bytes": sum(int(p["archive_bytes"]) for p in package_index),
            "savings_bytes": sum(int(p["savings_bytes"]) for p in package_index),
        },
    })

    baseline_by_path = {str(row["path"]): row for row in baseline}
    restore_results = restore_packages(eligible, package_index, baseline_by_path)
    write_new(TARGET / "RESTORE-RESULTS.json", restore_results)
    write_new(TARGET / "RUN-RECEIPTS" / "restore-validation.json", receipt(
        "restore-validation",
        ["zstd", "--test", "<each-package>", "and", "tar", "-xf", "<stream>", "-C", str(RESTORE)],
        ROOT, baseline_payload["created_at"], now(), 0.0, 0 if restore_results["technical_restore"] == "PASS" else 1,
        [{"path": str(PACKAGES), "packages": len(package_index)}],
        [{"path": "RESTORE-RESULTS.json", "sha256": sha256(TARGET / "RESTORE-RESULTS.json")}],
        state="COMPLETE" if restore_results["technical_restore"] == "PASS" else "FAILED",
        executor_role="SELF_VALIDATOR",
    ))
    matrix, analysis_results = analysis_matrix_and_results()
    write_new(TARGET / "ANALYSIS-REPRODUCTION-MATRIX.json", {"created_at": now(), "entries": matrix})
    write_new(TARGET / "ANALYSIS-RESULTS.json", analysis_results)
    write_new(TARGET / "RUN-RECEIPTS" / "analysis-validation.json", receipt(
        "analysis-validation",
        [sys.executable, "-B", "<each-sealed-analyze.py>"],
        RESTORE, baseline_payload["created_at"], now(), 0.0, 0 if analysis_results["verdict"] == "PASS" else 1,
        [{"path": str(RESTORE), "analyzers": len(matrix)}],
        [{"path": "ANALYSIS-RESULTS.json", "sha256": sha256(TARGET / "ANALYSIS-RESULTS.json")}],
        state="COMPLETE" if analysis_results["verdict"] == "PASS" else "FAILED",
        executor_role="SELF_VALIDATOR",
    ))

    copy_audit = {
        "verdict": "UNEVALUATED",
        "classification": "SINGLE_COPY",
        "temporary_copy": str(PACKAGES),
        "restore_copy": str(RESTORE),
        "failure_domain": "same filesystem as source; /tmp and workspace are both on /dev/nvme0n1p2",
        "second_failure_independent_destination": "NOT_AUTHORIZED_OR_NAMED",
        "st_4_satisfied": False,
    }
    write_new(TARGET / "COPY-AUDIT.json", copy_audit)

    candidates = {
        "created_at": now(),
        "execution_authorized": False,
        "st_6_status": "NOT_AUTHORIZED",
        "candidates": [],
        "candidate_bytes": 0,
        "reason": "zero files classified REGENERABLE_CANDIDATE; all evidence resolves to PRESERVE/COLD_PRESERVE/PERMANENT_HOLD, and independent restoration plus a second failure-domain copy are absent",
        "explicit_exclusions": ["CLAIM_BEARING", "FAILURE_RECORD", "PERMANENT_HOLD", "UNEVALUATED"],
    }
    write_new(TARGET / "DEACCESSION-CANDIDATES.json", candidates)

    after = snapshot(source_names)
    hold_after = [row for row in after if str(row["path"]).split("/", 1)[0] in HOLD]
    source_unchanged = stable_view(baseline) == stable_view(after)
    hold_unchanged = stable_view(hold_before) == stable_view(hold_after)
    packages_ok = all(Path(str(p["temporary_archive"])).is_file() and sha256(Path(str(p["temporary_archive"]))) == p["archive_sha256"] for p in package_index)
    technical_restore_ok = restore_results["technical_restore"] == "PASS"
    analysis_ok = analysis_results["verdict"] == "PASS"
    criteria = {
        "SC-0": {"verdict": "PASS" if source_unchanged else "FAIL", "reason": "preexisting LAB/EVIDENCE payload snapshot unchanged"},
        "SC-1": {"verdict": "PASS" if hold_unchanged else "FAIL", "reason": "four hold directories unchanged and excluded from packages"},
        "SC-2": {"verdict": "PASS" if len(classifications) == len(baseline) else "FAIL", "reason": "every source file has epistemic and retention axes"},
        "SC-3": {"verdict": "PASS" if packages_ok else "FAIL", "reason": "temporary archives and outer hashes validate; no historical seal rederived"},
        "SC-4": {"verdict": "UNEVALUATED", "reason": f"technical restore={technical_restore_ok}, but validation is SELF_VALIDATION"},
        "SC-5": {"verdict": "PASS" if analysis_ok else "FAIL", "reason": "all five applicable sealed analyzers compared by exact stdout SHA-256; zero deaccession candidates"},
        "SC-6": {"verdict": "UNEVALUATED", "reason": "no second failure-independent destination authorized"},
        "SC-7": {"verdict": "PASS", "reason": "candidate list is empty and excludes claim/failure/hold/unevaluated material"},
        "SC-8": {"verdict": "PASS" if source_unchanged else "FAIL", "reason": "ST-6 NOT_AUTHORIZED; no original removed"},
        "SC-9": {"verdict": "PASS" if source_unchanged else "FAIL", "reason": "no preexisting evidence, claim, release, historical seal or scientific status changed"},
    }
    failed = [key for key, value in criteria.items() if value["verdict"] == "FAIL"]
    unevaluated = [key for key, value in criteria.items() if value["verdict"] == "UNEVALUATED"]
    outcome = "NOT_SAFE_TO_MIGRATE" if failed else ("COLD_COPY_ONLY" if unevaluated else "MIGRATION_READY")
    gate = {
        "mission_id": MISSION_ID,
        "created_at": now(),
        "authorized_scope": "ST-0 through ST-5; /tmp packages; ST-6 and removal not authorized",
        "criteria": criteria,
        "failed": failed,
        "unevaluated": unevaluated,
        "g_storage": "PASS" if not failed and not unevaluated else "NOT_PASS",
        "outcome": outcome,
        "st_6": "NOT_AUTHORIZED",
        "source_unchanged": source_unchanged,
        "hold_unchanged": hold_unchanged,
        "temporary_package_totals": {
            "source_bytes": sum(int(p["source_bytes"]) for p in package_index),
            "archive_bytes": sum(int(p["archive_bytes"]) for p in package_index),
        },
    }
    write_new(TARGET / "GATE-RESULTS.json", gate)
    print(json.dumps(gate, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
