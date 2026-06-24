# Phase 031 Demo: Semantic Slot Diversity

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py -q
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-031-semantic-slot-diversity
python3 scripts/run_phase_regression.py --phase-id phase-031-semantic-slot-diversity --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-031-semantic-slot-diversity --output-dir app/runs/phase-031-semantic-slot-diversity
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- Regression reports 20 completed workflows.
- Prior-knowledge duplicate count remains 20.
- Selected semantic slots are split across non-duplicate slots.
- Audit reports the same semantic slot coverage.
- Validation passes.

## Observed Behavior

20-turn regression passed:

```text
prior_knowledge_duplicate_candidate_count=20
selected_semantic_slot_counts={'identification_risk': 10, 'msa_week_coverage': 10}
selected_unique_semantic_slot_count=2
completed_workflows=20
```

Audit passed:

```text
final_status=replicated_with_known_limits
selected_semantic_slot_counts={'identification_risk': 10, 'msa_week_coverage': 10}
selected_unique_semantic_slot_count=2
selected_openai_reasoning_count=20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-031-semantic-slot-diversity/phase_regression_summary.json
app/runs/phase-031-semantic-slot-diversity/replication_audit.json
app/runs/phase-031-semantic-slot-diversity/friends-question-loop/friends_loop_session.json
```

## Video

No video was generated. This is a non-UI selection-policy phase; command-output evidence and generated JSON artifacts are the relevant demo evidence.

## Known Gaps

- City-week event-spending remains suppressed because the provided prior notebook knowledge marks that replay proposal as a duplicate.
- Replay output is fixed; live OpenAI behavior still needs credentials.

## Requirement Mapping

- Diversity selector: `app/friends_loop.py`
- Regression/audit fields: `app/phase_regression.py`, `app/replication_audit.py`
- Tests: `tests/test_openai_reasoning.py`, `tests/test_phase_regression.py`, `tests/test_replication_audit.py`
