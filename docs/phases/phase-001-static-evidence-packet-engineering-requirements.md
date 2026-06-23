# Phase 001: Static Evidence Packet

## Phase Goal

Create the first deterministic Python implementation slice for the event-agent research system: a command-line workflow that reads the final runtime CSVs and writes an auditable static evidence packet.

## Requirements

- Establish a Python package under `app/`.
- Declare Microsoft Agent Framework as the agent runtime dependency.
- Load and profile the final city-week and MSA-week CSV files.
- Generate a deterministic evidence packet containing question, hypothesis, design, data profile, result, caveat, runtime metadata, and audit log.
- Write JSON and Markdown artifacts to a run directory.
- Provide a CLI entry point runnable with `python3 -m app.main`.
- Add unit tests for CSV profiling, packet shape, artifact writing, and runtime metadata.
- Keep Phase 001 free of live model/API calls.

## Non-Goals

- Multi-agent orchestration.
- Live LLM calls.
- Statistical inference beyond deterministic descriptive summaries.
- Notebook generation.
- 20-turn regression, because candidate selection, routing, notebooks, telemetry, reports, and memory are not implemented yet.

## Assumptions

- The final runtime CSVs exist under `data/reference/`.
- Python 3.12 is available.
- Microsoft Agent Framework is installed as package `agent-framework` and imported as `agent_framework`.
- Phase 001 can use the Python standard library for CSV and JSON handling.

## Affected Layers

- Runtime setup
- Data access
- Evidence packet generation
- CLI
- Tests
- Phase audit documentation

## Affected Modules

- `pyproject.toml`
- `app/`
- `tests/`
- `docs/installed-software.md`
- Phase 001 docs under `docs/`

## Dependency/Library Choices

- `agent-framework`: Microsoft Agent Framework runtime dependency for later agent phases.
- `pytest`: test runner already available in the container.
- Python standard library: `csv`, `json`, `argparse`, `dataclasses`, `datetime`, `importlib.metadata`, and `pathlib`.

## Architecture Notes

The implementation keeps responsibilities separate:

- `app.data_profile` profiles runtime CSVs.
- `app.agent_runtime` reports Microsoft Agent Framework availability.
- `app.evidence_packet` assembles evidence packet data and writes artifacts.
- `app.main` exposes the CLI.

This keeps Phase 001 deterministic while leaving room for later Microsoft Agent Framework agents to call the same evidence packet services.

## Data/API/Config Changes

- Reads `data/reference/joined_city_week_game_economic.csv`.
- Reads `data/reference/joined_msa_week_game_economic.csv`.
- Writes run artifacts under a caller-provided output directory.
- Adds `.env.example` as a non-secret template for future model/API configuration.

## Demo Requirements

- Run the CLI against the final CSV files.
- Show the generated JSON and Markdown artifact paths.
- Include command-output evidence in the demo doc.

## Test Requirements

- Unit tests cover data profile aggregation.
- Unit tests cover packet structure and artifact creation.
- Unit tests cover Microsoft Agent Framework runtime metadata.
- `python3 -m pytest -q` passes.
- `bash scripts/e2e.sh` exits successfully or neutrally.
- `bash scripts/validate.sh` passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not make network calls.
- Do not push, merge, or publish.
- Generated packets must only include aggregate CSV metadata, not secrets.

## Risks

- The full `agent-framework` package installs many integration dependencies; future phases may prefer narrower `agent-framework-core` plus specific providers.
- Static descriptive summaries can be mistaken for statistical evidence unless caveats are explicit.
- The 20-turn regression is not available until orchestration exists.

## Acceptance Criteria

- `python3 -m app.main --output-dir <dir>` writes `experiment_packet.json` and `experiment_packet.md`.
- Packet includes question, hypothesis, design, result, caveat, data profile, runtime metadata, and audit log.
- Runtime metadata reports Microsoft Agent Framework package/import status.
- Unit tests pass.
- Validation passes.
- Demo and deliverables-status docs record evidence and the 20-turn non-applicability rationale.

## Rollback Plan

Revert the Phase 001 commit or remove `pyproject.toml`, `app/`, `tests/`, and Phase 001 docs.
