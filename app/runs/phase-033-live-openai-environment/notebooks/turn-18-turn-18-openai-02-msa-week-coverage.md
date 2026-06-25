# Turn 18: Which MSAs have enough treated weeks and matched baseline weeks within the same season to produce stable event-spending estimates?

Selected candidate: `turn-18-openai-02-msa-week-coverage`

Rationale: A coverage screen by MSA and season ensures credible comparisons by confirming adequate treated and control week counts in the local data.

Caveat: Thresholds for 'sufficient' exposure (e.g., ≥8 treated and ≥8 baseline weeks) may need tuning by variance and sample size.

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
