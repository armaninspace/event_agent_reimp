"""CSV profiling helpers for final event/economic runtime files."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path


CITY_REQUIRED_COLUMNS = (
    "cityid",
    "week_start_monday",
    "revenue_all",
    "merchants_all",
    "has_game",
    "game_count",
)

MSA_REQUIRED_COLUMNS = (
    "msa_code",
    "week_start_monday",
    "revenue_all",
    "merchants_all",
    "has_game",
    "game_count",
    "msa_block_id",
)


@dataclass(frozen=True)
class CsvDataProfile:
    """Aggregate profile for a runtime CSV file."""

    path: str
    grain: str
    row_count: int
    column_count: int
    required_columns: tuple[str, ...]
    missing_columns: tuple[str, ...]
    missing_required_values: dict[str, int]
    unique_geographies: int
    unique_weeks: int
    has_game_rows: int

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable profile data."""
        data = asdict(self)
        data["required_columns"] = list(self.required_columns)
        data["missing_columns"] = list(self.missing_columns)
        return data


def profile_csv(
    path: Path,
    *,
    grain: str,
    required_columns: Iterable[str],
    geography_column: str,
) -> CsvDataProfile:
    """Profile one CSV file using deterministic aggregate checks."""
    required = tuple(required_columns)
    missing_required_values = {column: 0 for column in required}
    geographies: set[str] = set()
    weeks: set[str] = set()
    row_count = 0
    has_game_rows = 0

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = tuple(reader.fieldnames or ())
        missing_columns = tuple(column for column in required if column not in fieldnames)

        for row in reader:
            row_count += 1
            if row.get("has_game") == "1":
                has_game_rows += 1
            geography = row.get(geography_column)
            if geography:
                geographies.add(geography)
            week = row.get("week_start_monday")
            if week:
                weeks.add(week)
            for column in required:
                if not row.get(column):
                    missing_required_values[column] += 1

    return CsvDataProfile(
        path=str(path),
        grain=grain,
        row_count=row_count,
        column_count=len(fieldnames),
        required_columns=required,
        missing_columns=missing_columns,
        missing_required_values=missing_required_values,
        unique_geographies=len(geographies),
        unique_weeks=len(weeks),
        has_game_rows=has_game_rows,
    )


def profile_final_runtime_files(reference_dir: Path) -> dict[str, CsvDataProfile]:
    """Profile the required final city-week and MSA-week runtime CSV files."""
    return {
        "city_week": profile_csv(
            reference_dir / "joined_city_week_game_economic.csv",
            grain="city-week",
            required_columns=CITY_REQUIRED_COLUMNS,
            geography_column="cityid",
        ),
        "msa_week": profile_csv(
            reference_dir / "joined_msa_week_game_economic.csv",
            grain="MSA-week",
            required_columns=MSA_REQUIRED_COLUMNS,
            geography_column="msa_code",
        ),
    }
