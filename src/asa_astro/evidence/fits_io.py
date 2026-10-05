"""Safe FITS observation read + header WCS extraction (P2 / S2).

Rules:
- Source FITS bytes are never mutated (read-only open; no writeto on the source path).
- Coordinates are never invented: absent/incomplete WCS → fail closed.
- FITS TAN (minimum) and TAN-SIP via pinned ``astropy.wcs`` when headers support it.
- ``local-linear-CD`` remains a separately labelled approximation for simple metadata WCS
  (see ``wcs.parse_declared_wcs``); this module emits ``projection_model`` of
  ``TAN`` / ``TAN-SIP`` / ``other-fits-wcs`` as appropriate.
- Pixel grid in returned WCS records is **0-based image pixels** (FITS CRPIX is 1-based;
  converted on extract).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from .models import record_metadata
from .wcs import WcsUnavailable

ASTROPY_PIN = "6.1.7"


class FitsReadError(ValueError):
    """FITS could not be read safely or lacked required structure."""


class FitsWcsUnavailable(WcsUnavailable):
    """FITS present but no usable WCS headers (fail closed; coords not invented)."""


def _require_astropy():
    try:
        from astropy.io import fits  # noqa: F401
        from astropy.wcs import WCS  # noqa: F401
        import astropy
    except ImportError as exc:
        raise FitsReadError(
            f"astropy is required for FITS I/O (pinned {ASTROPY_PIN}); not installed: {exc}"
        ) from exc
    return astropy


def source_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _header_get(header: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in header and header[key] is not None:
            return header[key]
    return None


def _ctype_pair(header: Mapping[str, Any]) -> tuple[str, str]:
    c1 = str(_header_get(header, "CTYPE1") or "").strip().upper()
    c2 = str(_header_get(header, "CTYPE2") or "").strip().upper()
    return c1, c2


def _projection_model_from_ctypes(ctype1: str, ctype2: str, wcs_obj: Any) -> str:
    joined = f"{ctype1}+{ctype2}"
    sip = bool(getattr(wcs_obj, "sip", None) is not None)
    if "TAN-SIP" in ctype1 or "TAN-SIP" in ctype2 or (sip and "TAN" in ctype1):
        return "TAN-SIP"
    if "TAN" in ctype1 and "TAN" in ctype2:
        return "TAN"
    if ctype1 or ctype2:
        return "other-fits-wcs"
    raise FitsWcsUnavailable(f"FITS CTYPE not usable for sky projection: {joined!r}")


def _frame_epoch_from_header(header: Mapping[str, Any]) -> tuple[str, str]:
    # Prefer explicit RADESYS / EQUINOX; default ICRS/J2000 only when headers are sky-celestial.
    radesys = _header_get(header, "RADESYS", "RADECSYS")
    equinox = _header_get(header, "EQUINOX", "EPOCH")
    frame = str(radesys).strip() if radesys else "ICRS"
    if equinox is None:
        epoch = "J2000.0"
    else:
        try:
            epoch = f"J{float(equinox):.1f}"
        except (TypeError, ValueError):
            epoch = str(equinox).strip() or "J2000.0"
    return frame, epoch


def _cd_matrix_deg(wcs_obj: Any) -> list[list[float]]:
    """Return 2x2 CD in degrees/pixel from astropy WCS (for transparency / fallbacks)."""
    # astropy pixel_scale_matrix is degrees per pixel when cunit is deg.
    try:
        matrix = wcs_obj.pixel_scale_matrix
        return [[float(matrix[0, 0]), float(matrix[0, 1])], [float(matrix[1, 0]), float(matrix[1, 1])]]
    except Exception as exc:  # noqa: BLE001 — fail closed rather than invent
        raise FitsWcsUnavailable(f"unable to derive CD matrix from FITS WCS: {exc}") from exc



def _minimal_wcs_header_cards(header: Mapping[str, Any]) -> dict[str, Any]:
    """Copy WCS-relevant FITS cards for round-trip projection (present-only; no invention)."""
    keys = [
        "WCSAXES", "CRPIX1", "CRPIX2", "CRVAL1", "CRVAL2",
        "CTYPE1", "CTYPE2", "CUNIT1", "CUNIT2",
        "CD1_1", "CD1_2", "CD2_1", "CD2_2",
        "PC1_1", "PC1_2", "PC2_1", "PC2_2",
        "CDELT1", "CDELT2", "CROTA2",
        "LONPOLE", "LATPOLE", "RADESYS", "RADECSYS", "EQUINOX", "EPOCH",
        "PV1_0", "PV1_1", "PV1_2", "PV2_0", "PV2_1", "PV2_2",
    ]
    # SIP coefficients if present
    for a_order in range(0, 10):
        for i in range(0, a_order + 1):
            j = a_order - i
            keys.append(f"A_{i}_{j}")
            keys.append(f"B_{i}_{j}")
            keys.append(f"AP_{i}_{j}")
            keys.append(f"BP_{i}_{j}")
    keys.extend(["A_ORDER", "B_ORDER", "AP_ORDER", "BP_ORDER"])
    out: dict[str, Any] = {}
    for key in keys:
        if key in header and header[key] is not None:
            val = header[key]
            out[key] = val if isinstance(val, (int, float, str, bool)) else str(val)
    return out


def extract_wcs_from_fits_header(
    header: Mapping[str, Any],
    *,
    source_reference: str | None = None,
) -> dict[str, Any]:
    """Build a wcs-solution record from a FITS header via ``astropy.wcs.WCS``.

    Never invents CRVAL/CD/CTYPE. Raises ``FitsWcsUnavailable`` when headers are
    insufficient for a celestial WCS.
    """

    _require_astropy()
    from astropy.wcs import WCS
    from astropy.wcs import FITSFixedWarning
    import warnings

    ctype1, ctype2 = _ctype_pair(header)
    if not ctype1 or not ctype2:
        raise FitsWcsUnavailable("FITS WCS incomplete: missing CTYPE1/CTYPE2")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        try:
            wcs_obj = WCS(header, naxis=2, relax=True)
        except Exception as exc:  # noqa: BLE001
            raise FitsWcsUnavailable(f"astropy.wcs failed to parse FITS header: {exc}") from exc

    if not getattr(wcs_obj, "has_celestial", False):
        # Older astropy: has_celestial may be property; also check ctype.
        if "RA" not in ctype1 and "GLON" not in ctype1:
            raise FitsWcsUnavailable("FITS WCS is not celestial; refusing to invent sky frame")

    try:
        # CRPIX in FITS is 1-based; our pipeline uses 0-based image pixels.
        crpix_fits = [float(wcs_obj.wcs.crpix[0]), float(wcs_obj.wcs.crpix[1])]
    except Exception as exc:  # noqa: BLE001
        raise FitsWcsUnavailable(f"FITS WCS missing CRPIX: {exc}") from exc
    crpix_0based = [crpix_fits[0] - 1.0, crpix_fits[1] - 1.0]

    try:
        crval = [float(wcs_obj.wcs.crval[0]), float(wcs_obj.wcs.crval[1])]
    except Exception as exc:  # noqa: BLE001
        raise FitsWcsUnavailable(f"FITS WCS missing CRVAL: {exc}") from exc

    ra_deg, dec_deg = crval[0] % 360.0, crval[1]
    if not -90.0 <= dec_deg <= 90.0:
        raise FitsWcsUnavailable(f"FITS CRVAL dec_deg {dec_deg} outside [-90, 90]")

    projection_model = _projection_model_from_ctypes(ctype1, ctype2, wcs_obj)
    cd = _cd_matrix_deg(wcs_obj)
    frame, epoch = _frame_epoch_from_header(header)

    standing = (
        "fits-header-tan-sip-hypothesis"
        if projection_model == "TAN-SIP"
        else "fits-header-tan-hypothesis"
        if projection_model == "TAN"
        else "fits-header-wcs-hypothesis"
    )

    record: dict[str, Any] = {
        **record_metadata("externally_supplied"),
        "status": "declared",
        "frame": frame,
        "epoch": epoch,
        "crpix": crpix_0based,
        "crval_deg": [ra_deg, dec_deg],
        "cd_deg_per_pixel": cd,
        "pixel_origin": "0-based-image-pixel",
        "projection_model": projection_model,
        "coordinate_standing": standing,
        "fits_crpix_1based": crpix_fits,
        "fits_ctype": [ctype1, ctype2],
        "wcs_library": f"astropy.wcs=={ASTROPY_PIN}",
        "wcs_header_cards": _minimal_wcs_header_cards(header),
        "notes": [
            "Extracted from FITS header via astropy.wcs; source FITS bytes were not modified.",
            "CRPIX converted from FITS 1-based to 0-based image pixels for detection centroids.",
            "Sky positions remain hypotheses until independently validated.",
            "local-linear-CD is a separate approximation path for simple declared metadata WCS; "
            f"this record uses projection_model={projection_model}.",
        ],
    }
    if source_reference:
        record["source_reference"] = source_reference
    return record


def extract_observation_metadata_from_header(header: Mapping[str, Any]) -> dict[str, Any]:
    """Present-only time / instrument / filter / pointing / scale from FITS cards."""

    def present(key: str, *alts: str) -> dict[str, Any]:
        value = _header_get(header, key, *alts)
        if value is None:
            return {"status": "absent", "value": None, "card": key}
        return {"status": "present", "value": value if isinstance(value, (int, float, str)) else str(value), "card": key}

    # Scale: prefer CD-derived later; expose CDELT when present.
    cdelt1 = _header_get(header, "CDELT1")
    cdelt2 = _header_get(header, "CDELT2")
    scale: dict[str, Any]
    if cdelt1 is not None and cdelt2 is not None:
        scale = {
            "status": "present",
            "cdelt_deg": [float(cdelt1), float(cdelt2)],
            "note": "Raw CDELT from header; prefer WCS CD/PC via extract_wcs_from_fits_header for geometry.",
        }
    else:
        scale = {"status": "absent", "cdelt_deg": None, "note": "CDELT not present; use WCS CD matrix when available."}

    pointing = {
        "ra_card": present("CRVAL1"),
        "dec_card": present("CRVAL2"),
        "object": present("OBJECT"),
        "telescop": present("TELESCOP"),
    }

    return {
        "time": {
            "date_obs": present("DATE-OBS", "DATEOBS"),
            "mjd_obs": present("MJD-OBS", "MJDOBS"),
            "exptime_s": present("EXPTIME", "EXPOSURE"),
        },
        "instrument": {
            "instrument": present("INSTRUME", "INSTRUMENT"),
            "telescope": present("TELESCOP"),
            "detector": present("DETECTOR"),
            "observatory": present("OBSERVAT"),
        },
        "filter": {
            "filter": present("FILTER", "FILTER1", "FILTNAM1"),
        },
        "pointing": pointing,
        "scale": scale,
    }


def read_fits_observation(
    path: str | Path,
    *,
    hdu_index: int | None = None,
    require_wcs: bool = True,
) -> dict[str, Any]:
    """Read a FITS file without mutating source bytes; extract metadata (+ WCS when present).

    Parameters
    ----------
    path:
        Filesystem path to the FITS file.
    hdu_index:
        Optional HDU index with WCS. When None, the first HDU with celestial WCS is used
        (primary then extensions). Fail closed if none qualify and ``require_wcs``.
    require_wcs:
        When True (default), raise ``FitsWcsUnavailable`` if no celestial WCS is found.
        When False, return ``wcs_solution=None`` with honesty flags.
    """

    astropy = _require_astropy()
    from astropy.io import fits

    input_path = Path(path)
    if not input_path.is_file():
        raise FitsReadError(f"FITS path does not exist: {input_path}")

    before = source_sha256(input_path)
    byte_size = input_path.stat().st_size

    # Read-only; never writeto the source path.
    with fits.open(input_path, mode="readonly", memmap=False) as hdul:
        hdu_summaries = []
        chosen = None
        chosen_index = None
        indices = range(len(hdul)) if hdu_index is None else [hdu_index]
        for idx in indices:
            hdu = hdul[idx]
            header = hdu.header
            summary = {
                "index": idx,
                "name": hdu.name,
                "xtension": header.get("XTENSION"),
                "naxis": int(header.get("NAXIS") or 0),
                "naxis1": header.get("NAXIS1"),
                "naxis2": header.get("NAXIS2"),
                "has_ctype": bool(header.get("CTYPE1") and header.get("CTYPE2")),
            }
            hdu_summaries.append(summary)
            if chosen is not None:
                continue
            if not summary["has_ctype"]:
                continue
            try:
                wcs_record = extract_wcs_from_fits_header(
                    header,
                    source_reference=f"fits:{input_path.name}#hdu{idx}",
                )
            except FitsWcsUnavailable:
                continue
            chosen = (header, wcs_record)
            chosen_index = idx

        after_open_sha = source_sha256(input_path)
        if after_open_sha != before:
            raise FitsReadError("FITS source bytes changed during read; refusing to continue")

        header_meta = None
        wcs_solution = None
        if chosen is not None:
            header, wcs_solution = chosen
            header_meta = extract_observation_metadata_from_header(header)
        elif require_wcs:
            raise FitsWcsUnavailable(
                "Fail closed: no celestial FITS WCS found in any inspected HDU; "
                "coordinates were not invented."
            )

    after = source_sha256(input_path)
    if after != before:
        raise FitsReadError("FITS source bytes changed after read; refusing to continue")

    return {
        "schema": "asa-astro-fits-observation-read-v1",
        "path": str(input_path),
        "original_filename": input_path.name,
        "sha256": before,
        "byte_size": byte_size,
        "source_image_mutated": False,
        "astropy_version": astropy.__version__,
        "astropy_pin_expected": ASTROPY_PIN,
        "hdu_index": chosen_index,
        "hdus": hdu_summaries,
        "header_metadata": header_meta,
        "wcs_solution": wcs_solution,
        "wcs_present": wcs_solution is not None,
        "coordinates_invented": False,
        "projection_model": (wcs_solution or {}).get("projection_model"),
        "coordinate_standing": (wcs_solution or {}).get("coordinate_standing"),
    }


def pixel_to_sky_fits_wcs(
    x: float,
    y: float,
    fits_header: Mapping[str, Any],
) -> dict[str, float | str]:
    """Project a 0-based image pixel through FITS header WCS via astropy (TAN/SIP capable).

    Does not invent WCS. Raises ``FitsWcsUnavailable`` on failure.
    """

    _require_astropy()
    from astropy.wcs import WCS
    from astropy.wcs import FITSFixedWarning
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        try:
            wcs_obj = WCS(fits_header, naxis=2, relax=True)
        except Exception as exc:  # noqa: BLE001
            raise FitsWcsUnavailable(f"astropy.wcs failed: {exc}") from exc

    # astropy.wcs.WCS.pixel_to_world uses origin=0 (0-based image pixels) by default —
    # matching our detection centroid convention after CRPIX conversion.
    try:
        sky = wcs_obj.pixel_to_world(float(x), float(y))
    except Exception as exc:  # noqa: BLE001
        raise FitsWcsUnavailable(f"pixel_to_world failed: {exc}") from exc

    # SkyCoord → ra/dec degrees
    try:
        ra = float(sky.ra.deg) % 360.0
        dec = float(sky.dec.deg)
    except Exception:
        # Some WCS return tuple of quantities
        ra = float(sky[0].deg) % 360.0 if hasattr(sky[0], "deg") else float(sky[0]) % 360.0
        dec = float(sky[1].deg) if hasattr(sky[1], "deg") else float(sky[1])

    if not -90.0 <= dec <= 90.0:
        raise FitsWcsUnavailable(f"projected dec_deg {dec} outside [-90, 90]")

    frame, epoch = _frame_epoch_from_header(fits_header)
    return {"ra_deg": ra, "dec_deg": dec, "frame": frame, "epoch": epoch}


__all__ = [
    "ASTROPY_PIN",
    "FitsReadError",
    "FitsWcsUnavailable",
    "read_fits_observation",
    "extract_wcs_from_fits_header",
    "extract_observation_metadata_from_header",
    "pixel_to_sky_fits_wcs",
    "source_sha256",
]
