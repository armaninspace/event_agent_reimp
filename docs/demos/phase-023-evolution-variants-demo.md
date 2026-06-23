# Phase 023 Demo: Evolution Variants

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_question_governance.py tests/test_friends_loop.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-023-evolution-variants --turns 20
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-023-evolution-variants --output-dir app/runs/phase-023-evolution-variants
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- 20-turn regression passes.
- Every selected candidate carries evolution variant metadata.
- Audit records 20 evolution variants.
- Validation passes.

## Observed Behavior

Commands completed successfully.

```text
python3 -m pytest tests/test_question_governance.py tests/test_friends_loop.py tests/test_phase_regression.py -q
..........                                                               [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-023-evolution-variants --turns 20
wrote app/runs/phase-023-evolution-variants/phase_regression_summary.json
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
app/runs/phase-023-evolution-variants/friends-question-loop/friends_loop_session.json
app/runs/phase-023-evolution-variants/phase_regression_summary.json
app/runs/phase-023-evolution-variants/replication_audit.json
```

Evolution variant summary:

```text
selected_evolution_metadata_count: 20
selected_evolution_variant_count: 20
actions: carry_forward, combine, strengthen
turn-01 child_question_id: crowd-spending:carry_forward
turn-01 evolved_question: Do big sports crowds actually turn into more local spending?
turn-03 child_question_id: market-coverage:strengthen
turn-03 evolved_question: What stronger checks would make this prior question more reliable: Which markets have enough event exposure for a careful spending comparison?
```

Audit summary:

```text
final_status: replicated_with_known_limits
selected_evolution_metadata_count: 20
selected_evolution_variant_count: 20
```

## 20-Turn Regression

Implemented and passed after adding deterministic evolved question variants.

## Video

No video was generated. This is a governance metadata phase; session JSON plus regression/audit summaries are the relevant demo outputs.

## Known Gaps

- Variants are deterministic, not live model-generated rewrites.
- Parent/child IDs are not stored in a graph database.

## Requirement Mapping

- Evolution variants: `app/question_evolution.py`
- Regression check: `app/phase_regression.py`
- Audit count: `app/replication_audit.py`
- Tests: `tests/test_question_governance.py`, `tests/test_friends_loop.py`, `tests/test_replication_audit.py`
