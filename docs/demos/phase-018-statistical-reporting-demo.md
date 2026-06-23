# Phase 018 Demo: Statistical Evidence Reporting

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_reporting.py tests/test_notebook_workspace.py -q
python3 scripts/run_phase_regression.py --phase-id phase-018-statistical-reporting --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Renderer tests pass.
- Business report renders statistical evidence safely.
- Per-turn Markdown notebooks render statistical evidence.
- Wiki findings record attached statistical results.
- 20-turn regression still passes.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest tests/test_reporting.py tests/test_notebook_workspace.py -q
......                                                                   [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-018-statistical-reporting --turns 20
wrote app/runs/phase-018-statistical-reporting/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
turns_have_statistical_evidence=True
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

## Evidence

Generated reporting artifacts:

```text
app/runs/phase-018-statistical-reporting/friends-question-loop/business_evidence_report.html
app/runs/phase-018-statistical-reporting/notebooks/turn-01-turn-01-crowd-spending.md
app/runs/phase-018-statistical-reporting/notebooks/findings.md
app/runs/phase-018-statistical-reporting/phase_regression_summary.json
```

Artifact checks:

```text
business report contains "Statistical Evidence": True
business report contains matched city result ID: True
turn-01 Markdown contains "Statistical Evidence": True
findings.md contains "attached 4 statistical results": True
business report statistical section count: 20
```

Regression summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
turns_have_statistical_evidence: True
```

## 20-Turn Regression

Implemented and passed after rendering statistical evidence in reports and notebook/wiki memory.

## Video

No video was generated. This is a static report/notebook rendering phase; generated HTML and Markdown artifacts are the relevant demo outputs.

## Known Gaps

- Detailed statistical tables remain in JSON rather than full HTML tables.
- No interactive charts.

## Requirement Mapping

- Business report rendering: `app/reporting.py`
- Notebook/wiki rendering: `app/notebook_workspace.py`
- Tests: `tests/test_reporting.py`, `tests/test_notebook_workspace.py`
