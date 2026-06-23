"""Deterministic same-week/same-block matched-control tests."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

from app.statistical_tests import OUTCOMES


@dataclass(frozen=True)
class MatchedComparison:
    """Matched-control exploratory comparison result."""

    dataset: str
    grain: str
    outcome: str
    block_column: str
    exposed_rows: int
    matched_exposed_rows: int
    unmatched_exposed_rows: int
    control_rows_used: int
    mean_matched_difference: float | None
    status: str
    diagnostics: dict[str, object]
    caveats: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable result data."""
        return asdict(self)


def run_matched_comparison(
    path: Path,
    *,
    dataset: str,
    grain: str,
    outcome: str,
    block_column: str,
) -> MatchedComparison:
    """Compare exposed rows with same-week/same-block unexposed controls."""
    controls: dict[tuple[str, str], list[float]] = defaultdict(list)
    exposed: list[dict[str, str]] = []
    missing_block = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            block = row.get(block_column) or ""
            week = row.get("week_start_monday") or ""
            value = row.get(outcome)
            if not block:
                missing_block += 1
                continue
            if value in (None, ""):
                continue
            if row.get("has_game") in {"1", "true", "True"}:
                exposed.append(row)
            else:
                controls[(week, block)].append(float(value))

    differences: list[float] = []
    control_rows_used = 0
    unmatched = 0
    for row in exposed:
        key = (row.get("week_start_monday") or "", row.get(block_column) or "")
        matched_controls = controls.get(key, [])
        if not matched_controls:
            unmatched += 1
            continue
        control_mean = sum(matched_controls) / len(matched_controls)
        differences.append(float(row[outcome]) - control_mean)
        control_rows_used += len(matched_controls)

    status = "ok"
    caveats = [
        "Exploratory observational matched comparison only; not causal proof.",
        "Matching uses same week and same block only; residual confounding may remain.",
    ]
    mean_difference = None
    if not differences:
        status = "not_testable"
        caveats.append("No exposed rows had same-week/same-block unexposed controls.")
    else:
        mean_difference = sum(differences) / len(differences)
        if len(differences) < 5:
            status = "fragile"
            caveats.append("Fewer than five exposed rows had matched controls.")

    return MatchedComparison(
        dataset=dataset,
        grain=grain,
        outcome=outcome,
        block_column=block_column,
        exposed_rows=len(exposed),
        matched_exposed_rows=len(differences),
        unmatched_exposed_rows=unmatched,
        control_rows_used=control_rows_used,
        mean_matched_difference=mean_difference,
        status=status,
        diagnostics={
            "missing_block_rows": missing_block,
            "control_groups": len(controls),
        },
        caveats=caveats,
    )


def run_matched_tests(reference_dir: Path) -> dict[str, object]:
    """Run configured matched-control comparisons."""
    configs = [
        (
            "city_week",
            "city-week",
            reference_dir / "joined_city_week_game_economic.csv",
            "event_msa_block_id",
        ),
        (
            "msa_week",
            "MSA-week",
            reference_dir / "joined_msa_week_game_economic.csv",
            "msa_block_id",
        ),
    ]
    results = [
        run_matched_comparison(path, dataset=dataset, grain=grain, outcome=outcome, block_column=block_column)
        for dataset, grain, path, block_column in configs
        for outcome in OUTCOMES
    ]
    return {
        "schema_version": "phase-012.matched-control-tests.v1",
        "results": [result.to_dict() for result in results],
        "all_results_have_caveats": all(result.caveats for result in results),
        "not_testable_count": sum(1 for result in results if result.status == "not_testable"),
    }


def write_matched_smoke(report: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    """Write matched smoke JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "matched_smoke.json"
    markdown_path = output_dir / "matched_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_matched_smoke_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_matched_smoke_markdown(report: dict[str, object]) -> str:
    """Render matched smoke report as Markdown."""
    lines = ["# Matched Control Smoke Report", "", f"Schema: {report['schema_version']}", ""]
    for result in report["results"]:
        lines.extend(
            [
                f"## {result['dataset']} / {result['outcome']}",
                "",
                f"- Grain: {result['grain']}",
                f"- Status: {result['status']}",
                f"- Matched exposed rows: {result['matched_exposed_rows']}",
                f"- Unmatched exposed rows: {result['unmatched_exposed_rows']}",
                f"- Control rows used: {result['control_rows_used']}",
                f"- Mean matched difference: {result['mean_matched_difference']}",
                "- Caveats:",
                *[f"  - {caveat}" for caveat in result["caveats"]],
                "",
            ]
        )
    return "\n".join(lines)
