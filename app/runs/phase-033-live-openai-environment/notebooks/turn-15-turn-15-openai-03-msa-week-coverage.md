# Turn 15: How many MSAs meet a minimum design of at least six game weeks and six matched baseline weeks within the sample period?

Selected candidate: `turn-15-openai-03-msa-week-coverage`

Rationale: Establishing exposure and comparison depth per MSA ensures sufficient power for within-MSA estimates and is directly measurable from MSA-week event flags.

Caveat: Overly strict thresholds may exclude informative mid-sized markets.

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
- `turn-15-openai-02-identification-risk`
- `turn-15-openai-01-city-week-event-spending`

Notebook status: `lightweight_executed`.
