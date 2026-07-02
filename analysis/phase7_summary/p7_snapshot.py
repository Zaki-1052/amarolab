# analysis/phase7_summary/p7_snapshot.py
from pathlib import Path
import MDAnalysis as mda
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

RMSD_CSV = str(ROOT / 'analysis' / 'phase2_rmsd' / 'rmsd_data.csv')

GLPA = " ".join([f"GLPA{i}" for i in range(1, 25)])

RECEPTOR     = "segid PROA PROB PROC"
LIGAND       = "segid HETA"
MEMBRANE     = f"segid MEMB or segid {GLPA}"

# ── Find representative frame ────────────────────────────────

rmsd = pd.read_csv(RMSD_CSV)
mean_rmsd = rmsd['receptor_rmsd'].mean()
best_frame = int(rmsd.iloc[(rmsd['receptor_rmsd'] - mean_rmsd).abs().argsort().iloc[0]]['frame'])
best_rmsd  = rmsd.loc[rmsd['frame'] == best_frame, 'receptor_rmsd'].values[0]

print(f"Receptor RMSD: mean = {mean_rmsd:.3f} A")
print(f"Representative frame: {best_frame} (RMSD = {best_rmsd:.3f} A, time = {best_frame * 0.1:.1f} ns)")

# ── Load trajectory ──────────────────────────────────────────

u = mda.Universe(PSF, DCDS)
print(f"Loaded: {len(u.atoms)} atoms, {len(u.trajectory)} frames")

u.trajectory[best_frame]
print(f"Positioned at frame {best_frame}, box: "
      f"{u.dimensions[0]:.1f} x {u.dimensions[1]:.1f} x {u.dimensions[2]:.1f} A")

# ── Select components ────────────────────────────────────────

receptor     = u.select_atoms(RECEPTOR)
ligand       = u.select_atoms(LIGAND)
membrane     = u.select_atoms(MEMBRANE)
rec_lig      = u.select_atoms(f"{RECEPTOR} or {LIGAND}")
rec_lig_memb = u.select_atoms(f"{RECEPTOR} or {LIGAND} or {MEMBRANE}")

print(f"\nSelections:")
print(f"  Receptor:              {len(receptor):>6} atoms, {receptor.n_residues} residues")
print(f"  Ligand:                {len(ligand):>6} atoms")
print(f"  Membrane:              {len(membrane):>6} atoms, {membrane.n_residues} residues")
print(f"  Receptor + ligand:     {len(rec_lig):>6} atoms")
print(f"  Receptor + lig + memb: {len(rec_lig_memb):>6} atoms")

# ── Write PDBs ───────────────────────────────────────────────

f1 = f'{OUT}/5ht2ar_membrane_snapshot.pdb'
rec_lig_memb.write(f1)
print(f"\nWrote: {f1}")
print(f"  Receptor + psilocin + 585 lipids (no water, no ions, no G protein)")

f2 = f'{OUT}/5ht2ar_receptor_snapshot.pdb'
receptor.write(f2)
print(f"Wrote: {f2}")
print(f"  Receptor only (3 segments, 266 residues)")

f3 = f'{OUT}/5ht2ar_receptor_psilocin.pdb'
rec_lig.write(f3)
print(f"Wrote: {f3}")
print(f"  Receptor + psilocin (for binding pose figures)")

# ── Verify ───────────────────────────────────────────────────

for path, expected_label in [(f1, 'membrane'), (f2, 'receptor'), (f3, 'rec+lig')]:
    check = mda.Universe(path)
    print(f"\nVerify {expected_label}: {len(check.atoms)} atoms, "
          f"{check.atoms.n_residues} residues, "
          f"{len(set(check.atoms.segids))} segments")

print(f"\nFrame {best_frame} ({best_frame * 0.1:.1f} ns) — representative of the 10 ns trajectory.")
