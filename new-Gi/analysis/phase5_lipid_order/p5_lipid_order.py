# new-Gi/analysis/phase5_lipid_order/p5_lipid_order.py
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

SPECIES = [
    ('POPC', [('sn-1 (palmitoyl 16:0)', '3', 15),
              ('sn-2 (oleoyl 18:1)',     '2', 17)]),
    ('POPE', [('sn-1 (palmitoyl 16:0)', '3', 15),
              ('sn-2 (oleoyl 18:1)',     '2', 17)]),
    ('SDPE', [('sn-1 (stearoyl 18:0)',  '3', 17),
              ('sn-2 (DHA 22:6)',        '2', 21)]),
]

u = mda.Universe(PSF, DCDS)
n_frames = len(u.trajectory)
print(f"Loaded: {n_frames} frames, {len(u.atoms)} atoms")

# ── Leaflet assignment ────────────────────────────────────────

u.trajectory[0]
phosphorus = u.select_atoms("segid MEMB and name P")
z_mid = np.mean(phosphorus.positions[:, 2])

upper_resids = set()
lower_resids = set()
for atom in phosphorus:
    if atom.position[2] > z_mid:
        upper_resids.add(atom.resid)
    else:
        lower_resids.add(atom.resid)

print(f"Membrane midplane Z = {z_mid:.1f} A")
print(f"Leaflets: {len(upper_resids)} upper, {len(lower_resids)} lower")

# ── Pre-discover all C-H pairs from bonding topology ─────────

print("\nDiscovering C-H pairs...")
all_chains = []

for resname, chains in SPECIES:
    for chain_label, prefix, n_c in chains:
        ch_groups = []

        for i in range(2, 2 + n_c):
            c_name = f"C{prefix}{i}"
            c_sel = u.select_atoms(
                f"segid MEMB and resname {resname} and name {c_name}"
            )
            if len(c_sel) == 0:
                continue

            h_names = sorted(
                a.name for a in c_sel[0].bonded_atoms if a.name.startswith('H')
            )
            h_sels = []
            for hn in h_names:
                hs = u.select_atoms(
                    f"segid MEMB and resname {resname} and name {hn}"
                )
                if len(hs) == len(c_sel):
                    h_sels.append(hs)

            if h_sels:
                ch_groups.append((c_sel, h_sels, i))

        if not ch_groups:
            print(f"  WARNING: no C-H groups for {resname} {chain_label}")
            continue

        lipid_resids = ch_groups[0][0].resids
        n_lipids = len(lipid_resids)
        upper_mask = np.array([r in upper_resids for r in lipid_resids])
        n_upper = int(upper_mask.sum())
        n_lower = n_lipids - n_upper

        accum = {}
        for _, _, pos in ch_groups:
            accum[pos] = {
                'all_sum': 0.0, 'all_n': 0,
                'up_sum': 0.0, 'up_n': 0,
                'lo_sum': 0.0, 'lo_n': 0,
            }

        all_chains.append({
            'resname': resname,
            'label': chain_label,
            'ch_groups': ch_groups,
            'upper_mask': upper_mask,
            'n_lipids': n_lipids,
            'n_upper': n_upper,
            'n_lower': n_lower,
            'accum': accum,
        })

        n_pos = len(ch_groups)
        h_counts = [len(hs) for _, hs, _ in ch_groups]
        print(f"  {resname} {chain_label}: {n_pos} carbons, "
              f"{n_lipids} lipids ({n_upper}U/{n_lower}L), "
              f"H/carbon: {h_counts}")

# ── Single-pass S_CD computation ──────────────────────────────

print(f"\nComputing S_CD ({n_frames} frames, {len(all_chains)} chains)...")

for fi, ts in enumerate(u.trajectory):
    if (fi + 1) % 25 == 0:
        print(f"  frame {fi + 1}/{n_frames}")

    for chain in all_chains:
        mask = chain['upper_mask']
        lo_mask = ~mask
        for c_sel, h_sels, pos in chain['ch_groups']:
            a = chain['accum'][pos]
            for h_sel in h_sels:
                ch = h_sel.positions - c_sel.positions
                norms = np.linalg.norm(ch, axis=1, keepdims=True)
                cos2 = (ch / norms)[:, 2] ** 2

                a['all_sum'] += cos2.sum()
                a['all_n'] += len(cos2)
                a['up_sum'] += cos2[mask].sum()
                a['up_n'] += int(mask.sum())
                a['lo_sum'] += cos2[lo_mask].sum()
                a['lo_n'] += int(lo_mask.sum())

