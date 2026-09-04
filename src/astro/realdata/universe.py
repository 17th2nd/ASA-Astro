"""Frozen extract → Astro universe → ASA kernel, through the unchanged catalogue parsers and frontier derivation.

This module never reads the reference labels. It reads only the two ``input_*.csv`` files of the frozen extract.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from astro.asa.adapter import AstroAdapter
from astro.catalogues.fragments import merge_fragments
from astro.catalogues.parsers import gaia_host_map, parse_exoplanets, parse_gaia_hosts
from astro.domain import Entity, Universe
from astro.knowledge.frontier import Frontier, derive_frontier, load_frontier
from astro.pipeline import FACET
from . import EXP_ID
from .dataset import DATASET_DIR

INPUT_EXO = DATASET_DIR / "input_pscomppars_rows.csv"
INPUT_GAIA = DATASET_DIR / "input_gaia_rows.csv"


def build_base_universe(label: str = EXP_ID, hosts: Iterable[str] | None = None, exo_path: Path = INPUT_EXO, gaia_path: Path = INPUT_GAIA) -> Universe:
    """Parse the frozen extract exactly as the store does. ``hosts`` restricts to the named host designations (tests)."""
    exo = parse_exoplanets(exo_path)
    gaia = parse_gaia_hosts(gaia_host_map(exo), gaia_path)
    universe = merge_fragments(label, exo, gaia)
    if hosts is not None:
        keep = set()
        wanted = set(hosts)
        for e in universe.entities:
            if e.kind == "star" and e.designation in wanted:
                keep.add(e.entity_id)
                for r in universe.relationships_of(e.entity_id, "hosts"):
                    keep.update(r.participants())
        universe = Universe.create(label, universe.data_class, [e for e in universe.entities if e.entity_id in keep],
                                   [v for v in universe.evidence if v.subject_id in keep],
                                   [r for r in universe.relationships if all(p in keep for p in r.participants())], [])
    return universe


def with_frontier(universe: Universe, as_of: str) -> tuple[Universe, Frontier]:
    front = derive_frontier(universe, as_of, tiles=False)
    return front.apply(universe, label=universe.label), front


def build_universe(as_of: str, label: str = EXP_ID, hosts: Iterable[str] | None = None) -> tuple[Universe, Frontier]:
    return with_frontier(build_base_universe(label, hosts), as_of)


def load_kernel(universe: Universe, frontier: Frontier | None, slug: str = "realdata") -> AstroAdapter:
    adapter = AstroAdapter.in_memory(FACET, slug)
    if frontier is not None:
        load_frontier(adapter, universe, frontier)
    else:
        adapter.load_universe(universe)
    return adapter


def host_of_planet(universe: Universe, planet_designation: str) -> Entity:
    planet = universe.find(planet_designation)
    for r in universe.relationships_of(planet.entity_id, "hosts"):
        if planet.entity_id in r.role_map.get("companion", ()):
            return universe.entity(r.role_map["host"][0])
    raise KeyError(f"no host for {planet_designation}")
