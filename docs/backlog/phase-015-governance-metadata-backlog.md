# Phase 015 Backlog: Governance Metadata

## P015-001: Implement Tournament Governance

- Stable item ID: `P015-001`
- Title: Add deterministic pairwise tournament
- Rationale: Candidate selection needs inspectable debate/ranking metadata.
- Affected files/modules: `app/question_tournament.py`
- Implementation steps: Compare candidates pairwise, score component dimensions, record rank/wins/losses/transcripts.
- Unit test expectations: Tournament ranks candidates and records transcripts.
- E2E test expectations: Governance smoke reports tournament metadata.
- Demo relevance: Smoke and regression artifacts show selected tournament ranks.
- Acceptance criteria: Selected candidates carry tournament metadata.
- Status: done

## P015-002: Implement Reflection And Evolution

- Stable item ID: `P015-002`
- Title: Add deterministic reviewer and evolution metadata
- Rationale: Candidate governance needs critique and continuity between turns.
- Affected files/modules: `app/question_reflection.py`, `app/question_evolution.py`
- Implementation steps: Add answerability review fields and evolution action metadata.
- Unit test expectations: Reflection and evolution functions are tested.
- E2E test expectations: Governance smoke reports reflection/evolution metadata.
- Demo relevance: Regression artifacts show selected metadata coverage.
- Acceptance criteria: Selected candidates carry reflection and evolution metadata.
- Status: done

## P015-003: Integrate Governance Into Loop And Regression

- Stable item ID: `P015-003`
- Title: Make governance metadata required in 20-turn runs
- Rationale: The phase is only complete if selected candidates carry metadata through the full workflow.
- Affected files/modules: `app/friends_loop.py`, `app/phase_regression.py`, `tests/test_friends_loop.py`
- Implementation steps: Add governance telemetry, tournament-based selection, not-answerable filtering, and regression metadata checks.
- Unit test expectations: Friends-loop selected candidates include metadata.
- E2E test expectations: 20-turn regression passes with metadata coverage true.
- Demo relevance: Phase regression summary is acceptance evidence.
- Acceptance criteria: 20-turn regression completes with all metadata families present.
- Status: done

## P015-004: Validate, Demo, Status, Commit

- Stable item ID: `P015-004`
- Title: Close Phase 015
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 015 docs and repository state.
- Implementation steps: Run tests, governance smoke, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 015 is locally committed.
- Status: done
