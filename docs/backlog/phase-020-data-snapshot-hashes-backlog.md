# Phase 020 Backlog: Data Snapshot Hashes

## P020-001: Implement Reference Data Snapshot Hashing

- Stable item ID: `P020-001`
- Title: Add SHA-256 data snapshot metadata
- Rationale: The audit contract should identify exact input data bytes.
- Affected files/modules: `app/data_snapshot.py`
- Implementation steps: Hash joined reference CSVs, count rows/bytes, produce combined hash.
- Unit test expectations: Snapshot helper is tested.
- E2E test expectations: Phase regression writes snapshot metadata.
- Demo relevance: Snapshot hashes are audit evidence.
- Acceptance criteria: Snapshot metadata is complete.
- Status: done

## P020-002: Integrate Snapshot Into Regression And Audit

- Stable item ID: `P020-002`
- Title: Require data snapshot coverage
- Rationale: The replication audit should fail if regression lacks data snapshot hashes.
- Affected files/modules: `app/phase_regression.py`, `app/replication_audit.py`, scripts and tests.
- Implementation steps: Add summary/audit fields, CLI output, and tests.
- Unit test expectations: Regression and audit tests assert snapshot coverage.
- E2E test expectations: Audit against Phase 020 run passes.
- Demo relevance: Audit JSON/Markdown includes data snapshot coverage.
- Acceptance criteria: Audit records combined snapshot hash.
- Status: done

## P020-003: Validate, Demo, Status, Commit

- Stable item ID: `P020-003`
- Title: Close Phase 020
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 020 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, audit, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 020 is locally committed.
- Status: done
