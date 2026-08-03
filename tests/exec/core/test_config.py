"""Configuration loading, validation, immutability, and fingerprint tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from astro_exec.core.config import CONFIG_SCHEMA_VERSION, config_from_mapping, configuration_schema, load_config
from astro_exec.core.errors import ConfigurationError


ROOT = Path(__file__).resolve().parents[3]


class ConfigurationTests(unittest.TestCase):
    """Verify the explicit Phase 2 TOML contract."""

    def test_repository_config_is_stable_and_immutable(self) -> None:
        """G1 config: schema validation, fingerprint stability, and immutability hold."""
        first = load_config(ROOT / "config/astro-exec-phase2.toml")
        second = load_config(ROOT / "config/astro-exec-phase2.toml")

        self.assertEqual(first.schema_version, CONFIG_SCHEMA_VERSION)
        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertEqual(first.snapshot()["config_fingerprint"], first.fingerprint)
        self.assertEqual(first.to_record()["defaults"], {"applied": [], "policy": "no-implicit-defaults"})
        self.assertTrue(str(first.identity).startswith("CFG-"))
        with self.assertRaises(FrozenInstanceError):
            first.mode = "measurement"  # type: ignore[misc]

    def test_unknown_keys_and_unsafe_paths_fail_closed(self) -> None:
        """G1 config: unknown fields and escaping paths fail validation."""
        base = load_config(ROOT / "config/astro-exec-phase2.toml").to_record()
        base["unexpected"] = True
        with self.assertRaises(ConfigurationError):
            config_from_mapping(base)

        unsafe = load_config(ROOT / "config/astro-exec-phase2.toml").to_record()
        unsafe["execution"]["frozen_manifest"] = "../outside"
        with self.assertRaises(ConfigurationError):
            config_from_mapping(unsafe)

    def test_packaged_versioned_schema_is_binding(self) -> None:
        """G1 config: the packaged schema is versioned and rejects omissions."""

        schema = configuration_schema()
        self.assertEqual(schema["$id"], "urn:asa-astro:astro-exec-config-v1")
        missing = load_config(ROOT / "config/astro-exec-phase2.toml").to_record()
        del missing["defaults"]
        with self.assertRaises(ConfigurationError):
            config_from_mapping(missing)


if __name__ == "__main__":
    unittest.main()
