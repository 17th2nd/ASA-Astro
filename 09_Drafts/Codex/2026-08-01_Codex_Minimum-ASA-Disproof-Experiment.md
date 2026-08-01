# The Minimum ASA Disproof Experiment

Status: proposed preregistration; no result and no claim of validation

Date: 2026-08-01

## Decision

Run one blind **Gaia–DE440 perturber-selection challenge**.

ASA receives an observation-constrained Solar-System state and a declared prediction task. It must choose four of sixteen massive asteroid force terms to retain in a reduced dynamical model. A standard celestial-mechanics sensitivity calculation receives the same information and makes the same choice. Nonlinear counterfactual integrations then measure which choice preserves the full-model trajectory more accurately.

If ASA does not materially and consistently beat that baseline, stop the Astronomy Validation Programme.

This is the smallest fair experiment because it gives ASA the exact kind of problem on which it claims to matter—context-dependent allocation under relational evidence and uncertainty—while giving conventional astronomy its strongest cheap answer. Random ranking, mass-only ranking, degree centrality, PageRank, image processing, ontology recovery, explanation scoring, cosmological simulations, and expert judgement are not needed.

## The single claim under test

> Under an equal information set and a fixed four-perturber budget, ASA selects a reduced force model whose predicted target trajectory is more faithful to the full JPL-anchored model than a first-order variational-sensitivity selector.

This is an incremental claim. It does not ask whether ASA can reproduce Newtonian gravity. It asks whether ASA adds anything useful after ordinary celestial mechanics is already present.

The null hypothesis is:

> ASA has no practically important advantage over the variational selector.

Failure to reject that null ends the programme. A finite benchmark cannot refute every possible interpretation of ASA; it can decisively refute the programme's reason for asking astrophysicists to use it.

## Experimental system

### Observational constraint: Gaia

Use the frozen Gaia DR3 Solar System Object epoch-astrometry tables. Gaia DR3 supplies more than 23 million epoch observations for more than 150,000 Solar System objects, as well as orbit products for 154,741 asteroids. Its per-observation random and within-transit systematic covariance terms are published, so the experiment can propagate measurement uncertainty rather than invent it.

For each target, fit the initial state using the first 70% of its Gaia epochs in chronological order. Use the remaining 30% only as a pre-unblinding apparatus check. Construct 32 fixed posterior state draws using the published Gaia covariance model. Both ASA and the baseline receive the same fitted state distribution.

### Dynamical reference: JPL DE440

Use JPL DE440 for the Sun, Moon, and planetary ephemerides. Hold that background ephemeris fixed. Use the public JPL `SB441-N16` sixteen-massive-asteroid perturber set as the sixteen candidate direct force terms. The counterfactual is therefore precise:

> Set the direct acceleration of the target due to candidate asteroid \(p\) to zero while holding the DE440 background fixed.

This is a model-term counterfactual, not the claim that an asteroid can literally be removed from the historical Solar System. DE440 itself was produced by fitting numerically integrated orbits to observations and its full construction includes 343 asteroid perturbations plus Kuiper-belt terms. Those effects remain in the fixed background; only the sixteen selectable direct target-acceleration terms are varied.

Validate the nominal full-force trajectory against JPL Horizons at agreed reference epochs. Repeat a sample of integrations at ten-times tighter numerical tolerance. Any counterfactual effect not exceeding the resulting numerical floor is treated as zero.

### Targets: eight, selected without looking at ASA

Eight targets are the minimum useful test set. If ASA beats the baseline on all eight independent targets, a two-sided exact sign test gives \(p=0.0078125\) under equal win probability.

Build the eligible target pool before either method runs:

1. numbered Gaia DR3 asteroid, not one of the sixteen candidate perturbers;
2. at least 20 accepted Gaia field-of-view transits spanning at least 600 days;
3. no fitted non-gravitational term;
4. the full model passes the held-out Gaia residual check fixed below;
5. the difference between the full sixteen-perturber model and the zero-direct-asteroid model exceeds ten times the numerical floor over the twenty-year horizon.

