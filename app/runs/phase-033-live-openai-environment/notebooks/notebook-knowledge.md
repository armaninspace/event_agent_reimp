# Notebook Knowledge Base

Schema: `phase-027.notebook-knowledge-base.v1`
Entry count: `20`
Latest notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-20-turn-20-openai-01-city-week-event-spending.ipynb`
Latest seed question: Do post-game weeks in a city show a spending dip that offsets part of the home game-week gain, suggesting intertemporal substitution?

## Entries

### Turn 1: `turn-01-openai-02-msa-week-coverage`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-01-turn-01-openai-02-msa-week-coverage.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-01-turn-01-openai-02-msa-week-coverage.md`
- Status: `lightweight_executed`
- Semantic slot: `msa_week_coverage`
- Seed question: Which MSAs have enough event and baseline weeks to support a stable estimate of event-related spending lift?
- Caveat: Assumes our event calendar and spending data span a sufficient period to assess exposure.

### Turn 2: `turn-02-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-02-turn-02-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-02-turn-02-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: Does weekly local consumer spending scale with the number of home games in a city (e.g., single vs multi-game weeks), relative to matched baseline weeks?
- Caveat: Requires consistent week-level exposure counts and controls for seasonality and holidays.

### Turn 3: `turn-03-openai-02-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-03-turn-03-openai-02-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-03-turn-03-openai-02-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: Do surrounding non-game weeks show offsetting spending drops (t−1 or t+1) that indicate temporal substitution rather than true net gains?
- Caveat: Weekly aggregation may mask same-week displacement across days.

### Turn 4: `turn-04-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-04-turn-04-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-04-turn-04-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: How much higher is citywide consumer spending during home-game weeks compared with the same city's away-game weeks in the same season?
- Caveat: Assumes away weeks are not themselves local draws and that within-season schedules provide comparable baselines.

### Turn 5: `turn-05-openai-03-msa-week-coverage`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-05-turn-05-openai-03-msa-week-coverage.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-05-turn-05-openai-03-msa-week-coverage.md`
- Status: `lightweight_executed`
- Semantic slot: `msa_week_coverage`
- Seed question: Which MSAs meet a minimum coverage threshold (e.g., at least 12 game weeks and 12 matched baseline weeks within-year) to support within-MSA estimates?
- Caveat: Thresholds should be tuned to actual data density and seasonality patterns.

### Turn 6: `turn-06-openai-01-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-06-turn-06-openai-01-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-06-turn-06-openai-01-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: Do treated city-weeks show flat spending trends in the 4–8 weeks before events compared with matched non-event weeks in the same city?
- Caveat: Relies on stable weekly baselines and no anticipatory shocks.

### Turn 7: `turn-07-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-07-turn-07-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-07-turn-07-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: Within each city, does weekly consumer spending rise more in weeks with multiple home games versus single-game weeks after controlling for baseline trends?
- Caveat: Assumes the count of home games per week is measured accurately and not driven by unobserved promotions.

### Turn 8: `turn-08-openai-01-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-08-turn-08-openai-01-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-08-turn-08-openai-01-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: Do spending levels already trend upward in the one to two weeks before game weeks within the same city, suggesting residual confounding?
- Caveat: Requires sufficient pre-event, non-overlapping weeks per city to estimate clean pre-trends.

### Turn 9: `turn-09-openai-03-msa-week-coverage`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-09-turn-09-openai-03-msa-week-coverage.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-09-turn-09-openai-03-msa-week-coverage.md`
- Status: `lightweight_executed`
- Semantic slot: `msa_week_coverage`
- Seed question: Which city–season pairs have sufficient counts of event and baseline weeks to support a within-season difference-in-differences estimate?
- Caveat: Requires defining minimum thresholds for event and non-event weeks per city-season.

### Turn 10: `turn-10-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-10-turn-10-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-10-turn-10-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: Which merchant categories experience the largest incremental card spending during home game weeks versus matched baseline weeks by city?
- Caveat: Only measures spend in the card data sample and may miss cash-heavy venues.

