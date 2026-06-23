"""Runtime metadata for the Microsoft Agent Framework dependency."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import platform
import sys
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AgentRuntimeMetadata:
    """Installed agent runtime metadata captured without making model calls."""

    language: str
    python_version: str
    framework_name: str
    package_name: str
    import_name: str
    package_version: str | None
    import_available: bool

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable runtime metadata."""
        return asdict(self)


def get_agent_runtime_metadata() -> AgentRuntimeMetadata:
    """Inspect the local Python runtime and Microsoft Agent Framework package."""
    package_name = "agent-framework"
    import_name = "agent_framework"
    try:
        package_version: str | None = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        package_version = None

    return AgentRuntimeMetadata(
        language="python",
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        framework_name="Microsoft Agent Framework",
        package_name=package_name,
        import_name=import_name,
        package_version=package_version,
        import_available=importlib.util.find_spec(import_name) is not None,
    )


def platform_summary() -> str:
    """Return a concise platform string for audit output."""
    return f"{platform.system()} {platform.release()} ({platform.machine()})"
