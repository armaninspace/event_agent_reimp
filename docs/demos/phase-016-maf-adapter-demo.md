# Phase 016 Demo: Microsoft Agent Framework Adapter

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_maf_orchestration.py tests/test_agent_runtime.py -q
python3 scripts/run_maf_adapter_smoke.py --output-dir app/runs/phase-016-maf-adapter
python3 scripts/run_phase_regression.py --phase-id phase-016-maf-adapter --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Adapter tests pass.
- Adapter smoke writes JSON and Markdown artifacts.
- Adapter reports Microsoft Agent Framework package metadata.
- Adapter produces one deterministic workflow output.
- Adapter reports no model calls.
- 20-turn regression still passes.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest tests/test_maf_orchestration.py tests/test_agent_runtime.py -q
...                                                                      [100%]
```

```text
python3 scripts/run_maf_adapter_smoke.py --output-dir app/runs/phase-016-maf-adapter
wrote app/runs/phase-016-maf-adapter/maf_adapter_smoke.json
wrote app/runs/phase-016-maf-adapter/maf_adapter_smoke.md
framework=Microsoft Agent Framework
package=agent-framework 1.9.0
workflow=codex-thesis-replication-workflow
output_count=1
model_calls_performed=False
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-016-maf-adapter --turns 20
wrote app/runs/phase-016-maf-adapter/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

## Evidence

Generated MAF adapter artifacts:

```text
app/runs/phase-016-maf-adapter/maf_adapter_smoke.json
app/runs/phase-016-maf-adapter/maf_adapter_smoke.md
app/runs/phase-016-maf-adapter/phase_regression_summary.json
```

Adapter smoke summary:

```text
framework_name: Microsoft Agent Framework
package_name: agent-framework
package_version: 1.9.0
workflow_name: codex-thesis-replication-workflow
output_count: 1
model_calls_performed: False
output: MAF deterministic orchestration accepted: replicate governed thesis workflow
```

Regression summary:

```text
requested_turns: 20
completed_workflows: 20
stopped_early: False
workflow_task_statistical_misroutes: 0
selected_candidate_count: 20
selected_candidates_have_required_metadata: True
```

## 20-Turn Regression

Implemented and passed after adding the Microsoft Agent Framework adapter.

## Video

No video was generated. This is a non-UI runtime-adapter phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- No live model/provider calls are made.
- No cloud deployment is configured.
- The deterministic friends loop is not replaced by live MAF agents.

## Requirement Mapping

- Adapter: `app/maf_orchestration.py`
- Smoke command: `scripts/run_maf_adapter_smoke.py`
- Tests: `tests/test_maf_orchestration.py`
- Runtime metadata: `app/agent_runtime.py`
