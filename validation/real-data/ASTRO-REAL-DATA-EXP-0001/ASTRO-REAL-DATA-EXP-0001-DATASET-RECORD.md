# ASTRO-REAL-DATA-EXP-0001 — Dataset-selection record

Operator: Claude · Written 2026-09-04 (UTC), **before** any retrieval script, adapter or baseline was implemented and before
the frozen retrieval. One availability probe was made on 2026-09-04 to confirm that the ExoClock endpoint exists, what
fields it carries, how many of its planets have a name match in the archive snapshot already held by the repository, and
that the NASA Exoplanet Archive exposes reference-link columns. The probe copy is not used by the experiment; the frozen
retrieval happens after this record and is digest-recorded in the provenance file.

## 1. Research question

> Under the Context "transit-ephemeris maintenance in 2029" — which known transiting planets most need a new
> transit-timing observation — does the Astro engine's ranking of candidate host stars, computed from NASA Exoplanet
> Archive composite ephemerides, Gaia DR3 astrometry and ASA relational state, agree with the ExoClock project's
> independently assigned ephemeris priority better than (i) a brightness baseline, (ii) a tabulated period-uncertainty
> baseline, and (iii) graph-topology baselines (degree, PageRank) over the same ASA relational state?

## 2. Selected dataset

| Role | Source | Identity |
|---|---|---|
| **ASTRO input — ephemerides, host attributes** | NASA Exoplanet Archive, Planetary Systems Composite Parameters (`pscomppars`) | The repository's existing frozen snapshot: `data/catalogues/raw/exoplanetarchive_pscomppars.csv`, retrieved 2026-09-02T22:42:44Z, sha256 `efe8352882797b33ac36d5171b8fa9a8af6d67fe346a0dba39965af3d95556c6` (recorded in `data/catalogues/manifest.json`). Live table; no versioned release. |
| **ASTRO input — astrometry, photometry, Teff** | Gaia DR3 `gaia_source_lite` for archive host stars | Existing snapshot `data/catalogues/raw/gaia_dr3_hosts.csv`, retrieved 2026-09-02T22:53:43Z, sha256 `64f14a90ee2be1650a52bd38a5f12b1c71bcc3183ed4e8c0dc399ecf584cdb1a`. Release Gaia DR3 (2022-06-13). |
| **Leakage check — ephemeris provenance** | NASA Exoplanet Archive `pscomppars` reference links | New retrieval (TAP, CSV) of `pl_name, pl_orbper, pl_orbpererr1, pl_orbper_reflink, pl_tranmid, pl_tranmiderr1, pl_tranmid_reflink` for `tran_flag = 1`; digest and retrieval time recorded at retrieval. |
| **Independent reference truth** | ExoClock project planet database, `https://www.exoclock.space/database/planets_json` | New retrieval (JSON); digest and retrieval time recorded at retrieval. Field `priority ∈ {alert, high, medium, low}`. |

## 3. Exact fields used

ASTRO input (through the existing `astro.catalogues.parsers.parse_exoplanets` and `parse_gaia_hosts`, unchanged):
`pl_name, hostname, ra, dec, sy_vmag, sy_gaiamag, sy_dist, st_spectype, st_teff, st_rad, st_mass, pl_orbper,
pl_orbpererr1, pl_tranmid, pl_tranmiderr1, pl_trandur, pl_rade, pl_bmasse, tran_flag, discoverymethod, disc_year,
disc_facility, gaia_dr2_id, gaia_dr3_id, tic_id, hd_name, hip_name`; Gaia `source_id, ra, dec, parallax, parallax_error,
pmra, pmdec, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, radial_velocity, teff_gspphot, ruwe`.

Reference truth: ExoClock `name`, `priority`. Recorded alongside but **not used** for scoring: `star`, `ra_j2000`,
`dec_j2000`, `v_mag`, `total_observations`, `total_observations_recent`, `t0_bjd_tdb`, `t0_unc`, `period_days`,
`period_unc`, `duration_hours`, `min_telescope_inches`.

Leakage check: archive `pl_orbper_reflink`, `pl_tranmid_reflink` (`refstr` attribute) and the values `pl_orbper,
pl_orbpererr1, pl_tranmid, pl_tranmiderr1` for consistency with the 2026-09-02 snapshot.

## 4. Independent ground truth

ExoClock is an ESA-Ariel-linked, professionally coordinated ephemeris-maintenance programme (Kokori et al. 2022,
ApJS 258, 40; Kokori et al. 2023, ApJS 265, 4). Its database page (read 2026-09-04) defines the ephemeris priority as
follows: the target timing uncertainty is one twelfth of the transit duration in 2029; **alert** — observations in the
last two years show an O−C above ten minutes; **high** — predicted uncertainty above the target, or fewer than three
epochs observed in the last two years; **medium** — fewer than three epochs observed in the last year; **low** —
otherwise. The list contains only Ariel-observable targets.

The label is therefore an expert programme's operational judgement, published independently of this repository, that
combines (a) projected transit-time uncertainty — a quantity ASTRO's `ephemeris_drift` feature is declared to compute —
and (b) recency of observation in ExoClock's own records, which ASTRO has no evidence for. The label is ordinal;
grades are assigned alert = 3, high = 2, medium = 1, low = 0.

The reference answer is not derived from ASTRO, ASA, this repository or its operator.

## 5. Why the task is suitable for ASTRO

