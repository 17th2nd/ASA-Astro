# ASTRO-EXP-0001 — Minimum Validation Programme

## Document control

| Field | Value |
|---|---|
| Identifier | `ASTRO-EXP-0001` |
| Title | Minimum Validation Programme |
| Version | `1.0` — Version 1 freeze |
| Status | Frozen canonical protocol; not yet executed |
| Effective date | 2026-08-01 |
| Scope | One cross-context perturber-selection experiment; one primary endpoint; one terminal programme rule |
| Authority boundary | Governs only this experiment. It cannot authorize broader ASA, mathematical-novelty, graph-novelty, astronomy, or general-validity claims. |
| Tested claim | [`ASTRO-CLM-0070`](../../docs/claims/ASTRO-CLAIMS-0001.md#astro-clm-0070) |
| Statistical null | [`ASTRO-CLM-0071`](../../docs/claims/ASTRO-CLAIMS-0001.md#astro-clm-0071) |
| Terminal negative claim | [`ASTRO-CLM-0072`](../../docs/claims/ASTRO-CLAIMS-0001.md#astro-clm-0072) |
| Programme dependency | [`ASTRO-RESEARCH-0003`](../../09_Drafts/Claude/2026-08-01_Claude_ASTRO-RESEARCH-0003-Convergence-Architecture.md) |
| Results ledger | [`ASTRO-RESULTS-0001@1.0`](../results/ASTRO-RESULTS-0001.md) |
| Supersession state | Supersedes every earlier `ASTRO-EXP-0001` draft; earlier drafts are historical evidence only. |
| Canonical location | `validation/benchmarks/ASTRO-EXP-0001.md` |
| Verification status | Verified for Version 1 freeze by [`ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT`](../../reports/ASTRO-V1-RESEARCH-CONTROLS-FREEZE-REPORT.md) |
| Execution state | Experiments executed: `0`; empirical results: `0`; evidence level: `EH-0` |

**Decision:** one experiment, one remaining empirical question, one terminal rule.

This protocol supersedes every earlier ASTRO-EXP-0001 draft. Earlier proposals are historical evidence only and have no authority over target selection, analysis or claims.

## Purpose

Determine whether one fully specified ASA estimator, frozen after work on one asteroid population, transfers to a different asteroid population and selects a materially better reduced dynamical model than direct physical perturbation analysis.

This is the only unresolved scientific question. Mathematical novelty, graph novelty, composition rules, provenance, explanations, abstention and general architectural value are not tested. No result from those subjects can rescue failure here.

The programme contains one experiment because one experiment can answer the remaining question. Nothing else is authorised.

## Scientific hypotheses

For a deployment target, define a **material ASA win** as a reduction of at least 20% in the primary trajectory-error measure relative to the comparator, beyond the numerical resolution of the experiment.

### Hypothesis H1 — ASTRO-CLM-0070

A frozen ASA estimator transfers from Gaia DR3 main-belt asteroids to held-out Gaia DR3 near-Earth asteroids and produces material wins on at least 20 of 27 deployment targets.

### Statistical null H0 — ASTRO-CLM-0071

The probability of a material ASA win is at most one half in the declared deployment population.

Operationally, H0 is not rejected and `ASTRO-CLM-0070` is not demonstrated if ASA records 19 or fewer material wins among the 27 deployment targets. A tie, abstention or missing selection is not a win.

## The single experiment

Each target is a test particle in a fixed JPL dynamical environment. The candidate removable terms are the direct gravitational accelerations from the 16 massive asteroids in JPL `SB441-N16`. The Sun, Moon, planets, Pluto, relativistic terms and all ephemeris states supplied by JPL DE440 remain fixed and are never candidates for removal.

Both methods must retain exactly four of the 16 asteroid terms for a 20-year propagation:

1. **ASA:** the single estimator frozen at the end of calibration.
2. **Comparator:** direct leave-one-perturber-out finite perturbation. For each candidate asteroid, remove only that asteroid's direct acceleration from the full model, measure the resulting 20-year displacement, and retain the four candidates with the largest individual effects.

For comparator candidate $j$, the individual effect is

\[
L_j(t)=\operatorname{median}_{q}\max_k
\left\|\mathbf r_{full,q}(t_k)-\mathbf r_{-j,q}(t_k)\right\|.
\]

Rank candidates by decreasing $L_j(t)$ and break an exact tie by increasing permanent number. This comparator has no fitted parameter.

Both methods have the same frozen Gaia and JPL physical inputs. Neither may use the error of any four-perturber deployment model before its selection is sealed. Computational effort is not equalized: a new method must beat the established physical analysis, not merely be cheaper than it.

The comparator is retained because it is the smallest strong, physics-native existing method. It measures the declared counterfactual directly and is more probative than PageRank, mass, distance or random rankings. No weaker comparator is part of the confirmatory experiment.

## Primary endpoint

Let $t$ index a deployment target, $q=1,\ldots,32$ index fixed draws from its Gaia state posterior, and $k=0,\ldots,7305$ index daily epochs from 2017-07-01 00:00 TDB through 2037-07-01 00:00 TDB.

For method $m\in\{ASA,LOO\}$, let

\[
E_m(t)=\operatorname{median}_{q}
\max_k
\left\|
\mathbf r_{full,q}(t_k)-\mathbf r^{(4)}_{m,q}(t_k)
\right\|,
\]

where `full` retains all 16 asteroid terms and $m^{(4)}$ retains the four selected by method $m$. Positions are barycentric ICRF3 positions and errors are reported in kilometres.

Before unblinding, the truth laboratory establishes a target-specific numerical resolution $\delta_t$ by repeating the full and two selected-model propagations with tightened numerical accuracy. It sets $\delta_t$ to three times the largest change in either $E_m(t)$ caused by that tightening.

Target $t$ is a material ASA win exactly when

\[
E_{ASA}(t)+\delta_t \leq 0.80\,E_{LOO}(t).
\]

The primary endpoint is

\[
W=\sum_{t=1}^{27}
\mathbf 1\!\left[
E_{ASA}(t)+\delta_t\leq0.80E_{LOO}(t)
\right].
\]

The experiment succeeds if and only if $W\geq20$.

## Secondary endpoints

None.

All continuous error ratios, target-level errors, numerical resolutions and comparator rankings must be published, but they are descriptive diagnostics. They cannot change, qualify or rescue the primary decision.

## Success and failure conditions

A valid first run succeeds only when $W\geq20$. It then earns the independent replication specified below; it does not establish a general ASA claim.

A valid first run fails when $W\leq19$. That result is terminal. No diagnostic, explanation, calibration score or alternative analysis can convert it into survival.

## Ground truth

Ground truth is simulated dynamical response within the declared model, not astronomical truth in nature.

For each target and posterior draw, the truth laboratory performs:

1. one full 16-perturber propagation;
2. 16 single-deletion propagations used only to construct the comparator ranking;
3. one propagation retaining the four ASA selections;
4. one propagation retaining the four comparator selections.

The intervention on candidate $j$ is exact and singular:

\[
\mathbf a_j=
GM_j\frac{\mathbf r_j-\mathbf r}{\|\mathbf r_j-\mathbf r\|^3}
\quad\longrightarrow\quad
\mathbf 0.
\]

No other force, state, mass, observation, epoch or uncertainty is altered. The selected four-term models are evaluated directly so nonlinear interaction and cancellation remain in the endpoint.

The common force model uses Newtonian point-mass accelerations from the Sun, Moon, eight planets, Pluto and the `SB441-N16` asteroids, with their states and gravitational parameters fixed from DE440 and `SB441-N16`. Every propagation includes the same first post-Newtonian Einstein–Infeld–Hoffmann correction with PPN parameters $\beta=\gamma=1$. Nongravitational accelerations are excluded. This defines model-conditional ground truth and bounds every permitted claim.

The full Gaia fit produces a six-dimensional state mean $\hat{\mathbf x}_t$ and covariance $C_t$ at the common start epoch. Let $L_tL_t^T=C_t$, where $L_t$ is the unique lower-triangular Cholesky factor with positive diagonal. For the second through thirty-third points $\mathbf u_q$ of the standard six-dimensional Sobol sequence, define

\[
\mathbf x_{t,q}=\hat{\mathbf x}_t+L_t\Phi^{-1}(\mathbf u_q),
\]

where $\Phi^{-1}$ is applied componentwise. These 32 state vectors and their unit-cube source points are published in the frozen manifest before either deployment selection. The same vectors are used for the full, comparator and ASA propagations.

Gaia's TCB-tagged observations are converted to TDB with the IAU TCB–TDB transformation before fitting. All integrations and daily evaluation epochs use TDB; all reported positions use barycentric ICRF3 axes.

## Datasets

Only these sources are permitted:

- [Gaia DR3 Solar System Object data](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_cu9pvp/sec_cu9pvp_solsyst/): `gaiadr3.sso_observation`, `gaiadr3.sso_source` and the DR3 auxiliary orbit solution;
- the [Gaia DR3 SSO astrometric error model](https://gea.esac.esa.int/archive/documentation/GDR3/Data_analysis/chap_cu4sso/sec_cu4sso_processingsteps/ssec_cu4sso_astrometryerrormodel.html), including random and within-transit systematic components;
- [JPL DE440](https://ssd.jpl.nasa.gov/doc/de440_de441.html) for the fixed planetary and lunar ephemeris;
- JPL [`SB441-N16`](https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/SB441_IOM392R-21-005_perturbers.pdf) for the 16 asteroid trajectories and gravitational parameters;
- [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) only for the apparatus check described below.

Before target selection, the protocol custodian freezes a manifest containing every source locator, retrieval time, release identifier and cryptographic digest. A later data release or revised JPL orbit must not be substituted.

## Target population and selection

The experimental unit is one asteroid. Posterior draws are repeated measurements, not independent units.

An object is eligible only if it:

1. has a permanent minor-planet number and Gaia DR3 SSO observations;
2. is not one of the 16 candidate perturbers;
3. has at least 20 Gaia field-of-view transits spanning at least 600 days;
4. has no declared cometary activity or fitted nongravitational parameter;
5. passes every apparatus check below.

Population is assigned from the Gaia DR3 osculating orbit:

- **Calibration main belt:** $2.0\leq a\leq3.5$ au and perihelion $q\geq1.7$ au.
- **Deployment near Earth:** perihelion $q<1.3$ au.

Order calibration candidates by the hexadecimal SHA-256 digest of `ASTRO-EXP-0001-CAL-v1 | number`, where `number` is the decimal permanent number without leading zeroes.

The independent statistician generates one uniformly random 256-bit deployment salt only after the ASA estimator is frozen. The salt is generated once in a witnessed ceremony, published immediately and never redrawn. Order deployment candidates by the hexadecimal SHA-256 digest of `salt | ASTRO-EXP-0001-DEP-v1 | number`.

In each population, take the first 27 apparatus-valid objects. The next ten are ordered reserves. The calibration order is fixed in advance; the deployment order is unknowable to the ASA laboratory before freezing and exactly reproducible after the salt is published. No seed or salt may be searched for a favourable target set.

### Apparatus checks

Checks are completed before either method's deployment selections are opened:

1. Fit the full dynamical model to the chronologically first 70% of the Gaia transits. Its predictions for the final 30% must have reduced $\chi^2$ between 0.5 and 2.0 under the published Gaia covariance model.
2. At the start, midpoint and end epochs, the major-body and candidate-asteroid states used by the experiment must agree with the frozen JPL Horizons vectors to within 1 km after reference-frame and time-scale conversion.
3. The maximum 20-year displacement between the full model and a model omitting all 16 asteroid terms must exceed 100 times the numerical integration floor.
4. Repeating the full propagation at tightened numerical accuracy must not change any daily position by more than one hundredth of the all-asteroid displacement in check 3.

A failed check excludes the object before unblinding. It is replaced by the next reserve. Exclusions and all check values are published.

## Calibration environment

The 27 main-belt targets are open. The ASA laboratory may use their Gaia observations, the frozen JPL inputs and any simulations derived from those inputs. It may revise the ASA estimator during calibration.

Calibration has no endpoint and yields no evidence of transfer. It ends when the laboratory deposits a complete scientific specification of one estimator, all fitted quantities, its transformation from the permitted inputs to four selections, and a cryptographic digest of that frozen specification.

After deposit, no rule, parameter, threshold, feature, physical input or preprocessing choice may change. Failure to specify a deterministic four-selection result for every admissible deployment input is failure to freeze and ends the experiment.

## Deployment environment

The 27 near-Earth targets are disjoint from calibration. They use the same candidate set, force model, four-term budget, posterior construction, start epoch, duration and endpoint.

The frozen ASA estimator receives only the inputs declared at calibration. It must return exactly four distinct `SB441-N16` identifiers for every target. It may not be refitted, recalibrated or supplemented with target-specific judgement.

The distribution shift is therefore one change only: main-belt calibration objects become near-Earth deployment objects.

## Blind protocol

The decisive blind is outcome blinding. Target identity masking is used administratively but is not treated as secure because public orbital data may permit re-identification.

Four roles are separated:

1. **Protocol custodian:** freezes the data manifest, calibration targets, target rule and estimator digest.
2. **ASA laboratory:** calibrates, freezes and submits four selections per anonymous deployment record.
3. **Truth laboratory:** constructs and seals the posterior states, full trajectories, 16 single-deletion trajectories, comparator selections and comparator errors before receiving ASA's selections.
4. **Independent statistician:** receives the two sealed archives, verifies their timestamps and computes the prespecified endpoint.

After the estimator is frozen, the statistician generates the single deployment salt and the custodian applies the published target rule. The comparator archive and all counterfactual outcomes remain hidden from the ASA laboratory until its 27 selections are sealed. The truth laboratory then runs only the ASA-selected reduced models at the two predeclared numerical accuracies; it may not alter any earlier input, comparator result, tolerance or trajectory. The statistician opens the completed archives once. There is no interim look.

## Stopping rules

1. Stop before deployment if the ASA estimator is not completely frozen.
2. Stop without a scientific result if fewer than 27 deployment targets and ten reserves can be formed. The programme does not survive; a smaller post hoc sample is forbidden.
3. Before unblinding, replace an apparatus-invalid target only with the next ordered reserve.
4. After unblinding, do not replace, exclude or relabel any target.
5. Count an abstention, duplicate, invalid identifier or missing ASA submission as a non-win.
6. Stop the utility programme immediately if $W\leq19$. No reformulation or second deployment on the same hypothesis is permitted.
7. If $W\geq20$, stop development and proceed only to the independent replication specified below.

## Failure classification

| Class | Definition | Consequence |
|---|---|---|
| F0 — infeasible apparatus | The required target pool or stable physical measurement cannot be produced before unblinding. | `FAILED_EXPERIMENT`; no scientific effect is estimated; ASTRO-RESEARCH-0003 does not survive. |
| F1 — integrity failure | Outcome leakage, unequal undeclared inputs, an unfrozen ASA change, post-unblind exclusion or protocol deviation affects the endpoint. | `INVALID` if a result was recorded, otherwise `FAILED_EXPERIMENT`; publish the breach; ASTRO-RESEARCH-0003 does not survive. |
| F2 — scientific failure | A valid run gives $W\leq19$. | `NEGATIVE`; do not reject `ASTRO-CLM-0071`; record `ASTRO-CLM-0072`; end the ASA utility programme. |
| F3 — replication failure | The first run succeeds but the required independent replication does not. | Record the replication as `INCONSISTENT` or `FAILED_EXPERIMENT` as applicable; withdraw the bounded transfer claim and end the ASA utility programme. |

Only F2 is evidence that the frozen estimator failed the scientific comparison. F0 and F1 are not evidence of equivalence, but they do not authorise another, easier benchmark.

## Statistical analysis

The 27 deployment targets are the only independent observations. All 32 posterior draws are collapsed inside each target-level endpoint.

Under H0, the exact one-sided probability of 20 or more wins is

\[
P\{X\geq20\mid X\sim\operatorname{Binomial}(27,0.5)\}
=0.0095786452293396.
\]

Thus $W\geq20$ rejects H0 at one-sided $\alpha<0.01$. With a true material-win probability of 0.80, this rule has power `0.8444402928110182`. Exhaustive binomial-tail enumeration confirms that 27 targets with a 20-win threshold is the smallest integer sample-and-threshold pair providing both one-sided $\alpha<0.01$ under $p=0.5$ and power above `0.80` under $p=0.8$.

There is one hypothesis, one endpoint and no multiplicity adjustment. No imputation is permitted. Ties count against ASA. The statistician reports $W$, the exact binomial p-value, every $E_{ASA}$, $E_{LOO}$, $\delta_t$, and every ratio $E_{ASA}/E_{LOO}$.

The threshold is deliberately asymmetric. ASA must demonstrate a large and repeated benefit; approximate equality is programme failure.

## Replication requirements

An initial success is provisional. One independent laboratory must repeat the protocol with:

- the identical frozen ASA estimator;
- no recalibration using deployment outcomes;
- a new, independently generated one-time salt and the first 27 apparatus-valid near-Earth objects it orders after excluding the first deployment set;
- an independently constructed truth archive;
- the same comparator, endpoint, 20% materiality threshold and $W\geq20$ rule.

The independent laboratory must reproduce the first run's target-level errors within the registered numerical resolutions before opening the replication outcomes. The transfer result is replicated only if the second run also gives $W\geq20$. No pooled rescue analysis is permitted.

## Publication policy

This protocol and the frozen source manifest are public before deployment outcomes are generated. After the single unblinding, publish regardless of result:

- calibration and deployment target numbers;
- the one-time deployment salt and witnessed generation record;
- the ordered eligibility and exclusion record;
- the frozen ASA scientific specification and digest;
- both sealed selection archives;
- posterior-state definitions and all target-level truth outputs;
- numerical convergence checks;
- the complete prespecified analysis;
- every deviation, failure and adverse result.

Negative results receive the same permanent record as positive results. No target, ratio or criticism may be suppressed. Public announcement of a general ASA advantage is forbidden before successful independent replication.

## Permitted claims

After one valid success, the maximum claim under `ASTRO-CLM-0070` is:

> In ASTRO-EXP-0001, this frozen ASA estimator transferred from the declared Gaia DR3 main-belt calibration environment to the declared Gaia DR3 near-Earth deployment environment and reduced 20-year four-perturber trajectory error by at least 20% relative to direct leave-one-perturber-out selection on at least 20 of 27 targets.

After a successful independent replication, the words “and this result replicated on a non-overlapping sample under the same protocol” may be appended.

After any terminal failure, the required claim under `ASTRO-CLM-0072` is:

> ASTRO-EXP-0001 did not demonstrate a material cross-context advantage for ASA. The remaining ASA utility claim is terminated.

## Forbidden claims

No outcome authorises a claim that:

- ASA is proved, true, generally valid or scientifically necessary;
- ASA contains novel mathematics, graph theory, causal theory or physics;
- ASA beats DE440, JPL, Gaia, orbit determination or astronomy;
- simulated model truth is truth in nature;
- the result generalises beyond the frozen estimator, target populations, force model, horizon, candidate set or four-term budget;
- provenance, explanation, abstention, composition or governance caused the result unless separately randomized;
- ASA discovers astronomical objects, causes or physical laws;
- failure can be rescued by a new endpoint, weaker comparator, different target set or architectural interpretation.

## Expected criticism and scope

**“The truth is simulated.”** Correct. The experiment measures model reduction under a declared JPL dynamical model. It makes no claim about missing forces or nature beyond that model.

**“The comparator is expensive.”** Correct. Direct finite perturbation is used because beating a weak heuristic would not establish additional value.

**“Twenty-seven targets are not all asteroids.”** Correct. The claim is bounded to the sampled Gaia DR3 populations. The sample is only large enough for the terminal decision specified here.

**“A different ASA might work.”** Possibly, but that is a new programme. This protocol decides the only frozen estimator submitted to it.

## Cost and duration

Public data have no acquisition charge. The confirmatory deployment requires approximately 20,000 twenty-year test-particle propagations including posterior draws and convergence checks, plus independent orbital-dynamics and statistical review. The expected measurement cost is AUD 30,000–60,000, excluding prior ASA development. Duration is six to eight weeks after the ASA estimator is frozen.

## Final programme rule

There is no Experiment 2.

If the valid first run gives $W\leq19$, end the programme. If the first run gives $W\geq20$ but independent replication fails, end the programme. Only two consecutive successes under this frozen protocol permit the bounded replicated claim above.
