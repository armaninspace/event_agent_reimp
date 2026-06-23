import json
from pathlib import Path

from app.notebook_workspace import WIKI_FILES, initialize_workspace, summarize_workspace, write_correction_notebook, write_turn_notebook


def _turn(candidate_id: str = "turn-01-crowd-spending") -> dict[str, object]:
    return {
        "turn": 1,
        "selected_candidate": {
            "candidate_id": candidate_id,
            "question": "Do big sports crowds actually turn into more local spending?",
            "rationale": "Useful public question.",
            "semantic_slot": "city_week_event_spending",
            "score": 14,
            "caveat": "Observational only.",
        },
        "rejected_candidates": [
            {"candidate_id": "turn-01-market-coverage"},
            {"candidate_id": "turn-01-confounding-risk"},
        ],
        "statistical_evidence": {
            "result_count": 2,
            "min_adjusted_p_value": 0.01,
            "has_adjusted_significance": True,
            "result_ids": ["matched:city_week:revenue_all"],
            "caveats": ["Observational only."],
        },
    }


def test_initialize_workspace_creates_required_wiki_files(tmp_path: Path) -> None:
    initialize_workspace(tmp_path)

    assert all((tmp_path / filename).exists() for filename in WIKI_FILES)


def test_write_turn_notebook_creates_ipynb_markdown_and_appends_wiki(tmp_path: Path) -> None:
    artifacts = write_turn_notebook(tmp_path, turn=_turn())

    assert artifacts.notebook_path.exists()
    assert artifacts.markdown_path.exists()
    notebook = json.loads(artifacts.notebook_path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    assert notebook["metadata"]["event_agent"]["status"] == "scaffolded"
    assert any(cell["cell_type"] == "code" for cell in notebook["cells"])
    markdown = artifacts.markdown_path.read_text(encoding="utf-8")
    assert "Notebook status" in markdown
    assert "Statistical Evidence" in markdown
    assert "turn-01-crowd-spending" in (tmp_path / "decision-records.md").read_text(encoding="utf-8")
    assert "attached 2 statistical results" in (tmp_path / "findings.md").read_text(encoding="utf-8")


def test_summarize_workspace_counts_turn_artifacts(tmp_path: Path) -> None:
    write_turn_notebook(tmp_path, turn=_turn("turn-01-a"))
    second = _turn("turn-02-b")
    second["turn"] = 2
    write_turn_notebook(tmp_path, turn=second)

    summary = summarize_workspace(tmp_path)

    assert summary["wiki_files_exist"] is True
    assert summary["notebook_count"] == 2
    assert summary["markdown_export_count"] == 2
    assert summary["lightweight_executed_count"] == 0


def test_write_correction_notebook_creates_final_corrections_artifacts(tmp_path: Path) -> None:
    report = {
        "schema_version": "phase-test",
        "method": "Benjamini-Hochberg FDR correction",
        "result_count": 1,
        "results": [
            {
                "result_id": "matched:city_week:revenue_all",
                "p_value": 0.01,
                "adjusted_p_value": 0.02,
                "status": "ok",
            }
        ],
    }

    artifacts = write_correction_notebook(tmp_path, correction_report=report)
    summary = summarize_workspace(tmp_path)

    assert artifacts.notebook_path.name == "999-multiple-testing-corrections.ipynb"
    assert artifacts.markdown_path.name == "999-multiple-testing-corrections.md"
    assert artifacts.notebook_path.exists()
    assert artifacts.markdown_path.exists()
    assert "matched:city_week:revenue_all" in artifacts.markdown_path.read_text(encoding="utf-8")
    assert summary["correction_notebook_exists"] is True
    assert summary["correction_markdown_exists"] is True
