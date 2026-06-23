from pathlib import Path

from app.statistical_tests import compare_exposed_unexposed, run_exploratory_tests, write_statistical_smoke


def test_compare_exposed_unexposed_calculates_difference(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text(
        "has_game,revenue_all\n"
        "1,10\n"
        "1,14\n"
        "0,4\n"
        "0,6\n",
        encoding="utf-8",
    )

    result = compare_exposed_unexposed(path, dataset="fixture", grain="row", outcome="revenue_all")

    assert result.exposed_rows == 2
    assert result.unexposed_rows == 2
    assert result.exposed_mean == 12
    assert result.unexposed_mean == 5
    assert result.mean_difference == 7
    assert result.status == "fragile"
    assert result.caveats


def test_compare_exposed_unexposed_not_testable_without_unexposed_rows(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("has_game,revenue_all\n1,10\n1,14\n", encoding="utf-8")

    result = compare_exposed_unexposed(path, dataset="fixture", grain="row", outcome="revenue_all")

    assert result.status == "not_testable"
    assert result.mean_difference is None


def test_run_exploratory_tests_and_write_artifacts(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    reference_dir.mkdir()
    content = (
        "has_game,revenue_all,merchants_all\n"
        "1,10,2\n"
        "1,12,3\n"
        "0,8,1\n"
        "0,9,1.5\n"
    )
    (reference_dir / "joined_city_week_game_economic.csv").write_text(content, encoding="utf-8")
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(content, encoding="utf-8")

    report = run_exploratory_tests(reference_dir)
    json_path, markdown_path = write_statistical_smoke(report, tmp_path / "out")

    assert report["schema_version"] == "phase-010.exploratory-statistical-tests.v1"
    assert len(report["results"]) == 4
    assert report["all_results_have_caveats"] is True
    assert json_path.exists()
    assert markdown_path.exists()
