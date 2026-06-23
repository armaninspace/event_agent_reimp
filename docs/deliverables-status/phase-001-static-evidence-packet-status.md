# Phase 001 Deliverables Status: Static Evidence Packet

## Completed Items

- Added Python project metadata in `pyproject.toml`.
- Declared Microsoft Agent Framework dependency as `agent-framework>=1.9.0,<2.0.0`.
- Installed and verified `agent-framework 1.9.0`.
- Added Python package under `app/`.
- Implemented final CSV profiling for city-week and MSA-week runtime files.
- Implemented deterministic static evidence packet generation.
- Implemented CLI entry point with `python3 -m app.main`.
- Added unit tests for runtime metadata, data profiling, packet shape, and artifact writing.
- Generated Phase 001 packet artifacts.

## Blocked/Deferred Items

- 20-turn regression deferred because candidate selection, routing, notebooks, telemetry, reports, and memory are not implemented yet.
- Microsoft Agent Framework orchestration deferred to a later phase; Phase 001 verifies dependency and import metadata only.
- E2E suite deferred until there is a workflow boundary worth testing end to end.

## Files Changed

- `pyproject.toml`
- `app/__init__.py`
- `app/agent_runtime.py`
- `app/data_profile.py`
- `app/evidence_packet.py`
- `app/main.py`
- `tests/test_agent_runtime.py`
- `tests/test_data_profile.py`
- `tests/test_evidence_packet.py`
- `app/runs/phase-001-static-evidence-packet/experiment_packet.json`
- `app/runs/phase-001-static-evidence-packet/experiment_packet.md`
- `.env.example`
- `data/reference/joined_city_week_game_economic.csv`
- `data/reference/joined_msa_week_game_economic.csv`
- `docs/data-card-final-runtime-files.md`
- `docs/reimplementation-notes.md`
- `docs/installed-software.md`
- `docs/phases/phase-001-static-evidence-packet-engineering-requirements.md`
- `docs/backlog/phase-001-static-evidence-packet-backlog.md`
- `docs/demos/phase-001-static-evidence-packet-demo.md`
- `docs/deliverables-status/phase-001-static-evidence-packet-status.md`

## Dependencies Installed

| Tool/package | Version | Classification | Reason |
| --- | --- | --- | --- |
| agent-framework | 1.9.0 | runtime | Microsoft Agent Framework runtime for Python agent phases |

See `docs/installed-software.md`.

## Tests Run

- `python3 -m pytest -q`: passed, 5 tests.
- `python3 -m app.main --output-dir app/runs/phase-001-static-evidence-packet`: passed.
- `bash scripts/e2e.sh`: passed neutrally; no e2e suite detected.
- `bash scripts/validate.sh`: passed, including pytest.

## Demo Evidence

See `docs/demos/phase-001-static-evidence-packet-demo.md`.

Generated artifacts:

- `app/runs/phase-001-static-evidence-packet/experiment_packet.json`
- `app/runs/phase-001-static-evidence-packet/experiment_packet.md`

## Video Path Or Rationale

No video was generated. Phase 001 is a non-UI CLI/data-artifact phase, and command-output evidence plus packet artifacts are the appropriate demo evidence.

## Acceptance Criteria Status

- CLI writes JSON and Markdown packet artifacts: passed.
- Packet includes question, hypothesis, design, result, caveat, data profile, runtime metadata, and audit log: passed.
- Runtime metadata reports Microsoft Agent Framework package/import status: passed.
- Unit tests pass: passed.
- Validation passes: passed.
- 20-turn non-applicability rationale documented: passed.

## Risks

- `agent-framework` installs a broad bundle of integrations. Future phases may choose narrower framework packages if startup time or dependency surface becomes a problem.
- The static packet is only a readiness artifact; it must not be treated as validated statistical evidence.
- Later phases need explicit e2e and 20-turn regression helpers.

## Next Phase

Phase 002 should implement reference event data loading as reusable services and add the first workflow smoke boundary. If orchestration begins in that phase, define the 20-turn regression helper before accepting the phase.

## Commit Hash

Pending until local commit completes. The final response will report the created commit hash.

## Label/Tag

No tag applied.
