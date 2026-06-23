#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

check_path() {
  local path="$1"
  if [[ -e "$path" ]]; then
    echo "ok: $path"
  else
    echo "missing: $path" >&2
    failures=$((failures + 1))
  fi
}

check_executable() {
  local path="$1"
  if [[ -x "$path" ]]; then
    echo "ok executable: $path"
  else
    echo "not executable: $path" >&2
    failures=$((failures + 1))
  fi
}

required_paths=(
  "AGENTS.md"
  ".codex/hooks.json"
  ".codex/hooks/pre_tool_use_policy.py"
  ".codex/hooks/stop_validation.py"
  ".codex/hooks/session_start_context.py"
  ".codex/rules/default.rules"
  ".codex/agents/planner.toml"
  ".codex/agents/implementer.toml"
  ".codex/agents/tester.toml"
  ".codex/agents/reviewer.toml"
  ".agents/skills/phase-delivery/SKILL.md"
  ".agents/skills/install-and-note/SKILL.md"
  ".agents/skills/backlog-slice/SKILL.md"
  ".agents/skills/demo-and-status/SKILL.md"
  ".agents/skills/replan-on-block/SKILL.md"
  "docs/installed-software.md"
  "docs/phases"
  "docs/backlog"
  "docs/demos"
  "docs/deliverables-status"
  "docs/adr"
  "docs/adr/0001-codex-surface.md"
  "scripts/validate.sh"
  "scripts/e2e.sh"
  "scripts/record-demo.sh"
)

for path in "${required_paths[@]}"; do
  check_path "$path"
done

for path in \
  ".codex/hooks/pre_tool_use_policy.py" \
  ".codex/hooks/stop_validation.py" \
  ".codex/hooks/session_start_context.py" \
  "scripts/validate.sh" \
  "scripts/e2e.sh" \
  "scripts/record-demo.sh"; do
  check_executable "$path"
done

python3 .codex/hooks/session_start_context.py >/tmp/codex-session-start.out
python3 .codex/hooks/stop_validation.py >/tmp/codex-stop-validation.out
echo "ok: hook scripts execute"

if [[ -f package.json ]]; then
  if command -v pnpm >/dev/null 2>&1 && [[ -f pnpm-lock.yaml ]]; then
    pnpm test
  elif command -v npm >/dev/null 2>&1; then
    npm test
  else
    echo "skip: package.json present but npm/pnpm unavailable"
  fi
elif [[ -f pyproject.toml || -d tests ]]; then
  if command -v pytest >/dev/null 2>&1; then
    pytest
  else
    echo "skip: Python tests detected but pytest unavailable"
  fi
else
  echo "skip: no project test manifest detected"
fi

bash scripts/e2e.sh

if [[ "$failures" -gt 0 ]]; then
  echo "validation failed with $failures missing or non-executable required item(s)" >&2
  exit 1
fi

echo "validation passed"
