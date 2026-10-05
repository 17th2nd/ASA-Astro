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

There is **no** automated bridge that turns an observation `graph.json` into an Objective-ranked universe:

| Missing | Why it blocks Objective binding |
|---|---|
| FITS/WCS / astrometric localisation | Candidates are image-pixel hypotheses, not sky entities |
| Catalogue cross-match from detections | No established identity from pixels |
| Observed-vs-expected residual evidence | Gaps today are catalogue expectations, not observation residuals |

Promotion rules (non-negotiable): preserve source images; never silently fill missing values; distinguish **hypothesis** vs **established**. Candidate labels remain hypotheses until an explicit, evidenced resolution step exists.

## Next Astro-only steps (ordered)

1. Observation bundle → sky-candidate contract (WCS when present; else `unavailable`, never invented).
2. Cross-match interface emitting `matched` / `unresolved` / `contested` without collapsing representation→entity.
3. Thin harness: synthetic sky-localised candidates → temporary universe → one Objective evaluate (hypothesis flagged on every derived entity).