Order eligible designations by `SHA256(frozen-public-seed || designation)` and take the first eight. If a target fails an apparatus gate, replace it with the next hash-ranked target before ASA outputs are opened. No replacement is permitted after unblinding.

The held-out Gaia gate is a reduced \(\chi^2\) interval fixed before data access by an independent orbit-dynamics reviewer. The reviewer may widen it only before target identities are drawn. If eight targets cannot pass, the apparatus is inadequate and the experiment is invalid—not an ASA failure.

## The context

Each target has two prediction contexts:

- barycentric target position over five years from the fitted epoch;
- barycentric target position over twenty years from the fitted epoch.

Each context has the same hard resource limit: retain exactly four of the sixteen candidate direct asteroid force terms. The target, observable, horizon, coordinate frame, epoch, candidate set, and budget are frozen and hashed before scoring.

Two horizons are retained because horizon is the smallest physically meaningful change of context. They are not scored as independent samples; both are combined into one result per target.

## The two selectors

### ASA

Treat ASA as a black box. It may consume the target and perturber states, masses, Gaia-derived uncertainty, encounter geometry, typed relationships, provenance, and the frozen context. It returns an ordered list of the sixteen perturbers.

ASA's scoring rule, parameters, data transformations, and executable hash must be frozen before the eight target identities are revealed. It may not consume any leave-one-out integration, future full-model trajectory, held-out Gaia residual, or quantity derived from them.

An abstention counts as failure for that target: the experiment concerns allocation under a hard budget, so ASA cannot obtain a good score by refusing to choose.

### Existing-method baseline

Use one strong baseline only: a tangent-linear variational calculation along the nominal full trajectory.

For each candidate perturber \(p\), propagate the first-order state response to scaling its direct acceleration from \(\lambda_p=1\) toward \(0\). Rank candidates by the predicted maximum target-position displacement over the declared horizon. This is the conventional physical answer obtainable from one nominal integration plus sensitivity equations. Its equations, tolerances, and ranking tie-break must be frozen with ASA.

Both selectors receive identical physical quantities. The baseline is not denied masses, distances, encounter epochs, frames, or uncertainties merely because ASA represents them as relationships.

## Blind counterfactual truth

The truth generator is separated from both selectors.

For every target, horizon, and one of the 32 Gaia posterior draws:

1. integrate the full model with all sixteen direct asteroid force terms;
2. run sixteen leave-one-perturber-out integrations;
3. record, for diagnosis, each perturber's maximum positional effect

   \[
   D_{t,h,q,p}=\max_{0\leq \tau\leq h}
   \left\|\mathbf r_{\mathrm{full}}(\tau)-
   \mathbf r_{-p}(\tau)\right\|;
   \]

4. for each selector, integrate the reduced model containing only its top four perturbers;
5. record the operational error

   \[
   E_m(t,h)=\operatorname{median}_{q=1}^{32}
   \max_{0\leq \tau\leq h}
   \left\|\mathbf r_{\mathrm{full},q}(\tau)-
   \mathbf r_{m,q}^{(4)}(\tau)\right\|,
   \]

   where \(m\) is ASA or the variational baseline.

The individual \(D\) values explain the outcome but do not replace the downstream test. The selected four-body model is evaluated directly, so nonlinear interactions and cancellation cannot be hidden by a ranking metric.

## One primary result

For each target define

\[
R_t=\sqrt{
\frac{E_{\mathrm{ASA}}(t,5\,\mathrm{yr})}
     {\max(E_{\mathrm{VAR}}(t,5\,\mathrm{yr}),\epsilon)}}
\frac{E_{\mathrm{ASA}}(t,20\,\mathrm{yr})}
     {\max(E_{\mathrm{VAR}}(t,20\,\mathrm{yr}),\epsilon)}}
},
\]

