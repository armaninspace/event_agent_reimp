# Phase 032 Demo: Evolved Duplicate Follow-Ups

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-032-evolved-duplicate-followups
python3 scripts/run_phase_regression.py --phase-id phase-032-evolved-duplicate-followups --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-032-evolved-duplicate-followups --output-dir app/runs/phase-032-evolved-duplicate-followups
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass.
- Duplicate city-week replay proposals become matched-control follow-ups.
- Regression reports 20 evolved duplicate candidates.
- Regression and audit report all three semantic slots.
- Validation passes.

## Observed Behavior

20-turn regression passed:

```text
prior_knowledge_duplicate_candidate_count=20
prior_knowledge_evolved_duplicate_candidate_count=20
selected_semantic_slot_counts={'city_week_event_spending': 7, 'identification_risk': 6, 'msa_week_coverage': 7}
selected_unique_semantic_slot_count=3
```

Audit passed:

```text
final_status=replicated_with_known_limits
prior_knowledge_evolved_duplicate_candidate_count=20
selected_semantic_slot_counts={'city_week_event_spending': 7, 'identification_risk': 6, 'msa_week_coverage': 7}
selected_unique_semantic_slot_count=3
```

## Evidence

Generated artifacts:

```text
app/runs/phase-032-evolved-duplicate-followups/phase_regression_summary.json
app/runs/phase-032-evolved-duplicate-followups/replication_audit.json
app/runs/phase-032-evolved-duplicate-followups/friends-question-loop/friends_loop_session.json
```

## Video

No video was generated. This is a non-UI reasoning-policy phase; command-output evidence and generated JSON artifacts are the relevant demo evidence.

## Known Gaps

- Follow-up questions are deterministic templates in replay mode.
- Replay output is fixed; live OpenAI behavior still needs credentials.

## Requirement Mapping

- Evolved duplicate construction: `app/friends_loop.py`
- Regression/audit fields: `app/phase_regression.py`, `app/replication_audit.py`
- Tests: `tests/test_openai_reasoning.py`, `tests/test_phase_regression.py`, `tests/test_replication_audit.py`
