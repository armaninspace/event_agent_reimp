# Phase 025 Backlog: MAF OpenAI Bridge

## Completed

- Add provider-backed MAF workflow branch.
- Add MAF report fields for reasoning provider, mode, model, candidates, traces, and model-call status.
- Add MAF smoke CLI flags for reasoning mode, OpenAI model, and replay path.
- Add MAF replay test proving OpenAI reasoning is invoked inside a workflow executor.
- Run MAF replay smoke and write artifacts.
- Run 20-turn OpenAI replay phase regression.
- Update replication audit for MAF OpenAI bridge evidence.
- Run audit against Phase 025 artifacts.

## Remaining

- Run live MAF OpenAI smoke when `OPENAI_API_KEY` is available.
- Consider replacing deterministic tournament/reflection with provider-backed MAF executors while preserving replay.
- Consider adding structured-output enforcement for live model output.
