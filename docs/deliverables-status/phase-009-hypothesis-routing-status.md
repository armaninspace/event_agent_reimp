# Phase 009 Deliverables Status: Hypothesis Classification And Routing

## Completed Items

- Added `app/hypothesis_routing.py`.
- Implemented outcomes: `statistical_hypothesis`, `eda_question`, and `workflow_task`.
- Added workflow keyword routing for notebook, wiki, prompt, report, UI, logging, telemetry, and artifact questions.
- Added formal hypothesis field contract.
- Integrated classification metadata into friends-loop turns.
- Added telemetry events for `hypothesis.classified`, `question.submitted`, and `workflow.stage`.
- Updated regression to compute workflow-task statistical misroutes from session metadata.
- Added classifier and misroute tests.
- Ran a 20-turn regression with zero workflow-task statistical misroutes.

## Blocked/Deferred Items

- Statistical test execution remains deferred.
- Live LLM classification remains deferred.
- Rich formal hypothesis generation remains deferred.

## Files Changed

- `app/hypothesis_routing.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `tests/test_hypothesis_routing.py`
- `tests/test_friends_loop.py`
- `tests/test_phase_regression.py`
- `app/runs/phase-009-hypothesis-routing/`
- `docs/phases/phase-009-hypothesis-routing-engineering-requirements.md`
- `docs/backlog/phase-009-hypothesis-routing-backlog.md`
- `docs/demos/phase-009-hypothesis-routing-demo.md`
- `docs/deliverables-status/phase-009-hypothesis-routing-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 009.

## Tests Run

- `python3 -m pytest -q`: passed, 29 tests.
- `python3 scripts/run_phase_regression.py --phase-id phase-009-hypothesis-routing --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-009-hypothesis-routing-demo.md`.

Generated artifacts:

- `app/runs/phase-009-hypothesis-routing/phase_regression_summary.json`
- `app/runs/phase-009-hypothesis-routing/friends-question-loop/friends_loop_session.json`

## Video Path Or Rationale

No video was generated. Phase 009 is a non-UI routing/regression phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Notebook/wiki/report/UI/logging questions classify as workflow tasks: passed.
- Workflow-task statistical misroutes are zero in 20-turn regression: passed.
- Tests and validation pass: passed.

## Risks

- Keyword routing can be too simple for future public inputs.
- Future model-based routing must preserve the deterministic regression contract.
- Statistical execution still needs separate claim-boundary guardrails.

## Next Phase

Phase 010 should add matched statistical test scaffolding or a semantic query layer, then extend routing from `eda_review` toward real statistical execution only when formal hypothesis fields are present.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
