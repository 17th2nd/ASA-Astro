"""App-layer compatibility shim between the current-dev ASA kernel (c2ccd7d) and the Astro adapter.

Observed on 2026-10-05 against the pinned kernel (0.1.0-alpha13, remediation-133):

* ``AstroAdapter`` proposes every URO with ``proposer = ACTOR = "asa:uao:astro/adapter"``,
  which is also the Governor actor id passed to ``Kernel.bootstrap``.
* The pinned kernel enforces SPEC-0001 [RP-9]: a proposer must be a registered, active UAO
  (``URO-PARTICIPANT-UNKNOWN: proposer is not a registered UAO``), and it refuses to register
  the Governor actor id as an entity (``EVT-STATE``).

So the unmodified adapter cannot load any universe at this pin. Without editing src/, the app
registers a distinct proposer UAO and proposes with it. This changes the kernel event stream
(one extra ``register_entity`` event, proposer id on every proposal) and therefore the kernel
digest. It is NOT an accepted Astro adapter change: the real fix belongs to the adapter /
compat-gate lane (GAPS.md G-PIN-2). Every run records that this shim was applied.
"""

from __future__ import annotations

from typing import Any, Mapping

from astro.asa.adapter import AstroAdapter

PROPOSER = "asa:uao:astro/proposer"

SHIM_RECORD = {
    "id": "app-compat-proposer-uao",
    "applied": True,
    "status": "app-layer workaround — not accepted into src/astro; owned by adapter/compat-gate lane",
    "reason": "pinned kernel enforces SPEC-0001 [RP-9] (proposer must be a registered UAO) and refuses to register the Governor actor id; AstroAdapter uses its Governor actor id as proposer",
    "effect": f"registers UAO {PROPOSER} before loading the universe and proposes URO with it; the kernel digest therefore differs from what an unshimmed adapter would produce",
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
