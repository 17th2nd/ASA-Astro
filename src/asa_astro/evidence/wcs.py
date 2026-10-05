"""WCS-when-present pixel→sky localisation.

Fail closed when WCS is absent or incomplete. Never invent coordinates.
Sky positions derived here remain hypotheses (classification_status=hypothesis).
Source images are not modified; this module only transforms declared pixel centroids.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

from .models import ONTOLOGY_VERSION, SCHEMA_VERSION, record_metadata, stable_id

REQUIRED_WCS_KEYS = ("frame", "epoch", "crpix", "crval_deg", "cd_deg_per_pixel")


class WcsUnavailable(ValueError):
    """Raised when callers demand localisation but WCS is absent or incomplete."""


def _as_pair(value: Any, name: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise WcsUnavailable(f"WCS field {name} must be a length-2 array")
    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError) as exc:
        raise WcsUnavailable(f"WCS field {name} must contain numeric values") from exc


def _as_cd(value: Any) -> tuple[tuple[float, float], tuple[float, float]]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise WcsUnavailable("WCS field cd_deg_per_pixel must be a 2x2 matrix")
    row0 = _as_pair(value[0], "cd_deg_per_pixel[0]")
    row1 = _as_pair(value[1], "cd_deg_per_pixel[1]")
    return row0, row1


def parse_declared_wcs(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate and normalise a caller-declared WCS. Never invents missing fields.

    Returns a schema-shaped ``wcs-solution`` record with status=declared.
    Raises ``WcsUnavailable`` when payload is None/empty/incomplete/invalid.
    """

    if not payload:
        raise WcsUnavailable("WCS absent: no declared astrometric solution was supplied")
    missing = [key for key in REQUIRED_WCS_KEYS if key not in payload or payload[key] is None]
    if missing:
        raise WcsUnavailable(f"WCS incomplete: missing {', '.join(missing)}")

    crpix = _as_pair(payload["crpix"], "crpix")
    crval = _as_pair(payload["crval_deg"], "crval_deg")
    cd = _as_cd(payload["cd_deg_per_pixel"])
    ra_deg, dec_deg = crval
    if not 0.0 <= ra_deg < 360.0:
        raise WcsUnavailable(f"WCS crval ra_deg {ra_deg} outside [0, 360)")
    if not -90.0 <= dec_deg <= 90.0:
        raise WcsUnavailable(f"WCS crval dec_deg {dec_deg} outside [-90, 90]")
    frame = str(payload["frame"]).strip()
    epoch = str(payload["epoch"]).strip()
    if not frame or not epoch:
        raise WcsUnavailable("WCS frame and epoch must be non-empty strings")

    pixel_origin = payload.get("pixel_origin", "0-based-image-pixel")
    if pixel_origin != "0-based-image-pixel":
        raise WcsUnavailable("Only pixel_origin=0-based-image-pixel is supported in this thin slice")

    record: dict[str, Any] = {
        **record_metadata("externally_supplied"),
        "status": "declared",
        "frame": frame,
        "epoch": epoch,
        "crpix": [crpix[0], crpix[1]],
        "crval_deg": [ra_deg, dec_deg],
        "cd_deg_per_pixel": [[cd[0][0], cd[0][1]], [cd[1][0], cd[1][1]]],
        "pixel_origin": "0-based-image-pixel",
    }
    if "source_reference" in payload and payload["source_reference"] is not None:
        record["source_reference"] = str(payload["source_reference"])
    if "notes" in payload and payload["notes"] is not None:
        if not isinstance(payload["notes"], list) or not all(isinstance(n, str) for n in payload["notes"]):
            raise WcsUnavailable("WCS notes must be an array of strings")
        record["notes"] = list(payload["notes"])
    return record


def pixel_to_sky(x: float, y: float, wcs: Mapping[str, Any]) -> dict[str, float | str]:
    """Local linear CD transform: sky = CRVAL + CD · (pixel − CRPIX).

    Uses a local flat-sky approximation (no spherical projection). Suitable for
    small fields supplied with an already-solved CD matrix. Does not invent WCS.
    """

    crpix = _as_pair(wcs["crpix"], "crpix")
    crval = _as_pair(wcs["crval_deg"], "crval_deg")
    cd = _as_cd(wcs["cd_deg_per_pixel"])
    dx = float(x) - crpix[0]
    dy = float(y) - crpix[1]
    dra = cd[0][0] * dx + cd[0][1] * dy
    ddec = cd[1][0] * dx + cd[1][1] * dy
    ra = (crval[0] + dra) % 360.0
    dec = crval[1] + ddec
    if dec > 90.0 or dec < -90.0:
        raise WcsUnavailable(f"projected dec_deg {dec} outside [-90, 90]; WCS or pixel out of range")
    return {
        "ra_deg": ra,
        "dec_deg": dec,
        "frame": str(wcs["frame"]),
        "epoch": str(wcs["epoch"]),
    }


