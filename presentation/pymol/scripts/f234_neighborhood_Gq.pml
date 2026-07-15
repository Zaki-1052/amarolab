# presentation/pymol/scripts/f234_neighborhood_Gq.pml
# F234 neighborhood — Gq-coupled 5-HT2A receptor
#
# Build numbering (Gq):
#   F234 = PROB 156    D155 = PROA 77     Psilocin = HETA

load ../../../analysis/phase7_summary/5ht2ar_receptor_psilocin.pdb, Gq_receptor

hide all
show cartoon, Gq_receptor
color gray80, Gq_receptor
set cartoon_transparency, 0.8

# F234 — the mobility outlier
select F234, segi PROB and resi 156
show sticks, F234
show spheres, F234
set sphere_scale, 0.25, F234
color lightblue, F234 and elem C

# Core aromatic cage
select W336, segi PROC and resi 209
select F339, segi PROC and resi 212
select F340, segi PROC and resi 213
select F243, segi PROB and resi 165
select Y370, segi PROC and resi 243
select cage, W336 or F339 or F340 or F243 or Y370

show sticks, cage
color marine, W336 and elem C
color red, F339 and elem C
color orange, F340 and elem C
color green, F243 and elem C
color purple, Y370 and elem C

# D155 salt bridge
select D155, segi PROA and resi 77
show sticks, D155
color yellow, D155 and elem C

# Psilocin
select psilocin, segi HETA
show sticks, psilocin
color hotpink, psilocin and elem C

# Show all residues within 8 A as thin lines for context
select f234_shell, byres (all within 8 of F234) and segi PROA PROB PROC
show lines, f234_shell
set line_width, 1
color gray60, f234_shell and elem C

center F234
zoom F234, 12

set ray_opaque_background, 1
bg_color white
set stick_radius, 0.12

deselect
