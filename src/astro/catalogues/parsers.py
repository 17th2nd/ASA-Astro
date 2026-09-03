"""Parsers: raw catalogue snapshots → Fragment (entities, evidence, relationships), one row → one provenance."""

from __future__ import annotations

import csv
import json
import math
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from astro.domain import Coordinates, Entity, EntityState, EvidenceRecord, Provenance, RelationshipAssertion
from .fragments import Fragment
from .manifest import RAW, SOURCES, load_manifest


def _prov(key: str, row_ref: str, data_class: str = "real") -> Provenance:
    spec, m = SOURCES[key], load_manifest()
    entry = m.entries.get(key, {})
    return Provenance(source=spec.title, data_class=data_class, reference=f"{key}:{row_ref}", retrieved_at=entry.get("retrieved_at"))


def _f(value: Any) -> float | None:
    try:
        v = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def _s(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _rows(path: Path, delimiter: str = ",") -> Iterable[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        yield from csv.DictReader(fh, delimiter=delimiter)


def sexagesimal_to_deg(text: str, hours: bool) -> float | None:
    parts = re.split(r"[:\s]+", text.strip())
    if len(parts) < 2:
        return None
    try:
        sign = -1.0 if parts[0].strip().startswith("-") else 1.0
        a, b = abs(float(parts[0])), float(parts[1])
        c = float(parts[2]) if len(parts) > 2 and parts[2] else 0.0
    except ValueError:
        return None
    value = a + b / 60.0 + c / 3600.0
    return (value * 15.0) if hours else sign * value


def bjd_tdb_to_utc(bjd: float) -> str:
    """BJD(TDB) → ISO UTC. Ignores the ~69 s TDB−UTC offset and Earth light-time (up to ~8 min); recorded in evidence."""
    unix = (bjd - 2440587.5) * 86400.0
    return datetime.fromtimestamp(unix, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mjd_to_utc(mjd: float) -> str:
    return (datetime(1858, 11, 17, tzinfo=timezone.utc) + timedelta(days=mjd)).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---- NASA Exoplanet Archive ----------------------------------------------------------------------------
def parse_exoplanets(path: Path | None = None) -> Fragment:
    path = path or SOURCES["exoplanets"].path()
    frag = Fragment("exoplanets")
    hosts: dict[str, Entity] = {}
    for row in _rows(path):
        host_name, pl_name = _s(row.get("hostname")), _s(row.get("pl_name"))
        ra, dec = _f(row.get("ra")), _f(row.get("dec"))
        if not host_name or not pl_name or ra is None or dec is None:
            frag.skipped.append({"row": pl_name or host_name, "reason": "missing name or coordinates"})
            continue
        prov = _prov("exoplanets", pl_name)
        if host_name not in hosts:
            cat = {"NASA Exoplanet Archive": host_name}
            for col, label in (("gaia_dr3_id", "Gaia DR3"), ("gaia_dr2_id", "Gaia DR2"), ("gaia_id", "Gaia"), ("tic_id", "TIC"), ("hd_name", "HD"), ("hip_name", "HIP")):
                v = _s(row.get(col))
                if v:
                    cat[label] = v.replace(label + " ", "").replace("Gaia DR2 ", "").replace("Gaia DR3 ", "").strip()
            attrs: dict[str, Any] = {}
            for col, key in (("sy_vmag", "magnitude_v"), ("sy_gaiamag", "magnitude_g"), ("sy_dist", "distance_pc"), ("st_teff", "teff_k"), ("st_rad", "radius_solar"), ("st_mass", "mass_solar")):
                v = _f(row.get(col))
                if v is not None:
                    attrs[key] = v
            if _s(row.get("st_spectype")):
                attrs["spectral_type"] = _s(row.get("st_spectype"))
            hosts[host_name] = Entity.create("star", host_name, catalogue_ids={"NASA Exoplanet Archive": host_name}, aliases=tuple(f"{k} {v}" for k, v in cat.items() if k != "NASA Exoplanet Archive"),
                                             coordinates=Coordinates(ra % 360.0, max(-90.0, min(90.0, dec))), source=_prov("exoplanets", host_name), attributes=attrs)
            frag.entities.append(hosts[host_name])
            if attrs.get("magnitude_v") is not None:
                frag.evidence.append(EvidenceRecord.create("catalogue_measurement", hosts[host_name].entity_id, values={"mag_v": attrs["magnitude_v"], "band": "V", "note": "system V magnitude as tabulated"}, source=prov, quality=0.8))
            if attrs.get("teff_k") is not None:
                frag.evidence.append(EvidenceRecord.create("derived_measurement", hosts[host_name].entity_id, values={"teff_k": attrs["teff_k"], "method": "st_teff as tabulated (composite of published values)"}, source=prov, quality=0.8))
            if attrs.get("distance_pc") is not None:
                frag.evidence.append(EvidenceRecord.create("catalogue_measurement", hosts[host_name].entity_id, values={"distance_pc": attrs["distance_pc"], "note": "sy_dist as tabulated"}, source=prov, quality=0.8))
        host = hosts[host_name]
        pattrs: dict[str, Any] = {}
        for col, key in (("pl_rade", "radius_earth"), ("pl_bmasse", "mass_earth"), ("discoverymethod", "discovery_method"), ("disc_year", "discovery_year"), ("disc_facility", "discovery_facility")):
            v = row.get(col)
            if _s(v):
                pattrs[key] = _f(v) if key in ("radius_earth", "mass_earth", "discovery_year") else _s(v)
                if pattrs[key] is None:
                    pattrs.pop(key)
        planet = Entity.create("exoplanet", pl_name, catalogue_ids={"NASA Exoplanet Archive": pl_name}, coordinates=host.coordinates, source=prov, attributes=pattrs)
        frag.entities.append(planet)
        evidence_ids = []
        period, tmid, dur = _f(row.get("pl_orbper")), _f(row.get("pl_tranmid")), _f(row.get("pl_trandur"))
        transits = _s(row.get("tran_flag")) == "1"
        if period and tmid and transits:
            unc = {k: v for k, v in (("period_days", _f(row.get("pl_orbpererr1"))), ("epoch_days", _f(row.get("pl_tranmiderr1")))) if v is not None}
            eph = EvidenceRecord.create("ephemeris", host.entity_id, values={"period_days": period, "epoch_utc": bjd_tdb_to_utc(tmid), "epoch_bjd_tdb": tmid,
                                                                             "duration_hours": dur if dur else 2.0, "duration_source": "tabulated" if dur else "assumed 2.0 h (pl_trandur absent)",
                                                                             "planet": pl_name, "time_conversion": "BJD_TDB→UTC without TDB−UTC offset or light-time"},
                                        uncertainty=unc, source=prov, quality=0.9 if dur else 0.7)
            frag.evidence.append(eph)
            evidence_ids.append(eph.evidence_id)
        elif period:
            orb = EvidenceRecord.create("catalogue_measurement", planet.entity_id, values={"period_days": period, "transits": transits}, source=prov, quality=0.8)
            frag.evidence.append(orb)
            evidence_ids.append(orb.evidence_id)
        frag.relationships.append(RelationshipAssertion.create("hosts", {"host": host.entity_id, "companion": planet.entity_id}, evidence_ids=evidence_ids,
                                                               confidence=0.99 if evidence_ids else 0.9, source=prov))
    return frag


# ---- GCVS variable stars ---------------------------------------------------------------------------------
def parse_gcvs(path: Path | None = None) -> Fragment:
    path = path or SOURCES["gcvs"].path()
    frag = Fragment("gcvs")
    for row in _rows(path):
        name = re.sub(r"\s+", " ", _s(row.get("GCVS")))
        ra, dec = _f(row.get("RAJ2000")), _f(row.get("DEJ2000"))
        if not name or ra is None or dec is None:
            frag.skipped.append({"row": name or row.get("VarNum"), "reason": "missing name or coordinates"})
            continue
        prov = _prov("gcvs", _s(row.get("VarNum")) or name)
        attrs: dict[str, Any] = {"variability_type": _s(row.get("VarType"))}
        mag_max = _f(row.get("magMax"))
        if mag_max is not None:
            attrs["magnitude_max"] = mag_max
            attrs["magnitude_band"] = _s(row.get("flt"))
        if _s(row.get("SpType")):
            attrs["spectral_type"] = _s(row.get("SpType"))
        star = Entity.create("variable_star", name, catalogue_ids={"GCVS": _s(row.get("VarNum")) or name}, coordinates=Coordinates(ra % 360.0, max(-90.0, min(90.0, dec))), source=prov, attributes=attrs)
        frag.entities.append(star)
        values: dict[str, Any] = {"class": _s(row.get("VarType"))}
        period = _f(row.get("Period"))
        if period:
            values["period_days"] = period
        if mag_max is not None:
            values["mag_max"] = mag_max
        if _f(row.get("Min1")) is not None:
            values["mag_min"] = _f(row.get("Min1"))
        epoch = _f(row.get("Epoch"))
        if epoch:
            values["epoch_jd"] = epoch + 2400000.0 if epoch < 2400000 else epoch
        frag.evidence.append(EvidenceRecord.create("classification", star.entity_id, values=values, source=prov, quality=0.85))
        if mag_max is not None:
            phot = {"mag_max": mag_max, "band": _s(row.get("flt")) or "unspecified", "note": "GCVS maximum-light magnitude; minimum in mag_min where given"}
            if _f(row.get("Min1")) is not None:
                phot["mag_min"] = _f(row.get("Min1"))
            frag.evidence.append(EvidenceRecord.create("photometry", star.entity_id, values=phot, source=prov, quality=0.7))
    return frag


# ---- OpenNGC deep-sky ------------------------------------------------------------------------------------
_NGC_KIND = {"G": "galaxy", "GPair": "galaxy", "GTrpl": "galaxy", "GGroup": "galaxy", "PN": "nebula", "HII": "nebula", "DrkN": "nebula", "EmN": "nebula",
             "Neb": "nebula", "RfN": "nebula", "SNR": "nebula", "Cl+N": "nebula", "OCl": "star_cluster", "GCl": "star_cluster", "*Ass": "star_cluster",
             "*": "star", "**": "star", "Nova": "transient", "Other": "sky_region", "Dup": None, "NonEx": None}


def parse_openngc(path: Path | None = None) -> Fragment:
    path = path or SOURCES["openngc"].path()
    frag = Fragment("openngc")
    for row in _rows(path, delimiter=";"):
        name, typ = _s(row.get("Name")), _s(row.get("Type"))
        kind = _NGC_KIND.get(typ, "sky_region")
        if kind is None:
            frag.skipped.append({"row": name, "reason": f"type {typ}"})
            continue
        ra, dec = sexagesimal_to_deg(_s(row.get("RA")), hours=True), sexagesimal_to_deg(_s(row.get("Dec")), hours=False)
        if ra is None or dec is None:
            frag.skipped.append({"row": name, "reason": "no coordinates"})
            continue
        prov = _prov("openngc", name)
        attrs: dict[str, Any] = {"object_type": typ, "constellation": _s(row.get("Const"))}
        for col, key in (("V-Mag", "magnitude_v"), ("B-Mag", "magnitude_b"), ("MajAx", "major_axis_arcmin"), ("MinAx", "minor_axis_arcmin"), ("Redshift", "redshift"), ("SurfBr", "surface_brightness")):
            v = _f(row.get(col))
            if v is not None:
                attrs[key] = v
        if _s(row.get("Hubble")):
            attrs["morphology"] = _s(row.get("Hubble"))
        cats = {"NGC/IC": name}
        if _s(row.get("M")):
            cats["Messier"] = f"M{int(_f(row['M']))}" if _f(row.get("M")) is not None else _s(row.get("M"))
        aliases = tuple(a.strip() for a in _s(row.get("Identifiers")).split(",") if a.strip()) + ((cats["Messier"],) if "Messier" in cats else ())
        ent = Entity.create(kind, name, catalogue_ids=cats, aliases=aliases, coordinates=Coordinates(ra % 360.0, max(-90.0, min(90.0, dec))), source=prov, attributes=attrs)
        frag.entities.append(ent)
        if "magnitude_v" in attrs or "magnitude_b" in attrs:
            frag.evidence.append(EvidenceRecord.create("catalogue_measurement", ent.entity_id, values={k: v for k, v in attrs.items() if k.startswith("magnitude") or k == "redshift"}, source=prov, quality=0.7))
    return frag


# ---- Hunt & Reffert clusters -------------------------------------------------------------------------------
def parse_clusters(path: Path | None = None) -> Fragment:
    path = path or SOURCES["huntreffert_clusters"].path()
    frag = Fragment("huntreffert_clusters")
    for row in _rows(path):
        name = _s(row.get("Name"))
        ra, dec = _f(row.get("RA_ICRS")), _f(row.get("DE_ICRS"))
        if not name or ra is None or dec is None:
            frag.skipped.append({"row": name, "reason": "missing"})
            continue
        prov = _prov("huntreffert_clusters", name)
        attrs: dict[str, Any] = {"cluster_kind": {"o": "open_cluster", "m": "moving_group", "g": "globular_cluster"}.get(_s(row.get("Type")), _s(row.get("Type")))}
        for col, key in (("r50", "r50_deg"), ("N", "member_count"), ("Plx", "parallax_mas"), ("pmRA", "pmra_mas_yr"), ("pmDE", "pmdec_mas_yr"), ("dist50", "distance_pc"), ("logAge50", "log_age_yr")):
            v = _f(row.get(col))
            if v is not None:
                attrs[key] = v
        ent = Entity.create("star_cluster", name, catalogue_ids={"HuntReffert2023": name}, coordinates=Coordinates(ra % 360.0, max(-90.0, min(90.0, dec))), source=prov, attributes=attrs)
        frag.entities.append(ent)
        frag.evidence.append(EvidenceRecord.create("catalogue_measurement", ent.entity_id, values={k: v for k, v in attrs.items() if k != "cluster_kind"}, source=prov, quality=0.85))
    return frag


# ---- MPC observatory sites -----------------------------------------------------------------------------------
def parse_mpc_sites(path: Path | None = None) -> Fragment:
    """Fixed-width: code(3) longitude(10) ρcosφ'(9) ρsinφ'(9) name. Geodetic conversion is approximate (derived)."""
    path = path or SOURCES["mpc_sites"].path()
    frag = Fragment("mpc_sites")
    text = path.read_text(encoding="utf-8", errors="replace")
    body = text.split("<pre>", 1)[-1].split("</pre>", 1)[0]
    for line in body.splitlines():
        if len(line) < 31 or line.startswith("Code"):
            continue
        code, lon, c, s, name = line[0:3].strip(), _f(line[4:13]), _f(line[13:21]), _f(line[21:30]), line[30:].strip()
        if not code or lon is None or c is None or s is None or not name or (c == 0 and s == 0):
            continue
        rho = math.hypot(c, s)
        lat_gc = math.degrees(math.atan2(s, c))
        f = 1 / 298.257223563
        lat_gd = math.degrees(math.atan(math.tan(math.radians(lat_gc)) / (1 - f) ** 2)) if abs(lat_gc) < 89.9 else lat_gc
        # geocentric radius of the WGS84 ellipsoid at this geocentric latitude, in equatorial radii
        cg, sg = math.cos(math.radians(lat_gc)), math.sin(math.radians(lat_gc))
        r_ell = (1 - f) / math.sqrt(((1 - f) * cg) ** 2 + sg ** 2)
        elev = (rho - r_ell) * 6378137.0                                   # ±~0.5 km: MPC constants carry 5–6 decimals
        prov = _prov("mpc_sites", code, data_class="derived")
        ent = Entity.create("site", name, catalogue_ids={"MPC": code}, source=prov,
                            attributes={"latitude_deg": round(lat_gd, 5), "longitude_deg": round(lon % 360.0 if lon <= 180 else lon - 360.0, 5),
                                        "elevation_m": round(elev), "geodetic_note": "latitude and elevation derived from MPC parallax constants (WGS84); elevation approximate to ~0.5 km and unused by Astro features"})
        frag.entities.append(ent)
    return frag


# ---- ALeRCE ZTF transients -------------------------------------------------------------------------------
def parse_alerce(paths: list[Path] | None = None, sn_only: bool = True) -> Fragment:
    paths = paths or sorted(RAW.glob("alerce_*.json"))
    frag = Fragment("alerce_sn")
    seen = set()
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            oid, cls = _s(item.get("oid")), _s(item.get("class"))
            if not oid or oid in seen:
                continue
            if sn_only and not cls.startswith(("SN", "SLSN")):
                continue
            seen.add(oid)
            ra, dec = _f(item.get("meanra")), _f(item.get("meandec"))
            if ra is None or dec is None:
                continue
            prov = _prov("alerce_sn", oid)
            ent = Entity.create("transient", oid, catalogue_ids={"ZTF": oid}, coordinates=Coordinates(ra % 360.0, max(-90.0, min(90.0, dec))), source=prov,
                                attributes={"detections": int(item.get("ndet") or 0)})
            frag.entities.append(ent)
            last = mjd_to_utc(float(item["lastmjd"])) if item.get("lastmjd") else None
            first = mjd_to_utc(float(item["firstmjd"])) if item.get("firstmjd") else None
            frag.evidence.append(EvidenceRecord.create("alert", ent.entity_id, observed_at=last, source=prov, quality=0.7,
                                                       values={"classification": cls, "confidence": _f(item.get("probability")) or 0.0, "classifier": _s(item.get("classifier")),
                                                               "first_detection_utc": first, "detections": int(item.get("ndet") or 0),
                                                               "rarity": {"SLSN": 0.9, "SNIbc": 0.7, "SNII": 0.5, "SNIa": 0.4}.get(cls, 0.5),
                                                               "rarity_note": "declared per-class prior for benchmark use, not a measured quantity"}))
            frag.states.append(EntityState(ent.entity_id, last or first or "2026-01-01T00:00:00Z", observation_status="observed", candidate_status="candidate", alert_state="active", last_observed_at=last))
    return frag


# ---- Gaia DR3 for exoplanet hosts ----------------------------------------------------------------------------
def parse_gaia_hosts(host_by_gaia: dict[str, str], path: Path | None = None) -> Fragment:
    """Attach Gaia DR3 astrometry and photometry evidence to already-known host entities (keyed by Gaia DR3 source_id)."""
    path = path or SOURCES["gaia_hosts"].path()
    frag = Fragment("gaia_hosts")
    for row in _rows(path):
        sid = _s(row.get("source_id"))
        entity_id = host_by_gaia.get(sid)
        if entity_id is None:
            frag.skipped.append({"row": sid, "reason": "no host entity carries this Gaia DR3 id"})
            continue
        prov = _prov("gaia_hosts", sid)
        astro_vals: dict[str, Any] = {"ra_deg": _f(row.get("ra")), "dec_deg": _f(row.get("dec")), "frame": "ICRS", "epoch": "J2016.0"}
        unc: dict[str, Any] = {}
        for col, key in (("parallax", "parallax_mas"), ("pmra", "pmra_mas_yr"), ("pmdec", "pmdec_mas_yr"), ("radial_velocity", "radial_velocity_km_s"), ("ruwe", "ruwe")):
            v = _f(row.get(col))
            if v is not None:
                astro_vals[key] = v
        if _f(row.get("parallax_error")) is not None:
            unc["parallax_mas"] = _f(row.get("parallax_error"))
        ruwe = _f(row.get("ruwe"))
        quality = 0.95 if ruwe is not None and ruwe < 1.4 else 0.75
        frag.evidence.append(EvidenceRecord.create("astrometry", entity_id, values={k: v for k, v in astro_vals.items() if v is not None}, uncertainty=unc,
                                                   observed_at="2016-01-01T00:00:00Z", source=prov, quality=quality))
        phot: dict[str, Any] = {}
        for col, key in (("phot_g_mean_mag", "mag_g"), ("phot_bp_mean_mag", "mag_bp"), ("phot_rp_mean_mag", "mag_rp")):
            v = _f(row.get(col))
            if v is not None:
                phot[key] = v
        if phot:
            frag.evidence.append(EvidenceRecord.create("photometry", entity_id, values={**phot, "band_system": "Gaia DR3"}, observed_at="2016-01-01T00:00:00Z", source=prov, quality=0.95))
        teff = _f(row.get("teff_gspphot"))
        if teff is not None:
            frag.evidence.append(EvidenceRecord.create("derived_measurement", entity_id, values={"teff_k": teff, "method": "GSP-Phot"}, source=prov, quality=0.7))
    return frag


def gaia_host_map(exoplanet_fragment: Fragment) -> dict[str, str]:
    """Gaia DR3 source_id → host entity id, from the aliases the exoplanet parser attached."""
    out = {}
    for e in exoplanet_fragment.entities:
        for a in e.aliases:
            if a.startswith("Gaia DR3 "):
                out[a.split(" ", 2)[2]] = e.entity_id
    return out


PARSERS = {"exoplanets": parse_exoplanets, "gcvs": parse_gcvs, "openngc": parse_openngc, "huntreffert_clusters": parse_clusters,
           "mpc_sites": parse_mpc_sites, "alerce_sn": parse_alerce}
