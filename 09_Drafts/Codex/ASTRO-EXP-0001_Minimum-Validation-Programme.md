# ASTRO-EXP-0001 — Minimum Validation Programme

**Programme under test:** ASTRO-RESEARCH-0003  
**Status:** proposed preregistration  
**Purpose:** decide whether the research programme survives  
**Number of experiments:** one

## Reduction

Only an observed advantage over an existing scientific method can justify continuing the programme.

Structural recovery is excluded because catalogues already recover astronomical structure. Context switching is excluded as a separate experiment because a context-sensitive result has no value if its physical estimate is poor. Abstention, provenance, composition rules, selection correction and explanation quality are excluded as separate experiments because they are mechanisms, not scientific outcomes. PageRank, random ranking, mass-only ranking and image-derived ranking are excluded because beating weak comparators would not persuade an astrophysicist. Multiple domains are excluded because failure in the cleanest domain is already terminal.

One experiment remains.

---

## Experiment 1 — Blind counterfactual perturbation estimation

### Question

Does ASA estimate the dynamical importance of a perturbing body more accurately than standard variational perturbation analysis?

This is the only question.

### Experimental system

- Eight small bodies selected prospectively from the Gaia DR3 Solar System Object catalogue.
- Sixteen massive asteroid perturbers from the JPL perturber set.
- JPL DE440 as the fixed planetary and lunar dynamical background.
- One withdrawal: set one perturber's direct gravitational contribution to the target to zero.
- One observable: maximum geocentric sky-position displacement over twenty years.
- One unit: milliarcseconds.
- One comparator: first-order variational perturbation analysis.

The eight targets are selected without reference to ASA output or counterfactual results. They must have sufficient Gaia epoch astrometry to constrain an orbit, no fitted non-gravitational acceleration, and a detectable total response to the candidate perturber set. Eight is the minimum number permitting an all-target superiority result to cross a two-sided exact sign-test threshold of 0.01: eight wins from eight gives \(p=0.0078125\).

ASA and the comparator receive the same target state, perturber states, masses, observational uncertainties, reference frame, epoch and twenty-year prediction question. Neither receives a counterfactual result.

### Hypothesis

For previously unseen Gaia targets, ASA's predicted counterfactual displacement is both absolutely accurate and more accurate than the variational estimate.

For target \(t\), define the median factor-error score

\[
L_m(t)=\operatorname{median}_{p}
\left|\log_{10}
\frac{\widehat{\Delta}_{m}(t,p)+\epsilon}
     {\Delta_{\mathrm{true}}(t,p)+\epsilon}
\right|,
\]

where \(m\) is ASA or the variational comparator and \(\epsilon\) is the independently measured numerical floor. Lower is better. A score of \(\log_{10}2\) is a median factor-of-two error.

### Null

ASA is no more accurate than variational perturbation analysis, or ASA's absolute error is too large to be scientifically useful.

Formally, the null survives if either:

- \(L_{ASA}(t)\geq L_{VAR}(t)\) for any target; or
- the median ASA error across targets exceeds a factor of two.

### Ground truth

For every target and perturber:

1. propagate the target for twenty years in the full JPL-anchored dynamical model;
2. repeat with that perturber's direct gravitational contribution set to zero;
3. measure

   \[
   \Delta_{\mathrm{true}}(t,p)=
   \max_{0\leq\tau\leq20\,\mathrm{yr}}
   \operatorname{angular\ separation}
   \left[\mathbf r_{full}(\tau),\mathbf r_{-p}(\tau)\right].
   \]

Gaia astrometric uncertainties are propagated through repeated draws of the target's admissible initial state. The reported truth is the median counterfactual displacement, with its uncertainty interval.

This is exact ground truth only within the declared dynamical model. It is not metaphysical truth and it is not evidence that DE440 is complete.

Before unblinding, the full model must reproduce held-out Gaia astrometry within the preregistered residual bound, agree with JPL Horizons at reference epochs, and remain stable when numerical precision is tightened. Failure of these checks invalidates the apparatus; it does not count for or against ASA.

### Failure condition

ASTRO-RESEARCH-0003 fails if any one of the following occurs:

1. ASA fails to beat the variational comparator on even one of the eight targets.
2. ASA's median improvement over the comparator is less than 20%.
3. ASA's median absolute error exceeds a factor of two.
4. ASA abstains on any target or perturber above the numerical floor.
5. A target, threshold, observable, horizon or exclusion is changed after either prediction set is revealed.

A tie is failure. Seven wins from eight is failure. Good ranking with bad effect-size estimation is failure. Explanations, auditability or provenance cannot reverse failure.

### Success condition

ASTRO-RESEARCH-0003 survives only if all of the following are true:

1. \(L_{ASA}(t)<L_{VAR}(t)\) for all eight targets.
2. The median reduction in factor-error is at least 20%.
3. The median ASA estimate is within a factor of two of counterfactual truth.
4. The result survives the Gaia uncertainty draws and the numerical-convergence check.
5. All outcomes, including the worst target and every failed prediction, are reported.

Success establishes only this:

> ASA estimated leave-one-perturber dynamical effects better than standard first-order variational analysis in the frozen Gaia–DE440 experiment.

It does not establish general validity, discovery capability or usefulness outside this problem.

### Expected criticism

**“The ground truth is simulated.”** Correct. The result is truth conditional on DE440-class dynamics. Real intervention on a Solar System body is unavailable. This is why the conclusion is bounded.

**“Variational analysis is an unusually strong comparator.”** Correct. A weaker comparator would not answer whether ASA contributes beyond existing astronomy.

**“Eight targets are too few for generalisation.”** Correct. Eight is not intended to establish generality. It is the smallest sample capable of yielding a stringent all-target result. Failure is decisive; success only warrants further testing.

**“The Solar System is too simple or too physics-dominated for ASA.”** This is the programme's most favourable source of quantitative counterfactual truth. If ASA requires a domain where its target cannot be measured, the claim is not experimentally testable.

**“Gaia and JPL are not wholly independent.”** Correct. Gaia constrains the target state; JPL defines the dynamical reference. They are not presented as two independent confirmations.

### Cost

- Data access: no charge; Gaia, DE440 and Horizons are public.
- Experimental labour: approximately four to six scientist-weeks, including independent review.
- Computation: approximately 5,000 short N-body propagations, including uncertainty draws and convergence repetitions.
- Expected marginal compute cost: below AUD 2,000.
- Expected contracted total, including scientific labour and review: AUD 20,000–40,000.

### Duration

Four to six weeks from preregistration to signed result.

No extension is permitted to improve an unfavourable result.

---

## Programme decision

- **Apparatus invalid:** repair only the failed measurement apparatus and repeat the identical preregistered experiment once.
- **Experiment fails:** terminate the Astronomy Validation Programme.
- **Experiment succeeds:** ASTRO-RESEARCH-0003 survives provisionally and earns one independent replication. No broader claim is authorised.

There is no Experiment 2 in the Minimum Validation Programme.
