#!/usr/bin/env python3
"""Run the deterministic phase regression gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.phase_regression import run_phase_regression


def build_parser() -> argparse.ArgumentParser:
    """Create the regression command parser."""
    parser = argparse.ArgumentParser(description="Run a deterministic phase regression.")
    parser.add_argument("--phase-id", required=True, help="Stable phase identifier.")
    parser.add_argument("--turns", type=int, default=20, help="Number of turns to run.")
    parser.add_argument("--runs-dir", type=Path, default=Path("app/runs"), help="Base run artifact directory.")
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing final runtime CSV files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run phase regression from CLI arguments."""
    args = build_parser().parse_args(argv)
    summary, summary_path = run_phase_regression(
        phase_id=args.phase_id,
        turns=args.turns,
        runs_dir=args.runs_dir,
        reference_dir=args.reference_dir,
    )
    print(f"wrote {summary_path}")
    print(f"requested_turns={summary.requested_turns}")
    print(f"completed_workflows={summary.completed_workflows}")
    print(f"stopped_early={summary.stopped_early}")
    print(f"workflow_task_statistical_misroutes={summary.workflow_task_statistical_misroutes}")
    print(f"current_required_artifacts_exist={summary.current_required_artifacts_exist}")
    print(f"notebook_workspace_present={summary.notebook_workspace_present}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
