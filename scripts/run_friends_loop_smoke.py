#!/usr/bin/env python3
"""Run a deterministic friends-loop smoke workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.friends_loop import run_friends_question_loop


def build_parser() -> argparse.ArgumentParser:
    """Create the smoke command parser."""
    parser = argparse.ArgumentParser(description="Run a deterministic friends-loop smoke workflow.")
    parser.add_argument("--turns", type=int, default=2, help="Number of turns to run.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("app/runs/phase-003-friends-loop-skeleton/friends-question-loop"),
        help="Directory where loop artifacts will be written.",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing final runtime CSV files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the friends-loop smoke command."""
    args = build_parser().parse_args(argv)
    session = run_friends_question_loop(
        turn_count=args.turns,
        output_dir=args.output_dir,
        reference_dir=args.reference_dir,
    )
    summary = session["session_summary"]
    artifact_paths = session["artifact_paths"]
    assert isinstance(summary, dict)
    assert isinstance(artifact_paths, dict)
    print(f"completed_turns={summary['completed_turns']}")
    for turn in session["turns"]:
        selected = turn["selected_candidate"]
        rejected = turn["rejected_candidates"]
        print(
            f"turn={turn['turn']} selected={selected['candidate_id']} "
            f"rejected={','.join(candidate['candidate_id'] for candidate in rejected)}"
        )
    for name, path in artifact_paths.items():
        print(f"{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
