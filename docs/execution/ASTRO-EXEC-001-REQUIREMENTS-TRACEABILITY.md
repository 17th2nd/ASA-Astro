# ASTRO-EXEC-001 — Requirements Traceability

Every engine requirement traces to `ASTRO-THEORY-0001`, `ASTRO-EXP-0001`, `ASTRO-CLAIMS-0001`, `ASTRO-RESULTS-0001`, or an explicitly approved engineering decision. **No scientific behaviour may exist because an implementation operator considered it reasonable.**

Status vocabulary: `Specified` — fully derivable from a frozen artefact · `Ruling required` — depends on an open `UR` · `Engineering decision` — no scientific content, engineering judgement recorded here.

## 1. Traceability matrix

| Req | Source · section | Derived engineering requirement | Component | Validating test | Output | Status |
|---|---|---|---|---|---|---|
| R-001 | EXP §Datasets | Freeze a manifest of every source locator, retrieval time, release id and digest before target selection | Dataset Registry, Manifest Mgr | `test_manifest_freeze_completeness` | `manifest.json` | Specified |
| R-002 | EXP §Datasets | Permit only Gaia DR3 SSO, DE440, SB441-N16, Horizons (check only). Reject any other source | Input Manager | `test_rejects_unpermitted_dataset` | `UnmanifestedInput` | Specified |
| R-003 | EXP §Datasets | Forbid substituting a later release or revised JPL orbit | Dataset Registry | `test_release_substitution_blocked` | validation finding | Specified |
| R-004 | EXP §Target population 1–5 | Eligibility: permanent number; not a candidate perturber; ≥20 FoV transits spanning ≥600 d; no cometary activity or fitted nongravitational parameter; passes apparatus checks | Eligibility | `test_eligibility_all_five_rules` | eligibility record | Specified |
| R-005 | EXP §Target population | Calibration population $2.0\le a\le3.5$ au and $q\ge1.7$ au; deployment $q<1.3$ au, from Gaia DR3 osculating orbit | Eligibility | `test_population_assignment` | population label | Specified |
| R-006 | EXP §Target population | Calibration order by SHA-256 of `ASTRO-EXP-0001-CAL-v1 \| number` | Ordering | `test_cal_ordering_vectors` | ordered list | **Ruling required `UR-004`** |
| R-007 | EXP §Target population | Deployment order by SHA-256 of `salt \| ASTRO-EXP-0001-DEP-v1 \| number`; salt external, witnessed, published, never redrawn | Ordering | `test_dep_ordering_vectors` | ordered list | **Ruling required `UR-004`** |
| R-008 | EXP §Target population | Take first 27 apparatus-valid; next 10 are ordered reserves | Eligibility | `test_27_plus_10` | target set | Specified |
| R-009 | EXP §Target population | No seed or salt may be searched for a favourable target set | Controller | `test_single_salt_application` | audit record | Specified |
| R-010 | EXP §Ground truth | Posterior: $\mathbf x_{t,q}=\hat{\mathbf x}_t+L_t\Phi^{-1}(\mathbf u_q)$, $L_t$ the unique lower-triangular Cholesky with positive diagonal | Posterior | `test_cholesky_positive_diagonal` | 32 states | Specified |
| R-011 | EXP §Ground truth | $\mathbf u_q$ = points 2–33 of the standard 6-D Sobol sequence | Posterior | `test_sobol_vectors` | unit-cube points | **Ruling required `UR-006`** |
| R-012 | EXP §Ground truth | Publish the 32 states and their source points in the frozen manifest **before either deployment selection** | Manifest Mgr | `test_states_published_pre_selection` | `manifest.json` | Specified |
| R-013 | EXP §Ground truth | Same 32 vectors used for full, comparator and ASA propagations | Truth Lab | `test_shared_posterior_states` | provenance | Specified |
| R-014 | EXP §Ground truth | Fit produces 6-D mean and covariance at the common start epoch | Orbit fit | `test_fit_covariance_shape` | $\hat{\mathbf x}_t$, $C_t$ | **Ruling required `UR-003`** |
| R-015 | EXP §Ground truth | Force model: Newtonian point-mass Sun, Moon, 8 planets, Pluto, 16 SB441-N16 asteroids; states and GM fixed from DE440 and SB441-N16 | Force model | `test_force_model_composition` | context | Specified |
| R-016 | EXP §Ground truth | EIH 1PN correction in **every** propagation, $\beta=\gamma=1$ | Force model | `test_eih_applied_all_runs` | context | Specified |
| R-017 | EXP §Ground truth | Nongravitational accelerations excluded | Force model | `test_no_nongrav_terms` | context | Specified |
| R-018 | EXP §Ground truth | Deletion intervention is exact and singular: $\mathbf a_j\to\mathbf 0$; nothing else altered | Force model | `test_deletion_is_singular` | diff record | Specified |
| R-019 | EXP §Ground truth | Four propagation classes per target/draw: 1 full, 16 single-deletion, 1 ASA-selected, 1 comparator-selected | Truth Lab | `test_propagation_class_counts` | truth outputs | Specified |
| R-020 | EXP §Ground truth | Gaia TCB observations converted to TDB via IAU TCB–TDB before fitting | Timescales | `test_tcb_tdb_conversion` | evidence | Specified |
| R-021 | EXP §Primary endpoint | Integration and evaluation in TDB; positions barycentric ICRF3; errors in km | Frames, Metrics | `test_frames_and_units` | truth outputs | Specified |
| R-022 | EXP §Primary endpoint | Daily epochs $k=0..7305$, 2017-07-01 → 2037-07-01 00:00 TDB | Context | `test_epoch_grid_7306` | context | Specified |
| R-023 | EXP §Primary endpoint | $E_m(t)=\operatorname{median}_q\max_k\|\mathbf r_{full,q}-\mathbf r^{(4)}_{m,q}\|$ | Metrics | `test_endpoint_formula` | $E_m(t)$ | Specified |
| R-024 | EXP §Primary endpoint | $\delta_t=3\times$ largest change in either $E_m(t)$ under tightened accuracy, computed **before unblinding** | Resolution | `test_delta_t_definition` | $\delta_t$ | **Ruling required `UR-005`** |
| R-025 | EXP §Primary endpoint | Material win iff $E_{ASA}(t)+\delta_t\le0.80E_{LOO}(t)$ | Metrics | `test_materiality_rule` | per-target flag | Specified |
| R-026 | EXP §Primary endpoint | $W=\sum_{t=1}^{27}\mathbf 1[\cdot]$; success iff $W\ge20$ | Metrics | `test_W_and_threshold` | $W$ | Specified |
| R-027 | EXP §The single experiment | Both methods retain exactly 4 of 16, for a 20-year propagation | Controller | `test_exactly_four_distinct` | selections | Specified |
| R-028 | EXP §The single experiment | Comparator: $L_j=\operatorname{median}_q\max_k\|\mathbf r_{full,q}-\mathbf r_{-j,q}\|$; rank decreasing; tie broken by increasing permanent number; no fitted parameter | Comparator | `test_loo_ranking_and_tiebreak` | ranking | Specified |
| R-029 | EXP §The single experiment | Neither method may use the error of any four-perturber deployment model before its selection is sealed | Leakage Guard | `test_no_pre_seal_outcome_access` | seal digests | Specified |
| R-030 | EXP §Secondary endpoints | **No** secondary endpoint. Diagnostics are published but cannot qualify the decision | Metrics | `test_no_metric_alters_decision` | metrics | Specified |
| R-031 | EXP §Apparatus checks 1 | Fit on first 70 % of transits; reduced $\chi^2\in[0.5,2.0]$ on final 30 % under the published Gaia covariance model | Validation | `test_apparatus_check_1` | check record | **Ruling required `UR-003`** |
| R-032 | EXP §Apparatus checks 2 | Major-body and candidate states agree with frozen Horizons vectors within 1 km at start, midpoint, end | Validation | `test_apparatus_check_2` | check record | **Ruling required `UR-007`** |
| R-033 | EXP §Apparatus checks 3 | Max 20-year displacement between full and all-asteroids-omitted model exceeds 100× integration floor | Validation | `test_apparatus_check_3` | check record | **Ruling required `UR-005`** |
| R-034 | EXP §Apparatus checks 4 | Tightened-accuracy repeat changes no daily position by more than 1/100 of the check-3 displacement | Validation | `test_apparatus_check_4` | check record | **Ruling required `UR-005`** |
| R-035 | EXP §Apparatus checks | A failed check excludes the object **before unblinding**; replaced by next reserve; exclusions and all check values published | Controller | `test_exclusion_and_substitution` | exclusion record | **Ruling required `UR-010`** |
| R-036 | EXP §Calibration environment | Calibration yields no evidence of transfer and has no endpoint | Controller | `test_calibration_emits_no_endpoint` | — | Specified |
| R-037 | EXP §Calibration environment | Estimator freeze requires a complete specification and a cryptographic digest | Estimator Interface | `test_estimator_digest_required` | digest | **Ruling required `UR-001`** |
| R-038 | EXP §Calibration environment | After deposit, no rule, parameter, threshold, feature, input or preprocessing may change | Leakage Guard | `test_frozen_estimator_immutable` | digest check | Specified |
| R-039 | EXP §Deployment environment | Estimator returns exactly four distinct SB441-N16 identifiers for every target; no refit, recalibration or target-specific judgement | Estimator Interface | `test_four_distinct_every_target` | selections | **Ruling required `UR-001`** |
| R-040 | EXP §Blind protocol | Four separated roles; comparator archive and counterfactuals hidden from ASA lab until its 27 selections are sealed | Role partition | `test_role_capability_isolation` | sealed archives | Specified |
| R-041 | EXP §Blind protocol | Truth lab runs ASA-selected models only after sealing; may not alter any earlier input, comparator result, tolerance or trajectory | Truth Lab | `test_no_post_seal_mutation` | digest chain | Specified |
| R-042 | EXP §Blind protocol | The statistician opens the archives once. **There is no interim look** | Controller | `test_single_unblinding` | audit | Specified |
| R-043 | EXP §Stopping rules 1–7 | Encode all seven stopping rules, including terminal stop at $W\le19$ | Controller | `test_stopping_rules` | stop record | Specified |
| R-044 | EXP §Stopping rules 5 | Abstention, duplicate, invalid identifier or missing submission counts as a non-win | Metrics | `test_invalid_submission_is_nonwin` | per-target flag | Specified |
| R-045 | EXP §Failure classification | Classify F0/F1/F2/F3 with the stated consequences | Validation | `test_failure_classification` | F-class | Specified |
| R-046 | EXP §Statistical analysis | 27 targets are the only independent observations; 32 draws collapsed inside each target endpoint | Metrics | `test_draws_collapsed_within_target` | $E_m(t)$ | Specified |
| R-047 | EXP §Statistical analysis | Exact one-sided binomial; $P\{X\ge20\}=0.0095786452293396$; no multiplicity adjustment; no imputation; ties against ASA | Statistics | `test_exact_binomial_value` | p-value | Specified |
| R-048 | EXP §Statistical analysis | Report $W$, exact p, every $E_{ASA}$, $E_{LOO}$, $\delta_t$ and ratio | Result Generator | `test_required_reporting_set` | report | Specified |
| R-049 | EXP §Publication policy | Publish regardless of result; negative results receive equal permanence; no suppression | Result Generator | `test_publication_set_complete` | run package | Specified |
| R-050 | EXP §Permitted / Forbidden claims | Emit only the bounded permitted wording; never emit a forbidden claim | Claim Comparator | `test_forbidden_claim_strings_absent` | claims output | Specified |
| R-051 | CLM-0070 | Compare outcome to the `ASTRO-CLM-0070` condition without rewriting the claim | Claim Comparator | `test_claims_are_read_only` | comparison | Specified |
| R-052 | CLM-0071 | Report H0 rejection only at the preregistered one-sided threshold | Statistics | `test_h0_rejection_rule` | comparison | Specified |
| R-053 | CLM-0072 | On any terminal class, emit exactly the required negative wording | Claim Comparator | `test_terminal_wording_exact` | comparison | Specified |
| R-054 | RES §4 | Every candidate event carries the full envelope; unknown → `unknown`, inapplicable → `not_applicable`; blanks and sentinels prohibited | Ledger Writer | `test_event_envelope_complete` | candidate event | Specified |
| R-055 | RES §4 | Use only permitted event types | Ledger Writer | `test_event_type_vocabulary` | candidate event | Specified |
| R-056 | RES §5.1 | A result exists only when all five conditions hold | Ledger Writer | `test_result_definition_gate` | candidate event | Specified |
| R-057 | RES §16 | Minimum evidence package: all 14 items resolvable, else the result stays `EH-1` | Result Generator | `test_evidence_package_14_items` | package | Specified |
| R-058 | RES §17 | Serialized identifier allocation against canonical `origin/main`, with the fast-forward-retry rule; never renumber or edit a published event | Ledger Writer | `test_allocation_and_ff_retry` | candidate event | Specified |
| R-059 | RES INV-R01–R12 | Append-only; nothing deleted; identifiers permanent; corrections do not overwrite; negative evidence equally permanent | Ledger Writer | `test_ledger_invariants` | candidate event | Specified |
| R-060 | RES §18 | Begin from `EH-0`, ledger tip `AR1-E000003` | Ledger Writer | `test_starts_from_canonical_tip` | candidate event | Specified |
| R-061 | THEORY (metadata) | Verify frozen-artefact digests at run start; abort on drift | Core | `test_frozen_artefact_drift_aborts` | run abort | Engineering decision |
| R-062 | Brief §12 | Deterministic outputs under identical inputs; declared byte-identical vs semantic-equivalence classes | Determinism | `test_byte_identical_replay` | replay report | Engineering decision |
| R-063 | Brief §13 | No authoritative output without a provenance chain terminating at registered dataset digests | Provenance | `test_no_result_without_provenance` | provenance DAG | Engineering decision |
| R-064 | Brief §14 | Classify every artefact; only `authoritative-scientific` may be cited as evidence | Result Generator | `test_artefact_classification` | run package | Engineering decision |
| R-065 | Brief §18 | No engine module imports a renderer | Architecture | `test_no_rendering_imports` | import graph | Engineering decision |

