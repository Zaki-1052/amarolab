# analysis/phase10_rotamers/p10_rotamers.py
from pathlib import Path
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_dihedrals
from scipy.stats import circmean, circstd
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

OFFSETS = {'PROA': 78, 'PROB': 78, 'PROC': 127}

def lit_resid(resid, segid):
    return resid + OFFSETS.get(segid, 0)

# ── Target residues ──────────────────────────────────────────

CHI2_ATOM4 = {
    'TRP': 'CD1',
    'PHE': 'CD1',
    'TYR': 'CD1',
    'ASP': 'OD1',
}

TARGETS = [
    ('PROC', 209, 'TRP', 'W336'),
    ('PROC', 212, 'PHE', 'F339'),
    ('PROC', 213, 'PHE', 'F340'),
    ('PROB', 156, 'PHE', 'F234'),
    ('PROB', 165, 'PHE', 'F243'),
    ('PROC', 243, 'TYR', 'Y370'),
    ('PROA',  77, 'ASP', 'D155'),
]

# ── Compute chi1 and chi2 ───────────────────────────────────

chi_results = {}

for segid, resid, resname, lit_label in TARGETS:
    sel = f"segid {segid} and resid {resid}"
    n_atom  = u.select_atoms(f"{sel} and name N")
    ca_atom = u.select_atoms(f"{sel} and name CA")
    cb_atom = u.select_atoms(f"{sel} and name CB")
    cg_atom = u.select_atoms(f"{sel} and name CG")

    for name, ag in [('N', n_atom), ('CA', ca_atom), ('CB', cb_atom), ('CG', cg_atom)]:
        assert len(ag) == 1, f"{lit_label}: expected 1 {name}, got {len(ag)}"

    atom4_name = CHI2_ATOM4[resname]
    cd_atom = u.select_atoms(f"{sel} and name {atom4_name}")
    assert len(cd_atom) == 1, f"{lit_label}: expected 1 {atom4_name}, got {len(cd_atom)}"

    chi1_vals = np.empty(n_frames)
    chi2_vals = np.empty(n_frames)

    for fi, ts in enumerate(u.trajectory):
        chi1_vals[fi] = np.degrees(calc_dihedrals(
            n_atom.positions[0], ca_atom.positions[0],
            cb_atom.positions[0], cg_atom.positions[0],
        ))
        chi2_vals[fi] = np.degrees(calc_dihedrals(
            ca_atom.positions[0], cb_atom.positions[0],
            cg_atom.positions[0], cd_atom.positions[0],
        ))

    chi_results[lit_label] = {
        'chi1': chi1_vals, 'chi2': chi2_vals,
        'segid': segid, 'resid': resid, 'resname': resname,
    }
    print(f"{lit_label} ({resname} {segid} {resid}): chi1/chi2 computed")

# ── Rotamer state classification ─────────────────────────────

def classify_chi1(angle):
    if -120 < angle <= 0:
        return 'g-'
    elif 0 < angle <= 120:
        return 'g+'
    else:
        return 't'

def count_transitions(angles, hysteresis=30):
    states = [classify_chi1(a) for a in angles]
    transitions = 0
    current = states[0]
    for s in states[1:]:
        if s != current:
            transitions += 1
            current = s
    return transitions

# ── Summary statistics ───────────────────────────────────────

print(f"\n{'Residue':<10} {'chi1 mean':>10} {'chi1 std':>9} {'chi2 mean':>10} "
      f"{'chi2 std':>9} {'Rotamer':>8} {'Trans':>6}")
print('-' * 68)

summary_rows = []
for lit_label in [t[3] for t in TARGETS]:
    d = chi_results[lit_label]
    chi1_rad = np.radians(d['chi1'])
    chi2_rad = np.radians(d['chi2'])

    c1_mean = np.degrees(circmean(chi1_rad, high=np.pi, low=-np.pi))
    c1_std  = np.degrees(circstd(chi1_rad, high=np.pi, low=-np.pi))
    c2_mean = np.degrees(circmean(chi2_rad, high=np.pi, low=-np.pi))
    c2_std  = np.degrees(circstd(chi2_rad, high=np.pi, low=-np.pi))

    dominant = classify_chi1(c1_mean)
    n_trans  = count_transitions(d['chi1'])

    print(f"{lit_label:<10} {c1_mean:10.1f} {c1_std:9.1f} {c2_mean:10.1f} "
          f"{c2_std:9.1f} {dominant:>8} {n_trans:6d}")

    summary_rows.append({
        'lit_label': lit_label,
        'resname': d['resname'],
        'segid': d['segid'],
        'resid': d['resid'],
        'chi1_mean': round(c1_mean, 1),
        'chi1_std': round(c1_std, 1),
        'chi1_range': round(d['chi1'].max() - d['chi1'].min(), 1),
        'chi2_mean': round(c2_mean, 1),
        'chi2_std': round(c2_std, 1),
        'chi2_range': round(d['chi2'].max() - d['chi2'].min(), 1),
        'dominant_rotamer': dominant,
        'n_chi1_transitions': n_trans,
    })

# ── CSV: time series ─────────────────────────────────────────

