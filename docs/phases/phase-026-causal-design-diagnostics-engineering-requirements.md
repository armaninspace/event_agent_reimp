# Phase 026: Causal Design Diagnostics

## Phase Goal

Strengthen statistical evidence by attaching explicit causal-design diagnostics to every selected turn, using the existing same-week/same-block matched-control evidence.

## Requirements

- Add a causal-design diagnostics layer over matched-control results.
- Report design level, evidence grade, matched exposure rate, control usage, and limitations.
- Attach candidate-scoped causal-design summaries to `statistical_evidence`.
- Render causal-design diagnostics in the business report.
- Require causal-design diagnostics in phase regression.
- Add audit counts for causal-design and controlled-observational coverage.
- Keep the claim boundary explicit: controlled observational evidence is not causal proof.

## Non-Goals

- Claiming causal proof.
- Adding external calendars or randomized assignment.
- Replacing p-values or multiple-testing correction.
- Running live OpenAI inference.

## Assumptions

- Same-week/same-block matching is the strongest currently available design in the local data.
- Sparse matches should be labeled as fragile controlled observational evidence.
- The audit should count design coverage separately from statistical significance.

## Affected Layers

- Causal diagnostics
- Statistical execution
- Business reporting
- Phase regression
- Final audit
- Tests and documentation

## Affected Modules

- `app/causal_diagnostics.py`
- `app/statistical_execution.py`
- `app/reporting.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_causal_diagnostics.py`
- `tests/test_statistical_execution.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

`app.causal_diagnostics` consumes matched-control results and produces design diagnostics independent of p-values. `app.statistical_execution` attaches relevant diagnostics per candidate semantic slot. This keeps causal-design coverage inspectable without promoting observational associations to causal estimates.

## Data/API/Config Changes

- Statistical execution schema advances to `phase-026.statistical-execution.v2`.
- Turn `statistical_evidence` gains a `causal_design` object.
- Phase regression gains `turns_have_causal_design_diagnostics`.
- Replication audit gains `causal_design_turn_count` and `controlled_observational_turn_count`.

## Demo Requirements

- Run focused diagnostics/statistical/regression/audit tests.
- Run MAF replay smoke for the phase directory.
- Run a 20-turn replay phase regression.
- Run replication audit against Phase 026.
- Run full validation.

## Test Requirements

- Causal diagnostics grade matched-control evidence.
- Candidate evidence includes causal-design summaries.
- Regression requires causal-design diagnostics.
- Audit counts 20 causal-design turns.
- Validation passes.

## Security/Sandbox Considerations

- No secrets or external calls.
- Preserve claim boundaries in reports and artifacts.
- Do not downgrade causal caveats.

## Risks

- Same-week/same-block matching can still miss unobserved confounders.
- Sparse matched samples can be overread if the evidence grade is ignored.
- External event calendars would be needed for stronger causal identification.

## Acceptance Criteria

- 20-turn regression reports `turns_have_causal_design_diagnostics=True`.
- Audit reports `causal_design_turn_count=20`.
- Audit reports `controlled_observational_turn_count=20`.
- Business report renders causal-design diagnostics.
- Full validation passes.

## Rollback Plan

Revert the Phase 026 commit or remove causal diagnostics, schema additions, regression/audit checks, tests, artifacts, and docs.
