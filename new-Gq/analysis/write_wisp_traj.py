# new-Gq/analysis/write_wisp_traj.py
import MDAnalysis as mda
import numpy as np

BASE = "/Users/zakiralibhai/Documents/VS_Code/amarolab/openmm"
PSF  = f"{BASE}/step5_input.psf"
DCDS = [f"{BASE}/step7_{i}.dcd" for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)

u.add_TopologyAttr('chainIDs', values=np.full(u.atoms.n_atoms, ''))

chain_map = {
    "PROA": "R",  # 5-HT2A receptor (fragment 1, resids 1-109)
    "PROB": "R",  # 5-HT2A receptor (fragment 2, resids 110-185)
    "PROC": "R",  # 5-HT2A receptor (fragment 3, resids 186-266)
    "PROD": "A",  # mini-Gaq (fragment 1, resids 1-29)
    "PROE": "A",  # mini-Gaq (fragment 2, resids 30-111)
    "PROF": "A",  # mini-Gaq (fragment 3, resids 112-246)
    "PROG": "B",  # Gb1 (main body, resids 1-289)
    "PROH": "B",  # Gb1 (C-terminal, resids 290-338)
    "PROI": "G",  # Gg2 (fragment 1, resids 1-36)
    "PROJ": "G",  # Gg2 (fragment 2, resids 37-71)
    "HETA": "L",  # psilocin
}
for segid, cid in chain_map.items():
    seg = u.select_atoms(f"segid {segid}")
    seg.chainIDs = np.full(seg.n_atoms, cid)

sel = u.select_atoms("segid PROA PROB PROC PROD PROE PROF PROG PROH PROI PROJ HETA")
print(f"Selected {sel.n_atoms} atoms, {sel.n_residues} residues")
print(f"Frames: {len(u.trajectory)}")

with mda.Writer("traj_complex.pdb", sel.n_atoms) as W:
    for i, ts in enumerate(u.trajectory):
        W.write(sel)
        if (i + 1) % 10 == 0:
            print(f"  wrote frame {i + 1}/{len(u.trajectory)}")

print("Done: traj_complex.pdb")
