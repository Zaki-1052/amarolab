#!/usr/bin/env bash
# new-Gi/analysis/run_all.sh
# Runs the complete 9LL8 (Gi-coupled) analysis pipeline.
# Usage: cd to new-Gi/analysis/, then: bash run_all.sh
#
# Each phase writes output to its own directory and logs stdout to a .txt file.
# Phase 7 depends on phase 2's CSV. Cross-phase depends on phases 3 + 6.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TOTAL_START=$(date +%s)

run_phase() {
    local phase_name="$1"
    local script_path="$2"

    echo "──────────────────────────────────────────"
    echo "  $phase_name"
    echo "──────────────────────────────────────────"

    local phase_dir
    phase_dir="$(dirname "$script_path")"
    local log_file="${phase_dir}/${phase_name}.txt"

    local start=$(date +%s)
    python "$script_path" 2>&1 | tee "$log_file"
    local end=$(date +%s)
    local elapsed=$((end - start))

    echo ""
    echo "  -> ${phase_name} completed in ${elapsed}s"
    echo "  -> Log: ${log_file}"
    echo ""
}

echo ""
echo "============================================"
echo "  9LL8 (Gi-coupled) Analysis Pipeline"
echo "============================================"
echo ""
echo "Working directory: $SCRIPT_DIR"
echo "Started: $(date)"
echo ""

run_phase "phase2_rmsd" "phase2_rmsd/p2_rmsd.py"
run_phase "phase3_rmsf" "phase3_rmsf/p3_rmsf.py"
run_phase "phase4_psilocin" "phase4_psilocin/p4_psilocin.py"
run_phase "phase5_lipid_order" "phase5_lipid_order/p5_lipid_order.py"
run_phase "phase6_contacts" "phase6_contacts/p6_contacts.py"
run_phase "phase7_summary" "phase7_summary/p7_snapshot.py"
run_phase "phase8_hbonds" "phase8_hbonds/p8b_hbond_detail.py"
run_phase "phase9_aromatics" "phase9_aromatics/p9_aromatics.py"
run_phase "phase10_rotamers" "phase10_rotamers/p10_rotamers.py"
run_phase "crossphase" "p_crossphase.py"

TOTAL_END=$(date +%s)
TOTAL_ELAPSED=$((TOTAL_END - TOTAL_START))

echo "============================================"
echo "  Pipeline complete"
echo "============================================"
echo ""
echo "Total wall time: ${TOTAL_ELAPSED}s ($(( TOTAL_ELAPSED / 60 ))m $(( TOTAL_ELAPSED % 60 ))s)"
echo "Finished: $(date)"
echo ""
echo "Output summary:"
echo ""

for dir in phase2_rmsd phase3_rmsf phase4_psilocin phase5_lipid_order \
           phase6_contacts phase7_summary phase8_hbonds phase9_aromatics \
           phase10_rotamers; do
    n_png=$(find "$dir" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
    n_csv=$(find "$dir" -name "*.csv" 2>/dev/null | wc -l | tr -d ' ')
    n_pdb=$(find "$dir" -name "*.pdb" 2>/dev/null | wc -l | tr -d ' ')
    echo "  ${dir}: ${n_png} PNG, ${n_csv} CSV, ${n_pdb} PDB"
done

n_cross_png=$(find . -maxdepth 1 -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
echo "  crossphase: ${n_cross_png} PNG"
echo ""
