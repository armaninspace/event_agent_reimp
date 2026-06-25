# Turn 14: In weeks when a city hosts a home game, do matched peer MSAs without any events show no comparable spending increase, supporting a causal home-game effect?

Selected candidate: `turn-14-openai-01-identification-risk`

Rationale: Cross-MSA placebo comparisons by week help rule out national shocks and seasonality using only the local event calendar and weekly spending series.

Caveat: Requires a clean set of peer MSAs with verified no-event weeks and good seasonal matching.

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
- `turn-14-openai-03-city-week-event-spending`
- `turn-14-openai-02-msa-week-coverage`

Notebook status: `lightweight_executed`.
