"""Significance as a derived construct.

Computed by Astro over ASA relational state under a declared Objective and
ObservingContext. Never stored on an entity; every result is scoped to
(objective, context, universe digest, kernel digest, ASA baseline, Astro version).
"""

from .evaluator import SignificanceEvaluation, SignificanceResult, evaluate, explain
from .features import FEATURES, FeatureInput, FeatureValue

__all__ = ["FEATURES", "FeatureInput", "FeatureValue", "SignificanceEvaluation", "SignificanceResult", "evaluate", "explain"]
