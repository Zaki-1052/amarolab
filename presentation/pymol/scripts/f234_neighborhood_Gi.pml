# presentation/pymol/scripts/f234_neighborhood_Gi.pml
# F234 neighborhood — Gi-coupled 5-HT2A receptor
#
# Build numbering (Gi):
#   F234 = PROE 155    D155 = PROE 76     Psilocin = HETA
# Nearby pocket residues (within 8 A of F234) will vary;
# this shows the core aromatic cage + D155 + psilocin context.

load ../../../new-Gi/analysis/phase7_summary/5ht2ar_Gi_receptor_psilocin.pdb, Gi_receptor

hide all
show cartoon, Gi_receptor
color gray80, Gi_receptor
set cartoon_transparency, 0.8

# F234 — the mobility outlier
select F234, segi PROE and resi 155
show sticks, F234
show spheres, F234
set sphere_scale, 0.25, F234
color lightblue, F234 and elem C

# Immediate neighbors (within ~8 A of F234 in the pocket)
# Core aromatic cage
select W336, segi PROF and resi 205
select F339, segi PROF and resi 208
select F340, segi PROF and resi 209
select F243, segi PROE and resi 164
select Y370, segi PROF and resi 239
select cage, W336 or F339 or F340 or F243 or Y370

show sticks, cage
color marine, W336 and elem C
color red, F339 and elem C
color orange, F340 and elem C
color green, F243 and elem C
color purple, Y370 and elem C

# D155 salt bridge
select D155, segi PROE and resi 76
show sticks, D155
color yellow, D155 and elem C

# Psilocin
select psilocin, segi HETA
show sticks, psilocin
color hotpink, psilocin and elem C

# Show all residues within 8 A as thin lines for context
select f234_shell, byres (all within 8 of F234) and segi PROE PROF
show lines, f234_shell
set line_width, 1
color gray60, f234_shell and elem C

center F234
zoom F234, 12

set ray_opaque_background, 1
bg_color white
set stick_radius, 0.12

deselect
