# Phase 024 Demo: OpenAI Reasoning

## Setup

Run from the repository root:

```sh
cd /code
```

Live mode requires:

```sh
export OPENAI_API_KEY="..."
```

## Commands

```sh
python3 -m pytest tests/test_openai_reasoning.py tests/test_friends_loop.py tests/test_phase_regression.py -q
python3 scripts/run_openai_reasoning_smoke.py --mode replay --turns 2 --replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-024-openai-reasoning/openai-smoke
python3 scripts/run_openai_reasoning_smoke.py --mode live --turns 1 --output-dir app/runs/phase-024-openai-reasoning/live-smoke-missing-key
python3 scripts/run_phase_regression.py --phase-id phase-024-openai-reasoning --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-024-openai-reasoning --output-dir app/runs/phase-024-openai-reasoning
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- Replay smoke writes OpenAI provenance artifacts and reports `model_calls_performed=False`.
- Live smoke exits with a credential error when `OPENAI_API_KEY` is absent.
- 20-turn replay regression passes with `reasoning_provider=openai`.
- Audit reports 20 OpenAI reasoning records.
- Validation passes.

## Observed Behavior

Focused tests completed successfully:

```text
...........                                                              [100%]
```

Replay smoke completed successfully:

```text
mode=replay
provider=openai
model_calls_performed=False
selected_candidate_count=2
```

Live smoke without credentials failed honestly:

```text
OPENAI_API_KEY is required for --mode live.
```

20-turn replay regression completed successfully:

```text
requested_turns=20
completed_workflows=20
reasoning_provider=openai
reasoning_mode=replay
selected_candidates_have_openai_reasoning=True
openai_model_calls_performed=False
executed_notebook_count=20
failed_notebook_count=0
```

Audit completed successfully:

```text
final_status=replicated_with_known_limits
completed_twenty_turns=True
selected_openai_reasoning_count=20
openai_model_calls_performed=False
reasoning_provider=openai
reasoning_mode=replay
```

## Evidence

Generated artifacts:

```text
app/runs/phase-024-openai-reasoning/friends-question-loop/friends_loop_session.json
app/runs/phase-024-openai-reasoning/friends-question-loop/openai-reasoning/turn-01-openai-reasoning.json
app/runs/phase-024-openai-reasoning/openai-smoke/openai_reasoning_smoke.json
app/runs/phase-024-openai-reasoning/phase_regression_summary.json
app/runs/phase-024-openai-reasoning/replication_audit.json
```

## 20-Turn Regression

Implemented and passed with OpenAI replay provenance. Live OpenAI mode was not run because `OPENAI_API_KEY` is not available in this shell.

## Requirement Mapping

- OpenAI client and parser: `app/openai_reasoning.py`
- Friends-loop integration: `app/friends_loop.py`
- Regression integration: `app/phase_regression.py`
- Audit coverage: `app/replication_audit.py`
- Smoke command: `scripts/run_openai_reasoning_smoke.py`
- Tests: `tests/test_openai_reasoning.py`
