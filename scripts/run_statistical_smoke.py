#!/usr/bin/env python3
"""Run exploratory statistical smoke checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.statistical_tests import run_exploratory_tests, write_statistical_smoke


def build_parser() -> argparse.ArgumentParser:
    """Create parser for statistical smoke command."""
    parser = argparse.ArgumentParser(description="Run exploratory statistical smoke checks.")
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("app/runs/phase-010-exploratory-statistical-tests"),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run statistical smoke checks."""
    args = build_parser().parse_args(argv)
    report = run_exploratory_tests(args.reference_dir)
    json_path, markdown_path = write_statistical_smoke(report, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    print(f"results={len(report['results'])}")
    print(f"not_testable_count={report['not_testable_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
