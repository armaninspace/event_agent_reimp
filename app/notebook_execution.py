"""Lightweight execution backend for generated notebooks."""

from __future__ import annotations

import contextlib
import io
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class NotebookExecutionResult:
    """Execution result for one notebook."""

    path: str
    status: str
    executed_code_cells: int
    validation_error: str | None

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable execution result."""
        return asdict(self)


def execute_notebook_lightweight(path: Path) -> NotebookExecutionResult:
    """Execute generated notebook code cells in a lightweight local namespace."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace: dict[str, object] = {}
    execution_count = 0
    validation_error: str | None = None

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        execution_count += 1
        source = _source_to_text(cell.get("source", ""))
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(compile(source, str(path), "exec"), namespace)
        except Exception as exc:  # noqa: BLE001 - captured into notebook output intentionally.
            validation_error = f"{type(exc).__name__}: {exc}"
            cell["outputs"] = [
                {
                    "ename": type(exc).__name__,
                    "evalue": str(exc),
                    "output_type": "error",
                    "traceback": [validation_error],
                }
            ]
            cell["metadata"] = {**cell.get("metadata", {}), "event_agent_status": "failed"}
            break
        output_text = stdout.getvalue()
        cell["execution_count"] = execution_count
        cell["outputs"] = (
            [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": output_text,
                }
            ]
            if output_text
            else []
        )
        cell["metadata"] = {**cell.get("metadata", {}), "event_agent_status": "lightweight_executed"}

    status = "failed" if validation_error else "lightweight_executed"
    metadata = notebook.setdefault("metadata", {})
    event_agent = metadata.setdefault("event_agent", {})
    event_agent["status"] = status
    event_agent["execution_backend"] = "lightweight"
    event_agent["executed_code_cells"] = execution_count
    path.write_text(json.dumps(notebook, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _update_markdown_status(path.with_suffix(".md"), status=status)
    return NotebookExecutionResult(
        path=str(path),
        status=status,
        executed_code_cells=execution_count,
        validation_error=validation_error,
    )


def execute_workspace_lightweight(notebook_dir: Path) -> dict[str, object]:
    """Execute all turn notebooks in a workspace."""
    results = [execute_notebook_lightweight(path) for path in sorted(notebook_dir.glob("turn-*.ipynb"))]
    failures = [result for result in results if result.validation_error]
    return {
        "backend": "lightweight",
        "executed_notebook_count": len(results),
        "failed_notebook_count": len(failures),
        "all_lightweight_executed": bool(results) and not failures,
        "results": [result.to_dict() for result in results],
    }


def _source_to_text(source: object) -> str:
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def _update_markdown_status(path: Path, *, status: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("Notebook status: `scaffolded`. Execution is deferred.", f"Notebook status: `{status}`.")
    path.write_text(text, encoding="utf-8")
