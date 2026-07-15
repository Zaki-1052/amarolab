# wisp-analysis/analysis/differential.py
"""Cross-condition differential analysis for WISP networks.

Adapted from mpro-analysis/utils/processing.py compare_edges_between_dimers()
and compare_nodes_between_dimers(). Replaces ligand/state column grouping
with condition-based comparison. Adds filter_chains for restricting
comparison to specific chains (e.g., receptor-only for Gi vs Gq).
"""

import numpy as np
import pandas as pd


def _filter_by_chains(df, chains, is_edge=False):
    """Keep rows involving at least one chain in the given set.

    For edge DataFrames (source/sink columns): keeps rows where either
    endpoint's chain is in chains.
    For node DataFrames (chain column): keeps rows where chain is in chains.
    """
    if is_edge:
        mask = df['chain'].apply(
            lambda pair: pair[0] in chains or pair[1] in chains
        )
    else:
        mask = df['chain'].isin(chains)
    return df[mask].copy()


def compare_edges(target_df, reference_df, filter_chains=None):
    """Compare edges between two conditions and merge by summing weights.

    Returns a merged DataFrame with is_common and is_unique columns.
    """
    if filter_chains is not None:
        target_df = _filter_by_chains(target_df, filter_chains, is_edge=True)
        reference_df = _filter_by_chains(reference_df, filter_chains, is_edge=True)

    target_edges = set(
        tuple(sorted([row['source'], row['sink']]))
        for _, row in target_df.iterrows()
    )
    reference_edges = set(
        tuple(sorted([row['source'], row['sink']]))
        for _, row in reference_df.iterrows()
    )

    common_edges = target_edges.intersection(reference_edges)
    unique_edges = target_edges.difference(reference_edges)

    combined_df = pd.concat([target_df, reference_df], axis=0, ignore_index=True)

    exclude = {'weight', 'weight_chx', 'condition'}
    group_cols = [c for c in combined_df.columns if c not in exclude]

    merged_df = combined_df.groupby(
        group_cols, as_index=False, dropna=False
    ).agg({'weight': 'sum'}).copy()

    merged_df['is_common'] = merged_df.apply(
        lambda row: tuple(sorted([row['source'], row['sink']])) in common_edges,
        axis=1,
    )
    merged_df['is_unique'] = merged_df.apply(
        lambda row: tuple(sorted([row['source'], row['sink']])) in unique_edges,
        axis=1,
    )

    if 'normalized_weight' in merged_df.columns:
        return merged_df.sort_values(by='normalized_weight', ascending=False)
    return merged_df.sort_values(by='weight', ascending=False)


def compare_nodes(target_df, reference_df, filter_chains=None,
                  weight_col='normalized_weight'):
    """Compare nodes between two conditions and compute weight ratios.

    Returns a merged DataFrame with is_common, weight_ratio, and
    stabilized columns.
    """
    if filter_chains is not None:
        target_df = _filter_by_chains(target_df, filter_chains, is_edge=False)
        reference_df = _filter_by_chains(reference_df, filter_chains, is_edge=False)

    target_nodes = set(target_df['node'].values)
    reference_nodes = set(reference_df['node'].values)
    common_nodes = target_nodes.intersection(reference_nodes)

    combined_df = pd.concat([target_df, reference_df], axis=0, ignore_index=True)

    exclude = {'weight', 'normalized_weight', 'condition'}
    group_cols = [c for c in combined_df.columns if c not in exclude]

    merged_df = combined_df.groupby(
        group_cols, as_index=False, dropna=False
    ).agg({'weight': 'sum'}).copy()

    key_cols = ['node']
    ratio_df = target_df[key_cols + [weight_col]].merge(
        reference_df[key_cols + [weight_col]],
        on=key_cols,
        how='left',
        suffixes=('_target', '_reference'),
    )

    ratio_df['weight_ratio'] = np.where(
        ratio_df[f'{weight_col}_reference'] > 0,
        ratio_df[f'{weight_col}_target'] / ratio_df[f'{weight_col}_reference'],
        np.nan,
    )

    merged_df = merged_df.merge(
        ratio_df[key_cols + ['weight_ratio']],
        on=key_cols,
        how='left',
    )

    w = merged_df['weight']
    denom = w.max() - w.min()
    if denom == 0:
        merged_df['normalized_weight'] = 0.0
    else:
        merged_df['normalized_weight'] = np.round((w - w.min()) / denom, decimals=4)

    merged_df['is_common'] = merged_df['node'].isin(common_nodes)
    merged_df['stabilized'] = merged_df['weight_ratio'] >= 1

    return merged_df.sort_values(by='weight_ratio', ascending=False)
