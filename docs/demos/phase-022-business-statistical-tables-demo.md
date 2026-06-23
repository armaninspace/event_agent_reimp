# Phase 022 Demo: Business Statistical Tables

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_reporting.py tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-022-business-statistical-tables --turns 20
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-022-business-statistical-tables --output-dir app/runs/phase-022-business-statistical-tables
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Report and audit tests pass.
- 20-turn regression passes.
- Business report renders statistical result tables.
- Audit records 20 statistical sections and 20 statistical tables.
- Validation passes.

## Observed Behavior

Commands completed successfully.

```text
python3 -m pytest tests/test_reporting.py -q
...                                                                      [100%]
```

```text
python3 -m pytest tests/test_replication_audit.py -q
.                                                                        [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-022-business-statistical-tables --turns 20
wrote app/runs/phase-022-business-statistical-tables/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
turns_have_statistical_evidence=True
data_snapshot_complete=True
correction_notebook_present=True
correction_notebook_executed=True
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

## Evidence

Generated artifacts:

```text
app/runs/phase-022-business-statistical-tables/friends-question-loop/business_evidence_report.html
app/runs/phase-022-business-statistical-tables/phase_regression_summary.json
app/runs/phase-022-business-statistical-tables/replication_audit.json
```

Report checks:

```text
statistical-results table count: 20
contains "Adjusted p-value": True
contains matched city result ID: True
```

Audit summary:

```text
business_report_statistical_sections: 20
business_report_statistical_tables: 20
final_status: replicated_with_known_limits
```

## 20-Turn Regression

Implemented and passed after adding business-report statistical tables.

## Video

No video was generated. This is a static HTML reporting phase; generated HTML plus regression/audit JSON are the relevant demo outputs.

## Known Gaps

- No interactive charts.
- Tables still require reading caveats for correct interpretation.

## Requirement Mapping

- Report rendering: `app/reporting.py`
- Audit coverage: `app/replication_audit.py`
- Tests: `tests/test_reporting.py`, `tests/test_replication_audit.py`
