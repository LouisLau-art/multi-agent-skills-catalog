#!/usr/bin/env bash

set -euo pipefail

input=$(cat)
file_path=$(printf '%s' "$input" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))')

case "$file_path" in
  *package-lock.json|*yarn.lock|*pnpm-lock.yaml)
    echo "Lock file edits are blocked. Use the package manager instead." >&2
    exit 2
    ;;
  *)
    exit 0
    ;;
esac
