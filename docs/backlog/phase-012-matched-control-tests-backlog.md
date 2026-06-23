# Phase 012 Backlog: Matched Control Tests

## P012-001: Implement Matched Tests

- Stable item ID: `P012-001`
- Title: Add same-week/same-block matched comparisons
- Rationale: The statistics layer needs matched-control scaffolding beyond raw exposed-vs-unexposed summaries.
- Affected files/modules: `app/matched_tests.py`
- Implementation steps: Group controls by week/block, compare exposed rows to control means, report diagnostics and caveats.
- Unit test expectations: Matched and not-testable fixtures are tested.
- E2E test expectations: Smoke command passes on final CSVs.
- Demo relevance: Matched smoke output is phase evidence.
- Acceptance criteria: Results include matched counts and caveats.
- Status: done

## P012-002: Add Matched Smoke Script

- Stable item ID: `P012-002`
- Title: Add repeatable matched smoke command
- Rationale: Phase 012 needs a command proving matched tests run on final files.
- Affected files/modules: `scripts/run_matched_smoke.py`
- Implementation steps: Run configured matched comparisons and write JSON/Markdown artifacts.
- Unit test expectations: Artifact writer is tested.
- E2E test expectations: Command passes.
- Demo relevance: Demo records smoke output.
- Acceptance criteria: JSON and Markdown artifacts are written.
- Status: done

## P012-003: Validate, Demo, Status, Commit

- Stable item ID: `P012-003`
- Title: Close Phase 012
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 012 docs and repository state.
- Implementation steps: Run tests, matched smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 012 is locally committed.
- Status: done
