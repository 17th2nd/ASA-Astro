"""Canonical JSON serialization for digest-stable infrastructure records."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from .errors import CanonicalJSONError


def canonical_timestamp(value: datetime) -> str:
    """Return an aware timestamp as UTC RFC 3339 with six fractional digits.

    Naive datetimes are rejected because interpreting them would depend on an
    ambient workstation timezone. The fixed-width microsecond form is the only
    timestamp representation emitted by this module.
    """

    if value.tzinfo is None or value.utcoffset() is None:
        raise CanonicalJSONError("timestamp must include an explicit UTC offset")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _normalise(value: Any, location: str = "$") -> Any:
    if isinstance(value, datetime):
        return canonical_timestamp(value)
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalJSONError(
                "non-finite floating-point value rejected",
                details={"location": location},
            )
        return value
    if isinstance(value, Mapping):
        normalised: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str):
                raise CanonicalJSONError(
                    "canonical JSON object keys must be strings",
                    details={"location": location},
                )
            normalised[key] = _normalise(child, f"{location}.{key}")
        return normalised
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalise(child, f"{location}[{index}]") for index, child in enumerate(value)]
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

    normalised = _normalise(value)
    return json.dumps(
        normalised,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def canonical_bytes(value: Any) -> bytes:
    """Return the UTF-8 bytes of :func:`canonical_text`."""

    return canonical_text(value).encode("utf-8")
