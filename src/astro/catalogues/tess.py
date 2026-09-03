"""TESS light curves from MAST: search by TIC id, download SPOC 2-minute light-curve files, read them with a
minimal FITS binary-table reader (stdlib only), and produce time_series evidence whose data lives on disk
under a digest.

Time stamps are BTJD (BJD − 2457000, TDB); converted to UTC ignoring TDB−UTC as elsewhere, and stated.
"""

from __future__ import annotations

import csv
import json
import math
import struct
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from astro.domain import EvidenceRecord, Provenance
from astro_exec.core.hashing import sha256_file
from .parsers import bjd_tdb_to_utc

ROOT = Path(__file__).resolve().parents[3]
TS_DIR = ROOT / "var" / "timeseries"
MAST = "https://mast.stsci.edu/api/v0/invoke?request="
DOWNLOAD = "https://mast.stsci.edu/api/v0.1/Download/file?uri="
PROV_SOURCE = "MAST — TESS SPOC light curves"


def _mast(request: dict[str, Any]) -> dict[str, Any]:
    with urllib.request.urlopen(MAST + urllib.parse.quote(json.dumps(request)), timeout=300) as resp:
        return json.loads(resp.read().decode())


def search_lightcurves(tic: str) -> list[dict[str, Any]]:
    """SPOC 2-minute light-curve observations for a TIC id (single-sector products)."""
    r = _mast({"service": "Mast.Caom.Filtered", "format": "json", "params": {
        "columns": "obsid,obs_id,t_min,t_max,t_exptime,provenance_name,calib_level,target_name,sequence_number",
        "filters": [{"paramName": "obs_collection", "values": ["TESS"]}, {"paramName": "dataproduct_type", "values": ["timeseries"]},
                    {"paramName": "target_name", "values": [str(tic)]}]}})
    rows = [x for x in r.get("data", []) if x.get("provenance_name") == "SPOC" and x.get("t_exptime") == 120 and "-s0" in str(x.get("obs_id")) and str(x.get("obs_id")).count("-s0") == 1]
    return sorted(rows, key=lambda x: x["t_min"])


def lightcurve_product(obsid: int) -> dict[str, Any] | None:
    p = _mast({"service": "Mast.Caom.Products", "format": "json", "params": {"obsid": obsid}})
    lcs = [x for x in p.get("data", []) if x.get("productSubGroupDescription") == "LC"]
    return lcs[0] if lcs else None


