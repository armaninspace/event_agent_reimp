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
        "--notebook-execution-backend",
        choices=("lightweight", "nbclient"),
        default="lightweight",
        help="Notebook execution backend for generated turn notebooks.",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing final runtime CSV files.",
    )
    parser.add_argument(
        "--reasoning-mode",
        choices=("deterministic", "openai", "replay"),
        default="deterministic",
        help="Hypothesis generation mode.",
    )
    parser.add_argument("--openai-model", help="OpenAI model for reasoning-mode openai/replay.")
    parser.add_argument("--openai-replay-path", type=Path, help="Replay JSON for reasoning-mode replay.")
    parser.add_argument("--prior-notebook-knowledge-path", type=Path, help="Prior notebook-knowledge.json to read.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run phase regression from CLI arguments."""
    args = build_parser().parse_args(argv)
    summary, summary_path = run_phase_regression(
        phase_id=args.phase_id,
        turns=args.turns,
        runs_dir=args.runs_dir,
        reference_dir=args.reference_dir,
        notebook_execution_backend=args.notebook_execution_backend,
        reasoning_mode=args.reasoning_mode,
        openai_model=args.openai_model,
        openai_replay_path=args.openai_replay_path,
        prior_notebook_knowledge_path=args.prior_notebook_knowledge_path,
    )
    print(f"wrote {summary_path}")
    print(f"requested_turns={summary.requested_turns}")
    print(f"completed_workflows={summary.completed_workflows}")
    print(f"stopped_early={summary.stopped_early}")
    print(f"workflow_task_statistical_misroutes={summary.workflow_task_statistical_misroutes}")
    print(f"turns_have_statistical_evidence={summary.turns_have_statistical_evidence}")
    print(f"turns_have_causal_design_diagnostics={summary.turns_have_causal_design_diagnostics}")
    print(f"data_snapshot_complete={summary.data_snapshot_complete}")
    print(f"correction_notebook_present={summary.correction_notebook_present}")
    print(f"correction_notebook_executed={summary.correction_notebook_executed}")
    print(f"current_required_artifacts_exist={summary.current_required_artifacts_exist}")
    print(f"notebook_workspace_present={summary.notebook_workspace_present}")
    print(f"notebook_knowledge_present={summary.notebook_knowledge_present}")
    print(f"prior_notebook_knowledge_entry_count={summary.prior_notebook_knowledge_entry_count}")
    print(f"prior_knowledge_duplicate_candidate_count={summary.prior_knowledge_duplicate_candidate_count}")
    print(f"selected_semantic_slot_counts={summary.selected_semantic_slot_counts}")
    print(f"selected_unique_semantic_slot_count={summary.selected_unique_semantic_slot_count}")
    print(f"reasoning_provider={summary.reasoning_provider}")
    print(f"reasoning_mode={summary.reasoning_mode}")
    print(f"selected_candidates_have_openai_reasoning={summary.selected_candidates_have_openai_reasoning}")
    print(f"openai_model_calls_performed={summary.openai_model_calls_performed}")
    print(f"executed_notebook_count={summary.notebook_execution['executed_notebook_count']}")
    print(f"failed_notebook_count={summary.notebook_execution['failed_notebook_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
