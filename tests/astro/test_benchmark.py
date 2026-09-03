"""Benchmark harness (§18): honest comparison on the slice-1 synthetic universe."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from astro.benchmark import STRATEGIES, run_benchmark
from astro.domain import Universe
from astro.objectives.loaders import load_context, load_objective

ROOT = Path(__file__).resolve().parents[2]


def setup(name):
    u = Universe.load(ROOT / "data" / "universe" / "slice1.json")
    return u, load_objective(ROOT / "data" / "objectives" / name), load_context(ROOT / "data" / "contexts" / "night-2026-09-03.json", u)


class TestBenchmark(unittest.TestCase):
    def test_strategies_are_reproducible_and_scored(self):
        u, o, ctx = setup("C-stellar-variability.json")
        b = run_benchmark(u, o, ctx)
        self.assertEqual({r.strategy for r in b.results}, set(STRATEGIES))
        self.assertTrue(all(r.reproducible for r in b.results))
        by = {r.strategy: r for r in b.results}
        self.assertEqual(by["asa"].useful_actions, by["oracle"].useful_actions)          # slice-1 fact, not a general claim
        self.assertEqual(by["asa"].wasted_minutes, 0)
        self.assertGreater(by["fifo"].wasted_minutes, by["asa"].wasted_minutes)
        self.assertEqual(run_benchmark(u, o, ctx).benchmark_id, b.benchmark_id)

    def test_single_candidate_objective_has_no_discriminating_power(self):
        """Negative finding recorded as a test: with one eligible transient every strategy ties."""
        u, o, ctx = setup("B-transient-followup.json")
        b = run_benchmark(u, o, ctx)
        self.assertEqual({(r.useful_actions, r.wasted_minutes) for r in b.results}, {(1, 0)})

    def test_frontier_objectives_have_oracles_and_the_session_registers_disputes(self):
        """Objectives E and F on slice-1 plus four synthetic stars: one with gaps, one complete, one with a
        Teff dispute, one whose catalogues agree. Facts recorded, not general claims."""
        from astro.domain import Coordinates, Entity, EvidenceRecord, Provenance, RelationshipAssertion
        from astro.knowledge import derive_frontier
        syn = Provenance("astro-test-fixture", "synthetic", "tests/astro/test_benchmark.py")
        src = lambda ref: Provenance("astro-test-fixture", "synthetic", ref)
        u0 = Universe.load(ROOT / "data" / "universe" / "slice1.json")
        ents, evs, rels = list(u0.entities), list(u0.evidence), list(u0.relationships)
        gap = Entity.create("star", "SYN-GAP-X", catalogue_ids={"T": "gx"}, coordinates=Coordinates(331.0, -21.0), source=syn, attributes={"magnitude_v": 11.0})
        gap_pl = Entity.create("exoplanet", "SYN-GAP-X b", catalogue_ids={"T": "gxb"}, source=syn)
        gap_eph = EvidenceRecord.create("ephemeris", gap.entity_id, values={"period_days": 3.1, "epoch_utc": "2020-01-01T00:00:00Z", "duration_hours": 2.0, "planet": "SYN-GAP-X b"},
                                        uncertainty={"period_days": 0.0001, "epoch_days": 0.001}, source=src("catA:gx"))
        full = Entity.create("star", "SYN-FULL-Y", catalogue_ids={"T": "fy"}, coordinates=Coordinates(331.5, -21.5), source=syn, attributes={"magnitude_v": 11.0})
        full_pl = Entity.create("exoplanet", "SYN-FULL-Y b", catalogue_ids={"T": "fyb"}, source=syn)
        full_eph = EvidenceRecord.create("ephemeris", full.entity_id, values={"period_days": 2.2, "epoch_utc": "2026-08-01T00:00:00Z", "duration_hours": 2.0, "planet": "SYN-FULL-Y b"},
                                         uncertainty={"period_days": 0.00001, "epoch_days": 0.0001}, source=src("catA:fy"))
        full_ev = [full_eph] + [EvidenceRecord.create(k, full.entity_id, observed_at="2026-08-01T00:00:00Z", values=v, source=src("catA:fy")) for k, v in
                                (("photometry", {"mag_v": 11.0}), ("time_series", {"span_days": 30.0}), ("spectrum", {"teff_k": 5800.0}),
                                 ("astrometry", {"parallax_mas": 5.0, "pmra_mas_yr": 1.0, "pmdec_mas_yr": 1.0, "ruwe": 1.0}), ("catalogue_measurement", {"teff_k": 5800.0}))]
        disp = Entity.create("star", "SYN-DISP-Z", catalogue_ids={"T": "dz"}, coordinates=Coordinates(329.0, -19.0), source=syn, attributes={"magnitude_v": 10.5})
        disp_ev = [EvidenceRecord.create("catalogue_measurement", disp.entity_id, values={"teff_k": 6000.0}, source=src("catA:dz")),
                   EvidenceRecord.create("catalogue_measurement", disp.entity_id, values={"teff_k": 5000.0}, source=src("catB:dz"))]
        agree = Entity.create("star", "SYN-AGREE-W", catalogue_ids={"T": "aw"}, coordinates=Coordinates(329.5, -19.5), source=syn, attributes={"magnitude_v": 10.5})
        agree_ev = [EvidenceRecord.create("catalogue_measurement", agree.entity_id, values={"teff_k": 6000.0}, source=src("catA:aw")),
                    EvidenceRecord.create("catalogue_measurement", agree.entity_id, values={"teff_k": 6050.0}, source=src("catB:aw"))]
        ents += [gap, gap_pl, full, full_pl, disp, agree]
        evs += [gap_eph] + full_ev + disp_ev + agree_ev
        rels += [RelationshipAssertion.create("hosts", {"host": gap.entity_id, "companion": gap_pl.entity_id}, evidence_ids=[gap_eph.evidence_id], source=syn),
                 RelationshipAssertion.create("hosts", {"host": full.entity_id, "companion": full_pl.entity_id}, evidence_ids=[full_eph.evidence_id], source=syn)]
        u = Universe.create("slice1+frontier", "synthetic", ents, evs, rels, u0.states)
        f = derive_frontier(u, "2026-09-03T08:00:00Z", tiles=False)
        u = f.apply(u)
        self.assertEqual(f.counts["claims"]["contradictions"], 1)
        ctx = load_context(ROOT / "data" / "contexts" / "night-2026-09-03.json", u)
        e = {r.strategy: r for r in run_benchmark(u, load_objective(ROOT / "data" / "objectives" / "E-knowledge-gap-reduction.json"), ctx).results}
        self.assertTrue(all(r.reproducible for r in e.values()))
        self.assertEqual(e["asa"].wasted_minutes, 0)
        self.assertEqual([x["designation"] for x in e["asa"].executed], ["SYN-GAP-X"])
        self.assertEqual(e["oracle"].useful_actions, 5)                       # recall gap on record: E's min_score leaves four useful targets unplanned
        self.assertGreater(e["fifo"].wasted_minutes, 0)
        fr = {r.strategy: r for r in run_benchmark(u, load_objective(ROOT / "data" / "objectives" / "F-dispute-adjudication.json"), ctx).results}
        self.assertEqual([x["designation"] for x in fr["asa"].executed], ["SYN-DISP-Z"])   # the dispute is registered by the session's own load path
        self.assertEqual((fr["asa"].useful_actions, fr["asa"].wasted_minutes), (fr["oracle"].useful_actions, 0))
        self.assertTrue(all(x["designation"] != "SYN-AGREE-W" or not x["useful"] for r in fr.values() for x in r.executed))

    def test_engine_never_imports_the_oracle(self):
        for path in list((ROOT / "src" / "astro" / "significance").rglob("*.py")) + list((ROOT / "src" / "astro" / "execution").rglob("*.py")) + [ROOT / "src" / "astro" / "session.py", ROOT / "src" / "astro" / "pipeline.py"]:
            tree = ast.parse(path.read_text())
            mods = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module} | {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            self.assertFalse(any("benchmark" in m for m in mods), path)


if __name__ == "__main__":
    unittest.main()
