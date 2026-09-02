"""Slice 2: schedule, simulated execution, and the evaluate → execute → re-evaluate session loop."""

from __future__ import annotations

import unittest
from pathlib import Path

from astro.domain import Universe
from astro.execution import SimulatedExecutor, schedule_plan
from astro.objectives.context import parse_utc
from astro.objectives.loaders import load_context, load_objective
from astro.pipeline import decide, open_or_bootstrap
from astro.session import run_session

ROOT = Path(__file__).resolve().parents[2]
OBJ = ROOT / "data" / "objectives"
FIXED = dict(commit="0" * 40, issued_at="2026-09-03T08:00:00Z")


def setup(letter: str):
    u = Universe.load(ROOT / "data" / "universe" / "slice1.json")
    name = {"A": "A-exoplanet-transit-followup.json", "B": "B-transient-followup.json", "C": "C-stellar-variability.json", "D": "D-calibration.json"}[letter]
    return u, load_objective(OBJ / name), load_context(ROOT / "data" / "contexts" / "night-2026-09-03.json", u), open_or_bootstrap(u)


class TestSchedule(unittest.TestCase):
    def test_transit_is_scheduled_around_the_predicted_mid_transit(self):
        u, o, ctx, adapter = setup("A")
        d = decide(u, o, ctx, adapter, **FIXED)
        sched = schedule_plan(d.plan, d.evaluation, u, ctx)
        self.assertEqual([s.designation for s in sched.scheduled], ["SYN-HOST-A"])
        s = sched.scheduled[0]
        trace = next(c["trace"] for c in d.evaluation.result_for(s.entity_id).contributions if c["feature"] == "transit_window_proximity")
        mid = parse_utc(trace["next_transit_utc"])
        self.assertTrue(parse_utc(s.start_utc) <= mid <= parse_utc(s.end_utc))
        self.assertTrue(all(parse_utc(iv[0]) <= parse_utc(s.start_utc) and parse_utc(s.end_utc) <= parse_utc(iv[1])
                            for iv in [next(iv for iv in s.basis["visible_intervals"] if iv[0] <= s.start_utc)]))

    def test_no_overlaps_and_plan_order_respected_in_time(self):
        u, o, ctx, adapter = setup("D")
        d = decide(u, o, ctx, adapter, **FIXED)
        sched = schedule_plan(d.plan, d.evaluation, u, ctx)
        times = [(parse_utc(s.start_utc), parse_utc(s.end_utc)) for s in sched.scheduled]
        for (s1, e1), (s2, e2) in zip(times, times[1:]):
            self.assertLessEqual(e1, s2)
        self.assertEqual(sched.schedule_id, schedule_plan(d.plan, d.evaluation, u, ctx).schedule_id)


class TestPlanPolicy(unittest.TestCase):
    def test_min_score_keeps_unworthy_targets_off_the_plan(self):
        u, o, ctx, adapter = setup("A")
        d = decide(u, o, ctx, adapter, **FIXED)
        self.assertEqual([a.designation for a in d.plan.actions], ["SYN-HOST-A"])         # HOST-B has no transit tonight
        reasons = {s.designation: s.reason for s in d.plan.skipped}
        self.assertIn("below the objective's minimum", reasons["SYN-HOST-B"])

    def test_repeat_gap_uses_asa_registered_state(self):
        u, o, ctx, adapter = setup("D")
        s = run_session(u, o, ctx, adapter, max_cycles=4, **FIXED)
        self.assertEqual(s.executed(), ("SYN-STD-C",))
        second = s.cycles[1].decision.plan
        self.assertFalse(second.actions)
        self.assertTrue(any("repeat gap" in x.reason for x in second.skipped if x.designation == "SYN-STD-C"))


class TestSimulatedExecutor(unittest.TestCase):
    def test_execution_records_facts_only_and_is_labelled(self):
        u, o, ctx, adapter = setup("B")
        d = decide(u, o, ctx, adapter, **FIXED)
        sched = schedule_plan(d.plan, d.evaluation, u, ctx)
        evidence, state = SimulatedExecutor().execute(sched.scheduled[0], u, ctx)
        self.assertEqual({e.kind for e in evidence}, {"observation_log", "spectrum"})
        for e in evidence:
            self.assertEqual(e.source.data_class, "simulated")
            self.assertTrue(e.value_map.get("simulated"))
            self.assertNotIn("mag_v", e.value_map)
            self.assertNotIn("classification", e.value_map)
        self.assertEqual(state.observation_status, "observed")
        self.assertEqual(state.last_observed_at, sched.scheduled[0].end_utc)


class TestSessionLoop(unittest.TestCase):
    def test_transient_is_classified_once_then_the_loop_stops(self):
        u, o, ctx, adapter = setup("B")
        s = run_session(u, o, ctx, adapter, **FIXED)
        self.assertEqual(s.executed(), ("SYN-TR-2026a",))
        self.assertEqual(len(s.cycles), 2)
        self.assertIsNone(s.cycles[1].outcome)

    def test_variability_session_moves_to_the_next_target(self):
        u, o, ctx, adapter = setup("C")
        s = run_session(u, o, ctx, adapter, **FIXED)
        self.assertEqual(s.executed()[:2], ("SYN-VAR-D", "SYN-GIANT-F"))
        c1, c2 = s.cycles[0], s.cycles[1]
        self.assertEqual(c1.decision.evaluation.ranked()[0].designation, "SYN-VAR-D")
        self.assertNotEqual(c1.decision.evaluation.kernel_digest, c2.decision.evaluation.kernel_digest)   # new evidence entered ASA
        self.assertEqual(c1.outcome.universe_after, c2.universe_id)                                        # universes chain
        self.assertIn(c1.outcome.evidence[0].evidence_id, {e.evidence_id for e in s.final_universe.evidence})

    def test_session_is_deterministic_across_fresh_kernels(self):
        u, o, ctx, a1 = setup("C")
        a2 = open_or_bootstrap(u)
        s1 = run_session(u, o, ctx, a1, **FIXED)
        s2 = run_session(u, o, ctx, a2, **FIXED)
        self.assertEqual(s1.session_id, s2.session_id)
        self.assertEqual(s1.to_record(), s2.to_record())
        self.assertEqual(a1.digest(), a2.digest())

    def test_original_universe_is_never_mutated(self):
        u, o, ctx, adapter = setup("A")
        before = u.to_record()
        s = run_session(u, o, ctx, adapter, **FIXED)
        self.assertEqual(u.to_record(), before)
        self.assertNotEqual(s.final_universe.universe_id, u.universe_id)
        self.assertEqual({e.entity_id for e in s.final_universe.entities}, {e.entity_id for e in u.entities})


if __name__ == "__main__":
    unittest.main()
