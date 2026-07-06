# new-Gi/analysis/p_crossphase.py
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

BASE = str(Path(__file__).resolve().parent)
OUT  = BASE

rmsf_df = pd.read_csv(f'{BASE}/phase3_rmsf/rmsf_data.csv')
contact_df = pd.read_csv(f'{BASE}/phase6_contacts/contact_data.csv')

# ── Build lookups ─────────────────────────────────────────────

seq = rmsf_df.sort_values('resid').reset_index(drop=True)

chl_freq = {}
for _, row in contact_df[contact_df['lipid_species'] == 'CHL1'].iterrows():
    chl_freq[(row['resid'], row['segid'])] = row['contact_freq']

total_freq = contact_df.groupby(['resid', 'segid'])['contact_freq'].sum()
total_dict = total_freq.to_dict()

# ══════════════════════════════════════════════════════════════
# Part 1: CRAC / CARC motif scan
# ══════════════════════════════════════════════════════════════

# Two contiguous blocks (don't span the ICL3 gap at PROE 183 / PROF 184)
block1 = seq[seq['resid'] <= 183].to_dict('records')   # PROE
block2 = seq[seq['resid'] >= 184].to_dict('records')   # PROF


def scan_motifs(residues):
    n = len(residues)
    crac, carc = [], []

    for i, res in enumerate(residues):
        aa = res['resname']

        # CRAC: (L/V) - X1-5 - (Y) - X1-5 - (K/R)
        if aa == 'TYR':
            for back in range(1, 6):
                if i - back < 0:
                    break
                prev = residues[i - back]
                if prev['resname'] in ('LEU', 'VAL'):
                    for fwd in range(1, 6):
                        if i + fwd >= n:
                            break
                        nxt = residues[i + fwd]
                        if nxt['resname'] in ('LYS', 'ARG'):
                            crac.append({'lv': prev, 'y': res, 'kr': nxt,
                                         'back': back, 'fwd': fwd})

        # CARC: (K/R) - X1-5 - (Y/F) - X1-5 - (L/V)
        if aa in ('TYR', 'PHE'):
            for back in range(1, 6):
                if i - back < 0:
                    break
                prev = residues[i - back]
                if prev['resname'] in ('LYS', 'ARG'):
                    for fwd in range(1, 6):
                        if i + fwd >= n:
                            break
                        nxt = residues[i + fwd]
                        if nxt['resname'] in ('LEU', 'VAL'):
                            carc.append({'kr': prev, 'yf': res, 'lv': nxt,
                                         'back': back, 'fwd': fwd})

    return crac, carc


crac1, carc1 = scan_motifs(block1)
crac2, carc2 = scan_motifs(block2)
all_crac = crac1 + crac2
all_carc = carc1 + carc2


def get_chl(r):
    return chl_freq.get((r['resid'], r['segid']), 0.0)


def one_letter(resname):
    MAP = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q',
           'GLU':'E','GLY':'G','HSD':'H','HSE':'H','HSP':'H','ILE':'I',
           'LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S',
           'THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
    return MAP.get(resname, '?')


def fmt(r):
    return f"{one_letter(r['resname'])}{r['lit_resid']}"


def dedup_crac(matches):
    best = {}
    for m in matches:
        key = m['y']['resid']
        span = m['back'] + m['fwd']
        if key not in best or span < best[key][1]:
            best[key] = (m, span)
    return [v[0] for v in sorted(best.values(), key=lambda x: x[0]['y']['resid'])]


def dedup_carc(matches):
    best = {}
    for m in matches:
        key = m['yf']['resid']
        span = m['back'] + m['fwd']
        if key not in best or span < best[key][1]:
            best[key] = (m, span)
    return [v[0] for v in sorted(best.values(), key=lambda x: x[0]['yf']['resid'])]


n_residues = len(seq)
print("=" * 65)
print("CRAC/CARC cholesterol recognition motif scan")
print("=" * 65)
print(f"Scanned {n_residues} receptor residues in 2 contiguous blocks")
print(f"  Block 1: PROE resids 1-183 (lit 80-262)")
print(f"  Block 2: PROF resids 184-262 (lit 315-393)")

