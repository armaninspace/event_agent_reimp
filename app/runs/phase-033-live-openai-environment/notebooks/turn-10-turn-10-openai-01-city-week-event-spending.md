# Turn 10: Which merchant categories experience the largest incremental card spending during home game weeks versus matched baseline weeks by city?

Selected candidate: `turn-10-openai-01-city-week-event-spending`

Rationale: Category-level lifts clarify who benefits and can be tested by aggregating weekly spend by city, merchant category, and event-week indicators against matched baseline weeks.

Caveat: Only measures spend in the card data sample and may miss cash-heavy venues.

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
