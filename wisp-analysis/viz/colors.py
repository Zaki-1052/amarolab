# wisp-analysis/viz/colors.py
"""Config-driven color palettes and weight colormap helper.

Replaces mpro-analysis/utils/colors.py hardcoded dicts with functions
that pull colors from the YAML system config.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


FALLBACK = '#696969'


def domain_color(config, domain_name):
    if domain_name is None:
        return FALLBACK
    return config.get('colors', {}).get('domains', {}).get(domain_name, FALLBACK)


def chain_color(config, chain_id):
    return config.get('colors', {}).get('chains', {}).get(chain_id, FALLBACK)


def condition_color(config, condition_name):
    return config.get('colors', {}).get('conditions', {}).get(condition_name, FALLBACK)


def node_color(config, chain_table, node):
    domain = chain_table.node_to_domain(node)
    if domain is not None:
        return domain_color(config, domain)
    return chain_color(config, chain_table.node_to_chain(node))


def weight_colormap(weights, cmap_name='plasma'):
    """Map numeric weights to hex color strings via a matplotlib colormap."""
    cmap = plt.colormaps[cmap_name]
    norm = mcolors.Normalize(vmin=min(weights), vmax=max(weights))
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    return [mcolors.to_hex(c) for c in sm.to_rgba(weights)]


hex_list = (
    '#000080', '#0000CD', '#0000FF', '#40E0D0', '#1E90FF',
    '#87CEEB', '#87CEFA', '#A9A9A9', '#708090', '#696969',
    '#020202', '#DAA520', '#FF00FF', '#FF4500', '#32CD32',
    '#000000',
)
