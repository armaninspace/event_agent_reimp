#!/usr/bin/env python3
"""Best-effort final validation hints for Codex sessions."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED = [
    "AGENTS.md",
    ".codex/hooks.json",
    ".codex/rules/default.rules",
    "docs/installed-software.md",
    "scripts/validate.sh",
    "scripts/e2e.sh",
    "scripts/record-demo.sh",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Stop validation warning: missing required project files:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("Stop validation passed: required Codex surface files are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
