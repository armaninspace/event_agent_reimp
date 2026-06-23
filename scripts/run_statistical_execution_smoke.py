#!/usr/bin/env python3
"""Run governed statistical execution smoke checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.statistical_execution import build_statistical_execution_report, write_statistical_execution_smoke


def main() -> int:
    parser = argparse.ArgumentParser(description="Run statistical execution smoke checks.")
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-017-statistical-execution"))
    args = parser.parse_args()

    report = build_statistical_execution_report(args.reference_dir)
    json_path, markdown_path = write_statistical_execution_smoke(report, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"result_count={len(report['results'])}")
    print(f"method={report['method']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
