"""ASTRO-REAL-DATA-EXP-0001 apparatus tests: frozen dataset integrity, metrics, baselines, separation, determinism."""

from __future__ import annotations

import ast
import json
import tempfile
import unittest
from pathlib import Path

from astro.pipeline import ROOT, decide
from astro.realdata import HASH_SALT
from astro.realdata.baselines import degree, pagerank, relational_graph
from astro.realdata.dataset import DATASET_DIR, GRADE, PRIMARY_SAMPLE_SIZE, hash_order, load_reference, load_selection, normalise_name, verify_dataset
from astro.realdata.manifest import OBJECTIVE_PATH, declare_context, load_manifest, verify_manifest
from astro.realdata.metrics import average_ranks, ndcg_at_k, ordering, precision_at_k, spearman
from astro.realdata.universe import build_universe, host_of_planet, load_kernel
from astro.objectives.loaders import load_objective


class DatasetTests(unittest.TestCase):
    def test_frozen_extract_digests_verify(self):
        self.assertTrue(all(v["ok"] for v in verify_dataset().values()))

    def test_manifest_digest_verifies_and_matches_declarations(self):
        self.assertTrue(verify_manifest()["ok"])
        m = load_manifest()
        self.assertEqual(load_objective(OBJECTIVE_PATH).objective_id, m["objective"]["objective_id"])
        self.assertEqual(declare_context().context_id, m["context"]["context_id"])

    def test_primary_sample_is_the_hash_prefix_of_the_pool(self):
        sel = load_selection()
        self.assertEqual(len(sel["primary"]), PRIMARY_SAMPLE_SIZE)
        self.assertEqual(sel["primary"], sel["pool_ordered"][:PRIMARY_SAMPLE_SIZE])
        self.assertEqual(sel["pool_ordered"], sorted(sel["pool_ordered"], key=lambda n: (hash_order(n), n)))
        self.assertEqual(sel["hash_salt"], HASH_SALT)

    def test_every_primary_candidate_has_a_label_and_no_leakage_flag(self):
        sel, ref = load_selection(), load_reference()
        flagged = {x["name"] for x in sel["leakage_flagged"]}
        for p in sel["primary"]:
            self.assertIn(ref[p]["priority"], GRADE)
            self.assertNotIn(p, flagged)
            self.assertNotIn(p, sel["missing_uncertainty"])

    def test_name_normalisation(self):
        self.assertEqual(normalise_name("55 Cnc e"), normalise_name("55Cnce"))
        self.assertEqual(normalise_name("HAT-P-1 b"), normalise_name("HAT-P-1b"))
        self.assertNotEqual(normalise_name("HAT-P-1 b"), normalise_name("HAT-P-11 b"))


class MetricsTests(unittest.TestCase):
    def test_spearman_perfect_inverse_and_none(self):
        self.assertAlmostEqual(spearman([1, 2, 3, 4], [0, 1, 2, 3]), 1.0)
        self.assertAlmostEqual(spearman([4, 3, 2, 1], [0, 1, 2, 3]), -1.0)
        self.assertIsNone(spearman([1, 1, 1], [0, 1, 2]))
        self.assertEqual(average_ranks([None, 5.0, None, 7.0]), [3.5, 2.0, 3.5, 1.0])

    def test_ndcg_and_precision(self):
        grade = {"a": 3.0, "b": 2.0, "c": 0.0, "d": 1.0}
        self.assertAlmostEqual(ndcg_at_k(["a", "b", "d", "c"], grade, 4), 1.0)
        self.assertLess(ndcg_at_k(["c", "d", "b", "a"], grade, 4), 0.7)
        self.assertEqual(precision_at_k(["a", "b", "c", "d"], grade, 2), 1.0)
        self.assertEqual(ordering(["x", "y", "z"], [None, 2.0, 2.0]), ["y", "z", "x"])


