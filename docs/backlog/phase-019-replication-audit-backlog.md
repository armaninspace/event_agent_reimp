# Phase 019 Backlog: Final Replication Audit

## P019-001: Implement Replication Audit

- Stable item ID: `P019-001`
- Title: Add final thesis replication audit
- Rationale: Completion should be proven by artifacts, not only a narrative response.
- Affected files/modules: `app/replication_audit.py`, `scripts/run_replication_audit.py`
- Implementation steps: Check required files, latest regression summary, session metadata counts, statistical evidence, business report sections, and known limits.
- Unit test expectations: Audit passes against latest run artifacts.
- E2E test expectations: Audit command writes JSON and Markdown artifacts.
- Demo relevance: Audit artifacts are final replication evidence.
- Acceptance criteria: Audit reports `replicated_with_known_limits`.
- Status: done

## P019-002: Add Thesis Compatibility Alias

- Stable item ID: `P019-002`
- Title: Add `app/hypothesis_evolution.py`
- Rationale: The thesis text names `hypothesis_evolution.py`; the implementation used `question_evolution.py`.
- Affected files/modules: `app/hypothesis_evolution.py`
- Implementation steps: Re-export `evolve_candidates`.
- Unit test expectations: Covered indirectly by audit required-file checks.
- E2E test expectations: Audit required source files are present.
- Demo relevance: Audit records source-file coverage.
- Acceptance criteria: Compatibility module exists.
- Status: done

## P019-003: Validate, Demo, Status, Commit

- Stable item ID: `P019-003`
- Title: Close Phase 019
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 019 docs and repository state.
- Implementation steps: Run audit, 20-turn regression, audit latest run, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 019 is locally committed.
- Status: done
