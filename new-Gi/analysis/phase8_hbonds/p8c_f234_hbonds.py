# new-Gi/analysis/phase8_hbonds/p8c_f234_hbonds.py
#
# H-bond analysis for the F234 neighborhood: all protein-protein
# and protein-psilocin H-bonds within 8 A of F234 heavy atoms.
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
NEIGHBORHOOD_CUTOFF = 8.0

# ── Identify F234 neighborhood at frame 0 ────────────────────

u.trajectory[0]
f234_sel = "segid PROE and resid 155 and not name H*"
f234_atoms = u.select_atoms(f234_sel)
print(f"F234 heavy atoms: {len(f234_atoms)}")

neighborhood = u.select_atoms(
    f"(segid PROE PROF HETA) and around {NEIGHBORHOOD_CUTOFF} ({f234_sel})")
neighborhood_residues = neighborhood.residues

hood_resids_by_seg = {}
for res in neighborhood_residues:
    hood_resids_by_seg.setdefault(res.segid, []).append(str(res.resid))

hood_parts = []
for seg, rids in hood_resids_by_seg.items():
    hood_parts.append(f"(segid {seg} and resid {' '.join(rids)})")
HOOD_SEL = " or ".join(hood_parts)

hood_residues = u.select_atoms(HOOD_SEL).residues
print(f"F234 neighborhood ({NEIGHBORHOOD_CUTOFF} A): {len(hood_residues)} residues")

hood_rows = []
for res in sorted(hood_residues, key=lambda r: (r.segid, r.resid)):
    lit = lit_resid(res.resid, res.segid)
    print(f"  {res.resname}{lit} ({res.segid} {res.resid})")
    hood_rows.append({
        'resname': res.resname, 'lit_resid': lit,
        'segid': res.segid, 'resid': res.resid,
        'is_psilocin': res.segid == 'HETA',
    })

pd.DataFrame(hood_rows).to_csv(f'{OUT}/f234_neighborhood_residues.csv', index=False)
print(f"CSV saved: {OUT}/f234_neighborhood_residues.csv")

# ── Donor/acceptor tables (same as p8b) ─────────────────────

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

# ── Psilocin donors (if psilocin is in the neighborhood) ────

PSI_DONORS = [
    ('N1', 'H17', 'amine'),
    ('N2', 'H13', 'indole NH'),
    ('O',  'H16', 'hydroxyl'),
]

psi_in_hood = any(r.segid == 'HETA' for r in hood_residues)

psi_donor_atoms = {}
psi_acceptor = None
if psi_in_hood:
    for heavy, h, group in PSI_DONORS:
        ag_heavy = u.select_atoms(f"segid HETA and name {heavy}")
        ag_h     = u.select_atoms(f"segid HETA and name {h}")
        if len(ag_heavy) == 1 and len(ag_h) == 1:
            psi_donor_atoms[(heavy, h)] = (ag_heavy, ag_h, group)
    psi_acceptor = u.select_atoms("segid HETA and name O")
    print(f"Psilocin in neighborhood: {len(psi_donor_atoms)} donor groups, "
          f"{len(psi_acceptor)} acceptor atoms")

# ── Enumerate protein donors and acceptors in the hood ───────

donors = []
acceptors = []

for res in sorted(hood_residues, key=lambda r: (r.segid, r.resid)):
    if res.segid == 'HETA':
        continue
    base = f"segid {res.segid} and resid {res.resid}"
    lit = lit_resid(res.resid, res.segid)

    n_atom  = u.select_atoms(f"{base} and name N")
    hn_atom = u.select_atoms(f"{base} and name HN")
    if len(n_atom) == 1 and len(hn_atom) == 1:
        donors.append((n_atom, hn_atom, True, res, lit))

    o_atom = u.select_atoms(f"{base} and name O")
    if len(o_atom) == 1:
        acceptors.append((o_atom, True, res, lit))

    for heavy_name, h_name in SC_DONOR_DEFS.get(res.resname, []):
        ag_heavy = u.select_atoms(f"{base} and name {heavy_name}")
        ag_h     = u.select_atoms(f"{base} and name {h_name}")
        if len(ag_heavy) == 1 and len(ag_h) == 1:
            donors.append((ag_heavy, ag_h, False, res, lit))

    for acc_name in SC_ACCEPTOR_DEFS.get(res.resname, []):
        ag_acc = u.select_atoms(f"{base} and name {acc_name}")
        if len(ag_acc) == 1:
            acceptors.append((ag_acc, False, res, lit))

print(f"Protein donors: {len(donors)} ({sum(1 for d in donors if d[2])} BB, "
      f"{sum(1 for d in donors if not d[2])} SC)")
