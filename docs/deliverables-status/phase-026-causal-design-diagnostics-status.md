# Phase 026 Deliverables Status: Causal Design Diagnostics

## Completed Items

- Added causal-design diagnostics over matched-control results.
- Added candidate-scoped causal-design summaries to statistical evidence.
- Rendered causal-design diagnostics in the business report.
- Added phase regression coverage for causal-design diagnostics.
- Added replication audit counts for causal-design and controlled-observational turns.
- Added focused tests.
- Ran MAF replay smoke.
- Ran a 20-turn OpenAI replay phase regression.
- Refreshed replication audit against Phase 026.

## Blocked/Deferred Items

- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY`.
- External-calendar causal controls remain deferred until source data exists.

## Files Changed

- `app/causal_diagnostics.py`
- `app/statistical_execution.py`
- `app/reporting.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_causal_diagnostics.py`
- `tests/test_statistical_execution.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-026-causal-design-diagnostics/`
- `docs/phases/phase-026-causal-design-diagnostics-engineering-requirements.md`
- `docs/backlog/phase-026-causal-design-diagnostics-backlog.md`
- `docs/demos/phase-026-causal-design-diagnostics-demo.md`
- `docs/deliverables-status/phase-026-causal-design-diagnostics-status.md`

## Dependencies Installed

No new dependencies were installed.

## Tests Run

- `python3 -m pytest tests/test_causal_diagnostics.py tests/test_statistical_execution.py tests/test_phase_regression.py tests/test_replication_audit.py tests/test_reporting.py -q`: passed, 9 tests.
- `python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-026-causal-design-diagnostics`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-026-causal-design-diagnostics --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-026-causal-design-diagnostics --output-dir app/runs/phase-026-causal-design-diagnostics`: passed.
- `bash scripts/validate.sh`: passed, 59 tests.

## Demo Evidence

See `docs/demos/phase-026-causal-design-diagnostics-demo.md`.

Generated artifacts:

- `app/runs/phase-026-causal-design-diagnostics/phase_regression_summary.json`
- `app/runs/phase-026-causal-design-diagnostics/replication_audit.json`
- `app/runs/phase-026-causal-design-diagnostics/friends-question-loop/business_evidence_report.html`

## Acceptance Criteria Status

- 20-turn regression reports `turns_have_causal_design_diagnostics=True`: passed.
- Audit reports `causal_design_turn_count=20`: passed.
- Audit reports `controlled_observational_turn_count=20`: passed.
- Business report renders causal-design diagnostics: passed.
- Full validation passes: passed.

## Risks

- Controlled observational diagnostics can still be overread as causal proof.
- Stronger causal identification requires external controls not present in the current files.

## Commit Status

Pending until local commit completes.
