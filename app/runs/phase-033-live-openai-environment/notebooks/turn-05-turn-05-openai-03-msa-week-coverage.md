# Turn 5: Which MSAs meet a minimum coverage threshold (e.g., at least 12 game weeks and 12 matched baseline weeks within-year) to support within-MSA estimates?

Selected candidate: `turn-05-openai-03-msa-week-coverage`

Rationale: Coverage screening ensures reliable inference by confirming sufficient treated and baseline weeks per MSA before modeling event effects.

Caveat: Thresholds should be tuned to actual data density and seasonality patterns.

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
- `turn-05-openai-01-city-week-event-spending`
- `turn-05-openai-02-identification-risk`

Notebook status: `lightweight_executed`.
