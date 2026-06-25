# Turn 12: Which MSAs have at least six home-game weeks and twelve matched non-game weeks in the study window to support stable difference-in-differences estimates?

Selected candidate: `turn-12-openai-02-msa-week-coverage`

Rationale: A clear coverage screen ensures sufficient treated and control weeks per MSA, directly computable from the MSA-week event and spending availability tables.

Caveat: Thresholds may be tuned but require consistent weekly coverage flags.

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
- `turn-12-openai-01-city-week-event-spending`
- `turn-12-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
