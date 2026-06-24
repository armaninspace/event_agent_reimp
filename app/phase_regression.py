"""Phase regression gate for deterministic friends-loop runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.data_snapshot import build_reference_snapshot, snapshot_is_complete
from app.friends_loop import run_friends_question_loop
from app.hypothesis_routing import count_workflow_statistical_misroutes
from app.multiple_testing import build_correction_report
from app.notebook_execution import execute_workspace_lightweight, execute_workspace_nbclient
from app.notebook_workspace import summarize_workspace, write_correction_notebook
from app.notebook_knowledge_base import write_notebook_knowledge_base


CURRENT_REQUIRED_ARTIFACTS = (
    "session_json",
    "session_markdown",
    "telemetry_json",
    "discovery_decision_summary",
    "business_evidence_report",
    "playback_ui",
)


@dataclass(frozen=True)
class PhaseRegressionResult:
    """Machine-readable phase regression summary."""

    schema_version: str
    phase_id: str
    requested_turns: int
    completed_workflows: int
    stopped_early: bool
    workflow_task_statistical_misroutes: int
    selected_candidate_count: int
    selected_candidates_have_required_metadata: bool
    turns_have_statistical_evidence: bool
    turns_have_causal_design_diagnostics: bool
    data_snapshot_complete: bool
    data_snapshot: dict[str, object]
    correction_notebook_present: bool
    correction_notebook_executed: bool
    current_required_artifacts_exist: bool
    artifact_checks: dict[str, bool]
    notebook_workspace_present: bool
    notebook_workspace: dict[str, object]
    notebook_execution: dict[str, object]
    notebook_knowledge_present: bool
    notebook_knowledge: dict[str, object]
    prior_notebook_knowledge_entry_count: int
    prior_knowledge_duplicate_candidate_count: int
    prior_knowledge_evolved_duplicate_candidate_count: int
    selected_semantic_slot_counts: dict[str, int]
    selected_unique_semantic_slot_count: int
    reasoning_provider: str
    reasoning_mode: str
    selected_candidates_have_openai_reasoning: bool
    openai_model_calls_performed: bool
    telemetry_event_count: int
    telemetry_event_types: list[str]
    known_future_artifacts: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable summary data."""
        return asdict(self)


