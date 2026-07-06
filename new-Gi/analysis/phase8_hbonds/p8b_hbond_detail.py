# new-Gi/analysis/phase8_hbonds/p8b_hbond_detail.py
#
# Corrected H-bond analysis with explicit donor/acceptor chemistry.
# Uses hand-built donor/acceptor tables rather than MDAnalysis
# HydrogenBondAnalysis, which misclassifies psilocin C-H groups
# as H-bond donors due to CGenFF atom types.
from pathlib import Path
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_angles
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'charmm-gui-8313215931' / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)
n_frames = len(u.trajectory)
times_ns = np.arange(n_frames) * 0.1

OFFSETS = {'PROE': 79, 'PROF': 131}

def lit_resid(resid, segid):
    return resid + OFFSETS.get(segid, 0)

DA_CUTOFF = 3.5
DHA_ANGLE_CUTOFF = 130.0

GROUP_COLORS = {
    'amine':     '#d7191c',
    'hydroxyl':  '#2c7bb6',
    'indole NH': '#fdae61',
}

# ── Build pocket selection (same as phase 4) ─────────────────

u.trajectory[0]
pocket_dynamic = u.select_atoms(
    "(segid PROE PROF) and (around 5.0 (segid HETA))")

pocket_resids_by_seg = {}
for res in pocket_dynamic.residues:
    seg = res.segid
    pocket_resids_by_seg.setdefault(seg, []).append(str(res.resid))

pocket_parts = []
for seg, rids in pocket_resids_by_seg.items():
    pocket_parts.append(f"(segid {seg} and resid {' '.join(rids)})")
POCKET_SEL = " or ".join(pocket_parts)
pocket_residues = u.select_atoms(POCKET_SEL).residues

print(f"Binding pocket: {len(pocket_residues)} residues")

# ── Define psilocin H-bond groups ────────────────────────────

PSI_DONORS = [
    ('N1', 'H17', 'amine'),
    ('N2', 'H13', 'indole NH'),
    ('O',  'H16', 'hydroxyl'),
]

psi_donor_atoms = {}
for heavy, h, group in PSI_DONORS:
    ag_heavy = u.select_atoms(f"segid HETA and name {heavy}")
    ag_h     = u.select_atoms(f"segid HETA and name {h}")
    assert len(ag_heavy) == 1 and len(ag_h) == 1, \
        f"Psilocin {heavy}/{h}: got {len(ag_heavy)}/{len(ag_h)}"
    psi_donor_atoms[(heavy, h)] = (ag_heavy, ag_h, group)

psi_acceptor = u.select_atoms("segid HETA and name O")
assert len(psi_acceptor) == 1

# ── Enumerate protein donors and acceptors ───────────────────

SC_DONOR_DEFS = {
    'SER': [('OG', 'HG1')],
    'THR': [('OG1', 'HG1')],
    'TYR': [('OH', 'HH')],
    'TRP': [('NE1', 'HE1')],
    'ASN': [('ND2', 'HD21'), ('ND2', 'HD22')],
    'GLN': [('NE2', 'HE21'), ('NE2', 'HE22')],
    'LYS': [('NZ', 'HZ1'), ('NZ', 'HZ2'), ('NZ', 'HZ3')],
    'ARG': [('NE', 'HE'), ('NH1', 'HH11'), ('NH1', 'HH12'),
            ('NH2', 'HH21'), ('NH2', 'HH22')],
    'HIS': [('ND1', 'HD1'), ('NE2', 'HE2')],
}

SC_ACCEPTOR_DEFS = {
    'ASP': ['OD1', 'OD2'],
    'GLU': ['OE1', 'OE2'],
    'SER': ['OG'],
    'THR': ['OG1'],
    'TYR': ['OH'],
    'ASN': ['OD1'],
    'GLN': ['OE1'],
    'HIS': ['ND1', 'NE2'],
    'MET': ['SD'],
    'CYS': ['SG'],
}

protein_donors = []
protein_acceptors = []

