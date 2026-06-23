# Phase 011 Backlog: Semantic SQL Layer

## P011-001: Add DuckDB Semantic Layer

- Stable item ID: `P011-001`
- Title: Implement governed DuckDB query service
- Rationale: Agents and notebooks need local SQL over whitelisted final data views.
- Affected files/modules: `app/semantic_layer.py`
- Implementation steps: Create in-memory DuckDB views, validate SELECT-only SQL, enforce whitelist and row limit, return telemetry.
- Unit test expectations: Query guardrails are tested.
- E2E test expectations: Semantic smoke command passes.
- Demo relevance: Smoke artifacts are phase evidence.
- Acceptance criteria: SELECT-only whitelisted queries execute with telemetry.
- Status: done

## P011-002: Add Semantic Smoke Script

- Stable item ID: `P011-002`
- Title: Add repeatable semantic smoke command
- Rationale: Phase 011 needs a command that proves the semantic layer works on final CSVs.
- Affected files/modules: `scripts/run_semantic_smoke.py`
- Implementation steps: Run representative city/MSA queries and write JSON/Markdown outputs.
- Unit test expectations: Covered by semantic layer tests.
- E2E test expectations: Command passes.
- Demo relevance: Demo records smoke output.
- Acceptance criteria: JSON and Markdown artifacts are written.
- Status: done

## P011-003: Validate, Demo, Status, Commit

- Stable item ID: `P011-003`
- Title: Close Phase 011
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 011 docs and repository state.
- Implementation steps: Run tests, semantic smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 011 is locally committed.
- Status: done
