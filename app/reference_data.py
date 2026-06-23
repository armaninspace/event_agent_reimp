"""Reference event/economic data loading and quality checks."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path


CITY_WEEK_REQUIRED_COLUMNS = (
    "cityid",
    "cityname",
    "stateabbrev",
    "week_start_monday",
    "revenue_all",
    "merchants_all",
    "has_game",
    "game_count",
)

MSA_WEEK_REQUIRED_COLUMNS = (
    "msa",
    "msa_code",
    "week_start_monday",
    "revenue_all",
    "merchants_all",
    "has_game",
    "game_count",
    "msa_block_id",
)


@dataclass(frozen=True)
class ReferenceRecord:
    """Stable row contract for event/economic reference data."""

    grain: str
    geography_id: str
    geography_name: str
    week_start_monday: str
    revenue_all: float
    merchants_all: float
    has_game: bool
    game_count: int
    source_row: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable record."""
        return asdict(self)


@dataclass(frozen=True)
class DatasetQuality:
    """Quality summary for one reference dataset."""

    name: str
    grain: str
    path: str
    row_count: int
    required_columns: tuple[str, ...]
    missing_columns: tuple[str, ...]
    missing_required_values: dict[str, int]
    unique_geographies: int
    unique_weeks: int
    has_game_rows: int
    total_game_count: int
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable quality data."""
        data = asdict(self)
        data["required_columns"] = list(self.required_columns)
        data["missing_columns"] = list(self.missing_columns)
        data["warnings"] = list(self.warnings)
        return data


@dataclass(frozen=True)
class ReferenceDataQualityReport:
    """Quality report for all final runtime reference datasets."""

    schema_version: str
    datasets: dict[str, DatasetQuality]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable report data."""
        return {
            "schema_version": self.schema_version,
            "datasets": {name: dataset.to_dict() for name, dataset in self.datasets.items()},
            "warnings": self.warnings,
            "all_required_columns_present": self.all_required_columns_present,
            "all_required_values_present": self.all_required_values_present,
        }

    @property
    def warnings(self) -> list[str]:
        """Return all dataset warnings as one flat list."""
        return [warning for dataset in self.datasets.values() for warning in dataset.warnings]

    @property
    def all_required_columns_present(self) -> bool:
        """Return whether every dataset includes all required columns."""
        return all(not dataset.missing_columns for dataset in self.datasets.values())

    @property
    def all_required_values_present(self) -> bool:
        """Return whether every dataset has values for all required fields."""
        return all(sum(dataset.missing_required_values.values()) == 0 for dataset in self.datasets.values())


def load_city_week_records(path: Path) -> list[ReferenceRecord]:
    """Load city-week reference records from a final joined CSV."""
    return _load_records(
        path,
        grain="city-week",
        required_columns=CITY_WEEK_REQUIRED_COLUMNS,
        geography_id_column="cityid",
        geography_name_columns=("cityname", "stateabbrev"),
    )


def load_msa_week_records(path: Path) -> list[ReferenceRecord]:
    """Load MSA-week reference records from a final joined CSV."""
    return _load_records(
        path,
        grain="MSA-week",
        required_columns=MSA_WEEK_REQUIRED_COLUMNS,
        geography_id_column="msa_code",
        geography_name_columns=("msa",),
    )


def build_reference_quality_report(reference_dir: Path) -> ReferenceDataQualityReport:
    """Build a quality report for the final reference runtime files."""
    city_path = reference_dir / "joined_city_week_game_economic.csv"
    msa_path = reference_dir / "joined_msa_week_game_economic.csv"
    return ReferenceDataQualityReport(
        schema_version="phase-002.reference-data-quality.v1",
        datasets={
            "city_week": evaluate_dataset_quality(
                name="city_week",
                grain="city-week",
                path=city_path,
                required_columns=CITY_WEEK_REQUIRED_COLUMNS,
                geography_column="cityid",
            ),
            "msa_week": evaluate_dataset_quality(
                name="msa_week",
                grain="MSA-week",
                path=msa_path,
                required_columns=MSA_WEEK_REQUIRED_COLUMNS,
                geography_column="msa_code",
            ),
        },
    )


