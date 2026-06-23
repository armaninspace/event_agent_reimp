# Phase 003 Demo: Friends Loop Skeleton

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_friends_loop_smoke.py --turns 2 --output-dir app/runs/phase-003-friends-loop-skeleton/friends-question-loop
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Two-turn friends loop completes.
- Each turn has one selected candidate and two rejected candidates.
- Session JSON, session Markdown, telemetry JSON, and discovery decision summary are written.
- Candidate selection is deterministic under fixed inputs.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
............                                                             [100%]
```

```text
python3 scripts/run_friends_loop_smoke.py --turns 2 --output-dir app/runs/phase-003-friends-loop-skeleton/friends-question-loop
completed_turns=2
turn=1 selected=turn-01-crowd-spending rejected=turn-01-market-coverage,turn-01-confounding-risk
turn=2 selected=turn-02-market-coverage rejected=turn-02-crowd-spending,turn-02-confounding-risk
session_json=app/runs/phase-003-friends-loop-skeleton/friends-question-loop/friends_loop_session.json
session_markdown=app/runs/phase-003-friends-loop-skeleton/friends-question-loop/friends_loop_session.md
telemetry_json=app/runs/phase-003-friends-loop-skeleton/friends-question-loop/friends_loop_telemetry.json
discovery_decision_summary=app/runs/phase-003-friends-loop-skeleton/friends-question-loop/discovery_decision_summary.md
```

```text
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
12 passed in 0.12s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated files:

```text
app/runs/phase-003-friends-loop-skeleton/friends-question-loop/friends_loop_session.json
app/runs/phase-003-friends-loop-skeleton/friends-question-loop/friends_loop_session.md
app/runs/phase-003-friends-loop-skeleton/friends-question-loop/friends_loop_telemetry.json
app/runs/phase-003-friends-loop-skeleton/friends-question-loop/discovery_decision_summary.md
```

Session summary:

```text
requested_turns: 2
completed_turns: 2
stopped_early: False
selected candidates: turn-01-crowd-spending, turn-02-market-coverage
telemetry events: 13
event types: board.proposed, board.ranked, discussion.message, knowledge.read, memory.seeded, turn.completed, turn.started
```

## 20-Turn Regression

Phase 003 introduces the first orchestration skeleton, but it is still a minimal two-turn smoke loop without notebooks, reports, wiki memory, semantic SQL, or statistical routing. A full 20-turn acceptance gate is deferred to the next orchestration phase, where a dedicated `scripts/run_phase_regression.py --turns 20` helper should be added before accepting expanded loop behavior.

## Video

No video was generated. This is a non-UI CLI/orchestration phase, and command-output evidence plus generated session/telemetry artifacts are the relevant demo outputs.

## Known Gaps

- Role classes are deterministic scaffolds, not live Microsoft Agent Framework agents yet.
- Telemetry includes the core events needed for this phase but not the full future event set.
- No notebooks, wiki memory, business report, playback UI, or phase regression summary exist yet.

## Requirement Mapping

- Spark/Skeptic/Mapper/Moderator/DataAgent role classes: `app/friends_loop.py`
- `run_friends_question_loop(turn_count=2)`: `app/friends_loop.py`
- Session and telemetry artifacts: `DataAgent.write_artifacts`
- Smoke command: `scripts/run_friends_loop_smoke.py`
- Tests: `tests/test_friends_loop.py`
