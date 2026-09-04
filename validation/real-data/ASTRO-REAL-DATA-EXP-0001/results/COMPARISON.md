# ASTRO-REAL-DATA-EXP-0001 — comparison table

Run 2026-09-04T09:34:40Z · commit `00118ff1099ff65e59d27d08b2165b242e334071` · manifest sha256 `b6895cc59aca1571e7e9337e373c04579c5e53f1af386644196c204bde6a9452`

## primary (n = 100; grades {'alert': 2, 'high': 40, 'medium': 22, 'low': 36})

| method | Spearman ρ | NDCG@25 | P@25 (grade ≥ 2) | unranked |
|---|---:|---:|---:|---:|
| astro | 0.2745 | 0.4898 | 0.56 | 0 |
| brightness | 0.2584 | 0.4485 | 0.52 | 0 |
| sigma_period | 0.3953 | 0.5688 | 0.72 | 0 |
| degree | 0.0388 | 0.306 | 0.4 | 0 |
| pagerank | 0.0485 | 0.3917 | 0.44 | 0 |
| random (diagnostic) | 0.0417 | 0.3486 | 0.44 | 0 |
| projected_uncertainty_formula (diagnostic) | 0.2189 | 0.4898 | 0.56 | 0 |

Bootstrap 95% CIs (paired, 2000 resamples):

- astro: ρ CI [0.0657, 0.454]
- astro_minus_brightness: ρ CI [0.0657, 0.454], difference CI [-0.2431, 0.2564]
- astro_minus_sigma_period: ρ CI [0.0657, 0.454], difference CI [-0.2583, 0.0163]
- astro_minus_degree: ρ CI [0.0657, 0.454], difference CI [-0.0095, 0.4616]
- astro_minus_pagerank: ρ CI [0.0657, 0.454], difference CI [-0.0376, 0.4875]

## pool (secondary, non-decisive) (n = 527; grades {'alert': 24, 'high': 183, 'medium': 110, 'low': 210})

| method | Spearman ρ | NDCG@25 | P@25 (grade ≥ 2) | unranked |
|---|---:|---:|---:|---:|
| astro | 0.1346 | 0.6299 | 0.84 | 0 |
| brightness | 0.0993 | 0.457 | 0.64 | 0 |
| sigma_period | 0.3971 | 0.6833 | 0.96 | 0 |
| degree | -0.0355 | 0.5172 | 0.68 | 0 |
| pagerank | -0.0448 | 0.5085 | 0.68 | 0 |
| random (diagnostic) | 0.0208 | 0.3528 | 0.4 | 0 |
| projected_uncertainty_formula (diagnostic) | 0.1776 | 0.6237 | 0.84 | 0 |

## pool + leakage-flagged (secondary, non-decisive) (n = 588; grades {'alert': 25, 'high': 197, 'medium': 131, 'low': 235})

| method | Spearman ρ | NDCG@25 | P@25 (grade ≥ 2) | unranked |
|---|---:|---:|---:|---:|
| astro | 0.1129 | 0.5869 | 0.76 | 0 |
| brightness | 0.0958 | 0.4371 | 0.6 | 0 |
| sigma_period | 0.3713 | 0.6744 | 0.96 | 0 |
| degree | -0.0427 | 0.5185 | 0.68 | 0 |
| pagerank | -0.0531 | 0.4841 | 0.6 | 0 |
| random (diagnostic) | 0.0061 | 0.3603 | 0.4 | 0 |
| projected_uncertainty_formula (diagnostic) | 0.1533 | 0.6046 | 0.8 | 0 |

## Topology similarity (primary)

Spearman(ASTRO, degree) = 0.1839; Spearman(ASTRO, PageRank) = 0.0806

## Objective E as declared (diagnostic)

status counts on the primary sample: {'eligible': 100, 'ineligible': 0, 'indeterminate': 0}; Spearman ρ = 0.2911

## Acceptance checks (metrics only; adversarial checks are combined in the report)

```
{
 "checks": {
  "rho_margin": {
   "brightness": false,
   "sigma_period": false,
   "degree": true,
   "pagerank": true
  },
  "ci_above_zero": true,
  "ndcg_not_below": {
   "brightness": true,
   "sigma_period": false,
   "degree": true,
   "pagerank": true
  },
  "topology_below_limit": {
   "degree": true,
   "pagerank": true
  },
  "reproduces_topology": false
 },
 "metric_verdict_before_adversarial": "FAIL"
}
```
