"""Knowledge frontier: absence, derived relationships, claims and contradictions, tiles, and their ASA round trip."""

from __future__ import annotations

import struct
import unittest
from pathlib import Path

from astro.asa.adapter import AstroAdapter
from astro.catalogues import merge_fragments
from astro.catalogues.parsers import gaia_host_map, parse_alerce, parse_exoplanets, parse_gaia_hosts, parse_mpc_sites, parse_openngc
from astro.catalogues.tess import read_bintable
from astro.domain import Coordinates, Entity, EvidenceRecord, Provenance, Universe
from astro.knowledge import derive_frontier
from astro.knowledge.claims import derive_claims
from astro.knowledge.expectations import expected_kinds
from astro.knowledge.frontier import derive_gaps, load_frontier
from astro.knowledge.geometry import SkyGrid, separation_arcsec
from astro.knowledge.tiles import derive_tiles, tile_designation
from astro.objectives import ObservingContext
from astro.objectives.loaders import load_objective
from astro.significance import evaluate
from tests.astro.fixtures import FACET

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "tests" / "astro" / "fixtures" / "catalogues"
SYN = Provenance("astro-test-fixture", "synthetic", "tests/astro/test_knowledge.py")
AS_OF = "2026-09-03T08:00:00Z"


def real_fixture_universe() -> Universe:
    exo = parse_exoplanets(FIX / "exoplanets.csv")
    return merge_fragments("fixture", exo, parse_gaia_hosts(gaia_host_map(exo), FIX / "gaia_hosts.csv"), parse_mpc_sites(FIX / "mpc.html"),
                           parse_openngc(FIX / "openngc.csv"), parse_alerce([FIX / "alerce_SNIa.json"]))


class TestExpectationsAndGaps(unittest.TestCase):
    def test_transiting_hosts_expect_five_kinds_and_gaps_are_relationships(self):
        u = real_fixture_universe()
        host = next(e for e in u.entities if e.kind == "star" and u.relationships_of(e.entity_id, "hosts") and u.evidence_for(e.entity_id, "ephemeris"))
        kinds = {x.evidence_kind for x in expected_kinds(host, u)}
        self.assertEqual(kinds, {"ephemeris", "astrometry", "photometry", "spectrum", "time_series"})
        ev, rels, counts = derive_gaps(u, AS_OF)
        mine = [r for r in rels if r.role_map["subject"][0] == host.entity_id]
        self.assertEqual({r.literal_map["evidence_kind"] for r in mine}, {"spectrum", "time_series"})      # ephemeris/astrometry/photometry present
        self.assertFalse(ev)                                                                                # gaps are relationships, not evidence UAOs
        self.assertTrue(all(r.source.data_class == "derived" for r in rels))

    def test_gap_closes_when_evidence_arrives(self):
        u = real_fixture_universe()
        host = next(e for e in u.entities if e.kind == "star" and u.evidence_for(e.entity_id, "ephemeris"))
        f = derive_frontier(u, AS_OF, tiles=False)
        a = AstroAdapter.in_memory(FACET, "gaps")
        u1 = f.apply(u)
        load_frontier(a, u1, f)
        before = [e for e in a.snapshot().edges_of(host.entity_id, "lacks_evidence") if e.lifecycle == "registered"]
        self.assertIn("time_series", {dict(e.literals)["evidence_kind"] for e in before})
        ts = EvidenceRecord.create("time_series", host.entity_id, values={"span_days": 27.0, "cadence_minutes": 2.0, "simulated": True}, source=SYN, observed_at=AS_OF)
        u2 = u.with_evidence(ts)
        f2 = derive_frontier(u2, "2026-09-04T08:00:00Z", tiles=False)
        counts = load_frontier(a, f2.apply(u2), f2)
        after = [e for e in a.snapshot().edges_of(host.entity_id, "lacks_evidence") if e.lifecycle == "registered"]
        self.assertNotIn("time_series", {dict(e.literals)["evidence_kind"] for e in after})
        self.assertGreaterEqual(counts["gaps_retired"], 1)


