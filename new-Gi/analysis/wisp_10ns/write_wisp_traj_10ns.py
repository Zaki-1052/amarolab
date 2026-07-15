# new-Gi/analysis/wisp_10ns/write_wisp_traj_10ns.py
import MDAnalysis as mda
import numpy as np

BASE = "/Users/zakiralibhai/Documents/VS_Code/amarolab/new-Gi/charmm-gui-8313215931/openmm"
PSF  = f"{BASE}/step5_input.psf"
DCDS = [f"{BASE}/step7_{i}.dcd" for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)

u.add_TopologyAttr('chainIDs', values=np.full(u.atoms.n_atoms, ''))

chain_map = {
    "PROE": "R",  # 5-HT2A receptor (before ICL3)
    "PROF": "R",  # 5-HT2A receptor (after ICL3)
    "PROC": "A",  # Gai1 N-terminal fragment
    "PROD": "A",  # Gai1 C-terminal fragment
    "PROA": "B",  # Gb1
    "PROB": "G",  # Gg2
    "HETA": "L",  # psilocin
}
for segid, cid in chain_map.items():
    seg = u.select_atoms(f"segid {segid}")
    seg.chainIDs = np.full(seg.n_atoms, cid)

sel = u.select_atoms("segid PROE PROF PROC PROD PROA PROB HETA")
print(f"Selected {sel.n_atoms} atoms, {sel.n_residues} residues")
print(f"Frames: {len(u.trajectory)}")

with mda.Writer("traj_complex.pdb", sel.n_atoms) as W:
    for i, ts in enumerate(u.trajectory):
        W.write(sel)
        if (i + 1) % 10 == 0:
            print(f"  wrote frame {i + 1}/{len(u.trajectory)}")

print("Done: traj_complex.pdb")
