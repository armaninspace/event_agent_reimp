# Phase 017 Demo: Governed Statistical Execution

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_statistical_execution.py tests/test_friends_loop.py tests/test_phase_regression.py -q
python3 scripts/run_statistical_execution_smoke.py --output-dir app/runs/phase-017-statistical-execution
python3 scripts/run_phase_regression.py --phase-id phase-017-statistical-execution --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Statistical execution tests pass.
- Smoke command writes JSON and Markdown artifacts.
- Smoke report contains eight corrected statistical results.
- Every turn carries `statistical_evidence`.
- Telemetry includes `statistics.attached` once per turn.
- 20-turn regression reports statistical evidence coverage.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest tests/test_statistical_execution.py tests/test_friends_loop.py tests/test_phase_regression.py -q
........                                                                 [100%]
```

```text
python3 scripts/run_statistical_execution_smoke.py --output-dir app/runs/phase-017-statistical-execution
wrote app/runs/phase-017-statistical-execution/statistical_execution_smoke.json
wrote app/runs/phase-017-statistical-execution/statistical_execution_smoke.md
result_count=8
method=Benjamini-Hochberg FDR correction
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-017-statistical-execution --turns 20
wrote app/runs/phase-017-statistical-execution/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
turns_have_statistical_evidence=True
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

## Evidence

Generated statistical execution artifacts:

```text
app/runs/phase-017-statistical-execution/statistical_execution_smoke.json
app/runs/phase-017-statistical-execution/statistical_execution_smoke.md
app/runs/phase-017-statistical-execution/phase_regression_summary.json
```

Statistical execution smoke summary:

```text
schema_version: phase-017.statistical-execution.v1
result_count: 8
method: Benjamini-Hochberg FDR correction
```

First selected turn evidence:

```text
candidate_id: turn-01-crowd-spending
semantic_slot: city_week_event_spending
result_count: 4
has_adjusted_significance: True
min_adjusted_p_value: 2.4226335941393745e-68
result_ids:
- exploratory:city_week:revenue_all
- exploratory:city_week:merchants_all
- matched:city_week:revenue_all
- matched:city_week:merchants_all
```

Regression summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
turns_have_statistical_evidence: True
selected_candidate_count: 20
selected_candidates_have_required_metadata: True
statistics.attached events: 20
```

## 20-Turn Regression

Implemented and passed after attaching statistical evidence to selected turns.

## Video

No video was generated. This is a non-UI statistical execution phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- Evidence mapping is semantic-slot based.
- Results remain observational and exploratory.
- The business report does not yet render detailed statistical evidence sections.

## Requirement Mapping

- Statistical execution mapping: `app/statistical_execution.py`
- Loop integration: `app/friends_loop.py`
- Regression flag: `app/phase_regression.py`
- Smoke command: `scripts/run_statistical_execution_smoke.py`
- Tests: `tests/test_statistical_execution.py`, `tests/test_friends_loop.py`, `tests/test_phase_regression.py`
