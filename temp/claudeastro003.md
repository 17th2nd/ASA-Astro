# claudeastro003 — Slice 3: real catalogues in the ASA substrate

Programme: CLAUDE-ASTRO-BUILD-001 · Operator: Claude · Date: 2026-09-03 · Directive: "Build on the database UAO/USI URO with all accessible astronomy knowledge."

```
ASTRO_HEAD    = f0bc266  (+ this report; on top of 029a153)
ASA_BASELINE  = b855d4c730dc2553db7a693d91c7d4d0cf25d03c  (unchanged)
STORE         = var/astro-store  BUILD universe UNI-81a3ff535e29…  kernel seq 868292  digest sha256:37b191b9c282…
```

## What "accessible" turned out to mean

Every public astronomy endpoint this machine can reach without credentials was probed. Seven were ingested; each
row becomes a UAO (entity or evidence) or a URO (relationship) in the persistent kernel, with provenance naming the
source, release, licence and row. Raw snapshots are digest-recorded in `data/catalogues/manifest.json` and never
committed; the fixtures under `tests/astro/fixtures/catalogues/` are 20–40 real rows each so tests run offline.

| Source | Rows → Astro | Notes |
|---|---|---|
| NASA Exoplanet Archive `pscomppars` | 6,354 planets, 4,764 host stars, 6,354 `hosts` relationships, 4,727 transit ephemerides | BJD_TDB→UTC ignores TDB−UTC (~69 s) and light-time; recorded on every ephemeris. `gaia_id` does not exist in this table — `gaia_dr3_id` does. |
| Gaia DR3 `gaia_source_lite` | 4,408 hosts: astrometry (J2016), G/BP/RP photometry, GSP-Phot Teff | POST TAP in batches of 800; quality 0.95 when RUWE < 1.4 |
| GCVS 5.1 (VizieR) | 60,715 variable stars with class, period, magnitudes | 179 rows without coordinates skipped |
| OpenNGC | 13,309 NGC/IC objects: 10,750 galaxies, 430 nebulae, clusters, stars, 419 regions | **CC-BY-SA-4.0** — share-alike; 661 Dup/NonEx rows skipped, not invented |
| Hunt & Reffert 2023 | 7,167 clusters and moving groups | `Kind` column does not exist; VizieR TAP_SCHEMA is 403 |
| IAU MPC observatory codes | 2,689 sites; WGS84 latitude and elevation derived (Siding Spring 1164 m vs 1165 true) | labelled `derived` |
| ALeRCE ZTF light-curve classifier | 13 supernova candidates from the last 46 days (SNIa 9, SNIbc 2, SNII 1, SLSN 1) | API filter parameter is `class=`, not `class_name=` (which is silently ignored) |

Not reachable or not attempted: TNS (needs an account), SIMBAD per-object aliases (one request per object; deferred),
time-series archives (TESS/MAST; see findings).

## The store

`astro store build` parses, merges by identity (a host star seen by the Exoplanet Archive and Gaia is one entity),
and loads into a FileStorage kernel: 95,011 entities, 102,581 evidence, 6,354 relationships → 868,292 events in
327 s; 4.0 GB on disk; `BUILD.json` records counts by kind, snapshot digests, licences, timing, kernel head/digest.
Reload is idempotent (4 s, nothing appended). Opening the store replays the whole log (105 s). `astro store status --verify`:
Governor-less verifier passes chain, content-hash, content-schema, recorded-key-as-of-seq, governed-sequence, registry-binding
and replay checks, and the replay digest equals the live digest (5.5 min, 6.9 GB peak). Scale facts and the three follow-on ASA requests are in `temp/astro-asa-integration.md`.

## Real objectives, real night — Siding Spring (MPC 413), 2026-09-03 09:00–19:00 UTC, 1 m class, V ≤ 14

| Objective | Eligible | Result |
|---|---|---|
| A transit follow-up | 3,613 of 95,011 | **TOI-4311** (P = 0.990 d, transit 14:44 UTC, peaks at 89.8° altitude) scheduled 13:20–16:20 centred on the transit; TOI-178, HATS-16, TOI-849, WASP-94 A, WASP-98 next. 22 s to evaluate. |
| B transient follow-up | 13 | ZTF26ablsebw (SLSN candidate, p = 0.45, alert 1 day old) then ZTF26abkwmlm scheduled 11:40–13:10. |
| C stellar variability | 0 | **Negative finding.** The objective requires `time_series` evidence; GCVS supplies classifications with periods, not light curves. No target is eligible and the engine says so rather than substituting. Real light curves (TESS/MAST) are the next ingestion. |
| D calibration (anchor TOI-4311) | 5,553 | **Negative finding.** No catalogue asserts `calibration_reference_for`; every star scores 0.29 < 0.5 and nothing is planned. Deriving `near`/comparison relationships from coordinates is the next relationship class to build — labelled `derived`. |

Universe and kernel digest are unchanged after all four evaluations. Receipts and schedules: `var/runs/{A,B}/`.

## Defects and corrections this slice

- Evaluating 95k entities was quadratic: `RelationalSnapshot.edges_of/evidence_of` scanned all edges and links per entity, and the adapter's duplicate check scanned all UROs per proposal. Both now use lazily built indices; `Universe` lookups likewise. 22 s per objective over 95k entities.
- MPC elevation used the equatorial radius as sea level (Greenwich came out at −13 km); fixed with the WGS84 geocentric radius at the site's latitude.
- The store is heavy to open because the kernel replays every event; that is an ASA-side property, recorded as a request, not worked around in Astro.

## Scientific integrity

Every record carries `data_class` real or derived and a provenance reference to its source row. Conversions that
lose precision (BJD_TDB→UTC, MPC geodesy) are stated on the record. Classifier probabilities are used as alert
confidence and labelled as such; per-class "rarity" is a declared prior, not a measurement. OpenNGC is
share-alike; redistribution of derived Astro data that includes it would carry CC-BY-SA-4.0 — founder decision
if Astro data is ever published. Nothing here validates ASA scientifically.

## Tests

54 Astro tests (8 new catalogue tests on committed real-row fixtures), exec 38, frozen artefacts 6/6.

## Next

1. Time-series ingestion (TESS light curves via MAST) so objective C and asteroseismology-style workloads run on real data.
2. Derived relationships from geometry: `near` and `comparison_star_for` candidates around each transiting host, labelled `derived`, with the angular separation as a literal.
3. SIMBAD aliases and object types for hosts (batched TAP upload).
4. Kernel scale: checkpointed open, compact content store, batched persistence (ASA requests).
5. The visual three-pane interface over the real store.
