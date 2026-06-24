# Phase 031: Semantic Slot Diversity

## Phase Goal

Prevent the 20-turn thesis replication loop from repeatedly selecting the same non-duplicate semantic slot after prior-knowledge duplicate suppression.

## Requirements

- Track selected semantic slot counts during a friends-loop run.
- Annotate candidate reasoning with each slot's prior selection count.
- Prefer non-duplicate candidates from the least-used semantic slots after tournament ranking.
- Preserve tournament metadata and transcripts for all candidates.
- Report selected semantic slot counts in session, phase regression, CLI output, and audit.
- Run a 20-turn replay regression using Phase 027 notebook knowledge.

## Non-Goals

- Embedding-based semantic clustering.
- Live OpenAI inference.
- Allowing prior-knowledge duplicates to win just to fill every slot.
- Replacing tournament ranking.

## Assumptions

- A multi-turn thesis replication should cover multiple unresolved semantic slots when candidates are otherwise answerable.
- Prior-knowledge duplicates should remain lower priority than non-duplicate slots.
- Tournament rank should still break ties inside the least-used non-duplicate pool.

## Affected Layers

- Friends-loop candidate selection
- OpenAI and deterministic candidate reasoning metadata
- Phase regression summary
- Replication audit
- Tests and documentation

## Affected Modules

- `app/friends_loop.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_openai_reasoning.py`
- `tests/test_phase_regression.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The tournament still ranks every candidate. Final selection then filters to answerable, non-duplicate candidates and chooses from the least-used semantic slot count. If all answerable candidates are prior-knowledge duplicates, the same least-used rule applies to the full pool.

## Data/API/Config Changes

- Session summary gains `selected_semantic_slot_counts`.
- Session summary gains `selected_unique_semantic_slot_count`.
- Candidate reasoning gains `semantic_slot_prior_selection_count`.
- Phase regression and audit gain semantic slot coverage fields.

## Demo Requirements

- Run focused OpenAI/regression tests.
- Run MAF replay smoke.
- Run 20-turn replay phase regression with prior notebook knowledge.
- Run replication audit against Phase 031.
- Run full validation.

## Test Requirements

- Replay with a duplicate city-week prior seed balances between MSA coverage and identification risk.
- Deterministic three-turn regression covers all three semantic slots.
- Audit exposes semantic slot coverage for the latest phase artifacts.
- Validation passes.

## Security/Sandbox Considerations

- Uses only in-memory selection history and explicit prior knowledge path.
- Does not read secrets or environment files.
- Does not delete or rewrite prior phase artifacts.

## Risks

- Diversity preference may select a lower tournament-ranked question when a slot has been under-covered.
- With only three replay candidates, a prior-knowledge duplicate slot remains excluded, so Phase 031 covers two non-duplicate slots instead of all three.
- Replay evidence does not validate live model behavior.

## Acceptance Criteria

- Phase regression reports `selected_semantic_slot_counts={'identification_risk': 10, 'msa_week_coverage': 10}`.
- Audit reports `selected_unique_semantic_slot_count=2`.
- Prior-knowledge duplicate candidate count remains 20.
- Validation passes.

## Rollback Plan

Revert the Phase 031 commit or remove the semantic-slot selector, summary fields, tests, artifacts, and docs.
