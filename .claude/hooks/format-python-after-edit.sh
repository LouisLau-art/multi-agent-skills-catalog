#!/usr/bin/env bash

set -euo pipefail

input=$(cat)
file_path=$(printf '%s' "$input" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))')

if [[ -z "$file_path" || "$file_path" != *.py || ! -f "$file_path" ]]; then
  exit 0
fi

python3 -m black "$file_path" 2>/dev/null || \
  python3 -m yapf -i "$file_path" 2>/dev/null || \
  echo "No formatter available"
