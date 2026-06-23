# Phase 016: Microsoft Agent Framework Adapter

## Phase Goal

Add an explicit Microsoft Agent Framework orchestration adapter that can run locally and deterministically without external model credentials, while preserving the 20-turn regression workflow.

## Requirements

- Build a real Microsoft Agent Framework workflow object.
- Use deterministic function execution rather than live model calls.
- Write JSON and Markdown adapter smoke artifacts.
- Report package name, package version, workflow name, executor ID, outputs, and model-call status.
- Add tests proving the adapter runs and writes artifacts.
- Keep 20-turn regression passing after the adapter is added.

## Non-Goals

- Live LLM calls.
- Provider credentials.
- Cloud deployment.
- Replacing the deterministic friends-loop implementation.

## Assumptions

- The installed package is `agent-framework 1.9.0`.
- A `WorkflowBuilder` plus `FunctionExecutor` path is sufficient to prove local framework orchestration.
- Deterministic regression should remain the default until external provider credentials and policies are deliberately introduced.

## Affected Layers

- Agent runtime adapter
- Smoke artifacts
- Tests
- Documentation

## Affected Modules

- `app/maf_orchestration.py`
- `scripts/run_maf_adapter_smoke.py`
- `tests/test_maf_orchestration.py`

## Dependency/Library Choices

- Reuses existing `agent-framework>=1.9.0,<2.0.0`.
- No new dependency is required.

## Architecture Notes

The adapter uses `FunctionExecutor` and `WorkflowBuilder` from Microsoft Agent Framework. The executor writes workflow output through `WorkflowContext.yield_output`, matching the framework's documented workflow output pattern. This proves framework wiring without creating provider-specific chat clients or making network calls.

## Data/API/Config Changes

- Adds adapter smoke artifacts under `app/runs/phase-016-maf-adapter/`.
- No source data mutation.
- No environment variables required.

## Demo Requirements

- Run adapter smoke.
- Run adapter tests.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Adapter reports Microsoft Agent Framework metadata.
- Adapter produces one deterministic output.
- Adapter reports `model_calls_performed=False`.
- Adapter smoke artifacts are written.
- Validation passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not make external model calls.
- Do not require provider credentials.

## Risks

- The adapter proves local workflow orchestration, not production cloud deployment.
- Future live-agent phases will need provider-specific safety, secrets, cost, and observability controls.

## Acceptance Criteria

- MAF adapter smoke artifacts are written.
- Adapter uses the installed Microsoft Agent Framework package.
- Adapter runs without model calls.
- Tests and validation pass.
- 20-turn regression still passes.

## Rollback Plan

Revert the Phase 016 commit or remove the adapter module, smoke script, tests, artifacts, and docs.
