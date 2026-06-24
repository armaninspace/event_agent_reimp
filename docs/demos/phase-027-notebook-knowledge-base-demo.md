# Phase 027 Demo: Notebook Knowledge Base

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_notebook_knowledge_base.py tests/test_notebook_workspace.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-027-notebook-knowledge-base
python3 scripts/run_phase_regression.py --phase-id phase-027-notebook-knowledge-base --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-027-notebook-knowledge-base --output-dir app/runs/phase-027-notebook-knowledge-base
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- Regression writes notebook knowledge artifacts.
- Audit reports 20 knowledge entries.
- Validation passes.

## Observed Behavior

20-turn regression passed:

```text
notebook_workspace_present=True
notebook_knowledge_present=True
executed_notebook_count=20
failed_notebook_count=0
```

Audit passed:

```text
notebook_knowledge_present=True
notebook_knowledge_entry_count=20
selected_openai_reasoning_count=20
causal_design_turn_count=20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.md
app/runs/phase-027-notebook-knowledge-base/phase_regression_summary.json
app/runs/phase-027-notebook-knowledge-base/replication_audit.json
```

## Video

No video was generated. This is a non-UI artifact-memory phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo evidence.

## Known Gaps

- Candidate generation does not yet consume notebook knowledge entries.
- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY`.

## Requirement Mapping

- Knowledge extractor: `app/notebook_knowledge_base.py`
- Regression integration: `app/phase_regression.py`
- Audit checks: `app/replication_audit.py`
- Tests: `tests/test_notebook_knowledge_base.py`, `tests/test_replication_audit.py`
