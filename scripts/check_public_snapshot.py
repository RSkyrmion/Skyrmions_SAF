#!/usr/bin/env python3
"""Accept a public snapshot only with the explicitly declared A005R anomalies."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
KNOWN_A005R_ERRORS = (
    "- hash divergente: LAB/EVIDENCE/A005R/RUN-LOG.txt",
    "- hash divergente: LAB/EVIDENCE/A005R/ac1_theta0.mx3",
    "- hash divergente: LAB/EVIDENCE/A005R/ac2_theta30.mx3",
    "- hash divergente: LAB/EVIDENCE/A005R/ac3_par.mx3",
    "- hash divergente: LAB/EVIDENCE/A005R/run_batch.sh",
)


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "check_repository.py")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    if result.returncode == 0:
        print(result.stdout, end="")
        return 0

    expected = ["Repository validation failed:", *KNOWN_A005R_ERRORS]
    if result.returncode == 1 and lines == expected:
        print(
            "OK: a auditoria integral reporta somente as cinco divergências de "
            "A005R declaradas em WRITEBACK-035; nenhum erro adicional."
        )
        return 0

    print(result.stdout, end="", file=sys.stderr)
    print(
        "Public snapshot validation failed: o resultado não corresponde à "
        "quarentena exata de A005R.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
