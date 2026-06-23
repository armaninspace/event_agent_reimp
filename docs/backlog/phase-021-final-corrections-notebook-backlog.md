# Phase 021 Backlog: Final Corrections Notebook

## P021-001: Write Final Corrections Notebook

- Stable item ID: `P021-001`
- Title: Add `999-multiple-testing-corrections` artifacts
- Rationale: Notebook-backed evidence needs an explicit final multiple-testing correction notebook.
- Affected files/modules: `app/notebook_workspace.py`
- Implementation steps: Render correction notebook, Markdown export, index/log/findings entries, and tests.
- Unit test expectations: Correction notebook writer is tested.
- E2E test expectations: 20-turn regression writes correction artifacts.
- Demo relevance: Correction notebook artifacts are phase evidence.
- Acceptance criteria: `.ipynb` and `.md` correction artifacts exist.
- Status: done

## P021-002: Execute And Audit Correction Notebook

- Stable item ID: `P021-002`
- Title: Add correction notebook execution/regression flags
- Rationale: The final notebook should be validated, not just written.
- Affected files/modules: `app/notebook_execution.py`, `app/phase_regression.py`, `app/replication_audit.py`
- Implementation steps: Execute correction notebook, summarize status, add regression/audit fields, and tests.
- Unit test expectations: Execution summaries and regression/audit tests assert flags.
- E2E test expectations: Phase regression reports correction notebook executed.
- Demo relevance: Audit records correction notebook execution.
- Acceptance criteria: Regression and audit report correction notebook presence/execution.
- Status: done

## P021-003: Validate, Demo, Status, Commit

- Stable item ID: `P021-003`
- Title: Close Phase 021
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 021 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, audit, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 021 is locally committed.
- Status: done
