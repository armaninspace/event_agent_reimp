# Turn 18: Which MSAs have enough game and non-game weeks for a stable comparison?

Selected candidate: `turn-18-openai-02-msa-week-coverage`

Rationale: Coverage determines where later statistical tests are credible.

Caveat: Coverage does not estimate impact by itself.

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
- `turn-18-openai-01-city-week-event-spending`
- `turn-18-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
