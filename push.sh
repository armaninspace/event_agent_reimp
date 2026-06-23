#!/usr/bin/env bash
#
# Push this repo and its managed nested repos in dependency order.
#
# Correct order:
#   1. Commit and push nested repos first.
#   2. Commit and push the parent repo pointer for registered submodules.
#
# Usage:
#   ./push.sh
#   ./push.sh --dry-run
#   ./push.sh --parent-all
#   ./push.sh --nested-message "Update nested repos"
#   ./push.sh --parent-message "Update submodule pointer"
#
# By default, the parent commit stages only .gitmodules and the submodule
# pointer. Use --parent-all only when you intentionally want to commit every
# parent-repo change as well.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

REMOTE="origin"
MANAGED_REPOS=(
  "event_agent_tutorial"
  "event_agent_designnotes"
)
NESTED_COMMIT_MESSAGE="Update managed nested repos"
PARENT_COMMIT_MESSAGE="Update managed repo pointers"
DRY_RUN=0
PARENT_ALL=0

usage() {
  sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
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
    --parent-all)
      PARENT_ALL=1
      shift
      ;;
    --nested-message)
      NESTED_COMMIT_MESSAGE="${2:?missing value for --nested-message}"
      shift 2
      ;;
    --submodule-message)
      NESTED_COMMIT_MESSAGE="${2:?missing value for --submodule-message}"
      shift 2
      ;;
    --parent-message)
      PARENT_COMMIT_MESSAGE="${2:?missing value for --parent-message}"
      shift 2
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
    echo "Detached HEAD in $dir; check out a branch before pushing." >&2
    exit 1
  fi
  printf '%s\n' "$branch"
}

is_registered_gitlink() {
  local dir="$1"
  git ls-files --stage -- "$dir" | awk '$1 == "160000" { found = 1 } END { exit found ? 0 : 1 }'
}

is_configured_submodule() {
  local dir="$1"
  [[ -f .gitmodules ]] || return 1
  git config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null \
    | awk -v dir="$dir" '$2 == dir { found = 1 } END { exit found ? 0 : 1 }'
}

require_repo "$ROOT"

available_repos=()
registered_submodules=()
for repo_dir in "${MANAGED_REPOS[@]}"; do
  if [[ ! -d "$repo_dir" ]]; then
    echo "Skipping missing managed repo: $repo_dir"
    continue
  fi
  require_repo "$repo_dir"
  available_repos+=("$repo_dir")
  if is_registered_gitlink "$repo_dir" || is_configured_submodule "$repo_dir"; then
    registered_submodules+=("$repo_dir")
  fi
done

parent_branch="$(current_branch "$ROOT")"

echo "Parent repo     : $ROOT"
echo "Parent branch   : $parent_branch"
echo "Remote          : $REMOTE"
echo "Managed repos   : ${available_repos[*]:-(none)}"
echo "Registered links: ${registered_submodules[*]:-(none)}"
echo

echo "==> Step 1: commit nested repo changes"
for repo_dir in "${available_repos[@]}"; do
  branch="$(current_branch "$repo_dir")"
  echo "-- $repo_dir ($branch)"
  if [[ -n "$(git -C "$repo_dir" status --porcelain)" ]]; then
    run git -C "$repo_dir" add -A
    run git -C "$repo_dir" commit -m "$NESTED_COMMIT_MESSAGE"
  else
    echo "No changes to commit in $repo_dir."
  fi
done

echo
echo "==> Step 2: push nested repos first"
for repo_dir in "${available_repos[@]}"; do
  branch="$(current_branch "$repo_dir")"
  run git -C "$repo_dir" push -u "$REMOTE" "$branch"
done

echo
echo "==> Step 3: stage parent repo changes"
if [[ "$PARENT_ALL" -eq 1 ]]; then
  echo "Staging all parent changes because --parent-all was provided."
  run git add -A
else
  echo "Staging only .gitmodules and registered submodule pointers."
  run git add .gitmodules
  for repo_dir in "${registered_submodules[@]}"; do
    run git add "$repo_dir"
  done
  for repo_dir in "${available_repos[@]}"; do
    if ! is_registered_gitlink "$repo_dir" && ! is_configured_submodule "$repo_dir"; then
      echo "Note: $repo_dir is a nested git repo but is not a registered parent gitlink; not staging it in parent."
    fi
  done
fi

echo
echo "==> Step 4: commit parent repo"
if [[ -n "$(git diff --cached --name-only)" ]]; then
  run git commit -m "$PARENT_COMMIT_MESSAGE"
else
  echo "No staged parent changes to commit."
fi

echo
echo "==> Step 5: push parent repo"
run git push -u "$REMOTE" "$parent_branch"

echo
echo "Done."
