# Phase 008: Reports And Playback

## Phase Goal

Add static business evidence report and playback UI artifacts for every friends-loop run, then enforce them in the 20-turn regression gate.

## Requirements

- Generate `business_evidence_report.html`.
- Generate `ui/index.html`.
- Generate `phase_regression_summary.json` already handled by regression.
- Keep report stakeholder-readable and caveat-preserving.
- Keep playback UI static and able to render embedded telemetry without a dev server.
- Escape HTML and embedded JSON safely.
- Update regression gate to require business report and playback UI.
- Add tests for artifact creation and HTML escaping.

## Non-Goals

- Rich frontend framework.
- Video recording.
- Statistical claims.
- Live agent calls.

## Assumptions

- Static HTML is sufficient for Phase 008.
- Reports should distinguish exploratory/scaffolded evidence from validated findings.
- Playback can embed telemetry JSON directly for portability.

## Affected Layers

- Evidence/report layer
- Playback/observability layer
- Regression validation
- Tests

## Affected Modules

- `app/reporting.py`
- `app/friends_loop.py`
- `app/phase_regression.py`
- `tests/test_reporting.py`
- `tests/test_friends_loop.py`
- `tests/test_phase_regression.py`

## Dependency/Library Choices

No new dependencies are required. The implementation uses Python standard library `html` and `json`.

## Architecture Notes

Report generation is a separate module called by `DataAgent`. The business report is stakeholder-readable and caveat-forward. The playback UI embeds telemetry JSON and renders event rows in the browser.

## Data/API/Config Changes

- Friends-loop runs now write `business_evidence_report.html`.
- Friends-loop runs now write `ui/index.html`.
- Regression summary checks those artifacts.

## Demo Requirements

- Run a 20-turn regression.
- Show report/playback artifact paths.
- Record summary checks.

## Test Requirements

- Tests verify report/playback files are written.
- Tests verify unsafe HTML is escaped in business report.
- Tests verify regression requires report/playback artifacts.
- Validation passes.

## Security/Sandbox Considerations

- Escape public question and rationale text.
- Escape JSON before embedding in `<script>`.
- Do not use a dev server.
- Do not make network calls.

## Risks

- Static report is basic and not yet a polished product surface.
- Embedded telemetry can grow large in future runs.
- Report is descriptive; it must not overclaim statistical evidence.

## Acceptance Criteria

- 20-turn regression writes and requires business report and playback UI.
- Tests and validation pass.
- Reports preserve caveats and do not overclaim.

## Rollback Plan

Revert the Phase 008 commit or remove report/playback integration, artifacts, tests, and docs.
