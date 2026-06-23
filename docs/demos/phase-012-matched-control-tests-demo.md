# Phase 012 Demo: Matched Control Tests

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_matched_smoke.py --output-dir app/runs/phase-012-matched-control-tests
python3 scripts/run_phase_regression.py --phase-id phase-012-matched-control-tests --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Matched smoke writes JSON and Markdown artifacts.
- Four matched comparisons run.
- Results include diagnostics and caveats.
- 20-turn regression still passes.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.......................................                                  [100%]
```

```text
python3 scripts/run_matched_smoke.py --output-dir app/runs/phase-012-matched-control-tests
wrote app/runs/phase-012-matched-control-tests/matched_smoke.json
wrote app/runs/phase-012-matched-control-tests/matched_smoke.md
results=4
not_testable_count=0
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-012-matched-control-tests --turns 20
wrote app/runs/phase-012-matched-control-tests/phase_regression_summary.json
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
39 passed in 18.95s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated matched artifacts:

```text
app/runs/phase-012-matched-control-tests/matched_smoke.json
app/runs/phase-012-matched-control-tests/matched_smoke.md
```

Matched smoke summary:

```text
schema_version: phase-012.matched-control-tests.v1
results: 4
not_testable_count: 0
all_results_have_caveats: True
city_week revenue_all: status=ok, matched_exposed_rows=1996, unmatched_exposed_rows=256, mean_matched_difference=-0.031760
city_week merchants_all: status=ok, matched_exposed_rows=1996, unmatched_exposed_rows=256, mean_matched_difference=-0.012456
msa_week revenue_all: status=ok, matched_exposed_rows=2542, unmatched_exposed_rows=0, mean_matched_difference=0.012501
msa_week merchants_all: status=ok, matched_exposed_rows=2542, unmatched_exposed_rows=0, mean_matched_difference=0.002611
```

## 20-Turn Regression

Implemented and passed after adding matched-control tests.

## Video

No video was generated. This is a non-UI statistical smoke phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- No p-values or adjusted p-values yet.
- Matching uses same week and same block only.
- Results remain observational and exploratory.

## Requirement Mapping

- Matched test scaffold: `app/matched_tests.py`
- Smoke command: `scripts/run_matched_smoke.py`
- Tests: `tests/test_matched_tests.py`
