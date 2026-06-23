# Phase 002 Demo: Reference Event Data

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_reference_data_smoke.py --output-dir app/runs/phase-002-reference-event-data
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Smoke script loads both final runtime CSVs.
- Smoke script writes JSON and Markdown quality artifacts.
- Quality report records stable grains, required-field status, geography/week coverage, exposure rows, and warnings.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.........                                                                [100%]
```

```text
python3 scripts/run_reference_data_smoke.py --output-dir app/runs/phase-002-reference-event-data
wrote app/runs/phase-002-reference-event-data/reference_data_quality.json
wrote app/runs/phase-002-reference-event-data/reference_data_quality.md
city_week: rows=5777 geographies=53 weeks=109 has_game_rows=2277 warnings=0
msa_week: rows=48723 geographies=447 weeks=109 has_game_rows=2542 warnings=0
```

```text
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
9 passed in 0.10s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated files:

```text
app/runs/phase-002-reference-event-data/reference_data_quality.json
app/runs/phase-002-reference-event-data/reference_data_quality.md
```

Quality summary:

```text
schema_version: phase-002.reference-data-quality.v1
all_required_columns_present: True
all_required_values_present: True
warnings: []
city_week: rows=5777, geographies=53, weeks=109, has_game_rows=2277, total_game_count=7308
msa_week: rows=48723, geographies=447, weeks=109, has_game_rows=2542, total_game_count=8378
```

## 20-Turn Regression

Not applicable for Phase 002. This phase adds reference data loading and quality checks only. It still does not implement candidate selection, routing, notebooks, telemetry, reports, or memory. The 20-turn gate should be introduced before accepting the first phase that implements those orchestration surfaces.

## Video

No video was generated. This is a non-UI CLI/data-quality phase, and command-output evidence plus generated report artifacts are the relevant demo outputs.

## Known Gaps

- No raw join rebuild is implemented; final CSVs are used as runtime inputs.
- No statistical matching is implemented yet.
- No semantic SQL layer is implemented yet.
- No e2e suite or 20-turn regression exists yet.

## Requirement Mapping

- Reference data loader: `app/reference_data.py`
- Data quality checks: `app/reference_data.py`
- Reproducible fixture tests: `tests/test_reference_data.py`
- Smoke command: `scripts/run_reference_data_smoke.py`
- Smoke artifacts: `app/runs/phase-002-reference-event-data/`
