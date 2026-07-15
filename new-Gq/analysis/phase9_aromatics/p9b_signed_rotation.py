# new-Gq/analysis/phase9_aromatics/p9b_signed_rotation.py
#
# Signed aromatic ring reorientation with pairwise correlations.
# Gq version — same analysis as Gi p9b, different segments/offsets.
from pathlib import Path
import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parent.parent.parent.parent
BASE = str(REPO / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)
n_frames = len(u.trajectory)
times_ns = np.arange(n_frames) * 0.1

OFFSETS = {'PROA': 78, 'PROB': 78, 'PROC': 127}

def lit_resid(resid, segid):
    return resid + OFFSETS.get(segid, 0)

RINGS = [
    {
        'label': 'W336',
        'sel': 'segid PROC and resid 209 and name CG CD1 NE1 CE2 CD2 CE3 CZ3 CH2 CZ2',
        'n_atoms': 9,
        'color': '#2c7bb6',
    },
    {
        'label': 'F339',
        'sel': 'segid PROC and resid 212 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#d7191c',
    },
    {
        'label': 'F340',
        'sel': 'segid PROC and resid 213 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#fdae61',
    },
    {
        'label': 'F234',
        'sel': 'segid PROB and resid 156 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#abd9e9',
    },
    {
        'label': 'F243',
        'sel': 'segid PROB and resid 165 and name CG CD1 CD2 CE1 CE2 CZ',
        'n_atoms': 6,
        'color': '#1a9641',
    },
    {
        'label': 'Y370',
        'sel': 'segid PROC and resid 243 and name CG CD1 CD2 CE1 CE2 CZ',
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

# ── Compute ring normals with signed rotation ────────────────

def ring_normal(positions):
    centered = positions - positions.mean(axis=0)
    _, _, Vt = np.linalg.svd(centered)
    return Vt[2]

all_normals       = np.zeros((len(RINGS), n_frames, 3))
all_unsigned_delta = np.zeros((len(RINGS), n_frames))
all_signed_delta   = np.zeros((len(RINGS), n_frames))
ref_axis           = np.zeros((len(RINGS), 3))

for fi, ts in enumerate(u.trajectory):
    for ri, ag in enumerate(ring_groups):
        n = ring_normal(ag.positions)

        if fi == 0:
            ref_axis[ri] = n
            all_normals[ri, fi] = n
            continue

        if np.dot(n, all_normals[ri, fi - 1]) < 0:
            n = -n
        all_normals[ri, fi] = n

        n_prev = all_normals[ri, fi - 1]
        n_curr = n

        cos_theta = np.clip(np.dot(n_curr, n_prev), -1.0, 1.0)
        angle_unsigned = np.degrees(np.arccos(cos_theta))
        all_unsigned_delta[ri, fi] = angle_unsigned

        cross = np.cross(n_prev, n_curr)
        sign = np.sign(np.dot(cross, ref_axis[ri]))
        if sign == 0:
            sign = 1.0
        all_signed_delta[ri, fi] = sign * angle_unsigned

        drift = np.degrees(np.arccos(
            np.clip(abs(np.dot(n_curr, ref_axis[ri])), 0.0, 1.0)))
        if drift > 80:
            print(f"  WARNING: {RINGS[ri]['label']} frame {fi} — "
                  f"normal drifted {drift:.1f}° from reference axis")

    if (fi + 1) % 20 == 0:
        print(f"  frame {fi + 1}/{n_frames}")

all_unsigned_cumul = np.cumsum(all_unsigned_delta, axis=1)
all_signed_cumul   = np.cumsum(all_signed_delta, axis=1)
all_unsigned_norm  = all_unsigned_cumul / 180.0

# ── Summary ──────────────────────────────────────────────────

print(f"\n{'Ring':<12} {'Unsign tot':>10} {'Signed tot':>10} "
      f"{'Norm (÷180)':>11} {'Mean |Δ|':>8} {'Std |Δ|':>8} "
      f"{'Mean sΔ':>8} {'Std sΔ':>8}")
print('-' * 90)

summary_rows = []
for ri, ring in enumerate(RINGS):
    ud = all_unsigned_delta[ri, 1:]
    sd = all_signed_delta[ri, 1:]

    summary_rows.append({
        'ring_label': ring['label'],
        'total_unsigned_deg': round(float(all_unsigned_cumul[ri, -1]), 1),
        'total_signed_deg': round(float(all_signed_cumul[ri, -1]), 1),
        'normalized_unsigned': round(float(all_unsigned_norm[ri, -1]), 3),
        'mean_unsigned_delta': round(float(ud.mean()), 2),
        'std_unsigned_delta': round(float(ud.std()), 2),
        'max_unsigned_delta': round(float(ud.max()), 2),
        'mean_signed_delta': round(float(sd.mean()), 2),
        'std_signed_delta': round(float(sd.std()), 2),
    })

    print(f"{ring['label']:<12} "
          f"{all_unsigned_cumul[ri, -1]:10.1f} "
          f"{all_signed_cumul[ri, -1]:10.1f} "
          f"{all_unsigned_norm[ri, -1]:11.3f} "
          f"{ud.mean():8.2f} {ud.std():8.2f} "
          f"{sd.mean():8.2f} {sd.std():8.2f}")

# ── Pairwise correlations ────────────────────────────────────

CORR_LABELS = ['W336', 'F339', 'F340', 'F234']
corr_indices = [i for i, r in enumerate(RINGS) if r['label'] in CORR_LABELS]
n_corr = len(corr_indices)

corr_matrix = np.zeros((n_corr, n_corr))
for i in range(n_corr):
    for j in range(n_corr):
        corr_matrix[i, j] = np.corrcoef(
            all_signed_delta[corr_indices[i], 1:],
            all_signed_delta[corr_indices[j], 1:]
        )[0, 1]

print(f"\nPairwise Pearson r (signed deltas):")
header = f"{'':>8}" + "".join(f"{CORR_LABELS[j]:>8}" for j in range(n_corr))
print(header)
for i in range(n_corr):
    row = f"{CORR_LABELS[i]:>8}" + "".join(
        f"{corr_matrix[i, j]:8.3f}" for j in range(n_corr))
    print(row)

# ── Running correlation (10-frame / 1 ns windows) ───────────

window = 10
n_windows = n_frames - window
pairs = []
for i in range(n_corr):
    for j in range(i + 1, n_corr):
        pairs.append((i, j, f"{CORR_LABELS[i]}-{CORR_LABELS[j]}"))

running_corr = np.zeros((len(pairs), n_windows))
running_times = np.zeros(n_windows)

for wi in range(n_windows):
    start = wi + 1
    end = start + window
    running_times[wi] = times_ns[start + window // 2]
    for pi, (i, j, _) in enumerate(pairs):
        ri_i = corr_indices[i]
        ri_j = corr_indices[j]
        seg_i = all_signed_delta[ri_i, start:end]
        seg_j = all_signed_delta[ri_j, start:end]
        if seg_i.std() > 0 and seg_j.std() > 0:
            running_corr[pi, wi] = np.corrcoef(seg_i, seg_j)[0, 1]

# ── CSV ──────────────────────────────────────────────────────

ts_dict = {'frame': np.arange(n_frames), 'time_ns': times_ns}
for ri, ring in enumerate(RINGS):
    lbl = ring['label']
    ts_dict[f'{lbl}_delta_unsigned'] = all_unsigned_delta[ri].round(2)
    ts_dict[f'{lbl}_delta_signed']   = all_signed_delta[ri].round(2)
    ts_dict[f'{lbl}_cumul_unsigned'] = all_unsigned_cumul[ri].round(1)
    ts_dict[f'{lbl}_cumul_signed']   = all_signed_cumul[ri].round(1)

pd.DataFrame(ts_dict).to_csv(f'{OUT}/aromatic_signed_rotations.csv', index=False)
print(f"\nCSV saved: {OUT}/aromatic_signed_rotations.csv")

pd.DataFrame(summary_rows).to_csv(f'{OUT}/aromatic_signed_summary.csv', index=False)
print(f"CSV saved: {OUT}/aromatic_signed_summary.csv")

corr_df = pd.DataFrame(corr_matrix.round(3),
                        index=CORR_LABELS, columns=CORR_LABELS)
corr_df.to_csv(f'{OUT}/aromatic_correlations.csv')
print(f"CSV saved: {OUT}/aromatic_correlations.csv")

# ── Plot 1: signed cumulative rotations ──────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

for ri, ring in enumerate(RINGS):
    lw = 1.5 if ring['label'] in ('W336', 'Psilocin', 'F234') else 0.8
    ax.plot(times_ns, all_signed_cumul[ri], color=ring['color'],
            linewidth=lw, label=ring['label'])

ax.axhline(y=0, color='grey', linestyle='--', alpha=0.4, linewidth=0.5)
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Signed cumulative rotation (°)')
ax.set_title('Aromatic ring reorientation — signed (Gq)')
ax.legend(loc='best', fontsize=8)
fig.tight_layout()
fig.savefig(f'{OUT}/signed_cumulative_rotations.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/signed_cumulative_rotations.png")

# ── Plot 2: unsigned vs signed comparison ────────────────────

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

for ri, ring in enumerate(RINGS):
    lw = 1.5 if ring['label'] in ('W336', 'F234') else 0.8
    ax1.plot(times_ns, all_unsigned_cumul[ri], color=ring['color'],
             linewidth=lw, label=ring['label'])
    ax2.plot(times_ns, all_signed_cumul[ri], color=ring['color'],
             linewidth=lw, label=ring['label'])

ax1.set_ylabel('Unsigned cumulative (°)')
ax1.set_title('Unsigned (total reorientation magnitude)')
ax1.legend(loc='upper left', fontsize=7)

ax2.axhline(y=0, color='grey', linestyle='--', alpha=0.4, linewidth=0.5)
ax2.set_xlabel('Time (ns)')
ax2.set_ylabel('Signed cumulative (°)')
ax2.set_title('Signed (net directional rotation)')
ax2.legend(loc='best', fontsize=7)

fig.tight_layout()
fig.savefig(f'{OUT}/unsigned_vs_signed_cumulative.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/unsigned_vs_signed_cumulative.png")

# ── Plot 3: correlation matrix heatmap ───────────────────────

fig, ax = plt.subplots(figsize=(5, 4))

im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1,
               aspect='equal')
ax.set_xticks(range(n_corr))
ax.set_yticks(range(n_corr))
ax.set_xticklabels(CORR_LABELS, fontsize=9)
ax.set_yticklabels(CORR_LABELS, fontsize=9)

for i in range(n_corr):
    for j in range(n_corr):
        ax.text(j, i, f'{corr_matrix[i, j]:.2f}', ha='center', va='center',
                fontsize=10, color='white' if abs(corr_matrix[i, j]) > 0.5 else 'black')

fig.colorbar(im, ax=ax, label='Pearson r (signed Δ)')
ax.set_title('Pairwise aromatic rotation correlation (Gq)')
fig.tight_layout()
fig.savefig(f'{OUT}/aromatic_correlation_matrix.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/aromatic_correlation_matrix.png")

# ── Plot 4: running correlation ──────────────────────────────

PAIR_COLORS = ['#2c7bb6', '#d7191c', '#fdae61', '#1a9641', '#7570b3', '#e7298a']

fig, ax = plt.subplots(figsize=(8, 4))

for pi, (i, j, label) in enumerate(pairs):
    ax.plot(running_times, running_corr[pi], linewidth=1.0,
            color=PAIR_COLORS[pi % len(PAIR_COLORS)], label=label, alpha=0.8)

ax.axhline(y=0, color='grey', linestyle='--', alpha=0.4, linewidth=0.5)
ax.set_xlabel('Time (ns)')
ax.set_ylabel(f'Pearson r ({window}-frame window)')
ax.set_title('Running pairwise aromatic rotation correlation (Gq)')
ax.set_ylim(-1, 1)
ax.legend(loc='best', fontsize=7)
fig.tight_layout()
fig.savefig(f'{OUT}/aromatic_running_correlation.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/aromatic_running_correlation.png")
