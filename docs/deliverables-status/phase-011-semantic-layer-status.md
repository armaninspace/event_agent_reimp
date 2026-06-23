# Phase 011 Deliverables Status: Semantic SQL Layer

## Completed Items

- Installed and pinned `duckdb 1.5.4`.
- Added `app/semantic_layer.py`.
- Added whitelisted DuckDB views for `city_week_events` and `msa_week_events`.
- Added SELECT-only enforcement.
- Added non-whitelisted relation rejection.
- Added row limit enforcement.
- Added semantic query telemetry fields: SQL, referenced views, row count, columns, and preview.
- Added `scripts/run_semantic_smoke.py`.
- Added semantic layer tests.
- Ran semantic smoke on final CSVs.
- Ran a 20-turn regression after adding the semantic layer.

## Blocked/Deferred Items

- Persistent semantic cache deferred.
- Agent-generated SQL deferred.
- Rich metric definitions deferred.

## Files Changed

- `pyproject.toml`
- `docs/installed-software.md`
- `app/semantic_layer.py`
- `scripts/run_semantic_smoke.py`
- `tests/test_semantic_layer.py`
- `app/runs/phase-011-semantic-layer/semantic_smoke.json`
- `app/runs/phase-011-semantic-layer/semantic_smoke.md`
- `app/runs/phase-011-semantic-layer/phase_regression_summary.json`
- `app/runs/phase-011-semantic-layer/friends-question-loop/`
- `app/runs/phase-011-semantic-layer/notebooks/`
- `docs/phases/phase-011-semantic-layer-engineering-requirements.md`
- `docs/backlog/phase-011-semantic-layer-backlog.md`
- `docs/demos/phase-011-semantic-layer-demo.md`
- `docs/deliverables-status/phase-011-semantic-layer-status.md`

## Dependencies Installed

See `docs/installed-software.md`.

## Tests Run

- `python3 -m pytest -q`: passed, 36 tests.
- `python3 scripts/run_semantic_smoke.py --output-dir app/runs/phase-011-semantic-layer`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-011-semantic-layer --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-011-semantic-layer-demo.md`.

Generated artifacts:

- `app/runs/phase-011-semantic-layer/semantic_smoke.json`
- `app/runs/phase-011-semantic-layer/semantic_smoke.md`
- `app/runs/phase-011-semantic-layer/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 011 is a non-UI SQL/data-access phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Semantic smoke artifacts are written: passed.
- Guardrail tests pass: passed.
- 20-turn regression still passes: passed.
- Validation passes: passed.

## Risks

- Regex SQL guardrails are conservative but not a full SQL parser.
- Future agent-generated SQL should use stricter validation before broader query support.

## Next Phase

Phase 012 should integrate formal statistical hypotheses with the semantic/statistical execution path or add matched-control logic.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
