# Phase 019: Final Replication Audit

## Phase Goal

Add a machine-readable final audit that verifies the local implementation satisfies the thesis replication checklist against the latest 20-turn run artifacts.

## Requirements

- Check required source files for question forum, governance, statistical execution, Microsoft Agent Framework adapter, reports, notebooks, and data.
- Check the latest 20-turn regression completed all requested turns.
- Check selected candidates carry forum, tournament, reflection, and evolution metadata.
- Check every turn carries statistical evidence.
- Check the business report renders statistical evidence sections.
- Record known limits explicitly.
- Write JSON and Markdown audit artifacts.
- Keep the 20-turn regression and full validation passing.

## Non-Goals

- Claiming causal proof.
- Claiming live model-based debate.
- Cloud deployment.
- Human evaluation.

## Assumptions

- The latest acceptance run is `app/runs/phase-019-replication-audit`.
- Known limits are part of the final status, not failures.
- The final status should be auditable from files alone.

## Affected Layers

- Replication audit
- Compatibility surface
- Tests
- Documentation

## Affected Modules

- `app/replication_audit.py`
- `app/hypothesis_evolution.py`
- `scripts/run_replication_audit.py`
- `tests/test_replication_audit.py`

## Dependency/Library Choices

No new dependency is required.

## Architecture Notes

The audit reads local run artifacts and source-file presence rather than relying on a narrative claim. It writes JSON for tests and Markdown for human review.

## Data/API/Config Changes

- Adds audit artifacts under `app/runs/phase-019-replication-audit/`.
- Adds `app/hypothesis_evolution.py` compatibility alias for thesis wording.

## Demo Requirements

- Run replication audit.
- Run 20-turn regression.
- Rerun replication audit against the latest run directory.
- Record validation output.

## Test Requirements

- Final audit passes against latest run artifacts.
- Validation passes.

## Security/Sandbox Considerations

- Do not read `.env`.
- Do not make external model calls.
- Preserve known limits.

## Risks

- The audit validates local artifacts, not external scientific validity.
- Known limits remain: deterministic governance, observational statistics, deterministic MAF adapter.

## Acceptance Criteria

- Final audit reports `replicated_with_known_limits`.
- 20-turn regression completes with statistical evidence and metadata coverage.
- Audit JSON and Markdown artifacts are written.
- Tests and validation pass.

## Rollback Plan

Revert the Phase 019 commit or remove audit module, compatibility alias, script, tests, artifacts, and docs.
