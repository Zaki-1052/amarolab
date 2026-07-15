# wisp-analysis/scripts/verify_analysis.py
"""End-to-end verification of Phase 3 analysis orchestration.

Exercises single-condition analysis, differential comparison, CSV
round-tripping, and summary output against Gi WISP data.
"""

import sys
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'wisp-analysis'))

import yaml
import numpy as np
from core.chain_table import ChainTable
from core.parser import Parser
from core.filter import Filter
from analysis.single import analyze_run, _save_csv, _load_csv, _print_summary
from analysis.differential import compare_edges, compare_nodes


def load_config():
    config_path = ROOT / 'wisp-analysis' / 'config' / 'gi_9ll8.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)


def find_run(config, name):
    return [r for r in config['wisp_runs'] if r['name'] == name][0]


def test_analyze_run1(config, ct, tmpdir):
    print("=== Single-Condition Analysis (run1) ===")

    run1 = find_run(config, 'run1_d155_to_a5')
    out = os.path.join(tmpdir, 'gi_run1')

    dfs = analyze_run(config, ct, run1, cutoff_p=10, output_dir=out)

    assert set(dfs.keys()) == {'node_usage', 'edge_usage', 'hub_nodes', 'critical_edges'}
    print("  Return dict has all 4 usage types ✓")

    assert len(dfs['node_usage']) == 901
    assert len(dfs['edge_usage']) == 4182
    assert len(dfs['hub_nodes']) == 18
    assert len(dfs['critical_edges']) == 11
    print(f"  DataFrame row counts: node=901, edge=4182, hub=18, crit=11 ✓")

    csv_dir = os.path.join(out, 'csv')
    expected_csvs = [
        'node_usage_all.csv', 'edge_usage_all.csv',
        'hub_nodes_all.csv', 'critical_edges_all.csv',
        'node_usage_top10.csv', 'edge_usage_top10.csv',
    ]
    for csv_name in expected_csvs:
        csv_path = os.path.join(csv_dir, csv_name)
        assert os.path.exists(csv_path), f"CSV not found: {csv_path}"
    print(f"  All {len(expected_csvs)} CSV files created ✓")

    net_png = os.path.join(out, 'networkx', 'figures', 'gi_top10_2D-network.png')
    assert os.path.exists(net_png), f"2D network PNG not found: {net_png}"
    print(f"  2D network PNG created ✓")

    fig_dir = os.path.join(out, 'figures')
    profile_png = os.path.join(fig_dir, 'gi_node_weight_profile.png')
    assert os.path.exists(profile_png), f"Weight profile PNG not found: {profile_png}"
    print(f"  Weight profile PNG created ✓")

    top_png = os.path.join(fig_dir, 'top20_residues_per_chain.png')
    assert os.path.exists(top_png), f"Top residues PNG not found: {top_png}"
    print(f"  Top residues PNG created ✓")

    occ_files = [f for f in os.listdir(fig_dir) if f.startswith('occurrences_')]
    assert len(occ_files) > 0, "No occurrence PNGs created"
    print(f"  Residue occurrence PNGs created ({len(occ_files)} files) ✓")

    cxc_dir = os.path.join(out, 'chimerax')
    cxc_files = [f for f in os.listdir(cxc_dir) if f.endswith('.cxc')]
    assert len(cxc_files) == 1, f"Expected 1 CXC file, found {len(cxc_files)}"
    print(f"  ChimeraX CXC created ✓")

    return dfs


def test_csv_roundtrip(config, ct, tmpdir):
    print("\n=== CSV Round-Trip ===")

    run1 = find_run(config, 'run1_d155_to_a5')
    p = Parser('gi', 'edge_usage')
    path = ROOT / run1['output_dir'] / 'edge_usage.txt'
    records = p.parse_txt(path)
    df = p.build_df(records, ct)

    rt_dir = os.path.join(tmpdir, 'roundtrip')
    _save_csv(df, 'test_edges', rt_dir)

    loaded = _load_csv(os.path.join(rt_dir, 'csv', 'test_edges.csv'))
    assert len(loaded) == len(df), f"Row count mismatch: {len(loaded)} vs {len(df)}"

    row = loaded.iloc[0]
    assert isinstance(row['edge'], tuple), f"edge column not restored to tuple: {type(row['edge'])}"
    assert isinstance(row['revised_edge'], tuple), f"revised_edge not restored: {type(row['revised_edge'])}"
    assert isinstance(row['chain'], tuple), f"chain not restored to tuple: {type(row['chain'])}"
    print("  CSV round-trip preserves tuple columns (edge, revised_edge, chain) ✓")


