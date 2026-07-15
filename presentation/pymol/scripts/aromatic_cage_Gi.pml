# presentation/pymol/scripts/aromatic_cage_Gi.pml
# Aromatic cage around psilocin — Gi-coupled 5-HT2A receptor
#
# Build numbering (Gi): PROE offset +79, PROF offset +131
#   W336 = PROF 205    F339 = PROF 208    F340 = PROF 209
#   F234 = PROE 155    F243 = PROE 164    Y370 = PROF 239
#   Psilocin = HETA

load ../../../new-Gi/analysis/phase7_summary/5ht2ar_Gi_receptor_psilocin.pdb, Gi_receptor

hide all
show cartoon, Gi_receptor
color gray80, Gi_receptor
set cartoon_transparency, 0.75

# Aromatic cage residues
select W336, segi PROF and resi 205
select F339, segi PROF and resi 208
select F340, segi PROF and resi 209
select F234, segi PROE and resi 155
select F243, segi PROE and resi 164
select Y370, segi PROF and resi 239
select psilocin, segi HETA
select cage, W336 or F339 or F340 or F234 or F243 or Y370

show sticks, cage
show sticks, psilocin

# Color carbons by residue (heteroatoms keep standard colors)
color marine, W336 and elem C
color red, F339 and elem C
color orange, F340 and elem C
color lightblue, F234 and elem C
color green, F243 and elem C
color purple, Y370 and elem C
color hotpink, psilocin and elem C

# D155 salt bridge anchor
select D155, segi PROE and resi 76
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