## 2. Coverage summary

| Status | Count |
|---|---|
| Specified — fully traceable to a frozen artefact | 48 |
| Ruling required — blocked on an open `UR` | 12 |
| Engineering decision — no scientific content | 5 |
| **Total** | **65** |

The twelve blocked requirements depend on: `UR-001` → R-037, R-039 · `UR-003` → R-014, R-031 · `UR-004` → R-006, R-007 · `UR-005` → R-024, R-033, R-034 · `UR-006` → R-011 · `UR-007` → R-032 · `UR-010` → R-035.

**74 % of engine requirements are fully specified today.** The blocked minority is concentrated in target ordering, the Gaia fit, and numerical tolerances — each narrow and answerable by a custodian ruling, none requiring new science except `UR-001`.

## 3. Reverse trace — no orphan behaviour

Every planned component maps to at least one requirement above. Components proposed by the programme brief that trace to **no** frozen requirement are **not built**, and are recorded as such:

| Brief component | Trace | Disposition |
|---|---|---|
| Standing Engine (§9.8) | none in `ASTRO-EXP-0001` | Not built — `UR-002` |
| Deterministic Significance Engine (§9.9) | no experiment counterpart; the estimator is the only scoring step | Interface only — `UR-001` |
| Relationship Graph (§9.6) | only the fixed 27×16 candidate structure | Reduced to Perturber Relation Set |
| Entity Manager (§9.5) | identity is the permanent minor-planet number | Thin, exact lookup only |
| Visualisation Interface (§9.16) | no experiment requirement | Read-only export boundary, Phase 9 |

This table exists so that a later reviewer can see these were **assessed and consciously scoped**, not forgotten.
