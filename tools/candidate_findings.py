"""Candidate findings from a universe JSON, with the checks an astronomer would apply before believing them.

    PYTHONPATH=src python3 tools/candidate_findings.py var/universe-real-frontier-tess.json --as-of 2026-09-04T08:00:00Z \
        --out var/runs/candidate-findings.json [--clusters-csv data/catalogues/raw/vizier_huntreffert_clusters.csv]

Two lists, each reproducible from the committed code and the digest-recorded snapshots:

1. Cluster associations: every ``member_of`` relationship in the universe re-tested on proper motion
   (tangential-velocity difference v = 4.74047·Δμ/ϖ) and Gaia RUWE. Cluster proper motions come from the
   cluster entity attributes when the snapshot carries them, else from the raw Hunt & Reffert CSV.
2. Decayed ephemerides: transiting planets whose predicted transit-time uncertainty now exceeds the
   transit duration, *excluding* undetermined periods (σ_P/P > max_period_fraction), which are listed apart.

Nothing here is an evaluation; it is the candidate list an observer can falsify with one observation.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path

KM_S = 4.74047


def parse_utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("universe")
    ap.add_argument("--as-of", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--clusters-csv", default="data/catalogues/raw/vizier_huntreffert_clusters.csv")
    ap.add_argument("--max-tangential-km-s", type=float, default=3.0)
    ap.add_argument("--max-ruwe", type=float, default=1.4)
    ap.add_argument("--max-period-fraction", type=float, default=0.01)
    a = ap.parse_args()
    now = parse_utc(a.as_of)
    U = json.load(open(a.universe))
    ents = {e["entity_id"]: e for e in U["entities"]}
    ev_by: dict[str, list] = {}
    for r in U["evidence"]:
        ev_by.setdefault(r["subject_id"], []).append(r)
    raw_pm: dict[str, tuple[float, float]] = {}
    p = Path(a.clusters_csv)
    if p.exists():
        for row in csv.DictReader(p.open()):
            if row.get("pmRA") and row.get("pmDE"):
                raw_pm[row["Name"]] = (float(row["pmRA"]), float(row["pmDE"]))

    # 1. cluster associations
    assoc = []
    for r in U["relationships"]:
        if r["relationship_type"] != "member_of":
            continue
        m, g = r["roles"]["member"][0], r["roles"]["group"][0]
        me, ge = ents[m], ents[g]
        ast = next((x for x in ev_by.get(m, []) if x["kind"] == "astrometry" and "parallax_mas" in x["values"]), None)
        ga = ge["attributes"]
        cpm = (ga.get("pmra_mas_yr"), ga.get("pmdec_mas_yr"))
        if None in cpm:
            cpm = raw_pm.get(ge["designation"], (None, None))
        row = {"host": me["designation"], "cluster": ge["designation"], "cluster_kind": ga.get("cluster_kind"), "cluster_log_age_yr": ga.get("log_age_yr"),
               "asserted_confidence": r.get("confidence"), "status_in_universe": r.get("status"), "evidenced": bool(r.get("evidence_ids"))}
        if ast is None or None in cpm:
            row.update(verdict="untestable", reason="no host astrometry" if ast is None else "no cluster proper motion")
        else:
            v = ast["values"]
            plx = float(v["parallax_mas"])
            dmu = math.hypot(float(v["pmra_mas_yr"]) - cpm[0], float(v["pmdec_mas_yr"]) - cpm[1])
            dv = KM_S * dmu / plx if plx > 0 else float("inf")
            ruwe = v.get("ruwe")
            row.update(host_parallax_mas=round(plx, 4), cluster_parallax_mas=ga.get("parallax_mas"), delta_pm_mas_yr=round(dmu, 3),
                       delta_v_tan_km_s=round(dv, 2), host_ruwe=ruwe)
            if ruwe is not None and float(ruwe) > a.max_ruwe:
                row.update(verdict="untrusted", reason=f"RUWE {float(ruwe):.2f} > {a.max_ruwe}")
            elif dv <= a.max_tangential_km_s:
                row.update(verdict="kinematic member", reason=f"Δv_tan {dv:.2f} km/s ≤ {a.max_tangential_km_s}")
            else:
                row.update(verdict="rejected", reason=f"Δv_tan {dv:.2f} km/s > {a.max_tangential_km_s}")
        assoc.append(row)
    order = {"kinematic member": 0, "untrusted": 1, "untestable": 2, "rejected": 3}
    assoc.sort(key=lambda d: (order[d["verdict"]], d.get("delta_v_tan_km_s") or 0.0, d["host"]))

    # 2. decayed ephemerides
    drift, undetermined = [], []
    for eid, recs in ev_by.items():
        for rec in recs:
            if rec["kind"] != "ephemeris":
                continue
            v, u = rec.get("values", {}), rec.get("uncertainty", {})
            if "period_days" not in v or "epoch_utc" not in v or ("period_days" not in u and "epoch_days" not in u):
                continue
            period, sig_p = float(v["period_days"]), float(u.get("period_days", 0.0))
            n = abs((now - parse_utc(v["epoch_utc"])).total_seconds() / 86400.0 / period)
            dur = float(v.get("duration_hours", 2.0)) or 2.0
            base = {"host": ents[eid]["designation"], "planet": v.get("planet"), "period_days": period, "sigma_period_days": sig_p,
                    "sigma_epoch_days": u.get("epoch_days"), "epoch_utc": v["epoch_utc"], "cycles_since_epoch": round(n, 1),
                    "duration_hours": dur, "duration_source": v.get("duration_source"), "source": rec.get("source", {}).get("reference")}
            if period <= 0 or sig_p / period > a.max_period_fraction:
                undetermined.append({**base, "sigma_period_over_period": round(sig_p / period, 3)})
                continue
            sig = math.sqrt(float(u.get("epoch_days", 0.0)) ** 2 + (n * sig_p) ** 2)
            ratio = sig * 24.0 / dur
            if ratio >= 1.0:
                drift.append({**base, "sigma_transit_minutes": round(sig * 1440.0, 1), "sigma_over_duration": round(ratio, 3)})
    drift.sort(key=lambda d: -d["sigma_over_duration"])
    undetermined.sort(key=lambda d: -d["sigma_period_over_period"])

    out = {"as_of": a.as_of, "universe": a.universe, "universe_id": U.get("universe_id"),
           "parameters": {"max_tangential_km_s": a.max_tangential_km_s, "max_ruwe": a.max_ruwe, "max_period_fraction": a.max_period_fraction},
           "cluster_associations": {"total": len(assoc), "by_verdict": {k: sum(1 for d in assoc if d["verdict"] == k) for k in order}, "rows": assoc},
           "decayed_ephemerides": {"planets": len(drift), "hosts": len({d["host"] for d in drift}),
                                   "with_tabulated_duration": sum(1 for d in drift if d["duration_source"] == "tabulated"), "rows": drift},
           "undetermined_periods": {"planets": len(undetermined), "rows": undetermined}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "rows"}) for k, v in out.items()}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
