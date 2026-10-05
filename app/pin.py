"""Load and verify the ASA pin landed by 633f837a, then make the pinned kernel importable.

The pin is the ``sha`` field of the file named by ``app/config.json:asa_pin_file``
(``config/asa-baseline-current-dev.json``). ``src/astro/asa/locator.py`` still reads the
historical ``config/asa-baseline.json`` (b855d4c); rather than edit src/, the app points the
locator at the current-dev pin file *before* ``astro.asa.adapter`` is imported. This is an
app-layer integration seam, recorded in app/GAPS.md (G-PIN-1).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
APP_CONFIG = ROOT / "app" / "config.json"


class PinError(RuntimeError):
    """The pinned ASA checkout is missing, dirty or not at the pinned SHA."""


def app_config() -> dict[str, Any]:
    return json.loads(APP_CONFIG.read_text(encoding="utf-8"))


def pin_file() -> Path:
    return ROOT / app_config()["asa_pin_file"]


def pin_record() -> dict[str, Any]:
    return json.loads(pin_file().read_text(encoding="utf-8"))


def _baseline_tool():
    spec = importlib.util.spec_from_file_location("asa_app_tools_asa_baseline", ROOT / "tools" / "asa_baseline.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_pin() -> dict[str, Any]:
    """Run the repository's own verifier against the current-dev pin file. No network, no clone."""
    tool = _baseline_tool()
    try:
        receipt = tool.verify(config_path=pin_file())
    except RuntimeError as exc:
        raise PinError(str(exc)) from exc
    return receipt


_ACTIVATED: dict[str, Any] | None = None


def activate() -> dict[str, Any]:
    """Verify the pin and wire the Astro locator to it. Idempotent. Must run before importing astro.asa.adapter."""
    global _ACTIVATED
    if _ACTIVATED is not None:
        return _ACTIVATED
    receipt = verify_pin()
    record = pin_record()
    kernel_dir = Path(receipt["kernel_dir"])
    if str(kernel_dir) not in sys.path:
        sys.path.insert(0, str(kernel_dir))
    import astro.asa.locator as locator

    locator.CONFIG = pin_file()

    def ensure_importable() -> Path:
        verify_pin()
        if str(kernel_dir) not in sys.path:
            sys.path.insert(0, str(kernel_dir))
        return kernel_dir

    locator.ensure_importable = ensure_importable
    if "astro.asa.adapter" in sys.modules:  # already imported elsewhere; re-bind the imported names
        adapter = sys.modules["astro.asa.adapter"]
        adapter.ensure_importable = ensure_importable
    from asa_kernel.version import version_record

    kernel_reported = version_record()
    _ACTIVATED = {
        "pin_file": str(pin_file().relative_to(ROOT)),
        "pinned_sha": record["sha"],
        "pinned_ref": record["ref"],
        "pin_kind": record.get("pin_kind"),
        "pin_status_declared": record.get("kernel_status"),
        "pin_kernel_version_declared": record.get("kernel_version"),
        "kernel_version_reported_by_kernel": kernel_reported.get("kernel"),
        "kernel_status_reported_by_kernel": kernel_reported.get("status"),
        "historical_sha_preserved": record.get("historical_sha_preserved"),
        "verify_receipt": {k: v for k, v in receipt.items() if k != "kernel_dir"},
        "checkout_dir": record["checkout_dir"],
        "verified_by": "tools/asa_baseline.py verify(config_path=<pin file>)",
    }
    return _ACTIVATED
