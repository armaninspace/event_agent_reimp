# Phase 020 Demo: Data Snapshot Hashes

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_data_snapshot.py tests/test_phase_regression.py tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-020-data-snapshot-hashes --turns 20
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-020-data-snapshot-hashes --output-dir app/runs/phase-020-data-snapshot-hashes
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Snapshot/regression/audit tests pass.
- 20-turn regression reports `data_snapshot_complete=True`.
- Audit reports `data_snapshot_complete=True`.
- Audit records a combined data snapshot SHA-256.
- Validation passes.

## Observed Behavior

Commands completed successfully.

```text
python3 -m pytest tests/test_data_snapshot.py tests/test_phase_regression.py tests/test_replication_audit.py -q
.....                                                                    [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-020-data-snapshot-hashes --turns 20
wrote app/runs/phase-020-data-snapshot-hashes/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
turns_have_statistical_evidence=True
data_snapshot_complete=True
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

```text
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-020-data-snapshot-hashes --output-dir app/runs/phase-020-data-snapshot-hashes
wrote app/runs/phase-020-data-snapshot-hashes/replication_audit.json
wrote app/runs/phase-020-data-snapshot-hashes/replication_audit.md
final_status=replicated_with_known_limits
completed_twenty_turns=True
selected_candidates_have_required_metadata=True
turns_have_statistical_evidence=True
business_report_statistical_sections=20
```

## Evidence

Generated artifacts:

```text
app/runs/phase-020-data-snapshot-hashes/phase_regression_summary.json
app/runs/phase-020-data-snapshot-hashes/replication_audit.json
app/runs/phase-020-data-snapshot-hashes/replication_audit.md
```

Data snapshot summary:

```text
combined_sha256: eb78bb3a0b2f0116c3f03349f4b077781419789f22fb4e2df5de22d58df3c3c1
data/reference/joined_city_week_game_economic.csv rows=5777 bytes=3037004 sha256=3e7cd9d5915d0e2a3e33ffb3dda12211fc1b707c745a85866c3f7319b073a083
data/reference/joined_msa_week_game_economic.csv rows=48723 bytes=16997114 sha256=211726051f58d215314a2a9f39dd7028a3d5cc3e97db7c326f8215e5adbaa6da
```

Audit summary:

```text
final_status: replicated_with_known_limits
data_snapshot_complete: True
data_snapshot_combined_sha256: eb78bb3a0b2f0116c3f03349f4b077781419789f22fb4e2df5de22d58df3c3c1
business_report_statistical_sections: 20
```

## 20-Turn Regression

Implemented and passed after adding data snapshot hashes.

## Video

No video was generated. This is a reproducibility/audit phase; JSON/Markdown audit artifacts and regression summary are the relevant demo outputs.

## Known Gaps

- Hashes cover final joined reference CSVs, not every upstream source file.
- Hashes prove byte identity, not external data correctness.

## Requirement Mapping

- Snapshot helper: `app/data_snapshot.py`
- Regression integration: `app/phase_regression.py`
- Audit integration: `app/replication_audit.py`
- Tests: `tests/test_data_snapshot.py`, `tests/test_phase_regression.py`, `tests/test_replication_audit.py`
