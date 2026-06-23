# Phase 023 Deliverables Status: Evolution Variants

## Completed Items

- Added deterministic `evolved_question` values.
- Added `parent_question_id`.
- Added `child_question_id`.
- Added variant text for `split`, `combine`, `strengthen`, and `carry_forward`.
- Required evolution variant metadata in phase regression.
- Added `selected_evolution_variant_count` to replication audit.
- Updated audit default to Phase 023.
- Added governance, friends-loop, and audit tests.
- Ran a 20-turn regression after adding evolution variants.
- Refreshed the replication audit against the Phase 023 run.

## Blocked/Deferred Items

- Live model-generated rewrites remain deferred.
- Graph database storage for parent/child hypotheses remains deferred.

## Files Changed

- `app/question_evolution.py`
- `app/phase_regression.py`
- `app/replication_audit.py`
- `scripts/run_replication_audit.py`
- `tests/test_question_governance.py`
- `tests/test_friends_loop.py`
- `tests/test_replication_audit.py`
- `app/runs/phase-023-evolution-variants/friends-question-loop/friends_loop_session.json`
- `app/runs/phase-023-evolution-variants/phase_regression_summary.json`
- `app/runs/phase-023-evolution-variants/replication_audit.json`
- `app/runs/phase-023-evolution-variants/replication_audit.md`
- `docs/phases/phase-023-evolution-variants-engineering-requirements.md`
- `docs/backlog/phase-023-evolution-variants-backlog.md`
- `docs/demos/phase-023-evolution-variants-demo.md`
- `docs/deliverables-status/phase-023-evolution-variants-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 023.

## Tests Run

- `python3 -m pytest tests/test_question_governance.py tests/test_friends_loop.py tests/test_phase_regression.py -q`: passed, 10 tests.
- `python3 -m pytest tests/test_replication_audit.py -q`: passed, 1 test.
- `python3 scripts/run_phase_regression.py --phase-id phase-023-evolution-variants --turns 20`: passed.
- `python3 scripts/run_replication_audit.py --run-dir app/runs/phase-023-evolution-variants --output-dir app/runs/phase-023-evolution-variants`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-023-evolution-variants-demo.md`.

Generated artifacts:

- `app/runs/phase-023-evolution-variants/friends-question-loop/friends_loop_session.json`
- `app/runs/phase-023-evolution-variants/phase_regression_summary.json`
- `app/runs/phase-023-evolution-variants/replication_audit.json`

## Video Path Or Rationale

No video was generated. Phase 023 is a governance metadata phase, and JSON regression/audit artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- 20/20 selected candidates carry evolution variants: passed.
- Audit reports `selected_evolution_variant_count=20`: passed.
- 20-turn regression passes: passed.
- Tests and validation pass: passed.

## Risks

- Deterministic variants are less expressive than model-generated variants.
- Parent/child IDs are simple stable identifiers, not a graph store.

## Next Phase

Reassess remaining known limits. Remaining items are mostly product expansions: live debate, stronger causal designs, and provider-backed MAF agents.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
