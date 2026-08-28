#!/usr/bin/env python3
"""Validate compact AI provenance manifests for SAF evidence directories."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "LAB" / "EVIDENCE"
BASELINE = ROOT / "scripts" / "ai_provenance_baseline.txt"
MANIFEST = "AI-PROVENANCE.json"
REQUIRED = {
    "schema_version",
    "mission_id",
    "created_at",
    "ai_involvement",
    "research_stages",
    "systems",
    "persistent_context",
    "executable_actions",
    "retrieval_sources",
    "human_checkpoints",
    "validation_layers",
    "independence_limits",
    "known_limits",
    "disclosure_summary",
}
INVOLVEMENT = {"NONE", "ASSISTED", "MATERIAL", "EXTERNAL"}


def baseline_names() -> set[str]:
    if not BASELINE.exists():
        return set()
    return {
        line.strip()
        for line in BASELINE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"{path.relative_to(ROOT)}: JSON inválido ({exc})"]
    if not isinstance(payload, dict):
        return [f"{path.relative_to(ROOT)}: raiz deve ser um objeto JSON"]

    missing = sorted(REQUIRED - payload.keys())
    if missing:
        errors.append(
            f"{path.relative_to(ROOT)}: campos ausentes: {', '.join(missing)}"
        )
    involvement = payload.get("ai_involvement")
    if involvement not in INVOLVEMENT:
        errors.append(
            f"{path.relative_to(ROOT)}: ai_involvement deve ser "
            f"{', '.join(sorted(INVOLVEMENT))}"
        )
    if payload.get("schema_version") != 1:
        errors.append(f"{path.relative_to(ROOT)}: schema_version suportada é 1")
    if involvement != "NONE" and not payload.get("systems"):
        errors.append(f"{path.relative_to(ROOT)}: uso de IA exige systems não vazio")
    return errors


def main() -> int:
    baseline = baseline_names()
    errors: list[str] = []
    checked = 0
    if not EVIDENCE.is_dir():
        print("OK: diretório de evidência ausente; nada a conferir.")
        return 0

    for directory in sorted(path for path in EVIDENCE.iterdir() if path.is_dir()):
        manifest = directory / MANIFEST
        if not manifest.exists():
            if directory.name not in baseline:
                errors.append(
                    f"{directory.relative_to(ROOT)}/{MANIFEST}: ausente em diretório novo"
                )
            continue
        checked += 1
        errors.extend(validate(manifest))

    if errors:
        print("AI provenance validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"OK: {checked} manifesto(s) de proveniência de IA conferido(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