class TestGeometry(unittest.TestCase):
    def test_separation_and_grid(self):
        self.assertAlmostEqual(separation_arcsec(10.0, 0.0, 10.0, 1.0), 3600.0, places=3)
        a = Entity.create("star", "GA", catalogue_ids={"T": "1"}, coordinates=Coordinates(100.0, -30.0), source=SYN)
        b = Entity.create("star", "GB", catalogue_ids={"T": "2"}, coordinates=Coordinates(100.005, -30.004), source=SYN)
        c = Entity.create("star", "GC", catalogue_ids={"T": "3"}, coordinates=Coordinates(120.0, -30.0), source=SYN)
        grid = SkyGrid([a, b, c])
        near = grid.near(100.0, -30.0, 60.0)
        self.assertEqual([e.designation for e, _ in near], ["GA", "GB"])

    def test_derived_relationships_are_labelled_and_edges_stay_unevaluated_without_evidence(self):
        host = Entity.create("star", "HOSTX", catalogue_ids={"T": "h"}, coordinates=Coordinates(50.0, -40.0), source=SYN, attributes={"magnitude_v": 10.0})
        planet = Entity.create("exoplanet", "HOSTX b", catalogue_ids={"T": "hb"}, source=SYN)
        comp = Entity.create("star", "COMPX", catalogue_ids={"T": "c"}, coordinates=Coordinates(50.01, -40.005), source=SYN, attributes={"magnitude_v": 10.8})
        gal = Entity.create("galaxy", "GALX", catalogue_ids={"T": "g"}, coordinates=Coordinates(60.0, -20.0), source=SYN, attributes={"major_axis_arcmin": 3.0})
        tr = Entity.create("transient", "TRX", catalogue_ids={"T": "t"}, coordinates=Coordinates(60.003, -20.002), source=SYN)
        from astro.domain import RelationshipAssertion
        eph = EvidenceRecord.create("ephemeris", host.entity_id, values={"period_days": 3.0, "epoch_utc": AS_OF, "duration_hours": 2}, source=SYN)
        u = Universe.create("g", "synthetic", [host, planet, comp, gal, tr], [eph],
                            [RelationshipAssertion.create("hosts", {"host": host.entity_id, "companion": planet.entity_id}, evidence_ids=[eph.evidence_id], source=SYN)])
        f = derive_frontier(u, AS_OF, tiles=False)
        types = {r.relationship_type for r in f.relationships}
        self.assertTrue({"near", "comparison_star_for", "hosted_transient"} <= types)
        a = AstroAdapter.in_memory(FACET, "geom")
        load_frontier(a, f.apply(u), f)
        snap = a.snapshot()
        self.assertEqual({e.stance for e in snap.edges_of(host.entity_id, "near")}, {"endorsed"})                 # separation evidence supports it
        self.assertEqual({e.stance for e in snap.edges_of(host.entity_id, "comparison_star_for")}, {"unevaluated"})  # suggestive only
        self.assertEqual({e.stance for e in snap.edges_of(tr.entity_id, "hosted_transient")}, {"endorsed"})


