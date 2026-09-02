"""Deterministic, content-derived identity and the intrinsic-significance prohibition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from astro_exec.core.ids import stable_identifier

DATA_CLASSES = ("real", "derived", "synthetic", "simulated", "assumption")

# Any field whose name matches one of these stems is intrinsic significance in disguise.
_FORBIDDEN_STEMS = ("significance", "significant", "priority", "importance", "important", "rank", "score", "weight")


class IntrinsicSignificanceError(ValueError):
    """A domain record attempted to carry significance as an intrinsic attribute."""


def forbid_intrinsic(fields: Mapping[str, Any], owner: str) -> None:
    for name in fields:
        lowered = name.lower()
        if any(stem in lowered for stem in _FORBIDDEN_STEMS):
            raise IntrinsicSignificanceError(
                f"{owner} may not carry intrinsic significance field {name!r}; "
                "significance is a derived construct scoped to an objective"
            )


def content_id(prefix: str, payload: Any) -> str:
    """``PREFIX-<sha256>`` of the canonical JSON payload (astro_exec contract)."""
    return stable_identifier(prefix, payload)


def freeze_mapping(value: Mapping[str, Any] | None) -> tuple[tuple[str, Any], ...]:
    """Hashable, order-independent representation of a mapping of JSON values."""
    if not value:
        return ()
    out = []
    for key in sorted(value):
        item = value[key]
        if isinstance(item, Mapping):
            item = freeze_mapping(item)
        elif isinstance(item, list):
            item = tuple(item)
        out.append((key, item))
    return tuple(out)


def thaw(value: Any) -> Any:
    """Inverse of freeze_mapping for records."""
    if isinstance(value, tuple) and all(isinstance(i, tuple) and len(i) == 2 and isinstance(i[0], str) for i in value):
        return {k: thaw(v) for k, v in value}
    if isinstance(value, tuple):
        return [thaw(v) for v in value]
    return value


@dataclass(frozen=True, slots=True)
class Provenance:
    """Where a record came from and what class of data it is."""

    source: str
    data_class: str
    reference: str = ""
    retrieved_at: str | None = None

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError("provenance source is required")
        if self.data_class not in DATA_CLASSES:
            raise ValueError(f"data_class {self.data_class!r} not in {DATA_CLASSES}")

    def to_record(self) -> dict[str, Any]:
        return {"source": self.source, "data_class": self.data_class, "reference": self.reference, "retrieved_at": self.retrieved_at}

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "Provenance":
        return cls(record["source"], record["data_class"], record.get("reference", ""), record.get("retrieved_at"))
