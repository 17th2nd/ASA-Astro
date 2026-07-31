# Phase II validation harness

This Codex D-owned harness executes the committed Codex B and C interfaces without modifying
them. It uses the repository's deterministic synthetic image only; that fixture is not
astronomical Ground Truth.

Run from a clean checkout:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock
.venv/bin/pip install --no-deps -e .
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python \
  validation/run_phase2.py --output /tmp/asa-astro-phase2
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python \
  -m unittest discover -s tests -v
```

The output directory must not exist. The harness emits the preserved evidence bundle, five
Context-specific reasoning bundles, benchmark/adversarial/ablation results, explanation checks,
a self-contained `explorer.html`, and a SHA-256 manifest. Running it twice must produce identical
files.

The committed `validation/results/phase2/` directory is a deterministic record generated from
upstream commit `520f790a363660bbd97abf7f0f45f73cacc2d739`. It is an engineering benchmark, not a
scientific validation dataset or ASA-conformance result.
