# Phase 031 Deliverables Status: Semantic Slot Diversity

## Completed Items

- Added in-run selected semantic slot counts.
- Added candidate reasoning metadata for prior semantic slot selection count.
- Added least-used non-duplicate semantic slot selection after tournament ranking.
- Added semantic slot coverage fields to session, phase regression, audit, and CLI output.
- Added focused tests for replay and deterministic coverage.
- Ran MAF replay smoke.
- Ran a 20-turn OpenAI replay phase regression using Phase 027 prior knowledge.
- Refreshed replication audit against Phase 031.

## Blocked/Deferred Items

- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY`.
- Covering all three replay slots without selecting a prior duplicate requires a larger replay corpus or live model output.

## Files Changed

- `app/friends_loop.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_openai_reasoning.py`
- `tests/test_phase_regression.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-031-semantic-slot-diversity/`
- `docs/phases/phase-031-semantic-slot-diversity-engineering-requirements.md`
- `docs/backlog/phase-031-semantic-slot-diversity-backlog.md`
- `docs/demos/phase-031-semantic-slot-diversity-demo.md`
- `docs/deliverables-status/phase-031-semantic-slot-diversity-status.md`

## Dependencies Installed

No new dependencies were installed.

## Tests Run

- `python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py -q`: passed, 9 tests.
- `python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-031-semantic-slot-diversity`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-031-semantic-slot-diversity --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-031-semantic-slot-diversity --output-dir app/runs/phase-031-semantic-slot-diversity`: passed.
- `python3 -m pytest tests/test_openai_reasoning.py tests/test_phase_regression.py tests/test_replication_audit.py -q`: passed, 10 tests.
- `bash scripts/validate.sh`: passed, 64 tests.

## Demo Evidence

See `docs/demos/phase-031-semantic-slot-diversity-demo.md`.

Generated artifacts:

- `app/runs/phase-031-semantic-slot-diversity/phase_regression_summary.json`
- `app/runs/phase-031-semantic-slot-diversity/replication_audit.json`
- `app/runs/phase-031-semantic-slot-diversity/friends-question-loop/friends_loop_session.json`

## Acceptance Criteria Status

- Phase regression reports split semantic slot counts: passed.
- Audit reports `selected_unique_semantic_slot_count=2`: passed.
- Prior-knowledge duplicate candidate count remains 20: passed.
- Full validation passes: passed.

## Risks

- Diversity preference can override strict tournament order.
- Replay evidence does not validate live model behavior.

## Commit Status

Pending until local commit completes.
