# Phase 011: Semantic SQL Layer

## Phase Goal

Add a governed local DuckDB semantic layer over final city-week and MSA-week CSV files with SELECT-only enforcement, whitelisted views, row limits, and query telemetry.

## Requirements

- Use DuckDB for local analytical SQL.
- Expose whitelisted views:
  - `city_week_events`
  - `msa_week_events`
- Enforce SELECT-only queries.
- Reject access to non-whitelisted relations.
- Apply row limits.
- Record query telemetry with SQL, referenced views, row count, columns, and row preview.
- Add a smoke script that writes JSON/Markdown semantic query artifacts.
- Add tests for allowed SELECT, non-SELECT rejection, non-whitelisted table rejection, and row limits.

## Non-Goals

- Persistent semantic database.
- Mutation queries.
- Agent-driven SQL generation.
- Complex metric DSL.

## Assumptions

- Final CSV files are small enough to query directly with DuckDB CSV views.
- Regex-based relation extraction is sufficient for the current narrow query surface.
- Later phases can add richer metric definitions.

## Affected Layers

- Semantic/data access layer
- Query telemetry
- Tests
- Documentation

## Affected Modules

- `app/semantic_layer.py`
- `scripts/run_semantic_smoke.py`
- `tests/test_semantic_layer.py`
- Phase 011 docs under `docs/`

## Dependency/Library Choices

- `duckdb`: local analytical SQL over CSV files.

## Architecture Notes

The semantic layer opens an in-memory DuckDB connection, creates views backed by CSV files, validates SQL before execution, applies row limits, and returns telemetry alongside rows.

## Data/API/Config Changes

- Reads final CSVs under `data/reference/`.
- Writes semantic smoke artifacts under `app/runs/phase-011-semantic-layer/`.

## Demo Requirements

- Run semantic smoke command.
- Run 20-turn regression.
- Record validation output.

## Test Requirements

- Tests cover allowed SELECT.
- Tests cover non-SELECT rejection.
- Tests cover non-whitelisted relation rejection.
- Tests cover row limit enforcement.
- Validation passes.

## Security/Sandbox Considerations

- SELECT-only.
- Whitelisted views only.
- No source CSV mutation.
- Query preview limited.

## Risks

- SQL parsing is intentionally conservative and not a full parser.
- Later agent-generated SQL may need stricter parsing or DuckDB prepared validation.

## Acceptance Criteria

- Semantic smoke artifacts are written.
- Guardrail tests pass.
- 20-turn regression still passes.
- Validation passes.

## Rollback Plan

Revert the Phase 011 commit or remove semantic layer files, artifacts, tests, dependency pin, and docs.
