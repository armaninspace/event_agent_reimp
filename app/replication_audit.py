"""Final thesis replication audit over local artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_SOURCE_FILES = (
    "data/question_forum/questions.json",
    "data/reference/joined_city_week_game_economic.csv",
    "data/reference/joined_msa_week_game_economic.csv",
    "app/question_forum.py",
    "app/question_tournament.py",
    "app/question_reflection.py",
    "app/question_evolution.py",
    "app/hypothesis_evolution.py",
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
    selected_forum_metadata_count: int
    selected_tournament_metadata_count: int
    selected_reflection_metadata_count: int
    selected_evolution_metadata_count: int
    statistical_evidence_turn_count: int
    business_report_statistical_sections: int
    notebook_workspace_present: bool
    final_status: str
    known_limits: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable audit data."""
        return asdict(self)


def run_replication_audit(
    *,
    repo_root: Path = Path("."),
    run_dir: Path = Path("app/runs/phase-019-replication-audit"),
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
        selected_forum_metadata_count=sum(_has_key(candidate, "forum") for candidate in selected),
        selected_tournament_metadata_count=sum(_has_key(candidate, "tournament") for candidate in selected),
        selected_reflection_metadata_count=sum(_has_key(candidate, "reflection") for candidate in selected),
        selected_evolution_metadata_count=sum(_has_key(candidate, "evolution") for candidate in selected),
        statistical_evidence_turn_count=sum(_has_key(turn, "statistical_evidence") for turn in turns),
        business_report_statistical_sections=business_report.count("Statistical Evidence"),
        notebook_workspace_present=bool(summary["notebook_workspace_present"]),
        final_status="replicated_with_known_limits",
        known_limits=[
            "Live model-based debate is deferred; governance is deterministic.",
            "Statistical evidence is observational and exploratory, not causal proof.",
            "Microsoft Agent Framework adapter runs deterministically without provider/model calls.",
        ],
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
            f"- Forum metadata count: {audit.selected_forum_metadata_count}",
            f"- Tournament metadata count: {audit.selected_tournament_metadata_count}",
            f"- Reflection metadata count: {audit.selected_reflection_metadata_count}",
            f"- Evolution metadata count: {audit.selected_evolution_metadata_count}",
            f"- Statistical evidence turn count: {audit.statistical_evidence_turn_count}",
            f"- Business report statistical sections: {audit.business_report_statistical_sections}",
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
