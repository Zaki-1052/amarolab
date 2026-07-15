# wisp-analysis/scripts/verify_phase4.py
"""Phase 4 verification: Gq config, literature numbering, cross-system differential."""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import yaml
from core.chain_table import ChainTable
from core.parser import Parser
from core.filter import Filter
from analysis.differential import compare_edges, compare_nodes

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}  {detail}")


print("=" * 60)
print("Phase 4 Verification")
print("=" * 60)

# -------------------------------------------------------------------
print("\n--- 1. Gq ChainTable construction ---")
with open(ROOT / 'config' / 'gq_9as8.yaml') as f:
    gq_config = yaml.safe_load(f)
gq_ct = ChainTable(gq_config['chains'])

check("Gq total nodes", gq_ct.total_nodes == 922, f"got {gq_ct.total_nodes}")
check("Gq chain IDs", gq_ct.chain_ids == ['R', 'A', 'B', 'G', 'L'])
check("Gq chain R range", gq_ct.chain_node_range('R') == (1, 266))
check("Gq chain A range", gq_ct.chain_node_range('A') == (267, 512))
check("Gq chain B range", gq_ct.chain_node_range('B') == (513, 850))
check("Gq chain G range", gq_ct.chain_node_range('G') == (851, 921))
check("Gq chain L range", gq_ct.chain_node_range('L') == (922, 922))

# -------------------------------------------------------------------
print("\n--- 2. Gq landmark residues ---")
check("Gq D155 (R:D77)", gq_ct.node_to_label(77) == "R:D77")
check("Gq R173 DRY (R:R95)", gq_ct.node_to_label(95) == "R:R95")
check("Gq W336 toggle (R:W209)", gq_ct.node_to_label(209) == "R:W209")
check("Gq N376 NPxxY (R:N249)", gq_ct.node_to_label(249) == "R:N249")
check("Gq V246 a5 tip", gq_ct.node_to_label(512) == "A:V246")
check("Gq psilocin", gq_ct.node_to_resname(922) == "LIG")

# -------------------------------------------------------------------
print("\n--- 3. Literature numbering ---")
with open(ROOT / 'config' / 'gi_9ll8.yaml') as f:
    gi_config = yaml.safe_load(f)
gi_ct = ChainTable(gi_config['chains'])

landmarks = [
    ('D155', 'R', 76, 77),
    ('R173', 'R', 94, 95),
    ('W336', 'R', 205, 209),
    ('N376', 'R', 245, 249),
]

for lit_name, chain, gi_resid, gq_resid in landmarks:
    gi_node = gi_ct.chain_node_range(chain)[0] + gi_resid - 1
    gq_node = gq_ct.chain_node_range(chain)[0] + gq_resid - 1
    gi_lit = gi_ct.node_to_lit_label(gi_node)
    gq_lit = gq_ct.node_to_lit_label(gq_node)
    check(f"lit_label {lit_name} Gi==Gq", gi_lit == gq_lit, f"Gi={gi_lit}, Gq={gq_lit}")

# -------------------------------------------------------------------
print("\n--- 4. Gi ChainTable backward compatibility ---")
check("Gi total nodes", gi_ct.total_nodes == 901)
check("Gi D155 label", gi_ct.node_to_label(714) == "R:D76")
check("Gi D155 lit_label", gi_ct.node_to_lit_label(714) == "R:D155")

# Chain without literature offset (Gg2, offset=null) falls back to resid
gi_gg2_start = gi_ct.chain_node_range('G')[0]
check("Gi Gg2 lit_label fallback", gi_ct.node_to_lit_label(gi_gg2_start) == gi_ct.node_to_label(gi_gg2_start))

# -------------------------------------------------------------------
print("\n--- 5. Parser lit columns (Gi run1 data) ---")
p = Parser('gi', 'node_usage')
records = p.parse_txt(str(Path('new-Gi/analysis/wisp_run1_d155_to_a5/node_usage.txt')))
df = p.build_df(records, gi_ct)

check("node_usage has lit_node column", 'lit_node' in df.columns)
d155_row = df[df['node'] == 714]
check("D155 lit_node = R:D155", d155_row['lit_node'].values[0] == 'R:D155')

pe = Parser('gi', 'edge_usage')
erecs = pe.parse_txt(str(Path('new-Gi/analysis/wisp_run1_d155_to_a5/edge_usage.txt')))
edf = pe.build_df(erecs, gi_ct)

check("edge_usage has lit_edge column", 'lit_edge' in edf.columns)
check("edge_usage row count unchanged", len(edf) == 4182)

# -------------------------------------------------------------------
print("\n--- 6. Same-system differential (regression) ---")
p2 = Parser('gi', 'node_usage')
records2 = p2.parse_txt(str(Path('new-Gi/analysis/wisp_run1_d155_to_a5/node_usage.txt')))
df2 = p2.build_df(records2, gi_ct)

nm = compare_nodes(df, df2, match_col=None)
check("Self-compare nodes: 901 rows", len(nm) == 901)
check("Self-compare nodes: all common", nm['is_common'].all())

