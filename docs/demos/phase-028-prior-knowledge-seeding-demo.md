# Phase 028 Demo: Prior Knowledge Seeding

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_notebook_knowledge_base.py tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-028-prior-knowledge-seeding --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-028-prior-knowledge-seeding --output-dir app/runs/phase-028-prior-knowledge-seeding
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- Regression reports 20 prior knowledge entries.
- Audit reports 20 prior knowledge entries.
- OpenAI reasoning traces contain prior notebook knowledge summaries.
- Validation passes.

## Observed Behavior

20-turn regression passed:

```text
notebook_knowledge_present=True
prior_notebook_knowledge_entry_count=20
reasoning_provider=openai
reasoning_mode=replay
executed_notebook_count=20
failed_notebook_count=0
```

Audit passed:

```text
notebook_knowledge_present=True
notebook_knowledge_entry_count=20
prior_notebook_knowledge_entry_count=20
selected_openai_reasoning_count=20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-028-prior-knowledge-seeding/phase_regression_summary.json
app/runs/phase-028-prior-knowledge-seeding/replication_audit.json
app/runs/phase-028-prior-knowledge-seeding/friends-question-loop/openai-reasoning/turn-01-openai-reasoning.json
```

## Video

No video was generated. This is a non-UI memory wiring phase; command-output evidence and generated trace JSON are the relevant demo evidence.

## Known Gaps

- Replay mode proves prompt context, not live model behavior.
- Candidate policy does not yet score duplicates from prior knowledge.

## Requirement Mapping

- Knowledge summary: `app/notebook_knowledge_base.py`
- Prompt context: `app/openai_reasoning.py`
- Loop telemetry: `app/friends_loop.py`
- Regression/audit: `app/phase_regression.py`, `app/replication_audit.py`
