# Phase 014 Demo: QuestionForum Store

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_question_forum.py tests/test_friends_loop.py tests/test_phase_regression.py -q
python3 scripts/run_question_forum_smoke.py --output-dir app/runs/phase-014-question-forum-store
python3 scripts/run_phase_regression.py --phase-id phase-014-question-forum-store --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Forum records load and validate.
- Invalid statuses are rejected by tests.
- Forum smoke writes JSON and Markdown artifacts.
- Selected candidates carry `forum` metadata.
- 20-turn regression reports selected-candidate metadata coverage.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest tests/test_question_forum.py tests/test_friends_loop.py tests/test_phase_regression.py -q
.........                                                                [100%]
```

```text
python3 scripts/run_question_forum_smoke.py --output-dir app/runs/phase-014-question-forum-store
wrote app/runs/phase-014-question-forum-store/question_forum_smoke.json
wrote app/runs/phase-014-question-forum-store/question_forum_smoke.md
record_count=3
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-014-question-forum-store --turns 20
wrote app/runs/phase-014-question-forum-store/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

## Evidence

Generated forum artifacts:

```text
app/runs/phase-014-question-forum-store/question_forum_smoke.json
app/runs/phase-014-question-forum-store/question_forum_smoke.md
app/runs/phase-014-question-forum-store/phase_regression_summary.json
```

Forum smoke summary:

```text
record_count: 3
question_ids: crowd-spending, market-coverage, confounding-risk
statuses: needs-review, proposed, selected
```

Regression summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
selected_candidate_count: 20
selected_candidates_have_required_metadata: True
selected_forum_ids: crowd-spending, market-coverage
forum.loaded telemetry: True
```

## 20-Turn Regression

Implemented and passed after adding the QuestionForum store and selected-candidate forum metadata.

## Video

No video was generated. This is a non-UI governance/persistence phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- Forum storage is JSON-backed, not database-backed.
- Deterministic ranking still favors high-scoring repeated questions after the first turn.
- Tournament, reflection, and evolution metadata are not implemented yet.

## Requirement Mapping

- Forum loader: `app/question_forum.py`
- Seed data: `data/question_forum/questions.json`
- Candidate integration: `app/friends_loop.py`
- Regression metadata check: `app/phase_regression.py`
- Smoke command: `scripts/run_question_forum_smoke.py`
- Tests: `tests/test_question_forum.py`, `tests/test_friends_loop.py`
