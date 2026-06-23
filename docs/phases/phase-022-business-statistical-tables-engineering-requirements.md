# Phase 022: Business Statistical Tables

## Phase Goal

Remediate the report presentation gap by rendering full per-turn statistical result tables in the stakeholder-facing business report.

## Requirements

- Render a table of statistical result rows for every turn with attached statistical evidence.
- Include result ID, family, dataset, outcome, p-value, adjusted p-value, and status.
- Escape table content in HTML.
- Add audit coverage for statistical result table count.
- Keep 20-turn regression passing.

## Non-Goals

- Interactive charts.
- New statistical calculations.
- Publication layout redesign.

## Assumptions

- Phase 017 statistical evidence already carries result dictionaries.
- Static HTML tables are sufficient for stakeholder inspection.

## Affected Layers

- Business report rendering
- Final audit
- Tests
- Documentation

## Affected Modules

- `app/reporting.py`
- `app/replication_audit.py`
- `scripts/run_replication_audit.py`
- `tests/test_reporting.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The report renderer keeps summary fields and appends a compact table when `statistical_evidence["results"]` exists. Audit counts tables via the `statistical-results` CSS class.

## Data/API/Config Changes

- Business report sections include statistical results tables.
- Replication audit gains `business_report_statistical_tables`.

## Demo Requirements

- Run report and audit tests.
- Run a 20-turn regression.
- Run replication audit against the new report.
- Record validation output.

## Test Requirements

- Report table rendering and escaping are tested.
- Audit requires 20 statistical result tables in the latest run.
- Validation passes.

## Security/Sandbox Considerations

- Escape result IDs and caveats in HTML.
- Preserve observational caveats.

## Risks

- Tables improve inspectability but can still be overinterpreted without caveats.

## Acceptance Criteria

- Business report renders 20 statistical result tables in a 20-turn run.
- Audit reports `business_report_statistical_tables=20`.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 022 commit or remove report-table rendering, audit field, tests, artifacts, and docs.
