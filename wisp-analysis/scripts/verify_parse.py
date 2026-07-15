# wisp-analysis/scripts/verify_parse.py
"""End-to-end verification of Phase 1 foundation.

Validates ChainTable construction, Parser +1 fix, structure cross-check,
and Filter basics against the Gi complex WISP output.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'wisp-analysis'))

import yaml
from core.chain_table import ChainTable
from core.parser import Parser
from core.filter import Filter


def load_config():
    config_path = ROOT / 'wisp-analysis' / 'config' / 'gi_9ll8.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)


def test_chain_table(ct):
    print("=== ChainTable ===")

    assert ct.total_nodes == 901, f"total_nodes={ct.total_nodes}, expected 901"
    print(f"  total_nodes: {ct.total_nodes} ✓")

    assert ct.chain_ids == ['B', 'G', 'A', 'R', 'L']
    print(f"  chain_ids: {ct.chain_ids} ✓")

    # Top hub node: 0-idx 498 -> 1-idx 499 = Gai1 PHE88 (literature F215)
    assert ct.node_to_chain(499) == 'A'
    assert ct.node_to_resid(499) == 88
    assert ct.node_to_resname(499) == 'F'
    assert ct.node_to_label(499) == 'A:F88'
    assert ct.node_to_domain(499) == 'ras_domain'
    print("  top hub node 499 -> A:F88 (ras_domain) ✓")

    # Chain boundaries
    assert ct.node_to_chain(340) == 'B'
    assert ct.node_to_chain(341) == 'G'
    assert ct.node_to_chain(411) == 'G'
    assert ct.node_to_chain(412) == 'A'
    assert ct.node_to_chain(638) == 'A'
    assert ct.node_to_chain(639) == 'R'
    assert ct.node_to_chain(900) == 'R'
    assert ct.node_to_chain(901) == 'L'
    print("  chain boundaries (B/G, G/A, A/R, R/L) ✓")

    # DRY motif: chain R starts at node 639, resid 94 -> node 639+(94-1)=732
    assert ct.node_to_label(732) == 'R:R94'
    assert ct.is_conserved(731)  # D3.49
    assert ct.is_conserved(732)  # R3.50
    assert ct.is_conserved(733)  # Y3.51
    assert ct.node_to_domain(732) == 'TM3'
    print("  DRY motif (731-733) -> R:D93, R:R94, R:Y95 (TM3, conserved) ✓")

    # NPxxY motif: resids 245-249 -> nodes 639+(245-1)=883 through 887
    assert ct.node_to_label(883) == 'R:N245'
    assert ct.node_to_label(887) == 'R:Y249'
    assert all(ct.is_conserved(n) for n in range(883, 888))
    assert ct.node_to_domain(887) == 'TM7'
    print("  NPxxY motif (883-887) -> R:N245..R:Y249 (TM7, conserved) ✓")

    # Toggle switch: resid 205 -> node 639+(205-1)=843
    assert ct.node_to_label(843) == 'R:W205'
    assert ct.is_conserved(843)
    assert ct.node_to_domain(843) == 'TM6'
    print("  toggle switch W6.48 (843) -> R:W205 (TM6, conserved) ✓")

    # Source/sink from WISP run 1
    # D155 source: resid 76 -> node 639+(76-1)=714
    assert ct.node_to_label(714) == 'R:D76'
    # F354 sink: chain A resid 227 -> node 412+(227-1)=638
    assert ct.node_to_label(638) == 'A:F227'
    print("  WISP source R:D76 (714), sink A:F227 (638) ✓")

    # Top critical edge: 0-idx 623->738, 1-idx 624->739
    assert ct.edge_chains(624, 739) == ('A', 'R')
    assert ct.is_interchain(624, 739)
    assert ct.is_interdomain(624, 739)
    print("  top critical edge (624, 739) -> (A, R) interchain ✓")

    # Chain ranges
    assert ct.chain_node_range('B') == (1, 340)
    assert ct.chain_node_range('R') == (639, 900)
    print("  chain_node_range B=(1,340), R=(639,900) ✓")


def test_structure_verification(ct, config):
    print("\n=== Structure Verification ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    pdb_path = ROOT / run1['output_dir'] / 'average_structure.pdb'
    mismatches = ct.verify_against_structure(pdb_path)
    assert len(mismatches) == 0, f"Structure mismatches: {mismatches}"
    print(f"  all {ct.total_nodes} nodes match average_structure.pdb ✓")


def test_parser_node_usage(ct, config):
    print("\n=== Parser: node_usage ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    path = ROOT / run1['output_dir'] / 'node_usage.txt'

    p = Parser('gi', 'node_usage')
    records = p.parse_txt(path)
    assert len(records) == 901, f"records={len(records)}, expected 901"

    df = p.build_df(records, ct)
    assert len(df) == 901
    assert list(df.columns) == ['condition', 'chain', 'node', 'revised_node',
                                 'domain', 'conserved', 'weight', 'normalized_weight']

    top = df.nlargest(1, 'weight').iloc[0]
    assert top['node'] == 499
    assert top['revised_node'] == 'A:F88'
    assert top['normalized_weight'] == 1.0
    print(f"  {len(df)} rows, top node: {top['revised_node']} (weight={top['weight']}) ✓")


def test_parser_hub_nodes(ct, config):
    print("\n=== Parser: hub_nodes (+1 fix) ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    path = ROOT / run1['output_dir'] / 'hub_nodes.txt'

    p = Parser('gi', 'hub_nodes')
    records = p.parse_txt(path)
    assert len(records) == 18

    df = p.build_df(records, ct)
    assert len(df) == 18
    assert 'weight' in df.columns

    top = df.iloc[0]
    assert top['node'] == 499, f"top hub node={top['node']}, expected 499 (raw file says 498, +1=499)"
    assert top['revised_node'] == 'A:F88'
    assert top['weight'] == 367604
    print(f"  {len(df)} hubs, top: node={top['node']} -> {top['revised_node']} (weight={top['weight']}) ✓")
    print(f"  +1 fix verified: raw 498 -> parsed 499 ✓")


def test_parser_edge_usage(ct, config):
    print("\n=== Parser: edge_usage ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    path = ROOT / run1['output_dir'] / 'edge_usage.txt'

    p = Parser('gi', 'edge_usage')
    records = p.parse_txt(path)
    assert len(records) == 8364

    df = p.build_df(records, ct)
    assert len(df) == 4182, f"deduped edges={len(df)}, expected 4182 (8364/2)"
    assert 'weight_chx' in df.columns

    top = df.nlargest(1, 'weight').iloc[0]
    assert top['interchain'] == True
    print(f"  {len(df)} edges (deduped from {len(records)}), top: {top['revised_edge']} ✓")


def test_parser_critical_edges(ct, config):
    print("\n=== Parser: critical_edges (+1 fix) ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    path = ROOT / run1['output_dir'] / 'critical_edges.txt'

    p = Parser('gi', 'critical_edges')
    records = p.parse_txt(path)
    assert len(records) == 22

    df = p.build_df(records, ct)
    assert len(df) == 11, f"deduped critical edges={len(df)}, expected 11 (22/2)"
    assert 'weight' in df.columns

    top = df.iloc[0]
    assert top['source'] == 624
    assert top['sink'] == 739
    assert ct.edge_chains(624, 739) == ('A', 'R')
    print(f"  {len(df)} critical edges (deduped from {len(records)}), top: {top['revised_edge']} ✓")
    print(f"  +1 fix verified: raw (623,738) -> parsed (624,739) ✓")


def test_filter(ct, config):
    print("\n=== Filter ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    path = ROOT / run1['output_dir'] / 'node_usage.txt'

    p = Parser('gi', 'node_usage')
    records = p.parse_txt(path)
    df = p.build_df(records, ct)

    f = Filter()

    filtered = f.filter_df(df, condition='gi')
    assert len(filtered) == 901
    assert filtered.iloc[0]['normalized_weight'] >= filtered.iloc[-1]['normalized_weight']
    print(f"  filter_df(condition='gi'): {len(filtered)} rows (sorted desc) ✓")

    cutoff = f.cutoff_df(filtered, how='cutoff', cutoff_p=10)
    expected = int(901 * 0.10)
    assert len(cutoff) == expected, f"cutoff rows={len(cutoff)}, expected {expected}"
    print(f"  cutoff_df(10%): {len(cutoff)} rows ✓")

    cutoff_mean = f.cutoff_df(filtered, how='mean', mult=1)
    assert len(cutoff_mean) < len(filtered)
    print(f"  cutoff_df(mean+1*std): {len(cutoff_mean)} rows ✓")


def test_run2(ct, config):
    print("\n=== Run 2 (D155 -> DRY) ===")
    run2 = [r for r in config['wisp_runs'] if r['name'] == 'run2_d155_to_dry'][0]
    path = ROOT / run2['output_dir'] / 'node_usage.txt'

    p = Parser('gi', 'node_usage')
    records = p.parse_txt(path)
    df = p.build_df(records, ct)
    assert len(df) == 901
    print(f"  run2 node_usage: {len(df)} rows ✓")

    top = df.nlargest(5, 'weight')
    print(f"  top 5 nodes:")
    for _, row in top.iterrows():
        print(f"    {row['revised_node']:>10} ({row['chain']}, {row['domain']}) weight={row['weight']}")


def print_top_hubs(ct, config):
    print("\n=== Top 10 Hub Nodes ===")
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    path = ROOT / run1['output_dir'] / 'hub_nodes.txt'

    p = Parser('gi', 'hub_nodes')
    records = p.parse_txt(path)
    df = p.build_df(records, ct)

    print(f"  {'Node':>6}  {'Label':>12}  {'Chain':>5}  {'Domain':<15}  {'Conserved':>9}  {'Usage':>8}")
    print(f"  {'─'*6}  {'─'*12}  {'─'*5}  {'─'*15}  {'─'*9}  {'─'*8}")
    for _, row in df.head(10).iterrows():
        print(f"  {row['node']:>6}  {row['revised_node']:>12}  {row['chain']:>5}"
              f"  {str(row['domain']):<15}  {str(row['conserved']):>9}  {row['weight']:>8}")


def main():
    config = load_config()
    ct = ChainTable(config['chains'])

    test_chain_table(ct)
    test_structure_verification(ct, config)
    test_parser_node_usage(ct, config)
    test_parser_hub_nodes(ct, config)
    test_parser_edge_usage(ct, config)
    test_parser_critical_edges(ct, config)
    test_filter(ct, config)
    test_run2(ct, config)
    print_top_hubs(ct, config)

    print("\n" + "=" * 50)
    print("ALL CHECKS PASSED")
    print("=" * 50)


if __name__ == '__main__':
    main()
