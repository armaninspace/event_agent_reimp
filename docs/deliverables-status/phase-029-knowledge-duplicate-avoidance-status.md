# Phase 029 Deliverables Status: Knowledge Duplicate Avoidance

## Completed Items

- Added exact prior-seed duplicate detection for OpenAI proposals.
- Added `prior_knowledge_duplicate` candidate reasoning metadata.
- Penalized duplicate proposal novelty before tournament ranking.
- Added duplicate candidate counts to session, phase regression, and audit.
- Added focused tests.
- Ran MAF replay smoke.
- Ran a 20-turn OpenAI replay phase regression using Phase 027 prior knowledge.
- Refreshed replication audit against Phase 029.

## Blocked/Deferred Items

- Fuzzy/semantic duplicate matching remains deferred.
- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY`.

## Files Changed

- `app/friends_loop.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_openai_reasoning.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-029-knowledge-duplicate-avoidance/`
- `docs/phases/phase-029-knowledge-duplicate-avoidance-engineering-requirements.md`
- `docs/backlog/phase-029-knowledge-duplicate-avoidance-backlog.md`
- `docs/demos/phase-029-knowledge-duplicate-avoidance-demo.md`
- `docs/deliverables-status/phase-029-knowledge-duplicate-avoidance-status.md`

## Dependencies Installed

No new dependencies were installed.

## Tests Run

- `python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py -q`: passed, 8 tests.
- `python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q`: passed, 9 tests.
- `python3 scripts/run_phase_regression.py --phase-id phase-029-knowledge-duplicate-avoidance --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-029-knowledge-duplicate-avoidance --output-dir app/runs/phase-029-knowledge-duplicate-avoidance`: passed.
- `bash scripts/validate.sh`: passed, 63 tests.

## Demo Evidence

See `docs/demos/phase-029-knowledge-duplicate-avoidance-demo.md`.

Generated artifacts:

- `app/runs/phase-029-knowledge-duplicate-avoidance/phase_regression_summary.json`
- `app/runs/phase-029-knowledge-duplicate-avoidance/replication_audit.json`
- `app/runs/phase-029-knowledge-duplicate-avoidance/friends-question-loop/friends_loop_session.json`

## Acceptance Criteria Status

- Phase regression reports `prior_knowledge_duplicate_candidate_count=20`: passed.
- Audit reports `prior_knowledge_duplicate_candidate_count=20`: passed.
- Selected candidates move away from the repeated prior seed: passed.
- Full validation passes: passed.

## Risks

- Exact matching misses paraphrases.
- Replay evidence does not validate live model behavior.

## Commit Status

Pending until local commit completes.
