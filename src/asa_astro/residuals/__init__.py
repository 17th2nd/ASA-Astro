"""Observed-vs-expected residuals and next-evidence recommendations (Action UI fields)."""

from .observed_vs_expected import (
    ResidualsError,
    compute_observed_vs_expected,
    write_observed_vs_expected,
)

__all__ = [
    "ResidualsError",
    "compute_observed_vs_expected",
    "write_observed_vs_expected",
]
