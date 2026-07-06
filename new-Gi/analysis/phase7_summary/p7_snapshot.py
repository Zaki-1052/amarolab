# new-Gi/analysis/phase7_summary/p7_snapshot.py
from pathlib import Path
import MDAnalysis as mda
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'charmm-gui-8313215931' / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)

# ── Find representative frame from phase 2 RMSD data ────────

rmsd_csv = Path(__file__).resolve().parent.parent / 'phase2_rmsd' / 'rmsd_data.csv'
rmsd_df = pd.read_csv(rmsd_csv)

mean_rmsd = rmsd_df['receptor_rmsd'].mean()
closest_idx = (rmsd_df['receptor_rmsd'] - mean_rmsd).abs().idxmin()
rep_frame = int(rmsd_df.loc[closest_idx, 'frame'])
rep_time = rmsd_df.loc[closest_idx, 'time_ns']
rep_rmsd = rmsd_df.loc[closest_idx, 'receptor_rmsd']

print(f"Mean receptor RMSD: {mean_rmsd:.2f} A")
print(f"Representative frame: {rep_frame} (t = {rep_time:.1f} ns, RMSD = {rep_rmsd:.2f} A)")

u.trajectory[rep_frame]

# ── Snapshot 1: membrane + receptor + ligand ─────────────────

glpa_segs = " ".join([f"GLPA{i}" for i in range(1, 25)])
membrane_receptor = u.select_atoms(
    f"segid PROE PROF HETA MEMB {glpa_segs}")
membrane_receptor.write(f'{OUT}/5ht2ar_Gi_membrane_snapshot.pdb')
print(f"Snapshot 1: {OUT}/5ht2ar_Gi_membrane_snapshot.pdb "
      f"({len(membrane_receptor)} atoms)")

# ── Snapshot 2: receptor only ────────────────────────────────

receptor_only = u.select_atoms("segid PROE PROF")
receptor_only.write(f'{OUT}/5ht2ar_Gi_receptor_snapshot.pdb')
print(f"Snapshot 2: {OUT}/5ht2ar_Gi_receptor_snapshot.pdb "
      f"({len(receptor_only)} atoms)")

# ── Snapshot 3: receptor + psilocin ──────────────────────────

receptor_lig = u.select_atoms("segid PROE PROF HETA")
receptor_lig.write(f'{OUT}/5ht2ar_Gi_receptor_psilocin.pdb')
print(f"Snapshot 3: {OUT}/5ht2ar_Gi_receptor_psilocin.pdb "
      f"({len(receptor_lig)} atoms)")
