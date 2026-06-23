# Reimplementation Notes For The Event Agent Research System

These notes are for an engineer rebuilding the system described in `event-agent-thesis.md` from scratch. Treat the thesis as the architectural argument and this document as the build manual: what to implement first, which libraries were used, how to phase the work, how to verify multi-turn behavior, what to log, and where the common traps are.

The system is a governed event-evidence workflow. It is not just a chatbot. A public question should travel through question governance, hypothesis routing, statistical execution, notebook generation, wiki memory, telemetry, reports, and regression evidence. Every layer should leave artifacts that can be inspected after the run.

## 1. Technology Stack

The original implementation is Python-first and intentionally file-artifact-oriented. The important dependencies are pinned in `requirements.txt`:

| Library | Role |
| --- | --- |
| `pydantic` | Structured models and validation for hypotheses, packets, and typed payloads. |
| `numpy` | Numeric support for generated and reference data workflows. |
| `pandas` | Dataframe manipulation, summaries, notebook output tables, and report inputs. |
| `scipy` | Statistical tests and distributions. |
| `statsmodels` | Regression and statistical modeling support. |
| `scikit-learn` | Matching, similarity, and general data-science utilities where needed. |
| `matplotlib`, `seaborn`, `plotly` | Figures and exploratory visualizations. |
| `pyarrow` | Columnar data support when datasets grow beyond simple CSV use. |
| `duckdb` | Local analytical SQL and semantic layer backing. |
| `nbformat` | Programmatic notebook construction. |
| `nbclient` | Full Jupyter notebook execution backend. |
| `nbconvert` | Notebook export support. |
| `ipykernel` | Kernel support for nbclient execution. |
| `agent-framework` | Agent runtime dependency from the original environment. |

You can reimplement most of the core with the Python standard library plus pandas, scipy/statsmodels, duckdb, pydantic, nbformat, and nbclient. The UI reports in the original are static HTML generated from Python strings and JSON payloads. No frontend framework is required. Mermaid diagrams in documentation use the Mermaid CDN, not a build-time renderer.

