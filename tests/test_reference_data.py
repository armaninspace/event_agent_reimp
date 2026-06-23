from pathlib import Path

import pytest

from app.reference_data import (
    CITY_WEEK_REQUIRED_COLUMNS,
    build_reference_quality_report,
    evaluate_dataset_quality,
    load_city_week_records,
    write_quality_report,
)


def _write_city_fixture(path: Path) -> None:
    path.write_text(
        "cityid,cityname,stateabbrev,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,Alpha,AA,2026-01-05,10.5,2.0,1,1\n"
        "1,Alpha,AA,2026-01-12,11.0,2.1,0,0\n"
        "2,Beta,BB,2026-01-05,8.0,1.5,true,2\n",
        encoding="utf-8",
    )


def _write_msa_fixture(path: Path) -> None:
    path.write_text(
        "msa,msa_code,week_start_monday,revenue_all,merchants_all,has_game,game_count,msa_block_id\n"
        "Metro A,10000,2026-01-05,20.0,3.0,1,1,block-a\n"
        "Metro B,20000,2026-01-05,21.0,3.5,0,0,block-b\n",
        encoding="utf-8",
    )


def test_load_city_week_records_from_fixture_preserves_stable_grain(tmp_path: Path) -> None:
    city_path = tmp_path / "city.csv"
    _write_city_fixture(city_path)

    records = load_city_week_records(city_path)

    assert len(records) == 3
    assert {record.grain for record in records} == {"city-week"}
    assert records[0].geography_id == "1"
    assert records[0].geography_name == "Alpha, AA"
    assert records[0].week_start_monday == "2026-01-05"
    assert records[0].revenue_all == 10.5
    assert records[0].merchants_all == 2.0
    assert records[0].has_game is True
    assert records[0].game_count == 1


def test_load_city_week_records_rejects_missing_required_columns(tmp_path: Path) -> None:
    city_path = tmp_path / "city.csv"
    city_path.write_text("cityid,week_start_monday,revenue_all\n1,2026-01-05,1.0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_city_week_records(city_path)


def test_evaluate_dataset_quality_warns_for_weak_data(tmp_path: Path) -> None:
    weak_path = tmp_path / "weak.csv"
    weak_path.write_text(
        "cityid,cityname,stateabbrev,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,Alpha,AA,2026-01-05,10.5,2.0,0,0\n"
        ",Alpha,AA,2026-01-12,11.0,2.1,0,0\n",
        encoding="utf-8",
    )

    quality = evaluate_dataset_quality(
        name="city_week",
        grain="city-week",
        path=weak_path,
        required_columns=CITY_WEEK_REQUIRED_COLUMNS,
        geography_column="cityid",
    )

    assert quality.row_count == 2
    assert quality.has_game_rows == 0
    assert any("missing required values" in warning for warning in quality.warnings)
    assert any("no game exposure rows" in warning for warning in quality.warnings)


def test_build_reference_quality_report_and_write_artifacts(tmp_path: Path) -> None:
    reference_dir = tmp_path / "reference"
    reference_dir.mkdir()
    _write_city_fixture(reference_dir / "joined_city_week_game_economic.csv")
    _write_msa_fixture(reference_dir / "joined_msa_week_game_economic.csv")

    report = build_reference_quality_report(reference_dir)
    json_path, markdown_path = write_quality_report(report, tmp_path / "out")

    assert report.schema_version == "phase-002.reference-data-quality.v1"
    assert report.all_required_columns_present is True
    assert report.all_required_values_present is True
    assert report.datasets["city_week"].row_count == 3
    assert report.datasets["msa_week"].row_count == 2
    assert report.warnings == []
    assert json_path.exists()
    assert markdown_path.exists()
    assert "Reference Data Quality Report" in markdown_path.read_text(encoding="utf-8")