- The question is a Context: a declared purpose (ephemeris maintenance), a declared epoch (2029, the ExoClock
  definition epoch) and a declared feasibility constraint. The same universe under a different Context (transit
  tonight, dispute adjudication) gives a different ranking; that is the engine's central claim.
- The relevant evidence carries explicit uncertainty (`pl_orbpererr1`, `pl_tranmiderr1`) that must be propagated over
  elapsed cycles; the engine's declared uncertainty treatment is what is being tested.
- Typed relationships enter through `hosts` (planet ↔ host, endorsed by evidence), `measures` claims and
  `contradicts` disputes (Teff and distance between archive and Gaia), and `lacks_evidence` gaps — the ASA relational
  state the graph baselines will be computed on.
- A fair simple baseline exists (brightness; tabulated period uncertainty), a fair graph baseline exists (degree,
  PageRank over the ASA relational graph), and the whole run takes seconds on one machine.

## 6. Candidate inclusion and exclusion rules (declared here; frozen in the manifest)

1. Planet present in the ExoClock database at retrieval with `priority ∈ {alert, high, medium, low}`.
2. Name match to an archive `pl_name` after removing spaces and hyphens and case-folding; unmatched names are listed.
3. Archive row has `tran_flag = 1`, `pl_orbper`, `pl_tranmid`, **and both** `pl_orbpererr1` and `pl_tranmiderr1`
   (rows lacking either uncertainty are held out as the *missing-evidence* adversarial set, not invented).
4. The host has exactly one transiting planet in the archive snapshot and exactly one ExoClock entry, so the unit of
   analysis (host star, which is where the engine attaches ephemeris evidence) carries one label.
5. **Leakage exclusion:** the archive's `pl_orbper_reflink` or `pl_tranmid_reflink` `refstr` contains `KOKORI`
   (an ExoClock publication supplied the ephemeris the engine would read), or the live reflink row's period/epoch
   values differ from the 2026-09-02 snapshot (reference not attributable to the value used). Excluded candidates are
   listed with the reason.
6. Primary sample: order the remaining pool by the hexadecimal SHA-256 of `ASTRO-REAL-DATA-EXP-0001-v1 | <pl_name>`
   and take the first 100. The full remaining pool is a secondary, non-decisive analysis; the pool including
   leakage-flagged planets is a further secondary analysis with the flag reported.

## 7. Possible leakage risks

| Risk | Handling |
|---|---|
| The archive composite ephemeris was published by ExoClock (Kokori et al.), so the input uncertainty is ExoClock's own | Rule 5 excludes such planets from the primary sample; the count is reported. |
| ExoClock's current ephemeris is newer than any publication; low-priority planets are those ExoClock has observed most | Not a leak into ASTRO's input (ASTRO reads the archive only); it is label noise that hurts every method equally. Recorded as a limitation. |
| The operator declared the objective after knowing the label definition | Unavoidable for a new objective; the declaration uses only existing feature code, is pre-registered with a content id before any run, and never changes. Objective E "Knowledge-gap reduction", declared 2026-09-03 before this programme, is run unchanged as a secondary check. |
| Name-matching errors | Exact normalised match only; unmatched names listed; no manual pairing. |
| Archive rows updated between 2026-09-02 (snapshot) and the reflink retrieval | Rule 5: value mismatch ⇒ excluded from the primary sample. |

## 8. Licence and provenance

- NASA Exoplanet Archive: public domain / NASA data policy; cite the archive (doi:10.26133/NEA13). Operated by
  Caltech under contract with NASA.
- Gaia DR3: ESA Gaia data policy; cite Gaia Collaboration 2016, 2023.
- ExoClock: public database offered for programmatic access on its own database page; citation of Kokori et al.
  2022/2023 required in any use. The experiment stores only the candidate rows' `name`, `priority` and the recorded
  non-scoring fields, with the retrieval time and digest of the full download. Wider publication of the extract is a
  founder decision (as recorded for OpenNGC in claudeastro003).
- Every stored row carries the source key, retrieval time and the sha256 of the raw file it came from
  (`dataset/PROVENANCE.json`).

## 9. Expected limitations

- The label mixes projected uncertainty with observation recency that ASTRO cannot see, so a perfect ranking is not
  achievable by any method reading these inputs; the ceiling is unknown and is not estimated post hoc.
- ASTRO's `ephemeris_drift` saturates at σ_T ≥ transit duration (value 1.0), so the most uncertain planets tie.
- The Context epoch (2029-01-01) follows ExoClock's definition; the retrieval-date Context is an adversarial check,
  not a second primary.
- Only single-transiting-planet hosts are candidates; multi-planet systems are out of scope.
- The archive's transit-midpoint conversion BJD_TDB → UTC in the existing parser ignores the ~69 s TDB−UTC offset and
  light-time (recorded on every ephemeris record); at the precision of this task it is immaterial.
- A positive result is engineering evidence about the Astro engine's uncertainty handling under one Context; it is
  not scientific validation of ASA, ASTRO-THEORY-0001 or any `ASTRO-CLM-*` claim, and the evidence level stays EH-0.

## 10. Why this task and not an easier one

Two tasks with more obviously favourable structure were rejected: cluster membership (the geometry rule was revised on
2026-09-04 after comparison with the literature — a post-hoc-tuned task cannot be re-run as a blind test), and
"which transits are observable tonight" against the archive's own transit service (same data, tests only Context
arithmetic). The ExoClock task has an external expert label, a genuinely competitive scalar baseline, and a known
unobservable component that can make ASTRO fail.