class ApparatusTests(unittest.TestCase):
    HOSTS = None

    @classmethod
    def setUpClass(cls):
        sel = load_selection()
        from astro.realdata.universe import build_base_universe
        base = build_base_universe()
        cls.HOSTS = [host_of_planet(base, p).designation for p in sel["primary"][:6]]
        cls.context = declare_context()
        cls.objective = load_objective(OBJECTIVE_PATH)
        cls.universe, cls.frontier = build_universe(cls.context.as_of, hosts=cls.HOSTS)
        cls.adapter = load_kernel(cls.universe, cls.frontier, "test")
        cls.decision = decide(cls.universe, cls.objective, cls.context, cls.adapter, issued_at=cls.context.as_of)

    def test_universe_is_real_and_candidates_carry_uncertainties(self):
        self.assertEqual(self.universe.data_class, "real")
        for h in self.HOSTS:
            e = self.universe.find(h)
            eph = [x for x in self.universe.evidence_for(e.entity_id, "ephemeris") if x.status == "admissible"]
            self.assertEqual(len(eph), 1)
            self.assertIn("period_days", eph[0].uncertainty_map)
            self.assertIn("epoch_days", eph[0].uncertainty_map)
            self.assertEqual(self.decision.evaluation.result_for(e.entity_id).status, "eligible")

    def test_graph_baselines_read_only_the_snapshot(self):
        ids = [self.universe.find(h).entity_id for h in self.HOSTS]
        deg, pr = degree(self.decision.snapshot, ids), pagerank(self.decision.snapshot, ids)
        self.assertTrue(all(deg[i] > 0 for i in ids))
        self.assertTrue(all(pr[i] is not None and pr[i] > 0 for i in ids))
        adj = relational_graph(self.decision.snapshot)
        total = sum(pagerank(self.decision.snapshot, list(adj)).values())
        self.assertAlmostEqual(total, 1.0, places=6)

    def test_evaluation_is_deterministic(self):
        universe, frontier = build_universe(self.context.as_of, hosts=self.HOSTS)
        adapter = load_kernel(universe, frontier, "test")
        again = decide(universe, self.objective, self.context, adapter, issued_at=self.context.as_of)
        self.assertEqual(again.evaluation.evaluation_id, self.decision.evaluation.evaluation_id)
        self.assertEqual(again.snapshot.digest, self.decision.snapshot.digest)

    def test_runner_writes_the_declared_outputs(self):
        from astro.realdata.experiment import run_experiment
        with tempfile.TemporaryDirectory() as tmp:
            run_experiment(Path(tmp), hosts=self.HOSTS)
            names = {p.name for p in Path(tmp).iterdir()}
            self.assertTrue({"results.json", "candidates_scored.csv", "candidates_scored.json", "explanations.json", "COMPARISON.md", "primary-run"} <= names)
            res = json.loads((Path(tmp) / "results.json").read_text())
            self.assertEqual(res["preconditions"]["ok"], True)
            self.assertIn("astro", res["metrics"]["primary"]["methods"])
            self.assertTrue((Path(tmp) / "primary-run" / "receipt.sha256").exists())


class SeparationTests(unittest.TestCase):
    def test_engine_facing_modules_never_read_reference_labels(self):
        """The universe adapter and the baselines must not touch the reference file or its loader."""
        for name in ("universe.py", "baselines.py"):
            src = (ROOT / "src" / "astro" / "realdata" / name).read_text(encoding="utf-8")
            tree = ast.parse(src)
            names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
            self.assertNotIn("load_reference", names, name)
            self.assertNotIn("reference_exoclock_priority", src, name)
            self.assertNotIn("priority", src, name)

    def test_engine_packages_do_not_import_the_experiment(self):
        for pkg in ("significance", "asa", "knowledge", "catalogues", "objectives", "domain", "execution"):
            for path in (ROOT / "src" / "astro" / pkg).rglob("*.py"):
                self.assertNotIn("realdata", path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
