from app.agent_runtime import get_agent_runtime_metadata


def test_agent_runtime_metadata_reports_python_and_framework() -> None:
    metadata = get_agent_runtime_metadata()

    assert metadata.language == "python"
    assert metadata.framework_name == "Microsoft Agent Framework"
    assert metadata.package_name == "agent-framework"
    assert metadata.import_name == "agent_framework"
    assert metadata.import_available is True
    assert metadata.package_version is not None
