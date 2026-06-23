"""Command-line entry point for event-agent evidence packet generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from app.evidence_packet import DEFAULT_QUESTION, build_static_evidence_packet, write_evidence_packet


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Generate a deterministic static evidence packet.")
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing final runtime CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("app/runs/phase-001-static-evidence-packet"),
        help="Directory where packet artifacts will be written.",
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Public question to include in the packet.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the static evidence packet CLI."""
    args = build_parser().parse_args(argv)
    packet = build_static_evidence_packet(reference_dir=args.reference_dir, question=args.question)
    artifacts = write_evidence_packet(packet, args.output_dir)
    print(f"wrote {artifacts.json_path}")
    print(f"wrote {artifacts.markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
