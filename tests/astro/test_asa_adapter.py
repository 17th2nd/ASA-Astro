"""Astro ↔ ASA adapter: deterministic translation, endorsement by evidence, restart and replay."""

from __future__ import annotations

import ast
import shutil
import tempfile
import unittest
from pathlib import Path

from astro.asa.adapter import AstroAdapter, FileStorage, decimal_text, uao_id
from astro.domain import EntityState
from tests.astro.fixtures import FACET, small_universe

ROOT = Path(__file__).resolve().parents[2]


class TestDecimalText(unittest.TestCase):
    def test_restricted_decimal_strings(self):
        self.assertEqual(decimal_text(1.0), "1")
        self.assertEqual(decimal_text(0.9), "0.9")
        self.assertEqual(decimal_text(1800), "1800")
        self.assertEqual(decimal_text(0.000001), "0.000001")
        self.assertEqual(decimal_text(-0.0), "0")


class TestAdapter(unittest.TestCase):
    def test_load_is_deterministic_and_idempotent(self):
        u = small_universe()
        a = AstroAdapter.in_memory(FACET)
        counts = a.load_universe(u)
        self.assertEqual(counts, {"entities": 4, "evidence": 2, "relationships": 2, "supports": 1, "states": 1, "status_updates": 0})
        d1, seq1 = a.digest(), a.k.head()["seq"]
        again = a.load_universe(u)
        self.assertEqual(again["entities"], 0)
        self.assertEqual(a.digest(), d1)
        self.assertEqual(a.k.head()["seq"], seq1)                       # duplicates fold; nothing appended
        b = AstroAdapter.in_memory(FACET)
        b.load_universe(u)
        self.assertEqual(b.digest(), d1)                                # second fresh kernel: same digest
        self.assertEqual(b.k.head()["head"], a.k.head()["head"])         # deterministic clock: same head hash

    def test_evidence_endorses_supported_relationship(self):
        u = small_universe()
        a = AstroAdapter.in_memory(FACET)
        a.load_universe(u)
        snap = a.snapshot()
        host = u.find("SYN-HOST-1").entity_id
        hosts = snap.edges_of(host, "hosts")
        near = snap.edges_of(host, "near")
        self.assertEqual(len(hosts), 1)
        self.assertEqual(hosts[0].stance, "endorsed")                    # cited ephemeris evidence → supports → endorsed
        self.assertEqual(len(hosts[0].supported_by), 1)
        self.assertEqual(near[0].stance, "unevaluated")                  # no evidence cited → stays unevaluated
        self.assertEqual(near[0].role_of(host), "pair")
        self.assertEqual(len(snap.evidence_of(host)), 2)
        self.assertEqual(snap.state_of(host).literals and dict(snap.state_of(host).literals)["observation_status"], "observed")

    def test_state_supersession(self):
        u = small_universe()
        a = AstroAdapter.in_memory(FACET)
        a.load_universe(u)
        host = u.find("SYN-HOST-1").entity_id
        old = a.snapshot().state_of(host)
        a.register_state(EntityState(host, "2026-09-02T00:00:00Z", observation_status="scheduled", last_observed_at="2026-08-20T03:00:00Z"))
        snap = a.snapshot()
        new = snap.state_of(host)
        self.assertNotEqual(old.key, new.key)
        self.assertEqual(dict(new.literals)["observation_status"], "scheduled")
        self.assertEqual([s.lifecycle for s in snap.states if s.key == old.key], ["superseded"])

    def test_restart_replay_and_verify(self):
        u = small_universe()
        wd = Path(tempfile.mkdtemp(prefix="astro-adapter-"))
        try:
            a = AstroAdapter.bootstrap(FileStorage(wd / "store"), FACET, "test")
            a.load_universe(u)
            d1, snap1 = a.digest(), a.snapshot()
            del a
            b = AstroAdapter.open(FileStorage(wd / "store"))
            self.assertEqual(b.digest(), d1)
            self.assertEqual(b.snapshot(), snap1)
            self.assertEqual(b.replay_digest(), d1)
            self.assertEqual(b.verify()["digest"], d1)
        finally:
            shutil.rmtree(wd, ignore_errors=True)

    def test_provenance_reaches_kernel_events(self):
        u = small_universe()
        a = AstroAdapter.in_memory(FACET)
        a.load_universe(u)
        host = u.find("SYN-HOST-1").entity_id
        prov = a.provenance(host)
        self.assertTrue(prov)
        self.assertTrue(all("event" in p and "seq" in p for p in prov))

    def test_adapter_uses_only_the_consumer_contract(self):
        tree = ast.parse((ROOT / "src" / "astro" / "asa" / "adapter.py").read_text())
        mods = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        self.assertEqual({m for m in mods if m.startswith("asa_kernel")}, {"asa_kernel.api", "asa_kernel.identity", "asa_kernel.storage"})

    def test_uao_id_is_stable(self):
        self.assertEqual(uao_id("ENT-x"), uao_id("ENT-x"))
        self.assertTrue(uao_id("ENT-x").startswith("asa:uao:astro/"))


if __name__ == "__main__":
    unittest.main()
