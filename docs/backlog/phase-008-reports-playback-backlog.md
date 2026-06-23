# Phase 008 Backlog: Reports And Playback

## P008-001: Implement Static Report Renderers

- Stable item ID: `P008-001`
- Title: Add business report and playback UI rendering
- Rationale: Every run should be inspectable by humans.
- Affected files/modules: `app/reporting.py`
- Implementation steps: Render escaped business HTML and embedded telemetry playback HTML.
- Unit test expectations: HTML escaping and generated content are tested.
- E2E test expectations: 20-turn regression writes both files.
- Demo relevance: HTML paths are phase evidence.
- Acceptance criteria: Static HTML files are created without a dev server.
- Status: done

## P008-002: Integrate Reports Into DataAgent

- Stable item ID: `P008-002`
- Title: Write report artifacts during friends-loop runs
- Rationale: Report artifacts must be produced for every run.
- Affected files/modules: `app/friends_loop.py`
- Implementation steps: Add report and playback file writes to `DataAgent.write_artifacts`.
- Unit test expectations: Friends-loop artifact paths include report/playback files.
- E2E test expectations: Smoke/regression commands write report/playback.
- Demo relevance: Demo cites artifact paths.
- Acceptance criteria: `business_evidence_report` and `playback_ui` artifact paths exist.
- Status: done

## P008-003: Tighten Regression Gate

- Stable item ID: `P008-003`
- Title: Require report/playback artifacts
- Rationale: Newly added artifacts should be enforced by the 20-turn gate.
- Affected files/modules: `app/phase_regression.py`
- Implementation steps: Add artifact checks for business report and playback UI.
- Unit test expectations: Regression summary reports both checks true.
- E2E test expectations: 20-turn regression passes.
- Demo relevance: Summary checks are recorded.
- Acceptance criteria: Regression requires business and playback HTML.
- Status: done

## P008-004: Validate, Demo, Status, Commit

- Stable item ID: `P008-004`
- Title: Close Phase 008
- Rationale: Phase protocol requires validation, demo, status, and local commit.
- Affected files/modules: Phase 008 docs and repository state.
- Implementation steps: Run tests, 20-turn regression, e2e, validation, document evidence, and commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Phase demo is updated.
- Acceptance criteria: Phase 008 is locally committed.
- Status: done
