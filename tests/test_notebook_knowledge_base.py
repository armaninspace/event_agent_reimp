import json
from pathlib import Path

from app.notebook_execution import execute_workspace_lightweight
from app.notebook_knowledge_base import build_notebook_knowledge_base, write_notebook_knowledge_base
from app.notebook_workspace import write_turn_notebook


def _turn(turn_number: int, candidate_id: str) -> dict[str, object]:
    return {
        "turn": turn_number,
        "selected_candidate": {
            "candidate_id": candidate_id,
            "question": "Do big sports crowds turn into local spending?",
            "rationale": "Useful public question.",
            "semantic_slot": "city_week_event_spending",
            "score": 14,
            "caveat": "Observational only.",
        },
        "rejected_candidates": [{"candidate_id": "rejected"}],
        "statistical_evidence": {
            "result_count": 1,
            "min_adjusted_p_value": 0.01,
            "has_adjusted_significance": True,
            "result_ids": ["matched:city_week:revenue_all"],
            "caveats": ["Observational only."],
        },
    }


def test_write_notebook_knowledge_base_extracts_executed_notebooks(tmp_path: Path) -> None:
    write_turn_notebook(tmp_path, turn=_turn(1, "turn-01-a"))
    write_turn_notebook(tmp_path, turn=_turn(2, "turn-02-b"))
    execute_workspace_lightweight(tmp_path)

    json_path, markdown_path, knowledge = write_notebook_knowledge_base(tmp_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert knowledge["schema_version"] == "phase-027.notebook-knowledge-base.v1"
    assert knowledge["entry_count"] == 2
    assert knowledge["latest_seed_question"] == "Do big sports crowds turn into local spending?"
    entries = knowledge["entries"]
    assert isinstance(entries, list)
    assert entries[-1]["notebook_status"] == "lightweight_executed"
    assert entries[-1]["semantic_slot"] == "city_week_event_spending"
    assert "turn-02-b" in markdown_path.read_text(encoding="utf-8")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["entry_count"] == 2


def test_build_notebook_knowledge_base_handles_empty_workspace(tmp_path: Path) -> None:
    knowledge = build_notebook_knowledge_base(tmp_path)

    assert knowledge["entry_count"] == 0
    assert knowledge["latest_notebook"] is None
