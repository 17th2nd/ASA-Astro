#!/usr/bin/env python3
"""Report observation-bundle readiness for Objective binding. Read-only; no silent fills."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("bundle", type=Path, help="asa_astro observe output directory")
    args = p.parse_args(argv)
    root: Path = args.bundle
    required = ["graph.json", "provenance.json", "manifest.json", "summary.md"]
    missing = [n for n in required if not (root / n).exists()]
    if missing:
        print(json.dumps({"status": "failed", "error": f"missing {missing}"}, sort_keys=True))
        return 1
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    graph = json.loads((root / "graph.json").read_text(encoding="utf-8"))
    source_dir = root / "source"
    sources = sorted(source_dir.glob("*")) if source_dir.exists() else []
    source_digests = {s.name: sha256(s) for s in sources if s.is_file()}
    nodes = graph.get("nodes") or graph.get("candidates") or []
    edges = graph.get("edges") or graph.get("assertions") or []
    # Never claim Objective-ready: image-space only until WCS/crossmatch exist.
    report = {
        "status": "observation_ready_objective_not_bound",
        "bundle": str(root),
        "processing_run_id": manifest.get("processing_run_id") or manifest.get("run_id"),
        "source_files": list(source_digests),
        "source_sha256": source_digests,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "epistemic": {
            "candidates_are": "hypothesis",
            "physical_claim_allowed": False,
            "silent_fill_of_missing_wcs_or_identity": False,
            "objective_binding": "blocked_until_wcs_and_crossmatch",
        },
        "blockers": [
            "no_wcs_astrometric_localisation",
            "no_catalogue_crossmatch_from_detections",
            "no_observed_vs_expected_residual_path",
        ],
        "next": "docs/pipeline/OPERATOR-C-OBSERVATION-TO-OBJECTIVE-STATUS-0001.md",
    }
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
