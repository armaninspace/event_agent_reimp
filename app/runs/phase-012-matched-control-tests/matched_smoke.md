# Matched Control Smoke Report

Schema: phase-012.matched-control-tests.v1

## city_week / revenue_all

- Grain: city-week
- Status: ok
- Matched exposed rows: 1996
- Unmatched exposed rows: 256
- Control rows used: 9705
- Mean matched difference: -0.03175996843993237
- Caveats:
  - Exploratory observational matched comparison only; not causal proof.
  - Matching uses same week and same block only; residual confounding may remain.

## city_week / merchants_all

- Grain: city-week
- Status: ok
- Matched exposed rows: 1996
- Unmatched exposed rows: 256
- Control rows used: 9705
- Mean matched difference: -0.012455992684044412
- Caveats:
  - Exploratory observational matched comparison only; not causal proof.
  - Matching uses same week and same block only; residual confounding may remain.

## msa_week / revenue_all

- Grain: MSA-week
- Status: ok
- Matched exposed rows: 2542
- Unmatched exposed rows: 0
- Control rows used: 17018
- Mean matched difference: 0.012500577246086825
- Caveats:
  - Exploratory observational matched comparison only; not causal proof.
  - Matching uses same week and same block only; residual confounding may remain.

## msa_week / merchants_all

- Grain: MSA-week
- Status: ok
- Matched exposed rows: 2542
- Unmatched exposed rows: 0
- Control rows used: 17018
- Mean matched difference: 0.0026108761347287345
- Caveats:
  - Exploratory observational matched comparison only; not causal proof.
  - Matching uses same week and same block only; residual confounding may remain.
