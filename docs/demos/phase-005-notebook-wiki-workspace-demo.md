# Phase 005 Demo: Notebook And Wiki Workspace

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_phase_regression.py --phase-id phase-005-notebook-wiki-workspace --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Regression command runs 20 deterministic friends-loop turns.
- Each turn writes one scaffolded `.ipynb` and one Markdown export.
- Required wiki files exist and are updated.
- `phase_regression_summary.json` reports `notebook_workspace_present=True`.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
..................                                                       [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-005-notebook-wiki-workspace --turns 20
wrote app/runs/phase-005-notebook-wiki-workspace/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
```

```text
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
18 passed in 0.17s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated regression summary:

```text
app/runs/phase-005-notebook-wiki-workspace/phase_regression_summary.json
```

Workspace summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
current_required_artifacts_exist: True
notebook_workspace_present: True
telemetry_event_count: 161
notebook_count: 20
markdown_export_count: 20
wiki_files_exist: True
```

Notebook workspace:

```text
app/runs/phase-005-notebook-wiki-workspace/notebooks/
```

The workspace contains 48 files: 8 wiki files, 20 scaffolded notebooks, and 20 Markdown exports.

## 20-Turn Regression

Implemented and passed. The regression gate now requires the notebook workspace.

## Video

No video was generated. This is a non-UI CLI/notebook-artifact phase, and command-output evidence plus generated notebooks/wiki files are the relevant demo outputs.

## Known Gaps

- Notebooks are scaffolded only and are not executed.
- `nbformat`, `nbclient`, and `nbconvert` are not installed yet.
- Business report and playback UI remain deferred.
- Live Microsoft Agent Framework orchestration remains deferred.

## Requirement Mapping

- Workspace writer: `app/notebook_workspace.py`
- Friends-loop integration: `app/friends_loop.py`
- Regression gate check: `app/phase_regression.py`
- Tests: `tests/test_notebook_workspace.py`, `tests/test_friends_loop.py`, `tests/test_phase_regression.py`
