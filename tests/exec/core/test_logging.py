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
        """G1 logging: diagnostic events carry stable context without timestamps."""

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            logger = StructuredLogger(path, "RUN-" + "0" * 64, "lifecycle")
            logger.emit("info", "run-created", details={"dry_run": True}, provenance_id="PV-" + "1" * 64)
            logger.emit("warning", "empty-package")
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

            self.assertEqual([record["sequence"] for record in records], [0, 1])
            self.assertNotIn("recorded_at", records[0])
            self.assertEqual(records[0]["component"], "lifecycle")
            self.assertEqual(records[0]["provenance_id"], "PV-" + "1" * 64)
            self.assertEqual(records[0]["classification"], "diagnostic-log-not-scientific-evidence")
            with self.assertRaises(ConfigurationError):
                StructuredLogger(path, logger.run_id, "lifecycle")


if __name__ == "__main__":
    unittest.main()
