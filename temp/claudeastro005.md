# claudeastro005 — Frontier audit: candidates to the literature, E/F oracles on real data

Programme: CLAUDE-ASTRO-BUILD-001 · Operator: Claude · Date: 2026-09-04 · Directive (2026-09-03 close): check the candidate findings before anyone else sees them; cap absurd tabulated uncertainties; baselines and an independent oracle for E and F; then the visual interface.

```
ASTRO_HEAD    = 500ca2a + this report   ASA_BASELINE = b855d4c730dc2553db7a693d91c7d4d0cf25d03c (unchanged)
STORE         = var/astro-store2 (analysis)   var/astro-store3 rebuilding with the corrected rule (see §6)
TESTS         = 65/65 Astro
```

## 1. The four candidate cluster associations — all fail

| Host / cluster | Position + parallax | Δv_tan (km/s) | RUWE | Literature | Verdict |
|---|---|---|---|---|---|
| GPX-1 / Trumpler 2 | 1.5 r50; 1.48 vs 1.45 mas | 23.4 | 0.95 | Benni et al. 2021 (MNRAS) tested this: 60 pc apart today, never a member; Cantat-Gaudin & Anders 2020 concur | **rejected** |
| Kepler-1383 / HSC_603 | 1.8 r50; 0.955 vs 0.948 | 29.8 | 0.99 | host 3.47±0.78 Gyr vs 207 Myr; HSC_603 flagged probable asterism (UCC), reclassified moving group (Hunt & Reffert 2024) | **rejected** |
| Kepler-780 / HSC_565 | 1.5 r50; 0.43 vs 0.35 | 365 | 18.7 | Gaia astrometry unusable; archive distance 558 pc → 1.8 mas; HSC_565 is a 3 kpc moving group with 22 mas/yr PM | **untrusted** |
| KOI-94 / CWNU_1183 | 1.7 r50; 2.11 vs 2.07 | 4.5 | 0.86 | Weiss et al. 2013: host 3.16±0.39 Gyr vs 46 Myr group; CWNU_1183 (r50 2.2°) swept up 39 Kepler-field hosts | **rejected** |

Δv_tan = 4.74047·|Δμ|/ϖ; host PM from Gaia DR3 (already in the store), cluster PM from Hunt & Reffert 2023 via VizieR (the TAP endpoint now returns 403 to curl but not to urllib; the classic `asu-tsv` interface works for spot checks).

**Lesson:** position and parallax are necessary, not sufficient. Every candidate passed both; the discriminant the literature used is proper motion. The formula did what the rule said; the rule was too weak.

## 2. Fixes (commits bf832b3, 8f89e28)

- `astro.knowledge.geometry`: membership endorsed only when Δv_tan ≤ 3 km/s and host RUWE ≤ 1.4; no PM on either side or bad RUWE → asserted without evidence (unevaluated); disagreeing PM → nothing asserted. Counts: `member_of`, `member_of_unevaluated`, `member_of_rejected_proper_motion`.
- Hunt & Reffert manifest query now carries `pmRA,pmDE`; parser records `pmra_mas_yr`/`pmdec_mas_yr`; snapshot re-fetched (7,167 rows, digest recorded); fixture updated.
- `ephemeris_drift`: σ_P/P > `max_period_fraction` (default 1%) is an undetermined period, not drift → rejected with trace; unavailable with reason if nothing sane remains. KOI-7892 c (75.2 ± 38.9 d) and five others no longer saturate the feature.

## 3. Re-test of all 244 associations (`tools/candidate_findings.py`, store2 universe)

41 kinematic members · 20 untrusted (RUWE) · 183 rejected. Survivors are the known ones: Praesepe 8 (K2-95/100/101/102/104/264, Pr0201, Pr0211), M67 5, Taurus 6 (Theia 7, CWNU 1129), Chamaeleon I 3, Upper Sco (K2-33, 1RXS J1609), Ruprecht 147 (K2-231), NGC 2423, IC 4651, TOI-1227. Six kinematic matches not confirmed from memory, to put to an astronomer: Kepler-1928 & Kepler-970 / HSC_572, Kepler-1915 / NGC 6866, Kepler-1938 / CWNU_1183, HD 220074 / Theia 1232, 2MASS J03590986+2009361 / HSC_1340.

## 4. Decayed ephemerides

Yesterday's 422 = hosts (552 planets). Sane (σ_P/P ≤ 1%): **419 hosts / 546 planets**; recoverable in one night (σ_T ≤ 12 h): **288 hosts / 352 planets** (K2-22 b, EPIC 228836835 b, K2-90 c, K2-239 c, K2-71 b, TOI-1749 b lead). Undetermined periods set aside: 6 (KOI-7892 c, EPIC 248847494 b, KIC 3558849 b, HD 224018 d, Kepler-82 b/c). K2-13 b and K2-11 b (0.8% period error, drift five weeks) argue for a tighter cap or a one-night flag. Output: `var/runs/candidate-findings-store2.json`.

## 5. Independent oracles and baselines for E and F (commits 2398c4f, 500ca2a)

