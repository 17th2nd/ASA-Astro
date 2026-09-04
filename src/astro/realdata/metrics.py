"""Rank-agreement metrics, pure Python, deterministic. Declared in the manifest before any result was seen."""

from __future__ import annotations

import random
from typing import Sequence


def average_ranks(values: Sequence[float | None]) -> list[float]:
    """1-based tie-averaged ranks, higher value = better (rank 1). None values tie below every ranked value."""
    n = len(values)
    idx = list(range(n))
    idx.sort(key=lambda i: (values[i] is None, -(values[i] if values[i] is not None else 0.0)))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[idx[j + 1]] == values[idx[i]]:
            j += 1
        r = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[idx[k]] = r
        i = j + 1
    return ranks


def spearman(scores: Sequence[float | None], grades: Sequence[float]) -> float | None:
    n = len(scores)
    if n < 3:
        return None
    ra, rb = average_ranks(scores), average_ranks([float(g) for g in grades])
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((a - ma) * (b - mb) for a, b in zip(ra, rb))
    va = sum((a - ma) ** 2 for a in ra)
    vb = sum((b - mb) ** 2 for b in rb)
    if va == 0 or vb == 0:
        return None
    return cov / (va * vb) ** 0.5


def ordering(ids: Sequence[str], scores: Sequence[float | None]) -> list[str]:
    """Best first; ties and unranked candidates broken by id ascending."""
    return [ids[i] for i in sorted(range(len(ids)), key=lambda i: (scores[i] is None, -(scores[i] if scores[i] is not None else 0.0), ids[i]))]


def ndcg_at_k(order: Sequence[str], grade_of: dict[str, float], k: int) -> float:
    import math
    dcg = sum(grade_of[o] / math.log2(i + 2) for i, o in enumerate(order[:k]))
    ideal = sorted(grade_of.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0


def precision_at_k(order: Sequence[str], grade_of: dict[str, float], k: int, min_grade: float = 2.0) -> float:
    top = order[:k]
    return sum(1 for o in top if grade_of[o] >= min_grade) / len(top) if top else 0.0


def bootstrap_ci(ids: Sequence[str], grade_of: dict[str, float], method_scores: dict[str, float | None], other_scores: dict[str, float | None] | None,
                 resamples: int, seed: int) -> dict:
    """Paired bootstrap over candidates: percentile 95% CI of rho(method) (and of rho(method) - rho(other) when given)."""
    rng = random.Random(seed)
    ids = list(ids)
    n = len(ids)
    vals, diffs = [], []
    for _ in range(resamples):
        sample = [ids[rng.randrange(n)] for _ in range(n)]
        g = [grade_of[s] for s in sample]
        r1 = spearman([method_scores.get(s) for s in sample], g)
        if r1 is None:
            continue
        vals.append(r1)
        if other_scores is not None:
            r2 = spearman([other_scores.get(s) for s in sample], g)
            if r2 is not None:
                diffs.append(r1 - r2)
    def ci(xs):
        if not xs:
            return None
        xs = sorted(xs)
        lo, hi = xs[int(0.025 * (len(xs) - 1))], xs[int(0.975 * (len(xs) - 1))]
        return [round(lo, 4), round(hi, 4)]
    return {"rho_ci95": ci(vals), "diff_ci95": ci(diffs) if other_scores is not None else None, "resamples_used": len(vals)}
