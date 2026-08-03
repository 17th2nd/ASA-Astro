"""Deterministic execution infrastructure for the ASA-Astro experiment.

The :mod:`astro_exec` package is independent from the historical
:mod:`asa_astro` proof of concept.  Phase 2 exposes infrastructure contracts
only; it performs no astronomy or scientific computation.
"""

from .core.errors import AstroExecError

__all__ = ["AstroExecError", "__version__"]
__version__ = "0.1.0"
