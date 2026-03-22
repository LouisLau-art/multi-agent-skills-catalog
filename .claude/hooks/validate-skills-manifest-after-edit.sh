#!/usr/bin/env bash

set -euo pipefail

input=$(cat)
file_path=$(printf '%s' "$input" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))')

if [[ -z "$file_path" || "$file_path" != *skills_manifest.csv* || ! -f "$file_path" ]]; then
  exit 0
fi

python3 - "$file_path" <<'PY'
import csv
import sys

path = sys.argv[1]
with open(path, newline="") as f:
    reader = csv.reader(f)
    next(reader, None)
    rows = sum(1 for _ in reader)

print(f"Valid CSV with {rows} skill rows")
PY
