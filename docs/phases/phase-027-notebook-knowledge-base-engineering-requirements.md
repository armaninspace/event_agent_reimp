# Phase 027: Notebook Knowledge Base

## Phase Goal

Implement the structured notebook knowledge base described by the thesis so notebooks become reusable agent memory, not just per-turn artifacts and Markdown exports.

## Requirements

- Extract structured knowledge from every turn notebook.
- Write `notebook-knowledge.json` for code and `notebook-knowledge.md` for humans/agents.
- Include notebook path, Markdown path, selected candidate, semantic slot, notebook status, execution backend, source cell IDs, seed question, and caveat.
- Build the knowledge base after notebook execution so status reflects executed artifacts.
- Add phase-regression and audit coverage.
- Keep 20-turn replay regression passing.

## Non-Goals

- Replacing the append-only wiki files.
- Adding a database.
- Using live OpenAI inference.
- Making notebook knowledge decide future candidates in this phase.

## Assumptions

- The generated notebook metadata and Markdown exports are sufficient to reconstruct compact memory entries.
- JSON plus Markdown is the right artifact pair for machine and human/agent readers.
- Candidate seeding from notebook knowledge can be a future phase.

## Affected Layers

- Notebook workspace
- Notebook execution
- Phase regression
- Final audit
- Tests and documentation

## Affected Modules

- `app/notebook_knowledge_base.py`
- `app/notebook_workspace.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_phase_regression.py`
- `scripts/run_replication_audit.py`
- `tests/test_notebook_knowledge_base.py`
- `tests/test_notebook_workspace.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The knowledge base is derived from committed artifacts, not from chat memory. The extractor reads generated notebooks and Markdown exports, then writes compact JSON and Markdown summaries. Phase regression writes the knowledge base after notebook execution so the entries capture `lightweight_executed` or `nbclient_executed` status.

## Data/API/Config Changes

- Notebook workspaces now include `notebook-knowledge.json` and `notebook-knowledge.md`.
- Phase regression summary gains `notebook_knowledge_present` and `notebook_knowledge`.
- Replication audit gains `notebook_knowledge_present` and `notebook_knowledge_entry_count`.

## Demo Requirements

- Run focused notebook knowledge tests.
- Run MAF replay smoke.
- Run 20-turn replay phase regression.
- Run replication audit against Phase 027.
- Run full validation.

## Test Requirements

- Empty workspaces produce zero-entry knowledge.
- Executed notebooks produce knowledge entries with executed status.
- Phase regression writes knowledge artifacts.
- Audit requires 20 knowledge entries.
- Full validation passes.

## Security/Sandbox Considerations

- The extractor reads only local generated notebooks and Markdown exports.
- Do not read secrets or environment files.
- Keep Markdown summaries compact to avoid memory noise.

## Risks

- Metadata extraction can drift if notebook structure changes.
- Knowledge entries are summaries, not full notebook substitutes.
- Candidate policy does not yet consume the knowledge base.

## Acceptance Criteria

- `notebook-knowledge.json` exists in the Phase 027 notebook workspace.
- `notebook-knowledge.md` exists in the Phase 027 notebook workspace.
- Phase regression reports `notebook_knowledge_present=True`.
- Audit reports `notebook_knowledge_entry_count=20`.
- Validation passes.

## Rollback Plan

Revert the Phase 027 commit or remove knowledge-base generation, regression/audit checks, tests, artifacts, and docs.
