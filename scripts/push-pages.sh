#!/usr/bin/env bash
set -euo pipefail

remote="${1:-origin}"
branch="${2:-main}"

GIT_TERMINAL_PROMPT=0 git push "$remote" "$branch"
