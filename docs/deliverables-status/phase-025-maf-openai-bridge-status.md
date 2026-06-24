# Phase 025 Deliverables Status: MAF OpenAI Bridge

## Completed Items

- Added a Microsoft Agent Framework workflow branch that invokes OpenAI hypothesis generation.
- Preserved deterministic MAF workflow behavior.
- Added MAF report fields for reasoning provider, mode, model, candidate count, candidate questions, traces, and model-call status.
- Added MAF smoke CLI flags for replay/live OpenAI reasoning.
- Added MAF replay test coverage.
- Updated replication audit to check MAF OpenAI bridge evidence.
- Ran MAF replay smoke.
- Ran a 20-turn OpenAI replay phase regression.
- Refreshed replication audit against Phase 025.

## Blocked/Deferred Items

- Live MAF OpenAI smoke was not run because `OPENAI_API_KEY` is not present in this shell.
- Full live model quality remains unvalidated in committed artifacts.

## Files Changed

- `app/maf_orchestration.py`
- `scripts/run_maf_adapter_smoke.py`
- `app/replication_audit.py`
- `scripts/run_replication_audit.py`
- `tests/test_maf_orchestration.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-025-maf-openai-bridge/`
- `docs/phases/phase-025-maf-openai-bridge-engineering-requirements.md`
- `docs/backlog/phase-025-maf-openai-bridge-backlog.md`
- `docs/demos/phase-025-maf-openai-bridge-demo.md`
- `docs/deliverables-status/phase-025-maf-openai-bridge-status.md`

## Dependencies Installed

No new dependencies were installed.

## Tests Run

- `python3 -m pytest tests/test_maf_orchestration.py -q`: passed, 3 tests.
- `python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-025-maf-openai-bridge`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-025-maf-openai-bridge --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-025-maf-openai-bridge --output-dir app/runs/phase-025-maf-openai-bridge`: passed.
- `bash scripts/validate.sh`: passed, 58 tests.

## Demo Evidence

See `docs/demos/phase-025-maf-openai-bridge-demo.md`.

Generated artifacts:

- `app/runs/phase-025-maf-openai-bridge/maf_adapter_smoke.json`
- `app/runs/phase-025-maf-openai-bridge/phase_regression_summary.json`
- `app/runs/phase-025-maf-openai-bridge/replication_audit.json`

## Acceptance Criteria Status

- MAF replay smoke reports `reasoning_provider=openai`: passed.
- MAF replay smoke reports three candidate questions: passed.
- Replication audit reports MAF OpenAI bridge evidence: passed.
- The deterministic-MAF known limit is removed from the current audit: passed.
- 20-turn regression passes: passed.
- Validation passes: passed.

## Risks

- Live OpenAI and live MAF model-call evidence still require credentials.
- Replay artifacts are integration evidence, not live quality evidence.

## Commit Status

Pending until local commit completes.
