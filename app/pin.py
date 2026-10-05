"""Load and verify the ASA pin landed by 633f837a, then make the pinned kernel importable.

The pin is the ``sha`` field of the file named by ``app/config.json:asa_pin_file``
(``config/asa-baseline-current-dev.json``). Commit a200dda taught ``src/astro/asa/locator.py``
to honour ``ASTRO_ASA_BASELINE_CONFIG``; the app sets that variable to the pin file before the
adapter is imported, so the locator itself verifies and loads the pinned kernel. No src/ edit,
no monkeypatching.
"""

from __future__ import annotations

import importlib.util
import json
import os
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
ENV = "ASTRO_ASA_BASELINE_CONFIG"


def activate() -> dict[str, Any]:
    """Verify the pin and select it for the Astro locator. Idempotent. Must run before importing astro.asa.adapter."""
    global _ACTIVATED
    if _ACTIVATED is not None:
        return _ACTIVATED
    receipt = verify_pin()
    record = pin_record()
    wanted = str(pin_file())
    existing = os.environ.get(ENV)
    if existing and Path(existing if Path(existing).is_absolute() else ROOT / existing).resolve() != pin_file().resolve():
        raise PinError(f"{ENV}={existing} conflicts with app pin file {wanted}")
    os.environ[ENV] = wanted
    import astro.asa.locator as locator

    if not hasattr(locator, "config_path"):
        raise PinError("astro.asa.locator has no config_path(); this app needs the a200dda locator (ASTRO_ASA_BASELINE_CONFIG)")
    if locator.config_path().resolve() != pin_file().resolve():
        raise PinError(f"locator resolves {locator.config_path()} instead of {wanted}")
    kernel_dir = locator.ensure_importable()  # the locator's own verify against the pin file
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
        "locator_baseline_sha": locator.asa_baseline_sha(),
        "verify_receipt": {k: v for k, v in receipt.items() if k != "kernel_dir"},
        "checkout_dir": record["checkout_dir"],
        "kernel_dir": str(Path(kernel_dir).relative_to(ROOT)),
        "selected_via": f"{ENV} (src/astro/asa/locator.py config_path, commit a200dda)",
        "verified_by": "tools/asa_baseline.py verify(config_path=<pin file>) — called by the app and by the locator",
    }
    return _ACTIVATED
