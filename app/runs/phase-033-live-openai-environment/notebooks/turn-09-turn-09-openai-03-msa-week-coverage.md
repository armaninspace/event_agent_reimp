# Turn 9: Which city–season pairs have sufficient counts of event and baseline weeks to support a within-season difference-in-differences estimate?

Selected candidate: `turn-09-openai-03-msa-week-coverage`

Rationale: A coverage screen at the city-season level ensures enough treated and control weeks to estimate stable within-season effects with fixed effects.

Caveat: Requires defining minimum thresholds for event and non-event weeks per city-season.

## Statistical Evidence

Result count: `4`

Minimum adjusted p-value: `6.264109922127072e-48`

Adjusted-significance flag: `True`

Result IDs:
- `exploratory:msa_week:revenue_all`
- `exploratory:msa_week:merchants_all`
- `matched:msa_week:revenue_all`
- `matched:msa_week:merchants_all`

Statistical caveats:
- Statistical evidence is observational; causal-design diagnostics do not prove causality.
- Adjusted p-values do not establish causality.

Rejected candidates:
- `turn-09-openai-01-city-week-event-spending`
- `turn-09-openai-02-identification-risk`

Notebook status: `lightweight_executed`.
