"""Upload → preserve source → thin path → receipt + observation/action honesty."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from app import pin as pinmod

ROOT = Path(__file__).resolve().parents[2]

try:
    PIN = pinmod.verify_pin()
    PIN_ERROR = None
except Exception as exc:  # pragma: no cover
    PIN, PIN_ERROR = None, str(exc)

NEEDS_PIN = unittest.skipIf(
    PIN is None,
    f"pinned ASA checkout not verified ({PIN_ERROR}); run "
    "python3 tools/asa_baseline.py --config config/asa-baseline-current-dev.json",
)


class _TempDataDir(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old = os.environ.get("ASA_ASTRO_APP_DATA_DIR")
        os.environ["ASA_ASTRO_APP_DATA_DIR"] = self._tmp.name

    def tearDown(self):
        if self._old is None:
            os.environ.pop("ASA_ASTRO_APP_DATA_DIR", None)
        else:
            os.environ["ASA_ASTRO_APP_DATA_DIR"] = self._old
        self._tmp.cleanup()


def _fixture_ppm(path: Path) -> Path:
    from tests.fixtures.generate_fixture import create_fixture
    return create_fixture(path)


@NEEDS_PIN
class UploadPreserveAndReceipt(_TempDataDir):
    def test_image_upload_preserves_source_and_sets_observation_present(self):
        from app import slice as s

        img = _fixture_ppm(Path(self._tmp.name) / "syn.ppm")
        data = img.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        view = s.run_slice(
            upload_bytes=data,
            upload_filename="syn.ppm",
            upload_media_type="image/x-portable-pixmap",
        )
        self.assertRegex(view["run_id"], r"^RCPT-[0-9a-f]{64}$")
        self.assertTrue(view["receipt"]["receipt_id_verified"])
        self.assertEqual(view["receipt"]["asa_baseline"], pinmod.pin_record()["sha"])
        self.assertEqual(pinmod.pin_record()["sha"], "c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2")

        us = view["uploaded_source"]
        self.assertTrue(us["present"])
        self.assertEqual(us["sha256"], digest)
        self.assertEqual(us["original_filename"], "syn.ppm")
        self.assertEqual(us["integrity_status"], "verified_sha256")
        self.assertTrue(us["process_observation_invoked"])
        stored = Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / us["stored_path"]
        self.assertTrue(stored.is_file())
        self.assertEqual(hashlib.sha256(stored.read_bytes()).hexdigest(), digest)

        run_dir = Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / "runs" / view["run_id"]
        src_art = json.loads((run_dir / "uploaded_source.json").read_text(encoding="utf-8"))
        self.assertEqual(src_art["sha256"], digest)
        self.assertEqual(src_art["original_filename"], "syn.ppm")

        oe = view["observation_evidence"]
        self.assertTrue(oe["present"], "process_observation always emits sky_localisations.json")
        self.assertIsNone(oe["wcs"], "no declared WCS in this case")
        self.assertTrue(oe["localisations"])
        for loc in oe["localisations"]:
            self.assertEqual(loc["status"], "unavailable")
            self.assertNotEqual(loc.get("classification_status"), "established")
            self.assertNotEqual(loc.get("label"), "established")

        # Residuals present (fail-closed unlocalised path) with hypothesis honesty
        ove = view["observed_vs_expected"]
        self.assertTrue(ove["present"])
        self.assertFalse(ove["epistemic"]["established_identity_promoted"])
        self.assertFalse(ove["epistemic"]["coordinates_invented"])
        self.assertTrue(ove["action_ui"]["honesty"]["hypothesis_only"])
        self.assertIn("WCS", ove["action_ui"]["headline"] or "")

    def test_image_upload_with_declared_wcs_localises_hypothesis_only(self):
        from app import slice as s

        img = _fixture_ppm(Path(self._tmp.name) / "syn-wcs.ppm")
        meta = {
            "instrument": "synthetic-test",
            "wcs": {
                "frame": "ICRS",
                "epoch": "J2000.0",
                "crpix": [32.0, 32.0],
                "crval_deg": [150.0, -30.0],
                "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
                "pixel_origin": "0-based-image-pixel",
                "source_reference": "app-upload-test",
            },
            "catalogue": {
                "match_radius_arcsec": 120.0,
                "provenance": {
                    "catalogue_name": "synthetic-app-catalogue",
                    "release": "test-0",
                    "query_description": "in-memory app upload test",
                },
                "entries": [
                    {
                        "catalogue_id": "SYN-APP-1",
                        "catalogue_name": "synthetic-app-catalogue",
                        "ra_deg": 150.0,
                        "dec_deg": -30.0,
                        "frame": "ICRS",
                        "epoch": "J2000.0",
                        "labels": ["synthetic"],
                        "evidence_ids": ["ev-syn-1"],
                    }
                ],
            },
        }
        view = s.run_slice(
            upload_bytes=img.read_bytes(),
            upload_filename="syn-wcs.ppm",
            metadata_bytes=(json.dumps(meta) + "\n").encode("utf-8"),
        )
        oe = view["observation_evidence"]
        self.assertTrue(oe["present"])
        self.assertIsNotNone(oe["wcs"])
        self.assertEqual(oe["wcs"]["status"], "declared")
        self.assertTrue(any(l["status"] == "localised" for l in oe["localisations"]))
        for loc in oe["localisations"]:
            if loc["status"] == "localised":
                self.assertEqual(loc["classification_status"], "hypothesis")
                self.assertNotEqual(loc["label"], "established-in-ASA-state")
                self.assertNotEqual(loc["label"], "established")
        for xm in oe["crossmatches"]:
            self.assertIn(xm["classification_status"], {"hypothesis", "provisional", "unknown"})
            self.assertNotEqual(xm["label"], "established")
            if xm["resolution_state"] == "matched":
                self.assertTrue(xm["evidence_qualified"])
        ove = view["observed_vs_expected"]
        self.assertTrue(ove["present"])
        self.assertFalse(ove["epistemic"]["established_identity_promoted"])
        run_dir = Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / "runs" / view["run_id"]
        self.assertTrue((run_dir / "observation_wcs.json").is_file())
        self.assertTrue((run_dir / "observation_localisations.json").is_file())
        self.assertTrue((run_dir / "observed_vs_expected.json").is_file())

    def test_fits_store_only_preserves_source_without_observation_present(self):
        from app import slice as s

        # Minimal non-image bytes with .fits suffix — store-only until FITS adapter.
        data = b"SIMPLE  =                    T / ASA-Astro preserve-source placeholder\nEND"
        digest = hashlib.sha256(data).hexdigest()
        view = s.run_slice(upload_bytes=data, upload_filename="placeholder.fits")
        us = view["uploaded_source"]
        self.assertTrue(us["present"])
        self.assertEqual(us["sha256"], digest)
        self.assertTrue(us["store_only"])
        self.assertFalse(us["process_observation_invoked"])
        self.assertFalse(view["observation_evidence"]["present"])
        self.assertFalse(view["observed_vs_expected"]["present"])
        self.assertTrue(any(u["kind"] == "observation-objective-bridge" for u in view["unknowns"]))


@NEEDS_PIN
class UploadHttpTests(_TempDataDir):
    def setUp(self):
        super().setUp()
        from app.server import make_server
        self.httpd = make_server("127.0.0.1", 0, quiet=True)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def test_multipart_upload_round_trip(self):
        img = _fixture_ppm(Path(self._tmp.name) / "http.ppm")
        boundary = "----AsaAstroBoundary7"
        body = b""
        for name, filename, ctype, data in (
            ("objective", None, None, b"A-exoplanet-transit-followup"),
            ("source", "http.ppm", "image/x-portable-pixmap", img.read_bytes()),
        ):
            body += f"--{boundary}\r\n".encode()
            if filename is None:
                body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
                body += data + b"\r\n"
            else:
                body += (
                    f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
                    f"Content-Type: {ctype}\r\n\r\n"
                ).encode()
                body += data + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            self.base + "/api/runs",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            status = r.status
            view = json.loads(r.read())
        self.assertIn(status, (200, 201))
        self.assertTrue(view["uploaded_source"]["present"])
        self.assertTrue(view["observation_evidence"]["present"])
        self.assertEqual(view["receipt"]["asa_baseline"], "c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2")


if __name__ == "__main__":
    unittest.main()
