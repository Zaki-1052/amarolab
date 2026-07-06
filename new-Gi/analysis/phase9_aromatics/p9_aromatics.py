# new-Gi/analysis/phase9_aromatics/p9_aromatics.py
from pathlib import Path
import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'charmm-gui-8313215931' / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)
n_frames = len(u.trajectory)
times_ns = np.arange(n_frames) * 0.1

OFFSETS = {'PROE': 79, 'PROF': 131}

def lit_resid(resid, segid):
    return resid + OFFSETS.get(segid, 0)

# ── Ring definitions ─────────────────────────────────────────
# All protein residue mappings PSF-verified:
#   W336 -> PROF 205 (TRP)    F339 -> PROF 208 (PHE)
#   F340 -> PROF 209 (PHE)    F234 -> PROE 155 (PHE)
#   F243 -> PROE 164 (PHE)    Y370 -> PROF 239 (TYR)

RINGS = [
    {
        'label': 'W336',
        'sel': 'segid PROF and resid 205 and name CG CD1 NE1 CE2 CD2 CE3 CZ3 CH2 CZ2',
        'n_atoms': 9,
        'color': '#2c7bb6',
    },
    {
        'label': 'F339',
        'sel': 'segid PROF and resid 208 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#d7191c',
    },
    {
        'label': 'F340',
        'sel': 'segid PROF and resid 209 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#fdae61',
    },
    {
        'label': 'F234',
        'sel': 'segid PROE and resid 155 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#abd9e9',
    },
    {
        'label': 'F243',
        'sel': 'segid PROE and resid 164 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#1a9641',
    },
    {
        'label': 'Y370',
        'sel': 'segid PROF and resid 239 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#7570b3',
    },
    {
        'label': 'Psilocin',
        'sel': 'segid HETA and name C2 C3 N2 C4 C5 C10 C6 C11 C12',
        'n_atoms': 9,
        'color': '#e7298a',
    },
]

# ── Pre-select ring atom groups ──────────────────────────────

ring_groups = []
for ring in RINGS:
    ag = u.select_atoms(ring['sel'])
    assert len(ag) == ring['n_atoms'], (
        f"{ring['label']}: expected {ring['n_atoms']} atoms, got {len(ag)}")
    ring_groups.append(ag)
    print(f"{ring['label']}: {len(ag)} ring atoms selected")

# ── Compute ring normals and cumulative rotation ─────────────

def ring_normal(positions):
    centered = positions - positions.mean(axis=0)
    _, _, Vt = np.linalg.svd(centered)
    return Vt[2]

all_normals = np.zeros((len(RINGS), n_frames, 3))
all_deltas  = np.zeros((len(RINGS), n_frames))

for fi, ts in enumerate(u.trajectory):
    for ri, ag in enumerate(ring_groups):
        n = ring_normal(ag.positions)
        if fi > 0 and np.dot(n, all_normals[ri, fi - 1]) < 0:
            n = -n
        all_normals[ri, fi] = n
        if fi > 0:
            cos_theta = np.clip(np.dot(all_normals[ri, fi], all_normals[ri, fi - 1]),
                                -1.0, 1.0)
            all_deltas[ri, fi] = np.degrees(np.arccos(cos_theta))

    if (fi + 1) % 20 == 0:
        print(f"  frame {fi + 1}/{n_frames}")

all_cumulative = np.cumsum(all_deltas, axis=1)
all_rotations  = all_cumulative / 360.0

# ── Summary ──────────────────────────────────────────────────

print(f"\n{'Ring':<12} {'Total (°)':>10} {'Rotations':>10} "
      f"{'Mean Δ (°)':>10} {'Max Δ (°)':>10} {'Std Δ (°)':>10}")
print('-' * 66)

summary_rows = []
for ri, ring in enumerate(RINGS):
    deltas = all_deltas[ri, 1:]
    total_angle = all_cumulative[ri, -1]
    total_rot   = all_rotations[ri, -1]
    mean_d = deltas.mean()
    max_d  = deltas.max()
    std_d  = deltas.std()

    print(f"{ring['label']:<12} {total_angle:10.1f} {total_rot:10.2f} "
          f"{mean_d:10.2f} {max_d:10.2f} {std_d:10.2f}")

    summary_rows.append({
        'ring_label': ring['label'],
        'total_angle_deg': round(total_angle, 1),
        'total_rotations': round(total_rot, 3),
        'mean_delta_deg': round(mean_d, 2),
        'max_delta_deg': round(max_d, 2),
        'std_delta_deg': round(std_d, 2),
    })

# ── CSV: per-frame data ──────────────────────────────────────

ts_dict = {'frame': np.arange(n_frames), 'time_ns': times_ns}
for ri, ring in enumerate(RINGS):
    lbl = ring['label']
    ts_dict[f'{lbl}_delta_deg']  = all_deltas[ri].round(2)
    ts_dict[f'{lbl}_cumul_deg']  = all_cumulative[ri].round(1)
    ts_dict[f'{lbl}_cumul_rot']  = all_rotations[ri].round(4)

pd.DataFrame(ts_dict).to_csv(f'{OUT}/aromatic_rotations.csv', index=False)
print(f"\nCSV saved: {OUT}/aromatic_rotations.csv")

# ── CSV: summary ─────────────────────────────────────────────

pd.DataFrame(summary_rows).to_csv(f'{OUT}/aromatic_summary.csv', index=False)
print(f"CSV saved: {OUT}/aromatic_summary.csv")

# ── Plot 1: cumulative rotations vs time ─────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

for ri, ring in enumerate(RINGS):
    lw = 1.5 if ring['label'] in ('W336', 'Psilocin') else 0.8
    ax.plot(times_ns, all_rotations[ri], color=ring['color'],
            linewidth=lw, label=ring['label'])

ax.set_xlabel('Time (ns)')
ax.set_ylabel('Cumulative rotations (total angle / 360)')
ax.set_title('Aromatic ring reorientation')
ax.legend(loc='upper left', fontsize=8)
fig.tight_layout()
fig.savefig(f'{OUT}/cumulative_rotations.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/cumulative_rotations.png")

# ── Plot 2: total rotations bar chart ────────────────────────

fig, ax = plt.subplots(figsize=(7, 4))

labels_bar = [ring['label'] for ring in RINGS]
values_bar = [all_rotations[ri, -1] for ri in range(len(RINGS))]
colors_bar = [ring['color'] for ring in RINGS]

bars = ax.barh(labels_bar, values_bar, color=colors_bar, edgecolor='white', linewidth=0.5)
ax.set_xlabel('Total rotations (cumulative angle / 360°)')
ax.set_title('Aromatic ring mobility over 10 ns')
ax.invert_yaxis()

for bar, val in zip(bars, values_bar):
    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
            f'{val:.2f}', va='center', fontsize=8)

fig.tight_layout()
fig.savefig(f'{OUT}/rotation_summary.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/rotation_summary.png")

# ── Plot 3: per-frame angular change ─────────────────────────

fig, ax = plt.subplots(figsize=(8, 4))

for ri, ring in enumerate(RINGS):
    ax.plot(times_ns, all_deltas[ri], color=ring['color'],
            linewidth=0.5, alpha=0.6, label=ring['label'])

ax.set_xlabel('Time (ns)')
ax.set_ylabel('Frame-to-frame angle change (°)')
ax.set_title('Per-frame aromatic ring reorientation')
ax.legend(loc='upper right', fontsize=7)
fig.tight_layout()
fig.savefig(f'{OUT}/angular_changes.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/angular_changes.png")
