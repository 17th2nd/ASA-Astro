"""Astronomical entities: identity independent of any objective."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .identity import Provenance, content_id, forbid_intrinsic, freeze_mapping, thaw

ENTITY_KINDS = (
    "star", "planet", "exoplanet", "moon", "galaxy", "nebula", "supernova", "variable_star", "transient",
    "candidate", "sky_region", "catalogue_source", "star_cluster", "asteroid", "comet",
    "instrument", "telescope", "site", "survey", "observation",
)


@dataclass(frozen=True, slots=True)
class Coordinates:
    ra_deg: float
    dec_deg: float
    frame: str = "ICRS"
    epoch: str = "J2000.0"

    def __post_init__(self) -> None:
        if not 0.0 <= self.ra_deg < 360.0:
            raise ValueError(f"ra_deg {self.ra_deg} outside [0, 360)")
        if not -90.0 <= self.dec_deg <= 90.0:
            raise ValueError(f"dec_deg {self.dec_deg} outside [-90, 90]")

    def to_record(self) -> dict[str, Any]:
        return {"ra_deg": self.ra_deg, "dec_deg": self.dec_deg, "frame": self.frame, "epoch": self.epoch}

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "Coordinates":
        return cls(float(r["ra_deg"]), float(r["dec_deg"]), r.get("frame", "ICRS"), r.get("epoch", "J2000.0"))


@dataclass(frozen=True, slots=True)
class Entity:
    """An astronomical entity. Identity derives from kind, designation and catalogue ids only."""

    entity_id: str
    kind: str
    designation: str
    catalogue_ids: tuple[tuple[str, str], ...] = ()
    aliases: tuple[str, ...] = ()
    coordinates: Coordinates | None = None
    source: Provenance | None = None
    attributes: tuple[tuple[str, Any], ...] = field(default=())

    @staticmethod
    def identity_seed(kind: str, designation: str, catalogue_ids: Mapping[str, str] | None) -> dict[str, Any]:
        return {"kind": kind, "designation": designation, "catalogue_ids": sorted((catalogue_ids or {}).items())}

    @classmethod
    def create(
        cls,
        kind: str,
        designation: str,
        *,
        catalogue_ids: Mapping[str, str] | None = None,
        aliases: tuple[str, ...] | list[str] = (),
        coordinates: Coordinates | None = None,
        source: Provenance | None = None,
        attributes: Mapping[str, Any] | None = None,
    ) -> "Entity":
        if kind not in ENTITY_KINDS:
            raise ValueError(f"entity kind {kind!r} not in ENTITY_KINDS")
        if not designation:
            raise ValueError("designation is required")
        forbid_intrinsic(attributes or {}, f"Entity {designation!r}")
        seed = cls.identity_seed(kind, designation, catalogue_ids)
        return cls(
            entity_id=content_id("ENT", seed),
            kind=kind,
            designation=designation,
            catalogue_ids=tuple(sorted((catalogue_ids or {}).items())),
            aliases=tuple(sorted(aliases)),
            coordinates=coordinates,
            source=source,
            attributes=freeze_mapping(attributes),
        )

    @property
    def attribute_map(self) -> dict[str, Any]:
        return thaw(self.attributes)

    def to_record(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "kind": self.kind,
            "designation": self.designation,
            "catalogue_ids": [list(pair) for pair in self.catalogue_ids],
            "aliases": list(self.aliases),
            "coordinates": self.coordinates.to_record() if self.coordinates else None,
            "source": self.source.to_record() if self.source else None,
            "attributes": self.attribute_map,
        }

    @classmethod
    def from_record(cls, r: Mapping[str, Any]) -> "Entity":
        entity = cls.create(
            r["kind"],
            r["designation"],
            catalogue_ids=dict(r.get("catalogue_ids") or []),
            aliases=tuple(r.get("aliases") or ()),
            coordinates=Coordinates.from_record(r["coordinates"]) if r.get("coordinates") else None,
            source=Provenance.from_record(r["source"]) if r.get("source") else None,
            attributes=r.get("attributes") or {},
        )
        if r.get("entity_id") and r["entity_id"] != entity.entity_id:
            raise ValueError(f"entity_id {r['entity_id']} does not match content identity {entity.entity_id}")
        return entity
