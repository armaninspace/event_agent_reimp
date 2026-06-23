# Phase 015: Governance Metadata

## Phase Goal

Add deterministic tournament, reflection, and evolution governance metadata to candidate selection and require that metadata in the 20-turn regression gate.

## Requirements

- Add pairwise candidate tournament scoring.
- Record public interest, novelty, testability, evidence value, and policy/business relevance component scores.
- Record tournament rank, wins, losses, and transcript entries.
- Add reviewer reflection metadata for misleading risk, weakening evidence, answerability, and status.
- Add question evolution metadata with `split`, `combine`, `strengthen`, and `carry_forward` actions.
- Penalize or filter `not-answerable` candidates during selection.
- Persist tournament, reflection, and evolution metadata on selected and rejected candidates.
- Add telemetry for tournament, reflection, and evolution passes.
- Require all selected candidates to carry forum, tournament, reflection, and evolution metadata in phase regression.

## Non-Goals

- LLM-generated debate.
- Literature-grounded novelty scoring.
- Human moderation.
- Live question rewriting.

## Assumptions

- Deterministic heuristics are appropriate for local thesis replication and regression evidence.
- Tournament rank should drive selection after reflection filters not-answerable candidates.
- Evolution metadata is descriptive and does not rewrite the source forum record yet.

## Affected Layers

- Candidate governance
- Selection policy
- Reflection/review
- Telemetry
- Phase regression
- Tests
- Documentation

## Affected Modules

- `app/question_tournament.py`
- `app/question_reflection.py`
- `app/question_evolution.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `scripts/run_governance_smoke.py`
- `tests/test_question_governance.py`
- `tests/test_friends_loop.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The governance modules accept candidate dictionaries and return metadata keyed by candidate ID. The friends loop composes those metadata records into selected and rejected candidates, which keeps governance explicit without coupling the modules to the `Candidate` dataclass.

## Data/API/Config Changes

- Selected and rejected candidate records gain `tournament`, `reflection`, and `evolution` objects.
- Telemetry gains `tournament.completed`, `reflection.completed`, and `evolution.completed` events.
- Phase regression selected-candidate metadata checks now require all governance families.

## Demo Requirements

- Run governance smoke.
- Run affected tests.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Tournament ranks candidates and records transcripts.
- Reflection records review status and misleading-risk metadata.
- Evolution strengthens repeated questions.
- Friends-loop selected candidates carry governance metadata.
- Regression selected-candidate metadata check includes forum, tournament, reflection, and evolution.

## Security/Sandbox Considerations

- Governance metadata must remain auditable and deterministic.
- Do not treat governance scores as causal evidence.

## Risks

- Heuristic scoring is not a substitute for human review.
- Deterministic evolution currently records metadata rather than rewriting candidate text.

## Acceptance Criteria

- Selected candidates carry tournament, reflection, and evolution metadata.
- Deterministic transcripts are stored.
- Not-answerable candidates are filtered from selection.
- Final 20-turn run completes with all metadata families present.

## Rollback Plan

Revert the Phase 015 commit or remove governance modules, smoke script, friends-loop integration, regression metadata checks, tests, artifacts, and docs.
