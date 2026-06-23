# Phase 001 Demo: Static Evidence Packet

## Setup

Run from the repository root:

```sh
cd /code
```

Microsoft Agent Framework was installed before the run:

```sh
python3 -m pip install agent-framework
```

## Commands

```sh
python3 -m pytest -q
python3 -m app.main --output-dir app/runs/phase-001-static-evidence-packet
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Unit tests pass.
- CLI writes `experiment_packet.json` and `experiment_packet.md`.
- Packet reports Python and Microsoft Agent Framework runtime metadata.
- Packet profiles both final CSV runtime files.
- E2E script exits neutrally because no e2e suite exists yet.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest -q
.....                                                                    [100%]
```

```text
python3 -m app.main --output-dir app/runs/phase-001-static-evidence-packet
wrote app/runs/phase-001-static-evidence-packet/experiment_packet.json
wrote app/runs/phase-001-static-evidence-packet/experiment_packet.md
```

```text
bash scripts/e2e.sh
no e2e suite detected; nothing to run
```

```text
bash scripts/validate.sh
5 passed in 0.06s
no e2e suite detected; nothing to run
validation passed
```

## Evidence

Generated files:

```text
app/runs/phase-001-static-evidence-packet/experiment_packet.json
app/runs/phase-001-static-evidence-packet/experiment_packet.md
```

Packet summary:

```text
schema_version: phase-001.static-evidence-packet.v1
city_week_rows: 5777
msa_week_rows: 48723
city_week_has_game_rows: 2277
msa_week_has_game_rows: 2542
all_required_columns_present: True
all_required_values_present: True
language: python
framework: Microsoft Agent Framework
package: agent-framework 1.9.0
import_available: True
```

## 20-Turn Regression

Not applicable for Phase 001. This phase does not implement candidate selection, routing, notebooks, telemetry, reports, or memory. The 20-turn gate begins once those orchestration surfaces exist. Phase 001 records this limitation in the packet caveat and status document.

## Video

No video was generated. This is a non-UI CLI/data-artifact phase, and command-output evidence plus generated packet artifacts are the relevant demonstration outputs.

## Known Gaps

- No Microsoft Agent Framework agent is orchestrated yet; the dependency and import metadata are verified.
- No e2e suite exists yet.
- No 20-turn regression exists yet.
- The packet is descriptive and does not make causal or inferential claims.

## Requirement Mapping

- Python package under `app/`: implemented.
- Microsoft Agent Framework runtime dependency: declared in `pyproject.toml`, installed, and verified in runtime metadata.
- Final CSV profiling: implemented in `app.data_profile`.
- Static evidence packet: implemented in `app.evidence_packet`.
- CLI: implemented in `app.main`.
- Tests: implemented under `tests/`.
- Demo evidence: this document and generated packet artifacts.