Recommended baseline:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 -m pytest -q
```

For a clean-room rewrite, keep the first version boring:

- Python package under `app/`
- scripts under `scripts/`
- tests under `tests/`
- public question seeds under `data/question_forum/`
- run artifacts under `app/runs/<run-id>/friends-question-loop/`
- notebooks and wiki memory under `common-analysis/notebooks/`

Do not start with a web application. Start with a deterministic CLI that writes auditable artifacts.

## 2. Architectural Spine

The minimum viable architecture has these layers:

1. QuestionForum store
2. Candidate generation and policy
3. Tournament ranking
4. Reflection review
5. Hypothesis evolution
6. Hypothesis/EDA/workflow classifier
7. Experimental design router
8. Statistical test runner
9. Notebook writer and executor
10. Wiki and notebook knowledge base
11. Telemetry event stream
12. Business report HTML
13. Playback HTML
14. Phase regression summary

The key design rule is separation:

- Public layer: readable stakeholder questions.
- Governance layer: candidate scoring, comparison, review, and evolution.
- Execution layer: formal hypotheses, test routing, data access, and statistics.
- Evidence layer: notebooks, wiki, telemetry, reports, summaries.

Do not let internal handles become public questions. Terms like `semantic_msa_batch_supported_positive`, `revenue_all`, and `matched_msa_week_controls` are useful inside code, but the public report should say things like "Do big sports crowds actually turn into more local spending?"

## 3. Phase Plan

Build this in phases. Each phase should have an acceptance test and a multi-turn regression gate. Do not try to build the whole system in one pass.

### Phase 1: Static Evidence Packet

Goal: convert one user question into a structured evidence packet.

Implement:

- schema context
- hypothesis card
- skeptic review
- design plan
- deterministic synthetic result
- JSON and Markdown output

Acceptance:

- one command writes an `experiment_packet.json`
- packet includes question, hypothesis, design, result, caveat, and audit log
- unit tests cover packet shape

### Phase 2: Reference Event Data

Goal: move beyond synthetic examples.

Implement:

- reference sports/game data loader
- local economic measure loader
- city-week join builder
- data quality checks
- reproducible fixture data

Acceptance:

- tests build city-week reference data from fixture inputs
- output records have stable grain and required fields
- warnings are explicit for missing or weak data

### Phase 3: Friends Loop

Goal: create a turn-based research loop with roles.

Implement friend roles as interfaces:

- Spark: proposes interesting candidates
- Skeptic: guards identification and claims
- Mapper: links data, semantic slots, and memory
- Moderator: ranks and selects candidates
- DataAgent: writes durable artifacts

Acceptance:

- `run_friends_question_loop(turn_count=2)` completes
- each turn has selected and rejected candidates
- session JSON and Markdown are written
- candidate selection is deterministic under fixed inputs

### Phase 4: Notebook Workspace And Wiki

Goal: make memory durable.

Implement:

- `common-analysis/notebooks/SCHEMA.md`
- `index.md`
- `log.md`
- `question-board.md`
- `decision-records.md`
- `caveats.md`
- `semantic-map.md`
- `findings.md`
- generated `.ipynb` per turn
- Markdown export per notebook

Acceptance:

- each turn writes a notebook and Markdown export
- wiki files are append-oriented
- next turn can read summary state from the wiki

### Phase 5: Lightweight Notebook Execution

Goal: stop treating notebooks as inert scaffolds.

Implement:

- notebook payload generation with `nbformat`
- lightweight executor for simple generated Python cells
- execution metadata
- output capture
- Markdown conversion

Acceptance:

- notebook code cells have outputs after execution
- report evaluator distinguishes `scaffolded` from `lightweight_executed`
- scaffolded notebooks cannot produce validated findings

### Phase 6: Nbclient Backend

Goal: support real Jupyter execution when needed.

Implement:

- `--notebook-execution-backend lightweight|nbclient`
- `nbclient.NotebookClient`
- kernel metadata
- timeout handling
- validation metadata

Acceptance:

- test can run one turn with `nbclient`
- notebook status becomes `nbclient_executed`
- readiness score improves but still does not imply validated/publishable evidence

### Phase 7: Hypothesis Classification And Routing

Goal: prevent workflow tasks from entering statistical testing.

Implement classifier outcomes:

- `statistical_hypothesis`
- `eda_question`
- `workflow_task`

Workflow-task trigger words should include artifact concepts such as notebook, wiki, prompt, report, UI, and logging. A question about which notebook to create is not a statistical hypothesis.

Acceptance:

- notebook reuse question classifies as `workflow_task`
- formal hypothesis requires H0, H1, population, unit, exposure, comparison, outcome, direction, test family, alpha, and decision rule
- workflow-task statistical misroute count is zero in regression summaries

### Phase 8: Matched Statistical Tests

Goal: execute actual exploratory statistical designs.

Implement:

- city-week matched controls
- MSA-week matched controls
- batch screens
- diagnostics
- p-values
- adjusted p-values
- caveats
- claim boundaries

Acceptance:

- tests cover positive, null, not-testable, and fragile cases
- every statistical result includes diagnostics and caveats
- reports say observational association, not causal proof

### Phase 9: Semantic Layer

Goal: allow governed local SQL for agents and notebooks.

Implement with DuckDB:

- whitelisted views
- SELECT-only enforcement
- row limits
- referenced view extraction
- query telemetry
- metric definitions

Acceptance:

- non-SELECT SQL fails
- non-whitelisted table access fails
- query telemetry records SQL, views, row count, columns, and row preview

### Phase 10: Reports And Playback

Goal: every run should be inspectable.

Implement:

- `friends_loop_session.json`
- `friends_loop_session.md`
- `friends_loop_telemetry.json`
- `business_evidence_report.html`
- `ui/index.html`
- `discovery_decision_summary.md`
- `phase_regression_summary.json`

Acceptance:

- both HTML formats are produced per run
- playback UI renders from moved telemetry JSON
- business report preserves caveats
- discovery decision summary exposes routing and decisions

### Phase 11: QuestionForum Store

Goal: make public questions first-class records.

Implement JSON records with:

- `question_id`
- `kind`
- `persona`
- `question`
- `rationale`
- `priority`
- `popularity`
- `source_url`
- `status`
- `tags`

Allowed statuses:

- `proposed`
- `selected`
- `tested`
- `answered`
- `needs-review`

Acceptance:

- forum records load and validate
- candidates can cite forum metadata
- selected candidates carry forum metadata in 20-turn regression

### Phase 12: Tournament, Reflection, Evolution

Goal: add Co-Scientist-inspired governance.

Tournament:

- pairwise comparisons
- public interest score
- novelty score
- testability score
- evidence value score
- policy/business relevance score
- rank, wins, losses, transcript

Reflection:

- what would make this misleading?
- what prior evidence would weaken this?
- is this answerable with current data?
- status: `pass`, `needs-review`, `not-answerable`

Evolution:

- `split`
- `combine`
- `strengthen`
- `carry_forward`

Acceptance:

- selected candidates carry tournament, reflection, and evolution metadata
- deterministic transcripts are stored
- not-answerable candidates are penalized or filtered
- final 20-turn run completes with all metadata families present

## 4. Multi-Turn Verification

A single turn is not enough. Most failures only appear after memory, candidate suppression, notebook reuse, and report aggregation have run several times.

Use a three-level verification ladder:

### Level 1: Unit Tests

Run focused tests after each module change:

```bash
python3 -m pytest tests/test_statistical_hypothesis.py -q
python3 -m pytest tests/test_semantic_layer.py -q
python3 -m pytest tests/test_report_evaluator.py -q
```

Use unit tests for:

- candidate classification
- forum loading
- tournament score math
- reflection statuses
- evolution actions
- semantic SQL guardrails
- notebook status detection
- report evaluator caps

### Level 2: Short Loop Smoke

Run one or two turns after orchestration changes:

```bash
python3 - <<'PY'
from pathlib import Path
from app.friends_loop import run_friends_question_loop