print(f"Protein acceptors: {len(acceptors)} ({sum(1 for a in acceptors if a[1])} BB, "
      f"{sum(1 for a in acceptors if not a[1])} SC)")

# ── Frame loop ──────────────────────────────────────────────

hbond_records = []

for fi, ts in enumerate(u.trajectory):

    # Protein-protein H-bonds within the neighborhood
    for don_ag, h_ag, don_is_bb, don_res, don_lit in donors:
        d_pos = don_ag.positions[0]
        h_pos = h_ag.positions[0]

        for acc_ag, acc_is_bb, acc_res, acc_lit in acceptors:
            if don_res == acc_res:
                continue
            a_pos = acc_ag.positions[0]
            dist = np.linalg.norm(d_pos - a_pos)
            if dist < DA_CUTOFF:
                angle_rad = calc_angles(d_pos, h_pos, a_pos)
                angle_deg = np.degrees(float(angle_rad))
                if angle_deg > DHA_ANGLE_CUTOFF:
                    d_type = 'BB' if don_is_bb else 'SC'
                    a_type = 'BB' if acc_is_bb else 'SC'
                    label = (f"{don_res.resname}{don_lit}:"
                             f"{don_ag.atoms[0].name}-{h_ag.atoms[0].name} → "
                             f"{acc_res.resname}{acc_lit}:{acc_ag.atoms[0].name}")
                    hbond_records.append((
                        fi, 'protein-protein', f'{d_type}-{a_type}',
                        label, dist, angle_deg))

    # Psilocin-protein H-bonds
    if psi_in_hood:
        for (psi_heavy, psi_h, psi_group) in psi_donor_atoms.values():
            d_pos = psi_heavy.positions[0]
            h_pos = psi_h.positions[0]
            for acc_ag, acc_is_bb, acc_res, acc_lit in acceptors:
                a_pos = acc_ag.positions[0]
                dist = np.linalg.norm(d_pos - a_pos)
                if dist < DA_CUTOFF:
                    angle_rad = calc_angles(d_pos, h_pos, a_pos)
                    angle_deg = np.degrees(float(angle_rad))
                    if angle_deg > DHA_ANGLE_CUTOFF:
                        bb_sc = 'BB' if acc_is_bb else 'SC'
                        label = (f"Psi:{psi_heavy.atoms[0].name}-"
                                 f"{psi_h.atoms[0].name} → "
                                 f"{acc_res.resname}{acc_lit}:{acc_ag.atoms[0].name}")
                        hbond_records.append((
                            fi, f'psilocin-{psi_group}', bb_sc,
                            label, dist, angle_deg))

        if psi_acceptor is not None and len(psi_acceptor) > 0:
            a_pos = psi_acceptor.positions[0]
            for don_ag, h_ag, don_is_bb, don_res, don_lit in donors:
                d_pos = don_ag.positions[0]
                dist = np.linalg.norm(d_pos - a_pos)
                if dist < DA_CUTOFF:
                    h_pos = h_ag.positions[0]
                    angle_rad = calc_angles(d_pos, h_pos, a_pos)
                    angle_deg = np.degrees(float(angle_rad))
                    if angle_deg > DHA_ANGLE_CUTOFF:
                        bb_sc = 'BB' if don_is_bb else 'SC'
                        label = (f"Psi:O ← {don_res.resname}{don_lit}:"
                                 f"{don_ag.atoms[0].name}-{h_ag.atoms[0].name}")
                        hbond_records.append((
                            fi, 'psilocin-hydroxyl', bb_sc,
                            label, dist, angle_deg))

    if (fi + 1) % 20 == 0:
        print(f"  frame {fi + 1}/{n_frames}: "
              f"{sum(1 for r in hbond_records if r[0] == fi)} H-bonds")

print(f"\nTotal H-bond observations: {len(hbond_records)}")

# ── Aggregate by bond type ──────────────────────────────────

bond_frames = defaultdict(set)
bond_dists  = defaultdict(list)
bond_angles = defaultdict(list)
bond_meta   = {}

for (fi, category, bond_type, label, dist, angle) in hbond_records:
    key = (category, bond_type, label)
    bond_frames[key].add(fi)
    bond_dists[key].append(dist)
    bond_angles[key].append(angle)
    bond_meta[key] = category

bond_sorted = []
for key, frames in bond_frames.items():
    occ = len(frames) / n_frames
    bond_sorted.append((key, occ, frames))

bond_sorted.sort(key=lambda x: -x[1])

print(f"\nUnique H-bond types: {len(bond_sorted)}")
print(f"\n{'Category':<20} {'Type':<7} {'Label':<55} {'Occ':>5} "
      f"{'Dist':>6} {'Angle':>6}")
