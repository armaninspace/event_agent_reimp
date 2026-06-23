# Phase 013 Deliverables Status: P-Values And Multiple Testing

## Completed Items

- Added `app/multiple_testing.py`.
- Added Welch p-values for exposed-vs-unexposed exploratory comparisons.
- Added one-sample t-test p-values for matched-control differences.
- Added Benjamini-Hochberg adjusted p-values across the smoke result family.
- Preserved observational caveats and removed stale no-p-value caveats from Phase 013 artifacts.
- Added `scripts/run_correction_smoke.py`.
- Added correction tests.
- Ran correction smoke on final CSVs.
- Ran a 20-turn regression after adding p-values and correction.

## Blocked/Deferred Items

- Statistical execution is not yet selected directly from forum-governed research questions.
- Publication-grade causal inference remains deferred.
- Rich model diagnostics remain deferred.

## Files Changed

- `app/multiple_testing.py`
- `scripts/run_correction_smoke.py`
- `tests/test_multiple_testing.py`
- `pyproject.toml`
- `docs/installed-software.md`
- `app/runs/phase-013-pvalues-multiple-testing/correction_smoke.json`
- `app/runs/phase-013-pvalues-multiple-testing/correction_smoke.md`
- `app/runs/phase-013-pvalues-multiple-testing/phase_regression_summary.json`
- `app/runs/phase-013-pvalues-multiple-testing/friends-question-loop/`
- `app/runs/phase-013-pvalues-multiple-testing/notebooks/`
- `docs/phases/phase-013-pvalues-multiple-testing-engineering-requirements.md`
- `docs/backlog/phase-013-pvalues-multiple-testing-backlog.md`
- `docs/demos/phase-013-pvalues-multiple-testing-demo.md`
- `docs/deliverables-status/phase-013-pvalues-multiple-testing-status.md`

## Dependencies Installed

- `scipy 1.18.0` via `python3 -m pip install scipy`

## Tests Run

- `python3 -m pytest -q`: passed, 41 tests.
- `python3 scripts/run_correction_smoke.py --output-dir app/runs/phase-013-pvalues-multiple-testing`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-013-pvalues-multiple-testing --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-013-pvalues-multiple-testing-demo.md`.

Generated artifacts:

- `app/runs/phase-013-pvalues-multiple-testing/correction_smoke.json`
- `app/runs/phase-013-pvalues-multiple-testing/correction_smoke.md`
- `app/runs/phase-013-pvalues-multiple-testing/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 013 is a non-UI statistical correction phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Correction smoke artifacts are written: passed.
- Results include raw and adjusted p-values: passed.
- Tests and validation pass: passed.
- 20-turn regression still passes: passed.

## Risks

- P-values can be overinterpreted without study-design context.
- Multiple-testing correction does not fix observational confounding.
- Future phases must connect governed research questions to statistical execution.

## Next Phase

Phase 014 should add a QuestionForum store so personas generate, rank, select, and carry governed question metadata through the 20-turn loop.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
