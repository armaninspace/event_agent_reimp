# Phase 010: Exploratory Statistical Tests

## Phase Goal

Add a conservative exploratory statistical test scaffold over the final city-week and MSA-week runtime files, producing explicit diagnostics, caveats, and machine-readable smoke artifacts without claiming causality.

## Requirements

- Implement deterministic exposed-vs-unexposed comparisons for city-week and MSA-week files.
- Support outcomes `revenue_all` and `merchants_all`.
- Report exposed/unexposed row counts, means, differences, diagnostics, and caveats.
- Mark results as exploratory observational associations, not causal proof.
- Add a repeatable smoke script that writes JSON and Markdown artifacts.
- Add tests for positive, null/weak, and not-testable cases.
- Keep 20-turn regression passing after adding the statistics layer.

## Non-Goals

- Full matched controls.
- P-values or multiple-testing correction.
- Claim promotion.
- Live model calls.

## Assumptions

- The final CSVs have stable `has_game`, `game_count`, `revenue_all`, and `merchants_all` fields.
- Phase 010 can start with deterministic descriptive comparisons before fuller matching.
- Later phases will add matched controls, p-values, and multiple-testing correction.

## Affected Layers

- Statistical execution scaffold
- Smoke validation
- Tests
- Documentation

## Affected Modules

- `app/statistical_tests.py`
- `scripts/run_statistical_smoke.py`
- `tests/test_statistical_tests.py`
- Phase 010 docs under `docs/`

## Dependency/Library Choices

No new dependencies are required. The implementation uses Python standard library CSV parsing and arithmetic.

## Architecture Notes

The statistics layer is separate from the friends loop. It can later be called by the router only when a selected candidate is a complete `statistical_hypothesis`. For now, the smoke command proves data-level statistical scaffolding exists.

## Data/API/Config Changes

- Reads final reference CSVs under `data/reference/`.
- Writes `statistical_smoke.json` and `statistical_smoke.md` under `app/runs/phase-010-exploratory-statistical-tests/`.

## Demo Requirements

- Run statistical smoke script.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Tests cover exposed/unexposed difference calculation.
- Tests cover not-testable data when an exposure group is missing.
- Tests cover report artifact writing.
- Validation passes.

## Security/Sandbox Considerations

- Do not mutate source CSVs.
- Do not overclaim causal findings.
- Do not read `.env`.

## Risks

- Descriptive differences may be misread as causal effects.
- Matching and multiple-testing correction are still future work.

## Acceptance Criteria

- Statistical smoke artifacts are written.
- Results include diagnostics and caveats.
- Tests and validation pass.
- 20-turn regression still passes.

## Rollback Plan

Revert the Phase 010 commit or remove statistics module, smoke script, tests, artifacts, and docs.
