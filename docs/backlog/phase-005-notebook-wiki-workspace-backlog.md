# Phase 005 Backlog: Notebook And Wiki Workspace

## P005-001: Implement Workspace Writer

- Stable item ID: `P005-001`
- Title: Add notebook/wiki workspace module
- Rationale: Loop memory needs durable append-oriented files.
- Affected files/modules: `app/notebook_workspace.py`
- Implementation steps: Add wiki initialization, append functions, per-turn notebook JSON, and Markdown export writing.
- Unit test expectations: Workspace files and per-turn artifacts are tested.
- E2E test expectations: 20-turn regression writes notebooks.
- Demo relevance: Workspace artifacts are phase evidence.
- Acceptance criteria: Required wiki files and turn artifacts are created.
- Status: done

## P005-002: Integrate Workspace Into Friends Loop

- Stable item ID: `P005-002`
- Title: Write notebooks and wiki updates during loop turns
- Rationale: Each turn should leave durable memory artifacts.
- Affected files/modules: `app/friends_loop.py`
- Implementation steps: Add `notebook_dir` argument, write turn artifacts, emit `notebook.created` and `wiki.updated` telemetry events.
- Unit test expectations: Friends-loop tests verify workspace artifacts.
- E2E test expectations: Smoke/regression commands write workspace files.
- Demo relevance: Telemetry and artifact paths show memory updates.
- Acceptance criteria: Each turn writes notebook and Markdown export.
- Status: done

## P005-003: Tighten Regression Gate

- Stable item ID: `P005-003`
- Title: Require notebook workspace in regression summary
- Rationale: Added surfaces must become part of the 20-turn gate.
- Affected files/modules: `app/phase_regression.py`, `tests/test_phase_regression.py`
- Implementation steps: Add notebook workspace checks and pass notebook dir to the loop.
- Unit test expectations: Summary reports notebook workspace present.
- E2E test expectations: 20-turn regression passes.
- Demo relevance: Phase demo records summary fields.
- Acceptance criteria: Regression summary requires notebook workspace.
- Status: done

## P005-004: Validate, Demo, Status, Commit

- Stable item ID: `P005-004`
- Title: Close Phase 005
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 005 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 005 is locally committed.
- Status: done
