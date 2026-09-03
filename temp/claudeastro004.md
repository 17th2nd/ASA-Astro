# claudeastro004 — Knowledge frontier on the real store

Programme: CLAUDE-ASTRO-BUILD-001 · Operator: Claude · Date: 2026-09-03 · Directive: "Proceed with all the recommendations … we want data and to build understanding of our own relationship formula through its dissemination."

```
ASTRO_HEAD    = 8156463 + this report   ASA_BASELINE = b855d4c730dc2553db7a693d91c7d4d0cf25d03c (unchanged)
STORE         = var/astro-store2   universe UNI-b35d2a016fee…   kernel seq 2,473,958   12 GB
```

## What was built (all six recommendations)

| # | Recommendation | Implementation |
|---|---|---|
| 1 | Absence as a first-class record | Declared expectations per entity kind with rationale and scope (`astro.knowledge.expectations`); each unmet one is a `lacks-evidence` URO in ASA, retired when the evidence arrives. |
| 2 | An objective that values ignorance reduction | Objective E "Knowledge-gap reduction": gap fraction, **ephemeris drift** (σ_T = √(σ_T0² + (n·σ_P)²) against transit duration), staleness, catalogue-flagged classification uncertainty, region emptiness, feasibility. |
| 3 | Relationships derived from geometry | `near` (haversine, with separation evidence → endorsed), cluster `member_of` (within 2 r50 and parallax agreement → endorsed with confidence), `hosted_transient` (none found in this catalogue set), `comparison_star_for` candidates (asserted **without** evidence → unevaluated: the semantic edge, on record). |
| 4 | ASA's dispute machinery | Measurement claims as `measures` UROs (Teff, distance incl. Gaia 1000/parallax, per-planet period), each supported by its evidence; disagreement beyond a declared tolerance → `asa.core/contradicts`. Objective F "Dispute adjudication". |
| 5 | Sky coverage as entities | 648 ten-degree tiles with density-percentile evidence and coverage-gap records for the emptiest quartile. |
| 6 | Continuous measurements | MAST/TESS SPOC 2-min light curves via a stdlib FITS reader; `time_series` evidence with on-disk CSV, digest, cadence, span, rms. |

## The frontier, as the store states it (2026-09-03 08:00 UTC)

| | Count | Detail |
|---|---|---|
| Entities · evidence · registered relationships | 95,659 · 187,438 · 136,139 | after TESS merge |
| **Blank spaces** (`lacks_evidence`) | **48,011** | time_series 42,028 · spectrum 4,476 · ephemeris 850 · catalogue_measurement 534 · photometry 68 · astrometry 55; by kind: variable_star 37,590 · star 9,861 · galaxy 302 · cluster 232 · transient 26 |
| **Semantic edges** (asserted, unsupported) | **2,297** | comparison_star_for 1,952 · hosts 345 (planets with no period/ephemeris evidence, e.g. imaging discoveries) |
| Derived and endorsed | 9,904 | near 9,660 · member_of 244 |
| **Disputes** (`contradicts`) | **439** over 432 stars | Teff 353 (Exoplanet Archive vs Gaia GSP-Phot, >7%) · distance 86 (sy_dist vs 1000/parallax, >15%) — e.g. CoRoT-35 6390 K vs 5656 K; Kepler-756 852 pc vs 1453 pc |
| Sky | 165 of 648 tiles | lowest coverage quartile or empty (per BUILD.json) |
| Feedback loop on real data | 49 TESS records merged → **25 gaps retired** | `lacks-evidence(time_series)` retired for every host whose light curve arrived |

## Tonight from Siding Spring (MPC 413), V ≤ 14 — all six objectives on one store, one context

| Objective | Eligible | Top and why |
|---|---|---|
| A transit follow-up | 3,613 | TOI-4311, transit 14:44 UTC, scheduled 13:20–16:20 (unchanged from claudeastro003) |
| B transient follow-up | 13 | ZTF26ablsebw (SLSN candidate), then ZTF26abkwmlm |
| **C stellar variability** | **25** (was 0) | NGTS-8: two TESS sectors, 0.72 of the 90-day span still missing; runs on real light curves for the first time |
| **E knowledge-gap reduction** | 67,351 | **K2-65**: 4 of 5 expected evidence kinds missing and its predicted transit time is uncertain by ±636 min against a 3.4 h transit (340 cycles since epoch) — one timed observation restores it. Then TOI-2194, K2-379. |
| **F dispute adjudication** | 4,759 (794 indeterminate) | **GJ 887**: Teff claims disagree (archive vs Gaia); then K2-129, WASP-20. Gaia GSP-Phot is known to be biased for M dwarfs, so this dispute is a real systematic, not noise. |
| D calibration | 5,553 | still nothing planned: no evidenced calibration references; the 1,952 comparison-star candidates are deliberately unevaluated until photometric stability evidence exists |

Kernel digest unchanged across the six evaluations. Receipts and schedules in `var/runs/{A,B,C,E,F}/`; frontier report `var/runs/frontier-report.json`.

## What the formula's dissemination taught us

- **Absence dominates.** Once expectations are declared, blank spaces outnumber relationships. The objective that values them (E) is bounded by feasibility and a minimum score, otherwise it would point at everything.
- **Most "contradictions" are model boundaries, not errors.** My first pass produced 1,678 period contradictions — all different planets around one host. The fix (per-planet claims) is a lesson about *what a claim is about*; the remaining 439 are real cross-catalogue disagreements, and the top one (GJ 887) is a known methodological bias. The formula surfaces semantic edges only when the claim identity is right.
- **Unevaluated is a state, not a failure.** 2,297 relationships sit in ASA asserted but unsupported. Objectives that exclude them (A–D) and objectives that include them (E, F) give different answers from the same store, as intended.
- **The loop closes on real data.** Light curves arriving from MAST retired 25 gap relationships without any special case.

## Defects found and fixed this slice

Adapter duplicate index collided for identity-literal types (claims, gaps, states) → literal-qualified index. Period claims across planets (above). Exoplanet Archive Teff/distance and GCVS magnitudes were attributes, not evidence → now evidence, so claims and gaps are honest. My evaluation script dropped tile coverage-gap evidence when merging TESS; the report now counts tiles by their identifier (BUILD.json holds the correct 165).

## Scale (recorded for ASA main in `temp/astro-asa-integration.md`)

2,473,590 events; load 4,477 s; open 293 s; 12 GB. Throughput fell to ≈550 ev/s because the kernel Governor's `_supports_count` scans every URO per `supports` proposal (O(n·m), read in source). Astro's own paths are indexed: universe load 280 s (320 MB JSON), snapshot 37 s, each objective 48–82 s over 95,659 entities.

## Tests

70 Astro tests (9 new: gaps and retirement, geometry endorsed vs unevaluated, claims → contradiction → objective F, tiles, FITS reader, frontier report), exec 38, frozen 6/6.

## Next

Baselines and an independent oracle for objectives E and F (§18 discipline applies to discovery too); SIMBAD aliases; photometric-stability evidence so comparison-star candidates can be adjudicated; a checkpointed kernel open; the three-pane visual over the frontier store.
