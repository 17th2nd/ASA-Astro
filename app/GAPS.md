# ASA-Astro V1 application — gaps and dependencies

Recorded by Operator D (Application/UX) on the thin slice. Each gap is something the app does **not** fake;
the UI shows the limitation or derives only from existing fields with a source link.

## Pin / adapter (Operator A pin, adapter compat-gate lane)

- **G-PIN-1 — locator default is still the historical pin (resolved for the app).** At `633f837a` the locator
  hard-coded `config/asa-baseline.json` (b855d4c); with `.asa/ASA` at c2ccd7d every `import astro.asa.adapter` raised
  `AsaBaselineUnavailable`. `a200dda` added `ASTRO_ASA_BASELINE_CONFIG` / `ASTRO_ASA_PIN_KIND=current_dev`; the app now
  sets `ASTRO_ASA_BASELINE_CONFIG` to the pin file (`app/pin.py`) — no monkeypatching. Still open for the pin owner:
  the default remains historical, so `tests/astro` run without the env var still fail to import (see report).
- **G-PIN-2 — adapter RP-9 (tip native; app residual shim).** Tip adapter sets `GOVERNOR_ACTOR=asa:uao:asa.core/governor-v1`
  distinct from propose proposer `asa:uao:astro/adapter` (SPEC-0001 RP-9). The thin-slice app still applies its
  pre-tip `app/compat.py` shim (`asa:uao:astro/proposer`) on every run — honesty of the path taken, not a claim
  that tip lacks RP-9; digest therefore still reflects the shim. Pin semantics unchanged (current_dev / c2ccd7d).
  Compat-gate / Assurance still owns accepting removal of the residual shim.
- **G-PIN-3 — declared vs reported kernel version.** The pin file declares `kernel_version: unreleased-remediation-133`;
  the kernel reports `0.1.0-alpha13`, status `ENGINEERING ALPHA — NOT RATIFIED`. Shown as an unknown.
- **G-PIN-4 — pin status.** The pin is `CURRENT DEVELOPMENT COMPATIBILITY PIN — NOT A FROZEN FINAL V1`. Shown as an unknown.

## Significance / pipeline lane (what the app needs produced)

- **G-SIG-0 — WCS / crossmatch / residuals / bridge (Significance FROZEN on tip `b785f22`).**
  Tip artefacts: `process_observation` always writes `sky_localisations.json` (unavailable if no WCS), optional
  `wcs_solution.json` / `catalogue_crossmatches.json`; `asa_astro.residuals` emits residuals / missing_expected /
  next_evidence_recommendations / action_ui; `asa_astro.bridge` sky→Objective keeps entities as hypothesis.
  **App upload bar (Operator D):** accept image/FITS → content-addressed preserve under `app/var/uploads/` → invoke
  `process_observation` when Pillow-decodable → project `observation_evidence.present=true` when bundle artefacts
  exist → project Action residual fields present-only → still run thin Objective path (synthetic universe) for the
  primary receipt. Honesty: never established from this slice; null sky when unavailable; no invented values;
  matched only if evidence_qualified. JSON-only runs (no upload) still have `observation_evidence.present=false`.
  Receipt verification is **not** blocked on missing WCS.
- **G-SIG-1 — image → Objective universe bridge is the primary app receipt for uploads (R1).** Tip `9c2157a`
  exports `asa_astro.bridge.observation_bundle_to_objective` (Runtime handoff A). Upload + successful
  `status=localised` rows → primary Objective via that API (never silent `data/universe/slice1.json`).
  Upload + fail-closed (no WCS / no localised rows / missing bundle) → error/honesty; no silent synthetic.
  No-upload / explicit `demo=True` → `slice1.json` OK, labelled `synthetic/demo` in `view.universe_provenance`.
  `view.json` records bridge path, universe_id, data_class, source sha, and observation claim ids when present.
- **G-SIG-2 — no dedicated "next evidence" record.** The receipt carries a plan (selected actions) and failed eligibility
  rules; the app lists those, labelled hypothesis, with source pointers. A pipeline-produced next-evidence record (what to
  collect, why, expected effect on the objective) is needed for anything richer. The store-backed frontier
  (`lacks-evidence` relationships) exists for the real-catalogue store but is not part of this slice's universe.
- **G-SIG-3 — no plain-language explanation record.** The receipt carries `astro.significance.explain` lines
  (`why_significant_now`, `why_not_more`). The app's summary sentences are fill-in templates over cited receipt fields
  only. A pipeline-owned narrative explanation is not produced.
- **G-SIG-4 — no "established" path in this slice.** With a `synthetic` universe every claim is a hypothesis by policy.
  A real-data universe (store build) and an agreed definition of "established" from Assurance are needed before the
  `established-in-ASA-state` label can ever appear; even then it is not empirical validation.
- **G-SIG-5 — no calibrated confidence.** Scores are Astro-derived under a declared weighting policy; the app never shows
  a confidence number the pipeline does not emit.


- **G-SIG-6 — local-linear CD ≠ spherical FITS TAN (F-SCI-02).** Declared-WCS localisation
  (`src/asa_astro/evidence/wcs.py` `pixel_to_sky`) applies a local flat-sky CD matrix only
  (`sky ≈ CRVAL + CD · (pixel − CRPIX)`). It is **not** a spherical TAN/SIP projection.
  Measured residual vs FITS TAN on Assurance IN-07 can reach ~6.57″. Treat projected RA/Dec as
  **computational hypotheses** with standing `image-space-projection-hypothesis` /
  `projection_model=local-linear-CD`. Disclosed here and in README; primary localisation UI text
  must not present RA/Dec-only ICRS copy (F-SCI-01).
- **G-SIG-7 — observation claim identity ≠ Objective RCPT (F-SCI-03).** Thin Objective
  `receipt_id` does not bind upload source/metadata digests. App `run_id` isolates storage only.
  Scientific observation-claim identity is pipeline `observation_identity` when present:
  `binding`, `source_sha256` + `metadata_sha256` + `wcs_digest`, and primary
  `observation_claim_digest` / `observation_claim_id` (`obsclaim-…`). UI/docs forbid citing
  bare RCPT for observation artefacts and surface filename/`__src-`/`__meta-`/full `run_id`
  as navigation discriminators when the claim id is absent.
- **G-SIG-8 — INT-0015 morphology strings (F-SCI-05).** Tip pipeline emits image-region
  `candidate_type` names (e.g. `compact_high_peak_image_region`, `separate_extended_image_region`).
  Older on-disk bundles may still contain provisional morphology labels such as
  `likely_foreground_point_source`, `background_extended_object`, `possible_companion_object`.
  These are **not** app scientific outputs and are **not** linked from the thin-slice UI.
  Interim disclosure for residual bundles OK; app does not surface them in labelled view claims.

## Deferred (by scope decision, not blocked)

Sky map, relationship graph view (`astro ui` navigator exists but uses D3 from a CDN), multi-objective comparison,
session loop (`astro session`), real-catalogue store runs. **Upload bar landed** (preserve source + process_observation
consume + Action residuals). **R1:** upload+localised uses `observation_bundle_to_objective` as the primary receipt;
no-upload/demo still uses synthetic `slice1.json` (labelled).

## Assurance

No self-acceptance. Acceptance of the slice, the label policy and both compat seams belongs to Assurance / ASA Chief.
