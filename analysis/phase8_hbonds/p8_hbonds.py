# analysis/phase8_hbonds/p8_hbonds.py
from pathlib import Path
import MDAnalysis as mda
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
from MDAnalysis.lib.distances import calc_angles
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)
n_frames = len(u.trajectory)
times_ns = np.arange(n_frames) * 0.1

OFFSETS = {'PROA': 78, 'PROB': 78, 'PROC': 127}

def lit_resid(resid, segid):
    return resid + OFFSETS.get(segid, 0)

# ── Build pocket selection (same as phase 4) ─────────────────

u.trajectory[0]
pocket_dynamic = u.select_atoms(
    "(segid PROA PROB PROC) and (around 5.0 (segid HETA))")

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
for res in sorted(pocket_residues, key=lambda r: (r.segid, r.resid)):
    print(f"  {res.segid} {res.resname:3s} {res.resid:3d}  "
          f"(lit {res.resname}{lit_resid(res.resid, res.segid)})")

# ── Part A: direct psilocin-pocket H-bonds ───────────────────

COMBINED_SEL = f"segid HETA or ({POCKET_SEL})"

hba = HydrogenBondAnalysis(
    u,
    donors_sel=COMBINED_SEL,
    hydrogens_sel=COMBINED_SEL,
    acceptors_sel=COMBINED_SEL,
    between=[["segid HETA", POCKET_SEL]],
    d_a_cutoff=3.5,
    d_h_a_angle_cutoff=130,
    update_selections=False,
)

print("\nRunning direct H-bond analysis...")
hba.run()

hbonds = hba.results.hbonds
print(f"Raw H-bond results shape: {hbonds.shape}")

if hbonds.ndim == 2 and hbonds.shape[0] > 0:
    if hbonds.shape[1] == 6:
        hb_frame   = hbonds[:, 0].astype(int)
        hb_donor   = hbonds[:, 1].astype(int)
        hb_hydro   = hbonds[:, 2].astype(int)
        hb_accept  = hbonds[:, 3].astype(int)
        hb_dist    = hbonds[:, 4]
        hb_angle   = hbonds[:, 5]
    else:
        hb_frame   = hbonds[:, 0].astype(int)
        hb_donor   = hbonds[:, 1].astype(int)
        hb_hydro   = hbonds[:, 2].astype(int)
        hb_accept  = hbonds[:, 3].astype(int)
        hb_dist    = hbonds[:, 4] if hbonds.shape[1] > 4 else np.zeros(len(hb_frame))
        hb_angle   = hbonds[:, 5] if hbonds.shape[1] > 5 else np.zeros(len(hb_frame))
    n_total_hbonds = len(hb_frame)
else:
    hb_frame = np.array([], dtype=int)
    n_total_hbonds = 0

print(f"Total H-bond observations across trajectory: {n_total_hbonds}")

direct_count = np.zeros(n_frames, dtype=int)
for f in hb_frame:
    if 0 <= f < n_frames:
        direct_count[f] += 1

print(f"Direct H-bonds per frame: {direct_count.mean():.1f} +/- {direct_count.std():.1f} "
      f"(range {direct_count.min()}-{direct_count.max()})")

# ── Per-residue H-bond occupancy ─────────────────────────────

residue_hbond_frames = defaultdict(set)
residue_dists = defaultdict(list)
residue_angles = defaultdict(list)

for i in range(n_total_hbonds):
    frame = hb_frame[i]
    d_idx = hb_donor[i]
    a_idx = hb_accept[i]

    d_atom = u.atoms[d_idx]
    a_atom = u.atoms[a_idx]

    if d_atom.segid == 'HETA':
        partner = a_atom
    elif a_atom.segid == 'HETA':
        partner = d_atom
    else:
        continue

    key = (partner.segid, partner.resid, partner.resname)
    residue_hbond_frames[key].add(frame)
    residue_dists[key].append(hb_dist[i])
    residue_angles[key].append(hb_angle[i])

print(f"\nPer-residue H-bond occupancy (direct):")
print(f"{'Residue':<20} {'Occupancy':>10} {'Mean dist':>10} {'Mean angle':>11}")
print('-' * 55)

occ_rows = []
for key in sorted(residue_hbond_frames.keys()):
    seg, rid, rn = key
    occ = len(residue_hbond_frames[key]) / n_frames
    md  = np.mean(residue_dists[key])
    ma  = np.mean(residue_angles[key])
    lit = lit_resid(rid, seg)
    label = f"{rn}{lit}"
    print(f"{label:<20} {occ:10.2f} {md:10.2f} {ma:11.1f}")
    occ_rows.append({
        'resid': rid, 'segid': seg, 'resname': rn,
        'lit_resid': lit, 'occupancy': round(occ, 3),
        'mean_distance': round(md, 2), 'mean_angle': round(ma, 1),
    })

# ── Part B: salt bridge with angle criterion ─────────────────

psilocin_N1 = u.select_atoms("segid HETA and name N1")
psilocin_H17 = u.select_atoms("segid HETA and name H17")
asp77_OD1 = u.select_atoms("segid PROA and resid 77 and name OD1")
asp77_OD2 = u.select_atoms("segid PROA and resid 77 and name OD2")

for name, ag in [('N1', psilocin_N1), ('H17', psilocin_H17),
                 ('OD1', asp77_OD1), ('OD2', asp77_OD2)]:
    assert len(ag) == 1, f"Expected 1 {name}, got {len(ag)}"

sb_dist  = np.empty(n_frames)
sb_angle = np.empty(n_frames)
sb_hbond = np.empty(n_frames, dtype=bool)

