# Phase 031 Backlog: Semantic Slot Diversity

## Completed

- Track selected semantic slot counts in friends-loop state.
- Annotate candidate reasoning with prior semantic slot selection count.
- Select from least-used non-duplicate semantic slots after tournament ranking.
- Add semantic slot coverage to phase regression and audit.
- Add focused tests for replay and deterministic coverage.
- Run MAF replay smoke.
- Run 20-turn replay regression.
- Refresh replication audit.

## Remaining

- Add live OpenAI run evidence when `OPENAI_API_KEY` is available.
- Add broader semantic clustering beyond the fixed thesis semantic slots.
- Add a larger replay corpus with multiple city-week variants so all three slots can be covered without selecting prior duplicates.
