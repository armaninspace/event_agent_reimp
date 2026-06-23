from pathlib import Path

from app.data_profile import CITY_REQUIRED_COLUMNS, profile_csv


def test_profile_csv_counts_rows_and_required_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "city.csv"
    csv_path.write_text(
        "cityid,week_start_monday,revenue_all,merchants_all,has_game,game_count\n"
        "1,2026-01-05,10.0,2.0,1,1\n"
        "1,2026-01-12,11.0,2.5,0,0\n"
        "2,2026-01-05,9.0,1.5,1,2\n",
        encoding="utf-8",
    )

    profile = profile_csv(
        csv_path,
        grain="city-week",
        required_columns=CITY_REQUIRED_COLUMNS,
        geography_column="cityid",
    )

    assert profile.row_count == 3
    assert profile.column_count == 6
    assert profile.missing_columns == ()
    assert profile.missing_required_values == {column: 0 for column in CITY_REQUIRED_COLUMNS}
    assert profile.unique_geographies == 2
    assert profile.unique_weeks == 2
    assert profile.has_game_rows == 2


def test_profile_csv_reports_missing_columns_and_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "city.csv"
    csv_path.write_text(
        "cityid,week_start_monday,revenue_all,merchants_all,has_game\n"
        "1,2026-01-05,10.0,2.0,1\n"
        ",2026-01-12,11.0,2.5,0\n",
        encoding="utf-8",
    )

    profile = profile_csv(
        csv_path,
        grain="city-week",
        required_columns=CITY_REQUIRED_COLUMNS,
        geography_column="cityid",
    )

    assert profile.missing_columns == ("game_count",)
    assert profile.missing_required_values["cityid"] == 1
    assert profile.missing_required_values["game_count"] == 2
