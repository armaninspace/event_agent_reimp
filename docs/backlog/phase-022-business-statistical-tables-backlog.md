# Phase 022 Backlog: Business Statistical Tables

## P022-001: Render Statistical Result Tables

- Stable item ID: `P022-001`
- Title: Add full statistical tables to business report
- Rationale: Stakeholders should inspect adjusted p-values and statuses without opening JSON.
- Affected files/modules: `app/reporting.py`, `tests/test_reporting.py`
- Implementation steps: Render escaped table rows for result ID, family, dataset, outcome, p-value, adjusted p-value, and status.
- Unit test expectations: Table rendering and escaping are tested.
- E2E test expectations: 20-turn business report has statistical tables.
- Demo relevance: Generated HTML is phase evidence.
- Acceptance criteria: Report contains statistical result tables.
- Status: done

## P022-002: Audit Report Table Coverage

- Stable item ID: `P022-002`
- Title: Count statistical tables in final audit
- Rationale: Report-table remediation should be enforced by the audit.
- Affected files/modules: `app/replication_audit.py`, `tests/test_replication_audit.py`
- Implementation steps: Count `statistical-results` tables and assert 20 in final audit.
- Unit test expectations: Audit test checks table count.
- E2E test expectations: Audit against Phase 022 run passes.
- Demo relevance: Audit JSON records table coverage.
- Acceptance criteria: Audit reports `business_report_statistical_tables=20`.
- Status: done

## P022-003: Validate, Demo, Status, Commit

- Stable item ID: `P022-003`
- Title: Close Phase 022
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 022 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, audit, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 022 is locally committed.
- Status: done
