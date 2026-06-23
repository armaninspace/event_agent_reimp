# Phase 014: QuestionForum Store

## Phase Goal

Make stakeholder-facing public questions first-class JSON-backed records and carry their forum metadata through selected friends-loop candidates.

## Requirements

- Add a `QuestionForum` loader and validator.
- Support records with `question_id`, `kind`, `persona`, `question`, `rationale`, `priority`, `popularity`, `source_url`, `status`, and `tags`.
- Enforce allowed statuses: `proposed`, `selected`, `tested`, `answered`, and `needs-review`.
- Seed `data/question_forum/questions.json` with public, stakeholder-readable questions.
- Attach forum metadata to generated candidates.
- Persist selected candidate forum metadata through sessions, telemetry, notebooks, reports, and the 20-turn regression summary.
- Add a repeatable forum smoke command.
- Keep 20-turn regression passing.

## Non-Goals

- Live forum moderation.
- Database-backed question storage.
- Human authentication or voting.
- Tournament/reflection/evolution scoring.

## Assumptions

- JSON is sufficient for the local thesis replication workflow.
- Forum records are source inputs, not generated run artifacts.
- Candidate IDs can remain stable while candidate text and rationale are sourced from forum records.

## Affected Layers

- Question governance
- Candidate generation
- Telemetry
- Phase regression
- Tests
- Documentation

## Affected Modules

- `app/question_forum.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `scripts/run_question_forum_smoke.py`
- `tests/test_question_forum.py`
- `tests/test_friends_loop.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The forum remains separate from statistical execution. `Spark` reads validated forum records and uses them to populate public question text, rationale, and candidate metadata. The regression gate now requires every selected candidate to carry a `forum` object with provenance fields.

## Data/API/Config Changes

- Adds `data/question_forum/questions.json`.
- Adds optional `question_forum_path` to `run_friends_question_loop`.
- Adds selected candidate `forum` metadata.
- Adds `forum.loaded` telemetry.

## Demo Requirements

- Run forum smoke.
- Run affected tests.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Forum records load and validate.
- Invalid statuses are rejected.
- Selected candidates carry forum metadata.
- Question submission telemetry carries forum metadata.
- Phase regression selected-candidate metadata check includes forum metadata.

## Security/Sandbox Considerations

- Forum text is treated as public content and must continue to be escaped in reports.
- Do not read `.env`.

## Risks

- JSON files do not provide moderation or concurrency control.
- Deterministic selection can overuse the same high-scoring forum question until tournament/evolution phases diversify candidates.

## Acceptance Criteria

- Forum records load and validate.
- Candidates cite forum metadata.
- Selected candidates carry forum metadata in 20-turn regression.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 014 commit or remove the forum module, seed file, smoke script, friends-loop integration, regression metadata requirement, tests, artifacts, and docs.
