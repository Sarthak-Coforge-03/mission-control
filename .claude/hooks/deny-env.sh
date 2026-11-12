#!/usr/bin/env bash
# PreToolUse: block any access to .env / .env.* files (.env.example is allowed).
python3 -c '
import json, os, re, sys
d = json.load(sys.stdin)
ti = d.get("tool_input", {})
path = ti.get("file_path") or ti.get("path") or ""
cmd = ti.get("command", "")
def is_env(name):
    return (name == ".env" or name.startswith(".env.")) and name != ".env.example"
if path and is_env(os.path.basename(path)):
    sys.exit(2)
for tok in re.findall(r"[^\s\x27\"=;|&<>()]*\.env(?:\.[\w.-]+)?\b", cmd):
    if is_env(os.path.basename(tok)):
        sys.exit(2)
' && exit 0
echo "Blocked: .env files are off limits." >&2
exit 2
