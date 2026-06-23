# Phase 023: Evolution Variants

## Phase Goal

Remediate the evolution metadata limitation by adding deterministic evolved question variants and parent/child IDs to every selected candidate.

## Requirements

- Add `parent_question_id`, `child_question_id`, and `evolved_question` to evolution metadata.
- Generate deterministic rewritten variants for `split`, `combine`, `strengthen`, and `carry_forward` actions.
- Require evolution variant metadata in phase regression.
- Count evolution variant coverage in replication audit.
- Keep 20-turn regression passing.

## Non-Goals

- Live LLM rewriting.
- Rich hypothesis graph database.
- Human moderation of evolved questions.

## Assumptions

- Deterministic variants are the right next step before live model rewriting.
- Parent/child IDs can use forum question IDs plus action labels.

## Affected Layers

- Question evolution
- Phase regression
- Final audit
- Tests
- Documentation

## Affected Modules

- `app/question_evolution.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_replication_audit.py`
- `tests/test_question_governance.py`
- `tests/test_friends_loop.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

Evolution remains deterministic and testable. Live or model-based rewriting can later target the same output contract: action, parent ID, child ID, evolved question, and rationale.

## Data/API/Config Changes

- Candidate `evolution` metadata gains `parent_question_id`, `child_question_id`, and `evolved_question`.
- Replication audit gains `selected_evolution_variant_count`.

## Demo Requirements

- Run governance/friends/regression tests.
- Run a 20-turn regression.
- Run replication audit against the new run.
- Record validation output.

## Test Requirements

- Evolution tests assert child IDs and rewritten question text.
- Friends-loop tests assert selected evolved questions exist.
- Regression requires evolution variant metadata.
- Audit requires 20 evolution variants.
- Validation passes.

## Security/Sandbox Considerations

- Do not present evolved variants as live human-approved forum text.
- Preserve caveats.

## Risks

- Deterministic rewrites are less expressive than model-generated variants.
- Parent/child IDs are simple strings rather than a full graph store.

## Acceptance Criteria

- 20/20 selected candidates carry evolution variants.
- Audit reports `selected_evolution_variant_count=20`.
- 20-turn regression passes.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 023 commit or remove evolution variant fields, regression/audit checks, tests, artifacts, and docs.
