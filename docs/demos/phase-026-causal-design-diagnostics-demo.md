# Phase 026 Demo: Causal Design Diagnostics

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_causal_diagnostics.py tests/test_statistical_execution.py tests/test_phase_regression.py tests/test_replication_audit.py tests/test_reporting.py -q
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json --output-dir app/runs/phase-026-causal-design-diagnostics
python3 scripts/run_phase_regression.py --phase-id phase-026-causal-design-diagnostics --turns 20 --reasoning-mode replay --openai-model gpt-5 --openai-replay-path data/reference/openai_hypothesis_replay.json
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-026-causal-design-diagnostics --output-dir app/runs/phase-026-causal-design-diagnostics
bash scripts/validate.sh
```

## Expected Behavior

- Focused tests pass after Phase 026 artifacts are generated.
- Regression reports causal-design diagnostics for every turn.
- Audit reports 20 causal-design turns.
- Business report includes causal-design diagnostic sections.
- Validation passes.

## Observed Behavior

20-turn regression passed:

```text
turns_have_statistical_evidence=True
turns_have_causal_design_diagnostics=True
reasoning_provider=openai
reasoning_mode=replay
executed_notebook_count=20
failed_notebook_count=0
```

Audit passed:

```text
causal_design_turn_count=20
controlled_observational_turn_count=20
maf_reasoning_provider=openai
maf_reasoning_mode=replay
```

## Evidence

Generated artifacts:

```text
app/runs/phase-026-causal-design-diagnostics/phase_regression_summary.json
app/runs/phase-026-causal-design-diagnostics/replication_audit.json
app/runs/phase-026-causal-design-diagnostics/friends-question-loop/business_evidence_report.html
```

## Video

No video was generated. This is a non-UI statistical diagnostics phase; command-output evidence and generated report artifacts are the relevant demo evidence.

## Known Gaps

- Controlled observational diagnostics still do not prove causality.
- Live OpenAI evidence remains blocked by missing `OPENAI_API_KEY` in this shell.

## Requirement Mapping

- Causal diagnostics: `app/causal_diagnostics.py`
- Statistical attachment: `app/statistical_execution.py`
- Report rendering: `app/reporting.py`
- Regression/audit checks: `app/phase_regression.py`, `app/replication_audit.py`
- Tests: `tests/test_causal_diagnostics.py`, `tests/test_statistical_execution.py`, `tests/test_replication_audit.py`
