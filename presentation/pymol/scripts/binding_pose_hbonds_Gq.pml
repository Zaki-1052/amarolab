# presentation/pymol/scripts/binding_pose_hbonds_Gq.pml
# Psilocin binding pose with H-bond distances — Gq-coupled
#
# Build numbering (Gq):
#   D155 = PROA 77     S242 = PROB 164    T160 = PROA 82
#   N343 = PROC 216    Psilocin = HETA

load ../../../analysis/phase7_summary/5ht2ar_receptor_psilocin.pdb, Gq_receptor

hide all
show cartoon, Gq_receptor
color gray80, Gq_receptor
set cartoon_transparency, 0.75

# Psilocin
select psilocin, segi HETA
show sticks, psilocin
color hotpink, psilocin and elem C

# H-bond partners
select D155, segi PROA and resi 77
select S242, segi PROB and resi 164
select T160, segi PROA and resi 82
select N343, segi PROC and resi 216

show sticks, D155 or S242 or T160 or N343
color yellow, D155 and elem C
color cyan, S242 and elem C
color palegreen, T160 and elem C
color lightorange, N343 and elem C

# H-bond distance measurements
# Amine N1 -> D155 OD1 (98% occupancy in Gq)
distance hb_amine_OD1, (segi HETA and name N1), (segi PROA and resi 77 and name OD1)

# Amine N1 -> D155 OD2 (44% occupancy in Gq)
distance hb_amine_OD2, (segi HETA and name N1), (segi PROA and resi 77 and name OD2)

# Indole NH N2 -> S242 OG (67% occupancy in Gq)
distance hb_indole_S242, (segi HETA and name N2), (segi PROB and resi 164 and name OG)

# Indole NH N2 -> T160 OG1 (19% occupancy in Gq)
distance hb_indole_T160, (segi HETA and name N2), (segi PROA and resi 82 and name OG1)

# Hydroxyl O <- N343 ND2 (3% occupancy, Gq-exclusive)
distance hb_hydroxyl_N343, (segi HETA and name O), (segi PROC and resi 216 and name ND2)

set dash_color, black
set dash_width, 2.0
set dash_gap, 0.3
set label_color, black
set label_size, 12

center psilocin
zoom psilocin, 8

set ray_opaque_background, 1
bg_color white

deselect
