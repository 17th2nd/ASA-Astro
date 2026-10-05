"""Thin harness: sky-localised candidates → temporary universe → Objective evaluate + receipt.

Rules enforced:
- Fail closed when no successful (status=localised) sky localisations exist.
- Never invent coordinates.
- Every derived sky entity is classified as **hypothesis**, never established.
- Catalogue associations remain hypothesis; matched only if evidence-qualified upstream.
- Source images are not touched (this module consumes localisation records only).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from astro.domain import (
    Coordinates,
    Entity,
    EntityState,
    EvidenceRecord,
    Provenance,
    Universe,
)
from astro.objectives import Objective, ObservingContext
from astro.pipeline import decide, open_or_bootstrap
from astro_exec.core.canonical_json import canonical_text


class SkyToObjectiveBridgeError(ValueError):
    """Bridge refused to proceed (fail closed)."""


SITE_DESIGNATION = "SYN-SITE-SKY-BRIDGE"
TELESCOPE_DESIGNATION = "SYN-SCOPE-SKY-BRIDGE"
AS_OF_DEFAULT = "2026-10-05T08:00:00Z"
WINDOW_START_DEFAULT = "2026-10-05T09:00:00Z"
WINDOW_END_DEFAULT = "2026-10-05T19:00:00Z"


def default_sky_candidate_objective() -> Objective:
    """Minimal objective for sky-localised observation candidates (hypothesis path)."""

    return Objective.declare(
        name="Sky-localised candidate characterisation",
        version="0.1.0",
        purpose_class="characterisation",
        question=(
            "Which sky-localised observation candidates warrant follow-up characterisation "
            "under declared WCS, without treating them as established sky identities?"
        ),
        authority="Operator-C asa-astro-v1-application sky→Objective thin harness",
        target_kinds=["candidate"],
        required_evidence=["astrometry"],
        eligible_relationship_types=[],
        unevaluated_relationships="exclude",
        missingness_policy="indeterminate",
        exclusions=["apparent_brightness_as_relevance", "silent_identity_promotion"],
        explanation_threshold=0.2,
        features=[
            {
                "name": "visibility",
                "weight": 3.0,
                "required": True,
                "params": {"min_altitude_deg": 20},
                "rationale": "Follow-up must be geometrically feasible from the declared site in the window.",
            },
            {
                "name": "candidate_status",
                "weight": 2.0,
                "required": False,
                "params": {
                    "values": {"candidate": 1.0, "confirmed": 0.2, "none": 0.4, "rejected": 0.0}
                },
                "rationale": "Hypothesis candidates gain most from characterisation; confirmed identities are deprioritised here.",
            },
            {
                "name": "evidence_scarcity",
                "weight": 2.0,
                "required": False,
                "params": {"needed": 2, "evidence_kinds": ["astrometry", "photometry"]},
                "rationale": "Sparse evidence increases the information value of one more measurement.",
            },
            {
                "name": "observation_gap",
                "weight": 1.0,
                "required": False,
                "params": {"cadence_hours": 24, "evidence_kinds": ["astrometry", "photometry"]},
                "rationale": "Recent cadence gaps flag candidates needing renewed coverage.",
            },
        ],
        plan={"action": "characterise_sky_candidate", "max_targets": 3, "duration_minutes": 20, "min_score": 0.2},
    )


def _write_json(path: Path, value: Any) -> None:
    path.write_text(canonical_text(value) + "\n", encoding="utf-8")


def _localised_only(localisations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in localisations:
        if item.get("status") != "localised":
            continue
        sky = item.get("sky") or {}
        if sky.get("ra_deg") is None or sky.get("dec_deg") is None:
            raise SkyToObjectiveBridgeError(
                "localised record lacks ra_deg/dec_deg; refusing to invent coordinates"
            )
        out.append(dict(item))
    return out


def _crossmatch_by_detection(
    crossmatches: Sequence[Mapping[str, Any]] | None,
) -> dict[str, dict[str, Any]]:
    if not crossmatches:
        return {}
    return {str(item["detection_id"]): dict(item) for item in crossmatches}


def build_temporary_universe(
    localisations: Sequence[Mapping[str, Any]],
    *,
    crossmatches: Sequence[Mapping[str, Any]] | None = None,
    label: str = "sky-bridge-temporary",
    as_of: str = AS_OF_DEFAULT,
) -> tuple[Universe, dict[str, Any]]:
    """Build a temporary synthetic universe from localised sky candidates.

    Every sky-derived entity carries ``classification_status=hypothesis``.
    Catalogue matches never promote to established identity.
    """

    localised = _localised_only(localisations)
    if not localised:
        raise SkyToObjectiveBridgeError(
            "Fail closed: no status=localised sky localisations; refusing Objective bridge "
            "(coordinates were not invented)."
        )

    prov = Provenance(
        "asa-astro-sky-to-objective-bridge",
        "synthetic",
        "temporary universe from WCS-when-present localisations; hypothesis only",
    )
    xm_by_det = _crossmatch_by_detection(crossmatches)

    site = Entity.create(
        "site",
        SITE_DESIGNATION,
        catalogue_ids={"SYN": "SKY-BRIDGE-SITE"},
        source=prov,
        attributes={"latitude_deg": -31.2733, "longitude_deg": 149.0644, "elevation_m": 1165.0},
    )
    telescope = Entity.create(
        "telescope",
        TELESCOPE_DESIGNATION,
        catalogue_ids={"SYN": "SKY-BRIDGE-SCOPE"},
        source=prov,
        attributes={"aperture_m": 0.5},
    )

    entities: list[Entity] = [site, telescope]
    evidence: list[EvidenceRecord] = []
    states: list[EntityState] = []
    entity_epistemic: list[dict[str, Any]] = []

    for index, loc in enumerate(sorted(localised, key=lambda item: item["id"]), start=1):
        sky = loc["sky"]
        designation = f"SKY-HYP-{index:03d}"
        detection_id = str(loc["detection_id"])
        xm = xm_by_det.get(detection_id)
        catalogue_ids: dict[str, str] = {"SKYBRIDGE": designation}
        attrs: dict[str, Any] = {
            "classification_status": "hypothesis",
            "identity_status": "hypothesis",
            "established_identity": False,
            "localisation_id": str(loc["id"]),
            "detection_id": detection_id,
            "wcs_present": True,
        }
        if loc.get("candidate_id"):
            attrs["observation_candidate_id"] = str(loc["candidate_id"])
        if xm is not None:
            attrs["crossmatch_resolution_state"] = str(xm.get("resolution_state"))
            attrs["crossmatch_evidence_qualified"] = bool(xm.get("evidence_qualified"))
            # Even matched+evidence-qualified stays hypothesis — never established.
            if xm.get("resolution_state") == "matched" and xm.get("candidates"):
                hit = xm["candidates"][0]
                catalogue_ids["XMATCH"] = str(hit["catalogue_id"])
                attrs["crossmatch_catalogue_id"] = str(hit["catalogue_id"])
                attrs["crossmatch_catalogue_name"] = str(hit["catalogue_name"])

        entity = Entity.create(
            "candidate",
            designation,
            catalogue_ids=catalogue_ids,
            coordinates=Coordinates(
                float(sky["ra_deg"]),
                float(sky["dec_deg"]),
                str(sky.get("frame") or "ICRS"),
                str(sky.get("epoch") or "J2000.0"),
            ),
            source=prov,
            attributes=attrs,
        )
        entities.append(entity)
        evidence.append(
            EvidenceRecord.create(
                "astrometry",
                entity.entity_id,
                values={
                    "ra_deg": float(sky["ra_deg"]),
                    "dec_deg": float(sky["dec_deg"]),
                    "frame": str(sky.get("frame") or "ICRS"),
                    "epoch": str(sky.get("epoch") or "J2000.0"),
                    "origin": "declared_wcs_localisation",
                    "classification_status": "hypothesis",
                },
                source=prov,
                observed_at=as_of,
                quality=0.7,
                status="admissible",
            )
        )
        states.append(
            EntityState(
                entity.entity_id,
                as_of,
                observation_status="observed",
                candidate_status="candidate",
                last_observed_at=as_of,
            )
        )
        entity_epistemic.append(
            {
                "entity_id": entity.entity_id,
                "designation": designation,
                "classification_status": "hypothesis",
                "established_identity": False,
                "detection_id": detection_id,
                "localisation_id": str(loc["id"]),
                "crossmatch_resolution_state": attrs.get("crossmatch_resolution_state"),
                "crossmatch_evidence_qualified": attrs.get("crossmatch_evidence_qualified", False),
            }
        )

    universe = Universe.create(label, "synthetic", entities, evidence, (), states)
    meta = {
        "site_designation": SITE_DESIGNATION,
        "telescope_designation": TELESCOPE_DESIGNATION,
        "hypothesis_entity_count": len(entity_epistemic),
        "entities": entity_epistemic,
        "established_identity_promoted": False,
        "coordinates_invented": False,
    }
    return universe, meta


def bridge_sky_localisations_to_objective(
    localisations: Sequence[Mapping[str, Any]],
    out_directory: str | Path,
    *,
    crossmatches: Sequence[Mapping[str, Any]] | None = None,
    objective: Objective | None = None,
    label: str = "sky-bridge-temporary",
    as_of: str = AS_OF_DEFAULT,
    window_start: str = WINDOW_START_DEFAULT,
    window_end: str = WINDOW_END_DEFAULT,
    issued_at: str | None = "2026-10-05T08:00:00Z",
    commit: str | None = None,
) -> dict[str, Any]:
    """Connect sky-localised candidates into Objective evaluate; write receipt + bridge manifest.

    ``out_directory`` must not already exist (refuses overwrite).
    """

    out = Path(out_directory)
    if out.exists():
        raise FileExistsError(f"output path already exists; refusing overwrite: {out}")

    universe, epistemic = build_temporary_universe(
        localisations, crossmatches=crossmatches, label=label, as_of=as_of
    )
    active_objective = objective or default_sky_candidate_objective()
    context = ObservingContext.declare(
        label="Sky-bridge temporary observing window",
        as_of=as_of,
        window_start=window_start,
        window_end=window_end,
        site_id=universe.find(SITE_DESIGNATION).entity_id,
        instrument_id=universe.find(TELESCOPE_DESIGNATION).entity_id,
        constraints={"limiting_magnitude": 16.0, "available_minutes": 240, "min_altitude_deg": 20},
    )

    adapter = open_or_bootstrap(universe)
    decision = decide(
        universe,
        active_objective,
        context,
        adapter,
        commit=commit or "sky-bridge-test",
        issued_at=issued_at,
    )

    out.mkdir(parents=True, exist_ok=False)
    _write_json(out / "universe.json", universe.to_record())
    _write_json(out / "objective.json", active_objective.to_record())
    _write_json(out / "context.json", context.to_record())
    _write_json(out / "evaluation.json", decision.evaluation.to_record())
    _write_json(out / "plan.json", decision.plan.to_record())
    decision.receipt.write(out)

    bridge_manifest = {
        "bridge_schema": "asa-astro-sky-to-objective-bridge-v1",
        "status": "evaluated",
        "epistemic": {
            "sky_candidates_are": "hypothesis",
            "established_identity_promoted": False,
            "coordinates_invented": False,
            "source_image_mutated": False,
            "catalogue_match_promotes_identity": False,
        },
        "universe_id": universe.universe_id,
        "objective_id": active_objective.objective_id,
        "context_id": context.context_id,
        "evaluation_id": decision.evaluation.evaluation_id,
        "receipt_id": decision.receipt.receipt_id,
        "asa_baseline": decision.snapshot.asa_baseline,
        "kernel_digest": decision.snapshot.digest,
        "hypothesis_entities": epistemic["entities"],
        "eligibility_summary": {
            "eligible": sum(1 for r in decision.evaluation.results if r.status == "eligible"),
            "ineligible": sum(1 for r in decision.evaluation.results if r.status == "ineligible"),
            "indeterminate": sum(1 for r in decision.evaluation.results if r.status == "indeterminate"),
        },
        "ranking": list(decision.evaluation.ranking()),
    }
    _write_json(out / "bridge_manifest.json", bridge_manifest)

    return {
        "output_directory": str(out),
        "universe_id": universe.universe_id,
        "receipt_id": decision.receipt.receipt_id,
        "evaluation_id": decision.evaluation.evaluation_id,
        "hypothesis_entity_count": epistemic["hypothesis_entity_count"],
        "established_identity_promoted": False,
        "coordinates_invented": False,
        "bridge_manifest": bridge_manifest,
    }


def bridge_observation_bundle_to_objective(
    bundle_directory: str | Path,
    out_directory: str | Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """Load ``sky_localisations.json`` (+ optional crossmatches) from an observe bundle and bridge."""

    root = Path(bundle_directory)
    sky_path = root / "sky_localisations.json"
    if not sky_path.is_file():
        raise SkyToObjectiveBridgeError(
            f"Fail closed: missing {sky_path.name}; run process_observation WCS wiring first"
        )
    sky = json.loads(sky_path.read_text(encoding="utf-8"))
    localisations = sky.get("localisations") or []
    if not sky.get("wcs_present"):
        raise SkyToObjectiveBridgeError(
            "Fail closed: observation bundle has no declared WCS (wcs_present=false); "
            "coordinates were not invented."
        )
    crossmatches = None
    cross_path = root / "catalogue_crossmatches.json"
    if cross_path.is_file():
        crossmatches = (json.loads(cross_path.read_text(encoding="utf-8")).get("crossmatches") or [])
    return bridge_sky_localisations_to_objective(
        localisations, out_directory, crossmatches=crossmatches, **kwargs
    )


__all__ = [
    "SkyToObjectiveBridgeError",
    "default_sky_candidate_objective",
    "build_temporary_universe",
    "bridge_sky_localisations_to_objective",
    "bridge_observation_bundle_to_objective",
]
