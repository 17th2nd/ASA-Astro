# ASTRO real-data test 001 — founder summary

**Verdict: FAIL** (by the rules written down before the run).

**What we tested.** We asked the Astro engine one real question: which known transiting planets most need a fresh
timing observation so their predicted transits stay usable in 2029. We gave it the NASA Exoplanet Archive's published
ephemerides and Gaia data for 100 randomly chosen planets, and compared its ranking with the priority labels published
independently by ExoClock, a professional programme that exists to do exactly this. We also ranked the same 100 planets
with simple methods: brightest first, largest published period error first, and two "how connected is it in the
graph" measures.

**Did ASTRO work on real data?** Mechanically, yes. It evaluated all 100, produced the same answer when rebuilt from
scratch, and every score is traceable to named evidence. It refused to rank anything when the uncertainties were removed,
which is the right behaviour.

**Did it beat the simple baseline?** No. Its agreement with ExoClock (ρ = 0.27) was about the same as "brightest first"
(0.26) and clearly worse than "largest published period error first" (0.40). It did beat the graph measures, which were
no better than random.

**Did relationships add value?** No. Removing them changed nothing. On this task every candidate has the same one
relationship, so there was nothing for them to add.

**Did Context add value?** It behaved correctly (changing the epoch or the telescope limit changed exactly what it should),
but it did not improve agreement with the reference, except that restricting to bright stars happened to help — because
ExoClock's priorities lean towards brighter stars.

**Did uncertainty improve the result?** It is the only thing carrying the signal. But the engine's way of using it
(projecting the error forward in time) did worse than the raw published error. And we found a defect: when only one of
the two uncertainties is missing, the engine silently treats it as zero and still scores the star. That failed a check we
had pre-registered as critical.

**Was the result mostly ordinary graph centrality?** No. ASTRO's ranking is almost unrelated to degree or PageRank.

**Single next recommended action.** Fix the silent zero-uncertainty defect in the drift feature (abstain, or say so in the
trace) — and do not run another value test until an astronomer, not the operator, has declared an objective on a task
where relationships actually carry information. This test shows the engine is honest and reproducible; it does not show
that it is useful.

This is an engineering result about the software. It is not scientific validation of anything, and the frozen
scientific programme is untouched.
