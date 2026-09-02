"""CLAUDE-ASTRO-BUILD-001 §8 demonstrations and §17 architectural-drift tests."""

from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from astro.asa.adapter import AstroAdapter
from astro.data.slice1 import build as build_slice1
from astro.domain import EvidenceRecord, Provenance, RelationshipAssertion, Universe
from astro.domain.identity import _FORBIDDEN_STEMS
from astro.objectives.loaders import load_context, load_objective
from astro.pipeline import decide, open_or_bootstrap
from astro.significance import evaluate
from tests.astro.fixtures import FACET

ROOT = Path(__file__).resolve().parents[2]
OBJ = {k: ROOT / "data" / "objectives" / f for k, f in
       {"A": "A-exoplanet-transit-followup.json", "B": "B-transient-followup.json", "C": "C-stellar-variability.json", "D": "D-calibration.json"}.items()}
CTX = ROOT / "data" / "contexts" / "night-2026-09-03.json"
SYN = Provenance("astro-test-fixture", "synthetic", "tests/astro/test_significance.py")
FIXED = dict(commit="0" * 40, issued_at="2026-09-03T08:00:00Z")


def setup():
    u = Universe.load(ROOT / "data" / "universe" / "slice1.json")
    objectives = {k: load_objective(p) for k, p in OBJ.items()}
    ctx = load_context(CTX, u)
    adapter = open_or_bootstrap(u)
    return u, objectives, ctx, adapter


class TestContextSwitchDemonstration(unittest.TestCase):
    """§8 first demonstration: fixed universe, objective A then B; ranking changes, universe does not."""

    def test_same_universe_different_objective_different_ranking(self):
        u, obj, ctx, adapter = setup()
        before_universe, before_kernel = u.to_record(), adapter.digest()
        a = decide(u, obj["A"], ctx, adapter, **FIXED)
        b = decide(u, obj["B"], ctx, adapter, **FIXED)
        self.assertNotEqual(a.evaluation.ranking(), b.evaluation.ranking())
        self.assertEqual(u.find(a.evaluation.ranking()[0]).designation if False else a.evaluation.ranked()[0].designation, "SYN-HOST-A")
        self.assertEqual(b.evaluation.ranked()[0].designation, "SYN-TR-2026a")
        self.assertNotEqual(a.plan.selected_ids(), b.plan.selected_ids())
        # the universe and the ASA relational state are untouched by evaluation
        self.assertEqual(u.to_record(), before_universe)
        self.assertEqual(adapter.digest(), before_kernel)
        self.assertEqual(a.snapshot, b.snapshot)
        self.assertEqual(a.evaluation.universe_id, b.evaluation.universe_id)
        self.assertEqual(a.evaluation.kernel_digest, b.evaluation.kernel_digest)

    def test_all_four_objectives_select_different_work(self):
        u, obj, ctx, adapter = setup()
        tops = {k: decide(u, o, ctx, adapter, **FIXED).evaluation.ranked()[0].designation for k, o in obj.items()}
        self.assertEqual(tops, {"A": "SYN-HOST-A", "B": "SYN-TR-2026a", "C": "SYN-VAR-D", "D": "SYN-STD-C"})

    def test_context_alone_changes_significance(self):
        u, obj, ctx, adapter = setup()
        base = decide(u, obj["D"], ctx, adapter, **FIXED)
        other_anchor = ctx.with_changes(anchor_targets=[u.find("SYN-HOST-B").entity_id])
        moved = decide(u, obj["D"], other_anchor, adapter, **FIXED)
        self.assertEqual(base.evaluation.ranked()[0].designation, "SYN-STD-C")
        self.assertNotEqual(moved.evaluation.ranked()[0].designation, "SYN-STD-C")      # STD-C calibrates HOST-A, not HOST-B
        no_site = ctx.with_changes(site_id=None)
        blind = decide(u, obj["A"], no_site, adapter, **FIXED)
        self.assertEqual({r.status for r in blind.evaluation.results if r.kind == "star" and r.evidence_ids}, {"indeterminate", "ineligible"})
        self.assertTrue(all(r.status != "eligible" for r in blind.evaluation.results))    # visibility is required and unavailable


