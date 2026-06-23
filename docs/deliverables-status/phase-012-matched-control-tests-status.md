# Phase 012 Deliverables Status: Matched Control Tests

## Completed Items

- Added `app/matched_tests.py`.
- Added same-week/same-block matched-control comparisons.
- Added city-week matching via `event_msa_block_id`.
- Added MSA-week matching via `msa_block_id`.
- Added outcome support for `revenue_all` and `merchants_all`.
- Added diagnostics and caveats to every matched result.
- Added `scripts/run_matched_smoke.py`.
- Added matched-control tests.
- Ran matched smoke on final CSVs.
- Ran a 20-turn regression after adding matched tests.

## Blocked/Deferred Items

- P-values and adjusted p-values deferred.
- Multiple-testing correction deferred.
- Rich matching diagnostics deferred.
- Statistical execution is not yet integrated into friends-loop selected candidates.

## Files Changed

- `app/matched_tests.py`
- `scripts/run_matched_smoke.py`
- `tests/test_matched_tests.py`
- `app/runs/phase-012-matched-control-tests/matched_smoke.json`
- `app/runs/phase-012-matched-control-tests/matched_smoke.md`
- `app/runs/phase-012-matched-control-tests/phase_regression_summary.json`
- `app/runs/phase-012-matched-control-tests/friends-question-loop/`
- `app/runs/phase-012-matched-control-tests/notebooks/`
- `docs/phases/phase-012-matched-control-tests-engineering-requirements.md`
- `docs/backlog/phase-012-matched-control-tests-backlog.md`
- `docs/demos/phase-012-matched-control-tests-demo.md`
- `docs/deliverables-status/phase-012-matched-control-tests-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 012.

## Tests Run

- `python3 -m pytest -q`: passed, 39 tests.
- `python3 scripts/run_matched_smoke.py --output-dir app/runs/phase-012-matched-control-tests`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-012-matched-control-tests --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-012-matched-control-tests-demo.md`.

Generated artifacts:

- `app/runs/phase-012-matched-control-tests/matched_smoke.json`
- `app/runs/phase-012-matched-control-tests/matched_smoke.md`
- `app/runs/phase-012-matched-control-tests/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 012 is a non-UI statistical smoke phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Matched smoke artifacts are written: passed.
- Results include diagnostics and caveats: passed.
- Tests and validation pass: passed.
- 20-turn regression still passes: passed.

## Risks

- Same-block/same-week matching does not eliminate all confounding.
- Future phases must add p-values, adjusted p-values, and stronger diagnostics before claim promotion.

## Next Phase

Phase 013 should add p-values and multiple-testing correction or integrate formal statistical hypotheses into the router/execution path.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
