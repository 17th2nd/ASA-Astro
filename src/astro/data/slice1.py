"""Slice 1 synthetic universe — generator.

SYNTHETIC. No real catalogue values. Designations are invented (``SYN-…``). The dataset exists
to prove that a fixed universe yields different significance under different objectives.
Regenerate with ``python3 -m astro.data.slice1 data/universe/slice1.json``; the committed file
must be byte-identical to the generator output (tested).
"""

from __future__ import annotations

import sys

from astro.domain import Coordinates, Entity, EntityState, EvidenceRecord, Provenance, RelationshipAssertion, Universe

SYN = Provenance("astro-slice1-generator", "synthetic", "src/astro/data/slice1.py")
AS_OF = "2026-09-03T08:00:00Z"


def build() -> Universe:
    # --- infrastructure ------------------------------------------------------------------------
    site = Entity.create("site", "SYN-SITE-SSO", catalogue_ids={"SYN": "SITE-1"}, source=SYN,
                         attributes={"latitude_deg": -31.2733, "longitude_deg": 149.0644, "elevation_m": 1165, "note": "synthetic site at Siding Spring-like coordinates"})
    scope = Entity.create("telescope", "SYN-SCOPE-1M", catalogue_ids={"SYN": "T-1"}, source=SYN, attributes={"aperture_m": 1.0})
    survey = Entity.create("survey", "SYN-TRANSIENT-SURVEY", catalogue_ids={"SYN": "SURV-1"}, source=SYN)

    # --- stars -----------------------------------------------------------------------------------
    host = Entity.create("star", "SYN-HOST-A", catalogue_ids={"SYN": "S-1"}, coordinates=Coordinates(330.0, -20.0), source=SYN,
                         attributes={"magnitude_v": 10.4, "spectral_type": "K1V"})
    host_b = Entity.create("star", "SYN-HOST-B", catalogue_ids={"SYN": "S-2"}, coordinates=Coordinates(15.0, -35.0), source=SYN,
                           attributes={"magnitude_v": 11.8, "spectral_type": "G8V"})
    calib = Entity.create("star", "SYN-STD-C", catalogue_ids={"SYN": "S-3"}, coordinates=Coordinates(330.6, -20.3), source=SYN,
                          attributes={"magnitude_v": 9.9, "spectral_type": "F5V"})
    variable = Entity.create("variable_star", "SYN-VAR-D", catalogue_ids={"SYN": "S-4"}, coordinates=Coordinates(300.0, -45.0), source=SYN,
                             attributes={"magnitude_v": 12.5, "variability_class": "delta_scuti_like"})
    plain = Entity.create("star", "SYN-PLAIN-E", catalogue_ids={"SYN": "S-5"}, coordinates=Coordinates(45.0, -10.0), source=SYN,
                          attributes={"magnitude_v": 8.7, "spectral_type": "A0V"})
    giant = Entity.create("star", "SYN-GIANT-F", catalogue_ids={"SYN": "S-6"}, coordinates=Coordinates(310.0, -30.0), source=SYN,
                          attributes={"magnitude_v": 9.3, "spectral_type": "K2III"})

    # --- companions / hosts / transients -------------------------------------------------------
    planet_a = Entity.create("exoplanet", "SYN-HOST-A b", catalogue_ids={"SYN": "P-1"}, source=SYN)
    planet_b = Entity.create("exoplanet", "SYN-HOST-B b", catalogue_ids={"SYN": "P-2"}, source=SYN)
    galaxy = Entity.create("galaxy", "SYN-GAL-G", catalogue_ids={"SYN": "G-1"}, coordinates=Coordinates(335.0, -25.0), source=SYN,
                           attributes={"morphology": "Sb"})
    transient = Entity.create("transient", "SYN-TR-2026a", catalogue_ids={"SYN": "TR-1"}, coordinates=Coordinates(335.02, -25.01), source=SYN,
                              attributes={"magnitude_v": 15.8})
    cluster = Entity.create("star_cluster", "SYN-CLUSTER-H", catalogue_ids={"SYN": "C-1"}, coordinates=Coordinates(310.5, -30.2), source=SYN)

    entities = [site, scope, survey, host, host_b, calib, variable, plain, giant, planet_a, planet_b, galaxy, transient, cluster]

    # --- evidence ---------------------------------------------------------------------------------
    ev = []
    eph_a = EvidenceRecord.create("ephemeris", host.entity_id, values={"period_days": 2.75, "epoch_utc": "2026-09-01T11:00:00Z", "duration_hours": 2.1},
                                  source=SYN, quality=0.92); ev.append(eph_a)
    eph_b = EvidenceRecord.create("ephemeris", host_b.entity_id, values={"period_days": 9.4, "epoch_utc": "2026-08-30T02:00:00Z", "duration_hours": 3.0},
                                  source=SYN, quality=0.80); ev.append(eph_b)
    phot_a1 = EvidenceRecord.create("photometry", host.entity_id, values={"mag_v": 10.4}, uncertainty={"mag_v": 0.01}, observed_at="2026-08-12T12:00:00Z",
                                    source=SYN, quality=0.9, instrument_id=scope.entity_id); ev.append(phot_a1)
    phot_b1 = EvidenceRecord.create("photometry", host_b.entity_id, values={"mag_v": 11.8}, uncertainty={"mag_v": 0.02}, observed_at="2026-09-02T14:00:00Z",
                                    source=SYN, quality=0.85, instrument_id=scope.entity_id); ev.append(phot_b1)
    phot_b2 = EvidenceRecord.create("photometry", host_b.entity_id, values={"mag_v": 11.79}, uncertainty={"mag_v": 0.02}, observed_at="2026-09-02T16:00:00Z",
                                    source=SYN, quality=0.85, instrument_id=scope.entity_id); ev.append(phot_b2)
    phot_b3 = EvidenceRecord.create("photometry", host_b.entity_id, values={"mag_v": 11.81}, uncertainty={"mag_v": 0.02}, observed_at="2026-09-02T18:00:00Z",
                                    source=SYN, quality=0.85, instrument_id=scope.entity_id); ev.append(phot_b3)
    cal_c = EvidenceRecord.create("calibration_assessment", calib.entity_id, values={"stability": 0.97, "bands": ["V"]}, observed_at="2026-07-01T00:00:00Z",
                                  source=SYN, quality=0.95); ev.append(cal_c)
    phot_c = EvidenceRecord.create("photometry", calib.entity_id, values={"mag_v": 9.9}, uncertainty={"mag_v": 0.005}, observed_at="2026-08-30T10:00:00Z",
                                   source=SYN, quality=0.98, instrument_id=scope.entity_id); ev.append(phot_c)
    ts_d = EvidenceRecord.create("time_series", variable.entity_id, values={"span_days": 12.0, "cadence_minutes": 2.0, "n_points": 8640}, observed_at="2026-06-20T00:00:00Z",
                                 source=SYN, quality=0.88, instrument_id=scope.entity_id); ev.append(ts_d)
    cls_d = EvidenceRecord.create("classification", variable.entity_id, values={"class": "delta_scuti_like", "period_hours": 3.1}, source=SYN, quality=0.7,
                                  derived_from=[ts_d.evidence_id]); ev.append(cls_d)
    phot_e = EvidenceRecord.create("photometry", plain.entity_id, values={"mag_v": 8.7}, uncertainty={"mag_v": 0.01}, observed_at="2026-05-01T00:00:00Z",
                                   source=SYN, quality=0.9); ev.append(phot_e)
    ts_f = EvidenceRecord.create("time_series", giant.entity_id, values={"span_days": 40.0, "cadence_minutes": 30.0, "n_points": 1920}, observed_at="2026-07-15T00:00:00Z",
                                 source=SYN, quality=0.8); ev.append(ts_f)
    alert_tr = EvidenceRecord.create("alert", transient.entity_id, values={"confidence": 0.82, "rarity": 0.6, "classification": "SN-candidate", "mag_v": 15.8},
                                     observed_at="2026-09-03T01:30:00Z", source=SYN, quality=0.75); ev.append(alert_tr)
    contested = EvidenceRecord.create("classification", transient.entity_id, values={"class": "AGN-flare"}, source=SYN, quality=0.4, status="contested"); ev.append(contested)
    astrom_g = EvidenceRecord.create("astrometry", galaxy.entity_id, values={"ra_deg": 335.0, "dec_deg": -25.0}, source=SYN, quality=0.9); ev.append(astrom_g)
    member_f = EvidenceRecord.create("catalogue_measurement", giant.entity_id, values={"membership_probability": 0.93}, source=SYN, quality=0.8); ev.append(member_f)

    # --- relationships ----------------------------------------------------------------------------
    rels = [
        RelationshipAssertion.create("hosts", {"host": host.entity_id, "companion": planet_a.entity_id}, evidence_ids=[eph_a.evidence_id], confidence=0.96, source=SYN),
        RelationshipAssertion.create("hosts", {"host": host_b.entity_id, "companion": planet_b.entity_id}, evidence_ids=[eph_b.evidence_id], confidence=0.9, source=SYN),
        RelationshipAssertion.create("calibration_reference_for", {"reference": calib.entity_id, "target": host.entity_id},
                                     evidence_ids=[cal_c.evidence_id], confidence=0.95, source=SYN),
        RelationshipAssertion.create("near", {"pair": [calib.entity_id, host.entity_id]}, literals={"separation_arcsec": 2400},
                                     evidence_ids=[phot_c.evidence_id], confidence=0.99, source=SYN),
        RelationshipAssertion.create("hosted_transient", {"host": galaxy.entity_id, "transient": transient.entity_id},
                                     evidence_ids=[astrom_g.evidence_id, alert_tr.evidence_id], confidence=0.8, source=SYN),
        RelationshipAssertion.create("candidate_of", {"candidate": transient.entity_id, "survey": survey.entity_id}, source=SYN),
        RelationshipAssertion.create("member_of", {"member": giant.entity_id, "group": cluster.entity_id}, evidence_ids=[member_f.evidence_id], confidence=0.93, source=SYN),
        RelationshipAssertion.create("located_at", {"instrument": scope.entity_id, "site": site.entity_id}, source=SYN),
        # asserted with no evidence: stays unevaluated in ASA and is excluded by objectives that require endorsement
        RelationshipAssertion.create("comparison_star_for", {"comparison": plain.entity_id, "target": host_b.entity_id}, source=SYN),
    ]

    # --- state -------------------------------------------------------------------------------------
    states = [
        EntityState(host.entity_id, AS_OF, observation_status="observed", last_observed_at="2026-08-12T12:00:00Z"),
        EntityState(host_b.entity_id, AS_OF, observation_status="observed", last_observed_at="2026-09-02T18:00:00Z"),
        EntityState(calib.entity_id, AS_OF, observation_status="observed", last_observed_at="2026-08-30T10:00:00Z"),
        EntityState(variable.entity_id, AS_OF, observation_status="observed", last_observed_at="2026-07-02T00:00:00Z"),
        EntityState(plain.entity_id, AS_OF, observation_status="observed", last_observed_at="2026-05-01T00:00:00Z"),
        EntityState(giant.entity_id, AS_OF, observation_status="observed", last_observed_at="2026-08-24T00:00:00Z"),
        EntityState(transient.entity_id, AS_OF, observation_status="unobserved", candidate_status="candidate", alert_state="active"),
    ]
    return Universe.create("slice1", "synthetic", entities, ev, rels, states)


if __name__ == "__main__":
    build().save(sys.argv[1] if len(sys.argv) > 1 else "data/universe/slice1.json")
