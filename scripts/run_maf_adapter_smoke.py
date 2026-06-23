#!/usr/bin/env python3
"""Run a deterministic Microsoft Agent Framework adapter smoke check."""

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
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-016-maf-adapter"))
    args = parser.parse_args()

    report = run_maf_adapter_sync(args.message)
    json_path, markdown_path = write_maf_adapter_smoke(report, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"framework={report.framework_name}")
    print(f"package={report.package_name} {report.package_version}")
    print(f"workflow={report.workflow_name}")
    print(f"output_count={report.output_count}")
    print(f"model_calls_performed={report.model_calls_performed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
