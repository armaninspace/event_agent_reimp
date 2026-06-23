# Phase 004: 20-Turn Regression Gate

## Phase Goal

Add the first enforceable 20-turn regression gate for the deterministic friends-loop skeleton, including a stable command, machine-readable summary, tests, and phase evidence.

## Requirements

- Add `scripts/run_phase_regression.py`.
- Run `run_friends_question_loop` with a configurable phase ID and turn count.
- Default regression turn count must be 20.
- Write `phase_regression_summary.json`.
- Summary must include requested turns, completed workflows, stopped-early status, selected-candidate metadata, artifact existence checks, telemetry event counts, and workflow-task statistical misroutes.
- Verify session JSON, telemetry JSON, discovery decision summary, and loop artifacts exist.
- Add tests for the regression summary and default 20-turn behavior.

## Non-Goals

- Notebook generation.
- Business evidence HTML.
- Playback UI.
- Real statistical routing.
- Live LLM or Microsoft Agent Framework calls.

## Assumptions

- Phase 004 can treat missing business/playback/notebook artifacts as known future gaps while still enforcing current-loop artifacts.
- Workflow-task statistical misroutes are zero because no statistical router exists yet and no workflow tasks are routed into tests.
- The deterministic friends loop can safely run 20 turns locally.

## Affected Layers

- Regression validation
- Orchestration smoke
- Artifact evidence
- Tests
- Documentation

## Affected Modules

- `scripts/run_phase_regression.py`
- `app/phase_regression.py`
- `tests/test_phase_regression.py`
- Phase 004 docs under `docs/`

## Dependency/Library Choices

No new dependencies are required. The regression helper uses Python standard library modules and existing app modules.

## Architecture Notes

`app.phase_regression` wraps the friends loop and validates artifact presence. The script is a thin CLI. Later phases can extend the summary with notebooks, reports, playback UI, and routing-specific checks without changing the command contract.

## Data/API/Config Changes

- Reads final reference CSVs through the friends loop.
- Writes under `app/runs/<phase-id>/friends-question-loop/`.
- Writes `phase_regression_summary.json` in the phase run directory.

## Demo Requirements

- Run `python3 scripts/run_phase_regression.py --phase-id phase-004-regression-gate --turns 20`.
- Record output, summary path, and key summary fields.

## Test Requirements

- Unit tests cover summary generation.
- Unit tests verify default turn count is 20.
- Unit tests verify required artifacts are checked.
- `python3 -m pytest -q` passes.
- `bash scripts/validate.sh` passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not make network calls.
- Do not push, merge, or publish.
- Do not mutate source CSVs.

## Risks

- Current regression does not yet validate notebooks, reports, playback UI, or real statistical routing.
- Future phases must tighten the acceptance gate as those surfaces are implemented.

## Acceptance Criteria

- 20-turn regression command completes.
- `phase_regression_summary.json` is written.
- Summary reports requested turns 20, completed workflows 20, stopped early false, and workflow-task statistical misroutes 0.
- Current required artifacts exist.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 004 commit or remove `app/phase_regression.py`, `scripts/run_phase_regression.py`, tests, regression artifacts, and Phase 004 docs.
