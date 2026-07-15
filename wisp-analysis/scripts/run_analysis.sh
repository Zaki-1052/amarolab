#!/usr/bin/env bash
# wisp-analysis/scripts/run_analysis.sh
# Run the WISP analysis pipeline for all runs defined in a config.
#
# Usage: bash wisp-analysis/scripts/run_analysis.sh <config.yaml> [output_base] [cutoff]

set -euo pipefail

CONFIG="${1:?Usage: $0 <config.yaml> [output_base] [cutoff]}"
OUTPUT_BASE="${2:-results/$(basename "$CONFIG" .yaml)}"
CUTOFF="${3:-10}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN="$SCRIPT_DIR/../main.py"

if [[ ! -f "$CONFIG" ]]; then
    echo "Config not found: $CONFIG"
    exit 1
fi

RUN_NAMES=$(awk '/^wisp_runs:/{f=1; next} f && /^[a-zA-Z]/{exit} f' "$CONFIG" | grep -E '^\s+- name:' | sed 's/.*name: *//')

for RUN in $RUN_NAMES; do
    echo "=== Analyzing $RUN ==="
    python "$MAIN" analyze "$CONFIG" --run "$RUN" --output "$OUTPUT_BASE/$RUN" --cutoff "$CUTOFF"
    echo ""
done

echo "All runs complete. Output in: $OUTPUT_BASE/"
