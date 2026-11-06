#!/usr/bin/env bash
set -euo pipefail
if ! command -v uv >/dev/null 2>&1; then
  echo 'Install uv first: https://docs.astral.sh/uv/getting-started/installation/' >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo 'Git is required.' >&2
  exit 1
fi
uv tool install --python 3.12 'git+https://github.com/jakecyr/chatgpt-voice-assistant.git'
echo 'Installed. Set OPENAI_API_KEY, then run gptassist. Ensure the uv tool bin directory is on your PATH (uv tool update-shell).'
