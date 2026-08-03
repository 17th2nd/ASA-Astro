"""Canonical JSON serialization for digest-stable infrastructure records."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from typing import Any

from .errors import CanonicalJSONError


def _validate(value: Any, location: str = "$") -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalJSONError(
                "non-finite floating-point value rejected",
                details={"location": location},
            )
        return
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise CanonicalJSONError(
                    "canonical JSON object keys must be strings",
                    details={"location": location},
                )
            _validate(child, f"{location}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            _validate(child, f"{location}[{index}]")
        return
    raise CanonicalJSONError(
        "value is outside the canonical JSON data model",
        details={"location": location, "type": type(value).__name__},
    )


def canonical_text(value: Any) -> str:
    """Serialize JSON data with sorted keys and no insignificant whitespace.

    The result uses UTF-8-compatible Unicode text, rejects non-finite floats,
    and relies on Python's shortest round-trip representation for finite
    binary64 values.
    """

    _validate(value)
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def canonical_bytes(value: Any) -> bytes:
    """Return the UTF-8 bytes of :func:`canonical_text`."""

    return canonical_text(value).encode("utf-8")
