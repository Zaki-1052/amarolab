#!/bin/bash
# new-Gq/analysis/run_wisp.sh
# WISP allosteric network analysis for 5-HT2A-Gq complex (PDB 9AS8)
#
# Run 1: D155 (orthosteric anchor) -> V246 (Gaq a5 helix tip) + full network analysis
# Run 2: D155 -> R173 (DRY motif) — reuses Run 1's correlation matrix
#
# Source:  R_ASP_77  = D155 (Ballesteros-Weinstein 3.32), salt bridge to psilocin
# Sink 1: A_VAL_246 = Gaq a5 helix C-terminal tip (2.91 A from receptor)
# Sink 2: R_ARG_95  = R173 (DRY motif central arginine, receptor-Gaq interface)
#
# Chain ID mapping in traj_complex.pdb:
#   R = 5-HT2A receptor (segids PROA + PROB + PROC)
#   A = mini-Gaq         (segids PROD + PROE + PROF)
#   B = Gb1              (segids PROG + PROH)
#   G = Gg2              (segids PROI + PROJ)
#   L = psilocin         (segid HETA)

set -euo pipefail
cd "$(dirname "$0")"

TRAJ="traj_complex.pdb"

if [ ! -f "$TRAJ" ]; then
    echo "ERROR: $TRAJ not found. Run write_wisp_traj.py first."
    exit 1
fi

echo "=== Run 1: D155 -> Gaq a5 helix (V246), full network analysis ==="
wisp "$TRAJ" \
    --source_residues R_ASP_77 \
    --sink_residues A_VAL_246 \
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
    --source_residues R_ASP_77 \
    --sink_residues R_ARG_95 \
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