class TestEvidenceArrivalDemonstration(unittest.TestCase):
    """§8 second demonstration: objective constant, new evidence arrives, priority changes."""

    def new_evidence(self, u: Universe):
        host_a, host_b = u.find("SYN-HOST-A"), u.find("SYN-HOST-B")
        fresh_phot_a = EvidenceRecord.create("photometry", host_a.entity_id, values={"mag_v": 10.41}, uncertainty={"mag_v": 0.01},
                                             observed_at="2026-09-03T06:30:00Z", source=SYN, quality=0.9)
        refined_eph_b = EvidenceRecord.create("ephemeris", host_b.entity_id, values={"period_days": 9.4, "epoch_utc": "2026-09-03T14:00:00Z", "duration_hours": 3.0},
                                              source=SYN, quality=0.95)
        return fresh_phot_a, refined_eph_b

    def test_new_evidence_changes_the_plan(self):
        u, obj, ctx, adapter = setup()
        first = decide(u, obj["A"], ctx, adapter, **FIXED)
        u2 = u.with_evidence(*self.new_evidence(u), label="slice1+evidence")
        adapter.load_universe(u2)                                       # incremental: only the new records are registered
        second = decide(u2, obj["A"], ctx, adapter, **FIXED)
        self.assertEqual(first.plan.actions[0].designation, "SYN-HOST-A")
        self.assertEqual(second.plan.actions[0].designation, "SYN-HOST-B")
        self.assertNotEqual(first.evaluation.kernel_digest, second.evaluation.kernel_digest)
        self.assertNotEqual(u.universe_id, u2.universe_id)
        self.assertEqual({e.entity_id for e in u.entities}, {e.entity_id for e in u2.entities})   # identities unchanged
        b_result = second.evaluation.result_for(u.find("SYN-HOST-B").entity_id)
        used = set(b_result.evidence_ids)
        self.assertIn(self.new_evidence(u)[1].evidence_id, used)                                # the decision cites the new record

    def test_contested_evidence_is_excluded_and_traced(self):
        u, obj, ctx, adapter = setup()
        tr = u.find("SYN-TR-2026a")
        r = decide(u, obj["B"], ctx, adapter, **FIXED).evaluation.result_for(tr.entity_id)
        excluded = [x for rule in r.eligibility if rule["rule"] == "evidence_policy" for x in rule["excluded"]]
        self.assertTrue(any(x["reason"] == "status contested" for x in excluded))
        self.assertTrue(all(u.evidence_for(tr.entity_id) and e.status == "admissible" for e in
                            [next(ev for ev in u.evidence if ev.evidence_id == eid) for eid in r.evidence_ids]))


class TestRelationshipSensitivity(unittest.TestCase):
    def test_new_endorsed_relationship_changes_ranking(self):
        u, obj, ctx, adapter = setup()
        plain, host_a = u.find("SYN-PLAIN-E"), u.find("SYN-HOST-A")
        base = decide(u, obj["D"], ctx, adapter, **FIXED)
        assess = EvidenceRecord.create("calibration_assessment", plain.entity_id, values={"stability": 0.99}, source=SYN, quality=0.9)
        rel = RelationshipAssertion.create("calibration_reference_for", {"reference": plain.entity_id, "target": host_a.entity_id},
                                           evidence_ids=[assess.evidence_id], confidence=0.9, source=SYN)
        u2 = u.with_evidence(assess).with_relationships(rel)
        adapter.load_universe(u2)
        after = decide(u2, obj["D"], ctx, adapter, **FIXED)
        self.assertGreater(after.evaluation.result_for(plain.entity_id).rank, 0)
        self.assertLess(after.evaluation.result_for(plain.entity_id).rank, base.evaluation.result_for(plain.entity_id).rank)
        self.assertIn("calibration_reference_for", [e.type_name for e in after.snapshot.edges_of(plain.entity_id)])

    def test_unevaluated_relationship_has_no_effect_when_excluded(self):
        u, obj, ctx, adapter = setup()
        plain, host_a = u.find("SYN-PLAIN-E"), u.find("SYN-HOST-A")
        base = decide(u, obj["D"], ctx, adapter, **FIXED).evaluation.result_for(plain.entity_id)
        rel = RelationshipAssertion.create("calibration_reference_for", {"reference": plain.entity_id, "target": host_a.entity_id}, source=SYN)  # no evidence
        u2 = u.with_relationships(rel)
        adapter.load_universe(u2)
        after = decide(u2, obj["D"], ctx, adapter, **FIXED)
        r = after.evaluation.result_for(plain.entity_id)
        edge = [e for e in after.snapshot.edges_of(plain.entity_id) if e.type_name == "calibration_reference_for"][0]
        self.assertEqual(edge.stance, "unevaluated")
        self.assertEqual(r.score, base.score)
        self.assertEqual(r.contributions, base.contributions)
        self.assertTrue(any(x["key"] == edge.key for rule in r.eligibility if rule["rule"] == "relationship_policy" for x in rule["excluded"]))


class TestDeterminism(unittest.TestCase):
    def test_fresh_kernels_reproduce_evaluation_plan_and_receipt(self):
        u, obj, ctx, a1 = setup()
        a2 = open_or_bootstrap(u)
        d1 = decide(u, obj["A"], ctx, a1, **FIXED)
        d2 = decide(u, obj["A"], ctx, a2, **FIXED)
        self.assertEqual(d1.snapshot, d2.snapshot)
        self.assertEqual(d1.evaluation.to_record(), d2.evaluation.to_record())
        self.assertEqual(d1.plan.to_record(), d2.plan.to_record())
        self.assertEqual(d1.receipt.receipt_id, d2.receipt.receipt_id)
        self.assertEqual(d1.receipt.to_record(), d2.receipt.to_record())


