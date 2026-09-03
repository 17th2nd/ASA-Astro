"""Frontier report: what the store says Astro does not know, summarised from ASA relational state."""

from __future__ import annotations

from collections import Counter
from typing import Any

from astro.asa.adapter import AstroAdapter, RelationalSnapshot
from astro.domain import Universe


def frontier_report(universe: Universe, snapshot: RelationalSnapshot, top: int = 10) -> dict[str, Any]:
    kinds = {e.entity_id: e.kind for e in universe.entities}
    names = {e.entity_id: e.designation for e in universe.entities}
    gaps = [e for e in snapshot.edges if e.type_name == "lacks_evidence" and e.lifecycle == "registered"]
    gap_by_kind = Counter(dict(e.literals).get("evidence_kind") for e in gaps)
    gap_by_entity_kind = Counter(kinds.get(dict(e.bindings)["subject"][0], "?") for e in gaps)
    unevaluated = [e for e in snapshot.edges if e.stance == "unevaluated" and e.lifecycle == "registered" and e.type_name not in ("lacks_evidence", "measures", "contradicts")]
    unevaluated_by_type = Counter(e.type_name for e in unevaluated)
    endorsed_derived = Counter(e.type_name for e in snapshot.edges if e.stance == "endorsed" and e.type_name in ("near", "member_of", "hosted_transient"))
    contradictions = [e for e in snapshot.edges if e.type_name == "contradicts" and e.lifecycle == "registered"]
    claim_by_key = {e.key: e for e in snapshot.edges if e.type_name == "measures"}
    disputed_entities: Counter = Counter()
    disputed_quantities: Counter = Counter()
    examples = []
    for c in contradictions:
        keys = c.participants()
        claims = [claim_by_key.get(k) for k in keys]
        if not all(claims):
            continue
        subject = dict(claims[0].bindings)["subject"][0]
        q = dict(claims[0].literals).get("quantity")
        disputed_entities[subject] += 1
        disputed_quantities[q] += 1
        if len(examples) < top:
            examples.append({"entity": names.get(subject, subject), "quantity": q,
                             "claims": [{"value": dict(cl.literals).get("value"), "unit": dict(cl.literals).get("unit"), "source": dict(cl.literals).get("source_key")} for cl in claims]})
    most_gapped = Counter(dict(e.bindings)["subject"][0] for e in gaps).most_common(top)
    return {
        "kernel_digest": snapshot.digest, "kernel_seq": snapshot.seq, "universe_id": universe.universe_id,
        "entities": len(universe.entities), "evidence": len(universe.evidence), "relationships_registered": sum(1 for e in snapshot.edges if e.lifecycle == "registered"),
        "blank_spaces": {"lacks_evidence": len(gaps), "by_missing_kind": dict(gap_by_kind.most_common()), "by_entity_kind": dict(gap_by_entity_kind.most_common()),
                         "most_gapped": [{"entity": names.get(k, k), "kind": kinds.get(k), "gaps": n} for k, n in most_gapped]},
        "semantic_edges": {"unevaluated_relationships": len(unevaluated), "by_type": dict(unevaluated_by_type.most_common()),
                           "derived_endorsed": dict(endorsed_derived.most_common())},
        "disputes": {"contradictions": len(contradictions), "entities_disputed": len(disputed_entities), "by_quantity": dict(disputed_quantities.most_common()),
                     "examples": examples},
        "sky": {"tiles": sum(1 for e in universe.entities if e.kind == "sky_region"),
                "gap_tiles": sum(1 for v in universe.evidence if v.kind == "coverage_gap" and kinds.get(v.subject_id) == "sky_region")},
    }


def render(report: dict[str, Any]) -> str:
    b, s, d = report["blank_spaces"], report["semantic_edges"], report["disputes"]
    lines = [f"Frontier of {report['entities']} entities / {report['evidence']} evidence / {report['relationships_registered']} registered relationships  (kernel seq {report['kernel_seq']})",
             f"Blank spaces: {b['lacks_evidence']} missing expected evidence records — by kind {b['by_missing_kind']}; by entity kind {b['by_entity_kind']}",
             "  most gapped: " + ", ".join(f"{m['entity']} ({m['kind']}, {m['gaps']})" for m in b["most_gapped"][:5]),
             f"Semantic edges: {s['unevaluated_relationships']} asserted-but-unsupported relationships {s['by_type']}; derived and endorsed {s['derived_endorsed']}",
             f"Disputes: {d['contradictions']} contradictions over {d['entities_disputed']} entities, by quantity {d['by_quantity']}"]
    for ex in d["examples"][:5]:
        lines.append("  e.g. " + ex["entity"] + " " + ex["quantity"] + ": " + " vs ".join(f"{c['value']} {c['unit']} ({c['source']})" for c in ex["claims"]))
    lines.append(f"Sky: {report['sky']['tiles']} tiles, {report['sky']['gap_tiles']} in the lowest coverage quartile or empty")
    return "\n".join(lines)
