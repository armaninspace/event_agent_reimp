#!/usr/bin/env bash
#
# Pull this repo and its managed nested repos in dependency order.
#
# Correct order:
#   1. Pull the parent repo first so .gitmodules and submodule pointers are current.
#   2. Initialize/update registered submodules to the parent-recorded commits.
#   3. Pull each managed nested repo branch so working trees are current too.
#
# Usage:
#   ./pull.sh
#   ./pull.sh --dry-run
#   ./pull.sh --rebase
#   ./pull.sh --allow-dirty
#   ./pull.sh --nested-only
#
# By default, this refuses to run when either repo has uncommitted changes.
# Use --allow-dirty only when you intentionally want git pull to merge/rebase
# around local work.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

REMOTE="origin"
MANAGED_REPOS=(
  "event_agent_tutorial"
  "event_agent_designnotes"
)
DRY_RUN=0
REBASE=0
ALLOW_DIRTY=0
NESTED_ONLY=0

usage() {
  sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'
}

run() {
  echo "+ $*"
  if [[ "$DRY_RUN" -eq 0 ]]; then
    "$@"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --rebase)
      REBASE=1
      shift
      ;;
    --allow-dirty)
      ALLOW_DIRTY=1
      shift
      ;;
    --nested-only)
      NESTED_ONLY=1
      shift
      ;;
    --submodule-only)
      NESTED_ONLY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

require_repo() {
  local dir="$1"
  if ! git -C "$dir" rev-parse --show-toplevel >/dev/null 2>&1; then
    echo "Not a git repo: $dir" >&2
    exit 1
  fi
}

current_branch() {
  local dir="$1"
  local branch
  branch="$(git -C "$dir" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  if [[ -z "$branch" ]]; then
    branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  fi
  if [[ -z "$branch" || "$branch" == "HEAD" ]]; then
    echo "Detached HEAD in $dir; check out a branch before pulling." >&2
    exit 1
  fi
  printf '%s\n' "$branch"
}

require_clean() {
  local dir="$1"
  local label="$2"
  if [[ "$ALLOW_DIRTY" -eq 0 && -n "$(git -C "$dir" status --porcelain)" ]]; then
    echo "$label has uncommitted changes: $dir" >&2
    echo "Commit/stash them first, or rerun with --allow-dirty." >&2
    exit 1
  fi
}

pull_current_branch() {
  local dir="$1"
  local branch="$2"
  if [[ "$REBASE" -eq 1 ]]; then
    run git -C "$dir" pull --rebase "$REMOTE" "$branch"
  else
    run git -C "$dir" pull "$REMOTE" "$branch"
  fi
}

is_registered_gitlink() {
  local dir="$1"
  git ls-files --stage -- "$dir" | awk '$1 == "160000" { found = 1 } END { exit found ? 0 : 1 }'
}

require_repo "$ROOT"
parent_branch="$(current_branch "$ROOT")"

available_repos=()
registered_submodules=()
for repo_dir in "${MANAGED_REPOS[@]}"; do
  if [[ -d "$repo_dir" ]]; then
    require_repo "$repo_dir"
    available_repos+=("$repo_dir")
  fi
  if is_registered_gitlink "$repo_dir"; then
    registered_submodules+=("$repo_dir")
  fi
done

echo "Parent repo     : $ROOT"
echo "Parent branch   : $parent_branch"
echo "Remote          : $REMOTE"
echo "Managed repos   : ${MANAGED_REPOS[*]}"
echo "Available repos : ${available_repos[*]:-(none)}"
echo "Registered links: ${registered_submodules[*]:-(none)}"
if [[ "$NESTED_ONLY" -eq 1 ]]; then
  echo "Mode            : nested only"
fi
echo

if [[ "$NESTED_ONLY" -eq 0 ]]; then
  require_clean "$ROOT" "Parent repo"
fi

for repo_dir in "${available_repos[@]}"; do
  require_clean "$repo_dir" "Managed repo $repo_dir"
done

if [[ "$NESTED_ONLY" -eq 0 ]]; then
  echo "==> Step 1: pull parent repo"
  pull_current_branch "$ROOT" "$parent_branch"

  echo
  echo "==> Step 2: initialize and update registered submodules to parent pointers"
  if [[ "${#registered_submodules[@]}" -gt 0 ]]; then
    run git submodule update --init --recursive "${registered_submodules[@]}"
  else
    echo "No registered submodules found."
  fi
else
  echo "==> Step 1: skip parent pull because --nested-only was requested"
  echo "Parent repo dirty state is preserved."
fi

available_repos=()
for repo_dir in "${MANAGED_REPOS[@]}"; do
  if [[ -d "$repo_dir" ]]; then
    require_repo "$repo_dir"
    available_repos+=("$repo_dir")
  else
    echo "Skipping missing managed repo after update: $repo_dir"
  fi
done

echo
echo "==> Step 3: pull managed nested repo branches"
for repo_dir in "${available_repos[@]}"; do
  branch="$(current_branch "$repo_dir")"
  echo "-- $repo_dir ($branch)"
  pull_current_branch "$repo_dir" "$branch"
done

echo
echo "==> Step 4: refresh parent submodule pointer state"
if [[ "${#registered_submodules[@]}" -gt 0 ]]; then
  run git submodule status --recursive "${registered_submodules[@]}"
else
  echo "No registered submodules found."
fi

if [[ "$NESTED_ONLY" -eq 1 ]]; then
  echo
  echo "Nested-only pull complete. If a registered submodule moved, the parent repo"
  echo "will show it as modified until you commit the updated submodule pointer."
fi

echo
echo "Done."