print("Done.\n")

# ── Post-process: compute |S_CD| from accumulated cos²θ ──────

def scd_from_cos2(s, n):
    if n == 0:
        return np.nan
    return abs(0.5 * (3.0 * (s / n) - 1.0))

rows = []
for chain in all_chains:
    positions = []
    scd_all = []
    scd_upper = []
    scd_lower = []

    for _, h_sels, pos in chain['ch_groups']:
        a = chain['accum'][pos]
        s_a = scd_from_cos2(a['all_sum'], a['all_n'])
        s_u = scd_from_cos2(a['up_sum'], a['up_n'])
        s_l = scd_from_cos2(a['lo_sum'], a['lo_n'])

        positions.append(pos)
        scd_all.append(s_a)
        scd_upper.append(s_u)
        scd_lower.append(s_l)

        rows.append({
            'lipid': chain['resname'],
            'chain': chain['label'],
            'carbon': pos,
            'n_h': len(h_sels),
            'scd_all': round(s_a, 4),
            'scd_upper': round(s_u, 4),
            'scd_lower': round(s_l, 4),
        })

    chain['positions'] = positions
    chain['scd_all'] = np.array(scd_all)
    chain['scd_upper'] = np.array(scd_upper)
    chain['scd_lower'] = np.array(scd_lower)

    print(f"{chain['resname']} {chain['label']}  "
          f"({chain['n_lipids']} lipids: {chain['n_upper']}U / {chain['n_lower']}L)")
    print(f"  |S_CD| range: {chain['scd_all'].min():.3f} - {chain['scd_all'].max():.3f}, "
          f"mean: {chain['scd_all'].mean():.3f}")

# ── CSV ───────────────────────────────────────────────────────

df = pd.DataFrame(rows)
df.to_csv(f'{OUT}/scd_data.csv', index=False)
print(f"\nCSV saved: {OUT}/scd_data.csv")

# ── Per-species plots ─────────────────────────────────────────

SN1_COLOR = '#2c7bb6'
SN2_COLOR = '#d7191c'

for resname, _ in SPECIES:
    species_chains = [c for c in all_chains if c['resname'] == resname]
    fig, ax = plt.subplots(figsize=(8, 4))

    for chain in species_chains:
        color = SN1_COLOR if 'sn-1' in chain['label'] else SN2_COLOR
        ax.plot(chain['positions'], chain['scd_all'],
                'o-', color=color, markersize=3, linewidth=1,
                label=chain['label'])

    ax.set_xlabel('Acyl chain carbon position')
    ax.set_ylabel('|S$_{CD}$|')
    ax.set_title(f'{resname}  ({species_chains[0]["n_lipids"]} lipids)')
    ax.set_ylim(0, 0.45)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f'{OUT}/scd_{resname}.png', dpi=150)
    plt.close()
    print(f"Plot saved: {OUT}/scd_{resname}.png")

# ── Leaflet comparison for POPC sn-2 ─────────────────────────

popc_sn2 = next(c for c in all_chains
                 if c['resname'] == 'POPC' and 'sn-2' in c['label'])

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(popc_sn2['positions'], popc_sn2['scd_all'],
        'o-', color='black', markersize=3, linewidth=1, label=f'All ({popc_sn2["n_lipids"]})')
ax.plot(popc_sn2['positions'], popc_sn2['scd_upper'],
        's--', color='#fdae61', markersize=3, linewidth=0.8,
        label=f'Upper ({popc_sn2["n_upper"]})')
ax.plot(popc_sn2['positions'], popc_sn2['scd_lower'],
        '^--', color='#abd9e9', markersize=3, linewidth=0.8,
        label=f'Lower ({popc_sn2["n_lower"]})')
ax.set_xlabel('Acyl chain carbon position')
ax.set_ylabel('|S$_{CD}$|')
ax.set_title('POPC sn-2 (oleoyl 18:1) — leaflet comparison')
ax.set_ylim(0, 0.45)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f'{OUT}/scd_POPC_leaflets.png', dpi=150)
plt.close()
print(f"Plot saved: {OUT}/scd_POPC_leaflets.png")
