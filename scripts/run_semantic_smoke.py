#!/usr/bin/env python3
"""Run semantic SQL smoke queries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.semantic_layer import SemanticLayer, write_semantic_smoke


def build_parser() -> argparse.ArgumentParser:
    """Create parser for semantic smoke command."""
    parser = argparse.ArgumentParser(description="Run governed semantic SQL smoke queries.")
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--output-dir", type=Path, default=Path("app/runs/phase-011-semantic-layer"))
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run semantic smoke queries."""
    args = build_parser().parse_args(argv)
    layer = SemanticLayer(args.reference_dir, row_limit=10)
    results = [
        layer.query("select week_start_monday, revenue_all, has_game from city_week_events where has_game = 1"),
        layer.query("select msa_code, week_start_monday, merchants_all from msa_week_events where has_game = 1"),
    ]
    json_path, markdown_path = write_semantic_smoke(results, args.output_dir)
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    for result in results:
        print(f"views={','.join(result.referenced_views)} rows={result.row_count} columns={','.join(result.columns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
