#!/usr/bin/env bash
set -euo pipefail

echo "Creating virtual environment in .venv..."
# Use PYTHON env var or python3 by default
PY_CMD="${PYTHON:-python3}"

if ! command -v "$PY_CMD" >/dev/null 2>&1; then
  echo "Python not found: $PY_CMD" >&2
  exit 1
fi

$PY_CMD -m venv .venv

VENV_PY=".venv/bin/python"
if [ ! -x "$VENV_PY" ]; then
  echo "Virtualenv python not found at $VENV_PY" >&2
  exit 1
fi

echo "Upgrading pip and installing requirements (if any)..."
"$VENV_PY" -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  "$VENV_PY" -m pip install -r requirements.txt || true
fi

echo "Initializing SQLite database at Databases/TodoList.db from resources/TodoListSetup.sql..."
if [ ! -f "resources/TodoListSetup.sql" ]; then
  echo "Schema file resources/TodoListSetup.sql not found." >&2
  exit 1
fi

mkdir -p Databases

