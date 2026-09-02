"""Objectives and observing contexts: the declared question under which significance is computed."""

from .context import ObservingContext
from .objective import FeatureSpec, Objective, ObjectiveError

__all__ = ["FeatureSpec", "Objective", "ObjectiveError", "ObservingContext"]
