import json
from pathlib import Path

from app.notebook_execution import execute_notebook_lightweight, execute_workspace_lightweight
from app.notebook_workspace import write_turn_notebook


def _turn(turn_number: int = 1) -> dict[str, object]:
    return {
        "turn": turn_number,
        "selected_candidate": {
            "candidate_id": f"turn-{turn_number:02d}-candidate",
            "question": "Does this notebook execute?",
            "rationale": "Execution smoke.",
            "semantic_slot": "execution_smoke",
            "score": 10,
            "caveat": "Generated notebook only.",
        },
        "rejected_candidates": [{"candidate_id": f"turn-{turn_number:02d}-rejected"}],
    }


def test_execute_notebook_lightweight_captures_output_and_metadata(tmp_path: Path) -> None:
    artifacts = write_turn_notebook(tmp_path, turn=_turn())

    result = execute_notebook_lightweight(artifacts.notebook_path)

    assert result.status == "lightweight_executed"
    assert result.executed_code_cells == 1
    assert result.validation_error is None
    notebook = json.loads(artifacts.notebook_path.read_text(encoding="utf-8"))
    assert notebook["metadata"]["event_agent"]["status"] == "lightweight_executed"
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert code_cells[0]["outputs"][0]["text"] == "validation_contract_passed\n"
    assert "lightweight_executed" in artifacts.markdown_path.read_text(encoding="utf-8")


def test_execute_workspace_lightweight_counts_all_notebooks(tmp_path: Path) -> None:
    write_turn_notebook(tmp_path, turn=_turn(1))
    write_turn_notebook(tmp_path, turn=_turn(2))

    summary = execute_workspace_lightweight(tmp_path)

    assert summary["executed_notebook_count"] == 2
    assert summary["failed_notebook_count"] == 0
    assert summary["all_lightweight_executed"] is True