class TestClaims(unittest.TestCase):
    def test_contradicting_claims_are_recorded_in_asa_and_drive_objective_f(self):
        star = Entity.create("star", "DISP", catalogue_ids={"T": "d"}, coordinates=Coordinates(330.0, -20.0), source=SYN, attributes={"magnitude_v": 9.0})
        t1 = EvidenceRecord.create("derived_measurement", star.entity_id, values={"teff_k": 5800.0}, source=Provenance("cat-A", "real", "exoplanets:DISP"))
        t2 = EvidenceRecord.create("derived_measurement", star.entity_id, values={"teff_k": 5000.0, "method": "GSP-Phot"}, source=Provenance("cat-B", "real", "gaia_hosts:1"))
        u = Universe.create("c", "synthetic", [star], [t1, t2])
        ev, claims, contradictions, counts = derive_claims(u)
        self.assertEqual(len(claims), 2)
        self.assertEqual(len(contradictions), 1)
        f = derive_frontier(u, AS_OF, tiles=False)
        a = AstroAdapter.in_memory(FACET, "claims")
        counts = load_frontier(a, f.apply(u), f)
        self.assertEqual(counts["contradictions"], 1)
        snap = a.snapshot()
        self.assertEqual(len(snap.disputes_of(star.entity_id)), 2)                      # both claims are party to one contradiction
        site = Entity.create("site", "S", catalogue_ids={"MPC": "413"}, source=SYN, attributes={"latitude_deg": -31.27, "longitude_deg": 149.07})
        u2 = f.apply(u).with_states() if False else Universe.create("c2", "synthetic", list(f.apply(u).entities) + [site], f.apply(u).evidence, f.apply(u).relationships)
        a.load_universe(u2)
        ctx = ObservingContext.declare(label="t", as_of=AS_OF, window_start="2026-09-03T09:00:00Z", window_end="2026-09-03T19:00:00Z", site_id=site.entity_id, constraints={"limiting_magnitude": 14})
        o = load_objective(ROOT / "data" / "objectives" / "F-dispute-adjudication.json")
        ev = evaluate(u2, a.snapshot(), o, ctx)
        r = ev.result_for(star.entity_id)
        self.assertEqual(r.status, "eligible")
        c = next(x for x in r.contributions if x["feature"] == "dispute_presence")
        self.assertEqual(c["value"], 1.0)
        self.assertEqual(c["trace"]["disputed_quantities"], ["teff_k"])


class TestTiles(unittest.TestCase):
    def test_tiles_cover_the_sky_and_flag_empty_regions(self):
        u = real_fixture_universe()
        tiles, ev, counts = derive_tiles(u)
        self.assertEqual(len(tiles), 648)
        self.assertEqual(tile_designation(123.4, -45.6), "TILE-RA120-DEC-50")
        gaps = [v for v in ev if v.kind == "coverage_gap"]
        self.assertTrue(gaps and counts["gap_tiles"] == len(gaps))
        self.assertTrue(all(v.source.data_class == "derived" for v in ev))


class TestFitsReader(unittest.TestCase):
    def test_reads_a_synthetic_bintable(self):
        def card(k, v): return f"{k:<8}= {v:>20}".ljust(80).encode()
        def block(cards):
            raw = b"".join(cards) + b"END".ljust(80)
            return raw + b" " * ((2880 - len(raw) % 2880) % 2880)
        primary = block([card("SIMPLE", "T"), card("BITPIX", "8"), card("NAXIS", "0")])
        rows = [(2100.0, 1000.0, 1.0, 0), (2100.00139, 1002.0, 1.0, 0), (2100.00278, float("nan"), 1.0, 8)]
        rowlen = 8 + 4 + 4 + 4
        hdr = block([card("XTENSION", "'BINTABLE'"), card("BITPIX", "8"), card("NAXIS", "2"), card("NAXIS1", str(rowlen)), card("NAXIS2", str(len(rows))),
                     card("PCOUNT", "0"), card("GCOUNT", "1"), card("TFIELDS", "4"), card("TTYPE1", "'TIME'"), card("TFORM1", "'D'"),
                     card("TTYPE2", "'PDCSAP_FLUX'"), card("TFORM2", "'E'"), card("TTYPE3", "'PDCSAP_FLUX_ERR'"), card("TFORM3", "'E'"),
                     card("TTYPE4", "'QUALITY'"), card("TFORM4", "'J'"), card("EXTNAME", "'LIGHTCURVE'")])
        body = b"".join(struct.pack(">dffi", *r) for r in rows)
        body += b"\0" * ((2880 - len(body) % 2880) % 2880)
        cols = read_bintable(primary + hdr + body, ("TIME", "PDCSAP_FLUX", "QUALITY"))
        self.assertEqual(cols["TIME"][0], 2100.0)
        self.assertEqual(cols["QUALITY"], [0, 0, 8])
        self.assertAlmostEqual(cols["PDCSAP_FLUX"][1], 1002.0, places=3)


if __name__ == "__main__":
    unittest.main()
