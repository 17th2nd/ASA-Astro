"""Locate the pinned ASA kernel and make ``asa_kernel`` importable.

The kernel is never vendored or edited. ``config/asa-baseline.json`` pins the
exact commit; ``tools/asa_baseline.py`` materialises it under ``.asa/ASA``.
Every Astro receipt records the baseline SHA returned here.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / "config" / "asa-baseline.json"


class AsaBaselineUnavailable(RuntimeError):
    """The pinned ASA checkout is missing or not at the pinned SHA."""


def baseline() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def kernel_dir() -> Path:
    b = baseline()
    return ROOT / b["checkout_dir"] / b["kernel_subdir"]


def asa_baseline_sha() -> str:
    return baseline()["sha"]


def ensure_importable() -> Path:
    """Verify the checkout and put the kernel directory on ``sys.path``."""
    spec = importlib.util.spec_from_file_location("astro_tools_asa_baseline", ROOT / "tools" / "asa_baseline.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module.verify()
    except RuntimeError as exc:
        raise AsaBaselineUnavailable(str(exc)) from exc
    kdir = kernel_dir()
    if str(kdir) not in sys.path:
        sys.path.insert(0, str(kdir))
    return kdir


def kernel_version_record() -> dict:
    ensure_importable()
    from asa_kernel.version import version_record

    return version_record()
