# Turn 17: Do placebo weeks immediately before or after home-game weeks show comparable spending bumps, suggesting time-varying confounders rather than true event effects?

Selected candidate: `turn-17-openai-01-identification-risk`

Rationale: Using city-level weekly event flags, we can compare spending in t-1 and t+1 to the event week t to detect anticipation or persistence patterns that indicate identification risk.

Caveat: Requires clear labeling of event and non-event weeks and consistent spending aggregation granularity.

## Statistical Evidence

Result count: `4`

Minimum adjusted p-value: `8.018939027100663e-08`

Adjusted-significance flag: `True`

Result IDs:
- `matched:city_week:revenue_all`
- `matched:city_week:merchants_all`
- `matched:msa_week:revenue_all`
- `matched:msa_week:merchants_all`

Statistical caveats:
- Statistical evidence is observational; causal-design diagnostics do not prove causality.
- Adjusted p-values do not establish causality.

Rejected candidates:
- `turn-17-openai-02-msa-week-coverage`
- `turn-17-openai-03-city-week-event-spending`

Notebook status: `lightweight_executed`.
