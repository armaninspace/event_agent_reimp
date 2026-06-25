# Turn 2: Does weekly local consumer spending scale with the number of home games in a city (e.g., single vs multi-game weeks), relative to matched baseline weeks?

Selected candidate: `turn-02-openai-01-city-week-event-spending`

Rationale: Testing a dose–response between game-week intensity and spending uses the city–week event counts and spend measures to link crowd exposure to observed lifts.

Caveat: Requires consistent week-level exposure counts and controls for seasonality and holidays.

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
- `turn-02-openai-02-city-week-event-spending`
- `turn-02-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
