from pathlib import Path

from app.maf_orchestration import run_maf_adapter_sync, write_maf_adapter_smoke


def test_maf_adapter_runs_deterministic_workflow_without_model_calls() -> None:
    report = run_maf_adapter_sync("governed public question")

    assert report.framework_name == "Microsoft Agent Framework"
    assert report.package_name == "agent-framework"
    assert report.package_version
    assert report.workflow_name == "codex-thesis-replication-workflow"
    assert report.output_count == 1
    assert report.outputs == ["MAF deterministic orchestration accepted: governed public question"]
    assert report.model_calls_performed is False


def test_maf_adapter_smoke_writes_artifacts(tmp_path: Path) -> None:
    report = run_maf_adapter_sync("artifact smoke")

    json_path, markdown_path = write_maf_adapter_smoke(report, tmp_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert "Microsoft Agent Framework Adapter Smoke" in markdown_path.read_text(encoding="utf-8")
