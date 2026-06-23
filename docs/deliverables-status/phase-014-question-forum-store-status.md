# Phase 014 Deliverables Status: QuestionForum Store

## Completed Items

- Added `app/question_forum.py`.
- Added `data/question_forum/questions.json`.
- Added validation for required forum fields.
- Added status validation for `proposed`, `selected`, `tested`, `answered`, and `needs-review`.
- Added unique question ID validation.
- Added `scripts/run_question_forum_smoke.py`.
- Integrated forum records into `Spark` candidate generation.
- Added `forum` metadata to candidate dictionaries.
- Added `forum.loaded` telemetry and forum metadata in `question.submitted` events.
- Expanded phase regression metadata checks to require selected candidate forum metadata.
- Ran a 20-turn regression after adding the QuestionForum store.

## Blocked/Deferred Items

- Tournament scoring deferred to Phase 015.
- Reflection/reviewer metadata deferred to Phase 015.
- Hypothesis evolution metadata deferred to Phase 015.
- Live forum moderation and database persistence deferred.

## Files Changed

- `app/question_forum.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `data/question_forum/questions.json`
- `scripts/run_question_forum_smoke.py`
- `tests/test_question_forum.py`
- `tests/test_friends_loop.py`
- `app/runs/phase-014-question-forum-store/question_forum_smoke.json`
- `app/runs/phase-014-question-forum-store/question_forum_smoke.md`
- `app/runs/phase-014-question-forum-store/phase_regression_summary.json`
- `app/runs/phase-014-question-forum-store/friends-question-loop/`
- `app/runs/phase-014-question-forum-store/notebooks/`
- `docs/phases/phase-014-question-forum-store-engineering-requirements.md`
- `docs/backlog/phase-014-question-forum-store-backlog.md`
- `docs/demos/phase-014-question-forum-store-demo.md`
- `docs/deliverables-status/phase-014-question-forum-store-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 014.

## Tests Run

- `python3 -m pytest tests/test_question_forum.py tests/test_friends_loop.py tests/test_phase_regression.py -q`: passed, 9 tests.
- `python3 scripts/run_question_forum_smoke.py --output-dir app/runs/phase-014-question-forum-store`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-014-question-forum-store --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-014-question-forum-store-demo.md`.

Generated artifacts:

- `app/runs/phase-014-question-forum-store/question_forum_smoke.json`
- `app/runs/phase-014-question-forum-store/question_forum_smoke.md`
- `app/runs/phase-014-question-forum-store/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 014 is a non-UI governance/persistence phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Forum records load and validate: passed.
- Candidates cite forum metadata: passed.
- Selected candidates carry forum metadata in 20-turn regression: passed.
- Tests and validation pass: passed.

## Risks

- JSON-backed forum storage does not support concurrent moderation.
- Deterministic ranking still needs tournament/reflection/evolution governance to avoid repetitive selections.

## Next Phase

Phase 015 should add deterministic tournament, reflection, and evolution metadata and require all selected candidates to carry those metadata families in a 20-turn regression.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
