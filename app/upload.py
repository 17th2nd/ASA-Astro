"""Upload registration for the ASA-Astro V1 thin app.

Preserves uploaded observation-source bytes under a content-addressed path with
sha256 integrity. Optionally invokes ``asa_astro.evidence.pipeline.process_observation``
(when the tip can decode the file) so the app can project present-only observation
honesty records (WCS / localisation / crossmatch). Does **not** bridge the
observation graph into the Objective universe — that remains Significance-owned.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Pillow-decodable formats documented by the Codex B / Operator C observation path.
PROCESSABLE_SUFFIXES = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ppm", ".bmp", ".tif", ".tiff",
})
# Accepted for preserve-source storage only until a FITS/declared-WCS adapter lands.
STORE_ONLY_SUFFIXES = frozenset({".fits", ".fit", ".fts"})
ALLOWED_SUFFIXES = PROCESSABLE_SUFFIXES | STORE_ONLY_SUFFIXES

MAX_UPLOAD_BYTES = 32 * 1024 * 1024  # 32 MiB
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+\-]{0,180}$")


class UploadError(ValueError):
    """Client-facing upload rejection."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_suffix(filename: str) -> str:
    suffix = Path(filename or "").suffix.lower()
    if suffix in ALLOWED_SUFFIXES:
        return suffix
    return ".bin"


def _safe_original_filename(filename: str | None) -> str:
    name = (filename or "upload.bin").replace("\\", "/").split("/")[-1].strip()
    if not name or name in (".", ".."):
        name = "upload.bin"
    if not SAFE_NAME.match(name):
        # Keep a usable name without path tricks; suffix still drives processability.
        suffix = _safe_suffix(name)
        stem = re.sub(r"[^A-Za-z0-9._+\-]+", "_", Path(name).stem)[:80] or "upload"
        name = f"{stem}{suffix}"
    return name



def _data_dir() -> Path:
    from . import slice as slicemod
    return slicemod.data_dir()


def uploads_dir() -> Path:
    return _data_dir() / "uploads"


def observation_bundles_dir() -> Path:
    return _data_dir() / "observation-bundles"


def guess_media_type(filename: str, declared: str | None = None) -> str:
    if declared and declared != "application/octet-stream":
        return declared
    guessed = mimetypes.guess_type(filename)[0]
    return guessed or "application/octet-stream"


