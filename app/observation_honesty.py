"""Present-only projection of Operator C / Significance observation honesty records.

Surfaces wcs-solution, sky-localisation, and catalogue-crossmatch fields that are
already present. Never invents WCS or crossmatch values. Never promotes
classification_status to established.
"""

from __future__ import annotations

from typing import Any

# Schema paths as source pointers (repo-relative).
SCHEMA_WCS = "schemas/observation/wcs-solution.schema.json"
SCHEMA_LOC = "schemas/observation/sky-localisation.schema.json"
SCHEMA_XM = "schemas/observation/catalogue-crossmatch.schema.json"

# Localisation / crossmatch classification_status may only be these (never established).
ALLOWED_CLASSIFICATION = frozenset({"hypothesis", "provisional", "unknown"})
ALLOWED_LOC_STATUS = frozenset({"localised", "unavailable", "rejected"})
ALLOWED_RESOLUTION = frozenset({"matched", "unresolved", "contested", "unavailable"})

CONTRACT_DOC = "docs/pipeline/WCS-WHEN-PRESENT-CROSSMATCH-0001.md"
CONTRACT_NOTE = (
    "Operator C honesty-field contract (Significance). Observation evidence records "
    "are present in-repo as schemas + transforms; not yet on universe/objective/receipt. "
    "Wire-in pending Operator C freeze (process_observation / Sky→candidates→Objective)."
)


def _ref(schema_path: str, record_id: str | None = None, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"schema": schema_path, "contract": CONTRACT_DOC}
    if record_id is not None:
        out["record_id"] = record_id
    for key, value in extra.items():
        if value is not None and value != "" and value != []:
            out[key] = value
    return out


def _classification(raw: Any) -> str:
    if raw in ALLOWED_CLASSIFICATION:
        return str(raw)
    return "unknown"


def project_wcs(record: dict[str, Any] | None) -> dict[str, Any] | None:
    """UI: 'WCS declared' + frame/epoch + source_reference if present. Absence = no WCS."""
    if not isinstance(record, dict):
        return None
    if record.get("status") != "declared":
        return None
    frame = record.get("frame")
    epoch = record.get("epoch")
    source_reference = record.get("source_reference")
    text_parts = ["WCS declared"]
    if frame is not None:
        text_parts.append(f"frame={frame}")
    if epoch is not None:
        text_parts.append(f"epoch={epoch}")
    if source_reference:
        text_parts.append(f"source_reference={source_reference}")
    return {
        "kind": "wcs-solution",
        "present": True,
        "status": "declared",
        "epistemic_classification": record.get("epistemic_classification"),
        "frame": frame,
        "epoch": epoch,
        "source_reference": source_reference,
        "text": " · ".join(text_parts),
        "label": "record",
        "source": _ref(SCHEMA_WCS, record.get("id"), source_reference=source_reference),
    }


