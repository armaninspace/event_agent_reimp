#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

phase_id="${1:-phase-000-codex-surface}"
demo_doc="docs/demos/${phase_id}-demo.md"

mkdir -p docs/demos demos

if [[ ! -f "$demo_doc" ]]; then
  cat > "$demo_doc" <<EOF_DEMO
# Demo: ${phase_id}

## Setup

TBD

## Commands

TBD

## Expected Behavior

TBD

## Observed Behavior

TBD

## Evidence

TBD

## Video

No video has been recorded yet. For non-UI phases, replace this with a non-applicability rationale and command-output evidence.

## Known Gaps

TBD

## Requirement Mapping

TBD
EOF_DEMO
  echo "created demo template: $demo_doc"
else
  echo "demo document already exists: $demo_doc"
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is available for future video capture."
  echo "Example: ffmpeg -video_size 1280x720 -framerate 30 -f x11grab -i :99.0 demos/${phase_id}.mp4"
else
  echo "video recording unavailable: ffmpeg not found. Document this blocker if the phase requires video."
fi
