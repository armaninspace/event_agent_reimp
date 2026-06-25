# Discovery Decision Summary

## Turn 1

Selected candidate: turn-01-openai-02-msa-week-coverage
Score: 26
Public rationale: Coverage diagnostics using counts of event vs non-event weeks and variance of spend enable us to flag markets with adequate sample size for credible comparisons.
Caveat: Assumes our event calendar and spending data span a sufficient period to assess exposure.
Rejected candidates: turn-01-openai-01-city-week-event-spending, turn-01-openai-03-identification-risk

## Turn 2

Selected candidate: turn-02-openai-01-city-week-event-spending
Score: 23
Public rationale: Testing a dose–response between game-week intensity and spending uses the city–week event counts and spend measures to link crowd exposure to observed lifts.
Caveat: Requires consistent week-level exposure counts and controls for seasonality and holidays.
Rejected candidates: turn-02-openai-02-city-week-event-spending, turn-02-openai-03-identification-risk

## Turn 3

Selected candidate: turn-03-openai-02-identification-risk
Score: 23
Public rationale: Lead/lag indicators around event weeks within each city can reveal anticipation or rebound effects using the current weekly panel.
Caveat: Weekly aggregation may mask same-week displacement across days.
Rejected candidates: turn-03-openai-01-identification-risk, turn-03-openai-03-identification-risk

## Turn 4

Selected candidate: turn-04-openai-01-city-week-event-spending
Score: 23
Public rationale: Away weeks provide a same-team, same-season counterfactual without local crowds, enabling a within-city comparison using weekly event and spending data.
Caveat: Assumes away weeks are not themselves local draws and that within-season schedules provide comparable baselines.
Rejected candidates: turn-04-openai-02-msa-week-coverage, turn-04-openai-03-identification-risk

## Turn 5

Selected candidate: turn-05-openai-03-msa-week-coverage
Score: 25
Public rationale: Coverage screening ensures reliable inference by confirming sufficient treated and baseline weeks per MSA before modeling event effects.
Caveat: Thresholds should be tuned to actual data density and seasonality patterns.
Rejected candidates: turn-05-openai-01-city-week-event-spending, turn-05-openai-02-identification-risk

## Turn 6

Selected candidate: turn-06-openai-01-identification-risk
Score: 25
Public rationale: A pre-trend check bounds causal claims by verifying parallel trends; the weekly city/MSA panel with event flags allows lead indicators and matched-within-city comparisons.
Caveat: Relies on stable weekly baselines and no anticipatory shocks.
Rejected candidates: turn-06-openai-03-city-week-event-spending, turn-06-openai-02-msa-week-coverage

## Turn 7

Selected candidate: turn-07-openai-01-city-week-event-spending
Score: 24
Public rationale: The event schedule allows counting home games per city-week, enabling a nonlinearity test of crowd intensity on spending using baseline-adjusted comparisons.
Caveat: Assumes the count of home games per week is measured accurately and not driven by unobserved promotions.
Rejected candidates: turn-07-openai-02-msa-week-coverage, turn-07-openai-03-identification-risk

## Turn 8

Selected candidate: turn-08-openai-01-identification-risk
Score: 25
Public rationale: A placebo-style lead test on the city-week panel using event flags and dates can reveal whether game timing aligns with pre-existing spending upswings.
Caveat: Requires sufficient pre-event, non-overlapping weeks per city to estimate clean pre-trends.
Rejected candidates: turn-08-openai-02-msa-week-coverage, turn-08-openai-03-city-week-event-spending

## Turn 9

Selected candidate: turn-09-openai-03-msa-week-coverage
Score: 24
Public rationale: A coverage screen at the city-season level ensures enough treated and control weeks to estimate stable within-season effects with fixed effects.
Caveat: Requires defining minimum thresholds for event and non-event weeks per city-season.
Rejected candidates: turn-09-openai-01-city-week-event-spending, turn-09-openai-02-identification-risk

## Turn 10

Selected candidate: turn-10-openai-01-city-week-event-spending
Score: 23
Public rationale: Category-level lifts clarify who benefits and can be tested by aggregating weekly spend by city, merchant category, and event-week indicators against matched baseline weeks.
Caveat: Only measures spend in the card data sample and may miss cash-heavy venues.
Rejected candidates: turn-10-openai-02-msa-week-coverage, turn-10-openai-03-identification-risk

