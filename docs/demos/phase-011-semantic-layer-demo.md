# Phase 011 Demo: Semantic SQL Layer

## Setup

Run from the repository root:

```sh
cd /code
```

DuckDB was installed:

```sh
python3 -m pip install duckdb
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_semantic_smoke.py --output-dir app/runs/phase-011-semantic-layer
python3 scripts/run_phase_regression.py --phase-id phase-011-semantic-layer --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Semantic smoke writes JSON and Markdown artifacts.
- Queries run only against whitelisted views.
- Row limit is applied.
- 20-turn regression still passes.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
....................................                                     [100%]
```

```text
python3 scripts/run_semantic_smoke.py --output-dir app/runs/phase-011-semantic-layer
wrote app/runs/phase-011-semantic-layer/semantic_smoke.json
wrote app/runs/phase-011-semantic-layer/semantic_smoke.md
views=city_week_events rows=10 columns=week_start_monday,revenue_all,has_game
views=msa_week_events rows=10 columns=msa_code,week_start_monday,merchants_all
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-011-semantic-layer --turns 20
wrote app/runs/phase-011-semantic-layer/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

```text
bash scripts/validate.sh
36 passed in 15.90s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated semantic artifacts:

```text
app/runs/phase-011-semantic-layer/semantic_smoke.json
app/runs/phase-011-semantic-layer/semantic_smoke.md
```

Semantic smoke summary:

```text
schema_version: phase-011.semantic-smoke.v1
results: 2
city_week_events rows=10 columns=week_start_monday,revenue_all,has_game
msa_week_events rows=10 columns=msa_code,week_start_monday,merchants_all
```

## 20-Turn Regression

Implemented and passed after adding the semantic layer.

## Video

No video was generated. This is a non-UI SQL/data-access phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- SQL relation extraction is conservative and not a full parser.
- No persistent semantic cache is written.
- Agent-generated SQL is not implemented yet.

## Requirement Mapping

- Semantic layer: `app/semantic_layer.py`
- Smoke command: `scripts/run_semantic_smoke.py`
- Tests: `tests/test_semantic_layer.py`
