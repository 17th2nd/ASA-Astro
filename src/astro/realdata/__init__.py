"""ASTRO-REAL-DATA-EXP-0001: one small real-data value test of the Astro engine.

Everything here is experiment apparatus — dataset retrieval and freezing, the universe adapter, declared
baselines, metrics, adversarial checks and the runner. It never modifies the engine, any objective already
declared under ``data/objectives/``, or any frozen scientific instrument. Results are engineering evidence about
the Astro engine; they are not scientific validation of ASA and do not change the EH-0 evidence level.
"""

EXP_ID = "ASTRO-REAL-DATA-EXP-0001"
HASH_SALT = "ASTRO-REAL-DATA-EXP-0001-v1"
