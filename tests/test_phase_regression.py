import json
from pathlib import Path

from app.phase_regression import run_phase_regression
from scripts.run_phase_regression import build_parser


def _write_reference_files(reference_dir: Path) -> None:
    reference_dir.mkdir()
    (reference_dir / "joined_city_week_game_economic.csv").write_text(
        "cityid,cityname,stateabbrev,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,Alpha,AA,2026-01-05,10.0,2.0,1,1\n",
        encoding="utf-8",
    )
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(
        "msa,msa_code,week_start_monday,revenue_all,merchants_all,has_game,game_count,msa_block_id\n"
        "Metro A,10000,2026-01-05,20.0,3.0,1,1,block-a\n",
        encoding="utf-8",
    )


def test_parser_defaults_to_twenty_turns() -> None:
    args = build_parser().parse_args(["--phase-id", "phase-test"])

    assert args.turns == 20


def test_run_phase_regression_writes_summary_and_checks_artifacts(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)

    summary, summary_path = run_phase_regression(
        phase_id="phase-test",
        turns=3,
        runs_dir=tmp_path / "runs",
        reference_dir=reference_dir,
    )

    assert summary.requested_turns == 3
    assert summary.completed_workflows == 3
    assert summary.stopped_early is False
    assert summary.workflow_task_statistical_misroutes == 0
    assert summary.selected_candidate_count == 3
    assert summary.selected_candidates_have_required_metadata is True
    assert summary.current_required_artifacts_exist is True
    assert summary.notebook_workspace_present is True
    assert summary.notebook_workspace["notebook_count"] == 3
    assert summary.notebook_workspace["markdown_export_count"] == 3
    assert summary.notebook_workspace["lightweight_executed_count"] == 3
    assert summary.notebook_execution["executed_notebook_count"] == 3
    assert summary.notebook_execution["failed_notebook_count"] == 0
    assert summary.notebook_execution["all_lightweight_executed"] is True
    assert summary.artifact_checks == {
        "session_json": True,
        "session_markdown": True,
        "telemetry_json": True,
        "discovery_decision_summary": True,
    }
    assert summary_path.exists()
    loaded = json.loads(summary_path.read_text(encoding="utf-8"))
    assert loaded["schema_version"] == "phase-004.phase-regression-summary.v1"


def test_run_phase_regression_supports_nbclient_backend(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)

    summary, _ = run_phase_regression(
        phase_id="phase-test-nbclient",
        turns=1,
        runs_dir=tmp_path / "runs",
        reference_dir=reference_dir,
        notebook_execution_backend="nbclient",
    )

    assert summary.notebook_workspace_present is True
    assert summary.notebook_execution["backend"] == "nbclient"
    assert summary.notebook_execution["executed_notebook_count"] == 1
    assert summary.notebook_execution["failed_notebook_count"] == 0
    assert summary.notebook_workspace["nbclient_executed_count"] == 1
