# new-Gi/analysis/phase2_rmsd/p2_rmsd.py
from pathlib import Path
import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSD
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'charmm-gui-8313215931' / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)

RECEPTOR_BB = "segid PROE PROF and backbone"
GPROTEIN_BB = "segid PROA PROB PROC PROD and backbone"

rmsd_receptor = RMSD(u, u, select=RECEPTOR_BB, ref_frame=0)
rmsd_receptor.run()

rmsd_gprotein = RMSD(u, u, select=GPROTEIN_BB, ref_frame=0)
rmsd_gprotein.run()

receptor_data = rmsd_receptor.results.rmsd
gprotein_data = rmsd_gprotein.results.rmsd

times_ns = np.arange(100) * 0.1

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(times_ns, receptor_data[:, 2], label='Receptor (PROE-PROF)', color='#2c7bb6')
ax.plot(times_ns, gprotein_data[:, 2], label='G protein (PROA-PROD)', color='#d7191c', alpha=0.8)
ax.set_xlabel('Time (ns)')
ax.set_ylabel('RMSD (Å)')
ax.legend()
fig.tight_layout()
fig.savefig(f'{OUT}/rmsd_time_series.png', dpi=150)
plt.close()

df = pd.DataFrame({
    'frame': np.arange(100),
    'time_ns': times_ns,
    'receptor_rmsd': receptor_data[:, 2],
    'gprotein_rmsd': gprotein_data[:, 2],
})
df.to_csv(f'{OUT}/rmsd_data.csv', index=False)

print(f"Receptor RMSD: {receptor_data[:, 2].min():.2f} - {receptor_data[:, 2].max():.2f} A")
print(f"G protein RMSD: {gprotein_data[:, 2].min():.2f} - {gprotein_data[:, 2].max():.2f} A")
print(f"Saved to {OUT}/")
