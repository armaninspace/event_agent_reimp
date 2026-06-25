# Turn 4: How much higher is citywide consumer spending during home-game weeks compared with the same city's away-game weeks in the same season?

Selected candidate: `turn-04-openai-01-city-week-event-spending`

Rationale: Away weeks provide a same-team, same-season counterfactual without local crowds, enabling a within-city comparison using weekly event and spending data.

Caveat: Assumes away weeks are not themselves local draws and that within-season schedules provide comparable baselines.

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
- `turn-04-openai-02-msa-week-coverage`
- `turn-04-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
