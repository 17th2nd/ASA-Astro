"""Dataset retrieval, freezing and candidate selection for ASTRO-REAL-DATA-EXP-0001.

Three separated things live under ``validation/real-data/ASTRO-REAL-DATA-EXP-0001/dataset/``:

- ``input_*.csv``          — raw catalogue rows the engine reads (NASA Exoplanet Archive snapshot of 2026-09-02, Gaia DR3);
- ``reference_exoclock_priority.json`` — the independent reference labels (ExoClock priority), never read by the engine;
- ``leakage_reflinks.csv`` — the archive's ephemeris reference links used only to exclude leaked candidates.

``PROVENANCE.json`` records every source URL, retrieval time, byte count and sha256; ``candidates.json`` records the
selection with every exclusion and its reason. Selection rules are those declared in the dataset record (§6).
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from astro.catalogues.manifest import RAW, load_manifest
from astro.pipeline import ROOT
from astro_exec.core.hashing import sha256_file
from . import EXP_ID, HASH_SALT

EXP_DIR = ROOT / "validation" / "real-data" / EXP_ID
DATASET_DIR = EXP_DIR / "dataset"
RESULTS_DIR = EXP_DIR / "results"

EXOCLOCK_URL = "https://www.exoclock.space/database/planets_json"
REFLINK_COLS = "pl_name,hostname,pl_orbper,pl_orbpererr1,pl_orbper_reflink,pl_tranmid,pl_tranmiderr1,pl_tranmid_reflink"
REFLINK_URL = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+{REFLINK_COLS}+from+pscomppars+where+tran_flag=1&format=csv"
EXOCLOCK_RAW = RAW / "exoclock_planets.json"
REFLINK_RAW = RAW / "exoplanetarchive_pscomppars_reflinks.csv"

GRADE = {"alert": 3, "high": 2, "medium": 1, "low": 0}
REFERENCE_FIELDS = ("name", "star", "priority", "ra_j2000", "dec_j2000", "v_mag", "total_observations", "total_observations_recent",
                    "t0_bjd_tdb", "t0_unc", "period_days", "period_unc", "duration_hours", "min_telescope_inches")
PRIMARY_SAMPLE_SIZE = 100
MIN_SAMPLE = 40


def normalise_name(name: str) -> str:
    return re.sub(r"[\s\-_]", "", name).lower()


def hash_order(name: str) -> str:
    return hashlib.sha256(f"{HASH_SALT} | {name}".encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _download(url: str, dest: Path, timeout: int = 120) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": f"asa-astro/{EXP_ID}"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"url": url, "path": str(dest.relative_to(ROOT)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "retrieved_at": _now()}


def fetch() -> dict[str, Any]:
    """Retrieve the two new sources and record every source's identity in PROVENANCE.json."""
    manifest = load_manifest()
    prov: dict[str, Any] = {"experiment": EXP_ID, "written_at": _now(), "sources": {}}
    for key in ("exoplanets", "gaia_hosts"):
        entry = manifest.entries[key]
        files = []
        for f in entry["files"]:
            path = ROOT / f["path"]
            actual = sha256_file(path) if path.exists() else None
            files.append({**f, "present": path.exists(), "sha256_verified": actual == f["sha256"]})
        prov["sources"][key] = {"role": "astro_input", "title": entry["title"], "url": entry["url"], "release": entry["release"],
                                "licence": entry["licence"], "citation": entry["citation"], "retrieved_at": entry["retrieved_at"], "files": files}
    prov["sources"]["exoclock"] = {"role": "reference_truth", "title": "ExoClock planet database (ephemeris priority)",
                                   "release": "live database", "licence": "Public database offered for programmatic access on the ExoClock database page; cite Kokori et al. 2022 (ApJS 258, 40) and 2023 (ApJS 265, 4)",
                                   "citation": "Kokori A. et al., 2022, ApJS 258, 40; Kokori A. et al., 2023, ApJS 265, 4",
                                   **_download(EXOCLOCK_URL, EXOCLOCK_RAW)}
    prov["sources"]["reflinks"] = {"role": "leakage_check", "title": "NASA Exoplanet Archive pscomppars ephemeris reference links (tran_flag = 1)",
                                   "release": "live table", "licence": "Public domain / NASA data policy; cite the archive (doi:10.26133/NEA13)",
                                   "citation": "NASA Exoplanet Archive, operated by Caltech under contract with NASA",
                                   **_download(REFLINK_URL, REFLINK_RAW)}
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    (DATASET_DIR / "PROVENANCE.json").write_text(json.dumps(prov, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return prov


def _f(v: Any) -> float | None:
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def _same(a: Any, b: Any) -> bool:
    fa, fb = _f(a), _f(b)
    if fa is None and fb is None:
        return True
    if fa is None or fb is None:
        return False
    return abs(fa - fb) <= 1e-9 * max(1.0, abs(fa), abs(fb))


def _refstr(link: str) -> str:
    m = re.search(r"refstr=([^\s>]+)", link or "")
    return m.group(1) if m else (link or "").strip()


def select() -> dict[str, Any]:
    """Apply the declared candidate rules and write the frozen extract. Deterministic given the raw files."""
    prov = json.loads((DATASET_DIR / "PROVENANCE.json").read_text(encoding="utf-8"))
    exo_path = ROOT / prov["sources"]["exoplanets"]["files"][0]["path"]
    gaia_path = ROOT / prov["sources"]["gaia_hosts"]["files"][0]["path"]
    for key, path in (("exoplanets", exo_path), ("gaia_hosts", gaia_path)):
        expected = prov["sources"][key]["files"][0]["sha256"]
        if sha256_file(path) != expected:
            raise RuntimeError(f"{key} snapshot digest drifted from {expected}")
    for key, path in (("exoclock", EXOCLOCK_RAW), ("reflinks", REFLINK_RAW)):
        if sha256_file(path) != prov["sources"][key]["sha256"]:
            raise RuntimeError(f"{key} raw file digest drifted")

    exoclock = json.loads(EXOCLOCK_RAW.read_text(encoding="utf-8"))
    with exo_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        exo_cols = list(reader.fieldnames or [])
        exo_rows = list(reader)
    with REFLINK_RAW.open(encoding="utf-8", newline="") as fh:
        ref_rows = {r["pl_name"]: r for r in csv.DictReader(fh)}
    with gaia_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        gaia_cols = list(reader.fieldnames or [])
        gaia_rows = list(reader)

    transiting = [r for r in exo_rows if r.get("tran_flag") == "1" and _f(r.get("pl_orbper")) is not None and _f(r.get("pl_tranmid")) is not None]
    by_norm = {normalise_name(r["pl_name"]): r for r in transiting}
    transiting_per_host: dict[str, int] = {}
    for r in transiting:
        transiting_per_host[r["hostname"]] = transiting_per_host.get(r["hostname"], 0) + 1

    matched, unmatched, exclusions = {}, [], []
    exoclock_per_host: dict[str, int] = {}
    for name, rec in sorted(exoclock.items()):
        if rec.get("priority") not in GRADE:
            exclusions.append({"name": name, "rule": 1, "reason": f"priority {rec.get('priority')!r} not in the declared label set"})
            continue
        row = by_norm.get(normalise_name(name))
        if row is None:
            unmatched.append(name)
            continue
        matched[name] = row
        exoclock_per_host[row["hostname"]] = exoclock_per_host.get(row["hostname"], 0) + 1

    pool, leakage_flagged, missing_uncertainty = [], [], []
    reference: dict[str, Any] = {}
    for name, row in sorted(matched.items()):
        pl = row["pl_name"]
        rec = exoclock[name]
        reference[pl] = {"exoclock_name": name, "priority": rec["priority"], "grade": GRADE[rec["priority"]],
                         **{k: rec.get(k) for k in REFERENCE_FIELDS if k not in ("name", "priority")}}
        if transiting_per_host[row["hostname"]] != 1 or exoclock_per_host[row["hostname"]] != 1:
            exclusions.append({"name": pl, "rule": 4, "reason": f"host {row['hostname']} has {transiting_per_host[row['hostname']]} transiting planets in the archive and {exoclock_per_host[row['hostname']]} ExoClock entries"})
            continue
        if _f(row.get("pl_orbpererr1")) is None or _f(row.get("pl_tranmiderr1")) is None:
            missing_uncertainty.append(pl)
            continue
        ref = ref_rows.get(pl)
        if ref is None:
            exclusions.append({"name": pl, "rule": 5, "reason": "no reference-link row for this planet in the live archive query"})
            continue
        consistent = all(_same(row.get(c), ref.get(c)) for c in ("pl_orbper", "pl_orbpererr1", "pl_tranmid", "pl_tranmiderr1"))
        refs = (_refstr(ref.get("pl_orbper_reflink")), _refstr(ref.get("pl_tranmid_reflink")))
        leaked = any("KOKORI" in s.upper() for s in refs)
        if not consistent:
            exclusions.append({"name": pl, "rule": 5, "reason": "live archive ephemeris values differ from the 2026-09-02 snapshot; reference not attributable", "reflinks": refs})
            continue
        if leaked:
            leakage_flagged.append({"name": pl, "reflinks": refs})
            continue
        pool.append(pl)

    ordered = sorted(pool, key=lambda n: (hash_order(n), n))
    primary = ordered[:PRIMARY_SAMPLE_SIZE]
    hosts_needed = {matched_row["hostname"] for n, matched_row in matched.items() if matched_row["pl_name"] in set(pool) | {x["name"] for x in leakage_flagged} | set(missing_uncertainty)}

    # frozen extract: every archive row of every host in scope (all its planets), and every Gaia row of those hosts
    input_rows = [r for r in exo_rows if r["hostname"] in hosts_needed]
    gaia_ids = {r["gaia_dr3_id"].replace("Gaia DR3 ", "").strip() for r in input_rows if r.get("gaia_dr3_id")}
    input_gaia = [r for r in gaia_rows if r.get("source_id") in gaia_ids]
    _write_csv(DATASET_DIR / "input_pscomppars_rows.csv", exo_cols, input_rows)
    _write_csv(DATASET_DIR / "input_gaia_rows.csv", gaia_cols, input_gaia)
    ref_cols = REFLINK_COLS.split(",")
    _write_csv(DATASET_DIR / "leakage_reflinks.csv", ref_cols,
               [ref_rows[r["pl_name"]] for r in sorted(matched.values(), key=lambda r: r["pl_name"]) if r["pl_name"] in ref_rows])
    (DATASET_DIR / "reference_exoclock_priority.json").write_text(json.dumps(reference, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    grades = [reference[n]["grade"] for n in primary]
    selection = {
        "experiment": EXP_ID, "selected_at": _now(), "hash_salt": HASH_SALT, "primary_sample_size": PRIMARY_SAMPLE_SIZE,
        "counts": {"exoclock_planets": len(exoclock), "matched": len(matched), "unmatched": len(unmatched), "single_host_with_uncertainties_pool_plus_flagged": len(pool) + len(leakage_flagged),
                   "leakage_flagged": len(leakage_flagged), "missing_uncertainty_heldout": len(missing_uncertainty), "pool": len(pool), "primary": len(primary),
                   "primary_grade_counts": {g: grades.count(GRADE[g]) for g in GRADE}, "pool_grade_counts": {g: sum(1 for n in pool if reference[n]["grade"] == GRADE[g]) for g in GRADE}},
        "primary": primary, "pool_ordered": ordered, "leakage_flagged": leakage_flagged, "missing_uncertainty": sorted(missing_uncertainty),
        "unmatched": sorted(unmatched), "exclusions": exclusions,
        "input_files": {p.name: {"sha256": sha256_file(p), "bytes": p.stat().st_size} for p in sorted(DATASET_DIR.glob("*")) if p.name != "candidates.json"},
    }
    (DATASET_DIR / "candidates.json").write_text(json.dumps(selection, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return selection


def _write_csv(path: Path, cols: list[str], rows: list[dict[str, Any]]) -> None:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in cols})
    path.write_text(buf.getvalue(), encoding="utf-8")


def load_selection() -> dict[str, Any]:
    return json.loads((DATASET_DIR / "candidates.json").read_text(encoding="utf-8"))


def load_reference() -> dict[str, Any]:
    return json.loads((DATASET_DIR / "reference_exoclock_priority.json").read_text(encoding="utf-8"))


def verify_dataset() -> dict[str, Any]:
    """Every frozen extract file must match the digest recorded at selection."""
    sel = load_selection()
    out = {}
    for name, rec in sel["input_files"].items():
        p = DATASET_DIR / name
        out[name] = {"expected": rec["sha256"], "actual": sha256_file(p) if p.exists() else None}
        out[name]["ok"] = out[name]["expected"] == out[name]["actual"]
    return out
