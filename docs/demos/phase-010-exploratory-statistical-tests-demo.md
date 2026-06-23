# Phase 010 Demo: Exploratory Statistical Tests

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_statistical_smoke.py --output-dir app/runs/phase-010-exploratory-statistical-tests
python3 scripts/run_phase_regression.py --phase-id phase-010-exploratory-statistical-tests --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Statistical smoke writes JSON and Markdown artifacts.
- Four exploratory comparisons run: city/MSA by revenue/merchants.
- All results include caveats.
- 20-turn regression still passes.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
................................                                         [100%]
```

```text
python3 scripts/run_statistical_smoke.py --output-dir app/runs/phase-010-exploratory-statistical-tests
wrote app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.json
wrote app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.md
results=4
not_testable_count=0
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-010-exploratory-statistical-tests --turns 20
wrote app/runs/phase-010-exploratory-statistical-tests/phase_regression_summary.json
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
32 passed in 20.42s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated statistical artifacts:

```text
app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.json
app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.md
```

Statistical smoke summary:

```text
schema_version: phase-010.exploratory-statistical-tests.v1
results: 4
not_testable_count: 0
all_results_have_caveats: True
city_week revenue_all: status=ok, exposed_rows=2277, unexposed_rows=3500, mean_difference=0.028791
city_week merchants_all: status=ok, exposed_rows=2277, unexposed_rows=3500, mean_difference=0.052018
msa_week revenue_all: status=ok, exposed_rows=2542, unexposed_rows=46181, mean_difference=-0.044792
msa_week merchants_all: status=ok, exposed_rows=2542, unexposed_rows=46181, mean_difference=0.025355
```

## 20-Turn Regression

Implemented and passed after adding the statistics layer.

## Video

No video was generated. This is a non-UI statistical smoke phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- Comparisons are descriptive exposed-vs-unexposed summaries, not full matched controls.
- No p-values or multiple-testing correction yet.
- Results must not be treated as causal proof.

## Requirement Mapping

- Statistical scaffold: `app/statistical_tests.py`
- Smoke command: `scripts/run_statistical_smoke.py`
- Tests: `tests/test_statistical_tests.py`
