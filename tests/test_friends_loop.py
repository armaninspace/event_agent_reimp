import json
from pathlib import Path

from app.friends_loop import run_friends_question_loop


def _write_reference_files(reference_dir: Path) -> None:
    reference_dir.mkdir()
    (reference_dir / "joined_city_week_game_economic.csv").write_text(
        "cityid,cityname,stateabbrev,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,Alpha,AA,2026-01-05,10.0,2.0,1,1\n"
        "2,Beta,BB,2026-01-12,12.0,3.0,0,0\n",
        encoding="utf-8",
    )
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(
        "msa,msa_code,week_start_monday,revenue_all,merchants_all,has_game,game_count,msa_block_id\n"
        "Metro A,10000,2026-01-05,20.0,3.0,1,1,block-a\n",
        encoding="utf-8",
    )


def test_run_friends_question_loop_completes_two_turns_with_selected_and_rejected(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)

    session = run_friends_question_loop(
        turn_count=2,
        output_dir=tmp_path / "run",
        reference_dir=reference_dir,
    )

    assert session["session_summary"]["completed_turns"] == 2
    assert len(session["turns"]) == 2
    for turn in session["turns"]:
        assert turn["selected_candidate"]["candidate_id"]
        assert len(turn["rejected_candidates"]) == 2


def test_run_friends_question_loop_selection_is_deterministic(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)

    first = run_friends_question_loop(turn_count=2, output_dir=tmp_path / "run-1", reference_dir=reference_dir)
    second = run_friends_question_loop(turn_count=2, output_dir=tmp_path / "run-2", reference_dir=reference_dir)

    first_selected = [turn["selected_candidate"]["candidate_id"] for turn in first["turns"]]
    second_selected = [turn["selected_candidate"]["candidate_id"] for turn in second["turns"]]
    assert first_selected == second_selected == ["turn-01-crowd-spending", "turn-02-market-coverage"]


def test_run_friends_question_loop_writes_artifacts_and_telemetry(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)

    session = run_friends_question_loop(turn_count=2, output_dir=tmp_path / "run", reference_dir=reference_dir)
    artifact_paths = session["artifact_paths"]

    for path in artifact_paths.values():
        assert Path(path).exists()

    telemetry = json.loads(Path(artifact_paths["telemetry_json"]).read_text(encoding="utf-8"))
    assert telemetry[0]["event_type"] == "memory.seeded"
    assert {event["event_type"] for event in telemetry} >= {
        "turn.started",
        "knowledge.read",
        "board.proposed",
        "board.ranked",
        "discussion.message",
        "turn.completed",
    }
    assert all("payload" in event for event in telemetry)
    assert "Discovery Decision Summary" in Path(artifact_paths["discovery_decision_summary"]).read_text(
        encoding="utf-8"
    )


def test_run_friends_question_loop_writes_notebook_workspace_when_requested(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    _write_reference_files(reference_dir)

    session = run_friends_question_loop(
        turn_count=2,
        output_dir=tmp_path / "run",
        reference_dir=reference_dir,
        notebook_dir=tmp_path / "notebooks",
    )

    assert all("notebook_artifacts" in turn for turn in session["turns"])
    telemetry = json.loads(Path(session["artifact_paths"]["telemetry_json"]).read_text(encoding="utf-8"))
    event_types = {event["event_type"] for event in telemetry}
    assert "notebook.created" in event_types
    assert "wiki.updated" in event_types