def _unavailable_localisation(
    detection_id: str,
    pixel_centroid: Mapping[str, Any],
    reason: str,
    candidate_id: str | None = None,
) -> dict[str, Any]:
    payload = {
        "detection_id": detection_id,
        "status": "unavailable",
        "reason": reason,
        "pixel": {"x": pixel_centroid.get("x"), "y": pixel_centroid.get("y")},
    }
    record: dict[str, Any] = {
        **record_metadata("computed"),
        "id": stable_id("skyloc", payload),
        "detection_id": detection_id,
        "status": "unavailable",
        "classification_status": "unknown",
        "pixel_centroid": {
            "x": float(pixel_centroid["x"]),
            "y": float(pixel_centroid["y"]),
            "unit": "pixel",
        },
        "sky": {"ra_deg": None, "dec_deg": None, "frame": None, "epoch": None},
        "wcs_present": False,
        "unavailable_reason": reason,
        "inference_basis": [
            "WCS-when-present policy: fail closed when astrometric solution is absent or incomplete.",
            "Coordinates were not invented.",
            reason,
        ],
    }
    if candidate_id:
        record["candidate_id"] = candidate_id
    return record


def localise_detection(
    detection: Mapping[str, Any],
    wcs_payload: Mapping[str, Any] | None,
    *,
    candidate_id: str | None = None,
    fail_closed: bool = True,
) -> dict[str, Any]:
    """Localise one detection's pixel centroid when WCS is present.

    When WCS is absent/incomplete:
    - default ``fail_closed=True`` returns status=unavailable (no invented coords);
    - if a caller mistakenly needs a hard error, pass nothing extra — unavailable is the contract.
    """

    detection_id = str(detection["id"])
    centroid = detection.get("centroid")
    if not isinstance(centroid, Mapping) or "x" not in centroid or "y" not in centroid:
        return _unavailable_localisation(
            detection_id,
            {"x": 0.0, "y": 0.0},
            "Detection lacks a pixel centroid; cannot localise.",
            candidate_id=candidate_id,
        )

    try:
        wcs = parse_declared_wcs(wcs_payload)
    except WcsUnavailable as exc:
        if not fail_closed:
            raise
        return _unavailable_localisation(detection_id, centroid, str(exc), candidate_id=candidate_id)

    sky = pixel_to_sky(float(centroid["x"]), float(centroid["y"]), wcs)
    payload = {
        "detection_id": detection_id,
        "status": "localised",
        "sky": sky,
        "wcs_source": wcs.get("source_reference"),
    }
    record: dict[str, Any] = {
        **record_metadata("computed"),
        "id": stable_id("skyloc", payload),
        "detection_id": detection_id,
        "status": "localised",
        "classification_status": "hypothesis",
        "pixel_centroid": {
            "x": float(centroid["x"]),
            "y": float(centroid["y"]),
            "unit": "pixel",
        },
        "sky": {
            "ra_deg": sky["ra_deg"],
            "dec_deg": sky["dec_deg"],
            "frame": sky["frame"],
            "epoch": sky["epoch"],
        },
        "wcs_present": True,
        "inference_basis": [
            "Pixel centroid projected through caller-declared WCS (local linear CD).",
            "Sky position is a hypothesis derived from declared calibration; not an established identity.",
            "Source image bytes were not modified.",
        ],
    }
    if candidate_id:
        record["candidate_id"] = candidate_id
    return record


def localise_detections(
    detections: Sequence[Mapping[str, Any]],
    wcs_payload: Mapping[str, Any] | None,
    *,
    candidate_ids: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Localise many detections. Fail closed per detection when WCS absent."""

    ids = candidate_ids or {}
    return [
        localise_detection(det, wcs_payload, candidate_id=ids.get(str(det["id"])))
        for det in detections
    ]


__all__ = [
    "WcsUnavailable",
    "parse_declared_wcs",
    "pixel_to_sky",
    "localise_detection",
    "localise_detections",
    "SCHEMA_VERSION",
    "ONTOLOGY_VERSION",
]
