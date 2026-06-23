#!/usr/bin/env python3
"""Run a QuestionForum load/validation smoke check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.question_forum import DEFAULT_FORUM_PATH, load_question_forum


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the QuestionForum store.")
    parser.add_argument("--forum-path", type=Path, default=DEFAULT_FORUM_PATH)
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-014-question-forum-store"))
    args = parser.parse_args()

    records = load_question_forum(args.forum_path)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": "phase-014.question-forum-smoke.v1",
        "forum_path": str(args.forum_path),
        "record_count": len(records),
        "question_ids": [record.question_id for record in records],
        "statuses": sorted({record.status for record in records}),
        "records": [record.to_dict() for record in records],
    }
    json_path = args.output_dir / "question_forum_smoke.json"
    markdown_path = args.output_dir / "question_forum_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_render_markdown(report), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"record_count={report['record_count']}")
    return 0


def _render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# QuestionForum Smoke",
        "",
        f"Schema: {report['schema_version']}",
        f"Forum path: {report['forum_path']}",
        f"Record count: {report['record_count']}",
        "",
        "## Questions",
        "",
    ]
    records = report["records"]
    assert isinstance(records, list)
    for item in records:
        assert isinstance(item, dict)
        lines.extend(
            [
                f"### {item['question_id']}",
                "",
                f"- Persona: {item['persona']}",
                f"- Status: {item['status']}",
                f"- Priority: {item['priority']}",
                f"- Popularity: {item['popularity']}",
                f"- Question: {item['question']}",
                "",
            ]
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
