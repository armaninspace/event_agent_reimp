# Phase 029: Knowledge Duplicate Avoidance

## Phase Goal

Use prior notebook knowledge to reduce repeated candidate selection by penalizing OpenAI proposals that duplicate recent seed questions.

## Requirements

- Compare OpenAI proposal questions against recent prior notebook seed questions.
- Mark duplicate proposals in candidate reasoning metadata.
- Reduce duplicate proposal novelty before tournament ranking.
- Count duplicate proposals in phase regression and audit.
- Run a 20-turn replay regression using Phase 027 notebook knowledge.

## Non-Goals

- Semantic embedding similarity.
- Live OpenAI inference.
- Eliminating all repetition across broad semantic families.
- Changing deterministic candidate generation.

## Assumptions

- Exact case-insensitive seed matching is a safe first duplicate-avoidance rule.
- Novelty penalty is enough to affect tournament ranking without hiding duplicates.
- Future phases can add fuzzy matching or embeddings.

## Affected Layers

- Friends-loop candidate construction
- OpenAI reasoning metadata
- Phase regression
- Final audit
- Tests and documentation

## Affected Modules

- `app/friends_loop.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_openai_reasoning.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The duplicate check runs after OpenAI proposals are parsed and before candidate records enter tournament ranking. A duplicate proposal keeps its question and rationale for auditability, but its novelty is capped at 1 and its reasoning metadata records `prior_knowledge_duplicate=True`.

## Data/API/Config Changes

- Candidate reasoning metadata gains `prior_knowledge_duplicate`.
- Session and phase summaries gain `prior_knowledge_duplicate_candidate_count`.
- Audit gains `prior_knowledge_duplicate_candidate_count`.

## Demo Requirements

- Run focused OpenAI/regression tests.
- Run 20-turn replay phase regression with prior notebook knowledge.
- Run replication audit against Phase 029.
- Run full validation.

## Test Requirements

- Prior duplicate proposal is marked.
- Selection shifts away from the duplicate when another candidate scores higher after novelty penalty.
- Audit reports 20 duplicate candidates in the Phase 029 replay run.
- Validation passes.

## Security/Sandbox Considerations

- Uses only explicit prior knowledge path.
- Does not read secrets or environment files.
- Does not delete or rewrite prior knowledge artifacts.

## Risks

- Exact string matching misses paraphrased duplicates.
- Novelty penalty can over-favor different-but-lower-value questions if configured too aggressively.
- Replay demonstrates deterministic ranking behavior, not live model quality.

## Acceptance Criteria

- Phase regression reports `prior_knowledge_duplicate_candidate_count=20`.
- Audit reports `prior_knowledge_duplicate_candidate_count=20`.
- Selected candidates move away from the repeated prior seed.
- Validation passes.

## Rollback Plan

Revert the Phase 029 commit or remove duplicate marking, novelty penalty, regression/audit fields, tests, artifacts, and docs.
