#!/usr/bin/env python3
"""Run a command while preserving an atomic, finalizable FPM execution receipt."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest(path: Path) -> dict[str, object]:
    item: dict[str, object] = {"path": str(path)}
    if not path.is_file():
        item["status"] = "MISSING"
        return item
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    item.update({"status": "PRESENT", "bytes": path.stat().st_size, "sha256": hasher.hexdigest()})
    return item


def write_atomic(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def run(args: argparse.Namespace) -> int:
    cwd = args.cwd.resolve()
    command = args.command
    executable = Path(command[0])
    if not executable.is_absolute():
        resolved = subprocess.run(["which", command[0]], text=True, capture_output=True).stdout.strip()
        executable = Path(resolved) if resolved else executable
    receipt: dict[str, object] = {
        "schema_version": 1,
        "mission_id": args.mission,
        "run_id": args.run_id,
        "command": command,
        "cwd": str(cwd),
        "started_at": now(),
        "finished_at": None,
        "duration_seconds": None,
        "exit_code": None,
        "timeout_seconds": args.timeout,
        "state": "RUNNING",
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "executable": digest(executable) if executable.is_file() else {"path": str(executable), "status": "UNRESOLVED"},
        },
        "parameters": json.loads(args.parameters),
        "determinism": {"seed": args.seed, "declared": args.determinism},
        "inputs": [digest((cwd / item).resolve()) for item in args.input],
        "outputs": [{"path": str((cwd / item).resolve()), "status": "EXPECTED"} for item in args.output],
        "executor": {"agent": args.executor, "human_checkpoint": args.checkpoint},
    }
    write_atomic(args.receipt, receipt)
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=cwd, timeout=args.timeout, check=False)
        receipt["exit_code"] = completed.returncode
        receipt["state"] = "COMPLETE" if completed.returncode == 0 else "FAILED"
        return_code = completed.returncode
    except subprocess.TimeoutExpired:
        receipt["state"] = "INTERRUPTED"
        receipt["exit_code"] = None
        receipt["interruption"] = "TIMEOUT"
        return_code = 124
    except BaseException as exc:
        receipt["state"] = "INTERRUPTED"
        receipt["interruption"] = f"{type(exc).__name__}: {exc}"
        return_code = 125
    finally:
        receipt["finished_at"] = now()
        receipt["duration_seconds"] = round(time.monotonic() - started, 9)
        receipt["outputs"] = [digest((cwd / item).resolve()) for item in args.output]
        write_atomic(args.receipt, receipt)
    return return_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mission", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--parameters", default="{}")
    parser.add_argument("--seed", default="UNSPECIFIED")
    parser.add_argument("--determinism", default="UNDECLARED")
    parser.add_argument("--executor", default="Codex")
    parser.add_argument("--checkpoint", default="UNSPECIFIED")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        print("a command is required after --", file=sys.stderr)
        return 2
    try:
        json.loads(args.parameters)
    except json.JSONDecodeError as exc:
        print(f"invalid --parameters JSON: {exc}", file=sys.stderr)
        return 2
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())

