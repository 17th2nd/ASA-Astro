"""Pluggable local Astrometry.net ``solve-field`` adapter (optional; fail closed).

Never invents coordinates. If ``solve-field`` is absent or the solve fails, raises
``SolveFieldUnavailable`` — callers must not substitute a fake WCS.
Source image/FITS bytes are copied to a scratch dir; the original path is never written.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .fits_io import FitsWcsUnavailable, extract_wcs_from_fits_header, source_sha256


class SolveFieldUnavailable(FitsWcsUnavailable):
    """solve-field binary missing, disabled, or failed — coordinates not invented."""


def solve_field_executable() -> str | None:
    """Return path to ``solve-field`` when present and executable; else None."""

    override = os.environ.get("ASA_ASTRO_SOLVE_FIELD")
    if override:
        path = Path(override)
        return str(path) if path.is_file() and os.access(path, os.X_OK) else None
    found = shutil.which("solve-field")
    return found


def solve_field_available() -> bool:
    return solve_field_executable() is not None


def run_solve_field(
    image_path: str | Path,
    *,
    out_directory: str | Path | None = None,
    timeout_s: float = 120.0,
    extra_args: list[str] | None = None,
) -> dict[str, Any]:
    """Run local ``solve-field`` on a copy of the image; return extracted WCS or fail closed.

    The source file is never modified. Output WCS FITS (``.new`` / ``.wcs``) is read via
    ``extract_wcs_from_fits_header``. Requires ``solve-field`` on PATH (or
    ``ASA_ASTRO_SOLVE_FIELD``).
    """

    exe = solve_field_executable()
    if exe is None:
        raise SolveFieldUnavailable(
            "Fail closed: solve-field not available on PATH "
            "(set ASA_ASTRO_SOLVE_FIELD to an executable to enable); "
            "coordinates were not invented."
        )

    src = Path(image_path)
    if not src.is_file():
        raise SolveFieldUnavailable(f"solve-field input does not exist: {src}")

    before = source_sha256(src)
    scratch_owned = out_directory is None
    out = Path(out_directory) if out_directory else Path(
        tempfile.mkdtemp(prefix="asa-solve-field-", dir="/tmp")
    )
    out.mkdir(parents=True, exist_ok=True)

    # Work on a scratch copy so the original cannot be overwritten by solve-field --overwrite.
    work_copy = out / f"input{src.suffix.lower() or '.fits'}"
    shutil.copy2(src, work_copy)
    if source_sha256(work_copy) != before:
        raise SolveFieldUnavailable("scratch copy integrity check failed")

    cmd = [
        exe,
        "--no-plots",
        "--new-fits",
        str(out / "solved.new"),
        "--wcs",
        str(out / "solved.wcs"),
        "--overwrite",
        str(work_copy),
    ]
    if extra_args:
        cmd[1:1] = list(extra_args)

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SolveFieldUnavailable(
            f"Fail closed: solve-field timed out after {timeout_s}s; coordinates were not invented."
        ) from exc
    finally:
        after = source_sha256(src)
        if after != before:
            raise SolveFieldUnavailable(
                "Source image bytes changed during solve-field; refusing result "
                "(coordinates were not invented)."
            )

    wcs_path = out / "solved.wcs"
    new_path = out / "solved.new"
    header_source = wcs_path if wcs_path.is_file() else new_path
    if completed.returncode != 0 or not header_source.is_file():
        raise SolveFieldUnavailable(
            "Fail closed: solve-field did not produce a WCS solution "
            f"(exit={completed.returncode}); coordinates were not invented. "
            f"stderr={completed.stderr[-500:]!r}"
        )

    from astropy.io import fits

    with fits.open(header_source, mode="readonly", memmap=False) as hdul:
        header = hdul[0].header
        wcs_record = extract_wcs_from_fits_header(
            header,
            source_reference=f"solve-field:{src.name}",
        )

    wcs_record = dict(wcs_record)
    wcs_record["notes"] = list(wcs_record.get("notes") or []) + [
        "Astrometric solution from local Astrometry.net solve-field adapter.",
        "Solution remains a hypothesis until independently validated.",
    ]
    wcs_record["solve_field"] = {
        "executable": exe,
        "returncode": completed.returncode,
        "work_directory": str(out),
        "wcs_artifact": str(header_source.name),
    }

    result = {
        "schema": "asa-astro-solve-field-result-v1",
        "status": "solved",
        "source_sha256": before,
        "source_image_mutated": False,
        "coordinates_invented": False,
        "wcs_solution": wcs_record,
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
    }
    (out / "solve_field_result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if scratch_owned:
        result["scratch_directory"] = str(out)
    return result


__all__ = [
    "SolveFieldUnavailable",
    "solve_field_available",
    "solve_field_executable",
    "run_solve_field",
]