session = run_friends_question_loop(
    turn_count=2,
    output_dir=Path("app/runs/smoke/friends-question-loop"),
    notebook_dir=Path("common-analysis/notebooks-smoke"),
)
print(session["session_summary"]["completed_turns"])
print(session["artifact_paths"])
PY
```

Check:

- completed turns
- session JSON exists
- telemetry JSON exists
- business report exists
- playback UI exists
- notebooks exist
- wiki was updated

### Level 3: 20-Turn Regression

Every phase that touches candidate selection, routing, notebooks, telemetry, reports, or memory should end with a 20-turn run.

Use a stable run id:

```bash
python3 scripts/run_phase_regression.py \
  --phase-id phase-XYZ-short-name \
  --turns 20
```

If you reimplement without this helper, the summary must still verify:

- requested turns: 20
- completed workflows: 20
- stopped early: false
- workflow-task statistical misroutes: 0
- selected candidates carry required metadata
- business HTML exists
- playback HTML exists
- session JSON exists
- telemetry JSON exists
- discovery decision summary exists
- notebook workspace updated

Do not accept a phase because "the run did not crash." The acceptance question is whether the expected metadata and artifacts exist on every selected turn.

## 5. Logging And Observability Contracts

Logging is not optional. For this system, logging is part of the research method.

Use structured JSON events, not only text logs. Each event should have:

- `event_id`
- `sequence`
- `time_offset_ms`
- `event_type`
- `turn`
- `actor`
- `summary`
- `payload`

Minimum event types:

- `turn.started`
- `knowledge.read`
- `board.proposed`
- `board.ranked`
- `semantic.query`
- `hypothesis.classified`
- `question.submitted`
- `workflow.stage`
- `result.studied`
- `notebook.created`
- `wiki.updated`
- `knowledge.updated`
- `discussion.message`
- `memory.seeded`
- `turn.completed`

Gotchas:

- Do not log only final answers. You need the board and rejected candidates.
- Do not log only prose. Store structured payloads that tests can inspect.
- Do not omit workflow stages. Debugging needs the path from candidate to packet to notebook.
- Do not put private chain-of-thought into logs. Use public rationale, assumptions, caveats, and review notes.
- Do not let telemetry depend on absolute paths only. Reports should still work when a telemetry file is moved.
- Keep prompt hashes in telemetry so prompt drift is visible.

For every run, write:

```text
friends_loop_session.json
friends_loop_session.md
friends_loop_telemetry.json
discovery_decision_summary.md
business_evidence_report.html
ui/index.html
phase_regression_summary.json
```

## 6. Notebook Implementation Gotchas

Notebook behavior is one of the easiest areas to overclaim.

### Use Two Execution Backends

Implement:

- `lightweight`: quick executor for generated Python cells
- `nbclient`: real Jupyter execution for higher fidelity

Do not pretend lightweight execution equals validated notebook execution. In scoring/reporting:

- `scaffolded`: notebook exists but code did not execute
- `lightweight_executed`: useful demo evidence, capped maturity
- `nbclient_executed`: stronger execution evidence, still not automatically validated
- `validated`: notebook passed explicit validation contract
- `published`: only after human/release process, if you add one

### Embed Validation Contracts

Each turn notebook should embed:

- selected candidate
- result summary
- formal hypothesis if applicable
- statistical result if applicable
- validation contract

Then execute a cell that compares notebook-visible values against the contract.

```python
validation_contract = result_summary.get("notebook_validation_contract", {})
observed_contract = {
    "schema_version": validation_contract.get("schema_version"),
    "kind": selected_candidate.get("kind"),
    "metric": result_summary.get("metric"),
    "value": result_summary.get("value"),
    "claim_strength": result_summary.get("claim_strength"),
}
assert all(
    observed_contract.get(key) == validation_contract.get(key)
    for key in observed_contract
)
```

The real contract should also check selected statistical fields, semantic slot, and data snapshot hashes.

### Export Markdown

Always export notebooks to Markdown. LLMs and reviewers can read Markdown more easily than `.ipynb` JSON.

Store both:

```text
turn-07-some-kind.ipynb
turn-07-some-kind.md
```

### Keep Run-Level Correction Separate

Per-turn notebooks are written during turns. Multiple-testing correction happens after all turns. Do not mutate old turn notebooks to add later correction results. Write a run-level correction notebook:

```text
999-multiple-testing-corrections.ipynb
999-multiple-testing-corrections.md
```

This keeps the audit trail clean.

## 7. Prompt And Role Gotchas

Keep role specs in Markdown if you want easy editing, but keep contracts in code.

Recommended split:

- Markdown prompts: role, voice, responsibilities, prohibited behavior, claim boundaries.
- Code: candidate data model, routing, scoring, validation, report generation, notebook execution, telemetry.

Why: prompts can guide behavior, but code can enforce behavior.

Prompt/version rules:

- Hash each prompt file with SHA-256.
- Store friend prompt hashes in session JSON and telemetry.
- Store evidence-agent prompt hashes separately.
- Fail or warn when expected prompt specs are missing.
- Do not rely on default prompts silently.

Common prompt mistakes:

- Asking the model to "be careful" instead of storing a caveat field.
- Letting internal handles become public questions.
- Allowing workflow questions to become statistical hypotheses.
- Treating generated rationale as private reasoning. Store only public rationale.
- Changing role files without updating prompt hashes in reports.

## 8. Report Rendering Gotchas

There are two different HTML products:

1. Business evidence report: stakeholder-readable findings and caveats.
2. Playback UI: replayable telemetry timeline.

Do not merge them. They serve different audiences.

Business report rules:

- Use public question text as headline.
- Preserve caveats near findings.
- Say "observational association", not causal proof.
- Show method and evidence strength.
- Avoid internal handles unless in technical appendix.

Playback UI rules:

- Render from `friends_loop_telemetry.json`.
- Include controls to step through events.
- Show actor, turn, event type, summary, and payload details.
- Work when telemetry JSON is moved or embedded.

Static HTML gotchas:

- Escape JSON before embedding it into `<script>` tags.
- Escape user/forum text in HTML.
- Keep large payloads collapsible or scrollable.
- Test moved-log rendering, not only in-place rendering.
- Do not depend on a dev server unless the UI truly requires one.

Documentation HTML gotcha:

- If you render Markdown thesis to HTML, preserve code fences and Mermaid blocks.
- Headings inside fenced code blocks must not become page headings.
- Mermaid diagrams can use the CDN for documentation, but production reports should tolerate CDN failure.

## 9. Statistical And Product Claim Gotchas

The system uses exploratory observational evidence. This must shape the product.

Never write:

```text
Sports events caused revenue to increase.
```

Prefer:

```text
Under the recorded matched observational design, event-exposed locality-weeks showed higher mean revenue_all than matched no-game controls. This is exploratory association, not causal proof.
```

Guardrails:

- every statistical result has a caveat
- every matched test has diagnostics
- repeated screens have multiple-testing correction
- weak sample support downgrades claims
- notebook maturity caps claim strength
- public report avoids causal language
- future work names robustness gaps

## 10. Data And Semantic Layer Gotchas

If you add a semantic layer, constrain it hard.

Rules:

- SELECT only
- whitelist views
- row limits
- no filesystem access through SQL
- no mutation
- record referenced views
- record query purpose
- record row counts and preview rows

Useful views in the original design:

- `city_week_economic_games`
- `msa_week_economic_games`
- `msa_blocks`
- `game_events_msa`
- `semantic_metric_definitions`

Do not let generated SQL become invisible. Every semantic query should appear in telemetry.

## 11. File And Artifact Contracts

Use stable paths so tests and humans know where to look.

Run directory:

```text
app/runs/<run-id>/friends-question-loop/
```

Required run files:

```text
friends_loop_session.json
friends_loop_session.md
friends_loop_telemetry.json
discovery_decision_summary.md
business_evidence_report.html
ui/index.html
phase_regression_summary.json
```

Notebook workspace:

```text
common-analysis/notebooks/
  SCHEMA.md
  index.md
  log.md
  question-board.md
  decision-records.md
  caveats.md
  semantic-map.md
  findings.md
  notebook-knowledge.json
  notebook-knowledge.md
  000-question-bank.ipynb
  000-question-bank.md
  turn-01-*.ipynb
  turn-01-*.md
  999-multiple-testing-corrections.ipynb
  999-multiple-testing-corrections.md
