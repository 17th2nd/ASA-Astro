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

    def test_engine_never_imports_the_oracle(self):
        for path in list((ROOT / "src" / "astro" / "significance").rglob("*.py")) + list((ROOT / "src" / "astro" / "execution").rglob("*.py")) + [ROOT / "src" / "astro" / "session.py", ROOT / "src" / "astro" / "pipeline.py"]:
            tree = ast.parse(path.read_text())
            mods = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module} | {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            self.assertFalse(any("benchmark" in m for m in mods), path)


if __name__ == "__main__":
    unittest.main()
