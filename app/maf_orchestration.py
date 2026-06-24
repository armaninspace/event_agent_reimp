"""Microsoft Agent Framework orchestration adapter for local and OpenAI-backed runs."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Never

from app.openai_reasoning import OpenAIHypothesisGenerator, OpenAIReasoningConfig
from app.question_forum import DEFAULT_FORUM_PATH, load_question_forum

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message=".*experimental.*")
    from agent_framework import FunctionExecutor, Workflow, WorkflowBuilder, WorkflowContext


EXECUTOR_ID = "codex-governance-summary"
OPENAI_EXECUTOR_ID = "codex-openai-hypothesis-generator"
WORKFLOW_NAME = "codex-thesis-replication-workflow"


@dataclass(frozen=True)
class MAFAdapterReport:
    """Machine-readable evidence from a MAF workflow run."""

    schema_version: str
    framework_name: str
    package_name: str
    package_version: str
    workflow_name: str
    executor_id: str
    input_message: str
    outputs: list[str]
    output_count: int
    reasoning_provider: str
    reasoning_mode: str
    reasoning_model: str | None
    model_calls_performed: bool
    candidate_count: int
    candidate_questions: list[str]
    trace_paths: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable adapter evidence."""
        return asdict(self)


async def summarize_governance_input(message: str, ctx: WorkflowContext[Never, str]) -> None:
    """Deterministic MAF workflow executor used for local regression smoke tests."""
    await ctx.yield_output(f"MAF deterministic orchestration accepted: {message}")


def build_deterministic_maf_workflow() -> Workflow:
    """Build a Microsoft Agent Framework workflow without external model calls."""
    executor = FunctionExecutor(summarize_governance_input, id=EXECUTOR_ID)
    return WorkflowBuilder(
        start_executor=executor,
        output_from=[executor],
        name=WORKFLOW_NAME,
        description="Deterministic adapter proving Microsoft Agent Framework workflow wiring.",
    ).build()


def build_openai_maf_workflow(*, config: OpenAIReasoningConfig, question_forum_path: Path = DEFAULT_FORUM_PATH) -> Workflow:
    """Build a MAF workflow whose executor invokes OpenAI-backed hypothesis generation."""

    async def generate_openai_hypotheses(message: str, ctx: WorkflowContext[Never, str]) -> None:
        forum_records = load_question_forum(question_forum_path) if question_forum_path.exists() else []
        generator = OpenAIHypothesisGenerator(config=config)
        batch = generator.propose(
            turn=1,
            forum_records=forum_records,
            prior_selected_ids=set(),
            prior_selected_forum_ids=set(),
        )
        await ctx.yield_output(
            json.dumps(
                {
                    "message": message,
                    "provider": batch.provider,
                    "mode": batch.mode,
                    "model": batch.model,
                    "model_calls_performed": batch.model_calls_performed,
                    "trace_path": batch.trace_path,
                    "candidate_count": len(batch.proposals),
                    "candidate_questions": [proposal.question for proposal in batch.proposals],
                    "prompt_hash": batch.prompt_hash,
                    "output_hash": batch.output_hash,
                },
                sort_keys=True,
            )
        )

    executor = FunctionExecutor(generate_openai_hypotheses, id=OPENAI_EXECUTOR_ID)
    return WorkflowBuilder(
        start_executor=executor,
        output_from=[executor],
        name=WORKFLOW_NAME,
        description="Microsoft Agent Framework workflow invoking OpenAI-backed hypothesis generation.",
    ).build()