nm_lit = compare_nodes(df, df2, match_col='lit_node')
check("Self-compare via lit_node: 901 rows", len(nm_lit) == 901)
check("Self-compare via lit_node: all common", nm_lit['is_common'].all())

em = compare_edges(edf, edf, match_col=None)
check("Self-compare edges: 4182 rows", len(em) == 4182)
check("Self-compare edges: all common", em['is_common'].all())

em_lit = compare_edges(edf, edf, match_col='lit_edge')
check("Self-compare via lit_edge: 4182 rows", len(em_lit) == 4182)
check("Self-compare via lit_edge: all common", em_lit['is_common'].all())

# -------------------------------------------------------------------
print("\n--- 7. Cross-system mock test ---")
mock_gi = pd.DataFrame({
    'condition': ['gi'] * 3,
    'chain': ['R', 'R', 'R'],
    'node': [714, 732, 883],
    'revised_node': ['R:D76', 'R:R94', 'R:N245'],
    'lit_node': ['R:D155', 'R:R173', 'R:N376'],
    'domain': ['TM3', 'TM3', 'TM7'],
    'conserved': [True, True, True],
    'weight': [100, 200, 300],
    'normalized_weight': [0.0, 0.5, 1.0],
})
mock_gq = pd.DataFrame({
    'condition': ['gq'] * 3,
    'chain': ['R', 'R', 'R'],
    'node': [77, 95, 249],
    'revised_node': ['R:D77', 'R:R95', 'R:N249'],
    'lit_node': ['R:D155', 'R:R173', 'R:N376'],
    'domain': ['TM3', 'TM3', 'TM7'],
    'conserved': [True, True, True],
    'weight': [150, 250, 350],
    'normalized_weight': [0.0, 0.5, 1.0],
})

result = compare_nodes(mock_gi, mock_gq, match_col='lit_node')
check("Cross-system mock: 3 rows", len(result) == 3)
check("Cross-system mock: all common", result['is_common'].all())
d155_ratio = result[result['lit_node'] == 'R:D155']['weight_ratio'].values[0]
check("Cross-system mock: D155 ratio correct", np.isnan(d155_ratio),
      f"D155 normalized_weight=0 in both -> NaN ratio, got {d155_ratio}")
r173_ratio = result[result['lit_node'] == 'R:R173']['weight_ratio'].values[0]
check("Cross-system mock: R173 ratio = 1.0", r173_ratio == 1.0,
      f"got {r173_ratio}")

# Cross-system edge mock
mock_gi_e = pd.DataFrame({
    'condition': ['gi'] * 2,
    'chain': [('R', 'R'), ('R', 'A')],
    'edge': [(714, 732), (714, 624)],
    'source': [714, 714],
    'sink': [732, 624],
    'revised_edge': [('R:D76', 'R:R94'), ('R:D76', 'A:T213')],
    'lit_edge': [('R:D155', 'R:R173'), ('R:D155', 'A:T340')],
    'interdomain': [False, True],
    'interchain': [False, True],
    'conserved_edge': [True, False],
    'weight': [100, 200],
    'normalized_weight': [0.0, 1.0],
    'weight_chx': [0.2, 1.2],
})
mock_gq_e = pd.DataFrame({
    'condition': ['gq'] * 2,
    'chain': [('R', 'R'), ('R', 'R')],
    'edge': [(77, 95), (77, 209)],
    'source': [77, 77],
    'sink': [95, 209],
    'revised_edge': [('R:D77', 'R:R95'), ('R:D77', 'R:W209')],
    'lit_edge': [('R:D155', 'R:R173'), ('R:D155', 'R:W336')],
    'interdomain': [False, True],
    'interchain': [False, False],
    'conserved_edge': [True, False],
    'weight': [150, 250],
    'normalized_weight': [0.0, 1.0],
    'weight_chx': [0.2, 1.2],
})

eres = compare_edges(mock_gi_e, mock_gq_e, match_col='lit_edge')
d155_r173 = eres[eres['lit_edge'].apply(lambda x: tuple(sorted(x))) == ('R:D155', 'R:R173')]
check("Cross-system edge mock: D155-R173 is common",
      len(d155_r173) == 1 and d155_r173['is_common'].values[0])

d155_t340 = eres[eres['lit_edge'].apply(lambda x: tuple(sorted(x))) == ('A:T340', 'R:D155')]
check("Cross-system edge mock: D155-T340 is unique",
      len(d155_t340) == 1 and d155_t340['is_unique'].values[0])

# -------------------------------------------------------------------
print("\n--- 8. Chain filter ---")
filtered = compare_nodes(mock_gi, mock_gq, filter_chains=['R'], match_col='lit_node')
check("Chain R filter: all 3 rows kept", len(filtered) == 3)

# -------------------------------------------------------------------
print("\n" + "=" * 60)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("ALL CHECKS PASSED")
else:
    print("SOME CHECKS FAILED")
    sys.exit(1)
