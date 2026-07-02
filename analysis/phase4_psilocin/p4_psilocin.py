# analysis/phase4_psilocin/p4_psilocin.py
from pathlib import Path
import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSD
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)
times_ns = np.arange(len(u.trajectory)) * 0.1

OFFSETS = {'PROA': 78, 'PROB': 78, 'PROC': 127}

def lit_resid(resid, segid):
    return resid + OFFSETS.get(segid, 0)

# ── Part A: salt bridge distance ──────────────────────────────

psilocin_N = u.select_atoms("segid HETA and name N1")
asp77_OD1  = u.select_atoms("segid PROA and resid 77 and name OD1")
asp77_OD2  = u.select_atoms("segid PROA and resid 77 and name OD2")

assert len(psilocin_N) == 1, f"Expected 1 psilocin N1, got {len(psilocin_N)}"
assert len(asp77_OD1) == 1, f"Expected 1 D77 OD1, got {len(asp77_OD1)}"
assert len(asp77_OD2) == 1, f"Expected 1 D77 OD2, got {len(asp77_OD2)}"
print(f"Selections OK: psilocin N1, D77 OD1, D77 OD2 (1 atom each)")

d_OD1 = np.empty(len(u.trajectory))
d_OD2 = np.empty(len(u.trajectory))

for i, ts in enumerate(u.trajectory):
    d_OD1[i] = np.linalg.norm(psilocin_N.positions[0] - asp77_OD1.positions[0])
    d_OD2[i] = np.linalg.norm(psilocin_N.positions[0] - asp77_OD2.positions[0])

salt_bridge = np.minimum(d_OD1, d_OD2)

print(f"\nSalt bridge (N1 — D77 min distance):")
print(f"  Range:  {salt_bridge.min():.2f} - {salt_bridge.max():.2f} A")
print(f"  Mean:   {salt_bridge.mean():.2f} +/- {salt_bridge.std():.2f} A")
print(f"  Median: {np.median(salt_bridge):.2f} A")

intact   = np.sum(salt_bridge < 3.5)
weakened = np.sum((salt_bridge >= 3.5) & (salt_bridge < 4.5))
marginal = np.sum((salt_bridge >= 4.5) & (salt_bridge < 6.0))
broken   = np.sum(salt_bridge >= 6.0)
n = len(salt_bridge)
print(f"  Intact   (<3.5 A): {intact:3d}/{n} ({intact/n*100:.0f}%)")
print(f"  Weakened (3.5-4.5): {weakened:3d}/{n} ({weakened/n*100:.0f}%)")
print(f"  Marginal (4.5-6.0): {marginal:3d}/{n} ({marginal/n*100:.0f}%)")
print(f"  Broken   (>6.0 A): {broken:3d}/{n} ({broken/n*100:.0f}%)")

# ── Part B: ligand RMSD ──────────────────────────────────────

u.trajectory[0]
pocket_dynamic = u.select_atoms("(segid PROA PROB PROC) and (around 5.0 (segid HETA))")

pocket_resids_by_seg = {}
for res in pocket_dynamic.residues:
    seg = res.segid
    pocket_resids_by_seg.setdefault(seg, []).append(str(res.resid))

pocket_parts = []
for seg, rids in pocket_resids_by_seg.items():
    pocket_parts.append(f"(segid {seg} and resid {' '.join(rids)})")
POCKET_SEL = " or ".join(pocket_parts)

pocket_residues = u.select_atoms(POCKET_SEL).residues
pocket_bb = u.select_atoms(f"({POCKET_SEL}) and backbone")
lig_heavy = u.select_atoms("segid HETA and not (name H*)")

print(f"\nBinding pocket: {len(pocket_residues)} residues, "
      f"{len(pocket_bb)} backbone atoms")
print(f"Ligand heavy atoms: {len(lig_heavy)}")
print(f"\nPocket residues:")
for res in sorted(pocket_residues, key=lambda r: (r.segid, r.resid)):
    print(f"  {res.segid} {res.resname:3s} {res.resid:3d}  "
          f"(lit {res.resname}{lit_resid(res.resid, res.segid)})")

lig_rmsd = RMSD(
    u, u,
    select=f"({POCKET_SEL}) and backbone",
    groupselections=["segid HETA and not (name H*)"],
    ref_frame=0
)
lig_rmsd.run()

pocket_rmsd = lig_rmsd.results.rmsd[:, 2]
ligand_rmsd = lig_rmsd.results.rmsd[:, 3]

print(f"\nLigand RMSD (heavy atoms, pocket-aligned):")
print(f"  Range:  {ligand_rmsd.min():.2f} - {ligand_rmsd.max():.2f} A")
print(f"  Mean:   {ligand_rmsd.mean():.2f} +/- {ligand_rmsd.std():.2f} A")
print(f"  Median: {np.median(ligand_rmsd):.2f} A")

print(f"\nPocket backbone RMSD:")
print(f"  Range:  {pocket_rmsd.min():.2f} - {pocket_rmsd.max():.2f} A")
print(f"  Mean:   {pocket_rmsd.mean():.2f} +/- {pocket_rmsd.std():.2f} A")

# ── CSV ───────────────────────────────────────────────────────

df = pd.DataFrame({
    'frame': np.arange(n),
    'time_ns': times_ns,
    'salt_bridge_min': salt_bridge,
    'n1_od1_dist': d_OD1,
    'n1_od2_dist': d_OD2,
    'ligand_rmsd': ligand_rmsd,
    'pocket_rmsd': pocket_rmsd,
})
df.to_csv(f'{OUT}/psilocin_data.csv', index=False)
print(f"\nCSV saved: {OUT}/psilocin_data.csv")

# ── Plot ──────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

ax1.plot(times_ns, d_OD1, color='#fdae61', linewidth=0.5, alpha=0.5, label='N1-OD1')
ax1.plot(times_ns, d_OD2, color='#abd9e9', linewidth=0.5, alpha=0.5, label='N1-OD2')
ax1.plot(times_ns, salt_bridge, color='#d7191c', linewidth=1.0, label='Min (salt bridge)')
ax1.axhline(y=3.5, color='grey', linestyle='--', alpha=0.5, label='3.5 Å cutoff')
ax1.set_ylabel('Distance (Å)')
ax1.set_title('Psilocin N1 — D77 (D155) salt bridge')
ax1.legend(loc='upper right', fontsize=7)

ax2.plot(times_ns, ligand_rmsd, color='#2c7bb6', linewidth=0.8, label='Psilocin heavy atoms')
ax2.plot(times_ns, pocket_rmsd, color='#abd9e9', linewidth=0.6, alpha=0.7,
         label='Pocket backbone')
ax2.set_xlabel('Time (ns)')
ax2.set_ylabel('RMSD (Å)')
ax2.set_title('Ligand RMSD (aligned to binding pocket)')
ax2.legend(loc='upper right', fontsize=7)

fig.tight_layout()
fig.savefig(f'{OUT}/binding_pose.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/binding_pose.png")
