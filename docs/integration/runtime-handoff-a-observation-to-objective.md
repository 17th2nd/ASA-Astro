# Runtime handoff A — observation bundle → Objective (S1)

**Owner:** Significance / Operator C (Astro). **App wire-up:** Runtime (do not land in this commit).

**Status:** Astro API frozen for Runtime consume. **Not V1 ACCEPT.**

## API

```python
from asa_astro.bridge import observation_bundle_to_objective, SkyToObjectiveBridgeError

result = observation_bundle_to_objective(
    bundle_directory,   # process_observation output dir
    out_directory,      # must not already exist
    *,
    objective=None,     # astro.objectives.Objective; default sky-candidate objective
    context=None,       # ObservingContext | mapping; else declared from site/window defaults
    site=None,          # declared observer site mapping (latitude_deg/longitude_deg optional)
    instrument=None,    # optional instrument mapping
    allow_synthetic_demo_site=False,  # True ONLY for tests/demos (SYN-SITE lat/lon)
)
```

### Return dict (Action/Runtime-facing fields)

| Field | Meaning |
| --- | --- |
| `receipt_id` | Objective RCPT (distinct from observation claim) |
| `universe_id` / `objective_id` / `context_id` / `evaluation_id` | Digest-identified artefacts under `out_directory` |
| `observation_identity` | Present-only claim digests from the bundle (`source_sha256`, `metadata_sha256`, `wcs_digest`, `observation_claim_digest`, `observation_claim_id`) — **not invented** |
| `site_standing` | `declared-metadata` \| `declared-incomplete` \| `undeclared` \| `synthetic-demo-only` |
| `site_demo_only` | True only when `allow_synthetic_demo_site=True` and no declared site |
| `slice1_substituted` | Always `False` on this path |
| `coordinates_invented` | Honesty flag |
| `established_identity_promoted` | Always `False` |
| `hypothesis_entity_count` | Count of sky-derived hypothesis candidates |
| `bridge_manifest` | Full epistemic + ranking summary (also written as `bridge_manifest.json`) |
| `api` | `"asa_astro.bridge.observation_bundle_to_objective"` |

Artefacts written under `out_directory`: `universe.json`, `objective.json`, `context.json`, `evaluation.json`, `plan.json`, `receipt.json`, `receipt.sha256`, `bridge_manifest.json`, and `observation_identity.json` when present.

## Fail-closed

- Missing `sky_localisations.json`
- `wcs_present=false`
- No `status=localised` rows
- Localised row lacking `ra_deg`/`dec_deg`

Never invents sky coordinates. Never substitutes `data/universe/slice1.json`.

## Site honesty (SYN-SITE kill for real uploads)

| Path | Behaviour |
| --- | --- |
| Declared `site=` (or bundle `associated_metadata.json` / `metadata.json` → `site` / `observer_site`) | Use declared attrs; lat/lon only if present in metadata |
| No site, `allow_synthetic_demo_site=False` (real upload default) | `SITE-UNDECLARED-HYPOTHESIS` — **no** lat/lon invented |
| `allow_synthetic_demo_site=True` and no site | Explicit demo SYN-SITE with hard-coded coords; labelled `synthetic-demo-only` |

## Runtime integration touchpoints (owned by Runtime — not landed here)

1. `app/upload.py` `run_process_observation`: after a successful localised bundle, call `observation_bundle_to_objective` instead of leaving `objective_bridge: absent…`.
2. `app/slice.py` `run_slice`: when upload present + localisation succeeded, primary receipt/universe from bridge out-dir; **do not** load `cfg["default_inputs"]["universe"]` (slice1) as silent substitute. JSON-only / demo runs may keep slice1.
3. Surface Action-facing fields already projected present-only: `observation_identity`, residuals / `missing_expected` / `next_evidence_recommendations` / `action_ui` from bundle (P7 — residuals already computable via `asa_astro.residuals`).
4. Fail closed in UI when bridge raises `SkyToObjectiveBridgeError` (show honesty, do not fall back to synthetic Objective as established/primary).

## Tests

`tests/unit/test_sky_to_objective_bridge.py` — localised+identity bind; no-localised fail-closed (no slice1); demo path under explicit flag.

## Pin

`config/asa-baseline-current-dev.json` → `c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2`. Historical `config/asa-baseline.json` untouched.
