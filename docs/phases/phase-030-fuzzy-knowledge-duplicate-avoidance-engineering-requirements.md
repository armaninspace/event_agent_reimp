# Phase 030: Fuzzy Knowledge Duplicate Avoidance

## Phase Goal

Extend prior notebook knowledge duplicate avoidance from exact seed-question matches to close paraphrases.

## Requirements

- Compare OpenAI proposal questions against recent prior notebook seed questions using token overlap.
- Preserve exact duplicate behavior as a high-similarity case.
- Mark near-duplicate proposals in candidate reasoning metadata.
- Record the similarity score and duplicate threshold for auditability.
- Keep duplicate novelty penalties before tournament ranking.
- Run a 20-turn replay regression using Phase 027 notebook knowledge.

## Non-Goals

- Embedding similarity.
- Live OpenAI inference.
- Full semantic-family clustering.
- Changing deterministic candidate generation.

## Assumptions

- Token Jaccard similarity is a useful low-dependency first pass for paraphrased repeated questions.
- A threshold of `0.62` catches close restatements without suppressing unrelated questions.
- Candidate reasoning metadata should expose the score rather than hiding the ranking policy.

## Affected Layers

- Friends-loop candidate construction
- OpenAI reasoning metadata
- Phase regression artifacts
- Final audit artifacts
- Tests and documentation

## Affected Modules

- `app/friends_loop.py`
- `tests/test_openai_reasoning.py`
- `app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance/`

## Dependency/Library Choices

No new dependency is required. The implementation uses Python `re` tokenization.

## Architecture Notes

The duplicate check runs after OpenAI proposals are parsed and before candidate records enter tournament ranking. Each OpenAI candidate receives `prior_knowledge_similarity` and `prior_knowledge_duplicate_threshold` metadata. Candidates at or above the threshold get `prior_knowledge_duplicate=True` and novelty capped at 1.

## Data/API/Config Changes

- Candidate reasoning metadata gains `prior_knowledge_similarity`.
- Candidate reasoning metadata gains `prior_knowledge_duplicate_threshold`.
- Existing duplicate counts remain unchanged and count both exact and fuzzy duplicates.

## Demo Requirements

- Run focused OpenAI/regression/audit tests.
- Run MAF replay smoke.
- Run 20-turn replay phase regression with prior notebook knowledge.
- Run replication audit against Phase 030.
- Run full validation.

## Test Requirements

- A paraphrased prior seed is marked as duplicate.
- Selection shifts away from the duplicate when another candidate scores higher after novelty penalty.
- Audit reports 20 duplicate candidates in the Phase 030 replay run.
- Validation passes.

## Security/Sandbox Considerations

- Uses only explicit prior knowledge path.
- Does not read secrets or environment files.
- Does not delete or rewrite prior knowledge artifacts.

## Risks

- Token similarity can miss deeper semantic duplicates.
- Token similarity can over-match questions with shared domain vocabulary.
- Replay demonstrates deterministic ranking behavior, not live model quality.

## Acceptance Criteria

- Focused tests pass with paraphrase duplicate coverage.
- Phase regression reports `prior_knowledge_duplicate_candidate_count=20`.
- Audit reports `prior_knowledge_duplicate_candidate_count=20`.
- Candidate reasoning includes similarity metadata.
- Validation passes.

## Rollback Plan

Revert the Phase 030 commit or restore exact matching in `app/friends_loop.py`, remove the paraphrase test expectations, artifacts, and docs.
