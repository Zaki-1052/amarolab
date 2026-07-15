# analysis/phase7_summary/p7b_membrane_padding.py
#
# Check that the protein has >= 15 A clearance to its periodic
# images and does not protrude beyond the lipid headgroups.
from pathlib import Path
import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)
n_frames = len(u.trajectory)
times_ns = np.arange(n_frames) * 0.1

PROTEIN_SEL = "segid PROA PROB PROC PROD PROE PROF PROG PROH PROI PROJ"
PHOSPHORUS_SEL = ("name P and not segid PROA PROB PROC PROD PROE PROF "
                  "PROG PROH PROI PROJ HETA")

THRESHOLD = 15.0

protein = u.select_atoms(PROTEIN_SEL)
phosphorus = u.select_atoms(PHOSPHORUS_SEL)

print(f"Protein: {len(protein)} atoms")
print(f"Phosphorus atoms (membrane): {len(phosphorus)}")

rows = []

for fi, ts in enumerate(u.trajectory):
    box = ts.dimensions[:3]
    pos = protein.positions

    prot_min = pos.min(axis=0)
    prot_max = pos.max(axis=0)
    prot_extent = prot_max - prot_min

    clearance = box - prot_extent

    p_pos = phosphorus.positions
    p_z = p_pos[:, 2]
    p_z_median = np.median(p_z)
    upper_p = p_z[p_z > p_z_median]
    lower_p = p_z[p_z <= p_z_median]
    membrane_top = upper_p.mean() if len(upper_p) > 0 else np.nan
    membrane_bot = lower_p.mean() if len(lower_p) > 0 else np.nan

    rows.append({
        'frame': fi,
        'time_ns': times_ns[fi],
        'box_x': round(box[0], 2),
        'box_y': round(box[1], 2),
        'box_z': round(box[2], 2),
        'prot_xmin': round(prot_min[0], 2),
        'prot_xmax': round(prot_max[0], 2),
        'prot_ymin': round(prot_min[1], 2),
        'prot_ymax': round(prot_max[1], 2),
        'prot_zmin': round(prot_min[2], 2),
        'prot_zmax': round(prot_max[2], 2),
        'extent_x': round(prot_extent[0], 2),
        'extent_y': round(prot_extent[1], 2),
        'extent_z': round(prot_extent[2], 2),
        'clearance_x': round(clearance[0], 2),
        'clearance_y': round(clearance[1], 2),
        'clearance_z': round(clearance[2], 2),
        'min_clearance': round(clearance.min(), 2),
        'membrane_top_z': round(membrane_top, 2),
        'membrane_bot_z': round(membrane_bot, 2),
    })

    if (fi + 1) % 20 == 0:
        print(f"  frame {fi + 1}/{n_frames}")

df = pd.DataFrame(rows)
df.to_csv(f'{OUT}/membrane_padding.csv', index=False)
print(f"\nCSV saved: {OUT}/membrane_padding.csv")

# ── Summary ──────────────────────────────────────────────────

print(f"\n{'Dimension':<6} {'Mean clearance':>14} {'Min clearance':>14} {'Pass':>5}")
print('-' * 44)
all_pass = True
for dim in ['x', 'y', 'z']:
    col = f'clearance_{dim}'
    mean_c = df[col].mean()
    min_c = df[col].min()
    ok = min_c >= THRESHOLD
    if not ok:
        all_pass = False
    print(f"{dim.upper():<6} {mean_c:14.1f} {min_c:14.1f} {'YES' if ok else 'NO':>5}")

print(f"\nProtein Z range: {df['prot_zmin'].min():.1f} to {df['prot_zmax'].max():.1f}")
mem_bot = pd.to_numeric(df['membrane_bot_z'], errors='coerce').mean()
mem_top = pd.to_numeric(df['membrane_top_z'], errors='coerce').mean()
print(f"Membrane Z (phosphorus means): bottom = {mem_bot:.1f}, top = {mem_top:.1f}")
print(f"\nOverall: {'PASS — all frames >= {:.0f} A'.format(THRESHOLD)}"
      if all_pass else
      f"\nOverall: FAIL — some frames below {THRESHOLD} A threshold")

# ── Plot ─────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 4))

for dim, color in [('x', '#2c7bb6'), ('y', '#d7191c'), ('z', '#1a9641')]:
    ax.plot(df['time_ns'], df[f'clearance_{dim}'],
            color=color, linewidth=1.0, label=f'{dim.upper()} clearance')

ax.axhline(y=THRESHOLD, color='black', linestyle='--', linewidth=1.0,
           label=f'{THRESHOLD:.0f} Å threshold')
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Clearance to periodic image (Å)')
ax.set_title('Membrane padding — protein clearance (Gq)')
ax.legend(loc='best', fontsize=8)
fig.tight_layout()
fig.savefig(f'{OUT}/membrane_padding.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/membrane_padding.png")
