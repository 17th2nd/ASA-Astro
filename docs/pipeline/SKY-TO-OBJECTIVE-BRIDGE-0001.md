# Sky → candidates → Objective bridge (0001)

**Branch:** `grok/asa-astro-v1-application`  
**Operator:** C  
**Scope:** Astro-only thin harness. No ASA programme edits. No identity promotion.

## Behaviour

1. Accept WCS-when-present `sky_localisation` records (and optional evidence-qualified crossmatches).
2. Fail closed if none are `status=localised` (never invent coordinates).
3. Build a **temporary synthetic universe** with `kind=candidate` entities; every derived entity carries `classification_status=hypothesis` and `established_identity=false`.
4. Evaluate under a declared sky-candidate Objective via `astro.pipeline.decide`.
5. Write standard receipt artefacts plus `bridge_manifest.json` recording hyp-vs-established epistemic flags.

## API

`asa_astro.bridge.bridge_sky_localisations_to_objective`  
`asa_astro.bridge.bridge_observation_bundle_to_objective` (reads observe-bundle `sky_localisations.json`)

## Tests

```bash
ASTRO_ASA_PIN_KIND=current_dev .venv/bin/python -m unittest tests.unit.test_sky_to_objective_bridge -v
```
