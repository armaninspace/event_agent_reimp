# Turn 20: Do post-game weeks in a city show a spending dip that offsets part of the home game-week gain, suggesting intertemporal substitution?

Selected candidate: `turn-20-openai-01-city-week-event-spending`

Rationale: Using weekly city event flags and baseline non-game weeks, we can estimate the game-week lift and then test for a compensating dip in the immediately following week within the same city.

Caveat: One sentence limitation.

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
- `turn-20-openai-02-msa-week-coverage`
- `turn-20-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
