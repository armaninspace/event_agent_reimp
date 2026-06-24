#!/usr/bin/env python3
"""Run an OpenAI-backed hypothesis generation smoke workflow."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.friends_loop import run_friends_question_loop


def build_parser() -> argparse.ArgumentParser:
    """Create the OpenAI reasoning smoke command parser."""
    parser = argparse.ArgumentParser(description="Run an OpenAI-backed friends-loop smoke workflow.")
    parser.add_argument("--mode", choices=("live", "replay"), default="live", help="OpenAI call mode.")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-5"), help="OpenAI model name.")
    parser.add_argument("--turns", type=int, default=1, help="Number of turns to run.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("app/runs/phase-024-openai-reasoning/openai-smoke"),
        help="Directory where smoke artifacts will be written.",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing final runtime CSV files.",
    )
    parser.add_argument("--replay-path", type=Path, help="Replay JSON path for --mode replay.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the OpenAI reasoning smoke command."""
    args = build_parser().parse_args(argv)
    if args.mode == "live" and not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is required for --mode live.", file=sys.stderr)
        return 2
    reasoning_mode = "openai" if args.mode == "live" else "replay"
    session = run_friends_question_loop(
        turn_count=args.turns,
        output_dir=args.output_dir / "friends-question-loop",
        reference_dir=args.reference_dir,
        reasoning_mode=reasoning_mode,
        openai_model=args.model,
        openai_replay_path=args.replay_path,
    )
    report = _smoke_report(session=session, mode=args.mode, model=args.model)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "openai_reasoning_smoke.json"
    markdown_path = args.output_dir / "openai_reasoning_smoke.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_render_markdown(report), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"mode={report['mode']}")
    print(f"provider={report['provider']}")
    print(f"model_calls_performed={report['model_calls_performed']}")
    print(f"selected_candidate_count={report['selected_candidate_count']}")
    return 0


def _smoke_report(*, session: dict[str, object], mode: str, model: str) -> dict[str, object]:
    turns = session["turns"]
    assert isinstance(turns, list)
    selected = [turn["selected_candidate"] for turn in turns]
    reasoning_records = [candidate["reasoning"] for candidate in selected if isinstance(candidate, dict)]
    return {
        "schema_version": "phase-024.openai-reasoning-smoke.v1",
        "mode": mode,
        "provider": "openai",
        "model": model,
        "selected_candidate_count": len(selected),
        "all_selected_have_openai_reasoning": all(
            isinstance(reasoning, dict) and reasoning.get("provider") == "openai" for reasoning in reasoning_records
        ),
        "model_calls_performed": any(
            isinstance(reasoning, dict) and bool(reasoning.get("model_calls_performed"))
            for reasoning in reasoning_records
        ),
        "selected": [
            {
                "candidate_id": candidate["candidate_id"],
                "question": candidate["question"],
                "semantic_slot": candidate["semantic_slot"],
                "reasoning": candidate["reasoning"],
            }
            for candidate in selected
        ],
        "artifact_paths": session["artifact_paths"],
    }


def _render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# OpenAI Reasoning Smoke",
        "",
        f"Schema: {report['schema_version']}",
        f"Mode: {report['mode']}",
        f"Provider: {report['provider']}",
        f"Model: {report['model']}",
        f"Selected candidate count: {report['selected_candidate_count']}",
        f"All selected have OpenAI reasoning: {report['all_selected_have_openai_reasoning']}",
        f"Model calls performed: {report['model_calls_performed']}",
        "",
        "## Selected Candidates",
        "",
    ]
    selected = report["selected"]
    assert isinstance(selected, list)
    for item in selected:
        assert isinstance(item, dict)
        reasoning = item["reasoning"]
        assert isinstance(reasoning, dict)
        lines.extend(
            [
                f"### {item['candidate_id']}",
                "",
                f"- Question: {item['question']}",
                f"- Semantic slot: {item['semantic_slot']}",
                f"- Mode: {reasoning['mode']}",
                f"- Model calls performed: {reasoning['model_calls_performed']}",
                f"- Trace path: {reasoning.get('trace_path')}",
                "",
            ]
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
