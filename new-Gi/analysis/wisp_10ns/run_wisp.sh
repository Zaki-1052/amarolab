#!/bin/bash
# new-Gi/analysis/wisp_10ns/run_wisp.sh
# WISP allosteric network analysis for 5-HT2A-Gi complex (PDB 9LL8) — 10ns subset
#
# Identical to the 100ns run script but uses the 10ns traj_complex.pdb.
# Purpose: 10ns pipeline test for apples-to-apples comparison with Gq 10ns.
#
# Source:  R_ASP_76  = D155 (Ballesteros-Weinstein 3.32)
# Sink 1: A_PHE_227 = F354 (Gai1 a5 helix C-terminal tip)
# Sink 2: R_ARG_94  = R173 (DRY motif central arginine)

set -euo pipefail
cd "$(dirname "$0")"

TRAJ="traj_complex.pdb"

if [ ! -f "$TRAJ" ]; then
    echo "ERROR: $TRAJ not found. Run write_wisp_traj_10ns.py first."
    exit 1
fi

echo "=== Run 1: D155 -> Ga a5 helix (F354), full network analysis ==="
wisp "$TRAJ" \
    --source_residues R_ASP_76 \
    --sink_residues A_PHE_227 \
    --node_definition RESIDUE_COM \
    --contact_map_distance_limit 4.5 \
    --n_paths 10 \
    --n_cores 4 \
    --analyze \
    --output_dir wisp_run1_d155_to_a5 \
    2>&1 | tee wisp_run1.log

MATRIX="wisp_run1_d155_to_a5/functionalized_matrix_with_contact_map_applied.pickle"

if [ ! -f "$MATRIX" ]; then
    echo "WARNING: Saved matrix not found at $MATRIX. Run 2 will recompute."
    LOAD_FLAG=""
else
    echo ""
    echo "=== Reusing correlation matrix from Run 1 ==="
    LOAD_FLAG="--wisp_saved_matrix_path $MATRIX"
fi

echo ""
echo "=== Run 2: D155 -> DRY motif (R173) ==="
wisp "$TRAJ" \
    --source_residues R_ASP_76 \
    --sink_residues R_ARG_94 \
    --node_definition RESIDUE_COM \
    --contact_map_distance_limit 4.5 \
    --n_paths 10 \
    --n_cores 4 \
    --analyze \
    --output_dir wisp_run2_d155_to_dry \
    $LOAD_FLAG \
    2>&1 | tee wisp_run2.log

echo ""
echo "=== Done ==="
echo "Run 1 output: wisp_run1_d155_to_a5/"
echo "Run 2 output: wisp_run2_d155_to_dry/"
