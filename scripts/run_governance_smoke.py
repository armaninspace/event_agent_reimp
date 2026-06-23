#!/usr/bin/env python3
"""Run a tournament/reflection/evolution governance smoke check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.friends_loop import run_friends_question_loop


def main() -> int:
    parser = argparse.ArgumentParser(description="Run governance metadata smoke checks.")
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-015-governance-metadata"))
    parser.add_argument("--turns", type=int, default=3)
    args = parser.parse_args()

    loop_dir = args.output_dir / "friends-question-loop-smoke"
    session = run_friends_question_loop(
        turn_count=args.turns,
        output_dir=loop_dir,
        reference_dir=args.reference_dir,
    )
    turns = session["turns"]
    assert isinstance(turns, list)
    selected = [turn["selected_candidate"] for turn in turns]
    report = {
        "schema_version": "phase-015.governance-smoke.v1",
        "turn_count": len(turns),
        "all_selected_have_tournament": all("tournament" in candidate for candidate in selected),
        "all_selected_have_reflection": all("reflection" in candidate for candidate in selected),
        "all_selected_have_evolution": all("evolution" in candidate for candidate in selected),
        "selected": [
            {
                "candidate_id": candidate["candidate_id"],
                "forum_question_id": candidate["forum"]["question_id"],
                "tournament_rank": candidate["tournament"]["rank"],
                "reflection_status": candidate["reflection"]["status"],
                "evolution_action": candidate["evolution"]["action"],
            }
            for candidate in selected
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "governance_smoke.json"
    markdown_path = args.output_dir / "governance_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_render_markdown(report), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"turn_count={report['turn_count']}")
    print(f"all_selected_have_tournament={report['all_selected_have_tournament']}")
    print(f"all_selected_have_reflection={report['all_selected_have_reflection']}")
    print(f"all_selected_have_evolution={report['all_selected_have_evolution']}")
    return 0


def _render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Governance Smoke",
        "",
        f"Schema: {report['schema_version']}",
        f"Turn count: {report['turn_count']}",
        f"All selected have tournament: {report['all_selected_have_tournament']}",
        f"All selected have reflection: {report['all_selected_have_reflection']}",
        f"All selected have evolution: {report['all_selected_have_evolution']}",
        "",
        "## Selected Candidates",
        "",
    ]
    selected = report["selected"]
    assert isinstance(selected, list)
    for item in selected:
        assert isinstance(item, dict)
        lines.extend(
            [
                f"### {item['candidate_id']}",
                "",
                f"- Forum question ID: {item['forum_question_id']}",
                f"- Tournament rank: {item['tournament_rank']}",
                f"- Reflection status: {item['reflection_status']}",
                f"- Evolution action: {item['evolution_action']}",
                "",
            ]
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
