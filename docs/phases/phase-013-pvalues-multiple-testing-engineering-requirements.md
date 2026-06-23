# Phase 013: P-Values And Multiple Testing

## Phase Goal

Add statistical p-values and Benjamini-Hochberg multiple-testing correction for exploratory and matched smoke outputs, while preserving observational claim boundaries.

## Requirements

- Compute Welch two-sample p-values for exposed-vs-unexposed exploratory comparisons.
- Compute one-sample t-test p-values for matched-control differences.
- Apply Benjamini-Hochberg adjusted p-values across all smoke results.
- Preserve diagnostics and caveats.
- Write JSON and Markdown correction artifacts.
- Add tests for p-value calculation, BH adjustment, and artifact writing.
- Keep 20-turn regression passing.

## Non-Goals

- Causal claim promotion.
- Human publication workflow.
- Rich effect-size modeling.

## Assumptions

- SciPy is acceptable for statistical p-values.
- Current tests are exploratory and observational.
- Adjusted p-values are evidence metadata, not proof.

## Affected Layers

- Statistical execution
- Multiple-testing correction
- Tests
- Documentation

## Affected Modules

- `app/multiple_testing.py`
- `scripts/run_correction_smoke.py`
- `tests/test_multiple_testing.py`
- Phase 013 docs under `docs/`

## Dependency/Library Choices

- `scipy`: t-tests and p-values.

## Architecture Notes

Correction combines results from exploratory and matched smoke runners into a single family and applies Benjamini-Hochberg correction. This keeps the audit trail explicit and avoids mutating old per-turn notebooks.

## Data/API/Config Changes

- Reads final reference CSVs.
- Writes correction artifacts under `app/runs/phase-013-pvalues-multiple-testing/`.

## Demo Requirements

- Run correction smoke command.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Tests cover BH adjustment monotonicity.
- Tests cover p-value output fields.
- Tests cover artifact writing.
- Validation passes.

## Security/Sandbox Considerations

- Do not claim causality.
- Do not mutate source CSVs.

## Risks

- P-values can be overinterpreted without study-design context.
- Multiple-testing correction does not fix observational confounding.

## Acceptance Criteria

- Correction smoke artifacts are written.
- Results include raw and adjusted p-values.
- Tests and validation pass.
- 20-turn regression still passes.

## Rollback Plan

Revert the Phase 013 commit or remove correction module, smoke script, tests, artifacts, dependency pin, and docs.
