# presentation/pymol/scripts/rmsf_bfactor_Gq.pml
# RMSF colored by B-factor — Gq-coupled 5-HT2A receptor

load ../../../analysis/phase3_rmsf/receptor_rmsf_bfactor.pdb, Gq_rmsf

hide all
show cartoon, Gq_rmsf
spectrum b, blue_white_red, Gq_rmsf, minimum=0.3, maximum=3.0

ramp_new rmsf_ramp, Gq_rmsf, [0.3, 1.5, 3.0], [blue, white, red]
set label_size, 14

orient Gq_rmsf

set ray_opaque_background, 1
bg_color white
set ray_shadows, 0

deselect