# ── CRAC ──────────────────────────────────────────────────────

crac_dedup = dedup_crac(all_crac)
print(f"\nCRAC motif: (L/V)-X1-5-(Y)-X1-5-(K/R)")
print(f"Raw matches: {len(all_crac)}, unique by central Y: {len(crac_dedup)}\n")

for m in crac_dedup:
    lv, y, kr = m['lv'], m['y'], m['kr']
    lv_c, y_c, kr_c = get_chl(lv), get_chl(y), get_chl(kr)
    region = y.get('region', '?')

    snippet_resids = range(lv['resid'], kr['resid'] + 1)
    snippet = ""
    for rid in snippet_resids:
        row = seq[seq['resid'] == rid]
        if len(row) > 0:
            aa = one_letter(row.iloc[0]['resname'])
            if rid == lv['resid'] or rid == y['resid'] or rid == kr['resid']:
                snippet += f"[{aa}]"
            else:
                snippet += aa
        else:
            snippet += "?"

    tag = ""
    if lv_c >= 0.8 and y_c >= 0.8 and kr_c >= 0.8:
        tag = " *** ALL ANCHORS CHL1 >= 0.8 ***"
    elif y_c >= 0.5:
        tag = " * Y contacts CHL1 *"

    print(f"  {fmt(lv)}-X{m['back']-1}-{fmt(y)}-X{m['fwd']-1}-{fmt(kr)}  "
          f"({region})  {snippet}{tag}")
    print(f"    {fmt(lv)} CHL1={lv_c:.2f}  {fmt(y)} CHL1={y_c:.2f}  "
          f"{fmt(kr)} CHL1={kr_c:.2f}")

# ── CARC ──────────────────────────────────────────────────────

carc_dedup = dedup_carc(all_carc)
print(f"\nCARC motif (reverse): (K/R)-X1-5-(Y/F)-X1-5-(L/V)")
print(f"Raw matches: {len(all_carc)}, unique by central Y/F: {len(carc_dedup)}\n")

for m in carc_dedup:
    kr, yf, lv = m['kr'], m['yf'], m['lv']
    kr_c, yf_c, lv_c = get_chl(kr), get_chl(yf), get_chl(lv)
    region = yf.get('region', '?')

    snippet_resids = range(kr['resid'], lv['resid'] + 1)
    snippet = ""
    for rid in snippet_resids:
        row = seq[seq['resid'] == rid]
        if len(row) > 0:
            aa = one_letter(row.iloc[0]['resname'])
            if rid == kr['resid'] or rid == yf['resid'] or rid == lv['resid']:
                snippet += f"[{aa}]"
            else:
                snippet += aa
        else:
            snippet += "?"

    tag = ""
    if kr_c >= 0.8 and yf_c >= 0.8 and lv_c >= 0.8:
        tag = " *** ALL ANCHORS CHL1 >= 0.8 ***"
    elif yf_c >= 0.5:
        tag = " * Y/F contacts CHL1 *"

    print(f"  {fmt(kr)}-X{m['back']-1}-{fmt(yf)}-X{m['fwd']-1}-{fmt(lv)}  "
          f"({region})  {snippet}{tag}")
    print(f"    {fmt(kr)} CHL1={kr_c:.2f}  {fmt(yf)} CHL1={yf_c:.2f}  "
          f"{fmt(lv)} CHL1={lv_c:.2f}")

# ══════════════════════════════════════════════════════════════
# Part 2: RMSF vs contact frequency
# ══════════════════════════════════════════════════════════════

print(f"\n{'=' * 65}")
print("RMSF vs total lipid contact frequency")
print(f"{'=' * 65}")

merged = seq.copy()
merged['total_contact'] = merged.apply(
    lambda r: total_dict.get((r['resid'], r['segid']), 0.0), axis=1)
merged['chl_contact'] = merged.apply(
    lambda r: chl_freq.get((r['resid'], r['segid']), 0.0), axis=1)

