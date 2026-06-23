# Phase 007 Demo: Nbclient Notebook Backend

## Setup

Run from the repository root:

```sh
cd /code
```

Notebook execution packages were installed:

```sh
python3 -m pip install nbformat nbclient nbconvert ipykernel
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_phase_regression.py --phase-id phase-007-nbclient-backend --turns 20 --notebook-execution-backend nbclient
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Regression command runs 20 deterministic friends-loop turns.
- All 20 generated notebooks execute through nbclient.
- Regression summary reports backend `nbclient`, 20 executed notebooks, and zero failures.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.......................                                                  [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-007-nbclient-backend --turns 20 --notebook-execution-backend nbclient
wrote app/runs/phase-007-nbclient-backend/phase_regression_summary.json
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
23 passed in 17.54s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated regression summary:

```text
app/runs/phase-007-nbclient-backend/phase_regression_summary.json
```

Summary fields:

```text
requested_turns: 20
completed_workflows: 20
notebook_workspace_present: True
backend: nbclient
executed_notebook_count: 20
failed_notebook_count: 0
all_nbclient_executed: True
notebook_count: 20
markdown_export_count: 20
nbclient_executed_count: 20
wiki_files_exist: True
```

## 20-Turn Regression

Implemented and passed with the `nbclient` backend.

## Video

No video was generated. This is a non-UI CLI/notebook-execution phase, and command-output evidence plus generated executed notebooks are the relevant demo outputs.

## Known Gaps

- Jupyter emitted local kernel TCP transport warnings during the 20-turn run. The command completed successfully; this is documented as a local execution warning.
- `nbclient_executed` still does not mean statistically validated.
- Business report and playback UI remain deferred.

## Requirement Mapping

- Nbclient backend: `app/notebook_execution.py`
- Regression backend selector: `app/phase_regression.py`, `scripts/run_phase_regression.py`
- Dependency pins: `pyproject.toml`
- Tests: `tests/test_notebook_execution.py`, `tests/test_phase_regression.py`
