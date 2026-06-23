# Phase 003: Friends Loop Skeleton

## Phase Goal

Create the first deterministic friends-loop orchestration skeleton with role interfaces, selected/rejected candidates per turn, structured telemetry, and durable session artifacts.

## Requirements

- Implement friend roles as interfaces/classes:
  - Spark proposes candidates.
  - Skeptic reviews identification and claim boundaries.
  - Mapper links candidates to data profiles and semantic slots.
  - Moderator ranks and selects candidates deterministically.
  - DataAgent writes durable artifacts.
- Implement `run_friends_question_loop(turn_count=2)` with deterministic output.
- Each turn must include selected and rejected candidates.
- Write session JSON, session Markdown, telemetry JSON, and discovery decision summary.
- Add a smoke script that runs a two-turn loop.
- Add tests for deterministic selection, artifacts, and telemetry shape.

## Non-Goals

- Live LLM calls.
- Microsoft Agent Framework orchestration.
- Notebook generation.
- Wiki memory.
- Statistical tests.
- Full 20-turn regression acceptance.

## Assumptions

- Phase 003 can use deterministic role classes while preserving future compatibility with Microsoft Agent Framework agents.
- Reference data quality reports from Phase 002 are sufficient as data context.
- Public rationale and caveats are logged; private reasoning is not logged.

## Affected Layers

- Governance layer
- Orchestration skeleton
- Telemetry
- Artifact writing
- Tests

## Affected Modules

- `app/friends_loop.py`
- `scripts/run_friends_loop_smoke.py`
- `tests/test_friends_loop.py`
- Phase 003 docs under `docs/`

## Dependency/Library Choices

No new dependencies are required. The implementation uses the Python standard library and existing app modules.

## Architecture Notes

The friends loop is intentionally deterministic. Role classes expose simple methods that can later be replaced or wrapped by Microsoft Agent Framework agents. Telemetry uses structured JSON events with stable event IDs and sequences.

## Data/API/Config Changes

- Reads final reference CSVs through `app.reference_data`.
- Writes run artifacts under `app/runs/phase-003-friends-loop-skeleton/friends-question-loop/`.

## Demo Requirements

- Run the two-turn smoke command.
- Record completed turns, selected candidates, rejected candidates, and artifact paths.
- Include telemetry evidence.

## Test Requirements

- Unit tests verify two turns complete.
- Unit tests verify each turn has selected and rejected candidates.
- Unit tests verify deterministic selection under fixed inputs.
- Unit tests verify session JSON, Markdown, telemetry JSON, and decision summary are written.
- Validation passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not make network calls.
- Do not log private chain-of-thought.
- Do not mutate source CSVs.

## Risks

- Deterministic role classes are a scaffold, not real multi-agent reasoning.
- Full artifact family from later phases is not complete yet.
- 20-turn regression should be introduced next, before more orchestration complexity accumulates.

## Acceptance Criteria

- `run_friends_question_loop(turn_count=2)` completes.
- Each turn has selected and rejected candidates.
- Session JSON and Markdown are written.
- Telemetry JSON and discovery decision summary are written.
- Candidate selection is deterministic under fixed inputs.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 003 commit or remove `app/friends_loop.py`, smoke script, tests, smoke artifacts, and Phase 003 docs.
