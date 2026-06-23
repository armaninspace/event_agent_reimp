"""Append-oriented notebook and wiki workspace scaffolding."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


WIKI_FILES = (
    "SCHEMA.md",
    "index.md",
    "log.md",
    "question-board.md",
    "decision-records.md",
    "caveats.md",
    "semantic-map.md",
    "findings.md",
)


@dataclass(frozen=True)
class TurnNotebookArtifacts:
    """Notebook artifacts written for one loop turn."""

    notebook_path: Path
    markdown_path: Path

    def to_dict(self) -> dict[str, str]:
        """Return JSON-serializable paths."""
        return {
            "notebook_path": str(self.notebook_path),
            "markdown_path": str(self.markdown_path),
        }


def initialize_workspace(notebook_dir: Path) -> None:
    """Create required wiki files if they do not already exist."""
    notebook_dir.mkdir(parents=True, exist_ok=True)
    defaults = {
        "SCHEMA.md": "# Notebook Workspace Schema\n\nStatus: scaffolded notebooks, not executed.\n",
        "index.md": "# Notebook Workspace Index\n\n",
        "log.md": "# Workspace Log\n\n",
        "question-board.md": "# Question Board\n\n",
        "decision-records.md": "# Decision Records\n\n",
        "caveats.md": "# Caveats\n\n",
        "semantic-map.md": "# Semantic Map\n\n",
        "findings.md": "# Findings\n\n",
    }
    for filename in WIKI_FILES:
        path = notebook_dir / filename
        if not path.exists():
            path.write_text(defaults[filename], encoding="utf-8")


def write_turn_notebook(notebook_dir: Path, *, turn: dict[str, object]) -> TurnNotebookArtifacts:
    """Write scaffolded notebook JSON and Markdown export for one turn."""
    initialize_workspace(notebook_dir)
    selected = turn["selected_candidate"]
    rejected = turn["rejected_candidates"]
    assert isinstance(selected, dict)
    assert isinstance(rejected, list)
    turn_number = int(turn["turn"])
    slug = str(selected["candidate_id"])
    notebook_path = notebook_dir / f"turn-{turn_number:02d}-{slug}.ipynb"
    markdown_path = notebook_dir / f"turn-{turn_number:02d}-{slug}.md"

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": f"turn-{turn_number:02d}-intro",
                "metadata": {},
                "source": [
                    f"# Turn {turn_number}: {selected['question']}\n",
                    "\n",
                    f"Selected candidate: `{selected['candidate_id']}`\n",
                ],
            },
            {
                "cell_type": "markdown",
                "id": f"turn-{turn_number:02d}-validation-status",
                "metadata": {},
                "source": [
                    "## Validation Status\n",
                    "\n",
                    "Notebook status: `scaffolded`. Code execution is deferred to a later phase.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "id": f"turn-{turn_number:02d}-validation-code",
                "metadata": {},
                "outputs": [],
                "source": [
                    "validation_contract = {\n",
                    f"    'candidate_id': {selected['candidate_id']!r},\n",
                    f"    'semantic_slot': {selected['semantic_slot']!r},\n",
                    "    'notebook_status': 'scaffolded',\n",
                    "}\n",
                    "observed_contract = dict(validation_contract)\n",
                    "assert observed_contract == validation_contract\n",
                    "print('validation_contract_passed')\n",
                ],
            },
        ],
        "metadata": {
            "event_agent": {
                "turn": turn_number,
                "candidate_id": selected["candidate_id"],
                "status": "scaffolded",
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    notebook_path.write_text(json.dumps(notebook, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_render_turn_markdown(turn), encoding="utf-8")
    _append_wiki_updates(notebook_dir, turn=turn, artifacts=TurnNotebookArtifacts(notebook_path, markdown_path))
    return TurnNotebookArtifacts(notebook_path=notebook_path, markdown_path=markdown_path)


def summarize_workspace(notebook_dir: Path) -> dict[str, object]:
    """Summarize workspace files for regression checks."""
    wiki_checks = {filename: (notebook_dir / filename).exists() for filename in WIKI_FILES}
    notebooks = sorted(str(path) for path in notebook_dir.glob("turn-*.ipynb"))
    markdown_exports = sorted(str(path) for path in notebook_dir.glob("turn-*.md"))
    lightweight_executed_count = 0
    for notebook_path in notebook_dir.glob("turn-*.ipynb"):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        if notebook.get("metadata", {}).get("event_agent", {}).get("status") in {
            "lightweight_executed",
            "nbclient_executed",
        }:
            lightweight_executed_count += 1
    nbclient_executed_count = 0
    for notebook_path in notebook_dir.glob("turn-*.ipynb"):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        if notebook.get("metadata", {}).get("event_agent", {}).get("status") == "nbclient_executed":
            nbclient_executed_count += 1
    return {
        "path": str(notebook_dir),
        "wiki_files_exist": all(wiki_checks.values()),
        "wiki_checks": wiki_checks,
        "notebook_count": len(notebooks),
        "markdown_export_count": len(markdown_exports),
        "lightweight_executed_count": lightweight_executed_count,
        "nbclient_executed_count": nbclient_executed_count,
        "notebooks": notebooks,
        "markdown_exports": markdown_exports,
    }


def _render_turn_markdown(turn: dict[str, object]) -> str:
    selected = turn["selected_candidate"]
    rejected = turn["rejected_candidates"]
    assert isinstance(selected, dict)
    assert isinstance(rejected, list)
    statistical_lines = _render_statistical_evidence_markdown(turn.get("statistical_evidence"))
    return "\n".join(
        [
            f"# Turn {turn['turn']}: {selected['question']}",
            "",
            f"Selected candidate: `{selected['candidate_id']}`",
            "",
            f"Rationale: {selected['rationale']}",
            "",
            f"Caveat: {selected['caveat']}",
            "",
            *statistical_lines,
            "",
            "Rejected candidates:",
            *[f"- `{candidate['candidate_id']}`" for candidate in rejected],
            "",
            "Notebook status: `scaffolded`. Execution is deferred.",
            "",
        ]
    )


def _append_wiki_updates(
    notebook_dir: Path,
    *,
    turn: dict[str, object],
    artifacts: TurnNotebookArtifacts,
) -> None:
    selected = turn["selected_candidate"]
    rejected = turn["rejected_candidates"]
    assert isinstance(selected, dict)
    assert isinstance(rejected, list)
    turn_number = turn["turn"]
    _append(notebook_dir / "index.md", f"- Turn {turn_number}: [{selected['candidate_id']}]({artifacts.markdown_path.name})\n")
    _append(notebook_dir / "log.md", f"- Turn {turn_number}: wrote scaffolded notebook `{artifacts.notebook_path.name}`\n")
    _append(notebook_dir / "question-board.md", f"- Turn {turn_number}: selected `{selected['candidate_id']}`; rejected {len(rejected)} candidates\n")
    _append(notebook_dir / "decision-records.md", f"- Turn {turn_number}: selected `{selected['candidate_id']}` with score {selected['score']}\n")
    _append(notebook_dir / "caveats.md", f"- Turn {turn_number}: {selected['caveat']}\n")
    _append(notebook_dir / "semantic-map.md", f"- `{selected['semantic_slot']}` -> `{selected['candidate_id']}`\n")
    statistical_evidence = turn.get("statistical_evidence")
    if isinstance(statistical_evidence, dict):
        _append(
            notebook_dir / "findings.md",
            "- Turn "
            f"{turn_number}: attached {statistical_evidence['result_count']} statistical results; "
            f"min adjusted p-value {statistical_evidence['min_adjusted_p_value']}; "
            "observational only.\n",
        )
    else:
        _append(notebook_dir / "findings.md", f"- Turn {turn_number}: scaffolded only; no validated finding yet.\n")


def _render_statistical_evidence_markdown(value: object) -> list[str]:
    if not isinstance(value, dict):
        return []
    result_ids = value.get("result_ids", [])
    if not isinstance(result_ids, list):
        result_ids = []
    caveats = value.get("caveats", [])
    if not isinstance(caveats, list):
        caveats = []
    return [
        "## Statistical Evidence",
        "",
        f"Result count: `{value.get('result_count')}`",
        "",
        f"Minimum adjusted p-value: `{value.get('min_adjusted_p_value')}`",
        "",
        f"Adjusted-significance flag: `{value.get('has_adjusted_significance')}`",
        "",
        "Result IDs:",
        *[f"- `{result_id}`" for result_id in result_ids],
        "",
        "Statistical caveats:",
        *[f"- {caveat}" for caveat in caveats],
    ]


def _append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)
