"""Causal-design diagnostics for observational event-spending evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from app.matched_tests import run_matched_tests
from app.statistical_tests import OUTCOMES


@dataclass(frozen=True)
class CausalDesignDiagnostic:
    """Observed control coverage and claim boundary for one dataset/outcome."""

    diagnostic_id: str
    dataset: str
    outcome: str
    design_level: str
    evidence_grade: str
    exposed_rows: int
    matched_exposed_rows: int
    unmatched_exposed_rows: int
    control_rows_used: int
    matched_exposure_rate: float | None
    controls_per_matched_exposure: float | None
    limitations: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable diagnostic data."""
        return asdict(self)


def build_causal_design_report(reference_dir: Path) -> dict[str, object]:
    """Build causal-design diagnostics from matched-control evidence."""
    matched_report = run_matched_tests(reference_dir)
    diagnostics = [_diagnostic_from_matched_result(result) for result in matched_report["results"]]
    return {
        "schema_version": "phase-026.causal-design-diagnostics.v1",
        "method": "same-week/same-block matched-control design diagnostics",
        "diagnostic_count": len(diagnostics),
        "controlled_result_count": sum(
            1
            for diagnostic in diagnostics
            if diagnostic.evidence_grade in {"controlled_observational", "fragile_controlled_observational"}
        ),
        "results": [diagnostic.to_dict() for diagnostic in diagnostics],
        "limitations": [
            "Controls reduce simple same-week/same-block confounding but do not prove causality.",
            "Unobserved shocks, selection into game weeks, and missing external calendars may still bias estimates.",
        ],
    }


def diagnostics_for_semantic_slot(report: dict[str, object], semantic_slot: str) -> list[dict[str, object]]:
    """Return causal diagnostics relevant to a candidate semantic slot."""
    results = report.get("results", [])
    if not isinstance(results, list):
        return []
    return [
        result
        for result in results
        if isinstance(result, dict) and _diagnostic_matches_slot(result, semantic_slot)
    ]


def summarize_designs(diagnostics: list[dict[str, object]]) -> dict[str, object]:
    """Summarize diagnostics for candidate-level statistical evidence."""
    grades = [str(item.get("evidence_grade")) for item in diagnostics if isinstance(item.get("evidence_grade"), str)]
    levels = [str(item.get("design_level")) for item in diagnostics if isinstance(item.get("design_level"), str)]
    return {
        "schema_version": "phase-026.candidate-causal-design.v1",
        "design_count": len(diagnostics),
        "strongest_design_level": _strongest_level(levels),
        "evidence_grade": _strongest_grade(grades),
        "diagnostic_ids": [item["diagnostic_id"] for item in diagnostics if isinstance(item.get("diagnostic_id"), str)],
        "diagnostics": diagnostics,
        "claim_boundary": "controlled observational evidence; not causal proof"
        if diagnostics
        else "no causal-design diagnostics available",
    }


def _diagnostic_from_matched_result(result: object) -> CausalDesignDiagnostic:
    if not isinstance(result, dict):
        raise ValueError("Matched result must be a dictionary.")
    exposed_rows = int(result["exposed_rows"])
    matched_rows = int(result["matched_exposed_rows"])
    unmatched_rows = int(result["unmatched_exposed_rows"])
    control_rows = int(result["control_rows_used"])
    matched_rate = matched_rows / exposed_rows if exposed_rows else None
    controls_per_match = control_rows / matched_rows if matched_rows else None
    evidence_grade = _evidence_grade(matched_rows=matched_rows, unmatched_rows=unmatched_rows)
    return CausalDesignDiagnostic(
        diagnostic_id=f"causal-design:{result['dataset']}:{result['outcome']}",
        dataset=str(result["dataset"]),
        outcome=str(result["outcome"]),
        design_level="same_week_same_block_matched" if matched_rows else "unmatched",
        evidence_grade=evidence_grade,
        exposed_rows=exposed_rows,
        matched_exposed_rows=matched_rows,
        unmatched_exposed_rows=unmatched_rows,
        control_rows_used=control_rows,
        matched_exposure_rate=matched_rate,
        controls_per_matched_exposure=controls_per_match,
        limitations=_limitations(evidence_grade),
    )


def _evidence_grade(*, matched_rows: int, unmatched_rows: int) -> str:
    if matched_rows >= 5 and unmatched_rows == 0:
        return "controlled_observational"
    if matched_rows > 0:
        return "fragile_controlled_observational"
    return "exploratory_only"


def _limitations(evidence_grade: str) -> list[str]:
    limitations = [
        "Design is observational and cannot rule out unobserved confounding.",
        "Matching only controls for shared week and block identifiers.",
    ]
    if evidence_grade == "fragile_controlled_observational":
        limitations.append("Matched sample is sparse or leaves exposed rows unmatched.")
    if evidence_grade == "exploratory_only":
        limitations.append("No matched controls are available for this dataset/outcome.")
    return limitations


def _diagnostic_matches_slot(result: dict[str, object], semantic_slot: str) -> bool:
    dataset = result.get("dataset")
    if semantic_slot == "city_week_event_spending":
        return dataset == "city_week"
    if semantic_slot == "msa_week_coverage":
        return dataset == "msa_week"
    if semantic_slot == "identification_risk":
        return result.get("outcome") in OUTCOMES
    return False


def _strongest_level(levels: list[str]) -> str | None:
    if "same_week_same_block_matched" in levels:
        return "same_week_same_block_matched"
    if "unmatched" in levels:
        return "unmatched"
    return None


def _strongest_grade(grades: list[str]) -> str | None:
    order = ["controlled_observational", "fragile_controlled_observational", "exploratory_only"]
    for grade in order:
        if grade in grades:
            return grade
    return None
