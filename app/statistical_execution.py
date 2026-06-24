"""Attach statistical execution evidence to governed candidate turns."""

from __future__ import annotations

import json
from pathlib import Path

from app.causal_diagnostics import build_causal_design_report, diagnostics_for_semantic_slot, summarize_designs
from app.multiple_testing import build_correction_report


def build_statistical_execution_report(reference_dir: Path) -> dict[str, object]:
    """Build the reusable statistical execution report for a friends-loop run."""
    correction_report = build_correction_report(reference_dir)
    causal_design_report = build_causal_design_report(reference_dir)
    return {
        "schema_version": "phase-026.statistical-execution.v2",
        "source_report_schema": correction_report["schema_version"],
        "causal_design_schema": causal_design_report["schema_version"],
        "method": correction_report["method"],
        "results": correction_report["results"],
        "causal_design": causal_design_report,
    }


def evidence_for_candidate(candidate: dict[str, object], execution_report: dict[str, object]) -> dict[str, object]:
    """Return candidate-scoped statistical evidence."""
    semantic_slot = str(candidate["semantic_slot"])
    results = [
        result
        for result in execution_report["results"]
        if isinstance(result, dict) and _result_matches_slot(result, semantic_slot)
    ]
    adjusted_values = [
        result["adjusted_p_value"]
        for result in results
        if isinstance(result.get("adjusted_p_value"), int | float)
    ]
    causal_design = summarize_designs(
        diagnostics_for_semantic_slot(
            execution_report.get("causal_design", {}),
            semantic_slot,
        )
    )
    return {
        "schema_version": execution_report["schema_version"],
        "method": execution_report["method"],
        "candidate_id": candidate["candidate_id"],
        "semantic_slot": semantic_slot,
        "result_count": len(results),
        "result_ids": [result["result_id"] for result in results],
        "min_adjusted_p_value": min(adjusted_values) if adjusted_values else None,
        "has_adjusted_significance": any(value < 0.05 for value in adjusted_values),
        "results": results,
        "causal_design": causal_design,
        "caveats": [
            "Statistical evidence is observational; causal-design diagnostics do not prove causality.",
            "Adjusted p-values do not establish causality.",
        ],
    }


def write_statistical_execution_smoke(report: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    """Write statistical execution smoke JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "statistical_execution_smoke.json"
    markdown_path = output_dir / "statistical_execution_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_statistical_execution_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_statistical_execution_markdown(report: dict[str, object]) -> str:
    """Render statistical execution evidence as Markdown."""
    lines = [
        "# Statistical Execution Smoke",
        "",
        f"Schema: {report['schema_version']}",
        f"Source schema: {report['source_report_schema']}",
        f"Method: {report['method']}",
        f"Causal design schema: {report.get('causal_design_schema')}",
        f"Result count: {len(report['results'])}",
        "",
    ]
    for result in report["results"]:
        lines.extend(
            [
                f"## {result['result_id']}",
                "",
                f"- P-value: {result['p_value']}",
                f"- Adjusted p-value: {result['adjusted_p_value']}",
                f"- Status: {result['status']}",
                "",
            ]
        )
    return "\n".join(lines)


def _result_matches_slot(result: dict[str, object], semantic_slot: str) -> bool:
    dataset = result.get("dataset")
    if semantic_slot == "city_week_event_spending":
        return dataset == "city_week"
    if semantic_slot == "msa_week_coverage":
        return dataset == "msa_week"
    if semantic_slot == "identification_risk":
        return result.get("family") == "matched"
    return False
