"""ASTRO-REAL-DATA-EXP-0001 command line.

    PYTHONPATH=src python3 tools/realdata_exp0001.py fetch        # retrieve ExoClock + archive reference links; write PROVENANCE.json
    PYTHONPATH=src python3 tools/realdata_exp0001.py select       # apply the declared candidate rules; write the frozen extract
    PYTHONPATH=src python3 tools/realdata_exp0001.py manifest     # freeze the pre-registration manifest (before any run)
    PYTHONPATH=src python3 tools/realdata_exp0001.py run          # the single pre-registered run + baselines + metrics
    PYTHONPATH=src python3 tools/realdata_exp0001.py adversarial  # bounded adversarial and ablation checks
    PYTHONPATH=src python3 tools/realdata_exp0001.py verify       # re-check dataset digests and manifest digest
"""

from __future__ import annotations

import json
import sys


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "fetch":
        from astro.realdata.dataset import fetch
        prov = fetch()
        print(json.dumps({k: {"sha256": v.get("sha256") or [f["sha256"] for f in v.get("files", [])], "retrieved_at": v.get("retrieved_at")} for k, v in prov["sources"].items()}, indent=1))
        return 0
    if cmd == "select":
        from astro.realdata.dataset import select
        sel = select()
        print(json.dumps(sel["counts"], indent=1))
        return 0
    if cmd == "verify":
        from astro.realdata.dataset import verify_dataset
        out = verify_dataset()
        print(json.dumps(out, indent=1))
        return 0 if all(v["ok"] for v in out.values()) else 1
    if cmd == "manifest":
        from astro.realdata.manifest import freeze_manifest
        print(json.dumps(freeze_manifest(), indent=1))
        return 0
    if cmd == "run":
        from astro.realdata.experiment import run_experiment
        print(json.dumps(run_experiment(), indent=1))
        return 0
    if cmd == "adversarial":
        from astro.realdata.adversarial import run_adversarial
        print(json.dumps(run_adversarial(), indent=1))
        return 0
    print(f"unknown command {cmd!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
