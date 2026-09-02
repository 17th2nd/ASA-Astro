#!/usr/bin/env python3
"""Materialise and verify the pinned ASA baseline consumed by Astro.

Reads ``config/asa-baseline.json``, ensures ``.asa/ASA`` is a checkout at exactly
the pinned SHA, and prints a JSON receipt. Never modifies the source repository.

    python3 tools/asa_baseline.py            # ensure + verify
    python3 tools/asa_baseline.py --verify   # verify only, no network, no clone
    ASTRO_ASA_SOURCE=/path/to/local/ASA python3 tools/asa_baseline.py   # clone from a local mirror
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "asa-baseline.json"


def load_baseline() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def checkout_dir(baseline: dict | None = None) -> Path:
    baseline = baseline or load_baseline()
    return ROOT / baseline["checkout_dir"]


def verify(baseline: dict | None = None) -> dict:
    """Return a receipt; raise RuntimeError if the checkout is absent or at the wrong SHA."""
    baseline = baseline or load_baseline()
    target = checkout_dir(baseline)
    if not (target / ".git").exists():
        raise RuntimeError(f"ASA baseline checkout missing at {target}; run tools/asa_baseline.py")
    head = _git("rev-parse", "HEAD", cwd=target)
    if head != baseline["sha"]:
        raise RuntimeError(f"ASA baseline checkout at {head}, pinned {baseline['sha']}")
    if _git("status", "--porcelain", cwd=target):
        raise RuntimeError("ASA baseline checkout is dirty; Astro never edits the consumed baseline")
    kernel = target / baseline["kernel_subdir"]
    if not (kernel / "asa_kernel" / "api.py").exists():
        raise RuntimeError(f"pinned checkout has no kernel at {kernel}")
    return {"asa_baseline": head, "ref": baseline["ref"], "kernel_dir": str(kernel), "kernel_version": baseline["kernel_version"]}


def ensure(baseline: dict | None = None) -> dict:
    baseline = baseline or load_baseline()
    target = checkout_dir(baseline)
    if not (target / ".git").exists():
        source = os.environ.get("ASTRO_ASA_SOURCE", baseline["repository"])
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", "--no-checkout", source, str(target)], check=True)
        _git("fetch", "--quiet", "origin", baseline["ref"], cwd=target)
        _git("checkout", "--quiet", "--detach", baseline["sha"], cwd=target)
    return verify(baseline)


def main(argv: list[str]) -> int:
    try:
        receipt = verify() if "--verify" in argv else ensure()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps({"status": "verified", **receipt}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
