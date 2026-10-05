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
        self.assertRegex(
            view["run_id"],
            r"^RCPT-[0-9a-f]{64}__src-[0-9a-f]{64}__meta-(?:[0-9a-f]{64}|none)$",
        )
        self.assertRegex(view["receipt"]["receipt_id"], r"^RCPT-[0-9a-f]{64}$")
        self.assertTrue(view["run_id"].startswith(view["receipt"]["receipt_id"] + "__src-"))
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


@NEEDS_PIN
class DualUploadNoCrossContamination(_TempDataDir):
    """R-INT-01: distinct uploads must not share/overwrite run dirs or leak artifacts."""

    def _wcs_meta(self) -> bytes:
        meta = {
            "instrument": "synthetic-test",
            "wcs": {
                "frame": "ICRS",
                "epoch": "J2000.0",
                "crpix": [32.0, 32.0],
                "crval_deg": [150.0, -30.0],
                "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
                "pixel_origin": "0-based-image-pixel",
                "source_reference": "app-upload-dual-a",
            },
            "catalogue": {
                "match_radius_arcsec": 120.0,
                "provenance": {
                    "catalogue_name": "synthetic-app-catalogue",
                    "release": "test-0",
                    "query_description": "dual-upload regression A",
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
        return (json.dumps(meta, sort_keys=True) + "\n").encode("utf-8")

    def _nowcs_meta(self) -> bytes:
        meta = {
            "instrument": "synthetic-test",
            "catalogue": {
                "match_radius_arcsec": 120.0,
                "provenance": {
                    "catalogue_name": "synthetic-app-catalogue",
                    "release": "test-0",
                    "query_description": "dual-upload regression B",
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
        return (json.dumps(meta, sort_keys=True) + "\n").encode("utf-8")

    def test_wcs_then_nowcs_isolated_run_dirs_and_artifacts(self):
        from app import slice as s

        img_a = _fixture_ppm(Path(self._tmp.name) / "dual-a.ppm")
        # Distinct source bytes for B.
        data_a = img_a.read_bytes()
        data_b = data_a + b"\n# dual-b-distinct\n"
        sha_a = hashlib.sha256(data_a).hexdigest()
        sha_b = hashlib.sha256(data_b).hexdigest()
        self.assertNotEqual(sha_a, sha_b)

        meta_a = self._wcs_meta()
        meta_b = self._nowcs_meta()
        self.assertNotEqual(hashlib.sha256(meta_a).hexdigest(), hashlib.sha256(meta_b).hexdigest())

        view_a = s.run_slice(
            upload_bytes=data_a,
            upload_filename="dual-a.ppm",
            metadata_bytes=meta_a,
        )
        view_b = s.run_slice(
            upload_bytes=data_b,
            upload_filename="dual-b.ppm",
            metadata_bytes=meta_b,
        )

        # Same Objective receipt id is allowed (G-SIG-1) but run dirs must diverge.
        self.assertEqual(view_a["receipt"]["receipt_id"], view_b["receipt"]["receipt_id"])
        self.assertNotEqual(view_a["run_id"], view_b["run_id"])
        self.assertIn(f"__src-{sha_a}__", view_a["run_id"])
        self.assertIn(f"__src-{sha_b}__", view_b["run_id"])
        self.assertFalse(view_b.get("reproduced"))

        data_root = Path(os.environ["ASA_ASTRO_APP_DATA_DIR"])
        dir_a = data_root / "runs" / view_a["run_id"]
        dir_b = data_root / "runs" / view_b["run_id"]
        self.assertTrue(dir_a.is_dir())
        self.assertTrue(dir_b.is_dir())
        self.assertNotEqual(dir_a, dir_b)

        # A produced WCS; B must not inherit it on disk or in view.
        self.assertTrue((dir_a / "observation_wcs.json").is_file())
        self.assertFalse((dir_b / "observation_wcs.json").exists())
        self.assertIsNotNone(view_a["observation_evidence"]["wcs"])
        self.assertIsNone(view_b["observation_evidence"]["wcs"])

        # run.json for B must not list observation_wcs among artifacts.
        run_b = json.loads((dir_b / "run.json").read_text(encoding="utf-8"))
        self.assertNotIn("observation_wcs.json", run_b.get("artifacts") or {})
        run_a = json.loads((dir_a / "run.json").read_text(encoding="utf-8"))
        self.assertIn("observation_wcs.json", run_a.get("artifacts") or {})

        # A's uploaded_source record must remain A after B lands.
        src_a = json.loads((dir_a / "uploaded_source.json").read_text(encoding="utf-8"))
        src_b = json.loads((dir_b / "uploaded_source.json").read_text(encoding="utf-8"))
        self.assertEqual(src_a["sha256"], sha_a)
        self.assertEqual(src_b["sha256"], sha_b)

        # Artifact resolution via the same keyed run id matches view honesty.
        self.assertIsNotNone(s.artifact_path(view_a["run_id"], "observation_wcs.json"))
        self.assertIsNone(s.artifact_path(view_b["run_id"], "observation_wcs.json"))
        loaded_b = s.load_view(view_b["run_id"])
        self.assertIsNotNone(loaded_b)
        self.assertIsNone(loaded_b["observation_evidence"]["wcs"])

        # Existing run dirs are never rewritten on identical re-upload.
        mtime_a = (dir_a / "run.json").stat().st_mtime_ns
        again_a = s.run_slice(
            upload_bytes=data_a,
            upload_filename="dual-a.ppm",
            metadata_bytes=meta_a,
        )
        self.assertTrue(again_a["reproduced"])
        self.assertEqual(again_a["run_id"], view_a["run_id"])
        self.assertEqual((dir_a / "run.json").stat().st_mtime_ns, mtime_a)


@NEEDS_PIN
class DualUploadHttpIsolation(_TempDataDir):
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

    def _multipart(self, filename: str, data: bytes, metadata: bytes | None):
        boundary = "----AsaAstroDualBoundary9"
        body = b""
        parts = [
            ("objective", None, None, b"A-exoplanet-transit-followup"),
            ("source", filename, "image/x-portable-pixmap", data),
        ]
        if metadata is not None:
            parts.append(("metadata", "meta.json", "application/json", metadata))
        for name, fname, ctype, payload in parts:
            body += f"--{boundary}\r\n".encode()
            if fname is None:
                body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
                body += payload + b"\r\n"
            else:
                body += (
                    f'Content-Disposition: form-data; name="{name}"; filename="{fname}"\r\n'
                    f"Content-Type: {ctype}\r\n\r\n"
                ).encode()
                body += payload + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            self.base + "/api/runs",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read())

    def test_http_second_upload_null_wcs_does_not_serve_first_wcs(self):
        img = _fixture_ppm(Path(self._tmp.name) / "http-dual.ppm")
        data_a = img.read_bytes()
        data_b = data_a + b"\n# http-dual-b\n"
        meta_a = (json.dumps({
            "instrument": "http-dual",
            "wcs": {
                "frame": "ICRS", "epoch": "J2000.0",
                "crpix": [32.0, 32.0], "crval_deg": [150.0, -30.0],
                "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
                "pixel_origin": "0-based-image-pixel",
                "source_reference": "http-dual-a",
            },
        }, sort_keys=True) + "\n").encode()
        meta_b = (json.dumps({"instrument": "http-dual"}, sort_keys=True) + "\n").encode()

        status_a, view_a = self._multipart("a.ppm", data_a, meta_a)
        status_b, view_b = self._multipart("b.ppm", data_b, meta_b)
        self.assertEqual(status_a, 201)
        self.assertEqual(status_b, 201)
        self.assertNotEqual(view_a["run_id"], view_b["run_id"])
        self.assertIsNotNone(view_a["observation_evidence"]["wcs"])
        self.assertIsNone(view_b["observation_evidence"]["wcs"])

        # GET artifact for B must 404; for A must 200 with declared WCS.
        from urllib.parse import quote
        url_a = f"{self.base}/api/runs/{quote(view_a['run_id'], safe='')}/artifacts/observation_wcs.json"
        url_b = f"{self.base}/api/runs/{quote(view_b['run_id'], safe='')}/artifacts/observation_wcs.json"
        with urllib.request.urlopen(url_a, timeout=60) as r:
            self.assertEqual(r.status, 200)
            body_a = json.loads(r.read())
        self.assertEqual(body_a.get("status"), "declared")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(url_b, timeout=60)
        self.assertEqual(ctx.exception.code, 404)

        # Plain receipt_id must not resolve to a sibling upload dir (refuse ambiguous serve).
        plain = view_a["receipt"]["receipt_id"]
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(
                f"{self.base}/api/runs/{plain}/artifacts/observation_wcs.json", timeout=60
            )
        self.assertEqual(ctx.exception.code, 404)



@NEEDS_PIN
class ListRunDiscriminators(_TempDataDir):
    """U-RUN-LIST-01: list payload carries filename + src/meta discriminators (no bare-RCPT-only identity)."""

    def test_list_runs_shows_src_meta_discriminators(self):
        from app import slice as s

        img_a = _fixture_ppm(Path(self._tmp.name) / "alpha.ppm")
        img_b_path = Path(self._tmp.name) / "beta.ppm"
        img_b = _fixture_ppm(img_b_path)
        # Distinct bytes so source sha256 (and run_id) differs from alpha.
        b = bytearray(img_b.read_bytes()); b[-1] = (b[-1] + 1) % 256; img_b.write_bytes(bytes(b))
        # Same objective path → shared receipt_id likely; distinct sources → distinct run_ids.
        va = s.run_slice(upload_bytes=img_a.read_bytes(), upload_filename="alpha.ppm")
        vb = s.run_slice(upload_bytes=img_b.read_bytes(), upload_filename="beta.ppm")
        self.assertNotEqual(va["run_id"], vb["run_id"])
        listed = {item["run_id"]: item for item in s.list_runs()}
        for view, name in ((va, "alpha.ppm"), (vb, "beta.ppm")):
            item = listed[view["run_id"]]
            self.assertEqual(item["original_filename"], name)
            self.assertTrue(item["keyed_upload"])
            self.assertIn("__src-", item["run_id"])
            self.assertIn("__meta-", item["run_id"])
            self.assertTrue(item["source_sha256_short"])
            # Must not collapse to identical display keys solely on receipt prefix.
            self.assertNotEqual(item["run_id"][:21], item["run_id"])  # run_id longer than truncated RCPT
            self.assertEqual(item["receipt_id"], view["receipt"]["receipt_id"])
        self.assertNotEqual(listed[va["run_id"]]["source_sha256_short"], listed[vb["run_id"]]["source_sha256_short"])


class ObservationClaimIdentityConsume(_TempDataDir):
    """F-SCI-03: prefer pipeline observation_claim_digest / observation_claim_id."""

    @NEEDS_PIN
    def test_upload_surfaces_observation_claim_id_not_rcpt(self):
        from app import slice as s

        img = _fixture_ppm(Path(self._tmp.name) / "claim.ppm")
        meta = {
            "instrument": "synthetic-test",
            "wcs": {
                "frame": "ICRS",
                "epoch": "J2000.0",
                "crpix": [32.0, 32.0],
                "crval_deg": [150.0, -30.0],
                "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
                "pixel_origin": "0-based-image-pixel",
                "source_reference": "app-upload-claim-test",
            },
        }
        view = s.run_slice(
            upload_bytes=img.read_bytes(),
            upload_filename="claim.ppm",
            metadata_bytes=(json.dumps(meta) + "\n").encode("utf-8"),
        )
        oid = view["observation_identity"]
        self.assertIsInstance(oid, dict)
        self.assertEqual(oid.get("binding"), "content-addressed-observation-claim")
        self.assertRegex(oid["observation_claim_digest"], r"^[0-9a-f]{64}$")
        self.assertEqual(oid["observation_claim_id"], f"obsclaim-{oid['observation_claim_digest']}")
        self.assertTrue(oid["source_sha256"])
        self.assertTrue(oid["metadata_sha256"])
        self.assertTrue(oid["wcs_digest"])
        self.assertNotEqual(oid["observation_claim_id"], view["receipt"]["receipt_id"])
        self.assertFalse(oid["observation_claim_id"].startswith("RCPT-"))

        listed = {item["run_id"]: item for item in s.list_runs()}
        item = listed[view["run_id"]]
        self.assertEqual(item["observation_claim_key"], oid["observation_claim_id"])
        # Localisation honesty fields preferred from pipeline when present.
        locs = [l for l in view["observation_evidence"]["localisations"] if l["status"] == "localised"]
        self.assertTrue(locs)
        for loc in locs:
            self.assertEqual(loc["projection_model"], "local-linear-CD")
            self.assertEqual(loc["coordinate_standing"], "image-space-projection-hypothesis")

    def test_list_discriminator_prefers_claim_id_over_legacy_digest(self):
        from app import slice as s

        view = {
            "receipt": {"receipt_id": "RCPT-" + ("a" * 64)},
            "uploaded_source": {"present": True, "sha256": "b" * 64, "original_filename": "x.ppm"},
            "observation_evidence": {"wcs": {"status": "declared"}},
            "observation_identity": {
                "binding": "content-addressed-observation-claim",
                "source_sha256": "b" * 64,
                "metadata_sha256": "c" * 64,
                "wcs_digest": "d" * 64,
                "observation_claim_digest": "e" * 64,
                "observation_claim_id": "obsclaim-" + ("e" * 64),
                "digest": "legacy-should-not-win",
            },
        }
        run_id = "RCPT-" + ("a" * 64) + "__src-" + ("b" * 64) + "__meta-" + ("c" * 64)
        disc = s._list_run_discriminators(run_id, view)
        self.assertEqual(disc["observation_claim_key"], "obsclaim-" + ("e" * 64))


class HonestyFlagPropagation(unittest.TestCase):

    """F-SCI-04: app must not overwrite pipeline coordinates_invented=True to False."""

    def test_coordinates_invented_true_is_not_forced_false(self):
        from app import upload as u

        # Unit-level: _honesty_flag prefers payload over hard-coded safety.
        self.assertIs(u._honesty_flag({"coordinates_invented": True}, None, "coordinates_invented"), True)
        self.assertIs(u._honesty_flag(None, {"coordinates_invented": True}, "coordinates_invented"), True)
        self.assertEqual(u._honesty_flag({}, None, "coordinates_invented"), "unknown")
        self.assertEqual(u._honesty_flag(None, None, "source_image_mutated"), "unknown")


class DocClaimSurfaces(unittest.TestCase):
    """F-SCI-02 / U-DOC: README + GAPS disclose linear-CD; sample WCS fixture exists."""

    def test_gaps_and_readme_disclose_linear_cd(self):
        root = Path(__file__).resolve().parents[2]
        gaps = (root / "app" / "GAPS.md").read_text(encoding="utf-8")
        readme = (root / "app" / "README.md").read_text(encoding="utf-8")
        self.assertIn("G-SIG-6", gaps)
        self.assertTrue("linear" in gaps.lower() and "cd" in gaps.lower())
        self.assertIn("TAN", gaps)
        self.assertTrue("linear" in readme.lower() or "G-SIG-6" in readme)
        fixture = root / "app" / "static" / "sample-upload-metadata-wcs.json"
        self.assertTrue(fixture.is_file())
        meta = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertIn("wcs", meta)
        self.assertEqual(meta["wcs"]["pixel_origin"], "0-based-image-pixel")


if __name__ == "__main__":
    unittest.main()
