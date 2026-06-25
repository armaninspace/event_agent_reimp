# Turn 8: Do spending levels already trend upward in the one to two weeks before game weeks within the same city, suggesting residual confounding?

Selected candidate: `turn-08-openai-01-identification-risk`

Rationale: A placebo-style lead test on the city-week panel using event flags and dates can reveal whether game timing aligns with pre-existing spending upswings.

Caveat: Requires sufficient pre-event, non-overlapping weeks per city to estimate clean pre-trends.

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
- `turn-08-openai-02-msa-week-coverage`
- `turn-08-openai-03-city-week-event-spending`

Notebook status: `lightweight_executed`.
