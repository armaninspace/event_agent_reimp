# Turn 1: Which MSAs have enough event and baseline weeks to support a stable estimate of event-related spending lift?

Selected candidate: `turn-01-openai-02-msa-week-coverage`

Rationale: Coverage diagnostics using counts of event vs non-event weeks and variance of spend enable us to flag markets with adequate sample size for credible comparisons.

Caveat: Assumes our event calendar and spending data span a sufficient period to assess exposure.

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
- `turn-01-openai-01-city-week-event-spending`
- `turn-01-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