```

Question forum:

```text
data/question_forum/questions.json
```

Prompt specs:

```text
app/agent_specs/friends/*.md
app/agent_specs/*.md
```

## 12. Data Files Needed

For a faithful reimplementation, keep the data surface small and explicit. The system needs public question seeds, sports event records, economic locality-week records, MSA matching metadata, and generated marts.

### Required Seed Files

These files should be treated as source inputs for the local demo/research workflow:

| Path | Required For | Notes |
| --- | --- | --- |
| `data/question_forum/questions.json` | QuestionForum layer | Public questions with persona, rationale, priority, popularity, source URL, status, and tags. |
| `data/reference/simple_economic_dataset.csv` | city-week and MSA-week economics | Main economic observation file. Current copy has about 87,745 rows. |
| `data/reference/simple_game_dataset.csv` | fallback game input | Game-level sports records. Used when enriched MSA game file is unavailable. |
| `data/reference/sports_games_msa_enriched.csv` | preferred game input | Game records enriched with MSA/block fields. Current copy has about 38,838 rows. |
| `data/reference/msa_blocks.csv` | MSA-week matching | MSA block metadata used for compact/sparse matching groups. |
| `data/reference/msa_attribute_master.csv` | MSA metadata | Attribute lookup for MSA labels, region, population, and related descriptors. |

The minimum city-week-only rebuild can start with:

```text
data/question_forum/questions.json
data/reference/simple_economic_dataset.csv
data/reference/simple_game_dataset.csv
```

The full MSA/semantic rebuild should include:

```text
data/reference/sports_games_msa_enriched.csv
data/reference/msa_blocks.csv
data/reference/msa_attribute_master.csv
```

### Generated Data Files

These can be regenerated from the seed files and should be documented as derived artifacts:

| Path | Generated By | Notes |
| --- | --- | --- |
| `data/reference/joined_city_week_game_economic.csv` | `scripts/build_reference_city_week_join.py` | City-week game/economic mart used by city-week matched tests. Current copy has about 5,777 rows. |
| `data/reference/joined_msa_week_game_economic.csv` | `scripts/build_msa_week_reference.py` | MSA-week game/economic mart used by MSA tests and semantic views. Current copy has about 48,723 rows. |
| `data/reference/semantic_layer.sqlite` | `app.semantic_layer.ensure_semantic_layer` | DuckDB/SQLite-style local semantic cache. Regenerate from CSVs instead of hand-editing. |
| `data/reference/real_weather_city_week.csv` | `app.tools.real_weather_pull` | Optional weather context. The current file is effectively empty/header-only in this workspace, so do not make core tests depend on it. |

Generation commands:

```bash
python3 scripts/build_reference_city_week_join.py \
  --economic data/reference/simple_economic_dataset.csv \
  --games data/reference/sports_games_msa_enriched.csv \
  --output data/reference/joined_city_week_game_economic.csv

python3 scripts/build_msa_week_reference.py \
  --economic data/reference/simple_economic_dataset.csv \
  --games data/reference/sports_games_msa_enriched.csv \
  --blocks data/reference/msa_blocks.csv \
  --output data/reference/joined_msa_week_game_economic.csv
```

The semantic layer should lazily build or refresh its local database from:

```text
data/reference/joined_city_week_game_economic.csv
data/reference/joined_msa_week_game_economic.csv
data/reference/msa_blocks.csv
data/reference/sports_games_msa_enriched.csv
data/reference/simple_economic_dataset.csv
```

### Data Contract Gotchas

- Do not require live API weather pulls for regression. They can rate-limit and make tests flaky.
- Prefer `sports_games_msa_enriched.csv` when available; fall back to `simple_game_dataset.csv` for city-week-only workflows.
- Treat `joined_*` files and `semantic_layer.sqlite` as reproducible outputs, not primary hand-maintained data.
- Keep row-grain explicit: city-week joins and MSA-week joins are different units of analysis.
- Store provenance fields in generated marts so reports can cite source files.
- Keep generated data small enough for CI-like 20-turn runs.
- Do not let notebooks mutate source CSVs.
- For clean-room demos, small fixture versions of these files are acceptable if they preserve column contracts and enough rows to exercise positive, null, fragile, and not-testable cases.

## 13. Suggested Tests

Start with these test classes:

- `test_question_forum_loads_and_validates_statuses`
- `test_tournament_outputs_pairwise_rank_and_transcript`
- `test_reflection_marks_workflow_or_unanswerable_items`
- `test_evolution_assigns_known_action`
- `test_notebook_reuse_question_is_workflow_task_not_hypothesis`
- `test_formal_hypothesis_requires_contract_fields`
- `test_semantic_layer_rejects_non_select_sql`
- `test_semantic_layer_rejects_non_whitelisted_views`
- `test_friends_loop_respects_turn_count_and_writes_artifacts`
- `test_friends_loop_persists_playback_telemetry`
- `test_business_report_is_written`
- `test_playback_ui_can_render_moved_log`
- `test_notebook_status_classification`
- `test_scaffolded_notebooks_cannot_be_validated_findings`
- `test_lightweight_notebook_execution_caps_maturity`
- `test_nbclient_backend_executes_notebooks`
- `test_phase_regression_summary_flags_workflow_statistical_misroutes`
- `test_selected_candidates_have_forum_tournament_reflection_evolution_metadata`

Regression tests should inspect artifacts, not only return values.

## 14. Minimal Acceptance Checklist

A clean-room implementation is credible when this checklist passes:

- `python3 -m pytest -q` passes.
- A 2-turn smoke run writes session JSON, telemetry JSON, both HTML reports, notebooks, Markdown exports, and wiki entries.
- A 20-turn run completes all 20 workflows.
- `stopped_early` is false.
- workflow-task statistical misroutes are zero.
- all selected candidates have forum metadata.
- all selected candidates have tournament metadata.
- all selected candidates have reflection metadata.
- all selected candidates have evolution metadata.
- business report uses public question wording.
- playback UI renders the telemetry timeline.
- discovery decision summary shows H0/H1, decisions, p-values, adjusted decisions, and designs.
- notebook status counts are recorded.
- prompt hashes are recorded.
- caveats are visible in notebooks and reports.

## 15. Reimplementation Order Of Operations

If you have to rebuild quickly, use this order:

1. Implement artifact directories and session JSON first.
2. Implement static candidate board and deterministic selection.
3. Add notebooks and Markdown exports.
4. Add telemetry events and playback UI.
5. Add business report.
6. Add hypothesis classification.
7. Add simple statistical runner.
8. Add wiki and notebook knowledge base.
9. Add semantic layer.
10. Add 20-turn regression summary.
11. Add QuestionForum.
12. Add tournament.
13. Add reflection.
14. Add evolution.
15. Add nbclient backend.
16. Add evidence promotion and report evaluator.

This order keeps the system demonstrable at every step. Avoid starting with the most sophisticated agent logic. Build the artifact spine first.

## 16. Final Advice

The main engineering mistake to avoid is treating the system as a prompt project. It is an artifact project. Prompts are useful, but artifacts are what make the system auditable.

The second mistake is accepting a single successful run. Multi-turn behavior is where the real failures appear: repeated questions, stale memory, missing notebooks, misrouted workflow tasks, report drift, and telemetry gaps.

The third mistake is overclaiming statistical results. A disciplined system that says "exploratory association with caveats" is more valuable than a dramatic system that implies causality it cannot prove.

Build the first version so that a skeptical reviewer can answer these questions from files alone:

- What question was asked?
- Who or what selected it?
- What alternatives were rejected?
- What data was used?
- What hypothesis was tested?
- What design was selected?
- What result was produced?
- What caveats apply?
- Which notebook executed?
- What memory was updated?
- What report was written?
- Did a 20-turn regression still pass?

If the files can answer those questions, the reimplementation is on the right track.
