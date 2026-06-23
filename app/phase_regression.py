"""Phase regression gate for deterministic friends-loop runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.friends_loop import run_friends_question_loop
from app.hypothesis_routing import count_workflow_statistical_misroutes
from app.notebook_execution import execute_workspace_lightweight, execute_workspace_nbclient
from app.notebook_workspace import summarize_workspace


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
    current_required_artifacts_exist: bool
    artifact_checks: dict[str, bool]
    notebook_workspace_present: bool
    notebook_workspace: dict[str, object]
    notebook_execution: dict[str, object]
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
) -> tuple[PhaseRegressionResult, Path]:
    """Run a deterministic phase regression and write its summary."""
    phase_dir = runs_dir / phase_id
    loop_dir = phase_dir / "friends-question-loop"
    notebook_dir = phase_dir / "notebooks"
    session = run_friends_question_loop(
        turn_count=turns,
        output_dir=loop_dir,
        reference_dir=reference_dir,
        notebook_dir=notebook_dir,
    )
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
    selected_candidates_have_required_metadata = all(
        isinstance(candidate, dict)
        and all(
            key in candidate
            for key in ("candidate_id", "question", "rationale", "semantic_slot", "score", "caveat", "forum")
        )
        and _has_forum_metadata(candidate["forum"])
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
        current_required_artifacts_exist=all(artifact_checks.values()),
        artifact_checks=artifact_checks,
        notebook_workspace_present=notebook_workspace_present,
        notebook_workspace=notebook_workspace,
        notebook_execution=notebook_execution,
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
