"""Knowledge frontier: what Astro does not know, stated as records.

Absence (expected evidence that is missing), claims and their contradictions, relationships
derived from geometry that nobody has asserted, and sky coverage — all written into the
universe as derived records and into ASA as relationships, so objectives can rank ignorance.
"""

from .expectations import EXPECTATIONS, expected_kinds
from .frontier import Frontier, derive_frontier

__all__ = ["EXPECTATIONS", "Frontier", "derive_frontier", "expected_kinds"]