where \(\epsilon\) is the frozen numerical-convergence floor.

Interpretation is direct:

- \(R_t<1\): ASA selected the better reduced force model for target \(t\);
- \(R_t=1\): no contribution;
- \(R_t>1\): the existing method was better.

Do not promote rank correlation, explanation quality, or context sensitivity to co-primary endpoints. They may diagnose a result but cannot rescue a failed operational comparison.

## The preregistered decision rule

ASA earns a bounded positive result only if all of the following hold:

1. \(R_t<1\) by more than the numerical floor for all eight targets;
2. the median \(R_t\leq0.80\), meaning at least a 20% median reduction in trajectory error relative to the standard selector;
3. ASA's selection step uses no more wall time than the variational selection step on the frozen hardware;
4. all data, code, target substitutions, exclusions, and negative results are released.

Everything else is failure, including a tie, improvement on seven of eight targets, an improvement smaller than 20% in the median, success obtained with greater selection cost, or any post-unblinding change.

If it fails, record:

> On a deliberately ASA-favourable, observation-constrained, context-dependent perturber-allocation task with exact within-model counterfactual outcomes, ASA did not improve on standard variational sensitivity. No empirical astronomy contribution has been demonstrated. The Astronomy Validation Programme is terminated.

No second catalogue, revised context, new weighting rule, or broader simulation programme follows the failure. A new programme would require a different independently motivated claim, not a repair of this benchmark.

## What would convince an astrophysicist

A pass would show one concrete thing: at equal information, equal retained-force budget, and no greater selection cost, ASA repeatedly chose force terms that preserved an independently generated nonlinear trajectory materially better than the ordinary sensitivity method.

That would be a bounded computational-astronomy contribution worth investigating. It would not prove ASA, validate a general theory of significance, or show that graph reasoning improves physics. It would justify exactly one statement:

> ASA improved perturber allocation in this frozen Gaia–DE440 benchmark.

The strength of the experiment is also why failure is terminal. The target pool is real, uncertainty comes from real Gaia astrometry, the dynamical background is JPL's, the outcome is numerical rather than subjective, the contexts are physical, and the comparison is against the method an orbital dynamicist would actually use.

## What is deliberately excluded

- no single-image demonstration;
- no Gaia cluster catalogue;
- no cosmological simulation;
- no PageRank, degree, random, mass-only, or inverse-distance straw baseline;
- no proof that ASA recovers known physics;
- no expert significance labels;
- no architectural conformance score;
- no explanation or provenance score as a substitute for prediction;
- no further experiment if the decision rule is missed.

## Public source basis

- [JPL, *The JPL Planetary and Lunar Ephemerides DE440 and DE441*](https://ssd.jpl.nasa.gov/doc/de440_de441.html): DE440/DE441 construction and observational fit.
- [JPL DE440 paper](https://ssd.jpl.nasa.gov/doc/Park.2021.AJ.DE440.pdf): integrated body set, including the asteroid and Kuiper-belt treatment.
- [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/): public high-accuracy ephemeris service used for nominal checks.
- [ESA Gaia DR3 Solar System survey](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_cu9pvp/sec_cu9pvp_solsyst/): SSO observation and orbit-product scope.
- [ESA Gaia DR3 astrometric error model](https://gea.esac.esa.int/archive/documentation/GDR3/Data_analysis/chap_cu4sso/sec_cu4sso_processingsteps/ssec_cu4sso_astrometryerrormodel.html): random and within-transit systematic covariance construction.
- [ASSIST: an ephemeris-quality test-particle integrator](https://arxiv.org/abs/2303.16246): a public route for DE440/441-class force-model and variational integrations. The experiment is not tied to this implementation if an equivalent independently reviewed integrator is used.

---

This document specifies the experiment. It does not presuppose that ASA survives it.
