# Phase 023 Backlog: Evolution Variants

## P023-001: Add Deterministic Evolved Questions

- Stable item ID: `P023-001`
- Title: Add evolved question variants
- Rationale: Evolution should produce concrete revised questions, not only action labels.
- Affected files/modules: `app/question_evolution.py`, `tests/test_question_governance.py`
- Implementation steps: Add parent/child IDs and evolved question text for each action.
- Unit test expectations: Evolution test asserts IDs and rewritten text.
- E2E test expectations: 20-turn selected candidates carry variants.
- Demo relevance: Session JSON is phase evidence.
- Acceptance criteria: Evolution metadata includes concrete variant fields.
- Status: done

## P023-002: Require Variant Coverage In Regression And Audit

- Stable item ID: `P023-002`
- Title: Make evolution variants audit-visible
- Rationale: The remediation should be enforced by regression and final audit.
- Affected files/modules: `app/phase_regression.py`, `app/replication_audit.py`, tests.
- Implementation steps: Require variant fields in selected metadata and count variants in audit.
- Unit test expectations: Friends-loop and audit tests assert variant coverage.
- E2E test expectations: Audit against Phase 023 run reports 20 variants.
- Demo relevance: Audit JSON records variant coverage.
- Acceptance criteria: Audit reports `selected_evolution_variant_count=20`.
- Status: done

## P023-003: Validate, Demo, Status, Commit

- Stable item ID: `P023-003`
- Title: Close Phase 023
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 023 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, audit, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 023 is locally committed.
- Status: done
