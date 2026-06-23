# Semantic Smoke Report

Schema: phase-011.semantic-smoke.v1

## Query: select week_start_monday, revenue_all, has_game from city_week_events where has_game = 1

- Referenced views: city_week_events
- Columns: week_start_monday, revenue_all, has_game
- Rows returned: 10

## Query: select msa_code, week_start_monday, merchants_all from msa_week_events where has_game = 1

- Referenced views: msa_week_events
- Columns: msa_code, week_start_monday, merchants_all
- Rows returned: 10
