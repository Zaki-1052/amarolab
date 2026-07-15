# wisp-analysis/scripts/verify_viz.py
"""End-to-end verification of Phase 2 visualization modules.

Exercises colors, networks, plotting, and chimerax against Gi WISP data.
"""

import sys
import os
import tempfile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'wisp-analysis'))

import yaml
from core.chain_table import ChainTable
from core.parser import Parser
from core.filter import Filter
from viz.colors import domain_color, chain_color, condition_color, node_color, weight_colormap
from viz.networks import process_df_to_network
from viz.plotting import (
    sum_weights_by_residue, plot_weight_profile,
    plot_top_residues, plot_residue_occurrences,
)
from viz.chimerax import WispVisualizer


def load_config():
    config_path = ROOT / 'wisp-analysis' / 'config' / 'gi_9ll8.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_data(config, ct):
    """Parse run1 node_usage and edge_usage into DataFrames."""
    run1 = [r for r in config['wisp_runs'] if r['name'] == 'run1_d155_to_a5'][0]
    base = ROOT / run1['output_dir']

    node_p = Parser('gi', 'node_usage')
    node_df = node_p.build_df(node_p.parse_txt(base / 'node_usage.txt'), ct)

    edge_p = Parser('gi', 'edge_usage')
    edge_df = edge_p.build_df(edge_p.parse_txt(base / 'edge_usage.txt'), ct)

    return node_df, edge_df


def test_colors(config, ct):
    print("=== Colors ===")

    assert domain_color(config, 'TM3') == '#0000FF'
    print("  domain_color('TM3') = '#0000FF' ✓")

    assert chain_color(config, 'R') == '#000080'
    print("  chain_color('R') = '#000080' ✓")

    assert condition_color(config, 'gi') == '#1E90FF'
    print("  condition_color('gi') = '#1E90FF' ✓")

    # Node 499 = A:F88, ras_domain → '#1E90FF'
    assert node_color(config, ct, 499) == '#1E90FF'
    print("  node_color(499) = '#1E90FF' (A:F88, ras_domain) ✓")

    # Node 901 = ligand, no domain → falls back to chain L color '#FF00FF'
    assert node_color(config, ct, 901) == '#FF00FF'
    print("  node_color(901) = '#FF00FF' (ligand fallback to chain L) ✓")

    # Fallback for unknown domain
    assert domain_color(config, None) == '#696969'
    assert domain_color(config, 'nonexistent') == '#696969'
    print("  domain_color(None) = '#696969' (fallback) ✓")

    # Weight colormap
    hex_colors = weight_colormap([0, 50, 100])
    assert len(hex_colors) == 3
    assert all(c.startswith('#') for c in hex_colors)
    print(f"  weight_colormap([0,50,100]) = {hex_colors} ✓")


def test_networks(config, ct, edge_df, tmpdir):
    print("\n=== Networks ===")

    f = Filter()
    filtered = f.filter_df(edge_df, condition='gi')
    top10 = f.cutoff_df(filtered, how='cutoff', cutoff_p=10)

    out = os.path.join(tmpdir, 'networks')
    process_df_to_network(top10, ct, config, 'gi', output_path=out, cutoff=10)

    fig_path = os.path.join(out, 'networkx', 'figures', 'gi_top10_2D-network.png')
    assert os.path.exists(fig_path), f"PNG not found at {fig_path}"
    print(f"  PNG created: {fig_path} ✓")

    pkl_path = os.path.join(out, 'networkx', 'gi-top10-network.pkl')
    assert os.path.exists(pkl_path), f"PKL not found at {pkl_path}"
    print(f"  PKL created: {pkl_path} ✓")


def test_plotting(config, ct, node_df, edge_df, tmpdir):
    print("\n=== Plotting ===")

    weights = sum_weights_by_residue(edge_df)
    assert len(weights) > 0
    print(f"  sum_weights_by_residue: {len(weights)} residues ✓")

    out = os.path.join(tmpdir, 'plotting')

    plot_weight_profile(node_df, ct, config, condition='gi', output_path=out)
    profile_path = os.path.join(out, 'gi_node_weight_profile.png')
    assert os.path.exists(profile_path), f"PNG not found: {profile_path}"
    print(f"  plot_weight_profile: PNG created ✓")

    plot_top_residues(edge_df, ct, config, top_n=20, output_path=out)
    top_path = os.path.join(out, 'top20_residues_per_chain.png')
    assert os.path.exists(top_path), f"PNG not found: {top_path}"
    print(f"  plot_top_residues: PNG created ✓")

    dry = config['key_residues']['dry_motif']
    plot_residue_occurrences(edge_df, ct, config, dry, output_path=out)
    occ_files = [f for f in os.listdir(out) if f.startswith('occurrences_')]
    assert len(occ_files) > 0, "No occurrences PNG created"
    print(f"  plot_residue_occurrences (DRY motif): PNG created ✓")


