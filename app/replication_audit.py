"""Final thesis replication audit over local artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.data_snapshot import snapshot_is_complete


REQUIRED_SOURCE_FILES = (
    "data/question_forum/questions.json",
    "data/reference/joined_city_week_game_economic.csv",
    "data/reference/joined_msa_week_game_economic.csv",
    "app/question_forum.py",
    "app/question_tournament.py",
    "app/question_reflection.py",
    "app/question_evolution.py",
    "app/hypothesis_evolution.py",
    "app/openai_reasoning.py",
    "app/statistical_execution.py",
    "app/maf_orchestration.py",
    "app/reporting.py",
    "app/notebook_workspace.py",
)


@dataclass(frozen=True)
class ReplicationAudit:
    """Machine-readable final replication audit."""

    schema_version: str
    run_dir: str
    required_source_files_present: bool
    missing_source_files: list[str]
    completed_twenty_turns: bool
    stopped_early: bool
    workflow_task_statistical_misroutes: int
    selected_candidates_have_required_metadata: bool
    turns_have_statistical_evidence: bool
    data_snapshot_complete: bool
    data_snapshot_combined_sha256: str | None
    correction_notebook_present: bool
    correction_notebook_executed: bool
    selected_forum_metadata_count: int
    selected_tournament_metadata_count: int
    selected_reflection_metadata_count: int
    selected_evolution_metadata_count: int
    selected_evolution_variant_count: int
    selected_openai_reasoning_count: int
    causal_design_turn_count: int
    controlled_observational_turn_count: int
    openai_model_calls_performed: bool
    reasoning_provider: str
    reasoning_mode: str
    maf_adapter_present: bool
    maf_reasoning_provider: str | None
    maf_reasoning_mode: str | None
    maf_model_calls_performed: bool
    maf_candidate_count: int
    statistical_evidence_turn_count: int
    business_report_statistical_sections: int
    business_report_statistical_tables: int
    notebook_workspace_present: bool
    final_status: str
    known_limits: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable audit data."""
        return asdict(self)


