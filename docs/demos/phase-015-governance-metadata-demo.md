# Phase 015 Demo: Governance Metadata

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_question_governance.py tests/test_friends_loop.py tests/test_phase_regression.py -q
python3 scripts/run_governance_smoke.py --output-dir app/runs/phase-015-governance-metadata --turns 3
python3 scripts/run_phase_regression.py --phase-id phase-015-governance-metadata --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Governance unit tests pass.
- Governance smoke writes JSON and Markdown artifacts.
- Selected candidates carry tournament, reflection, and evolution metadata.
- Governance telemetry events are present.
- 20-turn regression reports selected-candidate metadata coverage.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest tests/test_question_governance.py tests/test_friends_loop.py tests/test_phase_regression.py -q
..........                                                               [100%]
```

```text
python3 scripts/run_governance_smoke.py --output-dir app/runs/phase-015-governance-metadata --turns 3
wrote app/runs/phase-015-governance-metadata/governance_smoke.json
wrote app/runs/phase-015-governance-metadata/governance_smoke.md
turn_count=3
all_selected_have_tournament=True
all_selected_have_reflection=True
all_selected_have_evolution=True
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-015-governance-metadata --turns 20
wrote app/runs/phase-015-governance-metadata/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

## Evidence

Generated governance artifacts:

```text
app/runs/phase-015-governance-metadata/governance_smoke.json
app/runs/phase-015-governance-metadata/governance_smoke.md
app/runs/phase-015-governance-metadata/phase_regression_summary.json
```

Governance smoke summary:

```text
turn_count: 3
all_selected_have_tournament: True
all_selected_have_reflection: True
all_selected_have_evolution: True
turn-01-crowd-spending: forum=crowd-spending, rank=1, reflection=pass, evolution=carry_forward
turn-02-market-coverage: forum=market-coverage, rank=1, reflection=pass, evolution=combine
turn-03-market-coverage: forum=market-coverage, rank=1, reflection=pass, evolution=strengthen
```

Regression summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
selected_candidate_count: 20
selected_candidates_have_required_metadata: True
governance telemetry: tournament.completed, reflection.completed, evolution.completed
selected evolution actions: carry_forward, combine, strengthen
```

## 20-Turn Regression

Implemented and passed after adding tournament, reflection, and evolution metadata.

## Video

No video was generated. This is a non-UI candidate-governance phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- Governance is deterministic and heuristic, not model-generated debate.
- Evolution records action metadata but does not rewrite source forum questions.
- Literature grounding is not implemented.

## Requirement Mapping

- Tournament: `app/question_tournament.py`
- Reflection: `app/question_reflection.py`
- Evolution: `app/question_evolution.py`
- Loop integration: `app/friends_loop.py`
- Regression contract: `app/phase_regression.py`
- Smoke command: `scripts/run_governance_smoke.py`
- Tests: `tests/test_question_governance.py`, `tests/test_friends_loop.py`
