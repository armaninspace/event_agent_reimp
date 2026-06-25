# Turn 16: Do game weeks deliver a net spending gain when you compare week 0 to the combined weeks -1 and +1 in the same city?

Selected candidate: `turn-16-openai-01-city-week-event-spending`

Rationale: This tests whether observed event-week bumps reflect true incremental demand rather than timing shifts across adjacent weeks using the city-week spending series.

Caveat: Weekly aggregation may mask category-level substitution and visitor vs. resident effects.

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
- `turn-16-openai-02-msa-week-coverage`
- `turn-16-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
