# WCS-when-present localisation + detection→catalogue crossmatch (0001)

**Branch:** `grok/asa-astro-v1-application`  
**Operator:** C (Runtime Lead)  
**Scope:** Astro-only thin slice — contracts, pure-Python transforms, unit tests.  
**Status:** Implemented under fail-closed rules. Does **not** edit ASA programme material. Does **not** promote hypothesis→established identity.

## Mandatory rules (enforced)

| Rule | Enforcement |
|---|---|
| Fail closed when WCS absent | `localise_detection` emits `status=unavailable`, `sky.*=null` |
| Never invent coords | No default CRVAL/CD; incomplete WCS raises / unavailable |
| Hypothesis vs established | `classification_status=hypothesis` on localised + matched records |
| Catalogue matches evidence-qualified only | Sole positional hit without `evidence_ids` → `unresolved` |
| Preserve source images | Modules transform declared centroids only; no image I/O writes |
| Astro-only | Code under `src/asa_astro/evidence/`; schemas under `schemas/observation/` |
| Disk hygiene | Catalogue rows are caller-supplied in-memory; no large dumps |

## Contracts

- `schemas/observation/wcs-solution.schema.json` — declared WCS (externally supplied)
- `schemas/observation/sky-localisation.schema.json` — per-detection localisation result
- `schemas/observation/catalogue-crossmatch.schema.json` — `matched` / `unresolved` / `contested` / `unavailable`

## API

```python
from asa_astro.evidence import (
    parse_declared_wcs,
    localise_detection,
    localise_detections,
    crossmatch_localisation,
    crossmatch_localisations,
)

wcs = {
    "frame": "ICRS",
    "epoch": "J2000.0",
    "crpix": [x0, y0],                 # 0-based, same grid as detection centroids
    "crval_deg": [ra0, dec0],
    "cd_deg_per_pixel": [[cd11, cd12], [cd21, cd22]],
    "pixel_origin": "0-based-image-pixel",
}
loc = localise_detection(detection, wcs)          # or None → unavailable
xm = crossmatch_localisation(
    loc,
    catalogue_entries,                 # in-memory only
    match_radius_arcsec=2.0,
    catalogue_provenance={
        "catalogue_name": "...",
        "release": "...",
        "query_description": "...",
    },
)
```

### Resolution states

| State | Meaning |
|---|---|
| `matched` | Exactly one catalogue entry within radius **and** it carries ≥1 evidence ID |
| `unresolved` | Zero hits, or sole hit lacking evidence IDs |
| `contested` | Two or more hits within radius |
| `unavailable` | Localisation was not `localised` (WCS absent/incomplete) |

## What this does **not** do

- FITS header parsing / plate-solving / SIP / TAN projection beyond local linear CD
- Network catalogue fetch or on-disk catalogue materialisation
- Silent fill of missing calibration
- Collapse of candidate representation into an established sky entity
- Objective evaluate / universe binding (still a later harness step)

## Tests

```bash
.venv/bin/python -m unittest tests.unit.test_wcs_and_crossmatch -v
```

## `process_observation` wiring

`process_observation` always emits `sky_localisations.json`:

| Metadata | Behaviour |
|---|---|
| no `wcs` / `declared_wcs` | Fail closed: every localisation `status=unavailable`, sky coords null |
| incomplete/invalid WCS | Fail closed (same); reason recorded in provenance |
| complete declared WCS | Localise centroids; `classification_status=hypothesis`; write `wcs_solution.json` |
| optional `catalogue` block | In-memory evidence-qualified crossmatch → `catalogue_crossmatches.json` |

Source image bytes are never written; only content-addressed copies. Coordinates are never invented.

```bash
.venv/bin/python -m unittest tests.unit.test_process_observation_wcs -v
```

## Sky → Objective bridge

```python
from asa_astro.bridge import bridge_sky_localisations_to_objective
result = bridge_sky_localisations_to_objective(localisations, out_dir, crossmatches=crossmatches)
# writes universe/objective/context/evaluation/plan/receipt + bridge_manifest.json
# every sky entity: classification_status=hypothesis; established_identity_promoted=false
```

Fail closed when no `status=localised` records (or bundle `wcs_present=false`).

```bash
ASTRO_ASA_PIN_KIND=current_dev .venv/bin/python -m unittest tests.unit.test_sky_to_objective_bridge -v
```

## Next gaps

1. Optional FITS/`astropy.wcs` adapter behind the same declared-WCS contract (still fail closed).
2. Observed-vs-expected residual evidence for Action UI.
