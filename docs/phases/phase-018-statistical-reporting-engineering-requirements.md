# Phase 018: Statistical Evidence Reporting

## Phase Goal

Render attached statistical evidence in stakeholder-facing business reports and notebook/wiki memory so the statistical execution artifacts are inspectable without opening raw JSON.

## Requirements

- Render statistical evidence in the business evidence report.
- Escape statistical result IDs and caveats in HTML.
- Render statistical evidence in per-turn Markdown notebooks.
- Append statistical evidence summaries to wiki findings.
- Preserve backward compatibility for turn records without statistical evidence.
- Keep 20-turn regression passing.

## Non-Goals

- New statistical calculations.
- Interactive charting.
- Publication-grade report design.
- Live model narration.

## Assumptions

- Phase 017 attaches statistical evidence to turn records.
- Reports should keep causal caveats visible.
- Static HTML and Markdown are sufficient for this phase.

## Affected Layers

- Business report rendering
- Notebook Markdown export
- Wiki findings
- Tests
- Documentation

## Affected Modules

- `app/reporting.py`
- `app/notebook_workspace.py`
- `tests/test_reporting.py`
- `tests/test_notebook_workspace.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

Rendering is purely presentational. The report and notebook layers read `turn["statistical_evidence"]` when present and omit the section when absent. This keeps older artifacts and narrow tests compatible.

## Data/API/Config Changes

- Business report sections include statistical evidence summaries.
- Turn Markdown exports include statistical evidence summaries.
- `findings.md` records attached statistical evidence counts and minimum adjusted p-values.

## Demo Requirements

- Run renderer tests.
- Run 20-turn regression.
- Verify generated report and notebook/wiki outputs contain statistical evidence.
- Record validation output.

## Test Requirements

- Business report escapes statistical evidence content.
- Notebook Markdown includes statistical evidence content.
- Wiki findings record attached statistical results.
- Validation passes.

## Security/Sandbox Considerations

- Escape forum/statistical text in HTML.
- Preserve observational caveats.

## Risks

- Static summaries can still be overinterpreted without context.
- Detailed statistical tables remain in JSON rather than fully rendered HTML tables.

## Acceptance Criteria

- Business report renders statistical evidence.
- Notebook Markdown renders statistical evidence.
- Wiki findings record statistical evidence summaries.
- 20-turn regression still passes.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 018 commit or remove rendering changes, tests, artifacts, and docs.
