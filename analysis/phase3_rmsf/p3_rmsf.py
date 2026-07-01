# p3_rmsf.py
import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import RMSF
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

BASE = '/Users/zakiralibhai/Documents/School/biochemcore/charmm-gui-8190629385/openmm'
OUT  = '/Users/zakiralibhai/Documents/School/biochemcore/charmm-gui-8190629385/analysis/phase3_rmsf'

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

REGIONS = [
    ('TM1',    1,  21),
    ('ICL1',  22,  30),
    ('TM2',   31,  59),
    ('ECL1',  60,  71),
    ('TM3',   72, 100),
    ('ICL2', 101, 111),
    ('TM4',  112, 139),
    ('ECL2', 140, 159),
    ('TM5',  160, 185),
    ('ICL3c', 186, 191),
    ('TM6',  192, 221),
    ('ECL3', 222, 231),
    ('TM7',  232, 251),
    ('H8',   252, 264),
    ('Ct',   265, 266),
]

def assign_region(resid):
    for name, start, end in REGIONS:
        if start <= resid <= end:
            return name
    return 'other'

u = mda.Universe(PSF, DCDS)

receptor_ca = u.select_atoms("segid PROA PROB PROC and name CA")
print(f"Receptor CA atoms: {len(receptor_ca)}")

align.AlignTraj(
    u, u,
    select="segid PROA PROB PROC and backbone",
    ref_frame=0,
    in_memory=True,
).run()
print("Trajectory aligned to frame 0 (in memory)")

rmsf_calc = RMSF(receptor_ca).run()
resids = receptor_ca.resids
rmsf_values = rmsf_calc.results.rmsf
segids = receptor_ca.segids
resnames = receptor_ca.resnames

diffs = np.diff(resids)
gaps = np.where(diffs > 1)[0]
if len(gaps) > 0:
    print("Residue numbering gaps:")
    for g in gaps:
        print(f"  After resid {resids[g]} ({segids[g]}) -> {resids[g+1]} ({segids[g+1]})")
else:
    print("No gaps in residue numbering")

regions = [assign_region(r) for r in resids]

print(f"\nReceptor RMSF: {rmsf_values.min():.2f} - {rmsf_values.max():.2f} A")
print(f"Mean RMSF: {rmsf_values.mean():.2f} A")
print(f"Median RMSF: {np.median(rmsf_values):.2f} A")
print(f"\nPer-region summary:")

seen = []
for rn in regions:
    if rn not in seen:
        seen.append(rn)
for rn in seen:
    mask = np.array([r == rn for r in regions])
    vals = rmsf_values[mask]
    ids = resids[mask]
    print(f"  {rn:5s} (resid {ids[0]:3d}-{ids[-1]:3d}): "
          f"mean {vals.mean():.2f} +/- {vals.std():.2f} A, "
          f"range {vals.min():.2f}-{vals.max():.2f}, n={len(vals)}")

fig, ax = plt.subplots(figsize=(12, 4))

tm_regions = [(n, s, e) for n, s, e in REGIONS if n.startswith('TM')]
for name, start, end in tm_regions:
    ax.axvspan(start - 0.5, end + 0.5, alpha=0.08, color='#2c7bb6')

ax.plot(resids, rmsf_values, color='#2c7bb6', linewidth=0.8)

for boundary in [109.5, 185.5]:
    ax.axvline(x=boundary, color='red', linestyle=':', alpha=0.5,
               label='Segment boundary' if boundary == 109.5 else '')

ax.axhline(y=2.0, color='grey', linestyle='--', alpha=0.5, label='2.0 Å')

ymax = ax.get_ylim()[1]
for name, start, end in REGIONS:
    ax.text((start + end) / 2, ymax * 0.92, name,
            ha='center', va='top', fontsize=6, color='#555555')

ax.set_xlabel('Residue number (current numbering)')
ax.set_ylabel('RMSF (Å)')
ax.set_xlim(resids[0] - 2, resids[-1] + 2)
ax.legend(loc='upper right', fontsize=8)
fig.tight_layout()
fig.savefig(f'{OUT}/rmsf_profile.png', dpi=150)
plt.close()
print(f"\nPlot saved: {OUT}/rmsf_profile.png")

lit_resids = []
for r, s in zip(resids, segids):
    if s in ('PROA', 'PROB'):
        lit_resids.append(r + 78)
    else:
        lit_resids.append(r + 127)

df = pd.DataFrame({
    'resid': resids,
    'lit_resid': lit_resids,
    'resname': resnames,
    'segid': segids,
    'region': regions,
    'rmsf': rmsf_values,
})
df.to_csv(f'{OUT}/rmsf_data.csv', index=False)
print(f"CSV saved: {OUT}/rmsf_data.csv")

receptor_all = u.select_atoms("segid PROA PROB PROC")
u.add_TopologyAttr('tempfactors')
rmsf_by_resid = dict(zip(resids.astype(int), rmsf_values))
new_bfactors = np.array([rmsf_by_resid.get(int(a.resid), 0.0) for a in receptor_all])
receptor_all.tempfactors = new_bfactors
u.trajectory[0]
receptor_all.write(f'{OUT}/receptor_rmsf_bfactor.pdb')
print(f"B-factor PDB saved: {OUT}/receptor_rmsf_bfactor.pdb")

top5 = np.argsort(rmsf_values)[-5:][::-1]
print(f"\nTop 5 most flexible residues:")
for i in top5:
    print(f"  resid {resids[i]} ({resnames[i]}, {segids[i]}, {regions[i]}): {rmsf_values[i]:.2f} A")

bot5 = np.argsort(rmsf_values)[:5]
print(f"Top 5 most rigid residues:")
for i in bot5:
    print(f"  resid {resids[i]} ({resnames[i]}, {segids[i]}, {regions[i]}): {rmsf_values[i]:.2f} A")
