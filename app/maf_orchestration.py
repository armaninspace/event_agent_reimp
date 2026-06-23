"""Microsoft Agent Framework orchestration adapter for deterministic local runs."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Never

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message=".*experimental.*")
    from agent_framework import FunctionExecutor, Workflow, WorkflowBuilder, WorkflowContext


EXECUTOR_ID = "codex-governance-summary"
WORKFLOW_NAME = "codex-thesis-replication-workflow"


@dataclass(frozen=True)
class MAFAdapterReport:
    """Machine-readable evidence from a deterministic MAF workflow run."""

    schema_version: str
    framework_name: str
    package_name: str
    package_version: str
    workflow_name: str
    executor_id: str
    input_message: str
    outputs: list[str]
    output_count: int
    model_calls_performed: bool

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


async def run_maf_adapter(message: str) -> MAFAdapterReport:
    """Run the deterministic MAF workflow and return adapter evidence."""
    workflow = build_deterministic_maf_workflow()
    result = await workflow.run(message)
    outputs = [str(output) for output in result.get_outputs()]
    return MAFAdapterReport(
        schema_version="phase-016.maf-adapter.v1",
        framework_name="Microsoft Agent Framework",
        package_name="agent-framework",
        package_version=importlib.metadata.version("agent-framework"),
        workflow_name=WORKFLOW_NAME,
        executor_id=EXECUTOR_ID,
        input_message=message,
        outputs=outputs,
        output_count=len(outputs),
        model_calls_performed=False,
    )


def run_maf_adapter_sync(message: str) -> MAFAdapterReport:
    """Run the deterministic adapter from synchronous scripts/tests."""
    return asyncio.run(run_maf_adapter(message))


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
            f"Model calls performed: {report.model_calls_performed}",
            f"Output count: {report.output_count}",
            "",
            "## Outputs",
            "",
            *[f"- {output}" for output in report.outputs],
            "",
        ]
    )