print('-' * 105)
for key, occ, frames in bond_sorted:
    cat, btype, label = key
    md = np.mean(bond_dists[key])
    ma = np.mean(bond_angles[key])
    print(f"{cat:<20} {btype:<7} {label:<55} {occ:5.0%} {md:6.2f} {ma:6.1f}")

# ── Per-frame total count ───────────────────────────────────

total_per_frame = np.zeros(n_frames, dtype=int)
pp_per_frame = np.zeros(n_frames, dtype=int)
psi_per_frame = np.zeros(n_frames, dtype=int)

for (fi, category, *_) in hbond_records:
    total_per_frame[fi] += 1
    if category == 'protein-protein':
        pp_per_frame[fi] += 1
    else:
        psi_per_frame[fi] += 1

print(f"\nH-bonds/frame in F234 neighborhood: "
      f"{total_per_frame.mean():.1f} ± {total_per_frame.std():.1f} "
      f"(range {total_per_frame.min()}-{total_per_frame.max()})")
print(f"  protein-protein: {pp_per_frame.mean():.1f} ± {pp_per_frame.std():.1f}")
print(f"  psilocin: {psi_per_frame.mean():.1f} ± {psi_per_frame.std():.1f}")

# ── CSV: occupancy ──────────────────────────────────────────

occ_rows = []
for key, occ, frames in bond_sorted:
    cat, btype, label = key
    occ_rows.append({
        'category': cat, 'bond_type': btype, 'label': label,
        'occupancy': round(occ, 3),
        'mean_distance': round(np.mean(bond_dists[key]), 2),
        'mean_angle': round(np.mean(bond_angles[key]), 1),
    })

pd.DataFrame(occ_rows).to_csv(f'{OUT}/f234_hbond_occupancy.csv', index=False)
print(f"\nCSV saved: {OUT}/f234_hbond_occupancy.csv")

# ── Plot 1: occupancy histogram ─────────────────────────────

top_n = min(20, len(bond_sorted))
top_bonds = bond_sorted[:top_n]

if top_bonds:
    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.35)))

    labels_plot = []
    occs = []
    colors = []
    for key, occ, frames in top_bonds:
        cat, btype, label = key
        labels_plot.append(f"{label}  ({occ:.0%})")
        occs.append(occ)
        colors.append('#e7298a' if 'psilocin' in cat else '#2c7bb6')

    y_pos = np.arange(len(labels_plot))
    ax.barh(y_pos, occs, color=colors, edgecolor='white', linewidth=0.5,
            height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels_plot, fontsize=7, fontfamily='monospace')
    ax.set_xlabel('Occupancy (fraction of frames)')
    ax.set_title(f'H-bond occupancy — F234 neighborhood ({NEIGHBORHOOD_CUTOFF} Å)')
    ax.invert_yaxis()

    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor='#2c7bb6', label='Protein-protein'),
        Patch(facecolor='#e7298a', label='Psilocin'),
    ], loc='lower right', fontsize=8)

    fig.tight_layout()
    fig.savefig(f'{OUT}/f234_hbond_occupancy_histogram.png', dpi=150)
    plt.close()
    print(f"Plot saved: {OUT}/f234_hbond_occupancy_histogram.png")

# ── Plot 2: existence map (top 15) ──────────────────────────

map_n = min(15, len(bond_sorted))
map_bonds = bond_sorted[:map_n]

if map_bonds:
    existence = np.zeros((map_n, n_frames), dtype=int)
    row_labels = []
    row_cats = []

    for i, (key, occ, frames) in enumerate(map_bonds):
        cat, btype, label = key
        for f in frames:
            existence[i, f] = 1
        row_labels.append(f"{label}  ({occ:.0%})")
        row_cats.append(cat)

    fig_height = max(4, map_n * 0.38 + 1.5)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    rgba = np.zeros((map_n, n_frames, 4))
    for i in range(map_n):
        if 'psilocin' in row_cats[i]:
            r, g, b = mcolors.to_rgb('#e7298a')
        else:
            r, g, b = mcolors.to_rgb('#2c7bb6')
        for f in range(n_frames):
            if existence[i, f]:
                rgba[i, f] = [r, g, b, 0.9]
            else:
                rgba[i, f] = [0.95, 0.95, 0.95, 1.0]

    ax.imshow(rgba, aspect='auto', interpolation='none',
              extent=[0, times_ns[-1], map_n - 0.5, -0.5])
    ax.set_yticks(range(map_n))
    ax.set_yticklabels(row_labels, fontsize=7, fontfamily='monospace')
    ax.set_xlabel('Time (ns)')
    ax.set_title('F234 neighborhood H-bonds: formation and breaking')

    fig.tight_layout()
    fig.savefig(f'{OUT}/f234_hbond_existence_map.png', dpi=150)
    plt.close()
    print(f"Plot saved: {OUT}/f234_hbond_existence_map.png")
