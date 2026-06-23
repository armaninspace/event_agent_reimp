# Phase 014 Backlog: QuestionForum Store

## P014-001: Implement QuestionForum Loader

- Stable item ID: `P014-001`
- Title: Add JSON-backed forum records
- Rationale: Public questions need durable provenance and governance metadata.
- Affected files/modules: `app/question_forum.py`, `data/question_forum/questions.json`
- Implementation steps: Add record dataclass, loader, status validation, unique ID checks, and seed records.
- Unit test expectations: Valid records load and invalid statuses fail.
- E2E test expectations: Forum smoke command passes.
- Demo relevance: Smoke artifacts show record count and question IDs.
- Acceptance criteria: Forum records load and validate.
- Status: done

## P014-002: Carry Forum Metadata Through Candidates

- Stable item ID: `P014-002`
- Title: Attach forum provenance to selected candidates
- Rationale: The thesis requires selected candidates to carry forum metadata through the 20-turn run.
- Affected files/modules: `app/friends_loop.py`, `app/phase_regression.py`
- Implementation steps: Load forum records by default, enrich candidate dictionaries, add telemetry, and require metadata in regression.
- Unit test expectations: Selected candidates and telemetry include forum metadata.
- E2E test expectations: 20-turn regression reports selected metadata coverage.
- Demo relevance: Regression evidence proves every selected candidate carries forum metadata.
- Acceptance criteria: Selected candidates carry forum metadata in 20-turn regression.
- Status: done

## P014-003: Validate, Demo, Status, Commit

- Stable item ID: `P014-003`
- Title: Close Phase 014
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 014 docs and repository state.
- Implementation steps: Run tests, forum smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 014 is locally committed.
- Status: done
