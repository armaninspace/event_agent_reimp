# Phase 024 Backlog: OpenAI Reasoning

## Completed

- Add OpenAI Responses API client wrapper.
- Add prompt construction for public hypothesis generation.
- Add strict JSON parser and candidate validation.
- Add trace persistence with prompt and output hashes.
- Add live mode credential gate.
- Add replay mode for reproducible tests and phase runs.
- Carry OpenAI reasoning metadata on candidates.
- Thread reasoning mode through phase regression.
- Add OpenAI reasoning smoke CLI.
- Add audit fields for OpenAI reasoning coverage.
- Add focused tests.
- Run 20-turn OpenAI replay regression.

## Remaining

- Run live OpenAI smoke in an environment with `OPENAI_API_KEY`.
- Optionally add structured output schema support if the SDK/API surface is adopted project-wide.
- Optionally use OpenAI for question evolution rewrites, not only candidate proposal.
- Optionally connect OpenAI-backed agents directly into the Microsoft Agent Framework adapter.
