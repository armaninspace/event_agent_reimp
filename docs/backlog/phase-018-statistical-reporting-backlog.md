# Phase 018 Backlog: Statistical Evidence Reporting

## P018-001: Render Statistical Evidence In Reports

- Stable item ID: `P018-001`
- Title: Add report sections for statistical evidence
- Rationale: Stakeholders need to inspect statistical evidence from the business report.
- Affected files/modules: `app/reporting.py`, `tests/test_reporting.py`
- Implementation steps: Render result count, minimum adjusted p-value, significance flag, result IDs, and caveats.
- Unit test expectations: HTML escaping and statistical evidence rendering are tested.
- E2E test expectations: 20-turn regression report contains statistical evidence sections.
- Demo relevance: Generated HTML is phase evidence.
- Acceptance criteria: Business report renders statistical evidence safely.
- Status: done

## P018-002: Render Statistical Evidence In Notebook/Wiki Memory

- Stable item ID: `P018-002`
- Title: Add notebook and findings summaries
- Rationale: Notebook/wiki memory should carry statistical result summaries.
- Affected files/modules: `app/notebook_workspace.py`, `tests/test_notebook_workspace.py`
- Implementation steps: Add Markdown statistical evidence block and findings summary line.
- Unit test expectations: Markdown and findings content are tested.
- E2E test expectations: 20-turn regression notebooks contain statistical evidence.
- Demo relevance: Generated notebook Markdown and findings are phase evidence.
- Acceptance criteria: Notebook Markdown and wiki findings render statistical evidence.
- Status: done

## P018-003: Validate, Demo, Status, Commit

- Stable item ID: `P018-003`
- Title: Close Phase 018
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 018 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 018 is locally committed.
- Status: done
