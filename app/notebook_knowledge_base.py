"""Structured notebook knowledge base extracted from generated notebooks."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class NotebookKnowledgeEntry:
    """Compact durable memory extracted from one turn notebook and Markdown export."""

    notebook_path: str
    markdown_path: str
    turn: int
    candidate_id: str
    notebook_status: str
    execution_backend: str | None
    executed_code_cells: int
    semantic_slot: str
    source_cell_ids: list[str]
    seed_question: str
    caveat: str | None

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable knowledge entry."""
        return asdict(self)


def build_notebook_knowledge_base(notebook_dir: Path) -> dict[str, object]:
    """Extract structured memory from turn notebooks in a workspace."""
    entries = [_entry_from_notebook(path) for path in sorted(notebook_dir.glob("turn-*.ipynb"))]
    latest = entries[-1] if entries else None
    return {
        "schema_version": "phase-027.notebook-knowledge-base.v1",
        "notebook_dir": str(notebook_dir),
        "entry_count": len(entries),
        "latest_notebook": latest.notebook_path if latest else None,
        "latest_seed_question": latest.seed_question if latest else None,
        "latest_source_cell": latest.source_cell_ids[-1] if latest and latest.source_cell_ids else None,
        "entries": [entry.to_dict() for entry in entries],
    }


def write_notebook_knowledge_base(notebook_dir: Path) -> tuple[Path, Path, dict[str, object]]:
    """Write notebook knowledge JSON and Markdown artifacts."""
    knowledge = build_notebook_knowledge_base(notebook_dir)
    json_path = notebook_dir / "notebook-knowledge.json"
    markdown_path = notebook_dir / "notebook-knowledge.md"
    json_path.write_text(json.dumps(knowledge, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_notebook_knowledge_markdown(knowledge), encoding="utf-8")
    return json_path, markdown_path, knowledge


def load_notebook_knowledge_summary(path: Path | None) -> dict[str, object]:
    """Load a compact prior notebook knowledge summary for a new run."""
    if path is None or not path.exists():
        return {
            "schema_version": "phase-027.notebook-knowledge-summary.v1",
            "source_path": str(path) if path else None,
            "entry_count": 0,
            "latest_seed_question": None,
            "latest_source_cell": None,
            "latest_semantic_slot": None,
            "recent_seed_questions": [],
        }
    knowledge = json.loads(path.read_text(encoding="utf-8"))
    entries = knowledge.get("entries", [])
    if not isinstance(entries, list):
        entries = []
    recent_entries = [entry for entry in entries[-5:] if isinstance(entry, dict)]
    latest = recent_entries[-1] if recent_entries else {}
    return {
        "schema_version": "phase-027.notebook-knowledge-summary.v1",
        "source_path": str(path),
        "entry_count": int(knowledge.get("entry_count", len(entries))),
        "latest_seed_question": latest.get("seed_question"),
        "latest_source_cell": _latest_source_cell(latest),
        "latest_semantic_slot": latest.get("semantic_slot"),
        "recent_seed_questions": [
            entry["seed_question"]
            for entry in recent_entries
            if isinstance(entry.get("seed_question"), str) and entry["seed_question"]
        ],
    }


def render_notebook_knowledge_markdown(knowledge: dict[str, object]) -> str:
    """Render notebook knowledge base as compact Markdown."""
    lines = [
        "# Notebook Knowledge Base",
        "",
        f"Schema: `{knowledge['schema_version']}`",
        f"Entry count: `{knowledge['entry_count']}`",
        f"Latest notebook: `{knowledge['latest_notebook']}`",
        f"Latest seed question: {knowledge['latest_seed_question']}",
        "",
        "## Entries",
        "",
    ]
    entries = knowledge["entries"]
    assert isinstance(entries, list)
    for entry in entries:
        assert isinstance(entry, dict)
        lines.extend(
            [
                f"### Turn {entry['turn']}: `{entry['candidate_id']}`",
                "",
                f"- Notebook: `{entry['notebook_path']}`",
                f"- Markdown: `{entry['markdown_path']}`",
                f"- Status: `{entry['notebook_status']}`",
                f"- Semantic slot: `{entry['semantic_slot']}`",
                f"- Seed question: {entry['seed_question']}",
                f"- Caveat: {entry['caveat']}",
                "",
            ]
        )
    return "\n".join(lines)


def _entry_from_notebook(path: Path) -> NotebookKnowledgeEntry:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    metadata = notebook.get("metadata", {}).get("event_agent", {})
    if not isinstance(metadata, dict):
        metadata = {}
    markdown_path = path.with_suffix(".md")
    markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
    return NotebookKnowledgeEntry(
        notebook_path=str(path),
        markdown_path=str(markdown_path),
        turn=int(metadata.get("turn", 0)),
        candidate_id=str(metadata.get("candidate_id", "")),
        notebook_status=str(metadata.get("status", "unknown")),
        execution_backend=_optional_string(metadata.get("execution_backend")),
        executed_code_cells=int(metadata.get("executed_code_cells", 0)),
        semantic_slot=_extract_validation_field(notebook, "semantic_slot"),
        source_cell_ids=[
            str(cell.get("id"))
            for cell in notebook.get("cells", [])
            if isinstance(cell, dict) and isinstance(cell.get("id"), str)
        ],
        seed_question=_extract_title(markdown_text),
        caveat=_extract_prefixed_line(markdown_text, "Caveat:"),
    )


def _extract_validation_field(notebook: dict[str, object], field: str) -> str:
    needle = f"'{field}': "
    for cell in notebook.get("cells", []):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        text = "".join(source) if isinstance(source, list) else str(source)
        for line in text.splitlines():
            if needle in line:
                return line.split(needle, 1)[1].strip().strip(",").strip("'\"")
    return ""


def _extract_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# Turn "):
            return line.split(": ", 1)[1] if ": " in line else line.removeprefix("# ")
    return ""


def _extract_prefixed_line(markdown_text: str, prefix: str) -> str | None:
    for line in markdown_text.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return None


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _latest_source_cell(entry: dict[str, object]) -> str | None:
    source_cell_ids = entry.get("source_cell_ids")
    if isinstance(source_cell_ids, list) and source_cell_ids and isinstance(source_cell_ids[-1], str):
        return source_cell_ids[-1]
    return None
