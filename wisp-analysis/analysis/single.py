# wisp-analysis/analysis/single.py
"""Single-condition WISP analysis orchestrator.

Parses all four WISP output file types, applies cutoff filtering,
generates CSV exports, plots, 2D network diagrams, and ChimeraX scripts.
"""

import ast
import os

import pandas as pd

from core.parser import Parser
from core.filter import Filter
from viz.networks import process_df_to_network
from viz.plotting import (
    plot_weight_profile, plot_top_residues, plot_residue_occurrences,
)
from viz.chimerax import WispVisualizer


USAGE_TYPES = ['node_usage', 'edge_usage', 'hub_nodes', 'critical_edges']
FILTERABLE = {'node_usage', 'edge_usage'}


def _save_csv(df, name, output_dir):
    csv_dir = os.path.join(output_dir, 'csv')
    os.makedirs(csv_dir, exist_ok=True)
    df.to_csv(os.path.join(csv_dir, f'{name}.csv'), index=False)


def _load_csv(path):
    df = pd.read_csv(path)
    for col in ('edge', 'revised_edge', 'chain'):
        if col in df.columns:
            df[col] = df[col].apply(ast.literal_eval)
    return df


def _print_summary(dfs, chain_table, config):
    sys_name = config.get('system', {}).get('name', '')
    print(f"\n{'=' * 60}")
    print(f"  {sys_name} — Analysis Summary")
    print(f"{'=' * 60}")

    if 'hub_nodes' in dfs:
        hub_df = dfs['hub_nodes']
        print(f"\n  Hub Nodes ({len(hub_df)} total):")
        for cid in chain_table.chain_ids:
            if cid == 'L':
                continue
            chain_hubs = hub_df[hub_df['chain'] == cid].head(5)
            if len(chain_hubs) == 0:
                continue
            identity = cid
            for c in config['chains']:
                if c['id'] == cid:
                    identity = c.get('identity', cid)
                    break
            print(f"    Chain {cid} ({identity}): {len(hub_df[hub_df['chain'] == cid])} hubs")
            for _, row in chain_hubs.iterrows():
                print(f"      {row['revised_node']:>12}  weight={row['weight']:>8}")

    if 'edge_usage' in dfs:
        edge_df = dfs['edge_usage']
        print(f"\n  Edge Density:")
        chain_pairs = {}
        for _, row in edge_df.iterrows():
            pair = row['chain'] if isinstance(row['chain'], tuple) else ('?', '?')
            key = tuple(sorted(pair))
            chain_pairs[key] = chain_pairs.get(key, 0) + 1
        for pair, count in sorted(chain_pairs.items(), key=lambda x: -x[1]):
            label = f"{pair[0]}-{pair[1]}"
            print(f"    {label:>5}: {count:>5} edges")

        interchain = edge_df[edge_df['interchain']].nlargest(10, 'weight')
        if len(interchain) > 0:
            print(f"\n  Top 10 Interchain Edges:")
            for _, row in interchain.iterrows():
                print(f"    {str(row['revised_edge']):>30}  weight={row['weight']:>8}")

    if 'critical_edges' in dfs:
        crit_df = dfs['critical_edges']
        print(f"\n  Critical Edges ({len(crit_df)}):")
        for _, row in crit_df.head(5).iterrows():
            ic = " [interchain]" if row.get('interchain', False) else ""
            print(f"    {str(row['revised_edge']):>30}  weight={row['weight']:>8}{ic}")

    print(f"\n{'=' * 60}\n")


def analyze_run(config, chain_table, run_config, cutoff_p=10, output_dir=None):
    """Run the full single-condition analysis pipeline for one WISP run.

    Returns a dict of full (uncut) DataFrames keyed by usage type.
    """
    condition = run_config['condition']
    wisp_dir = run_config['output_dir']

    if output_dir is None:
        output_dir = os.path.join('results', run_config['name'])
    output_dir = str(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    dfs = {}
    top_dfs = {}

    for usage in USAGE_TYPES:
        txt_path = os.path.join(wisp_dir, f'{usage}.txt')
        parser = Parser(condition, usage)
        records = parser.parse_txt(txt_path)
        df = parser.build_df(records, chain_table)
        dfs[usage] = df
        _save_csv(df, f'{usage}_all', output_dir)

        if usage in FILTERABLE:
            f = Filter()
            sorted_df = f.filter_df(df, condition=condition)
            top_df = f.cutoff_df(sorted_df, how='cutoff', cutoff_p=cutoff_p)
            top_dfs[usage] = top_df
            _save_csv(top_df, f'{usage}_top{cutoff_p}', output_dir)

    _print_summary(dfs, chain_table, config)

    fig_dir = os.path.join(output_dir, 'figures')

    if 'edge_usage' in top_dfs:
        top_edge = top_dfs['edge_usage']
        process_df_to_network(
            top_edge, chain_table, config, condition,
            output_path=output_dir, cutoff=cutoff_p,
        )

        plot_top_residues(
            top_edge, chain_table, config,
            top_n=20, output_path=fig_dir,
        )

        for key_name, sel_dict in config.get('key_residues', {}).items():
            plot_residue_occurrences(
                top_edge, chain_table, config, sel_dict,
                output_path=fig_dir,
            )

    if 'node_usage' in top_dfs:
        top_node = top_dfs['node_usage']
        plot_weight_profile(
            top_node, chain_table, config,
            condition=condition, output_path=fig_dir,
        )

    if 'edge_usage' in top_dfs:
        top_edge = top_dfs['edge_usage']
        viz = WispVisualizer(chain_table, config, condition, cutoff=cutoff_p)
        viz.color_domains()
        viz.show_cylinder(top_edge)
        for key_name in config.get('key_residues', {}):
            viz.show_key_residues(key_name)
        viz.show_ligand()
        viz.visualize_conserved(top_edge)
        viz.write_cxc(os.path.join(output_dir, 'chimerax'))

    return dfs
