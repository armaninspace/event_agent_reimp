from pathlib import Path

from app.multiple_testing import benjamini_hochberg, build_correction_report, write_correction_smoke


def test_benjamini_hochberg_adjusts_p_values() -> None:
    adjusted = benjamini_hochberg([0.01, 0.04, 0.03, None])

    assert adjusted[0] == 0.03
    assert round(adjusted[1], 6) == 0.04
    assert round(adjusted[2], 6) == 0.04
    assert adjusted[3] is None


def test_build_correction_report_and_write_artifacts(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    reference_dir.mkdir()
    city = (
        "week_start_monday,event_msa_block_id,has_game,revenue_all,merchants_all\n"
        "2026-01-05,a,1,12,3\n"
        "2026-01-05,a,1,17,6\n"
        "2026-01-05,a,0,8,2\n"
        "2026-01-05,a,0,11,3\n"
    )
    msa = (
        "week_start_monday,msa_block_id,has_game,revenue_all,merchants_all\n"
        "2026-01-05,b,1,20,5\n"
        "2026-01-05,b,1,27,9\n"
        "2026-01-05,b,0,15,4\n"
        "2026-01-05,b,0,18,5\n"
    )
    (reference_dir / "joined_city_week_game_economic.csv").write_text(city, encoding="utf-8")
    (reference_dir / "joined_msa_week_game_economic.csv").write_text(msa, encoding="utf-8")

    report = build_correction_report(reference_dir)
    json_path, markdown_path = write_correction_smoke(report, tmp_path / "out")

    assert report["schema_version"] == "phase-013.pvalues-multiple-testing.v1"
    assert report["result_count"] == 8
    assert all("p_value" in result for result in report["results"])
    assert all("adjusted_p_value" in result for result in report["results"])
    assert json_path.exists()
    assert markdown_path.exists()
