# Turn 10: Which matched-control checks change the city game-week spending lift estimate after the baseline result?

Selected candidate: `turn-10-openai-01-city-week-event-spending`

Rationale: This tests the headline spending question against the city-week table. Prior notebook knowledge already covered the original seed, so this follow-up asks for stronger validation.

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
- `turn-10-openai-02-msa-week-coverage`
- `turn-10-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