ts_dict = {'frame': np.arange(n_frames), 'time_ns': times_ns}
for lit_label in [t[3] for t in TARGETS]:
    ts_dict[f'{lit_label}_chi1'] = chi_results[lit_label]['chi1'].round(2)
    ts_dict[f'{lit_label}_chi2'] = chi_results[lit_label]['chi2'].round(2)

pd.DataFrame(ts_dict).to_csv(f'{OUT}/rotamer_timeseries.csv', index=False)
print(f"\nCSV saved: {OUT}/rotamer_timeseries.csv")

# ── CSV: summary ─────────────────────────────────────────────

pd.DataFrame(summary_rows).to_csv(f'{OUT}/rotamer_summary.csv', index=False)
print(f"CSV saved: {OUT}/rotamer_summary.csv")

# ── Plot 1: chi1 time series ────────────────────────────────

labels = [t[3] for t in TARGETS]
fig, axes = plt.subplots(len(labels), 1, figsize=(10, 2.2 * len(labels)),
                         sharex=True)

for ax, lit_label in zip(axes, labels):
    chi1 = chi_results[lit_label]['chi1']
    lw = 1.2 if lit_label == 'W336' else 0.8
    color = '#2c7bb6' if lit_label == 'W336' else '#d7191c'
    ax.plot(times_ns, chi1, color=color, linewidth=lw)
    for y in [-60, 60, 180]:
        ax.axhline(y=y, color='grey', linestyle='--', alpha=0.3, linewidth=0.5)
    ax.set_ylim(-180, 180)
    ax.set_ylabel(f'{lit_label}\nχ1 (°)', fontsize=8)
    ax.tick_params(labelsize=7)

axes[-1].set_xlabel('Time (ns)')
axes[0].set_title('Chi1 dihedral angles — binding pocket residues')
fig.tight_layout()
fig.savefig(f'{OUT}/chi1_timeseries.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/chi1_timeseries.png")

# ── Plot 2: chi2 time series ────────────────────────────────

fig, axes = plt.subplots(len(labels), 1, figsize=(10, 2.2 * len(labels)),
                         sharex=True)

for ax, lit_label in zip(axes, labels):
    chi2 = chi_results[lit_label]['chi2']
    lw = 1.2 if lit_label == 'W336' else 0.8
    color = '#2c7bb6' if lit_label == 'W336' else '#d7191c'
    ax.plot(times_ns, chi2, color=color, linewidth=lw)
    ax.set_ylim(-180, 180)
    ax.set_ylabel(f'{lit_label}\nχ2 (°)', fontsize=8)
    ax.tick_params(labelsize=7)

axes[-1].set_xlabel('Time (ns)')
axes[0].set_title('Chi2 dihedral angles — binding pocket residues')
fig.tight_layout()
fig.savefig(f'{OUT}/chi2_timeseries.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/chi2_timeseries.png")

# ── Plot 3: W336 toggle switch ──────────────────────────────

w = chi_results['W336']
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

ax1.plot(times_ns, w['chi1'], color='#2c7bb6', linewidth=1.0)
ax1.axhspan(-120, 0, alpha=0.08, color='#2c7bb6', label='g-')
ax1.axhspan(0, 120, alpha=0.08, color='#1a9641', label='g+')
ax1.axhspan(120, 180, alpha=0.08, color='#d7191c', label='trans')
ax1.axhspan(-180, -120, alpha=0.08, color='#d7191c')
ax1.set_ylim(-180, 180)
ax1.set_ylabel('χ1 (°)')
ax1.set_title('W336 (W209) toggle switch')
ax1.legend(loc='upper right', fontsize=7)

ax2.plot(times_ns, w['chi2'], color='#2c7bb6', linewidth=1.0)
ax2.set_ylim(-180, 180)
ax2.set_ylabel('χ2 (°)')
ax2.set_xlabel('Time (ns)')

fig.tight_layout()
fig.savefig(f'{OUT}/w336_toggle_switch.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/w336_toggle_switch.png")

# ── Plot 4: rotamer distributions (chi1 vs chi2 scatter) ────

fig, axes = plt.subplots(2, 4, figsize=(14, 7))
axes_flat = axes.flatten()

for i, lit_label in enumerate(labels):
    ax = axes_flat[i]
    d = chi_results[lit_label]
    ax.scatter(d['chi1'], d['chi2'], s=8, alpha=0.5, color='#2c7bb6', edgecolors='none')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_title(lit_label, fontsize=9)
    ax.set_xlabel('χ1', fontsize=8)
    ax.set_ylabel('χ2', fontsize=8)
    ax.tick_params(labelsize=7)
    for y in [-60, 60, 180]:
        ax.axhline(y=y, color='grey', linestyle=':', alpha=0.3, linewidth=0.5)
        ax.axvline(x=y, color='grey', linestyle=':', alpha=0.3, linewidth=0.5)

axes_flat[-1].axis('off')

fig.suptitle('Side-chain rotamer distributions (χ1 vs χ2)', fontsize=11)
fig.tight_layout()
fig.savefig(f'{OUT}/rotamer_distributions.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/rotamer_distributions.png")
