# Phase 010 Deliverables Status: Exploratory Statistical Tests

## Completed Items

- Added `app/statistical_tests.py`.
- Added exposed-vs-unexposed descriptive comparisons for final city-week and MSA-week CSVs.
- Added outcome support for `revenue_all` and `merchants_all`.
- Added diagnostics and caveats to every result.
- Added `scripts/run_statistical_smoke.py`.
- Added statistical tests for difference calculation, not-testable handling, and artifact writing.
- Ran statistical smoke on final CSVs.
- Ran a 20-turn regression after adding the statistics layer.

## Blocked/Deferred Items

- Full matched controls deferred.
- P-values and adjusted p-values deferred.
- Multiple-testing correction deferred.
- Statistical execution is not yet integrated into the friends-loop router.

## Files Changed

- `app/statistical_tests.py`
- `scripts/run_statistical_smoke.py`
- `tests/test_statistical_tests.py`
- `app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.json`
- `app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.md`
- `app/runs/phase-010-exploratory-statistical-tests/phase_regression_summary.json`
- `app/runs/phase-010-exploratory-statistical-tests/friends-question-loop/`
- `app/runs/phase-010-exploratory-statistical-tests/notebooks/`
- `docs/phases/phase-010-exploratory-statistical-tests-engineering-requirements.md`
- `docs/backlog/phase-010-exploratory-statistical-tests-backlog.md`
- `docs/demos/phase-010-exploratory-statistical-tests-demo.md`
- `docs/deliverables-status/phase-010-exploratory-statistical-tests-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 010.

## Tests Run

- `python3 -m pytest -q`: passed, 32 tests.
- `python3 scripts/run_statistical_smoke.py --output-dir app/runs/phase-010-exploratory-statistical-tests`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-010-exploratory-statistical-tests --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-010-exploratory-statistical-tests-demo.md`.

Generated artifacts:

- `app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.json`
- `app/runs/phase-010-exploratory-statistical-tests/statistical_smoke.md`
- `app/runs/phase-010-exploratory-statistical-tests/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 010 is a non-UI statistical smoke phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Statistical smoke artifacts are written: passed.
- Results include diagnostics and caveats: passed.
- Tests and validation pass: passed.
- 20-turn regression still passes: passed.

## Risks

- Descriptive differences can be overinterpreted.
- Matching and multiple-testing correction are still required before stronger evidence claims.

## Next Phase

Phase 011 should implement matched controls or a semantic SQL layer, then integrate formal statistical hypotheses with the router.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
