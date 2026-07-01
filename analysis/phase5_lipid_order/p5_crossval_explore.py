# p5_crossval_explore.py
import MDAnalysis as mda
import numpy as np

BASE = '/Users/zakiralibhai/Documents/School/biochemcore/charmm-gui-8190629385/openmm'
PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)

from lipyphilic.analysis.order_parameter import SCC

popc_sn2_names = [f"C2{i}" for i in range(2, 19)]
tail_sel = f"segid MEMB and resname POPC and name {' '.join(popc_sn2_names)}"
print(f"Tail selection: {len(u.select_atoms(tail_sel))} atoms, 17 names, 48 POPC")

scc = SCC(universe=u, tail_sel=tail_sel)
scc.run()

print("\n=== Exploring SCC output ===")
print(f"type(scc.SCC): {type(scc.SCC)}")
print(f"shape: {scc.SCC.shape}")
print(f"dtype: {scc.SCC.dtype}")
print(f"range: {np.nanmin(scc.SCC):.4f} to {np.nanmax(scc.SCC):.4f}")
print(f"NaN count: {np.isnan(scc.SCC).sum()} / {scc.SCC.size}")
print(f"ndim: {scc.SCC.ndim}")

if scc.SCC.ndim >= 2:
    print(f"\nFirst residue, all frames, all values:")
    print(scc.SCC[0])

if hasattr(scc, 'results'):
    rattrs = [a for a in dir(scc.results) if not a.startswith('_')]
    print(f"\nscc.results attributes: {rattrs}")
