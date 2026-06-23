# Phase 012: Matched Control Tests

## Phase Goal

Add deterministic matched-control exploratory tests using same-week and same-block controls for city-week and MSA-week final runtime files.

## Requirements

- Implement matched-control comparisons for `revenue_all` and `merchants_all`.
- Match exposed rows to unexposed controls with the same `week_start_monday` and block identifier.
- Use `event_msa_block_id` for city-week and `msa_block_id` for MSA-week.
- Report matched exposed rows, unmatched exposed rows, mean matched difference, diagnostics, and caveats.
- Add smoke script writing JSON/Markdown artifacts.
- Add tests for matched positive and not-testable cases.
- Keep 20-turn regression passing.

## Non-Goals

- P-values.
- Adjusted p-values.
- Multiple-testing correction.
- Causal claim promotion.

## Assumptions

- Same-week/same-block controls are a reasonable first deterministic matching scaffold.
- Later phases will add richer diagnostics and inferential tests.

## Affected Layers

- Statistical execution
- Smoke validation
- Tests
- Documentation

## Affected Modules

- `app/matched_tests.py`
- `scripts/run_matched_smoke.py`
- `tests/test_matched_tests.py`
- Phase 012 docs under `docs/`

## Dependency/Library Choices

No new dependencies are required.

## Architecture Notes

The matched test layer is separate from the descriptive statistics layer. It can later be called only for fully routed `statistical_hypothesis` candidates.

## Data/API/Config Changes

- Reads final reference CSVs under `data/reference/`.
- Writes matched smoke artifacts under `app/runs/phase-012-matched-control-tests/`.

## Demo Requirements

- Run matched smoke command.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Tests cover matched difference calculation.
- Tests cover not-testable cases with no controls.
- Tests cover artifact writing.
- Validation passes.

## Security/Sandbox Considerations

- Do not mutate source CSVs.
- Do not overclaim causal findings.

## Risks

- Same-block/same-week matching is a scaffold and may still be confounded.
- No p-values or multiple-testing correction yet.

## Acceptance Criteria

- Matched smoke artifacts are written.
- Results include diagnostics and caveats.
- Tests and validation pass.
- 20-turn regression still passes.

## Rollback Plan

Revert the Phase 012 commit or remove matched test module, smoke script, tests, artifacts, and docs.
