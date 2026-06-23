#!/usr/bin/env bash
set -euo pipefail

mkdir -p tmp/local tmp/pnpm-home tmp/pnpm-store tmp/npm-cache
docker run --rm -it \
  --init \
  --ipc=host \
  --mount type=bind,src="$PWD",dst=/code \
  -w /code \
  event_agent_reimp
#  -p 127.0.0.1:8621:8621 \
