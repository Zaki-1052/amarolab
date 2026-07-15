# wisp-analysis/main.py
"""WISP allosteric network analysis pipeline for multi-chain protein complexes.

Usage:
    python wisp-analysis/main.py analyze <config.yaml> --run <name> --output <dir>
    python wisp-analysis/main.py compare <config.yaml> --target-run <name> --ref-run <name> --output <dir>
"""

import argparse
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import yaml
from core.chain_table import ChainTable
from analysis.single import analyze_run
from analysis.differential import compare_edges, compare_nodes
from analysis.single import _save_csv
from core.parser import Parser
from core.filter import Filter
from viz.plotting import plot_weight_diff


def _load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def _find_run(config, run_name):
    for run in config['wisp_runs']:
        if run['name'] == run_name:
            return run
    available = [r['name'] for r in config['wisp_runs']]
    print(f"Error: run '{run_name}' not found. Available: {available}")
    sys.exit(1)


def cmd_analyze(args):
    config = _load_config(args.config)
    ct = ChainTable(config['chains'])
    run_config = _find_run(config, args.run)
    analyze_run(config, ct, run_config, cutoff_p=args.cutoff, output_dir=args.output)


def cmd_compare(args):
    config = _load_config(args.config)
    ct = ChainTable(config['chains'])

    if args.ref_config:
        ref_config = _load_config(args.ref_config)
        ref_ct = ChainTable(ref_config['chains'])
    else:
        ref_config = config
        ref_ct = ct

    target_run = _find_run(config, args.target_run)
    ref_run = _find_run(ref_config, args.ref_run)

    target_condition = target_run['condition']
    ref_condition = ref_run['condition']

    filter_chains = args.chains if args.chains else None
    cross_system = args.ref_config is not None

    for usage in ('edge_usage', 'node_usage'):
        target_parser = Parser(target_condition, usage)
        target_path = os.path.join(target_run['output_dir'], f'{usage}.txt')
        target_records = target_parser.parse_txt(target_path)
        target_df = target_parser.build_df(target_records, ct)

        ref_parser = Parser(ref_condition, usage)
        ref_path = os.path.join(ref_run['output_dir'], f'{usage}.txt')
        ref_records = ref_parser.parse_txt(ref_path)
        ref_df = ref_parser.build_df(ref_records, ref_ct)

        if usage == 'edge_usage':
            f = Filter()
            target_sorted = f.filter_df(target_df, condition=target_condition)
            ref_sorted = f.filter_df(ref_df, condition=ref_condition)
            edge_match = 'lit_edge' if cross_system else None
            merged = compare_edges(target_sorted, ref_sorted,
                                   filter_chains=filter_chains,
                                   match_col=edge_match)
        else:
            f = Filter()
            target_sorted = f.filter_df(target_df, condition=target_condition)
            ref_sorted = f.filter_df(ref_df, condition=ref_condition)
            node_match = 'lit_node' if cross_system else None
            merged = compare_nodes(target_sorted, ref_sorted,
                                   filter_chains=filter_chains,
                                   match_col=node_match)

        os.makedirs(args.output, exist_ok=True)
        _save_csv(merged, f'{usage}_diff_{target_condition}_vs_{ref_condition}', args.output)

        if usage == 'node_usage':
            combined = pd.concat([target_df, ref_df], ignore_index=True)
            fig_dir = os.path.join(args.output, 'figures')
            label_col = 'lit_node' if cross_system else None
            plot_weight_diff(
                combined, ct, config, ref_condition=ref_condition,
                output_path=fig_dir, label_col=label_col,
            )

    print(f"Differential analysis complete. Output in: {args.output}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command')
    sub.required = True

    analyze = sub.add_parser('analyze', help='Analyze a single WISP run')
    analyze.add_argument('config', help='Path to system YAML config file')
    analyze.add_argument('--run', required=True, help='WISP run name (from config)')
    analyze.add_argument('--output', required=True, help='Output directory')
    analyze.add_argument('--cutoff', type=int, default=10,
                         help='Percentage cutoff (default: 10)')
    analyze.set_defaults(func=cmd_analyze)

    compare = sub.add_parser('compare', help='Compare two conditions')
    compare.add_argument('config', help='Path to YAML config')
    compare.add_argument('--target-run', required=True, help='Target run name')
    compare.add_argument('--ref-run', required=True, help='Reference run name')
    compare.add_argument('--output', required=True, help='Output directory')
    compare.add_argument('--chains', nargs='+',
                         help='Restrict comparison to these chains')
    compare.add_argument('--ref-config',
                         help='Separate config for the reference condition')
    compare.set_defaults(func=cmd_compare)

    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
