# wisp-analysis/analysis/differential.py
"""Cross-condition differential analysis for WISP networks.

Adapted from mpro-analysis/utils/processing.py compare_edges_between_dimers()
and compare_nodes_between_dimers(). Replaces ligand/state column grouping
with condition-based comparison. Adds filter_chains for restricting
comparison to specific chains (e.g., receptor-only for Gi vs Gq).

For cross-system comparison (different ChainTables), pass match_col='lit_edge'
or match_col='lit_node' to match residues by literature numbering instead of
raw WISP node integers.
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


def compare_edges(target_df, reference_df, filter_chains=None, match_col=None):
    """Compare edges between two conditions and identify common/unique edges.

    When match_col is None (same-system): matches edges by raw (source, sink)
    integer tuples. When match_col is set (e.g., 'lit_edge' for cross-system):
    matches edges by the string-label tuples in that column.

    Returns a merged DataFrame with is_common and is_unique columns.
    """
    if filter_chains is not None:
        target_df = _filter_by_chains(target_df, filter_chains, is_edge=True)
        reference_df = _filter_by_chains(reference_df, filter_chains, is_edge=True)

    if match_col is not None:
        target_keys = set(
            tuple(sorted(row[match_col])) for _, row in target_df.iterrows()
        )
        ref_keys = set(
            tuple(sorted(row[match_col])) for _, row in reference_df.iterrows()
        )
    else:
        target_keys = set(
            tuple(sorted([row['source'], row['sink']]))
            for _, row in target_df.iterrows()
        )
        ref_keys = set(
            tuple(sorted([row['source'], row['sink']]))
            for _, row in reference_df.iterrows()
        )

    common_keys = target_keys.intersection(ref_keys)
    unique_keys = target_keys.difference(ref_keys)

    if match_col is not None:
        target_out = target_df.copy()
        target_out['_match_key'] = target_df[match_col].apply(
            lambda x: tuple(sorted(x))
        )
        target_out['is_common'] = target_out['_match_key'].isin(common_keys)
        target_out['is_unique'] = target_out['_match_key'].isin(unique_keys)
        target_out = target_out.drop(columns='_match_key')

        if 'normalized_weight' in target_out.columns:
            return target_out.sort_values(by='normalized_weight', ascending=False)
        return target_out.sort_values(by='weight', ascending=False)

    combined_df = pd.concat([target_df, reference_df], axis=0, ignore_index=True)

    exclude = {'weight', 'weight_chx', 'condition'}
    group_cols = [c for c in combined_df.columns if c not in exclude]

    merged_df = combined_df.groupby(
        group_cols, as_index=False, dropna=False
    ).agg({'weight': 'sum'}).copy()

    merged_df['is_common'] = merged_df.apply(
        lambda row: tuple(sorted([row['source'], row['sink']])) in common_keys,
        axis=1,
    )
    merged_df['is_unique'] = merged_df.apply(
        lambda row: tuple(sorted([row['source'], row['sink']])) in unique_keys,
        axis=1,
    )

    if 'normalized_weight' in merged_df.columns:
        return merged_df.sort_values(by='normalized_weight', ascending=False)
    return merged_df.sort_values(by='weight', ascending=False)


def compare_nodes(target_df, reference_df, filter_chains=None,
                  weight_col='normalized_weight', match_col=None):
    """Compare nodes between two conditions and compute weight ratios.

    When match_col is None (same-system): matches nodes by raw 'node' integer.
    When match_col is set (e.g., 'lit_node' for cross-system): matches by
    the string label in that column.

    Returns a merged DataFrame with is_common, weight_ratio, and
    stabilized columns.
    """
    if filter_chains is not None:
        target_df = _filter_by_chains(target_df, filter_chains, is_edge=False)
        reference_df = _filter_by_chains(reference_df, filter_chains, is_edge=False)

    key_col = match_col if match_col else 'node'

    target_keys = set(target_df[key_col].values)
    ref_keys = set(reference_df[key_col].values)
    common_keys = target_keys.intersection(ref_keys)

    ratio_df = target_df[[key_col, weight_col]].merge(
        reference_df[[key_col, weight_col]],
        on=key_col,
        how='left',
        suffixes=('_target', '_reference'),
    )

    ratio_df['weight_ratio'] = np.where(
        ratio_df[f'{weight_col}_reference'] > 0,
        ratio_df[f'{weight_col}_target'] / ratio_df[f'{weight_col}_reference'],
        np.nan,
    )

    result_df = target_df.copy()
    result_df = result_df.merge(
        ratio_df[[key_col, 'weight_ratio']],
        on=key_col,
        how='left',
    )

    result_df['is_common'] = result_df[key_col].isin(common_keys)
    result_df['stabilized'] = result_df['weight_ratio'] >= 1

    return result_df.sort_values(by='weight_ratio', ascending=False)
