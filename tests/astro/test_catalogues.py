"""Catalogue adapters on small committed fixtures (real rows, offline)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from astro.catalogues import merge_fragments
from astro.catalogues.manifest import SOURCES
from astro.catalogues.parsers import (bjd_tdb_to_utc, gaia_host_map, parse_alerce, parse_clusters, parse_exoplanets, parse_gaia_hosts,
                                      parse_gcvs, parse_mpc_sites, parse_openngc, sexagesimal_to_deg)
from astro.domain import Universe

FIX = Path(__file__).resolve().parent / "fixtures" / "catalogues"


class TestConversions(unittest.TestCase):
    def test_bjd_and_sexagesimal(self):
        self.assertEqual(bjd_tdb_to_utc(2459000.5), "2020-05-31T00:00:00Z")
        self.assertAlmostEqual(sexagesimal_to_deg("00:08:27.05", hours=True), 2.1127083, places=5)
        self.assertAlmostEqual(sexagesimal_to_deg("-12:49:22.3", hours=False), -12.822861, places=5)
        self.assertAlmostEqual(sexagesimal_to_deg("+27:43:03.6", hours=False), 27.7176667, places=5)


class TestParsers(unittest.TestCase):
    def test_exoplanets_hosts_and_ephemerides(self):
        f = parse_exoplanets(FIX / "exoplanets.csv")
        self.assertEqual(len(f.relationships), 40)                              # one hosts relationship per planet row
        stars = [e for e in f.entities if e.kind == "star"]
        planets = [e for e in f.entities if e.kind == "exoplanet"]
        self.assertEqual(len(planets), 40)
        self.assertTrue(all(e.source.data_class == "real" for e in f.entities))
        self.assertTrue(all(e.coordinates is not None for e in stars))
        for rel in f.relationships:
            self.assertEqual(rel.relationship_type, "hosts")
        eph = [v for v in f.evidence if v.kind == "ephemeris"]
        for v in eph:
            self.assertIn("period_days", v.value_map)
            self.assertTrue(v.value_map["epoch_utc"].endswith("Z"))
            self.assertIn("time_conversion", v.value_map)
        self.assertTrue(any(a.startswith("Gaia DR3 ") for s in stars for a in s.aliases))

    def test_gaia_attaches_to_hosts_by_dr3_id(self):
        exo = parse_exoplanets(FIX / "exoplanets.csv")
        m = gaia_host_map(exo)
        g = parse_gaia_hosts(m, FIX / "gaia_hosts.csv")
        self.assertTrue(g.evidence)
        host_ids = {e.entity_id for e in exo.entities}
        self.assertTrue(all(v.subject_id in host_ids for v in g.evidence))
        self.assertEqual({v.kind for v in g.evidence} - {"astrometry", "photometry", "derived_measurement"}, set())
        self.assertFalse(g.skipped)

    def test_gcvs_openngc_clusters(self):
        g = parse_gcvs(FIX / "gcvs.csv")
        self.assertEqual(len(g.entities), len(g.evidence))
        self.assertTrue(all(e.kind == "variable_star" for e in g.entities))
        self.assertTrue(all(v.kind == "classification" and "class" in v.value_map for v in g.evidence))
        n = parse_openngc(FIX / "openngc.csv")
        self.assertTrue(n.entities)
        self.assertTrue(all(e.kind in ("galaxy", "nebula", "star_cluster", "star", "transient", "sky_region") for e in n.entities))
        self.assertTrue(all(0 <= e.coordinates.ra_deg < 360 and -90 <= e.coordinates.dec_deg <= 90 for e in n.entities))
        self.assertTrue(any(r["reason"].startswith("type") for r in n.skipped))          # Dup/NonEx rows are skipped, not invented
        c = parse_clusters(FIX / "clusters.csv")
        self.assertEqual(len(c.entities), 20)
        self.assertTrue(all(e.kind == "star_cluster" for e in c.entities))

    def test_mpc_sites_geodesy(self):
        f = parse_mpc_sites(FIX / "mpc.html")
        by = {dict(e.catalogue_ids)["MPC"]: e for e in f.entities}
        sso = by["413"].attribute_map
        self.assertAlmostEqual(sso["latitude_deg"], -31.2773, places=2)
        self.assertAlmostEqual(sso["longitude_deg"], 149.0661, places=3)
        self.assertLess(abs(sso["elevation_m"] - 1165), 400)
        self.assertLess(abs(by["568"].attribute_map["elevation_m"] - 4205), 400)         # Maunakea
        self.assertEqual(by["413"].source.data_class, "derived")

    def test_alerce_supernova_candidates(self):
        f = parse_alerce([FIX / "alerce_SNIa.json"])
        self.assertTrue(f.entities)
        self.assertTrue(all(e.kind == "transient" for e in f.entities))
        for v in f.evidence:
            self.assertEqual(v.kind, "alert")
            self.assertTrue(0 <= v.value_map["confidence"] <= 1)
            self.assertEqual(v.value_map["classification"], "SNIa")
            self.assertIn("rarity_note", v.value_map)
        self.assertEqual(len(f.states), len(f.entities))
        self.assertTrue(all(s.alert_state == "active" and s.candidate_status == "candidate" for s in f.states))


class TestMerge(unittest.TestCase):
    def test_merge_is_identity_based_and_labelled_real(self):
        exo = parse_exoplanets(FIX / "exoplanets.csv")
        g = parse_gaia_hosts(gaia_host_map(exo), FIX / "gaia_hosts.csv")
        sites = parse_mpc_sites(FIX / "mpc.html")
        u = merge_fragments("fixture", exo, g, sites, exo)                     # exoplanets twice: no duplicates
        self.assertEqual(u.data_class, "real")
        self.assertEqual(len(u.entities), len({e.entity_id for e in exo.entities} | {e.entity_id for e in sites.entities}))
        host = next(e for e in u.entities if e.kind == "star" and any(a.startswith("Gaia DR3") for a in e.aliases))
        kinds = {v.kind for v in u.evidence_for(host.entity_id)}
        self.assertIn("astrometry", kinds)
        self.assertEqual(u.find_by_catalogue("MPC", "413").designation, "Siding Spring Observatory")
        self.assertEqual(Universe.from_record(u.to_record()).universe_id, u.universe_id)

    def test_every_source_has_licence_and_citation(self):
        for spec in SOURCES.values():
            self.assertTrue(spec.licence and spec.citation and spec.release, spec.key)


if __name__ == "__main__":
    unittest.main()
