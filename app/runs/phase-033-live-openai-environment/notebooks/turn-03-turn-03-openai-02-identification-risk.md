# Turn 3: Do surrounding non-game weeks show offsetting spending drops (t−1 or t+1) that indicate temporal substitution rather than true net gains?

Selected candidate: `turn-03-openai-02-identification-risk`

Rationale: Lead/lag indicators around event weeks within each city can reveal anticipation or rebound effects using the current weekly panel.

Caveat: Weekly aggregation may mask same-week displacement across days.

## Statistical Evidence

Result count: `4`

Minimum adjusted p-value: `8.018939027100663e-08`

Adjusted-significance flag: `True`

Result IDs:
- `matched:city_week:revenue_all`
- `matched:city_week:merchants_all`
- `matched:msa_week:revenue_all`
- `matched:msa_week:merchants_all`

Statistical caveats:
- Statistical evidence is observational; causal-design diagnostics do not prove causality.
- Adjusted p-values do not establish causality.

Rejected candidates:
- `turn-03-openai-01-identification-risk`
- `turn-03-openai-03-identification-risk`

Notebook status: `lightweight_executed`.