for res in sorted(pocket_residues, key=lambda r: (r.segid, r.resid)):
    base = f"segid {res.segid} and resid {res.resid}"
    lit = lit_resid(res.resid, res.segid)

    n_atom  = u.select_atoms(f"{base} and name N")
    hn_atom = u.select_atoms(f"{base} and name HN")
    if len(n_atom) == 1 and len(hn_atom) == 1:
        protein_donors.append((n_atom, hn_atom, True, res, lit))

    o_atom = u.select_atoms(f"{base} and name O")
    if len(o_atom) == 1:
        protein_acceptors.append((o_atom, True, res, lit))

    for heavy_name, h_name in SC_DONOR_DEFS.get(res.resname, []):
        ag_heavy = u.select_atoms(f"{base} and name {heavy_name}")
        ag_h     = u.select_atoms(f"{base} and name {h_name}")
        if len(ag_heavy) == 1 and len(ag_h) == 1:
            protein_donors.append((ag_heavy, ag_h, False, res, lit))

    for acc_name in SC_ACCEPTOR_DEFS.get(res.resname, []):
        ag_acc = u.select_atoms(f"{base} and name {acc_name}")
        if len(ag_acc) == 1:
            protein_acceptors.append((ag_acc, False, res, lit))

print(f"Protein donor-H pairs: {len(protein_donors)} "
      f"({sum(1 for d in protein_donors if d[2])} BB, "
      f"{sum(1 for d in protein_donors if not d[2])} SC)")
print(f"Protein acceptor atoms: {len(protein_acceptors)} "
      f"({sum(1 for a in protein_acceptors if a[1])} BB, "
      f"{sum(1 for a in protein_acceptors if not a[1])} SC)")

# ── Frame loop: detect real H-bonds ──────────────────────────

hbond_records = []

for fi, ts in enumerate(u.trajectory):
    # Psilocin donating to protein acceptors
    for (psi_heavy, psi_h, psi_group) in psi_donor_atoms.values():
        d_pos = psi_heavy.positions[0]
        h_pos = psi_h.positions[0]

        for (acc_ag, is_bb, res, lit) in protein_acceptors:
            a_pos = acc_ag.positions[0]
            dist = np.linalg.norm(d_pos - a_pos)
            if dist < DA_CUTOFF:
                angle_rad = calc_angles(d_pos, h_pos, a_pos)
                angle_deg = np.degrees(float(angle_rad))
                if angle_deg > DHA_ANGLE_CUTOFF:
                    bb_sc = 'BB' if is_bb else 'SC'
                    label = (f"{psi_heavy.atoms[0].name}-{psi_h.atoms[0].name} → "
                             f"{res.resname}{lit}:{acc_ag.atoms[0].name}")
                    hbond_records.append((
                        fi, psi_group, bb_sc, label, dist, angle_deg,
                        res.segid, res.resid, res.resname, lit))

    # Protein donating to psilocin O (hydroxyl acceptor)
    a_pos = psi_acceptor.positions[0]
    for (don_ag, h_ag, is_bb, res, lit) in protein_donors:
        d_pos = don_ag.positions[0]
        dist = np.linalg.norm(d_pos - a_pos)
        if dist < DA_CUTOFF:
            h_pos = h_ag.positions[0]
            angle_rad = calc_angles(d_pos, h_pos, a_pos)
            angle_deg = np.degrees(float(angle_rad))
            if angle_deg > DHA_ANGLE_CUTOFF:
                bb_sc = 'BB' if is_bb else 'SC'
                label = (f"O ← {res.resname}{lit}:"
                         f"{don_ag.atoms[0].name}-{h_ag.atoms[0].name}")
                hbond_records.append((
                    fi, 'hydroxyl', bb_sc, label, dist, angle_deg,
                    res.segid, res.resid, res.resname, lit))

    if (fi + 1) % 20 == 0:
        print(f"  frame {fi + 1}/{n_frames}: {sum(1 for r in hbond_records if r[0] == fi)} H-bonds")

print(f"\nTotal H-bond observations: {len(hbond_records)}")

# ── Aggregate by bond type ───────────────────────────────────

bond_type_frames = defaultdict(set)
bond_type_dists  = defaultdict(list)
bond_type_angles = defaultdict(list)
bond_type_info   = {}

for (fi, group, bb_sc, label, dist, angle, seg, rid, rn, lit) in hbond_records:
    key = (group, bb_sc, label)
    bond_type_frames[key].add(fi)
    bond_type_dists[key].append(dist)
    bond_type_angles[key].append(angle)
    bond_type_info[key] = {
        'psi_group': group, 'partner_type': bb_sc,
        'partner_resname': rn, 'partner_lit': lit,
        'partner_segid': seg, 'partner_resid': rid,
    }

bond_types_sorted = []
for key, frames in bond_type_frames.items():
    occ = len(frames) / n_frames
    bond_types_sorted.append((key, occ, frames))

