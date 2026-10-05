"""Detection→catalogue crossmatch (evidence-qualified).

Consumes sky-localised detections and an in-memory catalogue fragment supplied by
the caller. Never fetches or dumps large catalogues to disk. Emits
matched / unresolved / contested / unavailable. Matched requires catalogue
evidence IDs. Classification remains hypothesis — never silently established.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

from .models import record_metadata, stable_id


def angular_separation_arcsec(ra1_deg: float, dec1_deg: float, ra2_deg: float, dec2_deg: float) -> float:
    """Great-circle separation in arcseconds (spherical law of cosines, clamped)."""

    ra1, dec1, ra2, dec2 = map(math.radians, (ra1_deg, dec1_deg, ra2_deg, dec2_deg))
    cos_sep = math.sin(dec1) * math.sin(dec2) + math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2)
    cos_sep = max(-1.0, min(1.0, cos_sep))
    return math.degrees(math.acos(cos_sep)) * 3600.0


def _catalogue_entry_sky(entry: Mapping[str, Any]) -> tuple[float, float]:
    if "ra_deg" in entry and "dec_deg" in entry:
        return float(entry["ra_deg"]), float(entry["dec_deg"])
    sky = entry.get("sky")
    if isinstance(sky, Mapping) and sky.get("ra_deg") is not None and sky.get("dec_deg") is not None:
        return float(sky["ra_deg"]), float(sky["dec_deg"])
    raise ValueError("catalogue entry lacks ra_deg/dec_deg; refusing to invent coordinates")


def _normalise_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
    ra, dec = _catalogue_entry_sky(entry)
    evidence_ids = entry.get("evidence_ids") or []
    if not isinstance(evidence_ids, list) or not all(isinstance(i, str) for i in evidence_ids):
        raise ValueError("catalogue entry evidence_ids must be a list of strings")
    catalogue_id = str(entry.get("catalogue_id") or entry.get("id") or "").strip()
    if not catalogue_id:
        raise ValueError("catalogue entry requires catalogue_id")
    catalogue_name = str(entry.get("catalogue_name") or entry.get("source") or "").strip()
    if not catalogue_name:
        raise ValueError("catalogue entry requires catalogue_name")
    labels = entry.get("labels") or []
    if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
        raise ValueError("catalogue entry labels must be a list of strings")
    return {
        "catalogue_id": catalogue_id,
        "catalogue_name": catalogue_name,
        "ra_deg": ra,
        "dec_deg": dec,
        "frame": str(entry.get("frame") or (entry.get("sky") or {}).get("frame") or "ICRS"),
        "epoch": str(entry.get("epoch") or (entry.get("sky") or {}).get("epoch") or "J2000.0"),
        "evidence_ids": list(evidence_ids),
        "labels": list(labels),
    }


def crossmatch_localisation(
    localisation: Mapping[str, Any],
    catalogue_entries: Sequence[Mapping[str, Any]],
    *,
    match_radius_arcsec: float,
    catalogue_provenance: Mapping[str, Any],
) -> dict[str, Any]:
    """Crossmatch one sky localisation against in-memory catalogue entries.

    Rules:
    - If localisation is not ``localised``, emit ``unavailable`` (fail closed).
    - Within radius: 0 → unresolved; 1 with evidence → matched; 1 without evidence →
      unresolved (evidence-qualified only); >1 → contested.
    - ``classification_status`` is always ``hypothesis``.
    """

    if match_radius_arcsec <= 0:
        raise ValueError("match_radius_arcsec must be > 0")
    required_prov = ("catalogue_name", "release", "query_description")
    missing_prov = [k for k in required_prov if not catalogue_provenance.get(k)]
    if missing_prov:
        raise ValueError(f"catalogue_provenance missing {', '.join(missing_prov)}")

    localisation_id = str(localisation["id"])
    detection_id = str(localisation["detection_id"])
    provenance = {
        "catalogue_name": str(catalogue_provenance["catalogue_name"]),
        "release": str(catalogue_provenance["release"]),
        "query_description": str(catalogue_provenance["query_description"]),
    }
    for optional in ("licence", "snapshot_sha256"):
        if catalogue_provenance.get(optional):
            provenance[optional] = str(catalogue_provenance[optional])

    if localisation.get("status") != "localised":
        reason = localisation.get("unavailable_reason") or "Localisation unavailable; refusing catalogue match without sky coordinates."
        payload = {
            "localisation_id": localisation_id,
            "resolution_state": "unavailable",
            "reason": reason,
        }
        return {
            **record_metadata("inferred"),
            "id": stable_id("xmatch", payload),
            "localisation_id": localisation_id,
            "detection_id": detection_id,
            "resolution_state": "unavailable",
            "classification_status": "unknown",
            "match_radius_arcsec": float(match_radius_arcsec),
            "candidates": [],
            "evidence_qualified": False,
            "catalogue_provenance": provenance,
            "unavailable_reason": reason,
            "inference_basis": [
                "Fail closed: catalogue crossmatch requires a successful WCS-when-present localisation.",
                "Coordinates were not invented.",
                reason,
            ],
        }

    sky = localisation["sky"]
    ra = float(sky["ra_deg"])
    dec = float(sky["dec_deg"])
    normalised = [_normalise_entry(entry) for entry in catalogue_entries]
    within: list[dict[str, Any]] = []
    for entry in normalised:
        sep = angular_separation_arcsec(ra, dec, entry["ra_deg"], entry["dec_deg"])
        if sep <= match_radius_arcsec:
            within.append(
                {
                    "catalogue_id": entry["catalogue_id"],
                    "catalogue_name": entry["catalogue_name"],
                    "separation_arcsec": round(sep, 6),
                    "evidence_ids": sorted(set(entry["evidence_ids"])),
                    "sky": {
                        "ra_deg": entry["ra_deg"],
                        "dec_deg": entry["dec_deg"],
                        "frame": entry["frame"],
                        "epoch": entry["epoch"],
                    },
                    "labels": list(entry["labels"]),
                }
            )
    within.sort(key=lambda item: (item["separation_arcsec"], item["catalogue_id"]))

    if not within:
        resolution_state = "unresolved"
        evidence_qualified = False
        basis = [
            "No catalogue entry lies within the declared match radius.",
            "Detection remains an unresolved sky hypothesis; not an established entity.",
        ]
    elif len(within) == 1 and within[0]["evidence_ids"]:
        resolution_state = "matched"
        evidence_qualified = True
        basis = [
            "Exactly one catalogue entry within radius carries evidence IDs (evidence-qualified).",
            "Match is a hypothesis association; representation is not collapsed into established identity.",
        ]
    elif len(within) == 1:
        # Evidence-qualified only: a sole positional hit without evidence stays unresolved.
        resolution_state = "unresolved"
        evidence_qualified = False
        basis = [
            "Sole positional candidate lacks catalogue evidence_ids; match refused (evidence-qualified only).",
            "Detection remains unresolved; coordinates were not invented.",
        ]
    else:
        resolution_state = "contested"
        evidence_qualified = False
        basis = [
            f"{len(within)} catalogue entries lie within the match radius; association is contested.",
            "Competing candidates retained explicitly; no silent identity promotion.",
        ]

    payload = {
        "localisation_id": localisation_id,
        "resolution_state": resolution_state,
        "radius": match_radius_arcsec,
        "candidate_ids": [c["catalogue_id"] for c in within],
    }
    return {
        **record_metadata("inferred"),
        "id": stable_id("xmatch", payload),
        "localisation_id": localisation_id,
        "detection_id": detection_id,
        "resolution_state": resolution_state,
        "classification_status": "hypothesis",
        "match_radius_arcsec": float(match_radius_arcsec),
        "candidates": within,
        "evidence_qualified": evidence_qualified,
        "catalogue_provenance": provenance,
        "inference_basis": basis,
    }


def crossmatch_localisations(
    localisations: Sequence[Mapping[str, Any]],
    catalogue_entries: Sequence[Mapping[str, Any]],
    *,
    match_radius_arcsec: float,
    catalogue_provenance: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Crossmatch many localisations against the same in-memory catalogue fragment."""

    return [
        crossmatch_localisation(
            loc,
            catalogue_entries,
            match_radius_arcsec=match_radius_arcsec,
            catalogue_provenance=catalogue_provenance,
        )
        for loc in localisations
    ]


__all__ = [
    "angular_separation_arcsec",
    "crossmatch_localisation",
    "crossmatch_localisations",
]
