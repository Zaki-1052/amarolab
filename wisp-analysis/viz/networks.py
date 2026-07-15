# wisp-analysis/viz/networks.py
"""2D NetworkX graph visualization with domain coloring.

Adapted from mpro-analysis/utils/networks.py. All 306-offset logic,
mpro_seq label formatting, and selections imports replaced with
ChainTable lookups and config-driven colors.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

from viz.colors import node_color


def visualize_2D_network(G, chain_table, config, condition, cutoff,
                         output_path=None, combined=False, pos=None):
    print(len(G.edges))
    print(len(G.nodes))

    plt.figure(figsize=(16, 14))

    if combined:
        pos = nx.spring_layout(G, weight="normalized_weight", seed=42, k=1.5, iterations=200)
    else:
        pos = nx.kamada_kawai_layout(G, weight="normalized_weight")

    if not pos:
        pos = {n: np.array([x * 18, y * 18], dtype=float) for n, (x, y) in pos.items()}

    nodes = list(G.nodes())
    min_dist = 3.0
    n_iter = 220
    repel_k = 0.55
    max_step = 0.35

    for t in range(n_iter):
        cool = 1.0 - (t / n_iter) * 0.45
        for i in range(len(nodes)):
            u = nodes[i]
            for j in range(i + 1, len(nodes)):
                v = nodes[j]
                delta = pos[u] - pos[v]
                dist = np.linalg.norm(delta)
                if dist < 1e-8:
                    delta = np.random.uniform(-0.1, 0.1, size=2)
                    dist = np.linalg.norm(delta)
                if dist < min_dist:
                    direction = delta / dist
                    overlap = (min_dist - dist)
                    shift = repel_k * overlap * direction * cool
                    step_norm = np.linalg.norm(shift)
                    if step_norm > max_step:
                        shift = shift * (max_step / step_norm)
                    pos[u] += shift
                    pos[v] -= shift

    edge_w = [d.get("normalized_weight", 1.0) for _, _, d in G.edges(data=True)]
    if edge_w and max(edge_w) != min(edge_w):
        mn, mx = min(edge_w), max(edge_w)
        edge_w = [1.0 + 3.5 * (w - mn) / (mx - mn) for w in edge_w]
    else:
        edge_w = [1.5] * len(edge_w)

    node_colors = [node_color(config, chain_table, n) for n in G.nodes()]

    node_size = 1500
    nx.draw_networkx_edges(G, pos, width=edge_w, edge_color="black", alpha=0.9)

    node_list = list(G.nodes())
    is_conserved = [chain_table.is_conserved(n) for n in node_list]
    node_edgecolors = ["black" if c else "white" for c in is_conserved]
    node_lws = [2.2 if c else 0.8 for c in is_conserved]

    nx.draw_networkx_nodes(
        G, pos, nodelist=node_list, node_size=node_size,
        node_color=node_colors, edgecolors=node_edgecolors, linewidths=node_lws,
    )

    labels = {n: chain_table.node_to_label(n) for n in G.nodes()}

    conserved_nodes = [node_list[i] for i in range(len(node_list)) if is_conserved[i]]
    non_conserved_nodes = [node_list[i] for i in range(len(node_list)) if not is_conserved[i]]

    conserved_labels = {n: labels[n] for n in conserved_nodes}
    nx.draw_networkx_labels(
        G, pos, labels=conserved_labels,
        font_size=12, font_color="yellow", font_weight="bold",
    )

    non_conserved_labels = {n: labels[n] for n in non_conserved_nodes}
    nx.draw_networkx_labels(
        G, pos, labels=non_conserved_labels,
        font_size=12, font_color="white", font_weight="bold",
    )

    sys_name = config.get('system', {}).get('name', condition)
    plt.title(f"{sys_name} — {condition.capitalize()} 2D Network (Top {cutoff}%)")
    plt.axis("off")
    plt.gca().set_aspect("equal")
    plt.tight_layout()

    if output_path:
        fig_dir = os.path.join(output_path, 'networkx', 'figures')
        os.makedirs(fig_dir, exist_ok=True)
        fig_path = os.path.join(fig_dir, f"{condition}_top{cutoff}_2D-network.png")
        plt.gcf().savefig(fig_path, dpi=300, bbox_inches="tight")
        print(f"Saved figure to {fig_path}")

    plt.close()


def process_df_to_network(df, chain_table, config, condition,
                          output_path=None, cutoff=10, combined=False):
    G = nx.from_pandas_edgelist(df, 'source', 'sink', edge_attr=True)
    visualize_2D_network(G, chain_table, config, condition, cutoff,
                         output_path, combined=combined)

    if output_path:
        output_dir = os.path.join(output_path, 'networkx')
        os.makedirs(output_dir, exist_ok=True)
        tag = f"top{cutoff}" if cutoff else "all"
        combined_tag = "combined-" if combined else ""
        pkl_path = os.path.join(output_dir, f"{condition}-{tag}-{combined_tag}network.pkl")
        with open(pkl_path, 'wb') as f:
            pickle.dump(G, f)
