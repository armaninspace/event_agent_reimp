# Turn 7: Within each city, does weekly consumer spending rise more in weeks with multiple home games versus single-game weeks after controlling for baseline trends?

Selected candidate: `turn-07-openai-01-city-week-event-spending`

Rationale: The event schedule allows counting home games per city-week, enabling a nonlinearity test of crowd intensity on spending using baseline-adjusted comparisons.

Caveat: Assumes the count of home games per week is measured accurately and not driven by unobserved promotions.

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
- `turn-07-openai-02-msa-week-coverage`
- `turn-07-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
