# Phase 005: Notebook And Wiki Workspace

## Phase Goal

Make loop memory durable by adding a notebook/wiki workspace scaffold that writes append-oriented wiki files plus one scaffolded notebook and Markdown export per turn.

## Requirements

- Add notebook/wiki workspace support.
- Create or update:
  - `SCHEMA.md`
  - `index.md`
  - `log.md`
  - `question-board.md`
  - `decision-records.md`
  - `caveats.md`
  - `semantic-map.md`
  - `findings.md`
- Write one `.ipynb` file per turn.
- Write one Markdown export per turn.
- Keep wiki files append-oriented.
- Integrate workspace writing into `run_friends_question_loop`.
- Update phase regression summary to require notebook workspace artifacts.
- Add tests for per-turn notebooks, Markdown exports, wiki append behavior, and regression summary checks.

## Non-Goals

- Execute notebooks.
- Use `nbformat` or `nbclient`.
- Validate notebook code outputs.
- Build business report or playback UI.
- Live LLM or Microsoft Agent Framework orchestration.

## Assumptions

- Valid notebook JSON can be written directly for a scaffold phase.
- Execution status is `scaffolded`.
- Markdown exports can be generated from the same selected-candidate payload.
- Later phases will add real execution and conversion tooling.

## Affected Layers

- Memory/evidence layer
- Friends-loop artifact writing
- Regression validation
- Tests

## Affected Modules

- `app/notebook_workspace.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `tests/test_notebook_workspace.py`
- `tests/test_friends_loop.py`
- `tests/test_phase_regression.py`

## Dependency/Library Choices

No new dependencies are required. `nbformat` is not installed in this container, so Phase 005 writes minimal valid notebook JSON with the Python standard library. Notebook execution is deferred.

## Architecture Notes

The notebook workspace is an append-only evidence surface. The friends loop writes one turn notebook and Markdown export after candidate selection. Wiki files accumulate public decisions, caveats, semantic slots, and findings.

## Data/API/Config Changes

- Friends-loop runs now write notebook workspace files under a caller-provided `notebook_dir`.
- Phase regression now checks notebook workspace existence and per-turn notebook/export counts.

## Demo Requirements

- Run the 20-turn regression.
- Show that notebook workspace checks pass.
- Record generated wiki and notebook paths.

## Test Requirements

- Tests verify wiki files exist.
- Tests verify per-turn `.ipynb` and `.md` files exist.
- Tests verify append behavior across multiple turns.
- Tests verify regression summary requires notebook workspace.
- Validation passes.

## Security/Sandbox Considerations

- Do not execute generated notebook code.
- Do not log private chain-of-thought.
- Do not mutate source CSVs.
- Do not read `.env`.

## Risks

- Scaffolded notebooks can be overclaimed as executed evidence.
- Direct JSON notebooks are less ergonomic than `nbformat`; later execution phases should add the dependency.
- Regression now requires notebook workspace, so future loop changes must preserve it.

## Acceptance Criteria

- Each loop turn writes one notebook and one Markdown export.
- Wiki files exist and are append-oriented.
- 20-turn regression passes and reports notebook workspace checks as present.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 005 commit or remove notebook workspace integration, generated artifacts, tests, and Phase 005 docs.