bond_types_sorted.sort(key=lambda x: (
    ['amine', 'indole NH', 'hydroxyl'].index(x[0][0])
    if x[0][0] in ['amine', 'indole NH', 'hydroxyl'] else 3,
    -x[1],
))

print(f"\nUnique H-bond types: {len(bond_types_sorted)}")
print(f"\n{'Group':<12} {'Type':<4} {'Label':<45} {'Occ':>5} "
      f"{'Dist':>6} {'Angle':>6}")
print('-' * 82)
for key, occ, frames in bond_types_sorted:
    grp, ptype, label = key
    md = np.mean(bond_type_dists[key])
    ma = np.mean(bond_type_angles[key])
    print(f"{grp:<12} {ptype:<4} {label:<45} {occ:5.0%} {md:6.2f} {ma:6.1f}")

# ── Per-frame counts by functional group ─────────────────────

group_counts = {g: np.zeros(n_frames, dtype=int)
                for g in ['amine', 'hydroxyl', 'indole NH']}
total_count = np.zeros(n_frames, dtype=int)

for (fi, group, *_) in hbond_records:
    if group in group_counts:
        group_counts[group][fi] += 1
    total_count[fi] += 1

print(f"\nH-bonds per frame: {total_count.mean():.1f} +/- {total_count.std():.1f} "
      f"(range {total_count.min()}-{total_count.max()})")
for grp in ['amine', 'hydroxyl', 'indole NH']:
    c = group_counts[grp]
    print(f"  {grp:<12}: {c.mean():.1f} +/- {c.std():.1f} "
          f"(range {c.min()}-{c.max()})")

# ── Per-residue backbone vs side-chain occupancy ─────────────

residue_bb_frames = defaultdict(set)
residue_sc_frames = defaultdict(set)
residue_groups    = defaultdict(set)

for key, occ, frames in bond_types_sorted:
    grp, ptype, label = key
    info = bond_type_info[key]
    res_key = (info['partner_segid'], info['partner_resid'],
               info['partner_resname'], info['partner_lit'])
    if ptype == 'BB':
        residue_bb_frames[res_key].update(frames)
    else:
        residue_sc_frames[res_key].update(frames)
    residue_groups[res_key].add(grp)

all_residues = sorted(
    set(list(residue_bb_frames.keys()) + list(residue_sc_frames.keys())),
    key=lambda r: r[3],
)

print(f"\n{'Residue':<12} {'BB occ':>7} {'SC occ':>7} {'Groups'}")
print('-' * 55)
residue_rows = []
for res_key in all_residues:
    seg, rid, rn, lit = res_key
    bb_occ = len(residue_bb_frames.get(res_key, set())) / n_frames
    sc_occ = len(residue_sc_frames.get(res_key, set())) / n_frames
    grps = ', '.join(sorted(residue_groups[res_key]))
    print(f"{rn}{lit:<8} {bb_occ:7.0%} {sc_occ:7.0%}   {grps}")
    residue_rows.append({
        'resname': rn, 'lit_resid': lit, 'segid': seg, 'resid': rid,
        'bb_occupancy': round(bb_occ, 3), 'sc_occupancy': round(sc_occ, 3),
        'psi_groups': grps,
    })

# ── CSV ──────────────────────────────────────────────────────

pd.DataFrame(residue_rows).to_csv(f'{OUT}/hbond_detail_residues.csv', index=False)
print(f"\nCSV saved: {OUT}/hbond_detail_residues.csv")

detail_rows = []
for key, occ, frames in bond_types_sorted:
    grp, ptype, label = key
    info = bond_type_info[key]
    detail_rows.append({
        'psi_group': grp, 'partner_type': ptype, 'label': label,
        'occupancy': round(occ, 3),
        'mean_distance': round(np.mean(bond_type_dists[key]), 2),
        'mean_angle': round(np.mean(bond_type_angles[key]), 1),
        'partner_resname': info['partner_resname'],
        'partner_lit_resid': info['partner_lit'],
    })
pd.DataFrame(detail_rows).to_csv(f'{OUT}/hbond_detail_bonds.csv', index=False)
print(f"CSV saved: {OUT}/hbond_detail_bonds.csv")

ts_df = pd.DataFrame({
    'frame': np.arange(n_frames), 'time_ns': times_ns,
    'total_hbonds': total_count,
    'amine_hbonds': group_counts['amine'],
    'hydroxyl_hbonds': group_counts['hydroxyl'],
    'indole_nh_hbonds': group_counts['indole NH'],
})
ts_df.to_csv(f'{OUT}/hbond_detail_timeseries.csv', index=False)
print(f"CSV saved: {OUT}/hbond_detail_timeseries.csv")

