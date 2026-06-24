#!/usr/bin/env python3
"""Run a Microsoft Agent Framework adapter smoke check."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.maf_orchestration import run_maf_adapter_sync, write_maf_adapter_smoke


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Microsoft Agent Framework adapter smoke check.")
    parser.add_argument("--message", default="replicate governed thesis workflow")
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-025-maf-openai-bridge"))
    parser.add_argument(
        "--reasoning-mode",
        choices=("deterministic", "openai", "replay"),
        default="deterministic",
        help="Reasoning mode used inside the MAF workflow executor.",
    )
    parser.add_argument("--openai-model", help="OpenAI model for reasoning-mode openai/replay.")
    parser.add_argument("--openai-replay-path", type=Path, help="Replay JSON for reasoning-mode replay.")
    args = parser.parse_args()

    report = run_maf_adapter_sync(
        args.message,
        reasoning_mode=args.reasoning_mode,
        openai_model=args.openai_model,
        openai_replay_path=args.openai_replay_path,
        openai_trace_dir=args.output_dir / "openai-reasoning" if args.reasoning_mode in {"openai", "replay"} else None,
    )
    json_path, markdown_path = write_maf_adapter_smoke(report, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"framework={report.framework_name}")
    print(f"package={report.package_name} {report.package_version}")
    print(f"workflow={report.workflow_name}")
    print(f"reasoning_provider={report.reasoning_provider}")
    print(f"reasoning_mode={report.reasoning_mode}")
    print(f"candidate_count={report.candidate_count}")
    print(f"output_count={report.output_count}")
    print(f"model_calls_performed={report.model_calls_performed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
