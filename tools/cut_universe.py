"""Cut a cone out of a universe JSON: entities within ``radius_deg`` of (ra, dec), their evidence, the
relationships whose participants all remain, and their states. Real data stays labelled real; the
label records the cut so no one mistakes the piece for the whole.

    PYTHONPATH=src python3 tools/cut_universe.py var/universe-real-frontier-tess-v2.json 291.0 42.0 6.0 var/universe-kepler-cone.json
"""

from __future__ import annotations

import json
import math
import sys


def sep_deg(ra1, dec1, ra2, dec2):
    r1, d1, r2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    a = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2
    return math.degrees(2 * math.asin(min(1.0, math.sqrt(a))))


def main(src, ra, dec, radius, dst):
    ra, dec, radius = float(ra), float(dec), float(radius)
    U = json.load(open(src))
    keep = set()
    for e in U["entities"]:
        c = e.get("coordinates")
        if c is None or e["kind"] in ("observatory_site", "instrument", "site"):
            keep.add(e["entity_id"])          # sites, instruments and anything not on the sky travel with every cut
        elif sep_deg(ra, dec, c["ra_deg"], c["dec_deg"]) <= radius:
            keep.add(e["entity_id"])
    # companions (planets carry the host's coordinates) follow their host
    for r in U["relationships"]:
        if r["relationship_type"] == "hosts" and any(i in keep for i in r["roles"].get("host", ())):
            keep.update(x for v in r["roles"].values() for x in v)
    rels = []
    for r in U["relationships"]:
        ids = [x for v in r["roles"].values() for x in v]
        if all(i in keep for i in ids):
            rels.append(r)
    ents = [e for e in U["entities"] if e["entity_id"] in keep]
    evs = [x for x in U["evidence"] if x["subject_id"] in keep]
    sts = [s for s in U.get("states", []) if s["entity_id"] in keep]
    out = dict(U)
    out.update(label=f"{U.get('label', 'universe')} | cone ra={ra} dec={dec} r={radius}deg", entities=ents, evidence=evs, relationships=rels, states=sts)
    for k in ("universe_id", "digest"):
        out.pop(k, None)
    json.dump(out, open(dst, "w"))
    print(json.dumps({"entities": len(ents), "evidence": len(evs), "relationships": len(rels), "states": len(sts),
                      "kinds": sorted({e["kind"] for e in ents})}))


if __name__ == "__main__":
    main(*sys.argv[1:6])
