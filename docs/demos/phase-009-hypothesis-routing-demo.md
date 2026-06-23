# Phase 009 Demo: Hypothesis Classification And Routing

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_phase_regression.py --phase-id phase-009-hypothesis-routing --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Regression command runs 20 deterministic friends-loop turns.
- Selected candidates include classification metadata.
- Workflow-task statistical misroutes are computed from turn metadata.
- Misroute count is zero.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.............................                                            [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-009-hypothesis-routing --turns 20
wrote app/runs/phase-009-hypothesis-routing/phase_regression_summary.json
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
29 passed in 17.49s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated summary:

```text
app/runs/phase-009-hypothesis-routing/phase_regression_summary.json
```

Summary fields:

```text
requested_turns: 20
completed_workflows: 20
workflow_task_statistical_misroutes: 0
current_required_artifacts_exist: True
notebook_workspace_present: True
```

First five selected-turn classifications:

```text
classification: eda_question, eda_question, eda_question, eda_question, eda_question
route: eda_review, eda_review, eda_review, eda_review, eda_review
```

## 20-Turn Regression

Implemented and passed. The regression now computes workflow-task statistical misroutes from turn classification metadata.

## Video

No video was generated. This is a non-UI routing/regression phase; command-output evidence plus generated session/regression artifacts are the relevant demo outputs.

## Known Gaps

- Classifier is deterministic and keyword/field based.
- No statistical test runner exists yet.
- No live LLM classification exists yet.

## Requirement Mapping

- Classifier: `app/hypothesis_routing.py`
- Loop metadata and telemetry: `app/friends_loop.py`
- Regression misroute count: `app/phase_regression.py`
- Tests: `tests/test_hypothesis_routing.py`, `tests/test_friends_loop.py`, `tests/test_phase_regression.py`
