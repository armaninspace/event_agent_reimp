# Phase 021: Final Corrections Notebook

## Phase Goal

Remediate the notebook-backed evidence gap by adding a dedicated final `999-multiple-testing-corrections.ipynb` and Markdown export to each regression workspace.

## Requirements

- Write `999-multiple-testing-corrections.ipynb`.
- Write `999-multiple-testing-corrections.md`.
- Include the Benjamini-Hochberg correction method and corrected result rows.
- Execute the correction notebook in lightweight and nbclient regression paths.
- Keep turn notebook counts equal to requested turns.
- Add separate regression and audit flags for correction notebook presence/execution.
- Keep 20-turn regression passing.

## Non-Goals

- Interactive statistical charts.
- Full report redesign.
- New statistical methods.

## Assumptions

- The correction notebook can reuse the existing Phase 013 correction report.
- The correction notebook is an additional final notebook, not one of the per-turn notebooks.

## Affected Layers

- Notebook workspace
- Notebook execution
- Phase regression
- Final audit
- Tests
- Documentation

## Affected Modules

- `app/notebook_workspace.py`
- `app/notebook_execution.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_notebook_workspace.py`
- `tests/test_notebook_execution.py`
- `tests/test_phase_regression.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The correction notebook is managed separately from turn notebooks. `notebook_count` and `markdown_export_count` still count only `turn-*.ipynb` and `turn-*.md`; the final correction notebook has explicit presence/execution flags.

## Data/API/Config Changes

- Workspace summaries gain correction notebook presence/status/execution fields.
- Notebook execution summaries gain correction notebook execution result fields.
- Phase regression summaries gain `correction_notebook_present` and `correction_notebook_executed`.
- Replication audits gain correction notebook presence/execution fields.

## Demo Requirements

- Run focused notebook/regression/audit tests.
- Run a 20-turn regression.
- Run replication audit against the new run.
- Record validation output.

## Test Requirements

- Correction notebook writer creates `.ipynb` and `.md`.
- Workspace summary detects correction artifacts.
- Execution summaries expose correction notebook status.
- Regression and audit require correction notebook presence/execution.
- Validation passes.

## Security/Sandbox Considerations

- Do not mutate source CSVs.
- Preserve observational caveats.

## Risks

- The notebook validates the correction artifact contract, not external causal validity.
- Detailed result interpretation still depends on reading caveats.

## Acceptance Criteria

- `999-multiple-testing-corrections.ipynb` exists.
- `999-multiple-testing-corrections.md` exists.
- Correction notebook executes.
- Regression reports correction notebook presence/execution.
- Audit reports correction notebook presence/execution.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 021 commit or remove correction notebook writer/execution integration, regression/audit fields, tests, artifacts, and docs.
