"""Observed-vs-expected residuals + missing-expected + next-evidence recommendations.

Plain-language fields are shaped for the Action honesty UI. Hypothesis vs established
is preserved: residuals never promote catalogue association to established identity.
Fail closed when observed sky coordinates are unavailable (never invent).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from asa_astro.evidence.crossmatch import angular_separation_arcsec
from astro_exec.core.canonical_json import canonical_text
from asa_astro.evidence.wcs import compute_coordinates_invented


class ResidualsError(ValueError):
    """Residuals computation refused (fail closed)."""


def _plain_sep(sep: float | None) -> str:
    if sep is None:
        return "unknown"
    if sep < 1.0:
        return f"{sep:.2f} arcsec"
    if sep < 60.0:
        return f"{sep:.1f} arcsec"
    return f"{sep / 60.0:.2f} arcmin"


def _expected_sky(entry: Mapping[str, Any]) -> tuple[float, float]:
    if "ra_deg" in entry and "dec_deg" in entry:
        return float(entry["ra_deg"]), float(entry["dec_deg"])
    sky = entry.get("sky")
    if isinstance(sky, Mapping) and sky.get("ra_deg") is not None and sky.get("dec_deg") is not None:
        return float(sky["ra_deg"]), float(sky["dec_deg"])
    raise ResidualsError("expected entry lacks ra_deg/dec_deg; refusing to invent coordinates")


def _normalise_expected(entry: Mapping[str, Any]) -> dict[str, Any]:
    ra, dec = _expected_sky(entry)
    catalogue_id = str(entry.get("catalogue_id") or entry.get("id") or "").strip()
    if not catalogue_id:
        raise ResidualsError("expected entry requires catalogue_id")
    labels = entry.get("labels") or []
    if not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
        raise ResidualsError("expected entry labels must be a list of strings")
    return {
        "catalogue_id": catalogue_id,
        "catalogue_name": str(entry.get("catalogue_name") or entry.get("source") or "expected-catalogue"),
        "ra_deg": ra,
        "dec_deg": dec,
        "frame": str(entry.get("frame") or (entry.get("sky") or {}).get("frame") or "ICRS"),
        "epoch": str(entry.get("epoch") or (entry.get("sky") or {}).get("epoch") or "J2000.0"),
        "labels": list(labels),
        "evidence_ids": list(entry.get("evidence_ids") or []),
    }


def compute_observed_vs_expected(
    localisations: Sequence[Mapping[str, Any]],
    expected_entries: Sequence[Mapping[str, Any]],
    *,
    crossmatches: Sequence[Mapping[str, Any]] | None = None,
    match_radius_arcsec: float = 5.0,
    residual_tolerance_arcsec: float = 2.0,
) -> dict[str, Any]:
    """Compare observed sky localisations to expected catalogue positions.

    Returns Action-UI-oriented plain language fields without promoting identity.
    """

    if match_radius_arcsec <= 0 or residual_tolerance_arcsec <= 0:
        raise ResidualsError("radii must be > 0")

    expected = [_normalise_expected(e) for e in expected_entries]
    xm_by_det = {str(x["detection_id"]): x for x in (crossmatches or [])}

    residuals: list[dict[str, Any]] = []
    claimed_expected: set[str] = set()

    for loc in sorted(localisations, key=lambda item: str(item.get("id") or item.get("detection_id"))):
        detection_id = str(loc["detection_id"])
        xm = xm_by_det.get(detection_id)
        base = {
            "detection_id": detection_id,
            "localisation_id": str(loc.get("id") or ""),
            "candidate_id": loc.get("candidate_id"),
            "classification_status": "hypothesis",
            "established_identity": False,
        }

        if loc.get("status") != "localised":
            reason = loc.get("unavailable_reason") or "Sky localisation unavailable (WCS absent or incomplete)."
            residuals.append(
                {
                    **base,
                    "status": "unlocalised",
                    "observed_sky": None,
                    "expected": None,
                    "separation_arcsec": None,
                    "within_tolerance": False,
                    "plain_language": (
                        f"No sky position for detection {detection_id}: {reason} "
                        "Coordinates were not invented."
                    ),
                    "plain_language_short": "Not localised — WCS missing; no residual.",
                }
            )
            continue

        sky = loc["sky"]
        ra = float(sky["ra_deg"])
        dec = float(sky["dec_deg"])
        observed = {
            "ra_deg": ra,
            "dec_deg": dec,
            "frame": sky.get("frame") or "ICRS",
            "epoch": sky.get("epoch") or "J2000.0",
        }

        # Prefer evidence-qualified crossmatch hit when present; else nearest expected.
        chosen: dict[str, Any] | None = None
        sep: float | None = None
        if xm and xm.get("resolution_state") == "matched" and xm.get("evidence_qualified") and xm.get("candidates"):
            hit = xm["candidates"][0]
            chosen = {
                "catalogue_id": hit["catalogue_id"],
                "catalogue_name": hit["catalogue_name"],
                "ra_deg": hit["sky"]["ra_deg"],
                "dec_deg": hit["sky"]["dec_deg"],
                "labels": list(hit.get("labels") or []),
                "evidence_ids": list(hit.get("evidence_ids") or []),
                "via": "evidence_qualified_crossmatch",
            }
            sep = float(hit["separation_arcsec"])
        else:
            best = None
            for exp in expected:
                s = angular_separation_arcsec(ra, dec, exp["ra_deg"], exp["dec_deg"])
                if s <= match_radius_arcsec and (best is None or s < best[0]):
                    best = (s, exp)
            if best is not None:
                sep, exp = best
                chosen = {
                    "catalogue_id": exp["catalogue_id"],
                    "catalogue_name": exp["catalogue_name"],
                    "ra_deg": exp["ra_deg"],
                    "dec_deg": exp["dec_deg"],
                    "labels": list(exp["labels"]),
                    "evidence_ids": list(exp["evidence_ids"]),
                    "via": "nearest_expected_within_radius",
                }

        if chosen is None:
            residuals.append(
                {
                    **base,
                    "status": "unmatched",
                    "observed_sky": observed,
                    "expected": None,
                    "separation_arcsec": None,
                    "within_tolerance": False,
                    "plain_language": (
                        f"Observed sky candidate at RA {ra:.5f}°, Dec {dec:.5f}° has no expected "
                        f"catalogue source within {_plain_sep(match_radius_arcsec)}. "
                        "Treated as an unresolved hypothesis, not an established identity."
                    ),
                    "plain_language_short": "Observed with no nearby expected source (hypothesis).",
                }
            )
            continue

        claimed_expected.add(chosen["catalogue_id"])
        within = sep is not None and sep <= residual_tolerance_arcsec
        status = "within_tolerance" if within else "offset"
        residuals.append(
            {
                **base,
                "status": status,
                "observed_sky": observed,
                "expected": chosen,
                "separation_arcsec": None if sep is None else round(sep, 6),
                "within_tolerance": within,
                "residual_tolerance_arcsec": residual_tolerance_arcsec,
                "plain_language": (
                    f"Observed candidate is {_plain_sep(sep)} from expected {chosen['catalogue_id']} "
                    f"({chosen['catalogue_name']}). "
                    + (
                        "Within declared residual tolerance (hypothesis association only)."
                        if within
                        else "Outside residual tolerance — investigate WCS or catalogue epoch (still hypothesis)."
                    )
                ),
                "plain_language_short": (
                    f"{_plain_sep(sep)} from {chosen['catalogue_id']} "
                    + ("(OK)" if within else "(offset)")
                ),
            }
        )

    missing_expected: list[dict[str, Any]] = []
    for exp in expected:
        if exp["catalogue_id"] in claimed_expected:
            continue
        missing_expected.append(
            {
                "catalogue_id": exp["catalogue_id"],
                "catalogue_name": exp["catalogue_name"],
                "expected_sky": {
                    "ra_deg": exp["ra_deg"],
                    "dec_deg": exp["dec_deg"],
                    "frame": exp["frame"],
                    "epoch": exp["epoch"],
                },
                "labels": list(exp["labels"]),
                "classification_status": "hypothesis",
                "established_identity": False,
                "plain_language": (
                    f"Expected catalogue source {exp['catalogue_id']} ({exp['catalogue_name']}) "
                    f"at RA {exp['ra_deg']:.5f}°, Dec {exp['dec_deg']:.5f}° was not matched to any "
                    "observed sky-localised detection within the match radius."
                ),
                "plain_language_short": f"Missing expected {exp['catalogue_id']}.",
                "next_evidence": (
                    "Re-observe the field with verified WCS, or confirm the expected source falls "
                    "inside the detector footprint and detection threshold."
                ),
            }
        )

    recommendations = _recommendations(residuals, missing_expected, localisations)
    coordinates_invented = compute_coordinates_invented(localisations)

    unlocalised = sum(1 for r in residuals if r["status"] == "unlocalised")
    return {
        "schema": "asa-astro-observed-vs-expected-v1",
        "epistemic": {
            "residuals_are": "hypothesis",
            "established_identity_promoted": False,
            "coordinates_invented": coordinates_invented,
            "catalogue_match_promotes_identity": False,
        },
        "parameters": {
            "match_radius_arcsec": float(match_radius_arcsec),
            "residual_tolerance_arcsec": float(residual_tolerance_arcsec),
        },
        "summary": {
            "observed_localisation_count": len(localisations),
            "residual_count": len(residuals),
            "within_tolerance_count": sum(1 for r in residuals if r["status"] == "within_tolerance"),
            "offset_count": sum(1 for r in residuals if r["status"] == "offset"),
            "unmatched_count": sum(1 for r in residuals if r["status"] == "unmatched"),
            "unlocalised_count": unlocalised,
            "missing_expected_count": len(missing_expected),
            "wcs_fail_closed": unlocalised > 0 and unlocalised == len(localisations),
        },
        "residuals": residuals,
        "missing_expected": missing_expected,
        "next_evidence_recommendations": recommendations,
        # Action UI convenience aggregates
        "action_ui": {
            "headline": _headline(residuals, missing_expected),
            "residual_lines": [r["plain_language_short"] for r in residuals],
            "missing_lines": [m["plain_language_short"] for m in missing_expected],
            "recommendation_lines": [r["plain_language"] for r in recommendations],
            "honesty": {
                "hypothesis_only": True,
                "established_identity_promoted": False,
                "coordinates_invented": coordinates_invented,
            },
        },
    }


def _headline(residuals: list[dict[str, Any]], missing: list[dict[str, Any]]) -> str:
    if residuals and all(r["status"] == "unlocalised" for r in residuals):
        return "No sky residuals: WCS absent — fail closed; coordinates not invented."
    ok = sum(1 for r in residuals if r["status"] == "within_tolerance")
    off = sum(1 for r in residuals if r["status"] == "offset")
    unmatched = sum(1 for r in residuals if r["status"] == "unmatched")
    parts = [f"{ok} within tolerance", f"{off} offset", f"{unmatched} unmatched", f"{len(missing)} missing expected"]
    return "Observed vs expected (hypothesis): " + "; ".join(parts) + "."


def _recommendations(
    residuals: list[dict[str, Any]],
    missing: list[dict[str, Any]],
    localisations: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    recs: list[dict[str, Any]] = []
    priority = 1
    if residuals and all(r["status"] == "unlocalised" for r in residuals):
        recs.append(
            {
                "priority": priority,
                "code": "supply_declared_wcs",
                "action": "supply_declared_wcs",
                "plain_language": (
                    "Provide a declared WCS solution (or plate-solve receipt) for this observation "
                    "before comparing to catalogue expectations."
                ),
                "reason": "All detections are unlocalised; residuals cannot be computed without inventing coordinates.",
            }
        )
        priority += 1
    if any(r["status"] == "offset" for r in residuals):
        recs.append(
            {
                "priority": priority,
                "code": "verify_wcs_or_epoch",
                "action": "verify_wcs_or_catalogue_epoch",
                "plain_language": (
                    "Check the declared WCS and catalogue epoch: one or more observed positions "
                    "sit outside the residual tolerance of their expected counterparts."
                ),
                "reason": "Offset residuals present.",
            }
        )
        priority += 1
    if missing:
        recs.append(
            {
                "priority": priority,
                "code": "recover_missing_expected",
                "action": "deeper_or_retargeted_observation",
                "plain_language": (
                    f"{len(missing)} expected catalogue source(s) were not seen. "
                    "Confirm footprint coverage, then obtain deeper imaging or a lower detection threshold."
                ),
                "reason": "missing_expected non-empty",
            }
        )
        priority += 1
    if any(r["status"] == "unmatched" for r in residuals):
        recs.append(
            {
                "priority": priority,
                "code": "characterise_unmatched",
                "action": "characterise_unmatched_hypothesis",
                "plain_language": (
                    "Unmatched observed candidates remain hypotheses. Obtain confirmatory astrometry "
                    "or photometry before any identity claim."
                ),
                "reason": "unmatched observed sky candidates",
            }
        )
        priority += 1
    if not recs:
        recs.append(
            {
                "priority": 1,
                "code": "maintain_hypothesis_label",
                "action": "keep_hypothesis_label",
                "plain_language": (
                    "Residuals are within tolerance. Keep hypothesis labels; do not promote to "
                    "established identity without an explicit evidenced resolution step."
                ),
                "reason": "no offset/missing/unmatched issues",
            }
        )
    # Stable ordering
    recs.sort(key=lambda item: (item["priority"], item["code"]))
    return recs


def write_observed_vs_expected(report: Mapping[str, Any], path: str | Path) -> Path:
    """Write residuals report as canonical JSON (no large dumps)."""

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(canonical_text(dict(report)) + "\n", encoding="utf-8")
    return out


def compute_from_observation_bundle(
    bundle_directory: str | Path,
    expected_entries: Sequence[Mapping[str, Any]],
    **kwargs: Any,
) -> dict[str, Any]:
    """Load sky localisations (+ optional crossmatches) from an observe bundle."""

    root = Path(bundle_directory)
    sky_path = root / "sky_localisations.json"
    if not sky_path.is_file():
        raise ResidualsError(f"Fail closed: missing {sky_path.name}")
    sky = json.loads(sky_path.read_text(encoding="utf-8"))
    localisations = sky.get("localisations") or []
    crossmatches = None
    cross_path = root / "catalogue_crossmatches.json"
    if cross_path.is_file():
        crossmatches = json.loads(cross_path.read_text(encoding="utf-8")).get("crossmatches") or []
    return compute_observed_vs_expected(
        localisations, expected_entries, crossmatches=crossmatches, **kwargs
    )


__all__ = [
    "ResidualsError",
    "compute_observed_vs_expected",
    "write_observed_vs_expected",
    "compute_from_observation_bundle",
]
