# Synthetic observation fixture

`generate_fixture.py` creates a 96×96 P6 PPM containing deterministic encoded-pixel structures: one broad luminous ellipse, smaller luminous regions, compact bright regions, a cross-like contamination candidate, and a local dark deficit. It contains no third-party observation data and makes no astronomical identity or physical claim.

The fixture is algorithmic regression evidence only. Passing it does not establish performance on astronomical observations. `synthetic_observation.metadata.json` explicitly records unavailable calibration, physical scale, object identity, and scientific ground truth. `expected_assertions.json` defines modest invariants rather than invented expected astronomical classifications.
