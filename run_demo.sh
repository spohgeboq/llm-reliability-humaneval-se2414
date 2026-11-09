#!/bin/bash
set -e
cd "$(dirname "$0")"
PYTHON_BIN="./venv/bin/python"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Virtual environment not found!"
    exit 1
fi

TASK_ARG="${1:-HumanEval/0}"
CONDITION_ARG="${2:-both}"

$PYTHON_BIN src/demo_single_task.py --task_id "$TASK_ARG" --condition "$CONDITION_ARG"
