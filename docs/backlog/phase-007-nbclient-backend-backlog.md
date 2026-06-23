# Phase 007 Backlog: Nbclient Notebook Backend

## P007-001: Install And Pin Notebook Execution Dependencies

- Stable item ID: `P007-001`
- Title: Install nbclient stack
- Rationale: Real Jupyter execution requires notebook packages and a kernel.
- Affected files/modules: `pyproject.toml`, `docs/installed-software.md`
- Implementation steps: Install `nbformat`, `nbclient`, `nbconvert`, and `ipykernel`; pin dependencies; record installed software.
- Unit test expectations: Imports and nbclient tests pass.
- E2E test expectations: 20-turn nbclient regression passes.
- Demo relevance: Demo uses nbclient backend.
- Acceptance criteria: Dependencies are installed and documented.
- Status: done

## P007-002: Implement Nbclient Backend

- Stable item ID: `P007-002`
- Title: Add nbclient notebook execution
- Rationale: The system needs a real Jupyter execution backend.
- Affected files/modules: `app/notebook_execution.py`
- Implementation steps: Add single-notebook and workspace nbclient execution helpers.
- Unit test expectations: Metadata shows `nbclient_executed`.
- E2E test expectations: 20 generated notebooks execute.
- Demo relevance: Summary records nbclient execution.
- Acceptance criteria: Nbclient execution captures success and failure counts.
- Status: done

## P007-003: Integrate Backend Into Regression

- Stable item ID: `P007-003`
- Title: Add regression backend selector
- Rationale: Regression must be able to enforce nbclient execution.
- Affected files/modules: `app/phase_regression.py`, `scripts/run_phase_regression.py`
- Implementation steps: Add backend argument, branch execution, and summary checks.
- Unit test expectations: Regression supports `notebook_execution_backend="nbclient"`.
- E2E test expectations: CLI with `--notebook-execution-backend nbclient` passes.
- Demo relevance: Demo command uses this option.
- Acceptance criteria: Summary reports backend `nbclient`.
- Status: done

## P007-004: Validate, Demo, Status, Commit

- Stable item ID: `P007-004`
- Title: Close Phase 007
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 007 docs and repository state.
- Implementation steps: Run tests, 20-turn nbclient regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 007 is locally committed.
- Status: done
