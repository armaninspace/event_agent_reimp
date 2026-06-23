# Phase 017 Deliverables Status: Governed Statistical Execution

## Completed Items

- Added `app/statistical_execution.py`.
- Added reusable statistical execution report over corrected results.
- Added semantic-slot mapping from selected candidates to relevant corrected results.
- Added candidate-scoped `statistical_evidence`.
- Added `statistics.attached` telemetry.
- Added `turns_have_statistical_evidence` to phase regression.
- Updated regression CLI output to print statistical evidence coverage.
- Added `scripts/run_statistical_execution_smoke.py`.
- Added statistical execution tests.
- Ran a 20-turn regression after attaching statistical evidence.

## Blocked/Deferred Items

- Business report rendering of detailed statistical evidence remains deferred.
- Notebook exports do not yet include a dedicated final corrections notebook.
- Semantic-slot mapping is not yet user-configurable.

## Files Changed

- `app/statistical_execution.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `scripts/run_phase_regression.py`
- `scripts/run_statistical_execution_smoke.py`
- `tests/test_statistical_execution.py`
- `tests/test_friends_loop.py`
- `tests/test_phase_regression.py`
- `app/runs/phase-017-statistical-execution/statistical_execution_smoke.json`
- `app/runs/phase-017-statistical-execution/statistical_execution_smoke.md`
- `app/runs/phase-017-statistical-execution/phase_regression_summary.json`
- `app/runs/phase-017-statistical-execution/friends-question-loop/`
- `app/runs/phase-017-statistical-execution/notebooks/`
- `docs/phases/phase-017-statistical-execution-engineering-requirements.md`
- `docs/backlog/phase-017-statistical-execution-backlog.md`
- `docs/demos/phase-017-statistical-execution-demo.md`
- `docs/deliverables-status/phase-017-statistical-execution-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 017.

## Tests Run

- `python3 -m pytest tests/test_statistical_execution.py tests/test_friends_loop.py tests/test_phase_regression.py -q`: passed, 8 tests.
- `python3 scripts/run_statistical_execution_smoke.py --output-dir app/runs/phase-017-statistical-execution`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-017-statistical-execution --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-017-statistical-execution-demo.md`.

Generated artifacts:

- `app/runs/phase-017-statistical-execution/statistical_execution_smoke.json`
- `app/runs/phase-017-statistical-execution/statistical_execution_smoke.md`
- `app/runs/phase-017-statistical-execution/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 017 is a non-UI statistical execution phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Statistical execution smoke artifacts are written: passed.
- Every selected turn carries statistical evidence: passed.
- `statistics.attached` telemetry is present: passed.
- 20-turn regression reports `turns_have_statistical_evidence=True`: passed.
- Tests and validation pass: passed.

## Risks

- Semantic-slot mapping is coarse.
- Statistical evidence remains observational and exploratory.
- Regression runtime is higher because correction results are computed before the loop.

## Next Phase

Render statistical evidence in business reports and notebook/wiki memory so stakeholders can inspect the results without opening raw JSON.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
