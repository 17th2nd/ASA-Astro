"""App-layer compatibility shim between the current-dev ASA kernel (c2ccd7d) and the Astro adapter.

Honesty note (G-PIN-2, refreshed 2026-10-05 after tip RP-9 land):

* Tip adapter (`src/astro/asa/adapter.py`) now implements SPEC-0001 [RP-9] natively:
  stream writer ``GOVERNOR_ACTOR = "asa:uao:asa.core/governor-v1"`` is distinct from
  propose proposer ``ACTOR = "asa:uao:astro/adapter"`` (registered UAO). That tip path
  no longer needs an app-layer workaround for the old Governor-as-proposer collision.

* This app still applies an **additional** pre-tip shim: it registers
  ``asa:uao:astro/proposer`` and proposes with that id instead of the tip adapter's
  ``asa:uao:astro/adapter``. That changes the kernel event stream (extra
  ``register_entity`` + different proposer id on proposals) and therefore the kernel
  digest vs an unshimmed tip adapter run.

* Pin semantics are unchanged (still current_dev / c2ccd7d). The shim is recorded on
  every run for honesty of the path actually taken; accepting removal of the shim
  (align digests with tip adapter) remains Assurance / compat-gate owned (GAPS.md G-PIN-2).
"""

from __future__ import annotations

from typing import Any, Mapping

from astro.asa.adapter import AstroAdapter

PROPOSER = "asa:uao:astro/proposer"

SHIM_RECORD = {
    "id": "app-compat-proposer-uao",
    "applied": True,
    "status": "app-layer residual shim — tip already has native RP-9 (governor ≠ adapter proposer); not accepted into src/astro; owned by adapter/compat-gate lane",
    "reason": "tip RP-9 is landed (GOVERNOR_ACTOR=asa:uao:asa.core/governor-v1, propose proposer=asa:uao:astro/adapter); this app still proposes as asa:uao:astro/proposer for continuity with the pre-tip thin-slice path — residual honesty, not a claim that tip still lacks RP-9",
    "effect": f"registers UAO {PROPOSER} before loading the universe and proposes URO with it; the kernel digest therefore differs from an unshimmed tip adapter run",
    "source": "app/compat.py",
}

class PinnedAdapter(AstroAdapter):
    """AstroAdapter with a registered proposer UAO distinct from the Governor actor."""

    @classmethod
    def in_memory_registered(cls, registry_facet, stream_slug: str = "astro") -> "PinnedAdapter":
        adapter = cls.in_memory(registry_facet, stream_slug)
        if adapter.k.query(PROPOSER) is None:
            adapter._submit("register_entity", uao_id=PROPOSER, attributes={"role": "astro-proposer"})
        return adapter

    def _submit_uro(self, type_id: str, bindings: Mapping[str, list[str]], literals: Mapping[str, Any]):
        r = self._submit("propose", type_id=type_id, bindings=bindings, literals=dict(literals), proposer=PROPOSER)
        if r.key:
            self._uro_index[self._uro_key(type_id, bindings)] = r.key
            self._uro_index_lit[self._uro_key(type_id, bindings) + (self._lit_key(literals),)] = r.key
        return r