## Turn 11

Selected candidate: turn-11-openai-01-identification-risk
Score: 25
Public rationale: Lead-week placebo tests on city/MSA weekly panels can reveal pre-trends that would undermine causal claims.
Caveat: Assumes accurate game calendars and stable weekly alignment without major unrelated shocks.
Rejected candidates: turn-11-openai-02-msa-week-coverage, turn-11-openai-03-city-week-event-spending

## Turn 12

Selected candidate: turn-12-openai-02-msa-week-coverage
Score: 23
Public rationale: A clear coverage screen ensures sufficient treated and control weeks per MSA, directly computable from the MSA-week event and spending availability tables.
Caveat: Thresholds may be tuned but require consistent weekly coverage flags.
Rejected candidates: turn-12-openai-01-city-week-event-spending, turn-12-openai-03-identification-risk

## Turn 13

Selected candidate: turn-13-openai-01-city-week-event-spending
Score: 24
Public rationale: This isolates intensity effects by comparing tagged playoff vs regular-season event weeks within cities using weekly spending data and matched non-event baselines, directly informing planning for higher-stakes events.
Caveat: Differences could reflect concurrent tourism or media shocks unrelated to the games.
Rejected candidates: turn-13-openai-02-identification-risk, turn-13-openai-03-msa-week-coverage

## Turn 14

Selected candidate: turn-14-openai-01-identification-risk
Score: 23
Public rationale: Cross-MSA placebo comparisons by week help rule out national shocks and seasonality using only the local event calendar and weekly spending series.
Caveat: Requires a clean set of peer MSAs with verified no-event weeks and good seasonal matching.
Rejected candidates: turn-14-openai-03-city-week-event-spending, turn-14-openai-02-msa-week-coverage

## Turn 15

Selected candidate: turn-15-openai-03-msa-week-coverage
Score: 24
Public rationale: Establishing exposure and comparison depth per MSA ensures sufficient power for within-MSA estimates and is directly measurable from MSA-week event flags.
Caveat: Overly strict thresholds may exclude informative mid-sized markets.
Rejected candidates: turn-15-openai-02-identification-risk, turn-15-openai-01-city-week-event-spending

## Turn 16

Selected candidate: turn-16-openai-01-city-week-event-spending
Score: 24
Public rationale: This tests whether observed event-week bumps reflect true incremental demand rather than timing shifts across adjacent weeks using the city-week spending series.
Caveat: Weekly aggregation may mask category-level substitution and visitor vs. resident effects.
Rejected candidates: turn-16-openai-02-msa-week-coverage, turn-16-openai-03-identification-risk

## Turn 17

Selected candidate: turn-17-openai-01-identification-risk
Score: 24
Public rationale: Using city-level weekly event flags, we can compare spending in t-1 and t+1 to the event week t to detect anticipation or persistence patterns that indicate identification risk.
Caveat: Requires clear labeling of event and non-event weeks and consistent spending aggregation granularity.
Rejected candidates: turn-17-openai-02-msa-week-coverage, turn-17-openai-03-city-week-event-spending

## Turn 18

Selected candidate: turn-18-openai-02-msa-week-coverage
Score: 22
Public rationale: A coverage screen by MSA and season ensures credible comparisons by confirming adequate treated and control week counts in the local data.
Caveat: Thresholds for 'sufficient' exposure (e.g., ≥8 treated and ≥8 baseline weeks) may need tuning by variance and sample size.
Rejected candidates: turn-18-openai-01-city-week-event-spending, turn-18-openai-03-identification-risk

## Turn 19

Selected candidate: turn-19-openai-03-identification-risk
Score: 25
Public rationale: Detecting lead effects addresses a core identification concern; we can test for pretrends by estimating lead indicators or comparing pre-event weeks to matched baselines within city/MSA weekly data.
Caveat: Lead-window length affects power and may miss subtle anticipatory effects.
Rejected candidates: turn-19-openai-01-city-week-event-spending, turn-19-openai-02-msa-week-coverage

## Turn 20

Selected candidate: turn-20-openai-01-city-week-event-spending
Score: 22
Public rationale: Using weekly city event flags and baseline non-game weeks, we can estimate the game-week lift and then test for a compensating dip in the immediately following week within the same city.
Caveat: One sentence limitation.
Rejected candidates: turn-20-openai-02-msa-week-coverage, turn-20-openai-03-identification-risk
