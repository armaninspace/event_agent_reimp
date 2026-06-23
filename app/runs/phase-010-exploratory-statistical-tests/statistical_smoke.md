# Exploratory Statistical Smoke Report

Schema: phase-010.exploratory-statistical-tests.v1

## city_week / revenue_all

- Grain: city-week
- Status: ok
- Exposed rows: 2277
- Unexposed rows: 3500
- Exposed mean: -0.07603730917874396
- Unexposed mean: -0.10482782914285714
- Mean difference: 0.02879051996411318
- Caveats:
  - Exploratory observational association only; this is not causal proof.
  - No matched controls, p-values, or multiple-testing correction are applied in this phase.

## city_week / merchants_all

- Grain: city-week
- Status: ok
- Exposed rows: 2277
- Unexposed rows: 3500
- Exposed mean: -0.033629446288976725
- Unexposed mean: -0.0856475260857143
- Mean difference: 0.052018079796737574
- Caveats:
  - Exploratory observational association only; this is not causal proof.
  - No matched controls, p-values, or multiple-testing correction are applied in this phase.

## msa_week / revenue_all

- Grain: MSA-week
- Status: ok
- Exposed rows: 2542
- Unexposed rows: 46181
- Exposed mean: -0.048311449252557044
- Unexposed mean: -0.0035198904094757583
- Mean difference: -0.04479155884308129
- Caveats:
  - Exploratory observational association only; this is not causal proof.
  - No matched controls, p-values, or multiple-testing correction are applied in this phase.

## msa_week / merchants_all

- Grain: MSA-week
- Status: ok
- Exposed rows: 2542
- Unexposed rows: 46181
- Exposed mean: -0.026064516129032256
- Unexposed mean: -0.05141940347762066
- Mean difference: 0.025354887348588404
- Caveats:
  - Exploratory observational association only; this is not causal proof.
  - No matched controls, p-values, or multiple-testing correction are applied in this phase.
