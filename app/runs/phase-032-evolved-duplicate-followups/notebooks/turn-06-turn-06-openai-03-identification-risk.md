# Turn 6: Where do game weeks overlap with likely confounders in the weekly spending data?

Selected candidate: `turn-06-openai-03-identification-risk`

Rationale: A skeptical pass identifies markets where timing may bias conclusions.

Caveat: Confounding review needs external calendars for full resolution.

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
- `turn-06-openai-01-city-week-event-spending`
- `turn-06-openai-02-msa-week-coverage`

Notebook status: `lightweight_executed`.
