# presentation/pymol/scripts/aromatic_cage_Gq.pml
# Aromatic cage around psilocin — Gq-coupled 5-HT2A receptor
#
# Build numbering (Gq): PROA/PROB offset +78, PROC offset +127
#   W336 = PROC 209    F339 = PROC 212    F340 = PROC 213
#   F234 = PROB 156    F243 = PROB 165    Y370 = PROC 243
#   Psilocin = HETA

load ../../../analysis/phase7_summary/5ht2ar_receptor_psilocin.pdb, Gq_receptor

hide all
show cartoon, Gq_receptor
color gray80, Gq_receptor
set cartoon_transparency, 0.75

# Aromatic cage residues
select W336, segi PROC and resi 209
select F339, segi PROC and resi 212
select F340, segi PROC and resi 213
select F234, segi PROB and resi 156
select F243, segi PROB and resi 165
select Y370, segi PROC and resi 243
select psilocin, segi HETA
select cage, W336 or F339 or F340 or F234 or F243 or Y370

show sticks, cage
show sticks, psilocin

color marine, W336 and elem C
color red, F339 and elem C
color orange, F340 and elem C
color lightblue, F234 and elem C
color green, F243 and elem C
color purple, Y370 and elem C
color hotpink, psilocin and elem C

# D155 salt bridge anchor
select D155, segi PROA and resi 77
show sticks, D155
color yellow, D155 and elem C

center psilocin
zoom psilocin, 12

set ray_opaque_background, 1
bg_color white
set ray_shadows, 0
set stick_radius, 0.12
set label_size, 14

deselect
