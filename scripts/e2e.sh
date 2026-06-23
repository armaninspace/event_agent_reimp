#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f playwright.config.ts || -f playwright.config.js ]]; then
  if command -v pnpm >/dev/null 2>&1 && [[ -f pnpm-lock.yaml ]]; then
    pnpm exec playwright test
  elif command -v npx >/dev/null 2>&1; then
    npx playwright test
  else
    echo "playwright config found, but no playable Node runner is available" >&2
    exit 1
  fi
elif [[ -d e2e ]]; then
  if command -v pytest >/dev/null 2>&1 && find e2e -name '*.py' -print -quit | grep -q .; then
    pytest e2e
  else
    echo "e2e directory found, but no supported e2e runner was detected"
  fi
else
  echo "no e2e suite detected; nothing to run"
fi
