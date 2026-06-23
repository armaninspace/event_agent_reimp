# Phase 007: Nbclient Notebook Backend

## Phase Goal

Add a real Jupyter `nbclient` execution backend for generated turn notebooks and prove it through the 20-turn regression gate.

## Requirements

- Install and document `nbformat`, `nbclient`, `nbconvert`, and `ipykernel`.
- Add an `nbclient` notebook execution backend.
- Add `--notebook-execution-backend nbclient` to the phase regression command.
- Run a 20-turn regression with nbclient execution.
- Regression summary must report 20 nbclient-executed notebooks and zero failures.
- Add tests for nbclient execution and regression integration.

## Non-Goals

- Statistical notebook validation.
- Business report or playback UI.
- Live Microsoft Agent Framework orchestration.
- Publishing or remote execution.

## Assumptions

- Generated notebooks are trusted project artifacts.
- Local Jupyter kernel execution is acceptable for regression.
- Kernel TCP warnings are local execution warnings and should be documented.

## Affected Layers

- Notebook execution
- Regression validation
- Dependencies
- Tests
- Documentation

## Affected Modules

- `app/notebook_execution.py`
- `app/notebook_workspace.py`
- `app/phase_regression.py`
- `scripts/run_phase_regression.py`
- `pyproject.toml`
- `tests/test_notebook_execution.py`
- `tests/test_phase_regression.py`

## Dependency/Library Choices

- `nbformat`: read/write notebook documents.
- `nbclient`: execute notebooks through a Jupyter kernel.
- `nbconvert`: future export support.
- `ipykernel`: Python kernel for nbclient execution.

## Architecture Notes

The regression command now accepts `--notebook-execution-backend lightweight|nbclient`. The default remains `lightweight` for speed, while Phase 007 demo and acceptance use `nbclient`.

## Data/API/Config Changes

- Adds notebook packages to `pyproject.toml`.
- Adds Phase 007 installed software records.
- Writes Phase 007 regression artifacts under `app/runs/phase-007-nbclient-backend/`.

## Demo Requirements

- Run `python3 scripts/run_phase_regression.py --phase-id phase-007-nbclient-backend --turns 20 --notebook-execution-backend nbclient`.
- Record executed notebook count and failure count.
- Record validation output.

## Test Requirements

- Tests verify nbclient execution updates metadata.
- Tests verify workspace nbclient execution counts all notebooks.
- Tests verify phase regression supports nbclient backend.
- Validation passes.

## Security/Sandbox Considerations

- Execute only generated notebooks.
- Do not make external network/model calls.
- Document local Jupyter TCP warning.
- Do not read `.env`.

## Risks

- `nbclient` execution is slower than lightweight execution.
- Jupyter emits local TCP transport warnings.
- `nbclient_executed` is stronger than lightweight execution but still not statistical validation.

## Acceptance Criteria

- 20-turn nbclient regression completes.
- Summary reports backend `nbclient`, 20 executed notebooks, zero failures, and notebook workspace present.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 007 commit or remove nbclient integration, generated artifacts, tests, dependency pins, and Phase 007 docs.
