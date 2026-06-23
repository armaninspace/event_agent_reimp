#!/usr/bin/env python3
"""Best-effort pre-tool policy checks for local Codex sessions."""

from __future__ import annotations

import os
import re
import sys


SERIOUS_PATTERNS = [
    (re.compile(r"\bgit\s+push\b"), "git push requires explicit user permission"),
    (re.compile(r"\bgh\s+pr\s+merge\b"), "PR merge requires explicit user permission"),
    (re.compile(r"\brm\s+-rf\s+(/|\*|\.|~|\$HOME)\b"), "broad rm -rf is destructive"),
    (re.compile(r"\bnpm\s+publish\b|\bpnpm\s+publish\b|\byarn\s+npm\s+publish\b"), "publishing requires explicit user permission"),
]

SENSITIVE_PATHS = (".env", ".env.local", ".env.production", "secrets", "secret")


def main() -> int:
    payload = sys.stdin.read()
    command = payload or " ".join(sys.argv[1:])

    if not command:
        return 0

    for pattern, message in SERIOUS_PATTERNS:
        if pattern.search(command):
            print(f"Policy warning: {message}. Confirm permission before continuing.", file=sys.stderr)
            return 2

    lowered = command.lower()
    if any(path in lowered for path in SENSITIVE_PATHS) and re.search(r"\b(sed|tee|>|>>|rm|mv|cp)\b", command):
        print("Policy warning: command may modify secrets or environment files.", file=sys.stderr)
        return 2

    if os.environ.get("CODEX_POLICY_VERBOSE") == "1":
        print("Policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