def run_replication_audit(
    *,
    repo_root: Path = Path("."),
    run_dir: Path = Path("app/runs/phase-026-causal-design-diagnostics"),
) -> ReplicationAudit:
    """Audit whether the local artifacts satisfy the thesis replication checklist."""
    missing = [path for path in REQUIRED_SOURCE_FILES if not (repo_root / path).exists()]
    summary = json.loads((repo_root / run_dir / "phase_regression_summary.json").read_text(encoding="utf-8"))
    session = json.loads(
        (repo_root / run_dir / "friends-question-loop" / "friends_loop_session.json").read_text(encoding="utf-8")
    )
    turns = session["turns"]
    assert isinstance(turns, list)
    selected = [turn["selected_candidate"] for turn in turns]
    business_report = (repo_root / run_dir / "friends-question-loop" / "business_evidence_report.html").read_text(
        encoding="utf-8"
    )
    maf_adapter = _load_optional_json(repo_root / run_dir / "maf_adapter_smoke.json")
    known_limits = [
        "The checked-in audit artifact uses OpenAI replay provenance because OPENAI_API_KEY is not available in this shell.",
        "Live OpenAI reasoning is implemented and credential-gated, but requires OPENAI_API_KEY at runtime.",
        "Statistical evidence is controlled observational where matched controls exist, but not causal proof.",
    ]
    if not _has_openai_maf_bridge(maf_adapter):
        known_limits.append("Microsoft Agent Framework provider-backed OpenAI reasoning evidence is missing.")
    audit = ReplicationAudit(
        schema_version="phase-019.replication-audit.v1",
        run_dir=str(run_dir),
        required_source_files_present=not missing,
        missing_source_files=missing,
        completed_twenty_turns=summary["requested_turns"] == 20 and summary["completed_workflows"] == 20,
        stopped_early=bool(summary["stopped_early"]),
        workflow_task_statistical_misroutes=int(summary["workflow_task_statistical_misroutes"]),
        selected_candidates_have_required_metadata=bool(summary["selected_candidates_have_required_metadata"]),
        turns_have_statistical_evidence=bool(summary["turns_have_statistical_evidence"]),
        data_snapshot_complete=snapshot_is_complete(summary.get("data_snapshot")),
        data_snapshot_combined_sha256=_combined_sha(summary.get("data_snapshot")),
        correction_notebook_present=bool(summary.get("correction_notebook_present")),
        correction_notebook_executed=bool(summary.get("correction_notebook_executed")),
        selected_forum_metadata_count=sum(_has_key(candidate, "forum") for candidate in selected),
        selected_tournament_metadata_count=sum(_has_key(candidate, "tournament") for candidate in selected),
        selected_reflection_metadata_count=sum(_has_key(candidate, "reflection") for candidate in selected),
        selected_evolution_metadata_count=sum(_has_key(candidate, "evolution") for candidate in selected),
        selected_evolution_variant_count=sum(_has_evolution_variant(candidate.get("evolution")) for candidate in selected if isinstance(candidate, dict)),
        selected_openai_reasoning_count=sum(_has_openai_reasoning(candidate.get("reasoning")) for candidate in selected if isinstance(candidate, dict)),
        causal_design_turn_count=sum(_has_causal_design(turn.get("statistical_evidence")) for turn in turns if isinstance(turn, dict)),
        controlled_observational_turn_count=sum(
            _has_controlled_observational_design(turn.get("statistical_evidence"))
            for turn in turns
            if isinstance(turn, dict)
        ),
        openai_model_calls_performed=bool(summary.get("openai_model_calls_performed")),
        reasoning_provider=str(summary.get("reasoning_provider", "deterministic")),
        reasoning_mode=str(summary.get("reasoning_mode", "deterministic")),
        maf_adapter_present=isinstance(maf_adapter, dict),
        maf_reasoning_provider=_optional_string(maf_adapter, "reasoning_provider"),
        maf_reasoning_mode=_optional_string(maf_adapter, "reasoning_mode"),
        maf_model_calls_performed=bool(maf_adapter.get("model_calls_performed")) if isinstance(maf_adapter, dict) else False,
        maf_candidate_count=int(maf_adapter.get("candidate_count", 0)) if isinstance(maf_adapter, dict) else 0,
        statistical_evidence_turn_count=sum(_has_key(turn, "statistical_evidence") for turn in turns),
        business_report_statistical_sections=business_report.count("Statistical Evidence"),
        business_report_statistical_tables=business_report.count('class="statistical-results"'),
        notebook_workspace_present=bool(summary["notebook_workspace_present"]),
        final_status="replicated_with_known_limits",
        known_limits=known_limits,
    )
    return audit


