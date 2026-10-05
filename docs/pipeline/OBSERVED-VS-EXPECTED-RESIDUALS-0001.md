# Observed-vs-expected residuals (0001)

**Branch:** `grok/asa-astro-v1-application`  
**Operator:** C  
**Scope:** Astro-only. Plain-language fields for Action UI. No identity promotion.

## Outputs

`asa_astro.residuals.compute_observed_vs_expected(...)` returns:

| Field | Purpose |
|---|---|
| `residuals[]` | Per-detection observed vs expected (within_tolerance / offset / unmatched / unlocalised) |
| `missing_expected[]` | Expected catalogue sources not matched to any observation |
| `next_evidence_recommendations[]` | Ordered next actions with `plain_language` |
| `action_ui` | Headline + short lines + honesty flags for the Action thin app |

Every residual keeps `classification_status=hypothesis` and `established_identity=false`. Fail closed when localisation is unavailable (sky coords null; never invented).

## Tests

```bash
.venv/bin/python -m unittest tests.unit.test_observed_vs_expected -v
```