class TestIdentityInvariance(unittest.TestCase):
    def test_changing_context_cannot_change_identity(self):
        u, obj, ctx, adapter = setup()
        ids = {e.entity_id for e in u.entities}
        for o in obj.values():
            ev = evaluate(u, adapter.snapshot(), o, ctx)
            self.assertEqual({r.entity_id for r in ev.results}, ids)
            self.assertEqual(ev.universe_id, u.universe_id)
        self.assertEqual(Universe.load(ROOT / "data" / "universe" / "slice1.json").universe_id, u.universe_id)


class TestNoIntrinsicSignificance(unittest.TestCase):
    def test_domain_records_carry_no_significance_fields(self):
        u = Universe.load(ROOT / "data" / "universe" / "slice1.json")
        for e in u.entities:
            for key in e.attribute_map:
                self.assertFalse(any(s in key.lower() for s in _FORBIDDEN_STEMS), key)
        for ev in u.evidence:
            for key in ev.value_map:
                self.assertFalse(any(s in key.lower() for s in _FORBIDDEN_STEMS), key)

    def test_significance_lives_only_in_scoped_evaluations(self):
        u, obj, ctx, adapter = setup()
        before = u.to_record()
        d = decide(u, obj["A"], ctx, adapter, **FIXED)
        self.assertEqual(u.to_record(), before)
        rec = d.evaluation.to_record()
        for scope in ("objective_id", "context_id", "universe_id", "kernel_digest", "asa_baseline", "astro_version"):
            self.assertTrue(rec[scope])
        self.assertFalse(any("score" in attrs for attrs in (adapter.k.query(k)["attributes"] for k in adapter.k.state.uaos)))


class TestProvenance(unittest.TestCase):
    def test_receipt_traces_every_selection(self):
        u, obj, ctx, adapter = setup()
        d = decide(u, obj["A"], ctx, adapter, **FIXED)
        body = d.receipt.body
        self.assertEqual(body["asa_baseline"], json.loads((ROOT / "config" / "asa-baseline.json").read_text())["sha"])
        self.assertEqual(body["kernel_digest"], d.snapshot.digest)
        self.assertEqual(body["universe_id"], u.universe_id)
        evidence_ids = {e.evidence_id for e in u.evidence}
        edge_keys = {e.key for e in d.snapshot.edges}
        self.assertTrue(d.plan.actions)
        for action in d.plan.actions:
            ex = body["explanations"][action.entity_id]
            self.assertTrue(ex["why_significant_now"])
            self.assertTrue(set(ex["evidence_used"]) <= evidence_ids)
            self.assertTrue(set(ex["relationships_used"]) <= edge_keys)
            self.assertTrue(adapter.provenance(action.entity_id))
        skipped_reasons = {s.designation: s.reason for s in d.plan.skipped}
        self.assertIn("SYN-TR-2026a", skipped_reasons)

    def test_receipt_file_round_trip(self):
        import tempfile, shutil
        u, obj, ctx, adapter = setup()
        d = decide(u, obj["B"], ctx, adapter, **FIXED)
        wd = Path(tempfile.mkdtemp(prefix="astro-receipt-"))
        try:
            path = d.receipt.write(wd)
            rec = json.loads(path.read_text())
            self.assertEqual(rec["receipt_id"], d.receipt.receipt_id)
            self.assertEqual(rec["issued_at_classification"], "diagnostic-non-authoritative")
            self.assertTrue((wd / "receipt.sha256").read_text().startswith(__import__("hashlib").sha256(path.read_bytes()[:-1]).hexdigest()))
        finally:
            shutil.rmtree(wd, ignore_errors=True)


class TestBoundaryCompliance(unittest.TestCase):
    def test_astro_touches_asa_only_through_the_adapter_and_never_the_legacy_poc(self):
        for path in (ROOT / "src" / "astro").rglob("*.py"):
            tree = ast.parse(path.read_text())
            mods = set()
            for n in ast.walk(tree):
                if isinstance(n, ast.ImportFrom) and n.module:
                    mods.add(n.module)
                elif isinstance(n, ast.Import):
                    mods.update(a.name for a in n.names)
            self.assertFalse(any(m.startswith("asa_astro") for m in mods), path)
            kernel = {m for m in mods if m.startswith("asa_kernel")}
            if path.name in ("adapter.py", "locator.py"):
                self.assertTrue(kernel <= {"asa_kernel.api", "asa_kernel.identity", "asa_kernel.storage", "asa_kernel.version"}, (path, kernel))
            else:
                self.assertEqual(kernel, set(), path)
            self.assertFalse(any(m.split(".")[0] in {"matplotlib", "PIL", "pygame", "tkinter"} for m in mods), path)


class TestSlice1Dataset(unittest.TestCase):
    def test_committed_dataset_matches_generator_and_is_labelled_synthetic(self):
        committed = json.loads((ROOT / "data" / "universe" / "slice1.json").read_text())
        self.assertEqual(committed, build_slice1().to_record())
        self.assertEqual(committed["data_class"], "synthetic")
        self.assertTrue(all(e["source"]["data_class"] == "synthetic" for e in committed["entities"]))


if __name__ == "__main__":
    unittest.main()
