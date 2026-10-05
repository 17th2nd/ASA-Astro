# Operator C — Observation → Objective status (V1 application)

**Branch:** `grok/asa-astro-v1-application`  
**Pin:** `config/asa-baseline-current-dev.json` → `c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2`  
**Status:** Adapter green under current-dev; observation ingest and Objective evaluate are both executable; **no silent image→entity promotion**.

## Verified executable paths (2026-10-05)

1. **Observation ingest (Codex B PoC)** — `python -m asa_astro.cli <image> … --output <new-dir>`  
   Preserves source bytes under content-addressed `source/`; emits candidate graph with hypothesis labels only (`physical_claim=false`). Does **not** fill missing calibration/WCS.
2. **Objective evaluate (Astro engine)** — `ASTRO_ASA_PIN_KIND=current_dev astro evaluate --universe … --objective … --context … --out …`  
   Receipt records `asa_baseline` = current-dev SHA. Significance is Astro-derived over ASA relational snapshot.
3. **Adapter tests** — `ASTRO_ASA_PIN_KIND=current_dev python -m unittest tests.astro.test_asa_adapter -v`  
   Remediation-133 RP-9: adapter registers proposer UAO `asa:uao:astro/adapter` distinct from governor actor `asa:uao:astro/adapter-governor`.

## Gap (honest)

There is **no** automated bridge that turns an observation `graph.json` into an Objective-ranked universe. Thin-slice contracts for steps 1–2 now exist; the Objective harness does not.

| Missing / partial | Why it blocks Objective binding |
|---|---|
| FITS header / plate-solve → declared WCS | Thin slice accepts **caller-declared** WCS only (local linear CD); no FITS parser yet |
| WCS-when-present localisation | **Done (thin slice):** `asa_astro.evidence.wcs` — fail closed when absent; hypothesis labels |
| Catalogue cross-match from detections | **Done (thin slice):** `asa_astro.evidence.crossmatch` — matched/unresolved/contested; evidence-qualified only |
| Observed-vs-expected residual evidence | Gaps today are catalogue expectations, not observation residuals |
| graph.json → temporary universe → Objective | Still missing |

Promotion rules (non-negotiable): preserve source images; never silently fill missing values; distinguish **hypothesis** vs **established**. Candidate labels remain hypotheses until an explicit, evidenced resolution step exists. See `docs/pipeline/WCS-WHEN-PRESENT-CROSSMATCH-0001.md`.

## Next Astro-only steps (ordered)

1. ~~Observation bundle → sky-candidate contract (WCS when present; else `unavailable`, never invented).~~ **Thin slice landed** (`wcs-solution` / `sky-localisation` schemas + `wcs.py`).
2. ~~Cross-match interface emitting `matched` / `unresolved` / `contested` without collapsing representation→entity.~~ **Thin slice landed** (`catalogue-crossmatch` schema + `crossmatch.py`).
3. Thin harness: synthetic sky-localised candidates → temporary universe → one Objective evaluate (hypothesis flagged on every derived entity).
4. Optional: FITS/`astropy.wcs` → declared-WCS adapter (still fail closed; never invent).
5. Optional: wire localisation into `process_observation` only when metadata carries declared WCS.
