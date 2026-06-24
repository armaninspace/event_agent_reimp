# Phase 032 Deliverables Status: Evolved Duplicate Follow-Ups

## Completed Items

- Added slot-specific follow-up rewriting for prior-knowledge duplicate OpenAI proposals.
- Preserved duplicate metadata and original proposal question in candidate reasoning.
- Allowed evolved duplicates to compete in semantic-slot diversity selection.
- Added evolved duplicate counts to session, phase regression, audit, and CLI output.
- Added focused tests for evolved duplicates and three-slot coverage.
- Ran MAF replay smoke.
- Ran a 20-turn OpenAI replay phase regression using Phase 027 prior knowledge.
- Refreshed replication audit against Phase 032.

## Blocked/Deferred Items

- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY`.
- Model-authored follow-up rewriting remains deferred until live OpenAI credentials are available.

## Files Changed

- `app/friends_loop.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_openai_reasoning.py`
- `tests/test_phase_regression.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-032-evolved-duplicate-followups/`
- `docs/phases/phase-032-evolved-duplicate-followups-engineering-requirements.md`
- `docs/backlog/phase-032-evolved-duplicate-followups-backlog.md`
- `docs/demos/phase-032-evolved-duplicate-followups-demo.md`
- `docs/deliverables-status/phase-032-evolved-duplicate-followups-status.md`

## Dependencies Installed

No new dependencies were installed.

## Tests Run

- `python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py -q`: passed, 9 tests.
- `python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-032-evolved-duplicate-followups`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-032-evolved-duplicate-followups --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-032-evolved-duplicate-followups --output-dir app/runs/phase-032-evolved-duplicate-followups`: passed.
- `python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q`: passed, 10 tests.
- `bash scripts/validate.sh`: passed, 64 tests.

## Demo Evidence

See `docs/demos/phase-032-evolved-duplicate-followups-demo.md`.

Generated artifacts:

- `app/runs/phase-032-evolved-duplicate-followups/phase_regression_summary.json`
- `app/runs/phase-032-evolved-duplicate-followups/replication_audit.json`
- `app/runs/phase-032-evolved-duplicate-followups/friends-question-loop/friends_loop_session.json`

## Acceptance Criteria Status

- Phase regression reports `prior_knowledge_evolved_duplicate_candidate_count=20`: passed.
- Phase regression reports `selected_unique_semantic_slot_count=3`: passed.
- Audit reports all three semantic slots represented: passed.
- Full validation passes: passed.

## Risks

- Template-based evolution is less flexible than live OpenAI revision.
- Replay evidence does not validate live model behavior.

## Commit Status

Pending until local commit completes.