def run_phase_regression(
    *,
    phase_id: str,
    turns: int = 20,
    runs_dir: Path = Path("app/runs"),
    reference_dir: Path = Path("data/reference"),
    notebook_execution_backend: str = "lightweight",
    reasoning_mode: str = "deterministic",
    openai_model: str | None = None,
    openai_replay_path: Path | None = None,
    prior_notebook_knowledge_path: Path | None = None,
) -> tuple[PhaseRegressionResult, Path]:
    """Run a deterministic phase regression and write its summary."""
    phase_dir = runs_dir / phase_id
    loop_dir = phase_dir / "friends-question-loop"
    notebook_dir = phase_dir / "notebooks"
    data_snapshot = build_reference_snapshot(reference_dir)
    session = run_friends_question_loop(
        turn_count=turns,
        output_dir=loop_dir,
        reference_dir=reference_dir,
        notebook_dir=notebook_dir,
        reasoning_mode=reasoning_mode,
        openai_model=openai_model,
        openai_replay_path=openai_replay_path,
        prior_notebook_knowledge_path=prior_notebook_knowledge_path,
    )
    correction_report = build_correction_report(reference_dir)
    write_correction_notebook(notebook_dir, correction_report=correction_report)
    artifact_paths = session["artifact_paths"]
    assert isinstance(artifact_paths, dict)

    telemetry_path = Path(str(artifact_paths["telemetry_json"]))
    telemetry = json.loads(telemetry_path.read_text(encoding="utf-8"))
    artifact_checks = {
        name: Path(str(path)).exists()
        for name, path in artifact_paths.items()
        if name in CURRENT_REQUIRED_ARTIFACTS
    }
    turns_data = session["turns"]
    assert isinstance(turns_data, list)
    selected_candidates = [turn["selected_candidate"] for turn in turns_data]
    selected_reasoning = [
        candidate.get("reasoning") for candidate in selected_candidates if isinstance(candidate, dict)
    ]
    selected_candidates_have_openai_reasoning = bool(selected_reasoning) and all(
        isinstance(reasoning, dict) and reasoning.get("provider") == "openai" for reasoning in selected_reasoning
    )
    openai_model_calls_performed = any(
        isinstance(reasoning, dict) and bool(reasoning.get("model_calls_performed"))
        for reasoning in selected_reasoning
    )
    session_summary = session["session_summary"]
    assert isinstance(session_summary, dict)
    turns_have_statistical_evidence = all(
        isinstance(turn, dict) and _has_statistical_evidence(turn.get("statistical_evidence"))
        for turn in turns_data
    )
    turns_have_causal_design_diagnostics = all(
        isinstance(turn, dict) and _has_causal_design(turn.get("statistical_evidence"))
        for turn in turns_data
    )
    selected_candidates_have_required_metadata = all(
        isinstance(candidate, dict)
        and all(
            key in candidate
            for key in (
                "candidate_id",
                "question",
                "rationale",
                "semantic_slot",
                "score",
                "caveat",
                "forum",
                "tournament",
                "reflection",
                "evolution",
            )
        )
        and _has_forum_metadata(candidate["forum"])
        and _has_tournament_metadata(candidate["tournament"])
        and _has_reflection_metadata(candidate["reflection"])
        and _has_evolution_metadata(candidate["evolution"])
        for candidate in selected_candidates
    )
    if notebook_execution_backend == "lightweight":
        notebook_execution = execute_workspace_lightweight(notebook_dir)
        execution_ok = bool(notebook_execution["all_lightweight_executed"])
        executed_count_key = "lightweight_executed_count"
    elif notebook_execution_backend == "nbclient":
        notebook_execution = execute_workspace_nbclient(notebook_dir)
        execution_ok = bool(notebook_execution["all_nbclient_executed"])
        executed_count_key = "nbclient_executed_count"
    else:
        raise ValueError(f"Unsupported notebook execution backend: {notebook_execution_backend}")
    _, _, notebook_knowledge = write_notebook_knowledge_base(notebook_dir)
    notebook_workspace = summarize_workspace(notebook_dir)
    notebook_workspace_present = (
        bool(notebook_workspace["wiki_files_exist"])
        and notebook_workspace["notebook_count"] == turns
        and notebook_workspace["markdown_export_count"] == turns
        and notebook_workspace[executed_count_key] == turns
        and execution_ok
    )

    summary = PhaseRegressionResult(
        schema_version="phase-004.phase-regression-summary.v1",
        phase_id=phase_id,
        requested_turns=turns,
        completed_workflows=len(turns_data),
        stopped_early=False,
        workflow_task_statistical_misroutes=count_workflow_statistical_misroutes(turns_data),
        selected_candidate_count=len(selected_candidates),
        selected_candidates_have_required_metadata=selected_candidates_have_required_metadata,
        turns_have_statistical_evidence=turns_have_statistical_evidence,
        turns_have_causal_design_diagnostics=turns_have_causal_design_diagnostics,
        data_snapshot_complete=snapshot_is_complete(data_snapshot),
        data_snapshot=data_snapshot,
        correction_notebook_present=bool(notebook_workspace["correction_notebook_exists"])
        and bool(notebook_workspace["correction_markdown_exists"]),
        correction_notebook_executed=bool(notebook_workspace["correction_notebook_executed"])
        and bool(notebook_execution["correction_notebook_executed"]),
        current_required_artifacts_exist=all(artifact_checks.values()),
        artifact_checks=artifact_checks,
        notebook_workspace_present=notebook_workspace_present,
        notebook_workspace=notebook_workspace,
        notebook_execution=notebook_execution,
        notebook_knowledge_present=_has_notebook_knowledge(notebook_knowledge, expected_count=turns),
        notebook_knowledge=notebook_knowledge,
        prior_notebook_knowledge_entry_count=int(session_summary.get("prior_notebook_knowledge_entry_count", 0)),
        prior_knowledge_duplicate_candidate_count=int(session_summary.get("prior_knowledge_duplicate_candidate_count", 0)),
        prior_knowledge_evolved_duplicate_candidate_count=int(
            session_summary.get("prior_knowledge_evolved_duplicate_candidate_count", 0)
        ),
        selected_semantic_slot_counts=_semantic_slot_counts(session_summary.get("selected_semantic_slot_counts")),
        selected_unique_semantic_slot_count=int(session_summary.get("selected_unique_semantic_slot_count", 0)),
        reasoning_provider=str(session_summary.get("reasoning_provider", "deterministic")),
        reasoning_mode=str(session_summary.get("reasoning_mode", "deterministic")),
        selected_candidates_have_openai_reasoning=selected_candidates_have_openai_reasoning,
        openai_model_calls_performed=openai_model_calls_performed,
        telemetry_event_count=len(telemetry),
        telemetry_event_types=sorted({event["event_type"] for event in telemetry}),
        known_future_artifacts={
            "statistical_results": "deferred until statistical routing phase",
        },
    )
    summary_path = phase_dir / "phase_regression_summary.json"
    summary_path.write_text(json.dumps(summary.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary, summary_path


def _has_forum_metadata(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {
        "question_id",
        "kind",
        "persona",
        "priority",
        "popularity",
        "source_url",
        "status",
        "tags",
    }
    return required <= value.keys()


def _has_tournament_metadata(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {"rank", "wins", "losses", "score", "component_scores", "transcript"}
    return required <= value.keys()


def _has_reflection_metadata(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {"status", "misleading_risk", "weakening_evidence", "answerability"}
    return required <= value.keys()


def _has_evolution_metadata(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {"action", "source_question_id", "parent_question_id", "child_question_id", "evolved_question", "rationale"}
    return required <= value.keys()


def _has_statistical_evidence(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {
        "schema_version",
        "method",
        "candidate_id",
        "semantic_slot",
        "result_count",
        "result_ids",
        "has_adjusted_significance",
        "results",
        "caveats",
        "causal_design",
    }
    return required <= value.keys()


def _has_causal_design(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    causal_design = value.get("causal_design")
    if not isinstance(causal_design, dict):
        return False
    required = {"schema_version", "design_count", "evidence_grade", "diagnostic_ids", "diagnostics", "claim_boundary"}
    return required <= causal_design.keys() and int(causal_design.get("design_count", 0)) >= 1


def _has_notebook_knowledge(value: object, *, expected_count: int) -> bool:
    if not isinstance(value, dict):
        return False
    return (
        value.get("schema_version") == "phase-027.notebook-knowledge-base.v1"
        and int(value.get("entry_count", 0)) == expected_count
        and isinstance(value.get("latest_seed_question"), str)
    )


def _semantic_slot_counts(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    return {str(key): int(count) for key, count in value.items() if isinstance(count, int)}
