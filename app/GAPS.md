# ASA-Astro V1 application — gaps and dependencies

Recorded by Operator D (Application/UX) on the thin slice. Each gap is something the app does **not** fake;
the UI shows the limitation or derives only from existing fields with a source link.

## Pin / adapter (Operator A pin, adapter compat-gate lane)

- **G-PIN-1 — locator reads the historical pin.** `src/astro/asa/locator.py` hard-codes `config/asa-baseline.json`
  (b855d4c) and calls `tools/asa_baseline.verify()` without `config_path`. With `.asa/ASA` at the current-dev SHA
  (c2ccd7d) every `import astro.asa.adapter` raises `AsaBaselineUnavailable`. Consequence at base `633f837a`: 6 of 8
  `tests/astro` modules fail to import. The app works around it *without editing src/* by pointing `locator.CONFIG`
  at `config/asa-baseline-current-dev.json` before importing the adapter (`app/pin.py`). Needed: an accepted locator
  change (e.g. honour `--config` / an env var / make current-dev the active pin) by the pin owner.
- **G-PIN-2 — adapter proposer rejected by the pinned kernel.** Kernel `0.1.0-alpha13` (c2ccd7d) enforces SPEC-0001
  [RP-9]: a URO proposer must be a registered UAO (`URO-PARTICIPANT-UNKNOWN`), and it refuses to register the Governor
  actor id as an entity (`EVT-STATE`). `AstroAdapter` uses `ACTOR = asa:uao:astro/adapter` for both. So the unmodified
  adapter cannot load any universe at this pin. The app subclasses the adapter (`app/compat.py`): registers
  `asa:uao:astro/proposer` and proposes with it. This changes the event stream and therefore the kernel digest; every
  run records the shim (`run.json:compat_shims`, shown in the UI). Needed: the real adapter fix + compat-gate test run.
- **G-PIN-3 — declared vs reported kernel version.** The pin file declares `kernel_version: unreleased-remediation-133`;
  the kernel reports `0.1.0-alpha13`, status `ENGINEERING ALPHA — NOT RATIFIED`. Shown as an unknown.
- **G-PIN-4 — pin status.** The pin is `CURRENT DEVELOPMENT COMPATIBILITY PIN — NOT A FROZEN FINAL V1`. Shown as an unknown.

## Significance / pipeline lane (what the app needs produced)

- **G-SIG-1 — no image → Astro universe bridge.** The Codex B observe pipeline (`asa_astro.evidence`) emits an
  image-space candidate graph (`graph.json`, `provenance.json`; `asa_dependency: unavailable_not_consumed`); the Astro
  engine consumes a catalogue-style `Universe`. Nothing maps one into the other, so image upload cannot feed
  pin → snapshot → objective → receipt. The slice uses the repo example `data/universe/slice1.json` (synthetic).
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

## Deferred (by scope decision, not blocked)

Image upload and observe-pipeline session flow, sky map, relationship graph view (`astro ui` navigator exists but uses
D3 from a CDN), multi-objective comparison, session loop (`astro session`), real-catalogue store runs.

## Assurance

No self-acceptance. Acceptance of the slice, the label policy and both compat seams belongs to Assurance / ASA Chief.
