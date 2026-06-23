# Phase 015 Deliverables Status: Governance Metadata

## Completed Items

- Added `app/question_tournament.py`.
- Added deterministic pairwise tournament scoring.
- Added tournament rank, wins, losses, component scores, and transcripts.
- Added `app/question_reflection.py`.
- Added reflection metadata for misleading risk, weakening evidence, answerability, and status.
- Added `app/question_evolution.py`.
- Added evolution actions for `split`, `combine`, `strengthen`, and `carry_forward`.
- Integrated governance metadata into selected and rejected candidates.
- Added tournament-based selection with not-answerable filtering.
- Added governance telemetry events.
- Expanded phase regression selected-candidate metadata checks to require forum, tournament, reflection, and evolution.
- Added `scripts/run_governance_smoke.py`.
- Ran a 20-turn regression after adding governance metadata.

## Blocked/Deferred Items

- Microsoft Agent Framework orchestration adapter remains deferred.
- Statistical execution is not yet invoked directly from selected governed hypotheses.
- Literature-grounded novelty and live model debate remain deferred.

## Files Changed

- `app/question_tournament.py`
- `app/question_reflection.py`
- `app/question_evolution.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `scripts/run_governance_smoke.py`
- `tests/test_question_governance.py`
- `tests/test_friends_loop.py`
- `app/runs/phase-015-governance-metadata/governance_smoke.json`
- `app/runs/phase-015-governance-metadata/governance_smoke.md`
- `app/runs/phase-015-governance-metadata/phase_regression_summary.json`
- `app/runs/phase-015-governance-metadata/friends-question-loop/`
- `app/runs/phase-015-governance-metadata/friends-question-loop-smoke/`
- `app/runs/phase-015-governance-metadata/notebooks/`
- `docs/phases/phase-015-governance-metadata-engineering-requirements.md`
- `docs/backlog/phase-015-governance-metadata-backlog.md`
- `docs/demos/phase-015-governance-metadata-demo.md`
- `docs/deliverables-status/phase-015-governance-metadata-status.md`

## Dependencies Installed

No new dependencies were installed during Phase 015.

## Tests Run

- `python3 -m pytest tests/test_question_governance.py tests/test_friends_loop.py tests/test_phase_regression.py -q`: passed, 10 tests.
- `python3 scripts/run_governance_smoke.py --output-dir app/runs/phase-015-governance-metadata --turns 3`: passed.
- `python3 scripts/run_phase_regression.py --phase-id phase-015-governance-metadata --turns 20`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-015-governance-metadata-demo.md`.

Generated artifacts:

- `app/runs/phase-015-governance-metadata/governance_smoke.json`
- `app/runs/phase-015-governance-metadata/governance_smoke.md`
- `app/runs/phase-015-governance-metadata/phase_regression_summary.json`

## Video Path Or Rationale

No video was generated. Phase 015 is a non-UI governance phase, and command-output evidence plus generated artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- Selected candidates carry tournament, reflection, and evolution metadata: passed.
- Deterministic transcripts are stored: passed.
- Not-answerable candidates are filtered from selection: passed.
- Final 20-turn run completes with all metadata families present: passed.
- Tests and validation pass: passed.

## Risks

- Governance is deterministic and heuristic, not a substitute for human or model review.
- Evolution metadata does not yet rewrite source forum records.

## Next Phase

Phase 016 should add an explicit Microsoft Agent Framework orchestration adapter while preserving the deterministic local regression behavior.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
