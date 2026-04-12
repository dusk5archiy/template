# Params (
TASK_NAME=$1
# )

python -m venv \
  ".venv${TASK_NAME:+/TASK_NAME}"

# other options:
# --system-site-packages