def evaluate_dataset_quality(
    *,
    name: str,
    grain: str,
    path: Path,
    required_columns: Iterable[str],
    geography_column: str,
) -> DatasetQuality:
    """Evaluate required fields and basic coverage for one dataset."""
    required = tuple(required_columns)
    missing_required_values = {column: 0 for column in required}
    geographies: set[str] = set()
    weeks: set[str] = set()
    row_count = 0
    has_game_rows = 0
    total_game_count = 0

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = tuple(reader.fieldnames or ())
        missing_columns = tuple(column for column in required if column not in fieldnames)

        for row in reader:
            row_count += 1
            if _parse_bool(row.get("has_game", "")):
                has_game_rows += 1
            total_game_count += _parse_int(row.get("game_count", "0"))
            geography = row.get(geography_column)
            if geography:
                geographies.add(geography)
            week = row.get("week_start_monday")
            if week:
                weeks.add(week)
            for column in required:
                if not row.get(column):
                    missing_required_values[column] += 1

    warnings = _build_warnings(
        name=name,
        row_count=row_count,
        missing_columns=missing_columns,
        missing_required_values=missing_required_values,
        unique_geographies=len(geographies),
        unique_weeks=len(weeks),
        has_game_rows=has_game_rows,
        total_game_count=total_game_count,
    )
    return DatasetQuality(
        name=name,
        grain=grain,
        path=str(path),
        row_count=row_count,
        required_columns=required,
        missing_columns=missing_columns,
        missing_required_values=missing_required_values,
        unique_geographies=len(geographies),
        unique_weeks=len(weeks),
        has_game_rows=has_game_rows,
        total_game_count=total_game_count,
        warnings=warnings,
    )


def write_quality_report(report: ReferenceDataQualityReport, output_dir: Path) -> tuple[Path, Path]:
    """Write JSON and Markdown quality report artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "reference_data_quality.json"
    markdown_path = output_dir / "reference_data_quality.md"
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_quality_report_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_quality_report_markdown(report: ReferenceDataQualityReport) -> str:
    """Render a Markdown quality report."""
    lines = [
        "# Reference Data Quality Report",
        "",
        f"Schema: {report.schema_version}",
        "",
        f"All required columns present: {report.all_required_columns_present}",
        f"All required values present: {report.all_required_values_present}",
        "",
    ]
    for dataset in report.datasets.values():
        lines.extend(
            [
                f"## {dataset.name}",
                "",
                f"- Grain: {dataset.grain}",
                f"- Rows: {dataset.row_count}",
                f"- Unique geographies: {dataset.unique_geographies}",
                f"- Unique weeks: {dataset.unique_weeks}",
                f"- Rows with games: {dataset.has_game_rows}",
                f"- Total game count: {dataset.total_game_count}",
                f"- Missing columns: {', '.join(dataset.missing_columns) if dataset.missing_columns else 'none'}",
                "",
            ]
        )
        if dataset.warnings:
            lines.append("Warnings:")
            lines.extend(f"- {warning}" for warning in dataset.warnings)
            lines.append("")
    if not report.warnings:
        lines.extend(["## Warnings", "", "No warnings.", ""])
    return "\n".join(lines)


def _load_records(
    path: Path,
    *,
    grain: str,
    required_columns: tuple[str, ...],
    geography_id_column: str,
    geography_name_columns: tuple[str, ...],
) -> list[ReferenceRecord]:
    records: list[ReferenceRecord] = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = tuple(reader.fieldnames or ())
        missing_columns = tuple(column for column in required_columns if column not in fieldnames)
        if missing_columns:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing_columns)}")
        for row in reader:
            records.append(
                ReferenceRecord(
                    grain=grain,
                    geography_id=row[geography_id_column],
                    geography_name=_join_name(row, geography_name_columns),
                    week_start_monday=row["week_start_monday"],
                    revenue_all=_parse_float(row["revenue_all"]),
                    merchants_all=_parse_float(row["merchants_all"]),
                    has_game=_parse_bool(row["has_game"]),
                    game_count=_parse_int(row["game_count"]),
                    source_row=dict(row),
                )
            )
    return records


def _build_warnings(
    *,
    name: str,
    row_count: int,
    missing_columns: tuple[str, ...],
    missing_required_values: dict[str, int],
    unique_geographies: int,
    unique_weeks: int,
    has_game_rows: int,
    total_game_count: int,
) -> tuple[str, ...]:
    warnings: list[str] = []
    if row_count == 0:
        warnings.append(f"{name}: dataset has no rows")
    if missing_columns:
        warnings.append(f"{name}: missing required columns: {', '.join(missing_columns)}")
    missing_value_columns = [column for column, count in missing_required_values.items() if count > 0]
    if missing_value_columns:
        warnings.append(f"{name}: missing required values in: {', '.join(missing_value_columns)}")
    if unique_geographies == 0:
        warnings.append(f"{name}: no geography identifiers found")
    if unique_weeks == 0:
        warnings.append(f"{name}: no week_start_monday values found")
    if has_game_rows == 0 or total_game_count == 0:
        warnings.append(f"{name}: no game exposure rows found")
    return tuple(warnings)


def _join_name(row: dict[str, str], columns: tuple[str, ...]) -> str:
    return ", ".join(value for column in columns if (value := row.get(column)))


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def _parse_float(value: str) -> float:
    return float(value or 0)


def _parse_int(value: str) -> int:
    if not value:
        return 0
    return int(float(value))
