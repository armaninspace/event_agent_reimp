# Phase 017 Backlog: Governed Statistical Execution

## P017-001: Implement Statistical Evidence Mapping

- Stable item ID: `P017-001`
- Title: Map governed candidates to corrected results
- Rationale: Selected public questions need attached statistical execution evidence.
- Affected files/modules: `app/statistical_execution.py`
- Implementation steps: Build reusable execution report, filter results by semantic slot, return candidate-scoped evidence.
- Unit test expectations: Result filtering is tested.
- E2E test expectations: Statistical execution smoke passes.
- Demo relevance: Smoke artifacts show corrected result count and method.
- Acceptance criteria: Candidate evidence includes result IDs and caveats.
- Status: done

## P017-002: Attach Evidence To Loop And Regression

- Stable item ID: `P017-002`
- Title: Persist statistical evidence on every turn
- Rationale: The 20-turn workflow must prove selected questions carry execution artifacts.
- Affected files/modules: `app/friends_loop.py`, `app/phase_regression.py`, `scripts/run_phase_regression.py`
- Implementation steps: Compute report once per run, attach per-turn evidence, add telemetry, add regression flag.
- Unit test expectations: Friends-loop and regression tests assert evidence coverage.
- E2E test expectations: 20-turn regression reports `turns_have_statistical_evidence=True`.
- Demo relevance: Regression summary is acceptance evidence.
- Acceptance criteria: Every turn carries statistical evidence.
- Status: done

## P017-003: Validate, Demo, Status, Commit

- Stable item ID: `P017-003`
- Title: Close Phase 017
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 017 docs and repository state.
- Implementation steps: Run tests, smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 017 is locally committed.
- Status: done
