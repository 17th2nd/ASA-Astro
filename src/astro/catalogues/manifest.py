"""Source registry and digest manifest for raw catalogue snapshots."""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from astro_exec.core.hashing import sha256_file

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "data" / "catalogues" / "raw"
MANIFEST = ROOT / "data" / "catalogues" / "manifest.json"


@dataclass(frozen=True, slots=True)
class SourceSpec:
    key: str
    title: str
    url: str
    filename: str
    release: str
    licence: str
    citation: str
    kind: str                     # csv | json | html
    notes: str = ""

    def path(self) -> Path:
        return RAW / self.filename


_EXO_COLS = ("pl_name,hostname,ra,dec,sy_vmag,sy_gaiamag,sy_dist,st_spectype,st_teff,st_rad,st_mass,pl_orbper,pl_orbpererr1,"
             "pl_tranmid,pl_tranmiderr1,pl_trandur,pl_rade,pl_bmasse,tran_flag,discoverymethod,disc_year,disc_facility,gaia_dr2_id,gaia_dr3_id,tic_id,hd_name,hip_name")

SOURCES: dict[str, SourceSpec] = {s.key: s for s in (
    SourceSpec("exoplanets", "NASA Exoplanet Archive — Planetary Systems Composite Parameters (pscomppars)",
               f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+{_EXO_COLS}+from+pscomppars&format=csv",
               "exoplanetarchive_pscomppars.csv", "live table (composite parameters; no versioned release)",
               "Public domain / NASA data policy; cite the archive (doi:10.26133/NEA13)",
               "NASA Exoplanet Archive, operated by Caltech under contract with NASA", "csv",
               "pl_tranmid is BJD_TDB; converted to UTC ignoring the ~69 s TDB−UTC offset and light-time, recorded in the evidence."),
    SourceSpec("gcvs", "General Catalogue of Variable Stars (GCVS 5.1), VizieR B/gcvs/gcvs_cat",
               "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&MAXREC=100000&QUERY=select+VarNum,GCVS,RAJ2000,DEJ2000,VarType,magMax,Min1,flt,Epoch,Period,SpType+from+%22B/gcvs/gcvs_cat%22",
               "vizier_gcvs.csv", "GCVS 5.1 via VizieR", "CDS/VizieR terms; cite Samus+ 2017",
               "Samus N.N. et al., 2017, Astronomy Reports 61, 80", "csv"),
    SourceSpec("openngc", "OpenNGC — NGC/IC deep-sky objects",
               "https://raw.githubusercontent.com/mattiaverga/OpenNGC/master/database_files/NGC.csv",
               "openngc_NGC.csv", "master branch snapshot (see retrieval time)", "CC-BY-SA-4.0 (share-alike: derived redistribution must carry the same licence)",
               "Mattia Verga, OpenNGC, https://github.com/mattiaverga/OpenNGC", "csv"),
    SourceSpec("mpc_sites", "IAU Minor Planet Center observatory codes",
               "https://www.minorplanetcenter.net/iau/lists/ObsCodes.html", "mpc_ObsCodes.html", "live list",
               "MPC public data", "IAU Minor Planet Center, ObsCodes list", "html",
               "Parallax constants (longitude, ρcosφ', ρsinφ') converted to geodetic latitude and approximate elevation; recorded as derived."),
    SourceSpec("huntreffert_clusters", "Hunt & Reffert 2023 open clusters, VizieR J/A+A/673/A114/clusters",
               "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&MAXREC=100000&QUERY=select+Name,Type,RA_ICRS,DE_ICRS,r50,N,Plx,dist50,logAge50+from+%22J/A%2BA/673/A114/clusters%22",
               "vizier_huntreffert_clusters.csv", "2023 catalogue via VizieR", "CDS/VizieR terms; cite Hunt & Reffert 2023",
               "Hunt E.L., Reffert S., 2023, A&A 673, A114", "csv"),
    SourceSpec("gaia_hosts", "Gaia DR3 gaia_source_lite for NASA Exoplanet Archive host stars (by gaia_dr3_id)",
               "https://gea.esac.esa.int/tap-server/tap/sync (POST; ADQL: select source_id,ra,dec,parallax,parallax_error,pmra,pmdec,phot_g_mean_mag,phot_bp_mean_mag,phot_rp_mean_mag,radial_velocity,teff_gspphot,ruwe from gaiadr3.gaia_source_lite where source_id in (...); batches of 800)",
               "gaia_dr3_hosts.csv", "Gaia DR3 (2022-06-13)", "ESA Gaia data policy; cite Gaia Collaboration 2016, 2023",
               "Gaia Collaboration, Vallenari et al. 2023, A&A 674, A1", "csv", "Astrometric epoch J2016.0; positions used as-is (no proper-motion propagation)."),
    SourceSpec("alerce_sn", "ALeRCE ZTF light-curve classifier — recent supernova candidates",
               "https://api.alerce.online/ztf/v1/objects/?classifier=lc_classifier&class={cls}&ranking=1&probability=0.4&firstmjd=61240&page_size=500&order_by=lastmjd&order_mode=DESC",
               "alerce_{cls}.json", "live API (ZTF public alerts)", "ALeRCE/ZTF public; cite Förster+ 2021",
               "Förster F. et al., 2021, AJ 161, 242; ZTF public alert stream", "json",
               "One file per class in SNIa, SNII, SNIbc, SLSN. Classifier probability is used as alert confidence."),
)}


@dataclass(frozen=True, slots=True)
class Manifest:
    entries: dict[str, dict[str, Any]]

    def entry(self, key: str) -> dict[str, Any]:
        return self.entries[key]


def load_manifest() -> Manifest:
    if MANIFEST.exists():
        return Manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))
    return Manifest({})


def _save(m: Manifest) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m.entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def record_snapshot(spec: SourceSpec, files: list[Path], retrieved_at: str | None = None) -> dict[str, Any]:
    """Register existing raw files for a source in the manifest (digests, sizes, retrieval time)."""
    m = load_manifest()
    entry = {
        "title": spec.title, "url": spec.url, "release": spec.release, "licence": spec.licence, "citation": spec.citation,
        "retrieved_at": retrieved_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "notes": spec.notes,
        "files": [{"path": str(f.relative_to(ROOT)), "sha256": sha256_file(f), "bytes": f.stat().st_size} for f in files],
    }
    m.entries[spec.key] = entry
    _save(m)
    return entry


def fetch_source(key: str, classes: tuple[str, ...] = ("SNIa", "SNII", "SNIbc", "SLSN")) -> dict[str, Any]:
    """Download a source into the raw cache and record it. Never runs inside an evaluation."""
    spec = SOURCES[key]
    RAW.mkdir(parents=True, exist_ok=True)
    files = []
    targets = [(spec.url.format(cls=c), RAW / spec.filename.format(cls=c)) for c in classes] if "{cls}" in spec.url else [(spec.url, spec.path())]
    for url, path in targets:
        with urllib.request.urlopen(url, timeout=600) as resp:
            path.write_bytes(resp.read())
        files.append(path)
    return record_snapshot(spec, files)


def verify_snapshots() -> dict[str, bool]:
    """True per source when every recorded raw file exists with its recorded digest."""
    m = load_manifest()
    out = {}
    for key, entry in m.entries.items():
        out[key] = all((ROOT / f["path"]).exists() and sha256_file(ROOT / f["path"]) == f["sha256"] for f in entry["files"])
    return out
