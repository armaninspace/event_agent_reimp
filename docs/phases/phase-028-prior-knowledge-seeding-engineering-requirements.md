# Phase 028: Prior Knowledge Seeding

## Phase Goal

Make the friends loop read prior notebook knowledge before proposing candidates, so a run can start from durable notebook memory instead of only current-run state.

## Requirements

- Load a compact summary from a prior `notebook-knowledge.json`.
- Include prior knowledge in `knowledge.read` telemetry.
- Include prior knowledge in OpenAI hypothesis prompts and traces.
- Add CLI support for `--prior-notebook-knowledge-path`.
- Add phase-regression and audit fields for prior knowledge entry count.
- Run a 20-turn replay regression using Phase 027 knowledge as prior memory.

## Non-Goals

- Changing candidate selection outcomes in replay mode.
- Replacing the current QuestionForum records.
- Reading arbitrary notebook JSON from outside an explicit path.
- Live OpenAI inference.

## Assumptions

- A compact summary is safer than injecting all prior notebook text.
- Prompt traces are sufficient evidence that prior knowledge was available to live/replay OpenAI reasoning.
- Future phases can use the summary to alter deterministic candidate proposals.

## Affected Layers

- Notebook knowledge base
- Friends loop
- OpenAI prompt construction
- Phase regression
- Final audit
- CLI
- Tests and documentation

## Affected Modules

- `app/notebook_knowledge_base.py`
- `app/friends_loop.py`
- `app/openai_reasoning.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_notebook_knowledge_base.py`
- `tests/test_openai_reasoning.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The prior knowledge path is explicit. The loop loads a compact summary with entry count, latest seed question, latest semantic slot, latest source cell, and recent seed questions. OpenAI prompt construction embeds this summary, and telemetry records it for replay.

## Data/API/Config Changes

- `run_friends_question_loop` accepts `prior_notebook_knowledge_path`.
- `run_phase_regression` and its CLI accept `prior_notebook_knowledge_path`.
- Session summary gains `prior_notebook_knowledge_entry_count`.
- Audit gains `prior_notebook_knowledge_entry_count`.

## Demo Requirements

- Run focused knowledge/OpenAI/regression tests.
- Run 20-turn replay regression with Phase 027 knowledge as input.
- Run replication audit against Phase 028.
- Run full validation.

## Test Requirements

- Prior knowledge summary loads recent entries.
- OpenAI prompt contains prior knowledge.
- Friends-loop telemetry records prior knowledge.
- Audit reports 20 prior knowledge entries.
- Validation passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Read only an explicitly provided knowledge path.
- Keep prompt memory compact to reduce leakage and prompt noise.

## Risks

- Replay mode proves prompt context, not live model use.
- Knowledge summaries may be too compact for rich follow-up generation.
- Repeated prior seeds can still lead to repetitive candidates until candidate policy consumes them more deeply.

## Acceptance Criteria

- Phase regression reports `prior_notebook_knowledge_entry_count=20`.
- Audit reports `prior_notebook_knowledge_entry_count=20`.
- OpenAI traces include prior notebook knowledge summary.
- Validation passes.

## Rollback Plan

Revert the Phase 028 commit or remove prior-knowledge loading, prompt wiring, regression/audit fields, tests, artifacts, and docs.
