# Phase 004 Demo: 20-Turn Regression Gate

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_phase_regression.py --phase-id phase-004-regression-gate --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Regression command runs 20 deterministic friends-loop turns.
- `phase_regression_summary.json` is written.
- Summary reports requested turns 20, completed workflows 20, stopped early false, and workflow-task statistical misroutes 0.
- Current required artifacts exist.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
..............                                                           [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-004-regression-gate --turns 20
wrote app/runs/phase-004-regression-gate/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
```

```text
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
14 passed in 0.12s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated files:

```text
app/runs/phase-004-regression-gate/phase_regression_summary.json
app/runs/phase-004-regression-gate/friends-question-loop/friends_loop_session.json
app/runs/phase-004-regression-gate/friends-question-loop/friends_loop_session.md
app/runs/phase-004-regression-gate/friends-question-loop/friends_loop_telemetry.json
app/runs/phase-004-regression-gate/friends-question-loop/discovery_decision_summary.md
```

Summary fields:

```text
schema_version: phase-004.phase-regression-summary.v1
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
selected_candidate_count: 20
selected_candidates_have_required_metadata: True
current_required_artifacts_exist: True
telemetry_event_count: 121
telemetry_event_types: board.proposed, board.ranked, discussion.message, knowledge.read, memory.seeded, turn.completed, turn.started
```

## 20-Turn Regression

Implemented and passed for the current deterministic friends-loop artifact surface.

Known future artifacts are still marked deferred in the summary:

```text
business_html: deferred until report phase
playback_html: deferred until playback UI phase
notebook_workspace: deferred until notebook/wiki phase
```

## Video

No video was generated. This is a non-UI CLI/regression phase, and command-output evidence plus generated regression artifacts are the relevant demo outputs.

## Known Gaps

- The regression gate does not yet require business HTML, playback HTML, or notebooks because those surfaces do not exist.
- There is still no real statistical router, so workflow-task statistical misroutes are zero by construction.
- Microsoft Agent Framework live orchestration remains deferred.

## Requirement Mapping

- Regression service: `app/phase_regression.py`
- Regression CLI: `scripts/run_phase_regression.py`
- Summary artifact: `app/runs/phase-004-regression-gate/phase_regression_summary.json`
- Tests: `tests/test_phase_regression.py`
