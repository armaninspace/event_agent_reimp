# Phase 002: Reference Event Data

## Phase Goal

Move beyond static packet generation by adding reusable reference data services that load the final city-week and MSA-week event/economic files, validate their contracts, and write deterministic data-quality smoke artifacts.

## Requirements

- Implement reference data loaders for city-week and MSA-week final CSV files.
- Keep row grain explicit for every loaded dataset.
- Validate required fields, row counts, exposure coverage, week coverage, geography coverage, and missing required values.
- Emit explicit warnings for missing or weak data.
- Add reproducible fixture tests that build city-week reference records from fixture inputs.
- Add a smoke script that writes JSON and Markdown quality reports.
- Preserve Phase 001 packet behavior.

## Non-Goals

- Rebuild raw joins from source seed files.
- Implement matched statistical tests.
- Implement semantic SQL.
- Implement friends-loop orchestration.
- Run 20-turn regression before orchestration exists.

## Assumptions

- The workspace includes both final CSV files listed in `docs/data-card-final-runtime-files.md`.
- Final files are treated as runtime inputs for this phase.
- Python standard library CSV parsing is sufficient for contract and quality checks.

## Affected Layers

- Data access
- Data quality
- Smoke validation
- Tests
- Documentation

## Affected Modules

- `app/reference_data.py`
- `scripts/run_reference_data_smoke.py`
- `tests/test_reference_data.py`
- Phase 002 docs under `docs/`

## Dependency/Library Choices

No new dependencies are required. The implementation uses Python standard library modules: `csv`, `json`, `dataclasses`, `pathlib`, and `argparse`.

## Architecture Notes

`app.reference_data` is the new data contract boundary. It exposes small typed records and report objects that later phases can reuse for matching, semantic views, notebooks, and reports. It does not mutate source CSVs.

## Data/API/Config Changes

- Reads `data/reference/joined_city_week_game_economic.csv`.
- Reads `data/reference/joined_msa_week_game_economic.csv`.
- Writes smoke artifacts under `app/runs/phase-002-reference-event-data/`.

## Demo Requirements

- Run the smoke script against the real final CSVs.
- Record generated JSON and Markdown quality artifacts.
- Include representative warnings/counts in the demo doc.

## Test Requirements

- Unit tests cover fixture city-week loading and stable grain.
- Unit tests cover explicit warnings for missing/weak data.
- Unit tests cover full final-file quality report shape using temporary fixture files.
- `python3 -m pytest -q` passes.
- `bash scripts/validate.sh` passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not make network calls.
- Do not mutate source data.
- Generated reports include aggregate metadata only.

## Risks

- Final-file checks may be too permissive for later statistical phases.
- Standard-library CSV parsing is simple but less ergonomic than pandas for later modeling.
- 20-turn regression remains unavailable until orchestration exists.

## Acceptance Criteria

- Reference data loaders return records with stable grain and required fields.
- Quality reports include row, geography, week, exposure, missing-value, and warning information.
- Smoke script writes JSON and Markdown artifacts.
- Fixture tests pass.
- Validation passes.
- Phase 002 status documents the 20-turn deferral and next-phase trigger.

## Rollback Plan

Revert the Phase 002 commit or remove `app/reference_data.py`, `scripts/run_reference_data_smoke.py`, tests, smoke artifacts, and Phase 002 docs.
