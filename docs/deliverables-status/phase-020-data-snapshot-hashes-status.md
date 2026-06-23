# Phase 020 Deliverables Status: Data Snapshot Hashes

## Completed Items

- Added `app/data_snapshot.py`.
- Added SHA-256 hashing for joined city-week and MSA-week reference CSVs.
- Added byte counts and row counts for each hashed CSV.
- Added combined data snapshot SHA-256.
- Added `data_snapshot_complete` and `data_snapshot` to phase regression summaries.
- Added `data_snapshot_complete` and `data_snapshot_combined_sha256` to replication audits.
- Updated regression and audit CLIs.
- Added snapshot tests.
- Ran a 20-turn regression after adding data snapshot hashes.
- Refreshed the replication audit against the Phase 020 run.

## Blocked/Deferred Items

- Upstream raw/source file hashing remains deferred.
- External data correctness validation remains deferred.

## Files Changed

- `app/data_snapshot.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_data_snapshot.py`
- `tests/test_phase_regression.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-020-data-snapshot-hashes/phase_regression_summary.json`
- `app/runs/phase-020-data-snapshot-hashes/replication_audit.json`
- `app/runs/phase-020-data-snapshot-hashes/replication_audit.md`
- `app/runs/phase-020-data-snapshot-hashes/friends-question-loop/`
- `app/runs/phase-020-data-snapshot-hashes/notebooks/`
- `docs/phases/phase-020-data-snapshot-hashes-engineering-requirements.md`
- `docs/backlog/phase-020-data-snapshot-hashes-backlog.md`
- `docs/demos/phase-020-data-snapshot-hashes-demo.md`
- `docs/deliverables-status/phase-020-data-snapshot-hashes-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 020.

## Tests Run

- `python3 -m pytest tests/test_data_snapshot.py tests/test_phase_regression.py tests/test_replication_audit.py -q`: passed, 5 tests.
- `python3 scripts/run_phase_regression.py --phase-id phase-020-data-snapshot-hashes --turns 20`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-020-data-snapshot-hashes --output-dir app/runs/phase-020-data-snapshot-hashes`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-020-data-snapshot-hashes-demo.md`.

Generated artifacts:

- `app/runs/phase-020-data-snapshot-hashes/phase_regression_summary.json`
- `app/runs/phase-020-data-snapshot-hashes/replication_audit.json`
- `app/runs/phase-020-data-snapshot-hashes/replication_audit.md`

## Video Path Or Rationale

No video was generated. Phase 020 is a reproducibility/audit phase, and JSON/Markdown audit artifacts plus regression summary are the appropriate demo evidence.

## Acceptance Criteria Status

- Regression reports `data_snapshot_complete=True`: passed.
- Audit reports `data_snapshot_complete=True`: passed.
- Audit records the combined data snapshot SHA-256: passed.
- 20-turn regression passes: passed.
- Tests and validation pass: passed.

## Risks

- Hashes cover final joined reference CSVs only.
- Hashes prove reproducibility of local inputs, not external validity.

## Next Phase

Add a dedicated final corrections notebook so notebook-backed evidence includes an explicit multiple-testing correction artifact.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
