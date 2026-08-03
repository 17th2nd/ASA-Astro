"""Structured logging contract tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from astro_exec.core.errors import ConfigurationError
from astro_exec.core.logging import StructuredLogger


class StructuredLoggingTests(unittest.TestCase):
    """Verify canonical ordered JSONL without ambient timestamps."""

    def test_events_have_stable_sequences_and_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            logger = StructuredLogger(path, "RUN-" + "0" * 64)
            logger.emit("info", "run-created", details={"dry_run": True})
            logger.emit("warning", "empty-package")
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

            self.assertEqual([record["sequence"] for record in records], [0, 1])
            self.assertNotIn("recorded_at", records[0])
            with self.assertRaises(ConfigurationError):
                StructuredLogger(path, logger.run_id)


if __name__ == "__main__":
    unittest.main()
