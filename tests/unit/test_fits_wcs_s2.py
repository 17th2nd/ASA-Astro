"""S2 / P2: safe FITS read, TAN via astropy.wcs, solve-field fail-closed, local-linear-CD labelled."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from asa_astro.evidence.fits_io import (
    ASTROPY_PIN,
    FitsWcsUnavailable,
    read_fits_observation,
    source_sha256,
)
from asa_astro.evidence.solve_field import (
    SolveFieldUnavailable,
    run_solve_field,
    solve_field_available,
)
from asa_astro.evidence.validation import validate_instance
from asa_astro.evidence.wcs import (
    PROJECTION_MODEL,
    localise_detection,
    parse_declared_wcs,
    pixel_to_sky,
    pixel_to_sky_local_linear_cd,
)


def _write_tan_fits(path: Path, *, with_sip: bool = False) -> Path:
    from astropy.io import fits
    from astropy.wcs import WCS

    w = WCS(naxis=2)
    w.wcs.crpix = [32.5, 32.5]  # FITS 1-based
    w.wcs.crval = [150.0, -30.0]
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    w.wcs.cd = [[-0.0002777777778, 0.0], [0.0, 0.0002777777778]]
    w.wcs.radesys = "ICRS"
    w.wcs.equinox = 2000.0
    header = w.to_header()
    if with_sip:
        # Minimal SIP orders (identity-ish) so CTYPE becomes TAN-SIP when written carefully.
        header["CTYPE1"] = "RA---TAN-SIP"
        header["CTYPE2"] = "DEC--TAN-SIP"
        header["A_ORDER"] = 1
        header["B_ORDER"] = 1
        header["A_0_0"] = 0.0
        header["A_1_0"] = 0.0
        header["A_0_1"] = 0.0
        header["B_0_0"] = 0.0
        header["B_1_0"] = 0.0
        header["B_0_1"] = 0.0
    header["DATE-OBS"] = "2026-10-05T12:00:00"
    header["TELESCOP"] = "TEST-SCOPE"
    header["INSTRUME"] = "TEST-CAM"
    header["FILTER"] = "r"
    header["EXPTIME"] = 30.0
    data = np.zeros((64, 64), dtype=np.float32)
    data[30:35, 30:35] = 1000.0
    fits.PrimaryHDU(data=data, header=header).writeto(path, overwrite=True)
    return path


class FitsWcsS2Test(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="asa-fits-s2-", dir="/tmp")
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_safe_fits_read_preserves_bytes_and_extracts_tan(self) -> None:
        path = _write_tan_fits(self.root / "tan.fits")
        before = source_sha256(path)
        result = read_fits_observation(path)
        after = source_sha256(path)
        self.assertEqual(before, after)
        self.assertFalse(result["source_image_mutated"])
        self.assertFalse(result["coordinates_invented"])
        self.assertTrue(result["wcs_present"])
        self.assertEqual(result["projection_model"], "TAN")
        self.assertEqual(result["astropy_pin_expected"], ASTROPY_PIN)
        wcs = result["wcs_solution"]
        validate_instance("wcs_solution", wcs)
        self.assertEqual(wcs["projection_model"], "TAN")
        self.assertEqual(wcs["coordinate_standing"], "fits-header-tan-hypothesis")
        # CRPIX converted to 0-based
        self.assertAlmostEqual(wcs["crpix"][0], 31.5, places=5)
        self.assertAlmostEqual(wcs["crval_deg"][0], 150.0, places=5)
        self.assertIn("wcs_header_cards", wcs)
        meta = result["header_metadata"]
        self.assertEqual(meta["time"]["date_obs"]["status"], "present")
        self.assertEqual(meta["instrument"]["telescope"]["value"], "TEST-SCOPE")
        self.assertEqual(meta["filter"]["filter"]["value"], "r")

    def test_tan_pixel_to_sky_via_astropy_not_silent_local_linear(self) -> None:
        path = _write_tan_fits(self.root / "tan2.fits")
        result = read_fits_observation(path)
        wcs = result["wcs_solution"]
        # CRPIX in 0-based == centre → should recover CRVAL
        sky = pixel_to_sky(wcs["crpix"][0], wcs["crpix"][1], wcs)
        self.assertAlmostEqual(float(sky["ra_deg"]), 150.0, places=4)
        self.assertAlmostEqual(float(sky["dec_deg"]), -30.0, places=4)
        loc = localise_detection(
            {"id": "detection-aaaaaaaaaaaaaaaaaaaa", "centroid": {"x": wcs["crpix"][0], "y": wcs["crpix"][1], "unit": "pixel"}},
            wcs,
        )
        self.assertEqual(loc["status"], "localised")
        self.assertEqual(loc["projection_model"], "TAN")
        self.assertEqual(loc["classification_status"], "hypothesis")

    def test_tan_without_header_cards_fail_closed(self) -> None:
        bogus = {
            "frame": "ICRS",
            "epoch": "J2000.0",
            "crpix": [31.5, 31.5],
            "crval_deg": [150.0, -30.0],
            "cd_deg_per_pixel": [[-0.00027, 0.0], [0.0, 0.00027]],
            "pixel_origin": "0-based-image-pixel",
            "projection_model": "TAN",
            "coordinate_standing": "fits-header-tan-hypothesis",
        }
        with self.assertRaisesRegex(Exception, "wcs_header_cards"):
            pixel_to_sky(31.5, 31.5, bogus)

    def test_local_linear_cd_still_labelled_approximation(self) -> None:
        declared = parse_declared_wcs(
            {
                "frame": "ICRS",
                "epoch": "J2000.0",
                "crpix": [50.0, 50.0],
                "crval_deg": [120.0, -45.0],
                "cd_deg_per_pixel": [[1.0 / 3600.0, 0.0], [0.0, 1.0 / 3600.0]],
            }
        )
        self.assertEqual(declared["projection_model"], PROJECTION_MODEL)
        self.assertEqual(declared["coordinate_standing"], "image-space-projection-hypothesis")
        validate_instance("wcs_solution", declared)
        sky = pixel_to_sky_local_linear_cd(50.0, 50.0, declared)
        self.assertAlmostEqual(sky["ra_deg"], 120.0, places=6)

    def test_fits_without_wcs_fail_closed(self) -> None:
        from astropy.io import fits

        path = self.root / "nowcs.fits"
        fits.PrimaryHDU(data=np.zeros((8, 8), dtype=np.float32)).writeto(path)
        before = source_sha256(path)
        with self.assertRaises(FitsWcsUnavailable):
            read_fits_observation(path, require_wcs=True)
        self.assertEqual(before, source_sha256(path))
        result = read_fits_observation(path, require_wcs=False)
        self.assertFalse(result["wcs_present"])
        self.assertIsNone(result["wcs_solution"])
        self.assertFalse(result["coordinates_invented"])

    def test_solve_field_absent_fail_closed(self) -> None:
        if solve_field_available():
            self.skipTest("solve-field present on PATH; absence path not exercisable here")
        path = _write_tan_fits(self.root / "for-solve.fits")
        with self.assertRaisesRegex(SolveFieldUnavailable, "solve-field not available"):
            run_solve_field(path, out_directory=self.root / "solve-out")

    def test_sip_projection_model_when_header_declares_sip(self) -> None:
        path = _write_tan_fits(self.root / "sip.fits", with_sip=True)
        result = read_fits_observation(path)
        self.assertIn(result["projection_model"], {"TAN-SIP", "TAN"})
        validate_instance("wcs_solution", result["wcs_solution"])


if __name__ == "__main__":
    unittest.main()
