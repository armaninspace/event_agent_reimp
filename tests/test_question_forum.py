import json
from pathlib import Path

import pytest

from app.question_forum import load_question_forum


def test_question_forum_loads_and_validates_statuses(tmp_path: Path) -> None:
    forum_path = tmp_path / "questions.json"
    forum_path.write_text(
        json.dumps(
            [
                {
                    "question_id": "q1",
                    "kind": "event_impact",
                    "persona": "business owner",
                    "question": "Do crowds change spending?",
                    "rationale": "Readable public question.",
                    "priority": 8,
                    "popularity": 7,
                    "source_url": "local://q1",
                    "status": "proposed",
                    "tags": ["events"],
                }
            ]
        ),
        encoding="utf-8",
    )

    records = load_question_forum(forum_path)

    assert len(records) == 1
    assert records[0].question_id == "q1"
    assert records[0].candidate_metadata()["status"] == "proposed"


def test_question_forum_rejects_invalid_status(tmp_path: Path) -> None:
    forum_path = tmp_path / "questions.json"
    forum_path.write_text(
        json.dumps(
            [
                {
                    "question_id": "q1",
                    "kind": "event_impact",
                    "persona": "business owner",
                    "question": "Do crowds change spending?",
                    "rationale": "Readable public question.",
                    "priority": 8,
                    "popularity": 7,
                    "source_url": "local://q1",
                    "status": "done",
                    "tags": ["events"],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="invalid status"):
        load_question_forum(forum_path)
