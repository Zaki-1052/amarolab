# presentation/pymol/scripts/rmsf_bfactor_Gi.pml
# RMSF colored by B-factor — Gi-coupled 5-HT2A receptor
#
# The B-factor column contains per-residue RMSF values (A)
# written by p3_rmsf.py.

load ../../../new-Gi/analysis/phase3_rmsf/receptor_rmsf_bfactor.pdb, Gi_rmsf

hide all
show cartoon, Gi_rmsf
spectrum b, blue_white_red, Gi_rmsf, minimum=0.3, maximum=3.0

ramp_new rmsf_ramp, Gi_rmsf, [0.3, 1.5, 3.0], [blue, white, red]
set label_size, 14

orient Gi_rmsf

set ray_opaque_background, 1
bg_color white
set ray_shadows, 0

deselect
