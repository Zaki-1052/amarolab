# analysis/phase5_lipid_order/p5_crossval.py
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

from lipyphilic.analysis.order_parameter import SCC

# ── Run SCC on both POPC chains ───────────────────────────────

chains = {
    'sn-1': [f"C3{i}" for i in range(2, 17)],
    'sn-2': [f"C2{i}" for i in range(2, 19)],
}

scc_results = {}
for label, names in chains.items():
    sel = f"segid MEMB and resname POPC and name {' '.join(names)}"
    scc = SCC(universe=u, tail_sel=sel)
    scc.run()
    scc_results[label] = scc.SCC
    print(f"POPC {label}: shape {scc.SCC.shape}, "
          f"range [{scc.SCC.min():.3f}, {scc.SCC.max():.3f}]")

# ── Load manual S_CD means ────────────────────────────────────

df = pd.read_csv(f'{OUT}/scd_data.csv')
scd_means = {}
for label in chains:
    mask = (df['lipid'] == 'POPC') & (df['chain'].str.startswith(label))
    scd_means[label] = df.loc[mask, 'scd_all'].mean()

# ── Comparison table ──────────────────────────────────────────

print(f"\n{'Chain':<8} {'|S_CD| mean':>12} {'S_CC mean':>12} {'|S_CC|/2':>12} {'Ratio':>8}")
print("-" * 56)
for label in chains:
    scd = scd_means[label]
    scc_mean = scc_results[label].mean()
    approx = abs(scc_mean) / 2
    ratio = approx / scd if scd > 0 else float('nan')
    print(f"{label:<8} {scd:>12.4f} {scc_mean:>12.4f} {approx:>12.4f} {ratio:>8.2f}")

print(f"\nExpected: |S_CC|/2 ≈ |S_CD| for saturated chains (ratio ≈ 1.0)")
print(f"The relationship breaks at double bonds, so sn-2 may differ more.")

# ── Ordering check ────────────────────────────────────────────

scc_sn1_mean = scc_results['sn-1'].mean()
scc_sn2_mean = scc_results['sn-2'].mean()
scd_sn1 = scd_means['sn-1']
scd_sn2 = scd_means['sn-2']

print(f"\nOrdering check (saturated > unsaturated):")
print(f"  S_CD: sn-1 ({scd_sn1:.3f}) > sn-2 ({scd_sn2:.3f}): "
      f"{'PASS' if scd_sn1 > scd_sn2 else 'FAIL'}")
print(f"  S_CC: sn-1 ({scc_sn1_mean:.3f}) > sn-2 ({scc_sn2_mean:.3f}): "
      f"{'PASS' if scc_sn1_mean > scc_sn2_mean else 'FAIL'}")

# ── Per-lipid distribution ────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for ax, label in zip(axes, ['sn-1', 'sn-2']):
    per_lipid = scc_results[label].mean(axis=1)
    ax.hist(per_lipid, bins=12, color='#2c7bb6', edgecolor='white', alpha=0.8)
    ax.axvline(per_lipid.mean(), color='#d7191c', linestyle='--',
               label=f'mean = {per_lipid.mean():.3f}')
    ax.set_xlabel('Time-averaged S$_{CC}$')
    ax.set_ylabel('Count (lipids)')
    ax.set_title(f'POPC {label}  (n=48)')
    ax.legend(fontsize=8)

fig.suptitle('Per-lipid S$_{CC}$ distribution (lipyphilic)', fontsize=11)
fig.tight_layout()
fig.savefig(f'{OUT}/scd_crossval_POPC.png', dpi=150)
plt.close()
print(f"\nPlot saved: {OUT}/scd_crossval_POPC.png")
