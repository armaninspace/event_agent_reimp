# Phase 032: Evolved Duplicate Follow-Ups

## Phase Goal

Turn repeated prior notebook seed questions into auditable follow-up validation questions so all thesis semantic slots can be covered without selecting the same question verbatim.

## Requirements

- Detect prior-knowledge duplicate OpenAI proposals using the existing fuzzy similarity path.
- Preserve duplicate metadata and original question text in candidate reasoning.
- Rewrite duplicate proposals into semantic-slot-specific validation follow-up questions.
- Allow evolved duplicates to compete in semantic-slot diversity selection.
- Count evolved duplicate candidates in session, phase regression, CLI output, and audit.
- Run a 20-turn replay regression using Phase 027 notebook knowledge.

## Non-Goals

- Live OpenAI inference.
- Embedding-based question evolution.
- Changing the replay source data.
- Hiding the fact that a proposal originated as a duplicate.

## Assumptions

- A repeated high-value city-week spending question should become a stronger validation question rather than being suppressed forever.
- Evolved duplicate candidates remain auditably linked to their original duplicate proposal.
- Slot-specific follow-up templates are acceptable for replay mode because replay output is fixed.

## Affected Layers

- Friends-loop OpenAI candidate construction
- Semantic-slot diversity selection
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

Duplicate detection still runs before candidate ranking. A duplicate proposal gains `prior_knowledge_evolved_duplicate=True`, keeps `prior_knowledge_duplicate=True`, stores `prior_knowledge_original_question`, and receives a semantic-slot-specific follow-up question. The diversity selector treats evolved duplicates as eligible follow-ups rather than raw repeats.

## Data/API/Config Changes

- Session summary gains `prior_knowledge_evolved_duplicate_candidate_count`.
- Candidate reasoning gains `prior_knowledge_evolved_duplicate`.
- Candidate reasoning gains `prior_knowledge_original_question`.
- Phase regression and audit gain evolved duplicate counts.

## Demo Requirements

- Run focused OpenAI/regression/audit tests.
- Run MAF replay smoke.
- Run 20-turn replay phase regression with prior notebook knowledge.
- Run replication audit against Phase 032.
- Run full validation.

## Test Requirements

- A prior city-week duplicate becomes a matched-control follow-up.
- The selected evolved candidate preserves duplicate metadata.
- Six-turn replay covers all three semantic slots evenly.
- Final audit reports all three selected semantic slots.
- Validation passes.

## Security/Sandbox Considerations

- Uses only explicit prior knowledge path.
- Does not read secrets or environment files.
- Does not delete or rewrite prior phase artifacts.

## Risks

- Template-based follow-ups are less flexible than live OpenAI revision.
- Evolved duplicates can outrank lower-scoring non-duplicate proposals.
- Replay evidence does not validate live model behavior.

## Acceptance Criteria

- Phase regression reports `prior_knowledge_evolved_duplicate_candidate_count=20`.
- Phase regression reports `selected_unique_semantic_slot_count=3`.
- Audit reports all three semantic slots represented.
- Validation passes.

## Rollback Plan

Revert the Phase 032 commit or remove evolved duplicate rewriting, summary/audit fields, tests, artifacts, and docs.
