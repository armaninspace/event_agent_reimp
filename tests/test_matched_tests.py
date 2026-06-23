from pathlib import Path

from app.matched_tests import run_matched_comparison, run_matched_tests, write_matched_smoke


def test_run_matched_comparison_calculates_matched_difference(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text(
        "week_start_monday,block,has_game,revenue_all\n"
        "2026-01-05,a,1,12\n"
        "2026-01-05,a,0,8\n"
        "2026-01-05,a,0,10\n",
        encoding="utf-8",
    )

    result = run_matched_comparison(path, dataset="fixture", grain="row", outcome="revenue_all", block_column="block")

    assert result.matched_exposed_rows == 1
    assert result.unmatched_exposed_rows == 0
    assert result.control_rows_used == 2
    assert result.mean_matched_difference == 3
    assert result.status == "fragile"


def test_run_matched_comparison_not_testable_without_controls(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("week_start_monday,block,has_game,revenue_all\n2026-01-05,a,1,12\n", encoding="utf-8")

    result = run_matched_comparison(path, dataset="fixture", grain="row", outcome="revenue_all", block_column="block")

    assert result.status == "not_testable"
    assert result.mean_matched_difference is None


def test_run_matched_tests_and_write_artifacts(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    reference_dir.mkdir()
    city = (
        "week_start_monday,event_msa_block_id,has_game,revenue_all,merchants_all\n"
        "2026-01-05,a,1,12,3\n"
        "2026-01-05,a,0,8,2\n"
    )
    msa = (
        "week_start_monday,msa_block_id,has_game,revenue_all,merchants_all\n"
        "2026-01-05,b,1,20,5\n"
        "2026-01-05,b,0,15,4\n"
    )
    (reference_dir / "joined_city_week_game_economic.csv").write_text(city, encoding="utf-8")
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(msa, encoding="utf-8")

    report = run_matched_tests(reference_dir)
    json_path, markdown_path = write_matched_smoke(report, tmp_path / "out")

    assert report["schema_version"] == "phase-012.matched-control-tests.v1"
    assert len(report["results"]) == 4
    assert report["all_results_have_caveats"] is True
    assert json_path.exists()
    assert markdown_path.exists()
