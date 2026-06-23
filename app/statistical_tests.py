"""Exploratory statistical summaries for event/economic reference data."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


OUTCOMES = ("revenue_all", "merchants_all")


@dataclass(frozen=True)
class ExploratoryComparison:
    """Descriptive exposed-vs-unexposed comparison for one outcome."""

    dataset: str
    grain: str
    outcome: str
    exposed_rows: int
    unexposed_rows: int
    exposed_mean: float | None
    unexposed_mean: float | None
    mean_difference: float | None
    status: str
    diagnostics: dict[str, object]
    caveats: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable result data."""
        return asdict(self)


def compare_exposed_unexposed(
    path: Path,
    *,
    dataset: str,
    grain: str,
    outcome: str,
) -> ExploratoryComparison:
    """Compare outcome means between game-exposed and unexposed rows."""
    exposed: list[float] = []
    unexposed: list[float] = []
    missing_outcome = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_value = row.get(outcome)
            if raw_value in (None, ""):
                missing_outcome += 1
                continue
            value = float(raw_value)
            if row.get("has_game") in {"1", "true", "True"}:
                exposed.append(value)
            else:
                unexposed.append(value)

    caveats = [
        "Exploratory observational association only; this is not causal proof.",
        "No matched controls, p-values, or multiple-testing correction are applied in this phase.",
    ]
    status = "ok"
    exposed_mean = _mean(exposed)
    unexposed_mean = _mean(unexposed)
    mean_difference = None
    if exposed_mean is None or unexposed_mean is None:
        status = "not_testable"
        caveats.append("Both exposed and unexposed rows are required.")
    else:
        mean_difference = exposed_mean - unexposed_mean
        if len(exposed) < 5 or len(unexposed) < 5:
            status = "fragile"
            caveats.append("One comparison group has fewer than five rows.")

    return ExploratoryComparison(
        dataset=dataset,
        grain=grain,
        outcome=outcome,
        exposed_rows=len(exposed),
        unexposed_rows=len(unexposed),
        exposed_mean=exposed_mean,
        unexposed_mean=unexposed_mean,
        mean_difference=mean_difference,
        status=status,
        diagnostics={
            "missing_outcome_rows": missing_outcome,
            "minimum_group_rows": min(len(exposed), len(unexposed)),
        },
        caveats=caveats,
    )


def run_exploratory_tests(reference_dir: Path) -> dict[str, object]:
    """Run configured exploratory comparisons over final runtime files."""
    configs = [
        ("city_week", "city-week", reference_dir / "joined_city_week_game_economic.csv"),
        ("msa_week", "MSA-week", reference_dir / "joined_msa_week_game_economic.csv"),
    ]
    results = [
        compare_exposed_unexposed(path, dataset=dataset, grain=grain, outcome=outcome)
        for dataset, grain, path in configs
        for outcome in OUTCOMES
    ]
    return {
        "schema_version": "phase-010.exploratory-statistical-tests.v1",
        "results": [result.to_dict() for result in results],
        "all_results_have_caveats": all(result.caveats for result in results),
        "not_testable_count": sum(1 for result in results if result.status == "not_testable"),
    }


def write_statistical_smoke(report: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    """Write statistical smoke JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "statistical_smoke.json"
    markdown_path = output_dir / "statistical_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_statistical_smoke_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_statistical_smoke_markdown(report: dict[str, object]) -> str:
    """Render statistical smoke report as Markdown."""
    lines = [
        "# Exploratory Statistical Smoke Report",
        "",
        f"Schema: {report['schema_version']}",
        "",
    ]
    for result in report["results"]:
        lines.extend(
            [
                f"## {result['dataset']} / {result['outcome']}",
                "",
                f"- Grain: {result['grain']}",
                f"- Status: {result['status']}",
                f"- Exposed rows: {result['exposed_rows']}",
                f"- Unexposed rows: {result['unexposed_rows']}",
                f"- Exposed mean: {result['exposed_mean']}",
                f"- Unexposed mean: {result['unexposed_mean']}",
                f"- Mean difference: {result['mean_difference']}",
                "- Caveats:",
                *[f"  - {caveat}" for caveat in result["caveats"]],
                "",
            ]
        )
    return "\n".join(lines)


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)