def download(uri: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(DOWNLOAD + urllib.parse.quote(uri), timeout=600) as resp:
        dest.write_bytes(resp.read())
    return dest


# ---- minimal FITS BINTABLE reader --------------------------------------------------------------------------
_FMT = {"D": ("d", 8), "E": ("f", 4), "J": ("i", 4), "I": ("h", 2), "K": ("q", 8), "B": ("B", 1), "L": ("?", 1)}


def _headers(data: bytes) -> list[tuple[dict[str, str], int, int]]:
    """Return (header cards, data start, data length) for each HDU."""
    out, pos = [], 0
    while pos < len(data):
        cards: dict[str, str] = {}
        p = pos
        while True:
            block = data[p:p + 2880]
            if not block:
                return out
            for i in range(0, 2880, 80):
                card = block[i:i + 80].decode("ascii", "replace")
                key = card[:8].strip()
                if key == "END":
                    break
                if "=" in card[8:10]:
                    val = card[10:].split("/")[0].strip().strip("'").strip()
                    cards[key] = val
            p += 2880
            if key == "END":
                break
        naxis = int(cards.get("NAXIS", "0") or 0)
        size = 0
        if naxis:
            size = abs(int(cards.get("BITPIX", "8"))) // 8
            for n in range(1, naxis + 1):
                size *= int(cards.get(f"NAXIS{n}", "0"))
            size *= int(cards.get("GCOUNT", "1")) if "GCOUNT" in cards else 1
            size += int(cards.get("PCOUNT", "0")) if "PCOUNT" in cards else 0
        out.append((cards, p, size))
        pos = p + ((size + 2879) // 2880) * 2880
    return out


def read_bintable(data: bytes, wanted: tuple[str, ...]) -> dict[str, list[float]]:
    for cards, start, size in _headers(data):
        if cards.get("XTENSION") == "BINTABLE" and cards.get("EXTNAME", "").upper() in ("LIGHTCURVE", ""):
            nrow, rowlen, nfield = int(cards["NAXIS2"]), int(cards["NAXIS1"]), int(cards["TFIELDS"])
            offsets, fmts, names = [], [], []
            off = 0
            for i in range(1, nfield + 1):
                tform, ttype = cards[f"TFORM{i}"], cards.get(f"TTYPE{i}", f"col{i}")
                count = int("".join(ch for ch in tform if ch.isdigit()) or "1")
                code = tform[-1] if tform[-1] in _FMT else next((ch for ch in tform if ch in _FMT), "A")
                if code == "A" or code not in _FMT:
                    width = count
                    fmts.append(None)
                else:
                    width = _FMT[code][1] * count
                    fmts.append((_FMT[code][0], count))
                offsets.append(off); names.append(ttype); off += width
            cols = {w: [] for w in wanted}
            idx = {names[i]: i for i in range(nfield) if names[i] in wanted}
            for r in range(nrow):
                base = start + r * rowlen
                for name, i in idx.items():
                    fmt = fmts[i]
                    if fmt is None:
                        continue
                    v = struct.unpack(">" + fmt[0] * fmt[1], data[base + offsets[i]: base + offsets[i] + struct.calcsize(">" + fmt[0] * fmt[1])])
                    cols[name].append(v[0] if fmt[1] == 1 else v)
            return cols
    raise ValueError("no LIGHTCURVE binary table found")


@dataclass(frozen=True, slots=True)
class LightCurveSummary:
    path: Path
    sha256: str
    n_points: int
    n_good: int
    start_btjd: float
    end_btjd: float
    cadence_minutes: float
    rms_ppm: float | None


def summarise(fits_path: Path, csv_path: Path) -> LightCurveSummary:
    cols = read_bintable(fits_path.read_bytes(), ("TIME", "PDCSAP_FLUX", "PDCSAP_FLUX_ERR", "QUALITY"))
    rows = [(t, f, e, q) for t, f, e, q in zip(cols["TIME"], cols["PDCSAP_FLUX"], cols["PDCSAP_FLUX_ERR"], cols["QUALITY"]) if t == t and f == f]
    good = [(t, f) for t, f, e, q in rows if q == 0]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["time_btjd", "pdcsap_flux", "pdcsap_flux_err", "quality"])
        for t, f, e, q in rows:
            w.writerow([f"{t:.7f}", f"{f:.4f}", f"{e:.4f}", int(q)])
    times = [t for t, _ in good]
    dts = sorted(b - a for a, b in zip(times, times[1:]) if b > a)
    cadence = (dts[len(dts) // 2] * 1440.0) if dts else float("nan")
    rms = None
    if len(good) > 10:
        mean = sum(f for _, f in good) / len(good)
        rms = math.sqrt(sum((f / mean - 1.0) ** 2 for _, f in good) / len(good)) * 1e6
    return LightCurveSummary(csv_path, sha256_file(csv_path), len(rows), len(good), min(t for t, *_ in rows), max(t for t, *_ in rows), cadence, rms)


def fetch_tess_for_host(entity_id: str, tic: str, *, max_sectors: int = 2, retrieved_at: str) -> list[EvidenceRecord]:
    """Download up to ``max_sectors`` SPOC light curves for a host and return time_series evidence records."""
    out = []
    for obs in search_lightcurves(tic)[-max_sectors:]:
        product = lightcurve_product(obs["obsid"])
        if not product:
            continue
        fits_path = TS_DIR / "fits" / product["productFilename"]
        if not fits_path.exists():
            download(product["dataURI"], fits_path)
        csv_path = TS_DIR / f"{product['productFilename'].replace('.fits', '')}.csv"
        summary = summarise(fits_path, csv_path)
        sector = int(str(obs["obs_id"]).split("-s0")[1][:3])
        prov = Provenance(PROV_SOURCE, "real", f"tess:{product['dataURI']}", retrieved_at)
        values = {"mission": "TESS", "pipeline": "SPOC", "sector": sector, "tic": str(tic), "cadence_minutes": round(summary.cadence_minutes, 3),
                  "span_days": round(summary.end_btjd - summary.start_btjd, 4), "n_points": summary.n_points, "n_good": summary.n_good,
                  "start_utc": bjd_tdb_to_utc(summary.start_btjd + 2457000.0), "end_utc": bjd_tdb_to_utc(summary.end_btjd + 2457000.0),
                  "time_system": "BTJD (BJD_TDB − 2457000); UTC conversion ignores TDB−UTC", "flux": "PDCSAP_FLUX, quality==0",
                  "data_ref": str(csv_path.relative_to(ROOT)), "data_sha256": summary.sha256, "source_file": product["productFilename"]}
        if summary.rms_ppm is not None:
            values["rms_ppm"] = round(summary.rms_ppm, 1)
        out.append(EvidenceRecord.create("time_series", entity_id, observed_at=values["end_utc"], values=values, source=prov, quality=0.95))
    return out
