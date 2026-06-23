#!/usr/bin/env python3
"""Write a deterministic reference data quality smoke report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.reference_data import build_reference_quality_report, write_quality_report


def build_parser() -> argparse.ArgumentParser:
    """Create the smoke command parser."""
    parser = argparse.ArgumentParser(description="Run reference data quality checks.")
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing final runtime CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("app/runs/phase-002-reference-event-data"),
        help="Directory where smoke artifacts will be written.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the reference data smoke check."""
    args = build_parser().parse_args(argv)
    report = build_reference_quality_report(args.reference_dir)
    json_path, markdown_path = write_quality_report(report, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    for name, dataset in report.datasets.items():
        print(
            f"{name}: rows={dataset.row_count} geographies={dataset.unique_geographies} "
            f"weeks={dataset.unique_weeks} has_game_rows={dataset.has_game_rows} "
            f"warnings={len(dataset.warnings)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
