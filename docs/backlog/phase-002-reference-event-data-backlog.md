# Phase 002 Backlog: Reference Event Data

## P002-001: Implement Reference Data Contracts

- Stable item ID: `P002-001`
- Title: Add typed reference data records and loaders
- Rationale: Later phases need a reusable boundary for city-week and MSA-week data.
- Affected files/modules: `app/reference_data.py`
- Implementation steps: Add record dataclasses, loader functions, required-column contracts, and final-file loader.
- Unit test expectations: Fixture files load into stable records.
- E2E test expectations: Smoke script exercises real final files.
- Demo relevance: Quality report artifacts are generated from these loaders.
- Acceptance criteria: Loaded records expose grain, geography, week, exposure, and outcomes.
- Status: done

## P002-002: Implement Data Quality Reports

- Stable item ID: `P002-002`
- Title: Add explicit data quality checks and warnings
- Rationale: Warnings must be explicit for missing or weak data.
- Affected files/modules: `app/reference_data.py`
- Implementation steps: Add report dataclasses, counts, missing-value checks, weak-data warning rules, and Markdown rendering.
- Unit test expectations: Missing and weak fixture data produce warnings.
- E2E test expectations: Real final files produce a quality report.
- Demo relevance: Demo cites report summary and warnings.
- Acceptance criteria: Reports include row/geography/week/exposure counts and warning list.
- Status: done

## P002-003: Add Smoke Script

- Stable item ID: `P002-003`
- Title: Add repeatable reference data smoke command
- Rationale: Phase 002 needs a reproducible command that writes quality artifacts.
- Affected files/modules: `scripts/run_reference_data_smoke.py`
- Implementation steps: Load final files, build quality report, write JSON and Markdown outputs.
- Unit test expectations: Script functions are covered indirectly by report tests.
- E2E test expectations: `python3 scripts/run_reference_data_smoke.py --output-dir ...` succeeds.
- Demo relevance: Smoke output is the phase demo evidence.
- Acceptance criteria: JSON and Markdown reports are written.
- Status: done

## P002-004: Add Tests

- Stable item ID: `P002-004`
- Title: Add focused pytest coverage
- Rationale: Data contract regressions should be caught before orchestration depends on them.
- Affected files/modules: `tests/test_reference_data.py`
- Implementation steps: Add fixture CSV builders and tests for loading, quality reports, warnings, and artifact writing.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: Covered by validation.
- Demo relevance: Test output is recorded in phase docs.
- Acceptance criteria: Tests cover stable grain and explicit warnings.
- Status: done

## P002-005: Validate, Demo, Status, Commit

- Stable item ID: `P002-005`
- Title: Close Phase 002
- Rationale: The project protocol requires validation, demo, status, and a local commit.
- Affected files/modules: Phase 002 docs and repository state.
- Implementation steps: Run tests, run smoke script, run validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 002 is locally committed.
- Status: done
