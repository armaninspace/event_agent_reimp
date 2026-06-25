# Turn 13: How much does local card spending change in the host city during playoff game weeks versus regular-season game weeks, after adjusting for typical seasonal baselines?

Selected candidate: `turn-13-openai-01-city-week-event-spending`

Rationale: This isolates intensity effects by comparing tagged playoff vs regular-season event weeks within cities using weekly spending data and matched non-event baselines, directly informing planning for higher-stakes events.

Caveat: Differences could reflect concurrent tourism or media shocks unrelated to the games.

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
- `turn-13-openai-02-identification-risk`
- `turn-13-openai-03-msa-week-coverage`

Notebook status: `lightweight_executed`.
