# Phase 010 Backlog: Exploratory Statistical Tests

## P010-001: Implement Statistical Test Scaffold

- Stable item ID: `P010-001`
- Title: Add exposed-vs-unexposed comparison runner
- Rationale: The system needs an execution layer for exploratory statistical summaries.
- Affected files/modules: `app/statistical_tests.py`
- Implementation steps: Add result dataclasses, CSV aggregation, outcome comparisons, diagnostics, and caveats.
- Unit test expectations: Positive and not-testable fixtures are tested.
- E2E test expectations: Smoke command writes artifacts.
- Demo relevance: Smoke output is phase evidence.
- Acceptance criteria: Results include counts, means, differences, diagnostics, and caveats.
- Status: done

## P010-002: Add Statistical Smoke Script

- Stable item ID: `P010-002`
- Title: Add repeatable statistical smoke command
- Rationale: Phase 010 needs a local command that proves the statistics layer runs on final files.
- Affected files/modules: `scripts/run_statistical_smoke.py`
- Implementation steps: Run all configured exploratory comparisons and write JSON/Markdown outputs.
- Unit test expectations: Artifact writer is tested.
- E2E test expectations: Command passes on final CSVs.
- Demo relevance: Demo records smoke output.
- Acceptance criteria: JSON and Markdown artifacts are written.
- Status: done

## P010-003: Validate, Demo, Status, Commit

- Stable item ID: `P010-003`
- Title: Close Phase 010
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 010 docs and repository state.
- Implementation steps: Run tests, smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 010 is locally committed.
- Status: done
