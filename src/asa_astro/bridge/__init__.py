"""Sky-localised candidates → temporary universe → Objective evaluate (hypothesis-flagged).

Runtime handoff A (Significance-owned): ``observation_bundle_to_objective``.
"""

from .sky_to_objective import (
    DEMO_SITE_DESIGNATION,
    SkyToObjectiveBridgeError,
    UNDECLARED_SITE_DESIGNATION,
    bridge_observation_bundle_to_objective,
    bridge_sky_localisations_to_objective,
    default_sky_candidate_objective,
    load_observation_identity_from_bundle,
    observation_bundle_to_objective,
)

__all__ = [
    "SkyToObjectiveBridgeError",
    "DEMO_SITE_DESIGNATION",
    "UNDECLARED_SITE_DESIGNATION",
    "bridge_sky_localisations_to_objective",
    "observation_bundle_to_objective",
    "bridge_observation_bundle_to_objective",
    "default_sky_candidate_objective",
    "load_observation_identity_from_bundle",
]
