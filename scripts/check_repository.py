#!/usr/bin/env python3
"""Validate the lightweight public research repository without extra dependencies."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_SIZE = 50 * 1024 * 1024
FORBIDDEN_PREFIXES = (
    ".agents/",
    ".claude/",
    ".codex/",
    "ARCHIVE/",
    "SOURCES/fpm/",
)
ALLOWED_TOOL_FILES = {
    "TOOLS/README.md",
    "TOOLS/build.sh",
    "TOOLS/BUILD-LOG.txt",
    "TOOLS/SHA256-mumax3-bin.txt",
}
ALLOWED_PAPER_FILES = {
    "SOURCES/paper/README.md",
    "SOURCES/paper/SHA256SUMS.txt",
}
FORBIDDEN_SUFFIXES = (
    ".dat",
    ".ohf",
    ".omf",
    ".ovf",
    ".pem",
    ".pfx",
    ".p12",
    ".so",
)
SECRET_PATTERNS = {
    "private key": re.compile(rb"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "GitHub token": re.compile(rb"(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "AWS access key": re.compile(rb"AKIA[0-9A-Z]{16}"),
}
HASH_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+[ *](.+)$")


def forbidden_public_path(name: str) -> bool:
    return (
        name.startswith(FORBIDDEN_PREFIXES)
        or (name.startswith("TOOLS/") and name not in ALLOWED_TOOL_FILES)
        or (name.startswith("SOURCES/paper/") and name not in ALLOWED_PAPER_FILES)
    )


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        return [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        name = path.relative_to(ROOT).as_posix()
        if name.startswith(".git/") or forbidden_public_path(name):
            continue
        if name.lower().endswith(FORBIDDEN_SUFFIXES):
            continue
        if path.stat().st_size > MAX_FILE_SIZE:
            continue
        try:
            if path.open("rb").read(4) == b"\x7fELF":
                continue
        except OSError:
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    files = tracked_files()
    relative = {path.relative_to(ROOT).as_posix(): path for path in files}
    errors: list[str] = []
    checked_hashes = 0
    omitted_hashes = 0

    for name, path in relative.items():
        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            errors.append(f"arquivo maior que 50 MiB: {name} ({size} bytes)")
        if forbidden_public_path(name):
            errors.append(f"caminho proibido no espelho público: {name}")
        if name.lower().endswith(FORBIDDEN_SUFFIXES):
            errors.append(f"formato de dado/binário proibido: {name}")

        data = path.read_bytes()
        if data.startswith(b"\x7fELF"):
            errors.append(f"executável ELF versionado: {name}")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                errors.append(f"possível {label}: {name}")

        if path.suffix == ".py":
            try:
                ast.parse(data, filename=name)
            except SyntaxError as exc:
                errors.append(f"Python inválido em {name}: {exc}")

    for manifest in (path for path in files if path.name == "SHA256SUMS.txt"):
        for line_number, line in enumerate(manifest.read_text(errors="replace").splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            match = HASH_LINE.match(line)
            if not match:
                errors.append(f"linha SHA-256 inválida: {manifest.relative_to(ROOT)}:{line_number}")
                continue
            expected, local_name = match.groups()
            candidate = manifest.parent / local_name
            candidate_key = candidate.relative_to(ROOT).as_posix()
            if candidate_key not in relative:
                omitted_hashes += 1
                continue
            actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
            checked_hashes += 1
            if actual.lower() != expected.lower():
                errors.append(f"hash divergente: {candidate_key}")

    provenance = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_ai_provenance.py")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if provenance.returncode:
        errors.extend(
            f"proveniência: {line}"
            for line in provenance.stdout.splitlines()
            if line.strip()
        )

    evidence = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "check_evidence.py"), "--self-test"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if evidence.returncode:
        errors.extend(
            f"evidência recursiva: {line}"
            for line in evidence.stdout.splitlines()
            if line.strip() and not line.startswith("SEALED_VALID")
        )

    catalog = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "build_data_catalog.py"), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if catalog.returncode:
        errors.extend(
            f"catálogo: {line}" for line in catalog.stdout.splitlines() if line.strip()
        )

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(files)} arquivos; {checked_hashes} hashes conferidos; "
        f"{omitted_hashes} entradas correspondem a dados não publicados."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
