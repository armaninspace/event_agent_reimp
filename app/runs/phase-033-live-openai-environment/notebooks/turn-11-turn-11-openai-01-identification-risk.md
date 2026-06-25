# Turn 11: Do we observe a spending uptick in the week before home games (placebo lead), indicating potential confounding rather than true event impact?

Selected candidate: `turn-11-openai-01-identification-risk`

Rationale: Lead-week placebo tests on city/MSA weekly panels can reveal pre-trends that would undermine causal claims.

Caveat: Assumes accurate game calendars and stable weekly alignment without major unrelated shocks.

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
- `turn-11-openai-02-msa-week-coverage`
- `turn-11-openai-03-city-week-event-spending`

Notebook status: `lightweight_executed`.