has_contacts = merged[merged['total_contact'] > 0]
no_contacts = merged[merged['total_contact'] == 0]
print(f"Residues with lipid contacts: {len(has_contacts)}")
print(f"Residues with zero contacts: {len(no_contacts)}")

r_all, p_all = stats.spearmanr(merged['rmsf'], merged['total_contact'])
r_pos, p_pos = stats.spearmanr(has_contacts['rmsf'], has_contacts['total_contact'])
print(f"\nSpearman correlation (all {n_residues} residues): rho={r_all:.3f}, p={p_all:.2e}")
print(f"Spearman correlation (contacting only):  rho={r_pos:.3f}, p={p_pos:.2e}")

region_colors = {
    'TM1': '#1f77b4', 'TM2': '#1f77b4', 'TM3': '#1f77b4', 'TM4': '#1f77b4',
    'TM5': '#1f77b4', 'TM6': '#1f77b4', 'TM7': '#1f77b4',
    'ICL1': '#ff7f0e', 'ICL2': '#ff7f0e', 'ICL3c': '#ff7f0e',
    'ECL1': '#2ca02c', 'ECL2': '#2ca02c', 'ECL3': '#2ca02c',
    'H8': '#d62728', 'Ct': '#d62728',
}
region_labels = {
    '#1f77b4': 'TM helices',
    '#ff7f0e': 'ICL loops',
    '#2ca02c': 'ECL loops',
    '#d62728': 'H8 / C-term',
}

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Panel 1: RMSF vs total contacts, colored by region type
ax = axes[0]
plotted_labels = set()
for _, row in merged.iterrows():
    c = region_colors.get(row['region'], 'grey')
    lbl = region_labels.get(c, 'other')
    ax.scatter(row['total_contact'], row['rmsf'],
               color=c, alpha=0.6, s=20, edgecolors='none',
               label=lbl if lbl not in plotted_labels else '')
    plotted_labels.add(lbl)

ax.set_xlabel('Total lipid contact frequency')
ax.set_ylabel('RMSF (A)')
ax.set_title(f'RMSF vs lipid contacts (rho={r_all:.2f})')
ax.legend(fontsize=8, loc='upper right')

# Panel 2: RMSF vs cholesterol contacts specifically
r_chl, p_chl = stats.spearmanr(merged['rmsf'], merged['chl_contact'])
print(f"Spearman (RMSF vs CHL1 only):            rho={r_chl:.3f}, p={p_chl:.2e}")

ax = axes[1]
plotted_labels = set()
for _, row in merged.iterrows():
    c = region_colors.get(row['region'], 'grey')
    lbl = region_labels.get(c, 'other')
    ax.scatter(row['chl_contact'], row['rmsf'],
               color=c, alpha=0.6, s=20, edgecolors='none',
               label=lbl if lbl not in plotted_labels else '')
    plotted_labels.add(lbl)

ax.set_xlabel('CHL1 contact frequency')
ax.set_ylabel('RMSF (A)')
ax.set_title(f'RMSF vs cholesterol contacts (rho={r_chl:.2f})')
ax.legend(fontsize=8, loc='upper right')

fig.tight_layout()
fig.savefig(f'{OUT}/rmsf_vs_contacts.png', dpi=150)
plt.close()
print(f"\nPlot: {OUT}/rmsf_vs_contacts.png")

# Per-region summary
print(f"\nPer-region means:")
print(f"{'Region':<8} {'RMSF':>8} {'Contacts':>10} {'CHL1':>8} {'n':>5}")
print("-" * 43)
for region in ['TM1','TM2','TM3','ICL1','ICL2','ECL1','ECL2',
               'TM4','TM5','ICL3c','TM6','ECL3','TM7','H8','Ct']:
    sub = merged[merged['region'] == region]
    if len(sub) == 0:
        continue
    print(f"{region:<8} {sub['rmsf'].mean():>8.2f} {sub['total_contact'].mean():>10.2f} "
          f"{sub['chl_contact'].mean():>8.2f} {len(sub):>5}")
