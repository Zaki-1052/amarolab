# presentation/pymol/scripts/binding_pose_hbonds_Gi.pml
# Psilocin binding pose with H-bond distances — Gi-coupled
#
# Build numbering (Gi):
#   D155 = PROE 76     S242 = PROE 163    T160 = PROE 81
#   Psilocin = HETA (N1=amine, N2=indole NH, O=hydroxyl)

load ../../../new-Gi/analysis/phase7_summary/5ht2ar_Gi_receptor_psilocin.pdb, Gi_receptor

hide all
show cartoon, Gi_receptor
color gray80, Gi_receptor
set cartoon_transparency, 0.75

# Psilocin
select psilocin, segi HETA
show sticks, psilocin
color hotpink, psilocin and elem C

# H-bond partners
select D155, segi PROE and resi 76
select S242, segi PROE and resi 163
select T160, segi PROE and resi 81

show sticks, D155 or S242 or T160
color yellow, D155 and elem C
color cyan, S242 and elem C
color palegreen, T160 and elem C

# H-bond distance measurements
# Amine N1 -> D155 OD1 (93% occupancy in Gi)
distance hb_amine_OD1, (segi HETA and name N1), (segi PROE and resi 76 and name OD1)

# Amine N1 -> D155 OD2 (61% occupancy in Gi)
distance hb_amine_OD2, (segi HETA and name N1), (segi PROE and resi 76 and name OD2)

# Indole NH N2 -> S242 OG (54% occupancy in Gi)
distance hb_indole_S242, (segi HETA and name N2), (segi PROE and resi 163 and name OG)

# Indole NH N2 -> T160 OG1 (17% occupancy in Gi)
distance hb_indole_T160, (segi HETA and name N2), (segi PROE and resi 81 and name OG1)

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
