# wisp-analysis/core/filter.py
"""DataFrame filtering and cutoff utilities.

Adapted from mpro-analysis/utils/processing.py Filter class.
Changes: ligand/state replaced with condition; dead parameters removed
from filter_df; compress_dimer dropped (homodimer-specific).
"""

import numpy as np


class Filter:
    def filter_df(self, df, condition=None):
        """Filter DataFrame by condition, then sort by normalized_weight descending."""
        if condition is not None:
            filtered = df[df['condition'] == condition]
        else:
            filtered = df
        return filtered.sort_values('normalized_weight', ascending=False).copy()

    def cutoff_df(self, df, how='cutoff', mult=None, cutoff_p=None, cutoff_v=None):
        """Apply cutoff to a DataFrame based on normalized weights.

        Args:
            df: DataFrame with a 'normalized_weight' column.
            how: 'mean' (mean + mult*std), 'cutoff' (top cutoff_p percent),
                 or 'value' (normalized_weight >= cutoff_v).
        """
        filtered_df = df.copy()

        if how == 'mean':
            if mult is None:
                raise ValueError("mult parameter required when how='mean'")
            mean = np.mean(filtered_df['normalized_weight'])
            std = np.std(filtered_df['normalized_weight'])
            filtered_df = filtered_df[filtered_df['normalized_weight'] > mean + (mult * std)]

        elif how == 'cutoff':
            if cutoff_p is None:
                raise ValueError("cutoff_p parameter required when how='cutoff'")
            cutoff = int(len(filtered_df) * (cutoff_p / 100))
            filtered_df = filtered_df.head(cutoff)

        elif how == 'value':
            if cutoff_v is None:
                raise ValueError("cutoff_v parameter required when how='value'")
            filtered_df = filtered_df[filtered_df['normalized_weight'] >= cutoff_v]

        return filtered_df
