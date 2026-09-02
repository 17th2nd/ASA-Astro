"""Benchmark harness (directive §18): ASA-guided execution against simple alternative strategies.

Baselines never see significance. Utility is judged by an oracle declared per objective in
``oracles.py`` — the oracle reads the synthetic universe's own records (e.g. the true
ephemeris) and is used for scoring only, never for selection, except by the ``oracle``
strategy which is the upper bound. Negative findings are reported as such.
"""

from .harness import BenchmarkResult, StrategyResult, run_benchmark
from .strategies import STRATEGIES

__all__ = ["BenchmarkResult", "STRATEGIES", "StrategyResult", "run_benchmark"]
