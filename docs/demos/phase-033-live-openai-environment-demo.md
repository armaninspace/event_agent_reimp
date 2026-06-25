# Phase 033 Demo: Live OpenAI Environment

## Commands

```sh
set -a; source .env; set +a
python3 scripts/run_openai_reasoning_smoke.py --mode live --turns 1 --output-dir app/runs/phase-033-live-openai-environment/live-smoke
python3 scripts/run_phase_regression.py --phase-id phase-033-live-openai-environment --turns 20 --reasoning-mode openai --openai-model ${OPENAI_MODEL:-gpt-5} --prior-notebook-knowledge-path app/runs/phase-027-notebook-knowledge-base/notebooks/notebook-knowledge.json
python3 scripts/run_maf_adapter_smoke.py --reasoning-mode openai --openai-model ${OPENAI_MODEL:-gpt-5} --output-dir app/runs/phase-033-live-openai-environment
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-033-live-openai-environment --output-dir app/runs/phase-033-live-openai-environment
bash scripts/validate.sh
```

## Observed Behavior

Live OpenAI smoke:

```text
mode=live
provider=openai
model_calls_performed=True
selected_candidate_count=1
```

20-turn live regression:

```text
completed_workflows=20
reasoning_provider=openai
reasoning_mode=openai
openai_model_calls_performed=True
selected_semantic_slot_counts={'city_week_event_spending': 7, 'identification_risk': 7, 'msa_week_coverage': 6}
selected_unique_semantic_slot_count=3
```

Live MAF smoke:

```text
framework=Microsoft Agent Framework
reasoning_provider=openai
reasoning_mode=openai
model_calls_performed=True
```

Audit:

```text
final_status=replicated_with_known_limits
openai_model_calls_performed=True
reasoning_mode=openai
maf_reasoning_mode=openai
```

## Evidence

Generated artifacts:

```text
app/runs/phase-033-live-openai-environment/live-smoke/openai_reasoning_smoke.json
app/runs/phase-033-live-openai-environment/phase_regression_summary.json
app/runs/phase-033-live-openai-environment/maf_adapter_smoke.json
app/runs/phase-033-live-openai-environment/replication_audit.json
```

## Known Limits

- Statistical evidence remains controlled observational, not causal proof.
