#!/bin/bash
# run_production.sh — production MD blocks
# openmm_run.py auto-detects the best platform (CUDA on NVIDIA, HIP on Apple, etc.)
#
# Usage:
#   ./run_production.sh              # blocks 1-10
#   ./run_production.sh 2 10         # blocks 2-10 (pick up after block 1)

START_BLOCK=${1:-1}
END_BLOCK=${2:-10}

echo "Production MD: blocks ${START_BLOCK} through ${END_BLOCK}"

for cnt in $(seq "$START_BLOCK" "$END_BLOCK"); do
    pcnt=$(( cnt - 1 ))
    istep="step7_${cnt}"
    if [ "$cnt" -eq 1 ]; then
        pstep="step6.6_equilibration"
    else
        pstep="step7_${pcnt}"
    fi

    if [ ! -f "${pstep}.rst" ]; then
        echo "ERROR: ${pstep}.rst not found. Cannot start block ${cnt}."
        exit 1
    fi

    echo "$(date '+%H:%M:%S') Starting block ${cnt}/${END_BLOCK}..."
    python -u openmm_run.py -i step7_production.inp \
        -t toppar.str -p step5_input.psf -c step5_input.crd \
        -irst "${pstep}.rst" \
        -orst "${istep}.rst" \
        -odcd "${istep}.dcd" > "${istep}.out" 2>&1

    if [ $? -ne 0 ]; then
        echo "ERROR: Block ${cnt} failed. Check ${istep}.out"
        exit 1
    fi
    echo "$(date '+%H:%M:%S') Block ${cnt}/${END_BLOCK} complete."
done
echo "All production blocks complete."
