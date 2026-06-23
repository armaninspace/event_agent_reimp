# Phase 004 Backlog: 20-Turn Regression Gate

## P004-001: Implement Regression Summary Service

- Stable item ID: `P004-001`
- Title: Add phase regression summary generation
- Rationale: The project needs an enforceable 20-turn gate before orchestration expands.
- Affected files/modules: `app/phase_regression.py`
- Implementation steps: Run friends loop, inspect artifacts, compute summary fields, and write JSON.
- Unit test expectations: Summary fields are tested with fixture reference data.
- E2E test expectations: CLI runs 20 turns.
- Demo relevance: Summary JSON is primary evidence.
- Acceptance criteria: Summary reports requested/completed turns and artifact checks.
- Status: done

## P004-002: Add Regression CLI

- Stable item ID: `P004-002`
- Title: Add `scripts/run_phase_regression.py`
- Rationale: Docs already specify this command contract.
- Affected files/modules: `scripts/run_phase_regression.py`
- Implementation steps: Add phase ID, turns, reference dir, and runs dir arguments with default `--turns 20`.
- Unit test expectations: Default turn count is testable through parser.
- E2E test expectations: Command writes a summary.
- Demo relevance: Demo runs this command.
- Acceptance criteria: CLI default turn count is 20.
- Status: done

## P004-003: Add Regression Tests

- Stable item ID: `P004-003`
- Title: Test regression gate behavior
- Rationale: The gate should fail loudly if summary contracts drift.
- Affected files/modules: `tests/test_phase_regression.py`
- Implementation steps: Add fixture files, run regression with small counts in unit tests, verify default parser turns, and artifact checks.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: Covered by validation plus demo command.
- Demo relevance: Test output is recorded.
- Acceptance criteria: Tests cover summary shape and parser default.
- Status: done

## P004-004: Validate, Demo, Status, Commit

- Stable item ID: `P004-004`
- Title: Close Phase 004
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 004 docs and repository state.
- Implementation steps: Run 20-turn regression, tests, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 004 is locally committed.
- Status: done
