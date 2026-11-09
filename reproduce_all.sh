#!/bin/bash
set -e
cd "$(dirname "$0")"
PYTHON_BIN="./venv/bin/python"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Virtual environment not found!"
    exit 1
fi

$PYTHON_BIN src/calculate_metrics.py --input_logs logs/ --output_dir results/
$PYTHON_BIN src/statistics.py --metrics_file results/task_level_metrics.csv --output results/statistical_tests_log.txt
$PYTHON_BIN src/visualize.py --metrics_file results/task_level_metrics.csv --output_dir results/figures/