### Turn 11: `turn-11-openai-01-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-11-turn-11-openai-01-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-11-turn-11-openai-01-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: Do we observe a spending uptick in the week before home games (placebo lead), indicating potential confounding rather than true event impact?
- Caveat: Assumes accurate game calendars and stable weekly alignment without major unrelated shocks.

### Turn 12: `turn-12-openai-02-msa-week-coverage`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-12-turn-12-openai-02-msa-week-coverage.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-12-turn-12-openai-02-msa-week-coverage.md`
- Status: `lightweight_executed`
- Semantic slot: `msa_week_coverage`
- Seed question: Which MSAs have at least six home-game weeks and twelve matched non-game weeks in the study window to support stable difference-in-differences estimates?
- Caveat: Thresholds may be tuned but require consistent weekly coverage flags.

### Turn 13: `turn-13-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-13-turn-13-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-13-turn-13-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: How much does local card spending change in the host city during playoff game weeks versus regular-season game weeks, after adjusting for typical seasonal baselines?
- Caveat: Differences could reflect concurrent tourism or media shocks unrelated to the games.

### Turn 14: `turn-14-openai-01-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-14-turn-14-openai-01-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-14-turn-14-openai-01-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: In weeks when a city hosts a home game, do matched peer MSAs without any events show no comparable spending increase, supporting a causal home-game effect?
- Caveat: Requires a clean set of peer MSAs with verified no-event weeks and good seasonal matching.

### Turn 15: `turn-15-openai-03-msa-week-coverage`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-15-turn-15-openai-03-msa-week-coverage.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-15-turn-15-openai-03-msa-week-coverage.md`
- Status: `lightweight_executed`
- Semantic slot: `msa_week_coverage`
- Seed question: How many MSAs meet a minimum design of at least six game weeks and six matched baseline weeks within the sample period?
- Caveat: Overly strict thresholds may exclude informative mid-sized markets.

### Turn 16: `turn-16-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-16-turn-16-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-16-turn-16-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: Do game weeks deliver a net spending gain when you compare week 0 to the combined weeks -1 and +1 in the same city?
- Caveat: Weekly aggregation may mask category-level substitution and visitor vs. resident effects.

### Turn 17: `turn-17-openai-01-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-17-turn-17-openai-01-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-17-turn-17-openai-01-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: Do placebo weeks immediately before or after home-game weeks show comparable spending bumps, suggesting time-varying confounders rather than true event effects?
- Caveat: Requires clear labeling of event and non-event weeks and consistent spending aggregation granularity.

### Turn 18: `turn-18-openai-02-msa-week-coverage`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-18-turn-18-openai-02-msa-week-coverage.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-18-turn-18-openai-02-msa-week-coverage.md`
- Status: `lightweight_executed`
- Semantic slot: `msa_week_coverage`
- Seed question: Which MSAs have enough treated weeks and matched baseline weeks within the same season to produce stable event-spending estimates?
- Caveat: Thresholds for 'sufficient' exposure (e.g., ≥8 treated and ≥8 baseline weeks) may need tuning by variance and sample size.

### Turn 19: `turn-19-openai-03-identification-risk`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-19-turn-19-openai-03-identification-risk.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-19-turn-19-openai-03-identification-risk.md`
- Status: `lightweight_executed`
- Semantic slot: `identification_risk`
- Seed question: Do we see significant spending increases in the one to two weeks before game weeks, indicating pre-event trends that could bias impact estimates?
- Caveat: Lead-window length affects power and may miss subtle anticipatory effects.

### Turn 20: `turn-20-openai-01-city-week-event-spending`

- Notebook: `app/runs/phase-033-live-openai-environment/notebooks/turn-20-turn-20-openai-01-city-week-event-spending.ipynb`
- Markdown: `app/runs/phase-033-live-openai-environment/notebooks/turn-20-turn-20-openai-01-city-week-event-spending.md`
- Status: `lightweight_executed`
- Semantic slot: `city_week_event_spending`
- Seed question: Do post-game weeks in a city show a spending dip that offsets part of the home game-week gain, suggesting intertemporal substitution?
- Caveat: One sentence limitation.