- `astro.benchmark.oracles.knowledge_gap_reduction` (graded: fillable missing kinds + decayed transit in window) and `dispute_adjudication` (two admissible records, different sources, beyond tolerance; Gaia parallax as 1000/ϖ) recompute from raw evidence and declared expectations — never from `lacks_evidence`/`measures`/`contradicts` or features. `SimulatedExecutor` gains `reduce_gap` and `resolve_dispute`. Harness records `total_gain`; the oracle strategy orders by gain.
- **Defect found by the synthetic benchmark:** contradictions were only registered by `load_frontier` (store build), so in the session loop and benchmark (which call `adapter.load_universe` per cycle) objective F planned nothing. `AstroAdapter.load_universe` now records contradictions between registered claims and retires (never re-registers) a `lacks_evidence` gap whose evidence the universe holds. Test added (`test_frontier_objectives_have_oracles_and_the_session_registers_disputes`).
- Real data: `tools/cut_universe.py` cone of 3,061 entities (RA 340°, Dec −10°, r 10°; sites travel with every cut), Siding Spring 2026-09-04, V ≤ 14. Receipts `var/runs/benchmark-cone-dev-{E,F}.json`.

| F · Dispute adjudication (61 cands) | useful | wasted | first |
|---|---|---|---|
| fifo | 1/8 | 280/320 min | 120 min |
| random | 2/8 | 240/320 | 20 |
| static_priority (brightest) | 0/8 | 320/320 | never |
| **asa** | **6/6** | **0/240** | 20 |
| oracle | 6/6 | 0/240 | 20 |

| E · Knowledge-gap reduction (201 cands) | useful | gain | wasted |
|---|---|---|---|
| fifo | 6/8 | 9 | 120 |
| random | 5/8 | 7 | 180 |
| static_priority (brightest) | 8/8 | 17 | 0 |
| **asa** | 8/8 | **17** | 0 |
| oracle | 8/8 | 20 | 0 |

**Honest reading:** F discriminates (ASA = oracle, brightest-first scores zero). E as declared earns nothing over brightest-first on this cone — bright RV hosts lack time series and spectra just as faint K2 hosts do. On the synthetic universe E is precise but conservative (1 target, 0 waste, oracle 5; `min_score` 0.45 excludes the rest). The weights are for an astronomer to set; the benchmark measures them now.

## 6. Store 3 rebuild

`astro store build --store var/astro-store3 --frontier --as-of 2026-09-04T08:00:00Z --evidence-fragment var/tess-fragment.json --universe-out var/universe-real-frontier-tess-v2.json` running at report time; §7 of the next report (or an addendum below) records its counts. Expected: member_of endorsed ≈ 41, unevaluated ≈ 20, rejected ≈ 183.

## 7. Debug scope and navigator (afternoon, Brock: "settle for the debug scope of 50 pc … a graphic UI with visual navigation through the systems")

- `tools/cut_universe.py --max-distance-pc 50` → `var/universe-50pc-dev.json` (from the store2 universe; re-cut from v2 when store3 lands): 613 stars, 959 planets, 4 clusters (Melotte 25 = Hyades, HSC_906, HSC_2846, FSR_1017); 2,689 MPC sites travel with the cut and are excluded from the UI. 51 disputed stars, 596 with gaps. ⚠ No `member_of` in this set, and the Hyades host K2-25 will not get one from store3 either: in the store2 snapshot Melotte 25 carried no parallax (VizieR row had Plx null in the earlier column set), so no test ran; with today's snapshot (Plx 21.23 mas, PM 104.1/−28.7) K2-25 (22.36 mas, PM 122.4/−18.6) fails both the parallax window (Δϖ 1.1 mas against max(0.3, 3σ)) and the flat proper-motion test (Δv_tan 4.4 km/s) — a cluster 20 pc deep at 47 pc spans ±4 mas, and perspective makes members' proper motions differ by tens of mas/yr. Nearby extended clusters need a 3-D space-velocity (convergent-point) test with a depth-aware parallax window. Recorded as next work; the current rule is right for clusters beyond ~200 pc, which is where all 244 candidates were.
- `astro ui` (commit ff8342a): `astro.ui.export` (nodes with evidence/claims/disputes/gaps, graph edges with stance+lifecycle, per-objective scores with contributions, findings verdicts) + `astro.ui.navigator.html` (D3 7.9 UMD; sky | system graph | detail; breadcrumbs; filters: disputed / gaps / members / rejected / drift / hosts). Built on the 50 pc set with A/E/F under Siding Spring 2026-09-04: 1,576 nodes, 967 edges, 3.4 MB. Artifact c7f52b3b-2330-4abd-b6e6-a43a70962a91. Top under F: GJ 887, K2-129, LTT 1445 A, GJ 674 (all M dwarfs — the GSP-Phot bias again); under A: HR 858, TOI-2427, TOI-198; under E: TOI-2194, K2-129, K2-116.
- Benchmark E/F on the 50 pc set: see addendum.

## 8. Next

Tighten the drift cap / one-night flag and hand the 288-host list out; the six unconfirmed kinematic members to a Kepler-field astronomer; re-weight E with an astronomer and re-run the graded benchmark; cone benchmarks for A/B/C on real data; SIMBAD aliases; photometric-stability evidence; checkpointed kernel open; the three-pane visual.
