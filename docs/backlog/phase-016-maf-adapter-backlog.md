# Phase 016 Backlog: Microsoft Agent Framework Adapter

## P016-001: Implement Deterministic MAF Adapter

- Stable item ID: `P016-001`
- Title: Add Microsoft Agent Framework workflow adapter
- Rationale: The project must demonstrate real Python Microsoft Agent Framework usage, not only package metadata.
- Affected files/modules: `app/maf_orchestration.py`
- Implementation steps: Build a `WorkflowBuilder`/`FunctionExecutor` workflow, run it deterministically, and return adapter evidence.
- Unit test expectations: Adapter produces deterministic output and reports no model calls.
- E2E test expectations: Adapter smoke command passes.
- Demo relevance: Smoke artifacts prove framework orchestration.
- Acceptance criteria: Adapter uses installed `agent-framework` and runs locally.
- Status: done

## P016-002: Add Smoke Command And Tests

- Stable item ID: `P016-002`
- Title: Add repeatable MAF adapter smoke
- Rationale: Phase 016 needs reproducible command-output evidence.
- Affected files/modules: `scripts/run_maf_adapter_smoke.py`, `tests/test_maf_orchestration.py`
- Implementation steps: Write JSON/Markdown artifacts and test artifact writing.
- Unit test expectations: Smoke writer is tested.
- E2E test expectations: Smoke command passes.
- Demo relevance: Demo records smoke output.
- Acceptance criteria: JSON and Markdown adapter artifacts are written.
- Status: done

## P016-003: Validate, Demo, Status, Commit

- Stable item ID: `P016-003`
- Title: Close Phase 016
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 016 docs and repository state.
- Implementation steps: Run tests, MAF smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 016 is locally committed.
- Status: done
