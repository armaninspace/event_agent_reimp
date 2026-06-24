# Phase 025: MAF OpenAI Bridge

## Phase Goal

Replace the deterministic-only Microsoft Agent Framework limitation with a real MAF workflow path that invokes the same OpenAI-backed hypothesis generator used by the friends loop.

## Requirements

- Keep deterministic MAF workflow support for local smoke tests.
- Add a MAF workflow executor that calls OpenAI hypothesis generation in `openai` or `replay` mode.
- Persist MAF smoke artifacts showing provider, reasoning mode, candidate count, and model-call status.
- Add CLI flags for MAF reasoning mode, OpenAI model, and replay path.
- Update replication audit to verify MAF OpenAI bridge evidence.
- Remove the stale deterministic-MAF known limit when provider-backed MAF evidence exists.
- Keep 20-turn phase regression passing.

## Non-Goals

- Claiming replay is a live model call.
- Reading `.env`.
- Cloud deployment of Microsoft Agent Framework.
- Replacing all deterministic governance modules.

## Assumptions

- `agent-framework 1.9.0` remains the runtime package.
- FunctionExecutor is the correct local MAF integration point for invoking project-owned Python services.
- Replay mode is acceptable for committed artifacts when `OPENAI_API_KEY` is unavailable.

## Affected Layers

- Microsoft Agent Framework adapter
- OpenAI hypothesis generation
- Operator smoke scripts
- Final replication audit
- Tests and documentation

## Affected Modules

- `app/maf_orchestration.py`
- `scripts/run_maf_adapter_smoke.py`
- `app/replication_audit.py`
- `scripts/run_replication_audit.py`
- `tests/test_maf_orchestration.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

- Reuses existing `agent-framework>=1.9.0,<2.0.0`.
- Reuses existing `openai>=2.43.0,<3.0.0`.
- No new package install is required.

## Architecture Notes

The MAF workflow now has two execution modes. Deterministic mode keeps the original local workflow. OpenAI/replay modes build a `FunctionExecutor` whose body loads the QuestionForum records, invokes `OpenAIHypothesisGenerator`, and yields a JSON summary back through the MAF workflow output channel.

## Data/API/Config Changes

- `run_maf_adapter_sync` accepts `reasoning_mode`, `openai_model`, `openai_replay_path`, and `openai_trace_dir`.
- `MAFAdapterReport` now includes reasoning provider, mode, model, candidate count, candidate questions, trace paths, and model-call status.
- Replication audit now includes MAF bridge fields.

## Demo Requirements

- Run focused MAF tests.
- Run MAF replay smoke.
- Run 20-turn replay phase regression.
- Run replication audit against Phase 025.
- Run full validation.

## Test Requirements

- Deterministic MAF test still passes.
- Replay MAF test proves the workflow invokes OpenAI reasoning and writes a trace.
- Audit test proves Phase 025 has MAF OpenAI bridge evidence.
- Full validation passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not log API keys.
- Live `openai` mode remains credential-gated by the OpenAI reasoning layer.
- Replay artifacts must be labeled as replay with `model_calls_performed=False`.

## Risks

- Replay validates MAF/OpenAI wiring, not live model quality.
- A live MAF model-call run still requires `OPENAI_API_KEY`.
- MAF cloud deployment behavior is outside this local adapter.

## Acceptance Criteria

- MAF replay smoke reports `reasoning_provider=openai`.
- MAF replay smoke reports three candidate questions.
- Replication audit reports MAF OpenAI bridge evidence.
- The deterministic-MAF known limit is removed from the current audit.
- 20-turn regression passes.
- Validation passes.

## Rollback Plan

Revert the Phase 025 commit or remove the MAF OpenAI workflow branch, CLI flags, audit fields, tests, artifacts, and docs.
