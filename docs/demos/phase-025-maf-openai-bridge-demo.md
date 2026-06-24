# Phase 025 Demo: MAF OpenAI Bridge

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_maf_orchestration.py -q
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-025-maf-openai-bridge
python3 scripts/run_phase_regression.py --phase-id phase-025-maf-openai-bridge --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-025-maf-openai-bridge --output-dir app/runs/phase-025-maf-openai-bridge
bash scripts/validate.sh
```

## Expected Behavior

- MAF tests pass.
- MAF replay smoke reports OpenAI as the reasoning provider.
- MAF replay smoke produces three candidate questions.
- 20-turn regression passes.
- Audit reports MAF OpenAI bridge evidence.
- Validation passes.

## Observed Behavior

MAF tests passed:

```text
...                                                                      [100%]
```

MAF replay smoke passed:

```text
framework=Microsoft Agent Framework
package=agent-framework 1.9.0
workflow=codex-thesis-replication-workflow
reasoning_provider=openai
reasoning_mode=replay
candidate_count=3
output_count=1
model_calls_performed=False
```

20-turn regression passed:

```text
completed_workflows=20
reasoning_provider=openai
reasoning_mode=replay
selected_candidates_have_openai_reasoning=True
openai_model_calls_performed=False
executed_notebook_count=20
failed_notebook_count=0
```

Audit passed:

```text
selected_openai_reasoning_count=20
reasoning_provider=openai
reasoning_mode=replay
maf_adapter_present=True
maf_reasoning_provider=openai
maf_reasoning_mode=replay
maf_candidate_count=3
```

## Evidence

Generated artifacts:

```text
app/runs/phase-025-maf-openai-bridge/maf_adapter_smoke.json
app/runs/phase-025-maf-openai-bridge/maf_adapter_smoke.md
app/runs/phase-025-maf-openai-bridge/phase_regression_summary.json
app/runs/phase-025-maf-openai-bridge/replication_audit.json
```

## Video

No video was generated. This is a non-UI runtime-adapter phase; command-output evidence plus generated JSON/Markdown artifacts are the relevant demo evidence.

## Known Gaps

- Live MAF OpenAI smoke was not run because `OPENAI_API_KEY` is not present in this shell.
- Replay validates integration wiring, not live model quality.

## Requirement Mapping

- MAF OpenAI bridge: `app/maf_orchestration.py`
- CLI flags: `scripts/run_maf_adapter_smoke.py`
- Audit checks: `app/replication_audit.py`
- Tests: `tests/test_maf_orchestration.py`, `tests/test_replication_audit.py`