for fi, ts in enumerate(u.trajectory):
    d1 = np.linalg.norm(psilocin_N1.positions[0] - asp77_OD1.positions[0])
    d2 = np.linalg.norm(psilocin_N1.positions[0] - asp77_OD2.positions[0])

    if d1 <= d2:
        closer_O = asp77_OD1
        sb_dist[fi] = d1
    else:
        closer_O = asp77_OD2
        sb_dist[fi] = d2

    angle_rad = calc_angles(
        psilocin_N1.positions[0],
        psilocin_H17.positions[0],
        closer_O.positions[0],
    )
    sb_angle[fi] = np.degrees(float(angle_rad))
    sb_hbond[fi] = (sb_dist[fi] < 3.5) and (sb_angle[fi] > 130)

sb_occ = sb_hbond.sum() / n_frames
print(f"\nSalt bridge (N1-H17...D77):")
print(f"  Distance: {sb_dist.mean():.2f} +/- {sb_dist.std():.2f} A")
print(f"  Angle:    {sb_angle.mean():.1f} +/- {sb_angle.std():.1f} deg")
print(f"  H-bond occupancy: {sb_occ:.0%} ({sb_hbond.sum()}/{n_frames} frames)")

# ── Part C: water-mediated H-bonds ───────────────────────────
# Geometric proxy: count water oxygens within 3.5 A of both
# psilocin and a pocket residue in the same frame.

print("\nRunning water-mediated analysis (geometric proxy)...")
lig_heavy = u.select_atoms("segid HETA and not (name H*)")
pocket_heavy = u.select_atoms(f"({POCKET_SEL}) and not (name H*)")

water_mediated_count = np.zeros(n_frames, dtype=int)

for fi, ts in enumerate(u.trajectory):
    waters_near_lig = u.select_atoms(
        "name OH2 and (around 3.5 (segid HETA and not (name H*)))")
    if len(waters_near_lig) == 0:
        continue
    water_resids = set(waters_near_lig.resids)

    waters_near_pocket = u.select_atoms(
        f"name OH2 and (around 3.5 (({POCKET_SEL}) and not (name H*)))")
    bridge_resids = water_resids & set(waters_near_pocket.resids)
    water_mediated_count[fi] = len(bridge_resids)

print(f"Water-mediated bridges per frame: {water_mediated_count.mean():.1f} "
      f"+/- {water_mediated_count.std():.1f} "
      f"(range {water_mediated_count.min()}-{water_mediated_count.max()})")

# ── CSV: time series ─────────────────────────────────────────

ts_df = pd.DataFrame({
    'frame': np.arange(n_frames),
    'time_ns': times_ns,
    'n_direct_hbonds': direct_count,
    'n_water_mediated': water_mediated_count,
    'salt_bridge_dist': sb_dist.round(3),
    'salt_bridge_angle': sb_angle.round(1),
    'salt_bridge_hbond': sb_hbond,
})
ts_df.to_csv(f'{OUT}/hbond_timeseries.csv', index=False)
print(f"\nCSV saved: {OUT}/hbond_timeseries.csv")

# ── CSV: per-residue occupancy ───────────────────────────────

if occ_rows:
    pd.DataFrame(occ_rows).to_csv(f'{OUT}/hbond_occupancy.csv', index=False)
    print(f"CSV saved: {OUT}/hbond_occupancy.csv")
else:
    print("No direct H-bonds found; skipping occupancy CSV")

# ── Plot 1: H-bond time series ───────────────────────────────

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

ax1.plot(times_ns, direct_count, color='#2c7bb6', linewidth=0.8,
         label='Direct H-bonds')
ax1.plot(times_ns, water_mediated_count, color='#fdae61', linewidth=0.8,
         label='Water bridges')
ax1.set_ylabel('Count per frame')
ax1.set_title('Psilocin — pocket hydrogen bonds')
ax1.legend(loc='upper right', fontsize=7)

ax2.plot(times_ns, sb_dist, color='#d7191c', linewidth=0.8, label='Distance')
ax2.axhline(y=3.5, color='grey', linestyle='--', alpha=0.5, linewidth=0.5)
for fi in range(n_frames):
    if sb_hbond[fi]:
        ax2.axvspan(times_ns[fi] - 0.05, times_ns[fi] + 0.05,
                    alpha=0.15, color='#1a9641')
ax2.set_ylabel('N1-D77 distance (Å)')
ax2.set_xlabel('Time (ns)')
ax2.set_title('Salt bridge (green shading = H-bond by angle criterion)')
ax2.legend(loc='upper right', fontsize=7)

fig.tight_layout()
fig.savefig(f'{OUT}/hbond_timeseries.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/hbond_timeseries.png")

# ── Plot 2: per-residue occupancy bar chart ──────────────────

if occ_rows:
    occ_df = pd.DataFrame(occ_rows).sort_values('occupancy', ascending=True)
    fig, ax = plt.subplots(figsize=(7, max(3, len(occ_df) * 0.4)))

    labels = [f"{r['resname']}{r['lit_resid']}" for _, r in occ_df.iterrows()]
    ax.barh(labels, occ_df['occupancy'], color='#2c7bb6', edgecolor='white',
            linewidth=0.5)
    ax.set_xlabel('H-bond occupancy (fraction of frames)')
    ax.set_title('Psilocin H-bond partners')
    ax.set_xlim(0, 1)

    for i, (_, r) in enumerate(occ_df.iterrows()):
        ax.text(r['occupancy'] + 0.02, i, f"{r['occupancy']:.2f}",
                va='center', fontsize=8)

    fig.tight_layout()
    fig.savefig(f'{OUT}/hbond_occupancy.png', dpi=150)
    plt.close()
    print(f"Plot saved: {OUT}/hbond_occupancy.png")