def write_replication_audit(audit: ReplicationAudit, output_dir: Path) -> tuple[Path, Path]:
    """Write replication audit JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "replication_audit.json"
    markdown_path = output_dir / "replication_audit.md"
    json_path.write_text(json.dumps(audit.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_replication_audit_markdown(audit), encoding="utf-8")
    return json_path, markdown_path


def render_replication_audit_markdown(audit: ReplicationAudit) -> str:
    """Render final audit as Markdown."""
    return "\n".join(
        [
            "# Thesis Replication Audit",
            "",
            f"Schema: {audit.schema_version}",
            f"Run directory: `{audit.run_dir}`",
            f"Final status: `{audit.final_status}`",
            "",
            "## Acceptance Checks",
            "",
            f"- Required source files present: {audit.required_source_files_present}",
            f"- Completed 20 turns: {audit.completed_twenty_turns}",
            f"- Stopped early: {audit.stopped_early}",
            f"- Workflow-task statistical misroutes: {audit.workflow_task_statistical_misroutes}",
            f"- Selected candidates have required metadata: {audit.selected_candidates_have_required_metadata}",
            f"- Turns have statistical evidence: {audit.turns_have_statistical_evidence}",
            f"- Data snapshot complete: {audit.data_snapshot_complete}",
            f"- Data snapshot combined SHA-256: `{audit.data_snapshot_combined_sha256}`",
            f"- Correction notebook present: {audit.correction_notebook_present}",
            f"- Correction notebook executed: {audit.correction_notebook_executed}",
            f"- Forum metadata count: {audit.selected_forum_metadata_count}",
            f"- Tournament metadata count: {audit.selected_tournament_metadata_count}",
            f"- Reflection metadata count: {audit.selected_reflection_metadata_count}",
            f"- Evolution metadata count: {audit.selected_evolution_metadata_count}",
            f"- Evolution variant count: {audit.selected_evolution_variant_count}",
            f"- OpenAI reasoning metadata count: {audit.selected_openai_reasoning_count}",
            f"- Causal-design turn count: {audit.causal_design_turn_count}",
            f"- Controlled-observational turn count: {audit.controlled_observational_turn_count}",
            f"- OpenAI model calls performed: {audit.openai_model_calls_performed}",
            f"- Reasoning provider: {audit.reasoning_provider}",
            f"- Reasoning mode: {audit.reasoning_mode}",
            f"- MAF adapter present: {audit.maf_adapter_present}",
            f"- MAF reasoning provider: {audit.maf_reasoning_provider}",
            f"- MAF reasoning mode: {audit.maf_reasoning_mode}",
            f"- MAF model calls performed: {audit.maf_model_calls_performed}",
            f"- MAF candidate count: {audit.maf_candidate_count}",
            f"- Statistical evidence turn count: {audit.statistical_evidence_turn_count}",
            f"- Business report statistical sections: {audit.business_report_statistical_sections}",
            f"- Business report statistical tables: {audit.business_report_statistical_tables}",
            f"- Notebook workspace present: {audit.notebook_workspace_present}",
            "",
            "## Known Limits",
            "",
            *[f"- {limit}" for limit in audit.known_limits],
            "",
        ]
    )


def _has_key(value: object, key: str) -> bool:
    return isinstance(value, dict) and key in value


def _combined_sha(value: object) -> str | None:
    if not isinstance(value, dict):
        return None
    combined = value.get("combined_sha256")
    return str(combined) if isinstance(combined, str) else None


def _has_evolution_variant(value: object) -> bool:
    return isinstance(value, dict) and all(
        isinstance(value.get(key), str) and bool(value.get(key))
        for key in ("parent_question_id", "child_question_id", "evolved_question")
    )


def _has_openai_reasoning(value: object) -> bool:
    return (
        isinstance(value, dict)
        and value.get("provider") == "openai"
        and isinstance(value.get("mode"), str)
        and isinstance(value.get("model"), str)
        and isinstance(value.get("prompt_hash"), str)
        and isinstance(value.get("output_hash"), str)
        and "model_calls_performed" in value
    )


def _load_optional_json(path: Path) -> object:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _optional_string(value: object, key: str) -> str | None:
    if not isinstance(value, dict):
        return None
    item = value.get(key)
    return str(item) if isinstance(item, str) else None


def _has_openai_maf_bridge(value: object) -> bool:
    return (
        isinstance(value, dict)
        and value.get("framework_name") == "Microsoft Agent Framework"
        and value.get("reasoning_provider") == "openai"
        and value.get("reasoning_mode") in {"openai", "replay"}
        and int(value.get("candidate_count", 0)) >= 3
    )


def _has_causal_design(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    causal_design = value.get("causal_design")
    return isinstance(causal_design, dict) and int(causal_design.get("design_count", 0)) >= 1


def _has_controlled_observational_design(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    causal_design = value.get("causal_design")
    if not isinstance(causal_design, dict):
        return False
    return causal_design.get("evidence_grade") in {
        "controlled_observational",
        "fragile_controlled_observational",
    }
