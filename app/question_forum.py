"""JSON-backed public QuestionForum records."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


ALLOWED_STATUSES = frozenset({"proposed", "selected", "tested", "answered", "needs-review"})
DEFAULT_FORUM_PATH = Path("data/question_forum/questions.json")


@dataclass(frozen=True)
class QuestionForumRecord:
    """One stakeholder-facing public question record."""

    question_id: str
    kind: str
    persona: str
    question: str
    rationale: str
    priority: int
    popularity: int
    source_url: str
    status: str
    tags: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable forum record data."""
        return asdict(self)

    def candidate_metadata(self) -> dict[str, object]:
        """Return forum fields carried by a selected candidate."""
        return {
            "question_id": self.question_id,
            "kind": self.kind,
            "persona": self.persona,
            "priority": self.priority,
            "popularity": self.popularity,
            "source_url": self.source_url,
            "status": self.status,
            "tags": list(self.tags),
        }


def load_question_forum(path: Path = DEFAULT_FORUM_PATH) -> list[QuestionForumRecord]:
    """Load and validate QuestionForum records from JSON."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("QuestionForum JSON must contain a list of records.")
    records = [_record_from_dict(item, index=index) for index, item in enumerate(raw)]
    _validate_unique_ids(records)
    return sorted(records, key=lambda record: (-record.priority, -record.popularity, record.question_id))


def _record_from_dict(item: object, *, index: int) -> QuestionForumRecord:
    if not isinstance(item, dict):
        raise ValueError(f"QuestionForum record {index} must be an object.")
    required = {
        "question_id",
        "kind",
        "persona",
        "question",
        "rationale",
        "priority",
        "popularity",
        "source_url",
        "status",
        "tags",
    }
    missing = sorted(required - item.keys())
    if missing:
        raise ValueError(f"QuestionForum record {index} is missing fields: {', '.join(missing)}.")
    status = str(item["status"])
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"QuestionForum record {index} has invalid status: {status}.")
    tags = item["tags"]
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag for tag in tags):
        raise ValueError(f"QuestionForum record {index} tags must be non-empty strings.")
    priority = _bounded_int(item["priority"], field="priority", index=index)
    popularity = _bounded_int(item["popularity"], field="popularity", index=index)
    return QuestionForumRecord(
        question_id=_non_empty_string(item["question_id"], field="question_id", index=index),
        kind=_non_empty_string(item["kind"], field="kind", index=index),
        persona=_non_empty_string(item["persona"], field="persona", index=index),
        question=_non_empty_string(item["question"], field="question", index=index),
        rationale=_non_empty_string(item["rationale"], field="rationale", index=index),
        priority=priority,
        popularity=popularity,
        source_url=_non_empty_string(item["source_url"], field="source_url", index=index),
        status=status,
        tags=list(tags),
    )


def _bounded_int(value: object, *, field: str, index: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"QuestionForum record {index} {field} must be an integer.")
    if not 0 <= value <= 10:
        raise ValueError(f"QuestionForum record {index} {field} must be between 0 and 10.")
    return value


def _non_empty_string(value: object, *, field: str, index: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"QuestionForum record {index} {field} must be a non-empty string.")
    return value


def _validate_unique_ids(records: list[QuestionForumRecord]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for record in records:
        if record.question_id in seen:
            duplicates.add(record.question_id)
        seen.add(record.question_id)
    if duplicates:
        raise ValueError(f"Duplicate QuestionForum IDs: {', '.join(sorted(duplicates))}.")