def project_localisation(record: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(record, dict):
        return None
    status = record.get("status")
    if status not in ALLOWED_LOC_STATUS:
        return None
    classification = _classification(record.get("classification_status"))
    record_id = record.get("id")
    detection_id = record.get("detection_id")
    sky = record.get("sky") if isinstance(record.get("sky"), dict) else {}
    basis = record.get("inference_basis") if isinstance(record.get("inference_basis"), list) else []
    item: dict[str, Any] = {
        "kind": "sky-localisation",
        "id": record_id,
        "detection_id": detection_id,
        "candidate_id": record.get("candidate_id"),
        "status": status,
        "classification_status": classification,
        "wcs_present": record.get("wcs_present"),
        "pixel_centroid": record.get("pixel_centroid"),
        "inference_basis": basis,
        "label": classification,  # never established
        "source": _ref(SCHEMA_LOC, record_id, inference_basis=basis or None),
    }
    if status == "unavailable":
        reason = record.get("unavailable_reason")
        item["unavailable_reason"] = reason
        item["text"] = (
            f"localisation unavailable for detection {detection_id}"
            + (f": {reason}" if reason else " (no invented sky coords)")
        )
        item["sky"] = None
    elif status == "localised":
        item["sky"] = {
            "ra_deg": sky.get("ra_deg"),
            "dec_deg": sky.get("dec_deg"),
            "frame": sky.get("frame"),
            "epoch": sky.get("epoch"),
        }
        item["text"] = (
            f"localised detection {detection_id} → "
            f"ra={sky.get('ra_deg')} deg, dec={sky.get('dec_deg')} deg "
            f"({sky.get('frame')}/{sky.get('epoch')})"
        )
    else:  # rejected
        reason = record.get("unavailable_reason")
        item["unavailable_reason"] = reason
        item["sky"] = None
        item["text"] = f"localisation rejected for detection {detection_id}" + (f": {reason}" if reason else "")
    return item


def project_crossmatch(record: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(record, dict):
        return None
    state = record.get("resolution_state")
    if state not in ALLOWED_RESOLUTION:
        return None
    classification = _classification(record.get("classification_status"))
    evidence_qualified = bool(record.get("evidence_qualified"))
    record_id = record.get("id")
    detection_id = record.get("detection_id")
    candidates = record.get("candidates") if isinstance(record.get("candidates"), list) else []
    provenance = record.get("catalogue_provenance") if isinstance(record.get("catalogue_provenance"), dict) else {}
    basis = record.get("inference_basis") if isinstance(record.get("inference_basis"), list) else []
    item: dict[str, Any] = {
        "kind": "catalogue-crossmatch",
        "id": record_id,
        "localisation_id": record.get("localisation_id"),
        "detection_id": detection_id,
        "resolution_state": state,
        "classification_status": classification,
        "evidence_qualified": evidence_qualified,
        "match_radius_arcsec": record.get("match_radius_arcsec"),
        "candidates": candidates,
        "catalogue_provenance": provenance,
        "inference_basis": basis,
        "label": classification,  # never established
        "source": _ref(
            SCHEMA_XM,
            record_id,
            catalogue_provenance=provenance or None,
            inference_basis=basis or None,
        ),
    }
    if state == "matched" and evidence_qualified:
        sole = candidates[0] if candidates else {}
        item["text"] = (
            f"evidence-qualified match for detection {detection_id}: "
            f"{sole.get('catalogue_name')}/{sole.get('catalogue_id')} "
            f"(sep {sole.get('separation_arcsec')} arcsec) — identity remains {classification}"
        )
    elif state == "matched" and not evidence_qualified:
        # Schema says matched requires evidence_qualified; treat as unresolved for display honesty.
        item["resolution_state"] = "unresolved"
        item["text"] = (
            f"crossmatch for detection {detection_id}: sole hit lacks evidence_ids "
            f"(not evidence-qualified; shown as unresolved)"
        )
    elif state == "contested":
        names = [f"{c.get('catalogue_name')}/{c.get('catalogue_id')}" for c in candidates if isinstance(c, dict)]
        item["text"] = (
            f"contested crossmatch for detection {detection_id}: "
            f"{len(candidates)} candidates within radius — listing without picking a winner: "
            + ", ".join(names)
        )
    elif state == "unavailable":
        reason = record.get("unavailable_reason")
        item["unavailable_reason"] = reason
        item["text"] = f"crossmatch unavailable for detection {detection_id}" + (f": {reason}" if reason else "")
    else:  # unresolved
        reason = record.get("unavailable_reason")
        item["unavailable_reason"] = reason
        item["text"] = (
            f"unresolved crossmatch for detection {detection_id}"
            + (f": {reason}" if reason else f" ({len(candidates)} candidate(s) within radius)")
        )
    return item


def project_observation_evidence(
    *,
    wcs: dict[str, Any] | None = None,
    localisations: list[dict[str, Any]] | None = None,
    crossmatches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the present-only observation honesty block for the app view.

    Empty inputs → present=False (thin-slice Objective path has no observation records yet).
    """
    wcs_view = project_wcs(wcs)
    loc_views = [p for p in (project_localisation(r) for r in (localisations or [])) if p is not None]
    xm_views = [p for p in (project_crossmatch(r) for r in (crossmatches or [])) if p is not None]
    any_present = wcs_view is not None or bool(loc_views) or bool(xm_views)
    return {
        "observation_evidence_schema": "asa-astro-app-observation-honesty-v1",
        "contract": CONTRACT_DOC,
        "contract_note": CONTRACT_NOTE,
        "present": any_present,
        "wcs": wcs_view,
        "localisations": loc_views,
        "crossmatches": xm_views,
        "display_rules": {
            "surface_only_fields_that_are_present": True,
            "always_show_classification_status_and_resolution_state_when_present": True,
            "localisation_crossmatch_classification_status": sorted(ALLOWED_CLASSIFICATION),
            "never_established_from_this_slice": True,
            "matched_requires_evidence_qualified": True,
            "contested_lists_candidates_without_winner": True,
            "absence_of_wcs": "no WCS (do not invent)",
        },
    }
