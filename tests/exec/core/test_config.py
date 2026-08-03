"""Configuration loading, validation, immutability, and fingerprint tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from astro_exec.core.config import CONFIG_SCHEMA_VERSION, config_from_mapping, load_config
from astro_exec.core.errors import ConfigurationError


ROOT = Path(__file__).resolve().parents[3]


class ConfigurationTests(unittest.TestCase):
    """Verify the explicit Phase 2 TOML contract."""

    def test_repository_config_is_stable_and_immutable(self) -> None:
        first = load_config(ROOT / "config/astro-exec-phase2.toml")
        second = load_config(ROOT / "config/astro-exec-phase2.toml")

        self.assertEqual(first.schema_version, CONFIG_SCHEMA_VERSION)
        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertEqual(first.snapshot()["config_fingerprint"], first.fingerprint)
        with self.assertRaises(FrozenInstanceError):
            first.mode = "measurement"  # type: ignore[misc]

    def test_unknown_keys_and_unsafe_paths_fail_closed(self) -> None:
        base = load_config(ROOT / "config/astro-exec-phase2.toml").to_record()
        base["unexpected"] = True
        with self.assertRaises(ConfigurationError):
            config_from_mapping(base)

        unsafe = load_config(ROOT / "config/astro-exec-phase2.toml").to_record()
        unsafe["frozen_artefacts"][0]["path"] = "../outside"
        with self.assertRaises(ConfigurationError):
            config_from_mapping(unsafe)


if __name__ == "__main__":
    unittest.main()