def store_bytes(
    data: bytes,
    *,
    original_filename: str | None,
    media_type: str | None = None,
) -> dict[str, Any]:
    """Write a content-addressed copy under ``app/var/uploads/`` and return the source record."""
    if not data:
        raise UploadError("empty upload")
    if len(data) > MAX_UPLOAD_BYTES:
        raise UploadError(f"upload exceeds {MAX_UPLOAD_BYTES} bytes")
    filename = _safe_original_filename(original_filename)
    suffix = _safe_suffix(filename)
    if suffix not in ALLOWED_SUFFIXES:
        raise UploadError(
            "unsupported file type; accept image "
            f"({', '.join(sorted(PROCESSABLE_SUFFIXES))}) or FITS "
            f"({', '.join(sorted(STORE_ONLY_SUFFIXES))}) for preserve-source storage"
        )
    digest = _sha256(data)
    media = guess_media_type(filename, media_type)
    uploads_dir().mkdir(parents=True, exist_ok=True)
    stored_name = f"{digest}{suffix}"
    stored_path = uploads_dir() / stored_name
    if not stored_path.exists():
        tmp = Path(tempfile.mkdtemp(prefix=".up-", dir=uploads_dir()))
        try:
            candidate = tmp / stored_name
            candidate.write_bytes(data)
            if _sha256(candidate.read_bytes()) != digest:
                raise OSError("upload integrity verification failed")
            candidate.replace(stored_path)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        if _sha256(stored_path.read_bytes()) != digest:
            raise OSError(f"corrupt content-addressed upload at {stored_path}")
    processable = suffix in PROCESSABLE_SUFFIXES
    return {
        "schema": "asa-astro-app-uploaded-source-v1",
        "original_filename": filename,
        "stored_path": str(stored_path.relative_to(_data_dir())),
        "stored_abs_note": "path is relative to ASA_ASTRO_APP_DATA_DIR / app/var",
        "sha256": digest,
        "byte_size": len(data),
        "media_type": media,
        "suffix": suffix,
        "registration_policy": "content-addressed-copy",
        "integrity_status": "verified_sha256",
        "processable_by_process_observation": processable,
        "store_only": not processable,
        "registered_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))



def _expected_from_metadata(metadata_path: Path | None) -> list[dict]:
    """Pull expected catalogue entries from optional upload metadata (present-only)."""
    if metadata_path is None or not metadata_path.is_file():
        return []
    try:
        meta = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(meta, dict):
        return []
    catalogue = meta.get("catalogue")
    if isinstance(catalogue, dict) and isinstance(catalogue.get("entries"), list):
        return [e for e in catalogue["entries"] if isinstance(e, dict)]
    expected = meta.get("expected_entries")
    if isinstance(expected, list):
        return [e for e in expected if isinstance(e, dict)]
    return []


def _compute_residuals(bundle_dir: Path, metadata_path: Path | None) -> dict | None:
    """Present-only Action residuals/action_ui from tip ``asa_astro.residuals``."""
    from asa_astro.residuals.observed_vs_expected import ResidualsError, compute_from_observation_bundle

    expected = _expected_from_metadata(metadata_path)
    try:
        report = compute_from_observation_bundle(bundle_dir, expected)
    except ResidualsError as exc:
        return {
            "present": False,
            "error": str(exc),
            "residuals": [],
            "missing_expected": [],
            "next_evidence_recommendations": [],
            "action_ui": None,
        }
    report = dict(report)
    report["present"] = True
    return report



def _honesty_flag(summary: dict | None, sky_payload: dict | None, key: str):
    """Propagate pipeline honesty flag when present; else unknown (F-SCI-04).

    Never hard-code False. Prefer sky_localisations.json / summary.sky_epistemic /
    summary top-level keys when Significance emits them; until then return "unknown".
    """
    for src in (sky_payload, summary, (summary or {}).get("sky_epistemic") if isinstance(summary, dict) else None):
        if isinstance(src, dict) and key in src:
            return src[key]
    return "unknown"


def run_process_observation(
    source: dict[str, Any],
    *,
    metadata_bytes: bytes | None = None,
) -> dict[str, Any]:
    """Invoke tip ``process_observation`` when the stored file is Pillow-decodable.

    Returns a consume record with present-only WCS/localisation/crossmatch payloads
    loaded from the written bundle (never invented).
    """
    if not source.get("processable_by_process_observation"):
        return {
            "invoked": False,
            "reason": (
                "file is accepted for preserve-source storage only; "
                "process_observation requires a Pillow-decodable image until a "
                "FITS/declared-WCS adapter lands (Significance-owned)"
            ),
            "wcs": None,
            "localisations": [],
            "crossmatches": [],
            "bundle_path": None,
            "summary": None,
            "observed_vs_expected": None,
        }
    from asa_astro.evidence.pipeline import process_observation

    stored = _data_dir() / source["stored_path"]
    if not stored.is_file():
        raise UploadError("stored upload missing")
    observation_bundles_dir().mkdir(parents=True, exist_ok=True)
    meta_path: Path | None = None
    if metadata_bytes:
        try:
            meta_obj = json.loads(metadata_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise UploadError("optional metadata must be UTF-8 JSON object") from exc
        if not isinstance(meta_obj, dict):
            raise UploadError("optional metadata must be a JSON object")
        meta_tmp = observation_bundles_dir() / f".meta-{source['sha256']}.json"
        meta_tmp.write_bytes(json.dumps(meta_obj, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        meta_path = meta_tmp

    # Bundle directory is content-addressed from source (+ metadata) so re-uploads reuse.
    meta_digest = _sha256(metadata_bytes) if metadata_bytes else "none"
    bundle_name = f"obs-{source['sha256'][:24]}-meta-{meta_digest[:16]}"
    bundle_dir = observation_bundles_dir() / bundle_name
    if bundle_dir.exists():
        # Reuse prior bundle; process_observation refuses existing output paths.
        summary = {
            "processing_run_id": "reused-existing-bundle",
            "output_directory": str(bundle_dir),
            "source_sha256": source["sha256"],
            "reused": True,
        }
    else:
        summary = process_observation(
            stored,
            bundle_dir,
            metadata_path=meta_path,
            source_locator=f"app-upload:{source['sha256']}",
        )
    wcs = None
    localisations: list[dict[str, Any]] = []
    crossmatches: list[dict[str, Any]] = []
    sky_payload: dict[str, Any] | None = None
    wcs_path = bundle_dir / "wcs_solution.json"
    sky_path = bundle_dir / "sky_localisations.json"
    xm_path = bundle_dir / "catalogue_crossmatches.json"
    if wcs_path.is_file():
        wcs = _load_json(wcs_path)
    if sky_path.is_file():
        sky_payload = _load_json(sky_path)
        localisations = list(sky_payload.get("localisations") or [])
    if xm_path.is_file():
        xm = _load_json(xm_path)
        crossmatches = list(xm.get("crossmatches") or [])
    # Confirm content-addressed source copy inside the bundle matches upload digest.
    source_dir = bundle_dir / "source"
    bundle_source_sha = None
    if source_dir.is_dir():
        for child in source_dir.iterdir():
            if child.is_file() and child.name.startswith(source["sha256"]):
                bundle_source_sha = _sha256(child.read_bytes())
                break
    # F-SCI-03: present-only observation_identity from pipeline (never invent digests).
    observation_identity = None
    for src in (summary if isinstance(summary, dict) else None, sky_payload, wcs if isinstance(wcs, dict) else None):
        if isinstance(src, dict) and isinstance(src.get("observation_identity"), dict):
            observation_identity = src["observation_identity"]
            break
    if observation_identity is None and isinstance(summary, dict):
        # Accept flat component digests on summary when Significance lands that shape.
        comps = {}
        for k in ("source_sha256", "metadata_sha256", "wcs_digest", "binding",
                  "observation_claim_digest", "observation_claim_id"):
            if k in summary:
                comps[k] = summary[k]
        if "source_sha256" in comps:
            claim = (
                comps.get("observation_claim_digest")
                or summary.get("observation_identity_digest")
                or summary.get("digest")
            )
            observation_identity = {
                "binding": comps.get("binding") or "content-addressed-observation-claim",
                "source_sha256": comps["source_sha256"],
                "metadata_sha256": comps.get("metadata_sha256"),
                "wcs_digest": comps.get("wcs_digest"),
            }
            if claim:
                observation_identity["observation_claim_digest"] = claim
                observation_identity["observation_claim_id"] = (
                    comps.get("observation_claim_id") or f"obsclaim-{claim}"
                )

    return {
        "invoked": True,
        "reason": None,
        "wcs": wcs,
        "localisations": localisations,
        "crossmatches": crossmatches,
        "observation_identity": observation_identity,
        "bundle_path": str(bundle_dir.relative_to(_data_dir())),
        "summary": summary,
        "bundle_source_sha256_verified": bundle_source_sha == source["sha256"],
        "sky_localisation_count": len(localisations),
        "wcs_present": wcs is not None,
        "catalogue_crossmatch_count": len(crossmatches),
        "coordinates_invented": _honesty_flag(summary if isinstance(summary, dict) else None, sky_payload, "coordinates_invented"),
        "source_image_mutated": _honesty_flag(summary if isinstance(summary, dict) else None, sky_payload, "source_image_mutated"),
        "objective_bridge": (
            "absent — observation graph is NOT mapped into the Objective universe "
            "(G-SIG-1; Significance-owned). Thin Objective path still uses the "
            "synthetic example universe."
        ),
        "metadata_path": str(meta_path.relative_to(_data_dir())) if meta_path and meta_path.exists() else None,
        "observed_vs_expected": _compute_residuals(bundle_dir, meta_path),
    }
