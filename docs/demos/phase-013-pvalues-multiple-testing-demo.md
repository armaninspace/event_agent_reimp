# Phase 013 Demo: P-Values And Multiple Testing

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest -q
python3 scripts/run_correction_smoke.py --output-dir app/runs/phase-013-pvalues-multiple-testing
python3 scripts/run_phase_regression.py --phase-id phase-013-pvalues-multiple-testing --turns 20
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Tests pass.
- Correction smoke writes JSON and Markdown artifacts.
- Eight exploratory/matched statistical results include raw and adjusted p-values.
- Caveats remain attached to prevent causal overclaiming.
- 20-turn regression still passes.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.........................................                                [100%]
```

```text
python3 scripts/run_correction_smoke.py --output-dir app/runs/phase-013-pvalues-multiple-testing
wrote app/runs/phase-013-pvalues-multiple-testing/correction_smoke.json
wrote app/runs/phase-013-pvalues-multiple-testing/correction_smoke.md
result_count=8
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-013-pvalues-multiple-testing --turns 20
wrote app/runs/phase-013-pvalues-multiple-testing/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

```text
bash scripts/validate.sh
41 passed
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated correction artifacts:

```text
app/runs/phase-013-pvalues-multiple-testing/correction_smoke.json
app/runs/phase-013-pvalues-multiple-testing/correction_smoke.md
app/runs/phase-013-pvalues-multiple-testing/phase_regression_summary.json
```

Correction smoke summary:

```text
schema_version: phase-013.pvalues-multiple-testing.v1
method: Benjamini-Hochberg FDR correction
result_count: 8
exploratory:city_week:revenue_all p=2.95018e-05 adjusted=3.93357e-05 status=ok
exploratory:city_week:merchants_all p=3.02829e-69 adjusted=2.42263e-68 status=ok
exploratory:msa_week:revenue_all p=4.34246e-29 adjusted=1.15799e-28 status=ok
exploratory:msa_week:merchants_all p=1.56603e-48 adjusted=6.26411e-48 status=ok
matched:city_week:revenue_all p=4.00947e-08 adjusted=8.01894e-08 status=ok
matched:city_week:merchants_all p=3.50373e-07 adjusted=5.60597e-07 status=ok
matched:msa_week:revenue_all p=0.00028791 adjusted=0.00032904 status=ok
matched:msa_week:merchants_all p=0.0681001 adjusted=0.0681001 status=ok
```

## 20-Turn Regression

Implemented and passed after adding p-values and multiple-testing correction.

## Video

No video was generated. This is a non-UI statistical correction phase; command-output evidence and generated JSON/Markdown artifacts are the relevant demo outputs.

## Known Gaps

- P-values remain exploratory metadata.
- Benjamini-Hochberg correction does not remove observational confounding.
- Statistical execution is not yet selected directly from forum-governed research questions.

## Requirement Mapping

- Correction service: `app/multiple_testing.py`
- Smoke command: `scripts/run_correction_smoke.py`
- Tests: `tests/test_multiple_testing.py`