def test_differential_self_compare(config, ct, tmpdir):
    print("\n=== Differential: Self-Comparison ===")

    run1 = find_run(config, 'run1_d155_to_a5')
    base = ROOT / run1['output_dir']

    edge_p = Parser('gi', 'edge_usage')
    edge_df = edge_p.build_df(edge_p.parse_txt(base / 'edge_usage.txt'), ct)
    f = Filter()
    edge_sorted = f.filter_df(edge_df, condition='gi')

    merged_edges = compare_edges(edge_sorted, edge_sorted)
    assert merged_edges['is_common'].all(), "Self-comparison should have all edges common"
    assert not merged_edges['is_unique'].any(), "Self-comparison should have no unique edges"
    print(f"  compare_edges self-compare: all {len(merged_edges)} edges common, none unique ✓")

    node_p = Parser('gi', 'node_usage')
    node_df = node_p.build_df(node_p.parse_txt(base / 'node_usage.txt'), ct)
    node_sorted = f.filter_df(node_df, condition='gi')

    merged_nodes = compare_nodes(node_sorted, node_sorted)
    assert merged_nodes['is_common'].all(), "Self-comparison should have all nodes common"

    ratios = merged_nodes['weight_ratio'].dropna()
    assert np.allclose(ratios, 1.0), f"Self-comparison weight ratios should be 1.0, got {ratios.unique()}"
    print(f"  compare_nodes self-compare: all {len(merged_nodes)} nodes common, ratio=1.0 ✓")


def test_differential_chain_filter(config, ct, tmpdir):
    print("\n=== Differential: Chain Filter ===")

    run1 = find_run(config, 'run1_d155_to_a5')
    base = ROOT / run1['output_dir']

    edge_p = Parser('gi', 'edge_usage')
    edge_df = edge_p.build_df(edge_p.parse_txt(base / 'edge_usage.txt'), ct)
    f = Filter()
    edge_sorted = f.filter_df(edge_df, condition='gi')

    merged_r = compare_edges(edge_sorted, edge_sorted, filter_chains=['R'])
    for _, row in merged_r.iterrows():
        pair = row['chain']
        assert 'R' in pair, f"Filtered edge has no R chain: {pair}"
    print(f"  compare_edges(filter_chains=['R']): all {len(merged_r)} edges involve chain R ✓")

    node_p = Parser('gi', 'node_usage')
    node_df = node_p.build_df(node_p.parse_txt(base / 'node_usage.txt'), ct)
    node_sorted = f.filter_df(node_df, condition='gi')

    merged_r_nodes = compare_nodes(node_sorted, node_sorted, filter_chains=['R'])
    assert (merged_r_nodes['chain'] == 'R').all(), "Filtered nodes should all be chain R"
    r_start, r_end = ct.chain_node_range('R')
    expected_r_count = r_end - r_start + 1
    assert len(merged_r_nodes) == expected_r_count, \
        f"Filtered node count {len(merged_r_nodes)} != R chain size {expected_r_count}"
    print(f"  compare_nodes(filter_chains=['R']): {len(merged_r_nodes)} nodes, all chain R ✓")


def test_analyze_run2(config, ct, tmpdir):
    print("\n=== Single-Condition Analysis (run2) ===")

    run2 = find_run(config, 'run2_d155_to_dry')
    out = os.path.join(tmpdir, 'gi_run2')

    dfs = analyze_run(config, ct, run2, cutoff_p=10, output_dir=out)

    assert len(dfs['node_usage']) == 901
    assert len(dfs['edge_usage']) == 4182
    print(f"  run2 row counts: node=901, edge=4182 ✓")

    csv_dir = os.path.join(out, 'csv')
    assert os.path.exists(os.path.join(csv_dir, 'edge_usage_top10.csv'))
    print(f"  run2 CSV files created ✓")


def test_summary(config, ct):
    print("\n=== Summary Output ===")

    run1 = find_run(config, 'run1_d155_to_a5')
    base = ROOT / run1['output_dir']

    dfs = {}
    for usage in ('hub_nodes', 'edge_usage', 'critical_edges'):
        p = Parser('gi', usage)
        records = p.parse_txt(base / f'{usage}.txt')
        dfs[usage] = p.build_df(records, ct)

    _print_summary(dfs, ct, config)

    top_hub = dfs['hub_nodes'].iloc[0]
    assert top_hub['node'] == 499, f"Top hub is node {top_hub['node']}, expected 499"
    assert top_hub['revised_node'] == 'A:F88'
    print("  Top hub is A:F88 (node 499) ✓")


def main():
    config = load_config()
    ct = ChainTable(config['chains'])

    tmpdir = tempfile.mkdtemp(prefix='wisp_analysis_verify_')
    print(f"Output directory: {tmpdir}\n")

    dfs = test_analyze_run1(config, ct, tmpdir)
    test_csv_roundtrip(config, ct, tmpdir)
    test_differential_self_compare(config, ct, tmpdir)
    test_differential_chain_filter(config, ct, tmpdir)
    test_analyze_run2(config, ct, tmpdir)
    test_summary(config, ct)

    print("\n" + "=" * 50)
    print("ALL CHECKS PASSED")
    print("=" * 50)
    print(f"\nAnalysis output in: {tmpdir}")


if __name__ == '__main__':
    main()