async def run_maf_adapter(
    message: str,
    *,
    reasoning_mode: str = "deterministic",
    openai_model: str | None = None,
    openai_replay_path: Path | None = None,
    openai_trace_dir: Path | None = None,
) -> MAFAdapterReport:
    """Run the MAF workflow and return adapter evidence."""
    config = OpenAIReasoningConfig.from_env(
        mode=reasoning_mode,
        model=openai_model,
        trace_dir=openai_trace_dir,
        replay_path=openai_replay_path,
    )
    workflow = (
        build_deterministic_maf_workflow()
        if config.mode == "deterministic"
        else build_openai_maf_workflow(config=config)
    )
    result = await workflow.run(message)
    outputs = [str(output) for output in result.get_outputs()]
    provider_summary = _summarize_provider_outputs(outputs)
    return MAFAdapterReport(
        schema_version="phase-025.maf-openai-bridge.v1",
        framework_name="Microsoft Agent Framework",
        package_name="agent-framework",
        package_version=importlib.metadata.version("agent-framework"),
        workflow_name=WORKFLOW_NAME,
        executor_id=EXECUTOR_ID if config.mode == "deterministic" else OPENAI_EXECUTOR_ID,
        input_message=message,
        outputs=outputs,
        output_count=len(outputs),
        reasoning_provider=provider_summary["reasoning_provider"],
        reasoning_mode=config.mode,
        reasoning_model=config.model if config.mode in {"openai", "replay"} else None,
        model_calls_performed=provider_summary["model_calls_performed"],
        candidate_count=provider_summary["candidate_count"],
        candidate_questions=provider_summary["candidate_questions"],
        trace_paths=provider_summary["trace_paths"],
    )


def run_maf_adapter_sync(
    message: str,
    *,
    reasoning_mode: str = "deterministic",
    openai_model: str | None = None,
    openai_replay_path: Path | None = None,
    openai_trace_dir: Path | None = None,
) -> MAFAdapterReport:
    """Run the adapter from synchronous scripts/tests."""
    return asyncio.run(
        run_maf_adapter(
            message,
            reasoning_mode=reasoning_mode,
            openai_model=openai_model,
            openai_replay_path=openai_replay_path,
            openai_trace_dir=openai_trace_dir,
        )
    )


def write_maf_adapter_smoke(report: MAFAdapterReport, output_dir: Path) -> tuple[Path, Path]:
    """Write adapter smoke JSON and Markdown artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "maf_adapter_smoke.json"
    markdown_path = output_dir / "maf_adapter_smoke.md"
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_maf_adapter_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def render_maf_adapter_markdown(report: MAFAdapterReport) -> str:
    """Render adapter evidence as Markdown."""
    return "\n".join(
        [
            "# Microsoft Agent Framework Adapter Smoke",
            "",
            f"Schema: {report.schema_version}",
            f"Framework: {report.framework_name}",
            f"Package: {report.package_name} {report.package_version}",
            f"Workflow: {report.workflow_name}",
            f"Executor: {report.executor_id}",
            f"Reasoning provider: {report.reasoning_provider}",
            f"Reasoning mode: {report.reasoning_mode}",
            f"Reasoning model: {report.reasoning_model}",
            f"Model calls performed: {report.model_calls_performed}",
            f"Candidate count: {report.candidate_count}",
            f"Output count: {report.output_count}",
            "",
            "## Candidate Questions",
            "",
            *[f"- {question}" for question in report.candidate_questions],
            "",
            "## Outputs",
            "",
            *[f"- {output}" for output in report.outputs],
            "",
        ]
    )


def _summarize_provider_outputs(outputs: list[str]) -> dict[str, object]:
    if not outputs:
        return _deterministic_provider_summary()
    try:
        payload = json.loads(outputs[0])
    except json.JSONDecodeError:
        return _deterministic_provider_summary()
    if not isinstance(payload, dict) or payload.get("provider") != "openai":
        return _deterministic_provider_summary()
    candidate_questions = payload.get("candidate_questions")
    trace_path = payload.get("trace_path")
    return {
        "reasoning_provider": "openai",
        "model_calls_performed": bool(payload.get("model_calls_performed")),
        "candidate_count": int(payload.get("candidate_count", 0)),
        "candidate_questions": [str(question) for question in candidate_questions]
        if isinstance(candidate_questions, list)
        else [],
        "trace_paths": [str(trace_path)] if isinstance(trace_path, str) and trace_path else [],
    }


def _deterministic_provider_summary() -> dict[str, object]:
    return {
        "reasoning_provider": "deterministic",
        "model_calls_performed": False,
        "candidate_count": 0,
        "candidate_questions": [],
        "trace_paths": [],
    }
