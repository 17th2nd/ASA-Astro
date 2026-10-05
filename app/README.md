# ASA-Astro V1 application — thin slice

**Scope (ASA Chief, 2026-10-05):** pin → kernel snapshot → exactly one Objective → digest-identified
receipt, shown in an API and a browser UI with honesty labels (hypothesis vs established),
unknowns and next evidence listed separately. Upload bar (preserve source → process_observation consume → thin Objective receipt + honesty) is landed;
sky maps / graph view remain deferred. Status: **SELF_ACCEPTANCE=NO. LOCAL_ONLY.**

## Run (one command)

From the repository root (worktree root):

```bash
PYTHONPATH=src:. python3 -m app.server
```

- URL: <http://127.0.0.1:8765/> (change with `--host` / `--port`, defaults in `app/config.json`)
- Data directory: `app/var/runs/<RCPT-…>/` (gitignored). Override with `ASA_ASTRO_APP_DATA_DIR=/path`.
- Dependencies: Python ≥ 3.11 standard library + the repo's own pinned deps (`requirements.lock`). No web framework, no npm build, no CDN.
- Precondition: the pinned ASA checkout must exist at `.asa/ASA` at the pinned SHA. Materialise it with
  `python3 tools/asa_baseline.py --config config/asa-baseline-current-dev.json`
  (or, offline, `git clone --no-checkout <local ASA mirror> .asa/ASA && git -C .asa/ASA checkout --detach <sha>`).
  The server refuses to start if `tools/asa_baseline.py` does not verify the checkout.

## The pin

The app uses exactly the pin landed by commit `633f837a` ("feat(integration): current-dev ASA pin at remediation-133"):
`config/asa-baseline-current-dev.json` → `sha = c2ccd7d55e34d7ffe03fd21d8b633cde69c152d2`
(ref `agent/asa-v1-rc0-final-falsification-remediation-133`). `app/config.json:asa_pin_file` names that file; the SHA is
never duplicated in app code or config. The historical `config/asa-baseline.json` (`b855d4c`) is untouched.

## What a run does

1. **Pin** — `tools/asa_baseline.py verify(config_path=…)` checks `.asa/ASA` is clean and at the pinned SHA; the app sets
   `ASTRO_ASA_BASELINE_CONFIG` to the pin file so `astro.asa.locator` (a200dda) verifies and loads the same pin.
2. **Snapshot** — the repo example universe `data/universe/slice1.json` (labelled *synthetic*) is loaded into an in-memory
   pinned kernel via `AstroAdapter` (+ the app compat shim, GAPS G-PIN-2); `adapter.snapshot()` gives the kernel digest/head/seq.
3. **One Objective** — `astro.pipeline.decide(universe, objective, context, adapter)` evaluates the chosen objective
   (default `data/objectives/A-exoplanet-transit-followup.json`, context `data/contexts/night-2026-09-03.json`).
4. **Receipt** — `AstroDecisionReceipt` (`RCPT-<sha256 of canonical body>`); the app recomputes the digest and records
   `receipt_id_verified`. Re-running with identical inputs reproduces the identical receipt id (logged in `invocations.jsonl`).

Artifacts per run: `pin.json snapshot.json objective.json context.json evaluation.json plan.json receipt.json receipt.sha256 run.json view.json invocations.jsonl`.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/pin` | verified pin record |
| GET | `/api/objectives` | objectives available (one per run) |
| POST | `/api/runs` `{"objective": "<slug>"}` | run the slice; 201 new, 200 reproduced |
| POST | `/api/runs` multipart (`source` file, optional `metadata`, `objective`) | upload → preserve source (sha256) → optional `process_observation` → thin Objective receipt |
| GET | `/api/runs?q=` | list / search runs |
| GET | `/api/runs/<RCPT-…>` | labelled view |
| GET | `/api/runs/<RCPT-…>/artifacts/<name>` | raw artifact (traceability target of every cited field) |

## Honesty rules implemented

- Every displayed item carries `source: {artifact, pointer}` (JSON pointer into a run artifact); tests resolve every pointer.
- `established-in-ASA-state` requires: canonical ASA stance `endorsed`, lifecycle `registered`, evidence status `admissible`
  (for evidence) and data class `real`. It means established *inside this kernel state* — not empirical validation.
- Everything else is `hypothesis`, with the failing reasons shown. Objective scores, ranks, explanations and plans are always
  `hypothesis`. Digests and verified checkouts are `record` (engineering facts, not science).
- Unknowns and next evidence are derived only from existing fields (unavailable features, failed `required_evidence`
  eligibility, contested evidence, unevaluated relationships, trace model limitations, pin status) and listed separately.

## Tests

```bash
PYTHONPATH=src:. python3 -m unittest discover -s tests/app -t .
```
