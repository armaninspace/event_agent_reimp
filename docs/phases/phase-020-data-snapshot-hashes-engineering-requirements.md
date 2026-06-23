# Phase 020: Data Snapshot Hashes

## Phase Goal

Remediate the audit/reimplementation gap that the phase contract should check data snapshot hashes, so regression and final audit evidence identify the exact joined reference CSV inputs used by the run.

## Requirements

- Compute SHA-256 hashes for final joined city-week and MSA-week CSVs.
- Record byte counts and CSV row counts for each file.
- Record a combined SHA-256 over the file paths and hashes.
- Add snapshot metadata to phase regression summaries.
- Add snapshot completeness and combined hash to replication audits.
- Add tests for snapshot generation, regression coverage, and audit coverage.
- Run a 20-turn regression and refresh the audit against it.

## Non-Goals

- Rebuilding source marts.
- Hashing every generated artifact.
- External data provenance registry.

## Assumptions

- The final joined reference CSVs are the current data inputs for local thesis replication.
- SHA-256 is sufficient for local reproducibility evidence.

## Affected Layers

- Reference data reproducibility
- Phase regression
- Final audit
- Tests
- Documentation

## Affected Modules

- `app/data_snapshot.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_data_snapshot.py`
- `tests/test_phase_regression.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required. Hashing uses Python standard library `hashlib`.

## Architecture Notes

Snapshot hashing is isolated in `app.data_snapshot` and reused by regression and audit layers. Regression writes the full snapshot; audit checks that snapshot metadata exists and records the combined hash.

## Data/API/Config Changes

- Phase regression summaries gain `data_snapshot_complete` and `data_snapshot`.
- Replication audits gain `data_snapshot_complete` and `data_snapshot_combined_sha256`.
- Regression CLI prints `data_snapshot_complete`.

## Demo Requirements

- Run snapshot/regression/audit tests.
- Run a 20-turn regression.
- Run replication audit against the new run.
- Record validation output.

## Test Requirements

- Snapshot helper computes file hashes and row counts.
- Phase regression summary includes a complete snapshot.
- Replication audit requires data snapshot coverage.
- Validation passes.

## Security/Sandbox Considerations

- Do not mutate source CSVs.
- Do not read `.env`.

## Risks

- Hashes prove byte identity, not correctness of upstream data collection.
- The current snapshot covers final joined reference files only.

## Acceptance Criteria

- Regression reports `data_snapshot_complete=True`.
- Audit reports `data_snapshot_complete=True`.
- Audit records the combined data snapshot SHA-256.
- 20-turn regression passes.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 020 commit or remove snapshot helper, regression/audit fields, tests, artifacts, and docs.
