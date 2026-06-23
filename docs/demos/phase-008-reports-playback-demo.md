# Phase 008 Demo: Reports And Playback

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_phase_regression.py --phase-id phase-008-reports-playback --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Regression command runs 20 deterministic friends-loop turns.
- Business evidence report is written.
- Playback UI is written.
- Regression summary requires report/playback artifacts.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.........................                                                [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-008-reports-playback --turns 20
wrote app/runs/phase-008-reports-playback/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

```text
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
25 passed in 17.33s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated files:

```text
app/runs/phase-008-reports-playback/friends-question-loop/business_evidence_report.html
app/runs/phase-008-reports-playback/friends-question-loop/ui/index.html
app/runs/phase-008-reports-playback/phase_regression_summary.json
```

Artifact checks:

```text
business_evidence_report: True
playback_ui: True
session_json: True
session_markdown: True
telemetry_json: True
discovery_decision_summary: True
current_required_artifacts_exist: True
```

## 20-Turn Regression

Implemented and passed. The regression gate now requires business report and playback UI artifacts.

## Video

No video was generated. Static HTML artifacts are inspectable directly in the browser; command-output evidence and generated files are the relevant demo outputs for this phase.

## Known Gaps

- Report is static and intentionally basic.
- Playback UI is static and embedded-data only.
- Statistical results remain deferred.
- Live Microsoft Agent Framework orchestration remains deferred.

## Requirement Mapping

- Report renderer: `app/reporting.py`
- Artifact integration: `app/friends_loop.py`
- Regression checks: `app/phase_regression.py`
- Tests: `tests/test_reporting.py`, `tests/test_friends_loop.py`, `tests/test_phase_regression.py`