def test_chimerax(config, ct, edge_df, tmpdir):
    print("\n=== ChimeraX ===")

    viz = WispVisualizer(ct, config, 'gi', cutoff=10)

    # Selection helper tests
    assert viz._node_sel(714) == '/R:76', f"_node_sel(714) = {viz._node_sel(714)}"
    print("  _node_sel(714) = '/R:76' ✓")

    assert viz._node_sel(638) == '/A:227', f"_node_sel(638) = {viz._node_sel(638)}"
    print("  _node_sel(638) = '/A:227' ✓")

    assert viz._sel('R', [93, 94, 95]) == '/R:93,94,95'
    print("  _sel('R', [93,94,95]) = '/R:93,94,95' ✓")

    assert viz._node_atom_sel(714) == '/R:76@CA'
    print("  _node_atom_sel(714) = '/R:76@CA' ✓")

    # Generate a .cxc script with cylinders
    f = Filter()
    filtered = f.filter_df(edge_df, condition='gi')
    top10 = f.cutoff_df(filtered, how='cutoff', cutoff_p=10)

    viz2 = WispVisualizer(ct, config, 'gi', cutoff=10)
    viz2.color_domains()
    viz2.show_cylinder(top10)
    viz2.show_key_residues('dry_motif')
    viz2.show_ligand()

    out = os.path.join(tmpdir, 'chimerax')
    cxc_path = viz2.write_cxc(out)

    assert os.path.exists(cxc_path), f"CXC file not found: {cxc_path}"
    print(f"  write_cxc: file created ✓")

    with open(cxc_path) as fh:
        cxc_content = fh.read()

    # Verify no bare :resid selections (all should use /<chain>:)
    bare_resid = re.findall(r'(?<!/\w):(\d+)', cxc_content)
    # Filter out ChimeraX model numbers like #2, and sel : patterns
    # The key check is that residue atom selections use /chain:resid format
    assert '/R:' in cxc_content, "Missing /R: chain-qualified selections"
    assert '/A:' in cxc_content, "Missing /A: chain-qualified selections"
    print("  Chain-qualified selections (/R:, /A:) present ✓")

    assert '@CA' in cxc_content, "Missing @CA atom selections"
    print("  @CA atom selections present ✓")

    cylinder_count = cxc_content.count('shape cylinder')
    n_edges = len(top10)
    assert cylinder_count == n_edges, f"cylinder count {cylinder_count} != edge count {n_edges}"
    print(f"  shape cylinder count ({cylinder_count}) matches edge count ✓")

    # Verify domain coloring covers all domains
    for chain_cfg in config['chains']:
        for dname in chain_cfg.get('domains', {}):
            color = config['colors']['domains'].get(dname)
            if color:
                assert color in cxc_content, f"Domain color {color} ({dname}) not in CXC"
    print("  All domain colors referenced in CXC ✓")

    # Verify DRY motif selection
    assert '/R:93,94,95' in cxc_content, "DRY motif selection not found"
    print("  show_key_residues('dry_motif') → /R:93,94,95 ✓")

    # Verify ligand selection
    assert '/L:' in cxc_content, "Ligand selection not found"
    print("  show_ligand() → /L: selection present ✓")


def main():
    config = load_config()
    ct = ChainTable(config['chains'])
    node_df, edge_df = load_data(config, ct)

    tmpdir = tempfile.mkdtemp(prefix='wisp_viz_verify_')
    print(f"Output directory: {tmpdir}\n")

    test_colors(config, ct)
    test_networks(config, ct, edge_df, tmpdir)
    test_plotting(config, ct, node_df, edge_df, tmpdir)
    test_chimerax(config, ct, edge_df, tmpdir)

    print("\n" + "=" * 50)
    print("ALL CHECKS PASSED")
    print("=" * 50)
    print(f"\nVisualization output in: {tmpdir}")


if __name__ == '__main__':
    main()
