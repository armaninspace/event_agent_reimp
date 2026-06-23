# Phase 017: Governed Statistical Execution

## Phase Goal

Attach candidate-scoped statistical execution evidence to governed selected questions so the friends-loop turn record carries the statistical artifacts produced by the existing exploratory, matched, p-value, and multiple-testing layers.

## Requirements

- Build a reusable statistical execution report from the correction engine.
- Map selected candidates to relevant corrected results by semantic slot.
- Attach `statistical_evidence` to every turn.
- Record candidate ID, semantic slot, result IDs, result count, adjusted-significance flag, minimum adjusted p-value, results, and caveats.
- Add `statistics.attached` telemetry once per turn.
- Add a phase-regression flag proving every turn has statistical evidence.
- Add smoke artifacts for statistical execution.
- Keep the 20-turn regression passing.

## Non-Goals

- Causal claim promotion.
- New statistical models.
- Human publication review.
- Replacing the existing correction engine.

## Assumptions

- Existing Phase 013 correction results are the current statistical execution source.
- Semantic slots are sufficient to map public questions to relevant statistical results.
- Statistical evidence remains observational and exploratory.

## Affected Layers

- Statistical execution
- Candidate-to-evidence mapping
- Telemetry
- Phase regression
- Tests
- Documentation

## Affected Modules

- `app/statistical_execution.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `scripts/run_statistical_execution_smoke.py`
- `scripts/run_phase_regression.py`
- `tests/test_statistical_execution.py`
- `tests/test_friends_loop.py`
- `tests/test_phase_regression.py`

## Dependency/Library Choices

No new dependency is required. The phase reuses SciPy through the existing correction engine.

## Architecture Notes

The friends loop computes one statistical execution report per run and then filters that report per selected candidate. This keeps the 20-turn run practical while making every turn carry auditable statistical evidence.

## Data/API/Config Changes

- Turn records gain `statistical_evidence`.
- Telemetry gains `statistics.attached`.
- Phase regression gains `turns_have_statistical_evidence`.

## Demo Requirements

- Run statistical execution smoke.
- Run affected tests.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Candidate evidence filters results by semantic slot.
- Friends-loop turns carry statistical evidence.
- Telemetry includes one statistical attachment event per turn.
- Phase regression reports statistical evidence coverage.
- Validation passes.

## Security/Sandbox Considerations

- Do not overstate causality.
- Do not mutate source CSVs.
- Do not read `.env`.

## Risks

- Semantic-slot mapping is deterministic and coarse.
- Results remain observational and exploratory.
- Recomputing correction reports adds runtime to phase regression.

## Acceptance Criteria

- Statistical execution smoke artifacts are written.
- Every selected turn carries statistical evidence.
- `statistics.attached` telemetry is present.
- 20-turn regression reports `turns_have_statistical_evidence=True`.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 017 commit or remove statistical execution mapping, smoke script, loop integration, regression flag, tests, artifacts, and docs.
