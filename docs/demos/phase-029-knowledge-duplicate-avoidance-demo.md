# Phase 029 Demo: Knowledge Duplicate Avoidance

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-029-knowledge-duplicate-avoidance --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-029-knowledge-duplicate-avoidance --output-dir app/runs/phase-029-knowledge-duplicate-avoidance
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- Regression reports 20 prior-knowledge duplicate candidates.
- Audit reports 20 prior-knowledge duplicate candidates.
- Selected candidates shift away from the repeated prior city-week seed.
- Validation passes.

## Observed Behavior

20-turn regression passed:

```text
prior_notebook_knowledge_entry_count=20
prior_knowledge_duplicate_candidate_count=20
completed_workflows=20
```

Audit passed:

```text
prior_knowledge_duplicate_candidate_count=20
selected_openai_reasoning_count=20
causal_design_turn_count=20
```

Selected slot summary:

```text
selected_slots {'msa_week_coverage': 20}
duplicate_candidates 20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-029-knowledge-duplicate-avoidance/phase_regression_summary.json
app/runs/phase-029-knowledge-duplicate-avoidance/replication_audit.json
app/runs/phase-029-knowledge-duplicate-avoidance/friends-question-loop/friends_loop_session.json
```

## Video

No video was generated. This is a non-UI ranking-policy phase; command-output evidence and generated JSON artifacts are the relevant demo evidence.

## Known Gaps

- Duplicate detection is exact string matching.
- Replay output is fixed; live OpenAI behavior still needs credentials.

## Requirement Mapping

- Duplicate marking: `app/friends_loop.py`
- Regression/audit fields: `app/phase_regression.py`, `app/replication_audit.py`
- Tests: `tests/test_openai_reasoning.py`, `tests/test_replication_audit.py`
