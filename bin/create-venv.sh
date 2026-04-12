#!/bin/bash

# --- Create Python virtual environments

# Imports (
. bin/shared/utils.sh
# )

set -e

# Params (
TASK_NAME="$1"
# ) Params

install-python

mkdir -p .venv

CREATE_VENV_FILE="packages${TASK_NAME:+/$TASK_NAME}/create-venv.sh"

# Execute the task's setup file
if [[ -f "$CREATE_VENV_FILE" ]]; then
  chmod +x "$CREATE_VENV_FILE"
  "$CREATE_VENV_FILE" "$TASK_NAME"
else
  python -m venv ".venv${TASK_NAME:+/TASK_NAME}"
fi

# Activate the venv
. bin/venv.sh "$TASK_NAME"

# Install dependencies
if [[ -z "$TASK_NAME" && -f "requirements.txt" ]]; then
  pip install -r requirements.txt
else
  REQUIREMENTS_TXT_FILE="packages${TASK_NAME:+/$TASK_NAME}/requirements.txt"

  if [[ -f "$REQUIREMENTS_TXT_FILE" ]]; then
    pip install -r "$REQUIREMENTS_TXT_FILE"
  fi
fi
