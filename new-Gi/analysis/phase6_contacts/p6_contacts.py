# new-Gi/analysis/phase6_contacts/p6_contacts.py
from pathlib import Path
import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from MDAnalysis.lib.distances import capped_distance
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = str(ROOT / 'charmm-gui-8313215931' / 'openmm')
OUT  = str(Path(__file__).resolve().parent)

PSF  = f'{BASE}/step5_input.psf'
DCDS = [f'{BASE}/step7_{i}.dcd' for i in range(1, 11)]

u = mda.Universe(PSF, DCDS)

CUTOFF = 4.0
n_frames = len(u.trajectory)
times_ns = np.arange(n_frames) * 0.1

# ── Selections ────────────────────────────────────────────────

receptor = u.select_atoms("segid PROE PROF")
glpa_segs = " ".join([f"GLPA{i}" for i in range(1, 25)])
lipids = u.select_atoms(f"segid MEMB or segid {glpa_segs}")

print(f"Receptor: {len(receptor)} atoms, {len(receptor.residues)} residues")
print(f"Lipids:   {len(lipids)} atoms, {len(lipids.residues)} residues")
print(f"Frames: {n_frames}, cutoff: {CUTOFF} A\n")

# ── Precompute per-atom lookup arrays ─────────────────────────

rec_resids = receptor.resids
rec_segids_str = receptor.segids
seg_names = sorted(set(rec_segids_str))
seg_to_int = {s: i for i, s in enumerate(seg_names)}
rec_seg_int = np.array([seg_to_int[s] for s in rec_segids_str])

lip_resnames_str = lipids.resnames
RESNAME_MERGE = {'BGAL': 'GalCer', 'CER160': 'GalCer'}
lip_display = np.array([RESNAME_MERGE.get(rn, rn) for rn in lip_resnames_str])
display_names = sorted(set(lip_display))
dn_to_int = {dn: i for i, dn in enumerate(display_names)}
lip_dn_int = np.array([dn_to_int[dn] for dn in lip_display])

resname_lookup = {}
for res in receptor.residues:
    resname_lookup[(res.resid, res.segid)] = res.resname

print(f"Lipid species ({len(display_names)}): {', '.join(display_names)}")
print(f"Receptor segments: {seg_names}\n")

# ── Main contact loop ─────────────────────────────────────────
# Key = resid * 1000 + seg_int * 100 + dn_int
# With 2 receptor segments and ~16 lipid species, no collisions

contact_counts = defaultdict(int)

for fi, ts in enumerate(u.trajectory):
    if fi % 10 == 0:
        print(f"  Frame {fi}/{n_frames}...", end='\r')

    pairs, _ = capped_distance(
        receptor.positions, lipids.positions,
        max_cutoff=CUTOFF, box=ts.dimensions
    )

    if len(pairs) == 0:
        continue

    r_res = rec_resids[pairs[:, 0]]
    r_seg = rec_seg_int[pairs[:, 0]]
    l_dn  = lip_dn_int[pairs[:, 1]]

    keys = r_res.astype(np.int64) * 1000 + r_seg * 100 + l_dn
    for k in np.unique(keys):
        contact_counts[int(k)] += 1

print(f"\nDone. {len(contact_counts)} unique (residue, species) contacts.\n")

# ── Decode keys ───────────────────────────────────────────────

