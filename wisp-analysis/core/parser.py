# wisp-analysis/core/parser.py
"""WISP text file parser and DataFrame builder.

Adapted from mpro-analysis/utils/preprocessing.py Parser class.
Fixes: +1 indexing for hub_nodes/critical_edges, weight capture for both,
ChainTable-based enrichment instead of 306-offset Builder.
"""

import os
import pickle
import numpy as np
import pandas as pd
import networkx as nx


VALID_USAGES = {'node_usage', 'edge_usage', 'hub_nodes', 'critical_edges'}


class Parser:
    def __init__(self, condition, usage):
        if usage not in VALID_USAGES:
            raise ValueError(f"usage must be one of {VALID_USAGES}, got '{usage}'")
        self.condition = condition
        self.usage = usage

    def parse_txt(self, path):
        """Parse a WISP output text file into a list of record dicts.

        All node indices are converted from WISP's 0-indexed to 1-indexed.
        Weight/usage counts are captured for all four file types.
        """
        records = []
        with open(path) as fh:
            for raw in fh:
                line = raw.rstrip().split()
                if not line:
                    continue

                if self.usage == 'node_usage':
                    # "Node 0: 1800"
                    node = int(line[1][:-1]) + 1
                    weight = int(line[2])
                    records.append({'node': node, 'weight': weight})

                elif self.usage == 'hub_nodes':
                    # "Hub Node: 498 (usage: 367604)"
                    node = int(line[2]) + 1
                    weight = int(line[4].rstrip(')'))
                    records.append({'node': node, 'weight': weight})

                elif self.usage == 'edge_usage':
                    # "Edge 0 -> 1: 5"
                    source = int(line[1]) + 1
                    sink = int(line[3][:-1]) + 1
                    weight = int(line[4])
                    records.append({'source': source, 'sink': sink, 'weight': weight})

                elif self.usage == 'critical_edges':
                    # "Critical Edge 623 -> 738 (usage: 128624)"
                    source = int(line[2]) + 1
                    sink = int(line[4]) + 1
                    weight = int(line[6].rstrip(')'))
                    records.append({'source': source, 'sink': sink, 'weight': weight})

        return records

    def check_degeneracy(self, df):
        """Collapse bidirectional edges into canonical (sorted) form.

        edge_usage: sums weights from both directions.
        critical_edges: deduplicates (both directions carry identical weight).
        """
        if self.usage not in ('edge_usage', 'critical_edges'):
            return df

        df = df.copy()
        df['canonical_edge'] = df.apply(
            lambda r: tuple(sorted([r['source'], r['sink']])), axis=1
        )

        if self.usage == 'edge_usage':
            grouped = df.groupby('canonical_edge', as_index=False).agg({'weight': 'sum'})
        else:
            grouped = df.drop_duplicates(subset='canonical_edge')[['canonical_edge', 'weight']].copy()

        grouped[['source', 'sink']] = pd.DataFrame(
            grouped['canonical_edge'].tolist(), index=grouped.index
        )
        grouped['edge'] = grouped['canonical_edge']
        grouped = grouped.drop(columns='canonical_edge')

        return grouped.sort_values('weight', ascending=False).reset_index(drop=True)

    def build_df(self, records, chain_table):
        """Enrich parsed records into a DataFrame with chain/domain/conserved metadata."""
        df = pd.DataFrame(records)

        if self.usage in ('edge_usage', 'critical_edges'):
            df = self.check_degeneracy(df)
            df['condition'] = self.condition
            df['source'] = df['source'].astype(int)
            df['sink'] = df['sink'].astype(int)
            df['edge'] = df.apply(
                lambda r: tuple(sorted([r['source'], r['sink']])), axis=1
            )
            df['chain'] = df.apply(
                lambda r: chain_table.edge_chains(r['source'], r['sink']), axis=1
            )
            df['revised_edge'] = df.apply(
                lambda r: (chain_table.node_to_label(r['source']),
                           chain_table.node_to_label(r['sink'])), axis=1
            )
            df['lit_edge'] = df.apply(
                lambda r: (chain_table.node_to_lit_label(r['source']),
                           chain_table.node_to_lit_label(r['sink'])), axis=1
            )
            df['interdomain'] = df.apply(
                lambda r: chain_table.is_interdomain(r['source'], r['sink']), axis=1
            )
            df['interchain'] = df.apply(
                lambda r: chain_table.is_interchain(r['source'], r['sink']), axis=1
            )
            df['conserved_edge'] = df.apply(
                lambda r: chain_table.is_conserved(r['source'])
                          and chain_table.is_conserved(r['sink']), axis=1
            )

            if self.usage == 'edge_usage':
                df['weight'] = df['weight'].astype(int)
                w = df['weight']
                denom = w.max() - w.min()
                if denom == 0:
                    df['normalized_weight'] = 0.0
                    df['weight_chx'] = 0.2
                else:
                    df['normalized_weight'] = np.round((w - w.min()) / denom, decimals=4)
                    df['weight_chx'] = np.round(0.2 + (w - w.min()) / denom, decimals=4)

                df = df[['condition', 'chain', 'edge', 'source', 'sink',
                         'revised_edge', 'lit_edge', 'interdomain', 'interchain',
                         'conserved_edge', 'weight', 'normalized_weight', 'weight_chx']]
            else:
                df = df[['condition', 'chain', 'edge', 'source', 'sink',
                         'revised_edge', 'lit_edge', 'interdomain', 'interchain',
                         'conserved_edge', 'weight']]

        elif self.usage in ('node_usage', 'hub_nodes'):
            df['condition'] = self.condition
            df['node'] = df['node'].astype(int)
            df['revised_node'] = df['node'].apply(chain_table.node_to_label)
            df['lit_node'] = df['node'].apply(chain_table.node_to_lit_label)
            df['domain'] = df['node'].apply(chain_table.node_to_domain)
            df['chain'] = df['node'].apply(chain_table.node_to_chain)
            df['conserved'] = df['node'].apply(chain_table.is_conserved)

            if self.usage == 'node_usage':
                df['weight'] = df['weight'].astype(int)
                w = df['weight']
                denom = w.max() - w.min()
                if denom == 0:
                    df['normalized_weight'] = 0.0
                else:
                    df['normalized_weight'] = np.round((w - w.min()) / denom, decimals=4)

                df = df[['condition', 'chain', 'node', 'revised_node', 'lit_node',
                         'domain', 'conserved', 'weight', 'normalized_weight']]
            else:
                df = df[['condition', 'chain', 'node', 'revised_node', 'lit_node',
                         'domain', 'conserved', 'weight']]

        return df

    def create_graph(self, path):
        """Build a NetworkX graph from a WISP output file."""
        records = self.parse_txt(path)
        G = nx.Graph()

        if self.usage == 'node_usage':
            for r in records:
                G.add_node(r['node'], weight=r['weight'])
        elif self.usage == 'edge_usage':
            for r in records:
                G.add_edge(r['source'], r['sink'], weight=r['weight'])
        elif self.usage == 'critical_edges':
            for r in records:
                G.add_edge(r['source'], r['sink'], weight=r['weight'])
        elif self.usage == 'hub_nodes':
            for r in records:
                G.add_node(r['node'], weight=r['weight'])

        if G.number_of_edges() > 0:
            cc = max(nx.connected_components(G), key=len)
            G = G.subgraph(cc).copy()

        return G

    def create_graph_from_df(self, df, cutoff=None, output_path=None, combined=False):
        """Build a NetworkX graph from a DataFrame edgelist."""
        G = nx.from_pandas_edgelist(df, 'source', 'sink', edge_attr=True)
        cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(cc).copy()

        if output_path:
            output_dir = os.path.join(output_path, 'networkx')
            os.makedirs(output_dir, exist_ok=True)
            tag = f"top{cutoff}" if cutoff else "all"
            combined_tag = "combined-" if combined else ""
            pkl_path = f'{output_dir}/{self.condition}-{tag}-{combined_tag}network.pkl'
            with open(pkl_path, 'wb') as f:
                pickle.dump(G, f)

        return G
