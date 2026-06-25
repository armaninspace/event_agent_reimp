# Turn 6: Do treated city-weeks show flat spending trends in the 4–8 weeks before events compared with matched non-event weeks in the same city?

Selected candidate: `turn-06-openai-01-identification-risk`

Rationale: A pre-trend check bounds causal claims by verifying parallel trends; the weekly city/MSA panel with event flags allows lead indicators and matched-within-city comparisons.

Caveat: Relies on stable weekly baselines and no anticipatory shocks.

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
- `turn-06-openai-03-city-week-event-spending`
- `turn-06-openai-02-msa-week-coverage`

Notebook status: `lightweight_executed`.
