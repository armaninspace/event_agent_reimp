# Phase 001 Backlog: Static Evidence Packet

## P001-001: Establish Python Project Metadata

- Stable item ID: `P001-001`
- Title: Add Python project metadata
- Rationale: The project needs an explicit Python runtime direction and declared Microsoft Agent Framework dependency.
- Affected files/modules: `pyproject.toml`
- Implementation steps: Add project metadata, runtime dependencies, pytest configuration, and a console script.
- Unit test expectations: `python3 -m pytest -q` discovers tests.
- E2E test expectations: `bash scripts/e2e.sh` exits neutrally until e2e exists.
- Demo relevance: CLI command uses the package entry point module.
- Acceptance criteria: Project metadata exists and declares `agent-framework`.
- Status: done

## P001-002: Implement CSV Data Profiling

- Stable item ID: `P001-002`
- Title: Add final CSV profiling
- Rationale: Evidence packets need auditable source-data summaries.
- Affected files/modules: `app/data_profile.py`, `tests/test_data_profile.py`
- Implementation steps: Read CSV headers and rows, validate required fields, count geographies, weeks, exposure rows, and missing required values.
- Unit test expectations: Fixture CSVs produce deterministic profiles.
- E2E test expectations: Covered by CLI smoke command.
- Demo relevance: Packet output includes data profiles.
- Acceptance criteria: Profiles are deterministic and report missing required fields.
- Status: done

## P001-003: Implement Static Evidence Packet

- Stable item ID: `P001-003`
- Title: Generate JSON and Markdown evidence artifacts
- Rationale: Phase 001 acceptance requires one command writing an evidence packet.
- Affected files/modules: `app/evidence_packet.py`, `app/main.py`, `tests/test_evidence_packet.py`
- Implementation steps: Assemble packet fields, create output directory, write JSON and Markdown artifacts.
- Unit test expectations: Packet shape and artifact writing are tested.
- E2E test expectations: CLI smoke command writes artifacts.
- Demo relevance: Demo cites generated artifact paths.
- Acceptance criteria: JSON and Markdown packet files are created and include required sections.
- Status: done

## P001-004: Report Microsoft Agent Framework Runtime Metadata

- Stable item ID: `P001-004`
- Title: Add runtime metadata check
- Rationale: The project must verify it is Python-based and configured for Microsoft Agent Framework.
- Affected files/modules: `app/agent_runtime.py`, `tests/test_agent_runtime.py`
- Implementation steps: Report Python version, package version, import name, and availability without making external calls.
- Unit test expectations: Metadata shape is tested and does not require a live model.
- E2E test expectations: CLI packet includes runtime metadata.
- Demo relevance: Demo confirms `agent-framework` availability.
- Acceptance criteria: Runtime metadata reports `agent-framework` version when installed.
- Status: done

## P001-005: Validate, Demo, Status, Commit

- Stable item ID: `P001-005`
- Title: Run validation and close the phase
- Rationale: Phase loop requires evidence, status, and a local commit.
- Affected files/modules: `docs/demos/phase-001-static-evidence-packet-demo.md`, `docs/deliverables-status/phase-001-static-evidence-packet-status.md`
- Implementation steps: Run tests, e2e, validation, record demo/status, commit locally.
- Unit test expectations: `python3 -m pytest -q` passes.
- E2E test expectations: `bash scripts/e2e.sh` exits successfully or neutrally.
- Demo relevance: Records CLI output and generated files.
- Acceptance criteria: Phase docs contain evidence and commit hash is reported after commit.
- Status: done
