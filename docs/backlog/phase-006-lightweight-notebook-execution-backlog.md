# Phase 006 Backlog: Lightweight Notebook Execution

## P006-001: Add Validation Code Cells

- Stable item ID: `P006-001`
- Title: Include generated validation cells in turn notebooks
- Rationale: Notebooks need executable evidence objects, not only Markdown.
- Affected files/modules: `app/notebook_workspace.py`
- Implementation steps: Add a deterministic code cell with validation contract and assertion.
- Unit test expectations: Generated notebooks contain a code cell.
- E2E test expectations: 20-turn regression executes cells.
- Demo relevance: Executed notebooks are phase evidence.
- Acceptance criteria: Generated notebooks include validation contract code.
- Status: done

## P006-002: Implement Lightweight Executor

- Stable item ID: `P006-002`
- Title: Add lightweight notebook execution backend
- Rationale: Phase 006 acceptance requires code cells to execute and capture output.
- Affected files/modules: `app/notebook_execution.py`
- Implementation steps: Load notebook JSON, execute code cells, capture stdout, set outputs, execution counts, metadata, and write file.
- Unit test expectations: Execution output and metadata are tested.
- E2E test expectations: Regression executes all turn notebooks.
- Demo relevance: Summary reports executed count.
- Acceptance criteria: Execution status becomes `lightweight_executed`.
- Status: done

## P006-003: Tighten Regression Gate

- Stable item ID: `P006-003`
- Title: Require lightweight-executed notebooks in 20-turn regression
- Rationale: New evidence surface must be enforced by the regression gate.
- Affected files/modules: `app/phase_regression.py`, `tests/test_phase_regression.py`
- Implementation steps: Execute workspace notebooks during regression and add execution summary checks.
- Unit test expectations: Regression summary reports executed notebooks and zero failures.
- E2E test expectations: 20-turn regression passes.
- Demo relevance: Demo records summary fields.
- Acceptance criteria: Regression fails if notebooks are not executed.
- Status: done

## P006-004: Validate, Demo, Status, Commit

- Stable item ID: `P006-004`
- Title: Close Phase 006
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 006 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 006 is locally committed.
- Status: done
