#!/bin/sh
set -eu

exec codex -C /code -a never -s danger-full-access
