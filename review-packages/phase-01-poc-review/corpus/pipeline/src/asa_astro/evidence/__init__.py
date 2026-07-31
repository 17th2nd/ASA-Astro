"""Codex B-owned observation, evidence, candidate, and candidate-graph pipeline."""

from .models import PIPELINE_VERSION
from .pipeline import process_observation

__all__ = ["PIPELINE_VERSION", "process_observation"]
