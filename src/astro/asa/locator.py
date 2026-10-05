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
HISTORICAL_CONFIG = ROOT / "config" / "asa-baseline.json"
CURRENT_DEV_CONFIG = ROOT / "config" / "asa-baseline-current-dev.json"


class AsaBaselineUnavailable(RuntimeError):
    """The pinned ASA checkout is missing or not at the pinned SHA."""


def config_path() -> Path:
    """Resolve pin file. Default historical; set ASTRO_ASA_BASELINE_CONFIG or ASTRO_ASA_PIN_KIND=current_dev for V1."""
    import os
    override = os.environ.get("ASTRO_ASA_BASELINE_CONFIG")
    if override:
        path = Path(override)
        return path if path.is_absolute() else ROOT / path
    if os.environ.get("ASTRO_ASA_PIN_KIND", "").strip().lower() in {"current_dev", "current-dev", "dev"}:
        if not CURRENT_DEV_CONFIG.exists():
            raise AsaBaselineUnavailable(f"current-dev pin missing: {CURRENT_DEV_CONFIG}")
        return CURRENT_DEV_CONFIG
    return HISTORICAL_CONFIG


def baseline() -> dict:
    return json.loads(config_path().read_text(encoding="utf-8"))


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
        module.verify(config_path=config_path())
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
