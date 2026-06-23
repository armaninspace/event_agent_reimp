# Phase 019 Demo: Final Replication Audit

## Setup

Run from the repository root:

```sh
cd /code
```

## Commands

```sh
python3 -m pytest tests/test_replication_audit.py -q
python3 scripts/run_phase_regression.py --phase-id phase-019-replication-audit --turns 20
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-019-replication-audit --output-dir app/runs/phase-019-replication-audit
bash scripts/e2e.sh
bash scripts/validate.sh
```

## Expected Behavior

- Replication audit test passes.
- 20-turn regression passes.
- Audit command writes JSON and Markdown artifacts.
- Audit reports `replicated_with_known_limits`.
- Audit confirms metadata, statistical evidence, report, and notebook coverage.
- Validation passes.

## Observed Behavior

All commands completed successfully.

```text
python3 -m pytest tests/test_replication_audit.py -q
.                                                                        [100%]
```

```text
python3 scripts/run_phase_regression.py --phase-id phase-019-replication-audit --turns 20
wrote app/runs/phase-019-replication-audit/phase_regression_summary.json
requested_turns=20
completed_workflows=20
stopped_early=False
workflow_task_statistical_misroutes=0
turns_have_statistical_evidence=True
current_required_artifacts_exist=True
notebook_workspace_present=True
executed_notebook_count=20
failed_notebook_count=0
```

```text
python3 scripts/run_replication_audit.py --run-dir app/runs/phase-019-replication-audit --output-dir app/runs/phase-019-replication-audit
wrote app/runs/phase-019-replication-audit/replication_audit.json
wrote app/runs/phase-019-replication-audit/replication_audit.md
final_status=replicated_with_known_limits
completed_twenty_turns=True
selected_candidates_have_required_metadata=True
turns_have_statistical_evidence=True
business_report_statistical_sections=20
```

## Evidence

Generated audit artifacts:

```text
app/runs/phase-019-replication-audit/replication_audit.json
app/runs/phase-019-replication-audit/replication_audit.md
app/runs/phase-019-replication-audit/phase_regression_summary.json
```

Final audit summary:

```text
final_status: replicated_with_known_limits
completed_twenty_turns: True
workflow_task_statistical_misroutes: 0
selected_candidates_have_required_metadata: True
turns_have_statistical_evidence: True
business_report_statistical_sections: 20
notebook_workspace_present: True
selected_forum_metadata_count: 20
selected_tournament_metadata_count: 20
selected_reflection_metadata_count: 20
selected_evolution_metadata_count: 20
statistical_evidence_turn_count: 20
```

Known limits:

```text
Live model-based debate is deferred; governance is deterministic.
Statistical evidence is observational and exploratory, not causal proof.
Microsoft Agent Framework adapter runs deterministically without provider/model calls.
```

## 20-Turn Regression

Implemented and passed after adding the final replication audit.

## Video

No video was generated. This is a final audit phase; JSON/Markdown audit artifacts and the 20-turn regression summary are the relevant demo outputs.

## Known Gaps

- Live model-based debate is deferred.
- Statistical evidence remains observational and exploratory.
- Microsoft Agent Framework provider/model calls are disabled by design.

## Requirement Mapping

- Audit module: `app/replication_audit.py`
- Audit command: `scripts/run_replication_audit.py`
- Compatibility alias: `app/hypothesis_evolution.py`
- Test: `tests/test_replication_audit.py`
