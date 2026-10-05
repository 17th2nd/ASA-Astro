"""Sky-localised observation candidates → temporary universe → Objective evaluate + receipt.

Rules enforced:
- Fail closed when no successful (status=localised) sky localisations exist.
- Never invent sky coordinates.
- Never silently substitute the synthetic slice1 universe.
- Every derived sky entity is classified as **hypothesis**, never established.
- Catalogue associations remain hypothesis; matched only if evidence-qualified upstream.
- Source images are not touched (this module consumes localisation records only).
- Hard-coded SYN-SITE lat/lon is **demo-only** (``allow_synthetic_demo_site=True``).
  Real-upload path requires a declared site or an explicitly undeclared/hypothesis site
  (no pretended observatory coordinates).
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


# Demo-only designations — never used as a silent real-upload site.
DEMO_SITE_DESIGNATION = "SYN-SITE-SKY-BRIDGE"
DEMO_TELESCOPE_DESIGNATION = "SYN-SCOPE-SKY-BRIDGE"
# Historical aliases (tests / older callers).
SITE_DESIGNATION = DEMO_SITE_DESIGNATION
TELESCOPE_DESIGNATION = DEMO_TELESCOPE_DESIGNATION

UNDECLARED_SITE_DESIGNATION = "SITE-UNDECLARED-HYPOTHESIS"
UNDECLARED_TELESCOPE_DESIGNATION = "SCOPE-UNDECLARED-HYPOTHESIS"

AS_OF_DEFAULT = "2026-10-05T08:00:00Z"
WINDOW_START_DEFAULT = "2026-10-05T09:00:00Z"
WINDOW_END_DEFAULT = "2026-10-05T19:00:00Z"

# Explicit demo coordinates (Siding Spring-like); used ONLY when allow_synthetic_demo_site=True.
_DEMO_SITE_ATTRS = {
    "latitude_deg": -31.2733,
    "longitude_deg": 149.0644,
    "elevation_m": 1165.0,
    "site_standing": "synthetic-demo-only",
    "classification_status": "hypothesis",
    "demo_only": True,
}


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


def _coordinates_invented_from_localisations(localisations: Sequence[Mapping[str, Any]]) -> bool:
    """Compute honesty flag: True only if sky coords emitted without WCS (F-SCI-04)."""

    invented = False
    for loc in localisations:
        sky = loc.get("sky") if isinstance(loc.get("sky"), Mapping) else {}
        has_coords = sky.get("ra_deg") is not None or sky.get("dec_deg") is not None
        if has_coords and not loc.get("wcs_present"):
            invented = True
        if loc.get("status") == "localised" and not loc.get("wcs_present"):
            invented = True
    return invented


def _load_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def load_observation_identity_from_bundle(bundle_directory: str | Path) -> dict[str, Any] | None:
    """Present-only observation_identity from a process_observation bundle (never invented)."""

    root = Path(bundle_directory)
    for name in ("sky_localisations.json", "provenance.json", "manifest.json", "wcs_solution.json"):
        payload = _load_json_if_present(root / name)
        if payload and isinstance(payload.get("observation_identity"), dict):
            return dict(payload["observation_identity"])
    return None


def _site_from_mapping(
    site: Mapping[str, Any],
    prov: Provenance,
) -> tuple[Entity, dict[str, Any]]:
    """Build a site entity from declared observer metadata (no invented lat/lon)."""

    designation = str(
        site.get("designation")
        or site.get("site_designation")
        or site.get("name")
        or "DECLARED-SITE"
    )
    attrs: dict[str, Any] = {
        "classification_status": "hypothesis",
        "site_standing": "declared-metadata",
        "demo_only": False,
    }
    for key in ("latitude_deg", "longitude_deg", "elevation_m", "site_code", "timezone"):
        if key in site and site[key] is not None:
            attrs[key] = site[key]
    # Honesty: if lat/lon absent in declaration, do not invent them.
    if "latitude_deg" not in attrs or "longitude_deg" not in attrs:
        attrs["site_standing"] = "declared-incomplete"
        attrs["coordinates_present"] = False
    else:
        attrs["coordinates_present"] = True
    catalogue_ids = {"DECLARED": designation}
    if site.get("catalogue_id"):
        catalogue_ids["SITE"] = str(site["catalogue_id"])
    entity = Entity.create(
        "site",
        designation,
        catalogue_ids=catalogue_ids,
        source=prov,
        attributes=attrs,
    )
    epistemic = {
        "site_designation": designation,
        "site_standing": attrs["site_standing"],
        "demo_only": False,
        "coordinates_present": attrs.get("coordinates_present", False),
    }
    return entity, epistemic


def _resolve_site_and_instrument(
    *,
    site: Mapping[str, Any] | None,
    instrument: Mapping[str, Any] | None,
    allow_synthetic_demo_site: bool,
    prov: Provenance,
) -> tuple[Entity, Entity, dict[str, Any]]:
    """Resolve observer site/instrument without silently pretending a real observatory."""

    if site is not None:
        site_entity, site_meta = _site_from_mapping(site, prov)
        inst_designation = str(
            (instrument or {}).get("designation")
            or (instrument or {}).get("name")
            or f"SCOPE-FOR-{site_meta['site_designation']}"
        )
        inst_attrs: dict[str, Any] = {
            "classification_status": "hypothesis",
            "demo_only": False,
        }
        if instrument:
            for key in ("aperture_m", "instrument_code", "filter"):
                if key in instrument and instrument[key] is not None:
                    inst_attrs[key] = instrument[key]
        telescope = Entity.create(
            "telescope",
            inst_designation,
            catalogue_ids={"DECLARED": inst_designation},
            source=prov,
            attributes=inst_attrs,
        )
        site_meta["telescope_designation"] = inst_designation
        return site_entity, telescope, site_meta

    if allow_synthetic_demo_site:
        site_entity = Entity.create(
            "site",
            DEMO_SITE_DESIGNATION,
            catalogue_ids={"SYN": "SKY-BRIDGE-SITE"},
            source=prov,
            attributes=dict(_DEMO_SITE_ATTRS),
        )
        telescope = Entity.create(
            "telescope",
            DEMO_TELESCOPE_DESIGNATION,
            catalogue_ids={"SYN": "SKY-BRIDGE-SCOPE"},
            source=prov,
            attributes={
                "aperture_m": 0.5,
                "classification_status": "hypothesis",
                "demo_only": True,
            },
        )
        return (
            site_entity,
            telescope,
            {
                "site_designation": DEMO_SITE_DESIGNATION,
                "telescope_designation": DEMO_TELESCOPE_DESIGNATION,
                "site_standing": "synthetic-demo-only",
                "demo_only": True,
                "coordinates_present": True,
            },
        )

    # Real-upload default: undeclared hypothesis site — no invented lat/lon.
    site_entity = Entity.create(
        "site",
        UNDECLARED_SITE_DESIGNATION,
        catalogue_ids={"UNDECLARED": "SITE"},
        source=prov,
        attributes={
            "classification_status": "hypothesis",
            "site_standing": "undeclared",
            "coordinates_present": False,
            "demo_only": False,
            "note": (
                "Observer site was not declared in metadata; lat/lon were not invented. "
                "Visibility geometry is indeterminate until a site is supplied."
            ),
        },
    )
    telescope = Entity.create(
        "telescope",
        UNDECLARED_TELESCOPE_DESIGNATION,
        catalogue_ids={"UNDECLARED": "SCOPE"},
        source=prov,
        attributes={
            "classification_status": "hypothesis",
            "demo_only": False,
            "instrument_standing": "undeclared",
        },
    )
    return (
        site_entity,
        telescope,
        {
            "site_designation": UNDECLARED_SITE_DESIGNATION,
            "telescope_designation": UNDECLARED_TELESCOPE_DESIGNATION,
            "site_standing": "undeclared",
            "demo_only": False,
            "coordinates_present": False,
        },
    )


def build_temporary_universe(
    localisations: Sequence[Mapping[str, Any]],
    *,
    crossmatches: Sequence[Mapping[str, Any]] | None = None,
    label: str = "sky-bridge-temporary",
    as_of: str = AS_OF_DEFAULT,
    site: Mapping[str, Any] | None = None,
    instrument: Mapping[str, Any] | None = None,
    allow_synthetic_demo_site: bool = False,
    observation_identity: Mapping[str, Any] | None = None,
) -> tuple[Universe, dict[str, Any]]:
    """Build a temporary hypothesis universe from localised sky candidates.

    Every sky-derived entity carries ``classification_status=hypothesis``.
    Catalogue matches never promote to established identity.
    Does **not** load or substitute ``data/universe/slice1.json``.
    """

    localised = _localised_only(localisations)
    if not localised:
        raise SkyToObjectiveBridgeError(
            "Fail closed: no status=localised sky localisations; refusing Objective bridge "
            "(coordinates were not invented; synthetic slice1 was not substituted)."
        )

    data_class = "synthetic" if allow_synthetic_demo_site and site is None else "hypothesis"
    prov_note = (
        "temporary universe from WCS-when-present localisations; hypothesis only"
        + ("; synthetic-demo site" if allow_synthetic_demo_site and site is None else "")
    )
    if observation_identity and observation_identity.get("observation_claim_digest"):
        prov_note += f"; bound to observation_claim_digest={observation_identity['observation_claim_digest']}"
    prov = Provenance(
        "asa-astro-sky-to-objective-bridge",
        data_class if data_class != "hypothesis" else "synthetic",
        prov_note,
    )
    # Universe.data_class vocabulary is synthetic|real|mixed — hypothesis standing lives on entities.
    universe_data_class = "synthetic"
    xm_by_det = _crossmatch_by_detection(crossmatches)

    site_entity, telescope, site_meta = _resolve_site_and_instrument(
        site=site,
        instrument=instrument,
        allow_synthetic_demo_site=allow_synthetic_demo_site,
        prov=prov,
    )

    entities: list[Entity] = [site_entity, telescope]
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
        if observation_identity:
            if observation_identity.get("observation_claim_digest"):
                attrs["observation_claim_digest"] = observation_identity["observation_claim_digest"]
            if observation_identity.get("observation_claim_id"):
                attrs["observation_claim_id"] = observation_identity["observation_claim_id"]
            if observation_identity.get("source_sha256"):
                attrs["source_sha256"] = observation_identity["source_sha256"]
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
                "observation_claim_digest": attrs.get("observation_claim_digest"),
                "observation_claim_id": attrs.get("observation_claim_id"),
            }
        )

    universe = Universe.create(label, universe_data_class, entities, evidence, (), states)
    meta = {
        "site_designation": site_meta["site_designation"],
        "telescope_designation": site_meta["telescope_designation"],
        "site_standing": site_meta["site_standing"],
        "site_demo_only": bool(site_meta.get("demo_only")),
        "site_coordinates_present": bool(site_meta.get("coordinates_present")),
        "hypothesis_entity_count": len(entity_epistemic),
        "entities": entity_epistemic,
        "established_identity_promoted": False,
        "coordinates_invented": _coordinates_invented_from_localisations(localisations),
        "observation_identity": dict(observation_identity) if observation_identity else None,
        "slice1_substituted": False,
        "primary_universe_source": "sky-localisations-bridge",
    }
    return universe, meta


def _coerce_context(
    context: ObservingContext | Mapping[str, Any] | None,
    *,
    universe: Universe,
    site_designation: str,
    telescope_designation: str,
    as_of: str,
    window_start: str,
    window_end: str,
) -> ObservingContext:
    if isinstance(context, ObservingContext):
        return context
    if isinstance(context, Mapping):
        record = dict(context)
        if "site_id" not in record and "site_designation" not in record:
            record.setdefault("site_id", universe.find(site_designation).entity_id)
        if "instrument_id" not in record and "instrument_designation" not in record:
            record.setdefault("instrument_id", universe.find(telescope_designation).entity_id)
        if "site_designation" in record and "site_id" not in record:
            record["site_id"] = universe.find(str(record["site_designation"])).entity_id
        if "instrument_designation" in record and "instrument_id" not in record:
            record["instrument_id"] = universe.find(str(record["instrument_designation"])).entity_id
        return ObservingContext.from_record(
            {
                "label": record.get("label") or "Observation-bridge observing window",
                "as_of": record.get("as_of") or as_of,
                "window_start": record.get("window_start") or window_start,
                "window_end": record.get("window_end") or window_end,
                "site_id": record.get("site_id"),
                "instrument_id": record.get("instrument_id"),
                "constraints": record.get("constraints") or {
                    "limiting_magnitude": 16.0,
                    "available_minutes": 240,
                    "min_altitude_deg": 20,
                },
                "anchor_targets": record.get("anchor_targets") or (),
            }
        )
    return ObservingContext.declare(
        label="Observation-bridge observing window",
        as_of=as_of,
        window_start=window_start,
        window_end=window_end,
        site_id=universe.find(site_designation).entity_id,
        instrument_id=universe.find(telescope_designation).entity_id,
        constraints={"limiting_magnitude": 16.0, "available_minutes": 240, "min_altitude_deg": 20},
    )


def bridge_sky_localisations_to_objective(
    localisations: Sequence[Mapping[str, Any]],
    out_directory: str | Path,
    *,
    crossmatches: Sequence[Mapping[str, Any]] | None = None,
    objective: Objective | None = None,
    context: ObservingContext | Mapping[str, Any] | None = None,
    site: Mapping[str, Any] | None = None,
    instrument: Mapping[str, Any] | None = None,
    allow_synthetic_demo_site: bool = False,
    observation_identity: Mapping[str, Any] | None = None,
    label: str = "sky-bridge-temporary",
    as_of: str = AS_OF_DEFAULT,
    window_start: str = WINDOW_START_DEFAULT,
    window_end: str = WINDOW_END_DEFAULT,
    issued_at: str | None = "2026-10-05T08:00:00Z",
    commit: str | None = None,
) -> dict[str, Any]:
    """Connect sky-localised candidates into Objective evaluate; write receipt + bridge manifest.

    ``out_directory`` must not already exist (refuses overwrite).
    Does not substitute ``slice1`` or any shared synthetic universe.
    Hard-coded SYN-SITE coordinates require ``allow_synthetic_demo_site=True``.
    """

    out = Path(out_directory)
    if out.exists():
        raise FileExistsError(f"output path already exists; refusing overwrite: {out}")

    universe, epistemic = build_temporary_universe(
        localisations,
        crossmatches=crossmatches,
        label=label,
        as_of=as_of,
        site=site,
        instrument=instrument,
        allow_synthetic_demo_site=allow_synthetic_demo_site,
        observation_identity=observation_identity,
    )
    active_objective = objective or default_sky_candidate_objective()
    active_context = _coerce_context(
        context,
        universe=universe,
        site_designation=epistemic["site_designation"],
        telescope_designation=epistemic["telescope_designation"],
        as_of=as_of,
        window_start=window_start,
        window_end=window_end,
    )

    adapter = open_or_bootstrap(universe)
    decision = decide(
        universe,
        active_objective,
        active_context,
        adapter,
        commit=commit or "sky-bridge-test",
        issued_at=issued_at,
    )

    out.mkdir(parents=True, exist_ok=False)
    _write_json(out / "universe.json", universe.to_record())
    _write_json(out / "objective.json", active_objective.to_record())
    _write_json(out / "context.json", active_context.to_record())
    _write_json(out / "evaluation.json", decision.evaluation.to_record())
    _write_json(out / "plan.json", decision.plan.to_record())
    decision.receipt.write(out)

    coordinates_invented = _coordinates_invented_from_localisations(localisations)
    source_paths_written: list[str] = []
    source_image_mutated = len(source_paths_written) > 0
    oid = dict(observation_identity) if observation_identity else None

    bridge_manifest = {
        "bridge_schema": "asa-astro-sky-to-objective-bridge-v1",
        "status": "evaluated",
        "epistemic": {
            "sky_candidates_are": "hypothesis",
            "established_identity_promoted": False,
            "coordinates_invented": coordinates_invented,
            "source_image_mutated": source_image_mutated,
            "catalogue_match_promotes_identity": False,
            "site_standing": epistemic["site_standing"],
            "site_demo_only": epistemic["site_demo_only"],
            "slice1_substituted": False,
            "primary_universe_source": "sky-localisations-bridge",
        },
        "observation_identity": oid,
        "universe_id": universe.universe_id,
        "objective_id": active_objective.objective_id,
        "context_id": active_context.context_id,
        "evaluation_id": decision.evaluation.evaluation_id,
        "receipt_id": decision.receipt.receipt_id,
        "asa_baseline": decision.snapshot.asa_baseline,
        "kernel_digest": decision.snapshot.digest,
        "hypothesis_entities": epistemic["entities"],
        "site": {
            "designation": epistemic["site_designation"],
            "standing": epistemic["site_standing"],
            "demo_only": epistemic["site_demo_only"],
            "coordinates_present": epistemic["site_coordinates_present"],
        },
        "eligibility_summary": {
            "eligible": sum(1 for r in decision.evaluation.results if r.status == "eligible"),
            "ineligible": sum(1 for r in decision.evaluation.results if r.status == "ineligible"),
            "indeterminate": sum(1 for r in decision.evaluation.results if r.status == "indeterminate"),
        },
        "ranking": list(decision.evaluation.ranking()),
    }
    _write_json(out / "bridge_manifest.json", bridge_manifest)
    if oid is not None:
        _write_json(out / "observation_identity.json", oid)

    return {
        "output_directory": str(out),
        "universe_id": universe.universe_id,
        "receipt_id": decision.receipt.receipt_id,
        "evaluation_id": decision.evaluation.evaluation_id,
        "objective_id": active_objective.objective_id,
        "context_id": active_context.context_id,
        "hypothesis_entity_count": epistemic["hypothesis_entity_count"],
        "established_identity_promoted": False,
        "coordinates_invented": coordinates_invented,
        "source_image_mutated": source_image_mutated,
        "observation_identity": oid,
        "site_standing": epistemic["site_standing"],
        "site_demo_only": epistemic["site_demo_only"],
        "slice1_substituted": False,
        "bridge_manifest": bridge_manifest,
    }


def observation_bundle_to_objective(
    bundle_directory: str | Path,
    out_directory: str | Path,
    *,
    objective: Objective | None = None,
    context: ObservingContext | Mapping[str, Any] | None = None,
    site: Mapping[str, Any] | None = None,
    instrument: Mapping[str, Any] | None = None,
    allow_synthetic_demo_site: bool = False,
    as_of: str = AS_OF_DEFAULT,
    window_start: str = WINDOW_START_DEFAULT,
    window_end: str = WINDOW_END_DEFAULT,
    issued_at: str | None = "2026-10-05T08:00:00Z",
    commit: str | None = None,
    label: str = "observation-bridge-temporary",
) -> dict[str, Any]:
    """Runtime handoff A: process_observation bundle → Objective universe + receipt.

    Signature (Significance-owned):

        observation_bundle_to_objective(
            bundle_directory,
            out_directory,
            *,
            objective=None,
            context=None,
            site=None,
            instrument=None,
            allow_synthetic_demo_site=False,
            as_of=...,
            window_start=...,
            window_end=...,
            issued_at=...,
            commit=None,
            label="observation-bridge-temporary",
        ) -> dict

    Behaviour:
    - Loads ``sky_localisations.json`` (+ optional ``catalogue_crossmatches.json``).
    - Fail-closed if no ``status=localised`` rows or ``wcs_present=false``.
    - Never invents coordinates; never substitutes ``data/universe/slice1.json``.
    - Binds present-only ``observation_identity`` (source/metadata/wcs digests) into
      manifest, return value, and hypothesis entity attributes.
    - Site: declared ``site`` mapping, else undeclared hypothesis (no lat/lon), else
      explicit ``allow_synthetic_demo_site=True`` for tests/demos only.
    """

    root = Path(bundle_directory)
    sky_path = root / "sky_localisations.json"
    if not sky_path.is_file():
        raise SkyToObjectiveBridgeError(
            f"Fail closed: missing {sky_path.name}; run process_observation WCS wiring first "
            "(synthetic slice1 was not substituted)."
        )
    sky = json.loads(sky_path.read_text(encoding="utf-8"))
    localisations = sky.get("localisations") or []
    if not sky.get("wcs_present"):
        raise SkyToObjectiveBridgeError(
            "Fail closed: observation bundle has no declared WCS (wcs_present=false); "
            "coordinates were not invented; synthetic slice1 was not substituted."
        )
    if not any(item.get("status") == "localised" for item in localisations):
        raise SkyToObjectiveBridgeError(
            "Fail closed: no status=localised sky localisations in bundle; "
            "refusing Objective bridge (synthetic slice1 was not substituted)."
        )

    crossmatches = None
    cross_path = root / "catalogue_crossmatches.json"
    if cross_path.is_file():
        crossmatches = (json.loads(cross_path.read_text(encoding="utf-8")).get("crossmatches") or [])

    observation_identity = load_observation_identity_from_bundle(root)
    if observation_identity is None and isinstance(sky.get("observation_identity"), dict):
        observation_identity = dict(sky["observation_identity"])

    # Optional declared site from associated metadata copied into the bundle.
    resolved_site = site
    resolved_instrument = instrument
    if resolved_site is None:
        for meta_name in ("associated_metadata.json", "metadata.json", "observation_metadata.json"):
            meta = _load_json_if_present(root / meta_name)
            if not meta:
                continue
            if isinstance(meta.get("site"), dict):
                resolved_site = meta["site"]
            elif isinstance(meta.get("observer_site"), dict):
                resolved_site = meta["observer_site"]
            if resolved_instrument is None and isinstance(meta.get("instrument"), dict):
                resolved_instrument = meta["instrument"]
            elif resolved_instrument is None and isinstance(meta.get("instrument"), str):
                resolved_instrument = {"designation": meta["instrument"]}
            break

    result = bridge_sky_localisations_to_objective(
        localisations,
        out_directory,
        crossmatches=crossmatches,
        objective=objective,
        context=context,
        site=resolved_site,
        instrument=resolved_instrument,
        allow_synthetic_demo_site=allow_synthetic_demo_site,
        observation_identity=observation_identity,
        label=label,
        as_of=as_of,
        window_start=window_start,
        window_end=window_end,
        issued_at=issued_at,
        commit=commit,
    )
    result["bundle_directory"] = str(root)
    result["api"] = "asa_astro.bridge.observation_bundle_to_objective"
    return result


def bridge_observation_bundle_to_objective(
    bundle_directory: str | Path,
    out_directory: str | Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias kept for older callers; prefer ``observation_bundle_to_objective``."""

    return observation_bundle_to_objective(bundle_directory, out_directory, **kwargs)


__all__ = [
    "SkyToObjectiveBridgeError",
    "DEMO_SITE_DESIGNATION",
    "UNDECLARED_SITE_DESIGNATION",
    "default_sky_candidate_objective",
    "build_temporary_universe",
    "bridge_sky_localisations_to_objective",
    "observation_bundle_to_objective",
    "bridge_observation_bundle_to_objective",
    "load_observation_identity_from_bundle",
]
