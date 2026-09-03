"""Navigator export: one JSON document a browser can walk — systems, their relationships as ASA holds
them (with stance and lifecycle), the evidence behind each, per-objective significance with feature
contributions, and the candidate-findings verdicts. Nothing here scores anything; it reads the same
snapshot and evaluations the receipts are built from.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from astro.asa.adapter import RelationalSnapshot
from astro.domain import Universe
from astro.objectives import Objective, ObservingContext
from astro.significance import evaluate

OFF_SKY = ("site", "instrument", "telescope", "survey", "observation")
ATTR_KEYS = ("magnitude_v", "magnitude_max", "magnitude_band", "teff_k", "distance_pc", "variability_type", "cluster_kind", "member_count",
             "log_age_yr", "r50_deg", "radius_earth", "mass_earth", "discovery_method", "discovery_year", "discovery_facility", "morphology", "object_type")
GRAPH_TYPES = ("hosts", "near", "member_of", "comparison_star_for", "hosted_transient", "calibration_reference_for")


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _trim_values(values: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for k, v in values.items():
        if k in ("note", "time_conversion", "geodetic_note"):
            continue
        if _num(v):
            out[k] = round(v, 6) if isinstance(v, float) else v
        elif isinstance(v, str) and len(v) <= 80:
            out[k] = v
        elif isinstance(v, list) and len(v) <= 4:
            out[k] = v
    return out


def export_navigator(universe: Universe, snapshot: RelationalSnapshot, objectives: list[tuple[Objective, ObservingContext]],
                     findings: dict[str, Any] | None = None, *, max_evidence_per_node: int = 40) -> dict[str, Any]:
    nodes, index = [], {}
    plx = {}
    for rec in universe.evidence:
        if rec.kind == "astrometry" and _num(rec.value_map.get("parallax_mas")) and rec.value_map["parallax_mas"] > 0:
            plx[rec.subject_id] = float(rec.value_map["parallax_mas"])
    host_of: dict[str, str] = {}
    for rel in universe.relationships:
        if rel.relationship_type == "hosts":
            for c in rel.role_map.get("companion", ()):
                host_of[c] = rel.role_map["host"][0]
    for e in universe.entities:
        if e.kind in OFF_SKY:
            continue
        coords = e.coordinates or (universe.entity(host_of[e.entity_id]).coordinates if e.entity_id in host_of else None)
        a = e.attribute_map
        dist = 1000.0 / plx[e.entity_id] if e.entity_id in plx else (float(a["distance_pc"]) if _num(a.get("distance_pc")) else None)
        mag = next((float(a[k]) for k in ("magnitude_v", "magnitude_max", "magnitude_g") if _num(a.get(k))), None)
        index[e.entity_id] = len(nodes)
        nodes.append({"id": e.entity_id, "d": e.designation, "k": e.kind, "ra": round(coords.ra_deg, 5) if coords else None,
                      "dec": round(coords.dec_deg, 5) if coords else None, "dist": round(dist, 2) if dist else None, "mag": mag,
                      "aliases": list(e.aliases)[:6], "cat": [list(p) for p in e.catalogue_ids][:6],
                      "attrs": {k: a[k] for k in ATTR_KEYS if k in a}, "src": e.source.source if e.source else None,
                      "ev": [], "claims": [], "disputes": [], "gaps": []})
    for rec in sorted(universe.evidence, key=lambda r: (r.kind, r.observed_at or "", r.evidence_id)):
        i = index.get(rec.subject_id)
        if i is None or len(nodes[i]["ev"]) >= max_evidence_per_node:
            continue
        nodes[i]["ev"].append({"id": rec.evidence_id[:20], "kind": rec.kind, "src": rec.source.reference.split(":", 1)[0] if rec.source and rec.source.reference else (rec.source.source if rec.source else ""),
                               "cls": rec.source.data_class if rec.source else "", "at": rec.observed_at, "q": rec.quality, "st": rec.status,
                               "v": _trim_values(rec.value_map), "u": _trim_values(rec.uncertainty_map)})
    edges = []
    claim_by_key: dict[str, dict[str, Any]] = {}
    for edge in snapshot.edges:
        parts = [p for p in edge.participants() if p in index]
        lit = dict(edge.literals)
        if edge.type_name == "measures" and parts:
            c = {"key": edge.key[:16], "q": lit.get("quantity"), "v": lit.get("value"), "unit": lit.get("unit"), "src": lit.get("source_key"),
                 "stance": edge.stance, "lc": edge.lifecycle, "node": index[parts[0]]}
            claim_by_key[edge.key] = c
            if edge.lifecycle == "registered":
                nodes[index[parts[0]]]["claims"].append(c)
        elif edge.type_name == "lacks_evidence" and parts:
            if edge.lifecycle == "registered":
                nodes[index[parts[0]]]["gaps"].append(lit.get("evidence_kind"))
        elif edge.type_name in GRAPH_TYPES and len(parts) >= 1:
            roles = {role: [index[r] for r in refs if r in index] for role, refs in edge.bindings}
            if sum(len(v) for v in roles.values()) < 2 and edge.type_name != "hosts":
                continue
            edges.append({"key": edge.key[:16], "t": edge.type_name, "stance": edge.stance, "lc": edge.lifecycle, "roles": roles,
                          "lit": {k: v for k, v in lit.items() if k in ("separation_arcsec",)}, "nsup": len(edge.supported_by)})
    for edge in snapshot.edges:
        if edge.type_name == "contradicts" and edge.lifecycle == "registered":
            keys = [k for _, refs in edge.bindings for k in refs]
            cl = [claim_by_key[k] for k in keys if k in claim_by_key]
            if len(cl) == 2 and cl[0]["node"] == cl[1]["node"]:
                nodes[cl[0]["node"]]["disputes"].append({"q": cl[0]["q"], "a": {"v": cl[0]["v"], "src": cl[0]["src"]}, "b": {"v": cl[1]["v"], "src": cl[1]["src"]}, "unit": cl[0]["unit"]})
    objs = {}
    for objective, context in objectives:
        ev = evaluate(universe, snapshot, objective, context)
        scores = {}
        eligible = 0
        for r in ev.results:
            i = index.get(r.entity_id)
            if i is None:
                continue
            if r.status == "eligible":
                eligible += 1
                scores[str(i)] = {"s": r.score, "rank": r.rank, "c": [{"f": c["feature"], "v": c.get("value"), "w": c["weight"], "st": c["status"],
                                                                     "x": c.get("contribution")} for c in r.contributions], "u": list(r.unavailable)}
            else:
                failed = next((x for x in r.eligibility if not x.get("passed")), None)
                scores[str(i)] = {"s": None, "why": failed["detail"] if failed else "ineligible"}
        objs[objective.name] = {"id": objective.objective_id[:20], "question": objective.question, "purpose": objective.purpose_class,
                                "features": [{"name": f.name, "weight": f.weight, "required": f.required, "rationale": f.rationale} for f in objective.features],
                                "context": context.label, "eligible": eligible, "evaluation_id": ev.evaluation_id[:24], "scores": scores}
    fnd = {"associations": {}, "drift": {}, "undetermined": {}}
    if findings:
        for row in findings.get("cluster_associations", {}).get("rows", []):
            fnd["associations"].setdefault(row["host"], []).append({"cluster": row["cluster"], "verdict": row["verdict"], "reason": row.get("reason"), "dv": row.get("delta_v_tan_km_s"), "ruwe": row.get("host_ruwe")})
        for row in findings.get("decayed_ephemerides", {}).get("rows", []):
            fnd["drift"].setdefault(row["host"], []).append({"planet": row["planet"], "sigma_min": row["sigma_transit_minutes"], "ratio": row["sigma_over_duration"], "cycles": row["cycles_since_epoch"]})
        for row in findings.get("undetermined_periods", {}).get("rows", []):
            fnd["undetermined"].setdefault(row["host"], []).append({"planet": row["planet"], "period": row["period_days"], "sigma_period": row["sigma_period_days"]})
    kinds: dict[str, int] = {}
    for n in nodes:
        kinds[n["k"]] = kinds.get(n["k"], 0) + 1
    return {"meta": {"universe_id": universe.universe_id, "label": universe.label, "data_class": universe.data_class, "kernel_digest": snapshot.digest,
                     "kernel_seq": snapshot.seq, "asa_baseline": snapshot.asa_baseline, "nodes": len(nodes), "edges": len(edges), "kinds": kinds,
                     "disputed": sum(1 for n in nodes if n["disputes"]), "gapped": sum(1 for n in nodes if n["gaps"]),
                     "findings_as_of": findings.get("as_of") if findings else None},
            "nodes": nodes, "edges": edges, "objectives": objs, "findings": fnd}


def render_navigator(data: dict[str, Any], template: Path | None = None) -> str:
    template = template or Path(__file__).with_name("navigator.html")
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    return template.read_text(encoding="utf-8").replace("/*__ASTRO_DATA__*/null", payload)
