"""P-values and multiple-testing correction for statistical smoke results."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from scipy import stats

from app.matched_tests import run_matched_tests
from app.statistical_tests import OUTCOMES, run_exploratory_tests

_LEGACY_NO_PVALUE_CAVEAT = "No matched controls, p-values, or multiple-testing correction are applied in this phase."


@dataclass(frozen=True)
class CorrectedResult:
    """Statistical smoke result with raw and adjusted p-values."""

    result_id: str
    family: str
    dataset: str
    outcome: str
    statistic: float | None
    p_value: float | None
    adjusted_p_value: float | None
    status: str
    caveats: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable result data."""
        return asdict(self)


def benjamini_hochberg(p_values: list[float | None]) -> list[float | None]:
    """Apply Benjamini-Hochberg FDR correction."""
    indexed = [(index, p_value) for index, p_value in enumerate(p_values) if p_value is not None]
    total = len(indexed)
    adjusted: list[float | None] = [None] * len(p_values)
    if total == 0:
        return adjusted
    sorted_values = sorted(indexed, key=lambda item: item[1])
    running_min = 1.0
    for rank_from_end, (index, p_value) in enumerate(reversed(sorted_values), start=1):
        rank = total - rank_from_end + 1
        corrected = min(running_min, p_value * total / rank)
        running_min = corrected
        adjusted[index] = min(corrected, 1.0)
    return adjusted


def build_correction_report(reference_dir: Path) -> dict[str, object]:
    """Build combined p-value and multiple-testing correction report."""
    raw_results = _exploratory_p_values(reference_dir) + _matched_p_values(reference_dir)
    adjusted = benjamini_hochberg([result.p_value for result in raw_results])
    corrected = [
        CorrectedResult(
            result_id=result.result_id,
            family=result.family,
            dataset=result.dataset,
            outcome=result.outcome,
            statistic=result.statistic,
            p_value=result.p_value,
            adjusted_p_value=adjusted_value,
            status=result.status,
            caveats=_phase_appropriate_caveats(result.caveats)
            + [
                "P-values are exploratory metadata only.",
                "Adjusted p-values do not remove observational confounding.",
            ],
        )
        for result, adjusted_value in zip(raw_results, adjusted, strict=True)
    ]
    return {
        "schema_version": "phase-013.pvalues-multiple-testing.v1",
        "method": "Benjamini-Hochberg FDR correction",
        "result_count": len(corrected),
        "results": [result.to_dict() for result in corrected],
    }


def write_correction_smoke(report: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    """Write correction smoke JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "correction_smoke.json"
    markdown_path = output_dir / "correction_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_correction_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_correction_markdown(report: dict[str, object]) -> str:
    """Render correction report as Markdown."""
    lines = [
        "# P-Values And Multiple-Testing Correction",
        "",
        f"Schema: {report['schema_version']}",
        f"Method: {report['method']}",
        "",
    ]
    for result in report["results"]:
        lines.extend(
            [
                f"## {result['result_id']}",
                "",
                f"- Family: {result['family']}",
                f"- Statistic: {result['statistic']}",
                f"- P-value: {result['p_value']}",
                f"- Adjusted p-value: {result['adjusted_p_value']}",
                f"- Status: {result['status']}",
                "",
            ]
        )
    return "\n".join(lines)


def _exploratory_p_values(reference_dir: Path) -> list[CorrectedResult]:
    report = run_exploratory_tests(reference_dir)
    results: list[CorrectedResult] = []
    for item in report["results"]:
        exposed, unexposed = _load_groups(reference_dir, item["dataset"], item["outcome"])
        if len(exposed) < 2 or len(unexposed) < 2:
            statistic = None
            p_value = None
            status = "not_testable"
        else:
            test = stats.ttest_ind(exposed, unexposed, equal_var=False, nan_policy="omit")
            statistic = float(test.statistic)
            p_value = float(test.pvalue)
            status = item["status"]
        results.append(
            CorrectedResult(
                result_id=f"exploratory:{item['dataset']}:{item['outcome']}",
                family="exploratory",
                dataset=item["dataset"],
                outcome=item["outcome"],
                statistic=statistic,
                p_value=p_value,
                adjusted_p_value=None,
                status=status,
                caveats=item["caveats"],
            )
        )
    return results


def _phase_appropriate_caveats(caveats: list[str]) -> list[str]:
    """Drop caveats that described earlier phases before p-values existed."""
    return [caveat for caveat in caveats if caveat != _LEGACY_NO_PVALUE_CAVEAT]


def _matched_p_values(reference_dir: Path) -> list[CorrectedResult]:
    report = run_matched_tests(reference_dir)
    results: list[CorrectedResult] = []
    for item in report["results"]:
        differences = _load_matched_differences(reference_dir, item["dataset"], item["outcome"], item["block_column"])
        if len(differences) < 2:
            statistic = None
            p_value = None
            status = "not_testable"
        else:
            test = stats.ttest_1samp(differences, popmean=0.0, nan_policy="omit")
            statistic = float(test.statistic)
            p_value = float(test.pvalue)
            status = item["status"]
        results.append(
            CorrectedResult(
                result_id=f"matched:{item['dataset']}:{item['outcome']}",
                family="matched",
                dataset=item["dataset"],
                outcome=item["outcome"],
                statistic=statistic,
                p_value=p_value,
                adjusted_p_value=None,
                status=status,
                caveats=item["caveats"],
            )
        )
    return results


def _path_for_dataset(reference_dir: Path, dataset: str) -> Path:
    if dataset == "city_week":
        return reference_dir / "joined_city_week_game_economic.csv"
    return reference_dir / "joined_msa_week_game_economic.csv"


def _load_groups(reference_dir: Path, dataset: str, outcome: str) -> tuple[list[float], list[float]]:
    exposed: list[float] = []
    unexposed: list[float] = []
    with _path_for_dataset(reference_dir, dataset).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(outcome) in (None, ""):
                continue
            target = exposed if row.get("has_game") in {"1", "true", "True"} else unexposed
            target.append(float(row[outcome]))
    return exposed, unexposed


def _load_matched_differences(reference_dir: Path, dataset: str, outcome: str, block_column: str) -> list[float]:
    path = _path_for_dataset(reference_dir, dataset)
    controls: dict[tuple[str, str], list[float]] = {}
    exposed: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            block = row.get(block_column)
            value = row.get(outcome)
            if not block or value in (None, ""):
                continue
            key = (row.get("week_start_monday") or "", block)
            if row.get("has_game") in {"1", "true", "True"}:
                exposed.append(row)
            else:
                controls.setdefault(key, []).append(float(value))
    differences: list[float] = []
    for row in exposed:
        key = (row.get("week_start_monday") or "", row.get(block_column) or "")
        matched_controls = controls.get(key, [])
        if matched_controls:
            differences.append(float(row[outcome]) - (sum(matched_controls) / len(matched_controls)))
    return differences
