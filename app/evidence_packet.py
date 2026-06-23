"""Static evidence packet generation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.agent_runtime import get_agent_runtime_metadata, platform_summary
from app.data_profile import CsvDataProfile, profile_final_runtime_files


DEFAULT_QUESTION = "Do big sports crowds actually turn into more local spending?"


@dataclass(frozen=True)
class ArtifactPaths:
    """Paths written by an evidence packet run."""

    json_path: Path
    markdown_path: Path


def build_static_evidence_packet(
    *,
    reference_dir: Path,
    question: str = DEFAULT_QUESTION,
    generated_at: datetime | None = None,
) -> dict[str, object]:
    """Build a deterministic Phase 001 evidence packet."""
    timestamp = (generated_at or datetime.now(UTC)).replace(microsecond=0).isoformat()
    data_profiles = profile_final_runtime_files(reference_dir)
    runtime_metadata = get_agent_runtime_metadata().to_dict()

    city_profile = data_profiles["city_week"]
    msa_profile = data_profiles["msa_week"]
    result = {
        "summary": "Final runtime files are present and suitable for static packet generation.",
        "city_week_rows": city_profile.row_count,
        "msa_week_rows": msa_profile.row_count,
        "city_week_has_game_rows": city_profile.has_game_rows,
        "msa_week_has_game_rows": msa_profile.has_game_rows,
        "all_required_columns_present": all(not profile.missing_columns for profile in data_profiles.values()),
        "all_required_values_present": all(
            sum(profile.missing_required_values.values()) == 0 for profile in data_profiles.values()
        ),
    }

    return {
        "schema_version": "phase-001.static-evidence-packet.v1",
        "generated_at": timestamp,
        "question": question,
        "hypothesis": {
            "headline": "Sports event exposure is associated with measurable local economic activity.",
            "unit": "city-week and MSA-week",
            "exposure": "has_game / game_count",
            "outcomes": ["revenue_all", "merchants_all"],
            "claim_boundary": "descriptive readiness check only; no causal or inferential claim",
        },
        "design": {
            "phase": "phase-001-static-evidence-packet",
            "method": "deterministic CSV profiling and packet generation",
            "data_sources": [profile.path for profile in data_profiles.values()],
            "runtime": "Python with Microsoft Agent Framework dependency available for later agent phases",
        },
        "data_profile": {name: profile.to_dict() for name, profile in data_profiles.items()},
        "result": result,
        "caveat": (
            "This packet verifies data readiness and artifact generation only. It does not run matched controls, "
            "multiple-testing correction, notebook execution, or a 20-turn agent regression."
        ),
        "runtime_metadata": {
            **runtime_metadata,
            "platform": platform_summary(),
        },
        "audit_log": [
            {
                "event_type": "packet.created",
                "summary": "Created deterministic static evidence packet.",
                "time": timestamp,
            },
            {
                "event_type": "data.profiled",
                "summary": "Profiled final city-week and MSA-week runtime CSV files.",
                "time": timestamp,
            },
            {
                "event_type": "agent_runtime.checked",
                "summary": "Checked Microsoft Agent Framework package metadata without making external calls.",
                "time": timestamp,
            },
        ],
    }


def write_evidence_packet(packet: dict[str, object], output_dir: Path) -> ArtifactPaths:
    """Write evidence packet JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "experiment_packet.json"
    markdown_path = output_dir / "experiment_packet.md"

    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_packet_markdown(packet), encoding="utf-8")

    return ArtifactPaths(json_path=json_path, markdown_path=markdown_path)


def render_packet_markdown(packet: dict[str, object]) -> str:
    """Render a compact Markdown view of an evidence packet."""
    result = packet["result"]
    runtime = packet["runtime_metadata"]
    assert isinstance(result, dict)
    assert isinstance(runtime, dict)

    return "\n".join(
        [
            "# Static Evidence Packet",
            "",
            f"Generated: {packet['generated_at']}",
            "",
            f"Question: {packet['question']}",
            "",
            "## Result",
            "",
            f"- Summary: {result['summary']}",
            f"- City-week rows: {result['city_week_rows']}",
            f"- MSA-week rows: {result['msa_week_rows']}",
            f"- Required columns present: {result['all_required_columns_present']}",
            f"- Required values present: {result['all_required_values_present']}",
            "",
            "## Runtime",
            "",
            f"- Language: {runtime['language']}",
            f"- Framework: {runtime['framework_name']}",
            f"- Package: {runtime['package_name']} {runtime['package_version']}",
            f"- Import available: {runtime['import_available']}",
            "",
            "## Caveat",
            "",
            str(packet["caveat"]),
            "",
        ]
    )
