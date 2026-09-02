"""Catalogue adapters: real astronomy sources → labelled Astro universe fragments with provenance.

Every source is described by a :class:`SourceSpec` (URL/query, release, licence, citation).
``fetch`` writes a raw snapshot and records its SHA-256 and retrieval time in the manifest;
``parse`` turns a snapshot into entities, evidence and relationships whose Provenance names the
source, release and row. Raw snapshots are never edited. Nothing here decides significance.
"""

from .fragments import Fragment, merge_fragments
from .manifest import Manifest, SourceSpec, SOURCES, fetch_source, load_manifest

__all__ = ["Fragment", "Manifest", "SOURCES", "SourceSpec", "fetch_source", "load_manifest", "merge_fragments"]
