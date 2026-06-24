# Phase 030 Demo: Fuzzy Knowledge Duplicate Avoidance

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance
python3 scripts/run_phase_regression.py --phase-id phase-030-fuzzy-knowledge-duplicate-avoidance --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance --output-dir app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- A paraphrased prior seed is treated as a duplicate.
- Regression reports 20 prior-knowledge duplicate candidates.
- Audit reports 20 prior-knowledge duplicate candidates.
- Validation passes.

## Observed Behavior

Focused tests passed:

```text
9 passed
```

20-turn regression passed:

```text
prior_notebook_knowledge_entry_count=20
prior_knowledge_duplicate_candidate_count=20
completed_workflows=20
```

Audit passed:

```text
final_status=replicated_with_known_limits
prior_knowledge_duplicate_candidate_count=20
selected_openai_reasoning_count=20
causal_design_turn_count=20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance/phase_regression_summary.json
app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance/replication_audit.json
app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance/friends-question-loop/friends_loop_session.json
```

## Video

No video was generated. This is a non-UI ranking-policy phase; command-output evidence and generated JSON artifacts are the relevant demo evidence.

## Known Gaps

- Token-overlap matching is not full semantic embedding similarity.
- Replay output is fixed; live OpenAI behavior still needs credentials.

## Requirement Mapping

- Fuzzy duplicate marking: `app/friends_loop.py`
- Paraphrase test: `tests/test_openai_reasoning.py`
- Regression/audit artifacts: `app/runs/phase-030-fuzzy-knowledge-duplicate-avoidance/`