# ── Plot 1: H-bond existence map ────────────────────────────

n_bonds = len(bond_types_sorted)

if n_bonds > 0:
    row_labels = []
    row_groups = []
    existence  = np.zeros((n_bonds, n_frames), dtype=int)

    for i, (key, occ, frames) in enumerate(bond_types_sorted):
        grp, ptype, label = key
        for f in frames:
            existence[i, f] = 1
        row_labels.append(f"{label}  [{ptype}]  ({occ:.0%})")
        row_groups.append(grp)

    fig_height = max(4, n_bonds * 0.38 + 1.5)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    rgba = np.zeros((n_bonds, n_frames, 4))
    for i in range(n_bonds):
        grp = row_groups[i]
        r, g, b = mcolors.to_rgb(GROUP_COLORS.get(grp, '#999999'))
        for f in range(n_frames):
            if existence[i, f]:
                rgba[i, f] = [r, g, b, 0.9]
            else:
                rgba[i, f] = [0.95, 0.95, 0.95, 1.0]

    ax.imshow(rgba, aspect='auto', interpolation='none',
              extent=[0, times_ns[-1], n_bonds - 0.5, -0.5])

    ax.set_yticks(range(n_bonds))
    ax.set_yticklabels(row_labels, fontsize=7, fontfamily='monospace')
    ax.set_xlabel('Time (ns)')
    ax.set_title('Psilocin hydrogen bonds: formation and breaking')

    prev_grp = row_groups[0]
    for i, grp in enumerate(row_groups):
        if grp != prev_grp:
            ax.axhline(y=i - 0.5, color='black', linewidth=0.8)
            prev_grp = grp

    from matplotlib.patches import Patch
    legend_handles = [Patch(facecolor=c, label=g)
                      for g, c in GROUP_COLORS.items()]
    ax.legend(handles=legend_handles, loc='upper right', fontsize=7,
              framealpha=0.9)

    fig.tight_layout()
    fig.savefig(f'{OUT}/hbond_existence_map.png', dpi=150)
    plt.close()
    print(f"Plot saved: {OUT}/hbond_existence_map.png")

# ── Plot 2: functional group time series ─────────────────────

fig, ax = plt.subplots(figsize=(8, 4))

for grp in ['amine', 'hydroxyl', 'indole NH']:
    c = group_counts[grp]
    ax.plot(times_ns, c, color=GROUP_COLORS[grp], linewidth=0.9,
            label=f'{grp} ({c.mean():.1f}/frame)')

ax.set_xlabel('Time (ns)')
ax.set_ylabel('H-bonds per frame')
ax.set_title('Psilocin H-bonds by functional group')
ax.legend(loc='upper right', fontsize=8)
fig.tight_layout()
fig.savefig(f'{OUT}/hbond_by_group.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/hbond_by_group.png")

# ── Plot 3: per-residue backbone vs side-chain ──────────────

if residue_rows:
    res_df = pd.DataFrame(residue_rows).sort_values('lit_resid')
    labels = [f"{r['resname']}{r['lit_resid']}" for _, r in res_df.iterrows()]
    y_pos = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(7, max(4, len(labels) * 0.4)))

    ax.barh(y_pos, res_df['sc_occupancy'].values, height=0.7,
            color='#2c7bb6', label='Side-chain', edgecolor='white',
            linewidth=0.5)
    ax.barh(y_pos, res_df['bb_occupancy'].values, height=0.7,
            left=res_df['sc_occupancy'].values,
            color='#abd9e9', label='Backbone', edgecolor='white',
            linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel('H-bond occupancy (fraction of frames)')
    ax.set_title('Per-residue H-bond occupancy (backbone vs side-chain)')
    ax.legend(loc='lower right', fontsize=8)
    ax.invert_yaxis()

    for i, (_, r) in enumerate(res_df.iterrows()):
        total = r['bb_occupancy'] + r['sc_occupancy']
        if total > 0:
            ax.text(total + 0.02, i, f"{r['psi_groups']}", va='center',
                    fontsize=6.5, color='#555555')

    fig.tight_layout()
    fig.savefig(f'{OUT}/hbond_residue_detail.png', dpi=150)
    plt.close()
    print(f"Plot saved: {OUT}/hbond_residue_detail.png")