decoded = {}
for k, count in contact_counts.items():
    dn_int = k % 100
    seg_int = (k // 100) % 10
    resid = k // 1000
    segid = seg_names[seg_int]
    species = display_names[dn_int]
    decoded[(resid, segid, species)] = count / n_frames


def current_to_lit(resid, segid):
    if segid == 'PROE':
        return resid + 79
    elif segid == 'PROF':
        return resid + 131
    return resid


# ══════════════════════════════════════════════════════════════
# Analysis 1: contacts by lipid species
# ══════════════════════════════════════════════════════════════

species_totals = defaultdict(float)
for (resid, segid, species), freq in decoded.items():
    species_totals[species] += freq

mol_counts = {}
for dn in display_names:
    if dn == 'GalCer':
        mol_counts[dn] = 24
    else:
        mol_counts[dn] = len(u.select_atoms(f"segid MEMB and resname {dn}").residues)

species_sorted = sorted(species_totals.keys(),
                        key=lambda x: species_totals[x], reverse=True)

print(f"{'='*56}")
print("Analysis 1: contacts by lipid species")
print(f"{'='*56}")
print(f"{'Species':<10} {'Total freq':>12} {'N_mol':>8} {'Per-mol':>10}")
print("-" * 44)
for sp in species_sorted:
    n = mol_counts.get(sp, 0)
    per_mol = species_totals[sp] / n if n > 0 else 0
    print(f"{sp:<10} {species_totals[sp]:>12.1f} {n:>8} {per_mol:>10.2f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors = ['#d73027' if s == 'CHL1' else '#4575b4' for s in species_sorted]
axes[0].bar(range(len(species_sorted)),
            [species_totals[s] for s in species_sorted], color=colors)
axes[0].set_xticks(range(len(species_sorted)))
axes[0].set_xticklabels(species_sorted, rotation=45, ha='right', fontsize=8)
axes[0].set_ylabel('Summed contact frequency')
axes[0].set_title('Total contacts by species')

per_mol_sorted = sorted(display_names,
                        key=lambda x: species_totals.get(x, 0) / max(mol_counts.get(x, 1), 1),
                        reverse=True)
per_mol_vals = [species_totals.get(s, 0) / max(mol_counts.get(s, 1), 1)
                for s in per_mol_sorted]
colors2 = ['#d73027' if s == 'CHL1' else '#4575b4' for s in per_mol_sorted]
axes[1].bar(range(len(per_mol_sorted)), per_mol_vals, color=colors2)
axes[1].set_xticks(range(len(per_mol_sorted)))
axes[1].set_xticklabels(per_mol_sorted, rotation=45, ha='right', fontsize=8)
axes[1].set_ylabel('Contact frequency per molecule')
axes[1].set_title('Per-molecule contact tendency')

fig.tight_layout()
fig.savefig(f'{OUT}/contacts_by_species.png', dpi=150)
plt.close()
print(f"\nPlot: {OUT}/contacts_by_species.png")

# ══════════════════════════════════════════════════════════════
# Analysis 2: per-residue contact profile
# ══════════════════════════════════════════════════════════════

residue_totals = defaultdict(float)
for (resid, segid, species), freq in decoded.items():
    residue_totals[(resid, segid)] += freq

seg_colors = {'PROE': '#2c7bb6', 'PROF': '#fdae61'}

fig, ax = plt.subplots(figsize=(12, 4))
for seg in ['PROE', 'PROF']:
    resids_seg = sorted([r for (r, s) in residue_totals if s == seg])
    freqs_seg = [residue_totals[(r, seg)] for r in resids_seg]
    ax.plot(resids_seg, freqs_seg, color=seg_colors[seg],
            linewidth=0.8, label=seg, alpha=0.8)

ax.set_xlabel('Residue number (current numbering)')
ax.set_ylabel('Total contact frequency (all species)')
ax.set_title('Per-residue lipid contacts')
for boundary in [183.5]:
    ax.axvline(x=boundary, color='grey', linestyle=':', alpha=0.4)
ax.legend()
fig.tight_layout()
fig.savefig(f'{OUT}/contacts_per_residue.png', dpi=150)
plt.close()

print(f"\n{'='*56}")
print("Analysis 2: per-residue contact profile")
print(f"{'='*56}")
print(f"Plot: {OUT}/contacts_per_residue.png")

top20 = sorted(residue_totals.keys(),
               key=lambda x: residue_totals[x], reverse=True)[:20]
print(f"\nTop 20 most lipid-contacted residues:")
print(f"{'Resid':>6} {'Seg':<6} {'AA':<5} {'Lit#':>6} {'Total':>8}")
print("-" * 35)
for (resid, segid) in top20:
    rn = resname_lookup.get((resid, segid), '?')
    lit = current_to_lit(resid, segid)
    print(f"{resid:>6} {segid:<6} {rn:<5} {lit:>6} {residue_totals[(resid, segid)]:>8.2f}")

bottom10 = sorted(residue_totals.keys(),
                  key=lambda x: residue_totals[x])[:10]
print(f"\nBottom 10 (least lipid-contacted):")
print(f"{'Resid':>6} {'Seg':<6} {'AA':<5} {'Lit#':>6} {'Total':>8}")
print("-" * 35)
for (resid, segid) in bottom10:
    rn = resname_lookup.get((resid, segid), '?')
    lit = current_to_lit(resid, segid)
    print(f"{resid:>6} {segid:<6} {rn:<5} {lit:>6} {residue_totals[(resid, segid)]:>8.02f}")

# ══════════════════════════════════════════════════════════════
# Analysis 3: cholesterol contacts
# ══════════════════════════════════════════════════════════════

chl_contacts = {}
for (resid, segid, species), freq in decoded.items():
    if species == 'CHL1':
        chl_contacts[(resid, segid)] = freq

chl_sorted = sorted(chl_contacts.keys(),
                    key=lambda x: chl_contacts[x], reverse=True)

print(f"\n{'='*56}")
print("Analysis 3: cholesterol contacts")
print(f"{'='*56}")
print(f"Residues contacting CHL1: {len(chl_contacts)}")

print(f"\nTop 20 cholesterol-contacted residues:")
print(f"{'Resid':>6} {'Seg':<6} {'AA':<5} {'Lit#':>6} {'Freq':>8}")
print("-" * 35)
for (resid, segid) in chl_sorted[:20]:
    rn = resname_lookup.get((resid, segid), '?')
    lit = current_to_lit(resid, segid)
    print(f"{resid:>6} {segid:<6} {rn:<5} {lit:>6} {chl_contacts[(resid, segid)]:>8.2f}")

persistent = [(r, s) for (r, s) in chl_sorted if chl_contacts[(r, s)] >= 0.9]
print(f"\nPersistent CHL1 contacts (freq >= 0.9): {len(persistent)} residues")
for (resid, segid) in persistent:
    rn = resname_lookup.get((resid, segid), '?')
    lit = current_to_lit(resid, segid)
    print(f"  {rn}{lit} (resid {resid}, {segid}, freq {chl_contacts[(resid, segid)]:.2f})")

fig, ax = plt.subplots(figsize=(12, 4))
for seg in ['PROE', 'PROF']:
    resids_seg = sorted([r for (r, s) in chl_contacts if s == seg])
    freqs_seg = [chl_contacts[(r, seg)] for r in resids_seg]
    if resids_seg:
        ax.bar(resids_seg, freqs_seg, color=seg_colors[seg],
               alpha=0.7, width=1.0, label=seg)

ax.set_xlabel('Residue number (current numbering)')
ax.set_ylabel('CHL1 contact frequency')
ax.set_title('Cholesterol contacts per receptor residue')
ax.axhline(y=0.9, color='grey', linestyle='--', alpha=0.4, label='0.9 threshold')
for boundary in [183.5]:
    ax.axvline(x=boundary, color='grey', linestyle=':', alpha=0.4)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(f'{OUT}/cholesterol_contacts.png', dpi=150)
plt.close()
print(f"\nPlot: {OUT}/cholesterol_contacts.png")

# ── Save CSV ──────────────────────────────────────────────────

rows = []
for (resid, segid, species), freq in decoded.items():
    rn = resname_lookup.get((resid, segid), '?')
    lit = current_to_lit(resid, segid)
    rows.append({
        'resid': resid, 'segid': segid, 'resname': rn,
        'lit_resid': lit, 'lipid_species': species,
        'contact_freq': round(freq, 4),
    })

df = pd.DataFrame(rows)
df.sort_values(['segid', 'resid', 'lipid_species'], inplace=True)
df.to_csv(f'{OUT}/contact_data.csv', index=False)
print(f"\nCSV: {OUT}/contact_data.csv ({len(df)} rows)")
