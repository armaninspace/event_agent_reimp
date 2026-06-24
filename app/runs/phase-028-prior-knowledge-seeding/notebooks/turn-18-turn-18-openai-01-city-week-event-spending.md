# Turn 18: Which city game weeks show the largest spending lift after accounting for baseline weeks?

Selected candidate: `turn-18-openai-01-city-week-event-spending`

Rationale: This tests the headline spending question against the city-week table.

Caveat: The result remains observational without matched controls.

## Statistical Evidence

Result count: `4`

Minimum adjusted p-value: `2.4226335941393745e-68`

Adjusted-significance flag: `True`

Result IDs:
- `exploratory:city_week:revenue_all`
- `exploratory:city_week:merchants_all`
- `matched:city_week:revenue_all`
- `matched:city_week:merchants_all`

Statistical caveats:
- Statistical evidence is observational; causal-design diagnostics do not prove causality.
- Adjusted p-values do not establish causality.

Rejected candidates:
- `turn-18-openai-02-msa-week-coverage`
- `turn-18-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
