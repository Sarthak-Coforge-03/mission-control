#!/usr/bin/env bash
# Stop: run the test suite; any failure (including no tests collected) blocks the stop.
active=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("stop_hook_active", False))')
[[ "$active" == "True" ]] && exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 2
if ! out=$(uv run pytest -q 2>&1); then
  echo "Tests failed:" >&2
  echo "$out" | tail -30 >&2
  exit 2
fi
