# wisp-analysis/viz/plotting.py
"""Matplotlib-based WISP analysis plots.

Adapted from mpro-analysis/utils/plotting.py. Group A/B (homodimer)
split replaced with per-chain panels. Multi-ligand/multi-state iteration
removed — single condition per WISP run. Domain shading and conserved
residue markers added for multi-chain systems.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from viz.colors import chain_color, domain_color, node_color

DEFAULT_CHAIN_ORDER = ['R', 'A', 'B', 'G']


def sum_weights_by_residue(df):
    """Aggregate edge weights per residue (source + sink combined)."""
    source = df[['source', 'weight']].rename(columns={'source': 'node'})
    sink = df[['sink', 'weight']].rename(columns={'sink': 'node'})
    combined = pd.concat([source, sink], ignore_index=True)
    return combined.groupby('node')['weight'].sum()


def _resids_to_nodes(chain_table, chain_id, resids):
    """Convert chain-local resids to WISP 1-indexed node numbers."""
    start, _ = chain_table.chain_node_range(chain_id)
    return [start + (r - 1) for r in resids]


def _get_chain_order(chain_table, chains=None):
    """Return chain IDs in display order, skipping ligand chains."""
    if chains is not None:
        return [c for c in chains if c in chain_table.chain_ids]
    available = chain_table.chain_ids
    ordered = [c for c in DEFAULT_CHAIN_ORDER if c in available]
    for c in available:
        if c not in ordered and c != 'L':
            ordered.append(c)
    return ordered


def _get_chain_domains(config, chain_id):
    """Return the domains dict for a chain from config."""
    for chain in config['chains']:
        if chain['id'] == chain_id:
            return chain.get('domains', {})
    return {}


def plot_weight_profile(node_df, chain_table, config, condition=None,
                        chains=None, output_path=None):
    """Plot normalized node weights as per-chain line profiles.

    One subplot per chain. Domain boundaries shown as alternating shading.
    """
    if condition is not None:
        df = node_df[node_df['condition'] == condition].copy()
    else:
        df = node_df.copy()

    chain_order = _get_chain_order(chain_table, chains)
    n_chains = len(chain_order)
    fig, axes = plt.subplots(n_chains, 1, figsize=(14, 3 * n_chains), sharex=False)
    if n_chains == 1:
        axes = [axes]

    for idx, cid in enumerate(chain_order):
        ax = axes[idx]
        start, end = chain_table.chain_node_range(cid)
        chain_df = df[df['chain'] == cid].sort_values('node')

        resids = chain_df['node'].apply(chain_table.node_to_resid)
        weights = chain_df['normalized_weight']

        color = chain_color(config, cid)
        ax.plot(resids, weights, color=color, linewidth=1.2, alpha=0.9)
        ax.fill_between(resids, 0, weights, color=color, alpha=0.15)

        domains = _get_chain_domains(config, cid)
        for i, (dname, (dstart, dend)) in enumerate(domains.items()):
            dcolor = domain_color(config, dname)
            if i % 2 == 0:
                ax.axvspan(dstart, dend, alpha=0.08, color=dcolor)

        conserved_nodes = chain_df[chain_df['conserved']]['node']
        for n in conserved_nodes:
            rid = chain_table.node_to_resid(n)
            ax.axvline(rid, color='red', alpha=0.3, linewidth=0.5, linestyle='--')

        identity = cid
        for c in config['chains']:
            if c['id'] == cid:
                identity = c.get('identity', cid)
                break

        ax.set_ylabel('Normalized Weight')
        ax.set_title(f"Chain {cid} ({identity})", fontsize=10, loc='left')
        ax.set_xlim(1, chain_table.chain_node_range(cid)[1] - start + 1)

    axes[-1].set_xlabel('Residue ID (chain-local)')
    sys_name = config.get('system', {}).get('name', '')
    cond_label = condition if condition else 'all'
    fig.suptitle(f"{sys_name} — Node Usage Profile ({cond_label})", fontsize=13)
    plt.tight_layout()

    if output_path:
        os.makedirs(output_path, exist_ok=True)
        fig_path = os.path.join(output_path, f"{cond_label}_node_weight_profile.png")
        fig.savefig(fig_path, dpi=300, bbox_inches="tight")
        print(f"Saved figure to {fig_path}")

    plt.close(fig)


def plot_edge_weight_profile(edge_df, chain_table, config, condition=None,
                             chains=None, output_path=None):
    """Plot aggregated edge weights per residue as per-chain line profiles."""
    if condition is not None:
        df = edge_df[edge_df['condition'] == condition].copy()
    else:
        df = edge_df.copy()

    weight_by_node = sum_weights_by_residue(df)
    node_df = pd.DataFrame({
        'node': weight_by_node.index,
        'weight': weight_by_node.values,
    })
    w = node_df['weight']
    denom = w.max() - w.min()
    if denom == 0:
        node_df['normalized_weight'] = 0.0
    else:
        node_df['normalized_weight'] = np.round((w - w.min()) / denom, 4)
    node_df['chain'] = node_df['node'].apply(chain_table.node_to_chain)
    node_df['condition'] = condition if condition else 'all'
    node_df['conserved'] = node_df['node'].apply(chain_table.is_conserved)

    plot_weight_profile(node_df, chain_table, config, condition=node_df['condition'].iloc[0],
                        chains=chains, output_path=output_path)


def plot_top_residues(df, chain_table, config, aggfunc='sum', top_n=30,
                      per_chain=True, output_path=None):
    """Bar chart of top residues by aggregated edge weight.

    If per_chain, one subplot per chain. Otherwise single chart with
    bars colored by chain.
    """
    if 'source' in df.columns:
        agg = sum_weights_by_residue(df)
    else:
        agg = df.set_index('node')['weight']

    agg = agg.sort_values(ascending=False)

    if per_chain:
        chain_order = _get_chain_order(chain_table)
        n_chains = len(chain_order)
        fig, axes = plt.subplots(1, n_chains, figsize=(5 * n_chains, 6), sharey=True)
        if n_chains == 1:
            axes = [axes]

        for idx, cid in enumerate(chain_order):
            ax = axes[idx]
            start, end = chain_table.chain_node_range(cid)
            chain_agg = agg[(agg.index >= start) & (agg.index <= end)]
            top = chain_agg.head(top_n)

            labels = [chain_table.node_to_label(n) for n in top.index]
            colors = [node_color(config, chain_table, n) for n in top.index]
            ax.barh(range(len(top)), top.values, color=colors)
            ax.set_yticks(range(len(top)))
            ax.set_yticklabels(labels, fontsize=8)
            ax.invert_yaxis()
            ax.set_xlabel('Aggregated Weight')

            identity = cid
            for c in config['chains']:
                if c['id'] == cid:
                    identity = c.get('identity', cid)
                    break
            ax.set_title(f"Chain {cid} ({identity})", fontsize=10)

    else:
        fig, ax = plt.subplots(figsize=(10, 8))
        top = agg.head(top_n)
        labels = [chain_table.node_to_label(n) for n in top.index]
        colors = [node_color(config, chain_table, n) for n in top.index]
        ax.barh(range(len(top)), top.values, color=colors)
        ax.set_yticks(range(len(top)))
        ax.set_yticklabels(labels, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel('Aggregated Weight')

    sys_name = config.get('system', {}).get('name', '')
    fig.suptitle(f"{sys_name} — Top {top_n} Residues by Edge Weight", fontsize=13)
    plt.tight_layout()

    if output_path:
        os.makedirs(output_path, exist_ok=True)
        fig_path = os.path.join(output_path, f"top{top_n}_residues{'_per_chain' if per_chain else ''}.png")
        fig.savefig(fig_path, dpi=300, bbox_inches="tight")
        print(f"Saved figure to {fig_path}")

    plt.close(fig)


def plot_residue_occurrences(df, chain_table, config, selection_dict,
                             title_prefix="", output_path=None):
    """Bar chart of how often residues from a selection appear in the network.

    selection_dict: config format {'chain': str, 'resids': list} or
    {'chain': str, 'resid': int}. Looks up node numbers via ChainTable.
    """
    chain_id = selection_dict['chain']
    if 'resids' in selection_dict:
        resids = selection_dict['resids']
    elif 'resid' in selection_dict:
        resids = [selection_dict['resid']]
    else:
        return

    nodes = _resids_to_nodes(chain_table, chain_id, resids)

    if 'source' in df.columns:
        weight_by_node = sum_weights_by_residue(df)
    else:
        weight_by_node = df.set_index('node')['weight']

    sel_weights = weight_by_node.reindex(nodes, fill_value=0)

    labels = [chain_table.node_to_label(n) for n in sel_weights.index]
    colors = [node_color(config, chain_table, n) for n in sel_weights.index]

    fig, ax = plt.subplots(figsize=(max(6, len(labels) * 0.6), 5))
    ax.bar(range(len(labels)), sel_weights.values, color=colors)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Aggregated Edge Weight')

    sel_label = selection_dict.get('label', title_prefix)
    sys_name = config.get('system', {}).get('name', '')
    ax.set_title(f"{sys_name} — {sel_label}" if sel_label else f"{sys_name} — Residue Occurrences")
    plt.tight_layout()

    if output_path:
        os.makedirs(output_path, exist_ok=True)
        safe_name = sel_label.replace(' ', '_').replace('/', '-')[:40] if sel_label else 'residues'
        fig_path = os.path.join(output_path, f"occurrences_{safe_name}.png")
        fig.savefig(fig_path, dpi=300, bbox_inches="tight")
        print(f"Saved figure to {fig_path}")

    plt.close(fig)


def plot_weight_diff(df, chain_table, config, ref_condition,
                     chains=None, output_path=None, label_col=None):
    """Plot per-residue weight difference vs a reference condition.

    Requires df containing at least two conditions. When label_col is set
    (e.g., 'lit_node' for cross-system comparison), uses that column for
    residue alignment instead of raw node integers.
    """
    import re

    conditions = df['condition'].unique()
    target_conditions = [c for c in conditions if c != ref_condition]

    if not target_conditions:
        print(f"No conditions to compare against reference '{ref_condition}'")
        return

    if label_col is not None:
        idx_col = label_col
    else:
        idx_col = 'node'

    chain_order = _get_chain_order(chain_table, chains)

    ref_series = df[df['condition'] == ref_condition].set_index(idx_col)['normalized_weight']

    for target in target_conditions:
        target_series = df[df['condition'] == target].set_index(idx_col)['normalized_weight']
        diff = target_series.subtract(ref_series, fill_value=0)

        n_chains = len(chain_order)
        fig, axes = plt.subplots(n_chains, 1, figsize=(14, 3 * n_chains), sharex=False)
        if n_chains == 1:
            axes = [axes]

        for idx, cid in enumerate(chain_order):
            ax = axes[idx]

            if label_col is not None:
                chain_mask = diff.index.to_series().apply(
                    lambda lbl: lbl.split(':')[0] == cid
                )
                chain_diff = diff[chain_mask.values]
                resids = [int(re.search(r'\d+', lbl.split(':')[1]).group())
                          for lbl in chain_diff.index]
            else:
                start, end = chain_table.chain_node_range(cid)
                chain_diff = diff[(diff.index >= start) & (diff.index <= end)]
                resids = [chain_table.node_to_resid(n) for n in chain_diff.index]

            pos_mask = chain_diff >= 0
            ax.bar(resids, chain_diff.where(pos_mask, 0), color='steelblue', alpha=0.7, width=1)
            ax.bar(resids, chain_diff.where(~pos_mask, 0), color='tomato', alpha=0.7, width=1)
            ax.axhline(0, color='black', linewidth=0.5)

            identity = cid
            for c in config['chains']:
                if c['id'] == cid:
                    identity = c.get('identity', cid)
                    break
            ax.set_title(f"Chain {cid} ({identity})", fontsize=10, loc='left')
            ax.set_ylabel('Weight Diff')

        xlabel = 'Literature residue ID' if label_col else 'Residue ID (chain-local)'
        axes[-1].set_xlabel(xlabel)
        sys_name = config.get('system', {}).get('name', '')
        fig.suptitle(f"{sys_name} — {target} vs {ref_condition}", fontsize=13)
        plt.tight_layout()

        if output_path:
            os.makedirs(output_path, exist_ok=True)
            fig_path = os.path.join(output_path, f"weight_diff_{target}_vs_{ref_condition}.png")
            fig.savefig(fig_path, dpi=300, bbox_inches="tight")
            print(f"Saved figure to {fig_path}")

        plt.close(fig)
