# Phase 021 Demo: Final Corrections Notebook

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_notebook_workspace.py tests/test_notebook_execution.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-021-final-corrections-notebook --turns 20
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-021-final-corrections-notebook --output-dir app/runs/phase-021-final-corrections-notebook
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Focused notebook/regression/audit tests pass.
- 20-turn regression writes and executes `999-multiple-testing-corrections.ipynb`.
- Regression reports correction notebook presence/execution.
- Audit reports correction notebook presence/execution.
- Validation passes.

## Observed Behavior

Commands completed successfully.

```text
python3 -m pytest tests/test_notebook_workspace.py tests/test_notebook_execution.py tests/test_phase_regression.py -q
...........                                                              [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-021-final-corrections-notebook --turns 20
wrote app/runs/phase-021-final-corrections-notebook/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
turns_have_statistical_evidence=True
data_snapshot_complete=True
correction_notebook_present=True
correction_notebook_executed=True
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

```text
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-021-final-corrections-notebook --output-dir app/runs/phase-021-final-corrections-notebook
wrote app/runs/phase-021-final-corrections-notebook/replication_audit.json
wrote app/runs/phase-021-final-corrections-notebook/replication_audit.md
final_status=replicated_with_known_limits
completed_twenty_turns=True
selected_candidates_have_required_metadata=True
turns_have_statistical_evidence=True
business_report_statistical_sections=20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-021-final-corrections-notebook/notebooks/999-multiple-testing-corrections.ipynb
app/runs/phase-021-final-corrections-notebook/notebooks/999-multiple-testing-corrections.md
app/runs/phase-021-final-corrections-notebook/phase_regression_summary.json
app/runs/phase-021-final-corrections-notebook/replication_audit.json
```

Correction notebook evidence:

```text
correction_notebook_exists: True
correction_markdown_exists: True
correction_notebook_status: lightweight_executed
correction_notebook_executed: True
correction validation output: correction_contract_passed
Markdown contains Benjamini-Hochberg: True
Markdown contains matched city result: True
```

Regression summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
turns_have_statistical_evidence: True
data_snapshot_complete: True
correction_notebook_present: True
correction_notebook_executed: True
notebook_workspace_present: True
```

## 20-Turn Regression

Implemented and passed after adding the final corrections notebook.

## Video

No video was generated. This is a notebook evidence phase; generated notebook/Markdown artifacts and the regression summary are the relevant demo outputs.

## Known Gaps

- The correction notebook validates the correction artifact contract, not causal validity.
- No interactive charts are included.

## Requirement Mapping

- Correction notebook writer: `app/notebook_workspace.py`
- Execution integration: `app/notebook_execution.py`
- Regression integration: `app/phase_regression.py`
- Audit integration: `app/replication_audit.py`
- Tests: `tests/test_notebook_workspace.py`, `tests/test_notebook_execution.py`, `tests/test_phase_regression.py`, `tests/test_replication_audit.py`
