#!/usr/bin/env python3
"""Print concise project context at session start."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def exists(path: str) -> str:
    return "present" if (ROOT / path).exists() else "missing"


def main() -> int:
    print("Codex project context")
    print(f"- AGENTS.md: {exists('AGENTS.md')}")
    print(f"- phase skills: {exists('.agents/skills/phase-delivery/SKILL.md')}")
    print(f"- installed software log: {exists('docs/installed-software.md')}")
    print("- protocol: use phase docs, backlog slices, validation, demo, and status records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
