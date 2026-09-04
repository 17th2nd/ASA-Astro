"""Declared baselines. Each returns {host_entity_id: score or None}; higher is "more relevant"; None is unranked.

None of these reads the reference labels or the engine's significance output. The graph baselines read the
same ASA snapshot the engine reads and nothing else.
"""

from __future__ import annotations

import math
import random
from datetime import datetime, timezone
from typing import Iterable

from astro.asa.adapter import RelationalSnapshot
from astro.domain import Universe


def brightness(universe: Universe, hosts: Iterable[str]) -> dict[str, float | None]:
    out = {}
    for h in hosts:
        m = universe.entity(h).attribute_map.get("magnitude_v")
        out[h] = -float(m) if m is not None else None
    return out


def sigma_period(universe: Universe, hosts: Iterable[str]) -> dict[str, float | None]:
    out = {}
    for h in hosts:
        best = None
        for rec in universe.evidence_for(h, "ephemeris"):
            if rec.status != "admissible":
                continue
            s = rec.uncertainty_map.get("period_days")
            if s is not None:
                best = max(best or 0.0, float(s))
        out[h] = best
    return out


def degree(snapshot: RelationalSnapshot, hosts: Iterable[str]) -> dict[str, float | None]:
    return {h: float(len([e for e in snapshot.edges_of(h) if e.lifecycle == "registered"]) + len(snapshot.evidence_of(h))) for h in hosts}


def relational_graph(snapshot: RelationalSnapshot) -> dict[str, set[str]]:
    """Undirected ASA relational graph: entities, evidence records and UROs as nodes."""
    adj: dict[str, set[str]] = {}

    def link(a: str, b: str) -> None:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    for e in snapshot.edges:
        if e.lifecycle != "registered":
            continue
        for p in e.participants():          # entity–URO bindings (contradicts binds two claim UROs)
            link(p, e.key)
        for ev in e.supported_by:           # evidence–URO supports
            link(ev, e.key)
    for l in snapshot.evidence_links:       # evidence–subject links (via the evidence-of URO)
        link(l.evidence_id, l.key)
        link(l.key, l.subject_id)
    return adj


def pagerank(snapshot: RelationalSnapshot, hosts: Iterable[str], damping: float = 0.85, iterations: int = 200) -> dict[str, float | None]:
    adj = relational_graph(snapshot)
    nodes = sorted(adj)
    n = len(nodes)
    if n == 0:
        return {h: None for h in hosts}
    pr = {v: 1.0 / n for v in nodes}
    for _ in range(iterations):
        new = {}
        for v in nodes:
            s = 0.0
            for u in adj[v]:
                s += pr[u] / len(adj[u])
            new[v] = (1.0 - damping) / n + damping * s
        delta = sum(abs(new[v] - pr[v]) for v in nodes)
        pr = new
        if delta < 1e-14:
            break
    return {h: pr.get(h) for h in hosts}


def random_baseline(hosts: Iterable[str], seed: int) -> dict[str, float | None]:
    ids = sorted(hosts)
    rng = random.Random(seed)
    order = list(ids)
    rng.shuffle(order)
    return {h: float(len(order) - i) for i, h in enumerate(order)}


def projected_uncertainty_formula(rows_by_host: dict[str, dict], hosts: Iterable[str], as_of: str) -> dict[str, float | None]:
    """DIAGNOSTIC: sqrt(sigma_T0^2 + (n sigma_P)^2) * 24 / duration_hours at ``as_of``, straight from the archive row."""
    t = datetime.fromisoformat(as_of.replace("Z", "+00:00")).astimezone(timezone.utc)
    jd_now = 2440587.5 + t.timestamp() / 86400.0
    out = {}
    for h in hosts:
        row = rows_by_host.get(h)
        if row is None:
            out[h] = None
            continue
        try:
            period, sig_p, tmid, sig_t0 = float(row["pl_orbper"]), float(row["pl_orbpererr1"]), float(row["pl_tranmid"]), float(row["pl_tranmiderr1"])
        except (KeyError, ValueError, TypeError):
            out[h] = None
            continue
        dur = float(row["pl_trandur"]) if row.get("pl_trandur") not in (None, "") else 2.0
        n = abs((jd_now - tmid) / period)
        out[h] = math.sqrt(sig_t0 ** 2 + (n * sig_p) ** 2) * 24.0 / (dur or 2.0)
    return out
