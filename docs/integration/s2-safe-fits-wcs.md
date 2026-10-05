# S2 / P2 — Safe FITS + TAN/SIP + solve-field

**Owner:** Significance / Operator C. **Not V1 ACCEPT.**

## Modules

| Module | Role |
| --- | --- |
| `asa_astro.evidence.fits_io` | Read-only FITS open; preserve source bytes; extract WCS/time/instrument/filter/pointing/scale |
| `asa_astro.evidence.wcs` | `local-linear-CD` labelled approximation for declared metadata; routes TAN/SIP via astropy when `wcs_header_cards` present |
| `asa_astro.evidence.solve_field` | Optional local `solve-field` adapter; fail closed if absent |

## Pins

- `astropy==6.1.7`
- `numpy>=2.0,<2.3` (tested with `numpy==2.2.6`)

## Honesty

- Never invent coordinates; never mutate source FITS bytes.
- `projection_model`: `local-linear-CD` | `TAN` | `TAN-SIP` | `other-fits-wcs`
- FITS CRPIX converted 1-based → 0-based for detection centroids.
- TAN without `wcs_header_cards` fails closed (no silent local-linear substitute).
- `solve-field` missing → `SolveFieldUnavailable` (set `ASA_ASTRO_SOLVE_FIELD` to enable).

## App / Runtime

FITS upload processability in `app/upload.py` remains Runtime-owned. This commit exposes library APIs only.
