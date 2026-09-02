"""Persistent Astro store: real catalogues → merged universe → ASA kernel on disk, with a build receipt."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from astro import ASTRO_VERSION
from astro.asa.adapter import AstroAdapter, FileStorage
from astro.asa.locator import asa_baseline_sha
from astro.catalogues import merge_fragments
from astro.catalogues.manifest import load_manifest, verify_snapshots
from astro.catalogues.parsers import PARSERS, gaia_host_map, parse_gaia_hosts
from astro.domain import Universe
from astro.pipeline import FACET

DEFAULT_SOURCES = ("exoplanets", "gaia_hosts", "gcvs", "openngc", "huntreffert_clusters", "mpc_sites", "alerce_sn")


def build_universe(sources: tuple[str, ...] = DEFAULT_SOURCES, label: str = "astro-real") -> tuple[Universe, list[dict[str, Any]]]:
    """Parse the requested raw snapshots and merge them into one labelled ``real`` universe."""
    frags, summaries = [], []
    exo = None
    for key in sources:
        if key == "gaia_hosts":
            if exo is None:
                exo = PARSERS["exoplanets"]()
            frag = parse_gaia_hosts(gaia_host_map(exo))
        elif key == "exoplanets":
            exo = exo or PARSERS["exoplanets"]()
            frag = exo
        else:
            frag = PARSERS[key]()
        frags.append(frag)
        summaries.append(frag.summary())
    if "gaia_hosts" in sources and "exoplanets" not in sources:
        frags.insert(0, exo)
        summaries.insert(0, exo.summary())
    return merge_fragments(label, *frags), summaries


def build_store(store_dir: str | Path, sources: tuple[str, ...] = DEFAULT_SOURCES, universe_path: str | Path | None = None) -> dict[str, Any]:
    """Build (or extend) the persistent kernel store from the raw snapshots and write BUILD.json."""
    store_dir = Path(store_dir)
    snapshots = verify_snapshots()
    missing = [k for k in sources if not snapshots.get(k)]
    if missing:
        raise RuntimeError(f"raw snapshots missing or drifted for {missing}; run `astro catalogues fetch` first")
    t0 = time.time()
    universe, summaries = build_universe(sources)
    t_parse = time.time() - t0
    if universe_path:
        universe.save(universe_path)
    t1 = time.time()
    if store_dir.exists() and any(store_dir.iterdir()):
        adapter = AstroAdapter.open(FileStorage(store_dir))
    else:
        store_dir.mkdir(parents=True, exist_ok=True)
        adapter = AstroAdapter.bootstrap(FileStorage(store_dir), FACET, "real")
    counts = adapter.load_universe(universe)
    t_load = time.time() - t1
    head = adapter.k.head()
    manifest = load_manifest()
    receipt = {
        "build_schema": "astro-store-build-v1",
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "astro_version": ASTRO_VERSION, "asa_baseline": asa_baseline_sha(),
        "universe_id": universe.universe_id, "universe_label": universe.label, "universe_data_class": universe.data_class,
        "universe_path": str(universe_path) if universe_path else None,
        "entities": len(universe.entities), "evidence": len(universe.evidence), "relationships": len(universe.relationships),
        "kinds": _count(e.kind for e in universe.entities), "evidence_kinds": _count(e.kind for e in universe.evidence),
        "sources": summaries, "snapshot_digests": {k: [f["sha256"] for f in manifest.entries[k]["files"]] for k in sources},
        "licences": {k: manifest.entries[k]["licence"] for k in sources},
        "loaded_this_build": counts, "kernel_seq": head["seq"], "kernel_head": head["head"], "kernel_digest": adapter.digest(),
        "timing_s": {"parse_and_merge": round(t_parse, 1), "kernel_load": round(t_load, 1)},
    }
    (store_dir / "BUILD.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def _count(items) -> dict[str, int]:
    out: dict[str, int] = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return dict(sorted(out.items()))


def store_status(store_dir: str | Path, verify: bool = False) -> dict[str, Any]:
    store_dir = Path(store_dir)
    adapter = AstroAdapter.open(FileStorage(store_dir))
    build = json.loads((store_dir / "BUILD.json").read_text()) if (store_dir / "BUILD.json").exists() else {}
    out = {"store": str(store_dir), "kernel_head": adapter.k.head(), "kernel_digest": adapter.digest(), "build": build,
           "uaos": len(adapter.k.state.uaos), "uros": len(adapter.k.state.uros)}
    if verify:
        out["verify"] = adapter.verify()
        out["replay_digest_equal"] = adapter.replay_digest() == adapter.digest()
    return out
