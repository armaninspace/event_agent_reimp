# Turn 19: Do we see significant spending increases in the one to two weeks before game weeks, indicating pre-event trends that could bias impact estimates?

Selected candidate: `turn-19-openai-03-identification-risk`

Rationale: Detecting lead effects addresses a core identification concern; we can test for pretrends by estimating lead indicators or comparing pre-event weeks to matched baselines within city/MSA weekly data.

Caveat: Lead-window length affects power and may miss subtle anticipatory effects.

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
- `turn-19-openai-01-city-week-event-spending`
- `turn-19-openai-02-msa-week-coverage`

Notebook status: `lightweight_executed`.
