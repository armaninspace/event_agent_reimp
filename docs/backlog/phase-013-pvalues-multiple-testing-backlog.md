# Phase 013 Backlog: P-Values And Multiple Testing

## P013-001: Implement P-Value And Correction Service

- Stable item ID: `P013-001`
- Title: Add statistical p-values and BH correction
- Rationale: The evidence layer needs inferential metadata and multiple-testing discipline.
- Affected files/modules: `app/multiple_testing.py`
- Implementation steps: Add p-value calculations, BH correction, combined smoke report, caveats.
- Unit test expectations: P-value and adjustment functions are tested.
- E2E test expectations: Correction smoke command passes.
- Demo relevance: Correction artifacts are phase evidence.
- Acceptance criteria: Raw and adjusted p-values are present.
- Status: done

## P013-002: Add Correction Smoke Script

- Stable item ID: `P013-002`
- Title: Add repeatable correction smoke command
- Rationale: Phase 013 needs a local command proving corrections run on final files.
- Affected files/modules: `scripts/run_correction_smoke.py`
- Implementation steps: Run correction report and write JSON/Markdown artifacts.
- Unit test expectations: Artifact writer is tested.
- E2E test expectations: Command passes.
- Demo relevance: Demo records smoke output.
- Acceptance criteria: JSON and Markdown artifacts are written.
- Status: done

## P013-003: Validate, Demo, Status, Commit

- Stable item ID: `P013-003`
- Title: Close Phase 013
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 013 docs and repository state.
- Implementation steps: Run tests, correction smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 013 is locally committed.
- Status: done
