# Phase 024: OpenAI Reasoning

## Phase Goal

Replace make-believe hypothesis generation with a real OpenAI-backed reasoning path for candidate research questions, while preserving deterministic and replay modes only for CI and reproducible audit evidence.

## Requirements

- Add an OpenAI Responses API integration for hypothesis generation.
- Require `OPENAI_API_KEY` for live OpenAI reasoning.
- Fail clearly when live mode is requested without credentials.
- Persist OpenAI prompt/output provenance and parsed candidates.
- Carry provider, model, mode, prompt hash, output hash, and model-call status on selected candidates.
- Add an explicit replay mode for tests and repeatable phase runs.
- Thread OpenAI/replay reasoning through friends-loop and phase-regression CLI paths.
- Add audit coverage for OpenAI reasoning metadata.
- Keep deterministic mode available for legacy regression.

## Non-Goals

- Pretending replay is a live model call.
- Reading local `.env` files.
- Replacing Microsoft Agent Framework orchestration in this phase.
- Claiming causal proof from observational spending data.

## Assumptions

- The official OpenAI Python SDK is the right integration point.
- The Responses API is the forward path for new OpenAI text generation.
- Live execution depends on a caller-provided `OPENAI_API_KEY` in the process environment.

## Affected Layers

- Hypothesis generation
- Friends-loop orchestration
- Phase regression
- Final audit
- Operator CLI
- Tests and documentation

## Affected Modules

- `app/openai_reasoning.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_openai_reasoning_smoke.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_openai_reasoning.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

- Added `openai>=2.43.0,<3.0.0` to `pyproject.toml`.
- Used `client.responses.create(model=..., input=...)` from the official OpenAI Python SDK.

## Data/API/Config Changes

- New runtime modes: `deterministic`, `openai`, and `replay`.
- New replay fixture: `data/reference/openai_hypothesis_replay.json`.
- New selected candidate `reasoning` metadata.
- New phase summary fields for reasoning provider/mode and model-call status.
- New replication audit fields for OpenAI reasoning coverage.

## Demo Requirements

- Run focused OpenAI/friends/phase tests.
- Run OpenAI replay smoke.
- Verify live smoke fails without `OPENAI_API_KEY`.
- Run a 20-turn OpenAI replay phase regression.
- Run replication audit against Phase 024.
- Run full validation.

## Test Requirements

- Parse valid OpenAI JSON candidate output.
- Verify live generator calls an injected client and writes traces.
- Verify live SDK path requires `OPENAI_API_KEY`.
- Verify friends-loop replay marks OpenAI provenance without live calls.
- Verify final audit counts OpenAI reasoning metadata.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not log API keys.
- Store prompt/output hashes and raw model output only in local run artifacts.
- Keep replay and live model-call status explicit.

## Risks

- Live mode cannot be validated in shells without `OPENAI_API_KEY`.
- Replay validates wiring and provenance, not current model quality.
- OpenAI-generated questions still need downstream statistical and caveat discipline.

## Acceptance Criteria

- OpenAI-backed live path exists and requires credentials.
- Replay smoke passes and is visibly marked as replay.
- 20-turn phase regression passes with OpenAI replay provenance.
- Replication audit reports 20 OpenAI reasoning metadata records.
- Full validation passes.

## Rollback Plan

Revert the Phase 024 commit or remove OpenAI reasoning mode, replay fixture, CLI flags, audit fields, tests, artifacts, and docs.
