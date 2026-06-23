# Phase 006 Demo: Lightweight Notebook Execution

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_phase_regression.py --phase-id phase-006-lightweight-notebook-execution --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Regression command runs 20 deterministic friends-loop turns.
- Each generated notebook includes and executes a validation code cell.
- Notebook metadata records `lightweight_executed`.
- Regression summary reports 20 executed notebooks and zero failures.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
....................                                                     [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-006-lightweight-notebook-execution --turns 20
wrote app/runs/phase-006-lightweight-notebook-execution/phase_regression_summary.json
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
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
20 passed in 0.21s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated regression summary:

```text
app/runs/phase-006-lightweight-notebook-execution/phase_regression_summary.json
```

Summary fields:

```text
requested_turns: 20
completed_workflows: 20
notebook_workspace_present: True
notebook_count: 20
markdown_export_count: 20
lightweight_executed_count: 20
executed_notebook_count: 20
failed_notebook_count: 0
all_lightweight_executed: True
```

Representative notebook metadata:

```text
status: lightweight_executed
execution_backend: lightweight
executed_code_cells: 1
stdout: validation_contract_passed
```

## 20-Turn Regression

Implemented and passed. The regression gate now requires the notebook workspace and lightweight notebook execution.

## Video

No video was generated. This is a non-UI CLI/notebook-execution phase, and command-output evidence plus executed notebook artifacts are the relevant demo outputs.

## Known Gaps

- Lightweight execution is not full Jupyter kernel execution.
- `nbclient` backend remains deferred.
- Notebooks validate generated contract fields only; they are not statistical validation.
- Business report and playback UI remain deferred.

## Requirement Mapping

- Lightweight executor: `app/notebook_execution.py`
- Validation cells: `app/notebook_workspace.py`
- Regression gate: `app/phase_regression.py`
- Tests: `tests/test_notebook_execution.py`, `tests/test_notebook_workspace.py`, `tests/test_phase_regression.py`
