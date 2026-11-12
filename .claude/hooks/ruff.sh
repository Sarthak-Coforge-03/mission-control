#!/usr/bin/env bash
# PostToolUse: lint + format the edited Python file.
file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
[[ "$file" == *.py && -f "$file" ]] || exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0
uv run ruff format -q "$file"
if ! out=$(uv run ruff check --fix -q "$file" 2>&1); then
  echo "ruff found issues it could not fix in $file:" >&2
  echo "$out" >&2
  exit 2
fi
