"""Astro astronomy domain model.

Objects possess identity, evidence, relationships and state. They do not
possess intrinsic significance: no record in this package may carry a
significance, priority or importance field (enforced by ``identity.forbid_intrinsic``).
"""

from .entities import ENTITY_KINDS, Coordinates, Entity
from .evidence import EVIDENCE_KINDS, EVIDENCE_STATUSES, EvidenceRecord
from .identity import DATA_CLASSES, IntrinsicSignificanceError, Provenance, content_id
from .relationships import RELATIONSHIP_TYPES, RelationshipAssertion
from .state import ALERT_STATES, CANDIDATE_STATUSES, OBSERVATION_STATUSES, EntityState
from .universe import Universe, UniverseError

__all__ = [
    "ALERT_STATES", "CANDIDATE_STATUSES", "Coordinates", "DATA_CLASSES", "ENTITY_KINDS", "EVIDENCE_KINDS",
    "EVIDENCE_STATUSES", "Entity", "EntityState", "EvidenceRecord", "IntrinsicSignificanceError",
    "OBSERVATION_STATUSES", "Provenance", "RELATIONSHIP_TYPES", "RelationshipAssertion", "Universe",
    "UniverseError", "content_id",
]
