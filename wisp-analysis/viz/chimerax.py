# wisp-analysis/viz/chimerax.py
"""ChimeraX .cxc script generator for WISP network visualization.

Adapted from mpro-analysis/utils/visualize.py (MProVisualizer). All
306-offset logic replaced with ChainTable lookups. Selection syntax
changed from :resid to /<chain>:<resid> for multi-chain systems.
"""

import numpy as np
import os

from viz.colors import node_color, domain_color, chain_color


class WispVisualizer:

    def __init__(self, chain_table, config, condition, cutoff=10,
                 style='both', show='licorice'):
        self.chain_table = chain_table
        self.config = config
        self.condition = condition
        self.cutoff = cutoff
        self.style = style
        self.show = show
        self.color_interchain = True
        self.reset = True
        self.conserved_color = 'dodger blue'
        self.key_residue_color = 'goldenrod'
        self.node_color_default = '#232323'
        self.edge_color = '#020202'
        self.cylinder_transparency = 0
        self.highlight = None
        self.bydomain = False
        self.output_path = None

        self.commands = []
        self.name = f'top{self.cutoff}-{self.style}-{self.show[:3]}'

        self.initialize_visualization()

    def _add_command(self, command):
        if isinstance(command, list):
            self.commands.extend(command)
        else:
            self.commands.append(command)

    def _sel(self, chain_id, resids):
        """Build a ChimeraX selection string for residues in a chain."""
        if isinstance(resids, (int, np.integer)):
            return f'/{chain_id}:{resids}'
        return f'/{chain_id}:{",".join(str(r) for r in resids)}'

    def _sel_range(self, chain_id, start, end):
        """Build a ChimeraX range selection: /<chain>:<start>-<end>."""
        return f'/{chain_id}:{start}-{end}'

    def _node_sel(self, node):
        """Convert a WISP node number to a ChimeraX selection string."""
        chain = self.chain_table.node_to_chain(node)
        resid = self.chain_table.node_to_resid(node)
        return f'/{chain}:{resid}'

    def _node_atom_sel(self, node, atom='CA'):
        """Convert a WISP node to a ChimeraX atom selection."""
        chain = self.chain_table.node_to_chain(node)
        resid = self.chain_table.node_to_resid(node)
        return f'/{chain}:{resid}@{atom}'

    def default_view(self, visible_chains=None, silhouettes=False):
        """Set up the default view. Shows visible_chains with domain coloring,
        dims the rest with transparency."""
        if visible_chains is None:
            visible_chains = ['R', 'A']

        if self.reset:
            self._add_command(f'graphics silhouettes {"false" if not silhouettes else "true"};')
            self._add_command('cartoon suppress false;')
            self._add_command('close #2-*;')
            self._add_command('~show a;')
            self._add_command('transp 60 target c;')
            self._add_command('color dim gray;')

            for cid in self.chain_table.chain_ids:
                start, end = self.chain_table.chain_node_range(cid)
                s_start = self.chain_table.node_to_resid(start)
                s_end = self.chain_table.node_to_resid(end)
                sel = self._sel_range(cid, s_start, s_end)

                if cid in visible_chains:
                    self._add_command(f'show {sel} c; transp {sel} 0 target c;')
                else:
                    self._add_command(f'show {sel} c; transp {sel} 60 target c; color {sel} dim gray;')

    def initialize_visualization(self):
        self.default_view()
        if self.bydomain:
            self.color_domains()

    def color_domains(self):
        """Color every chain by its domain definitions from config."""
        for chain_cfg in self.config['chains']:
            cid = chain_cfg['id']
            domains = chain_cfg.get('domains', {})
            for dname, (dstart, dend) in domains.items():
                sel = self._sel_range(cid, dstart, dend)
                color = domain_color(self.config, dname)
                self._add_command(f'sel {sel}; color sel {color};')

    def color_chains(self):
        """Color each chain uniformly by its chain color."""
        for cid in self.chain_table.chain_ids:
            start, end = self.chain_table.chain_node_range(cid)
            s_start = self.chain_table.node_to_resid(start)
            s_end = self.chain_table.node_to_resid(end)
            sel = self._sel_range(cid, s_start, s_end)
            color = chain_color(self.config, cid)
            self._add_command(f'sel {sel}; color sel {color};')

    def highlight_dict_selection(self, sel_dict, transparency=60):
        """Highlight residues defined in a config-format selection dict.

        sel_dict values: {'chain': str, 'resids': list} or {'chain': str, 'resid': int}.
        """
        highlighted = []
        for name, entry in sel_dict.items():
            if isinstance(entry, dict):
                cid = entry.get('chain')
                resids = entry.get('resids', [entry['resid']] if 'resid' in entry else [])
                if cid and resids:
                    highlighted.append(self._sel(cid, resids))

        if highlighted:
            hide_sel = '~sel; sel ~(' + ' '.join(highlighted) + ');~show sel c;'
            self._add_command(hide_sel)

    def show_selection(self, chain_id, resids):
        """Show specific residues on a chain."""
        sel = self._sel(chain_id, resids)
        if self.show == 'licorice':
            self._add_command(
                f'sel {sel}; show sel&~@H* a; transp sel 0 target a; '
                f'color sel&~@C* byelement; style sel ball;'
            )
        else:
            self._add_command(
                f'sel {sel}; show sel&@CA a; transp sel&@CA 0 target a; '
                f'style sel sphere; size sel&@CA atomRadius 1;'
            )

    def show_key_residues(self, key_name, color=None):
        """Show a named residue group from config['key_residues']."""
        key_residues = self.config.get('key_residues', {})
        entry = key_residues.get(key_name)
        if entry is None:
            return

        if color is None:
            color = self.key_residue_color

        cid = entry.get('chain')
        resids = entry.get('resids', [entry['resid']] if 'resid' in entry else [])
        if not cid or not resids:
            return

        sel = self._sel(cid, resids)
        self._add_command(
            f'sel {sel}; show sel&~@H* a; style sel ball; '
            f'size sel&@CA atomRadius 1; color sel {color}; '
            f'color sel&~@C* byelement; transp sel 0 target a;'
        )

    def show_ligand(self):
        """Show the ligand chain from config."""
        for chain_cfg in self.config['chains']:
            if chain_cfg.get('is_ligand', False):
                cid = chain_cfg['id']
                sel = self._sel(cid, 1)
                lig_color = chain_color(self.config, cid)
                self._add_command(
                    f'sel {sel}; show sel&~@H* a; style sel ball; '
                    f'color sel {lig_color}; color sel&~@C* byelement;'
                )
                return

    def show_cylinder(self, df, critical=False):
        """Draw cylinders between edge endpoints on the 3D structure."""
        cylinder_transparency = self.cylinder_transparency

        if 'weight_chx' not in df.columns:
            wmin, wmax = df['weight'].min(), df['weight'].max()
            if wmax == wmin:
                df = df.copy()
                df['weight_chx'] = 0.7
            else:
                df = df.copy()
                df['weight_chx'] = np.round(
                    0.2 + (df['weight'] - wmin) / (wmax - wmin), 4
                )

        for count, (_, row) in enumerate(df.iterrows(), start=2):
            weight = row['weight_chx']
            source = row['source']
            sink = row['sink']

            src_color = self.node_color_default
            snk_color = self.node_color_default

            if not self.color_interchain:
                edge_clr = row.get('color', self.edge_color)
                src_color = edge_clr
                snk_color = edge_clr
            else:
                is_interchain = row.get('interchain', False)
                edge_clr = 'goldenrod' if is_interchain else self.edge_color

                src_domain = self.chain_table.node_to_domain(source)
                snk_domain = self.chain_table.node_to_domain(sink)
                if src_domain is not None:
                    src_color = domain_color(self.config, src_domain)
                if snk_domain is not None:
                    snk_color = domain_color(self.config, snk_domain)

                if critical and row.get('critical', False):
                    edge_clr = 'red'

            src_atom = self._node_atom_sel(source)
            snk_atom = self._node_atom_sel(sink)

            self._add_command(
                f'shape cylinder radius {weight} '
                f'frompoint {src_atom} topoint {snk_atom};'
                f'color #{count} {edge_clr}; transp #{count} {cylinder_transparency};'
            )

            src_sel = self._node_sel(source)
            snk_sel = self._node_sel(sink)
            self._add_command(
                f'sel {src_sel}@CA; show sel atoms; style sel sphere; '
                f'size sel atomRadius 1; color {src_sel}@C* {src_color};'
                f'sel {snk_sel}@CA; show sel atoms; style sel sphere; '
                f'size sel atomRadius 1; color {snk_sel}@C* {snk_color};'
            )

    def visualize_nodes(self, df):
        """Show node positions as spheres on the 3D structure."""
        filtered = df[df['condition'] == self.condition] if 'condition' in df.columns else df

        nodes = []
        for node in filtered['node'].values:
            nodes.append(self._node_sel(node))

        if nodes:
            sel_str = ' '.join(nodes)
            self._add_command(
                f'sel {sel_str}; show sel&@CA a; style sel&@CA sphere; '
                f'size sel atomRadius 1.0; color sel red;'
            )

    def select_conserved(self):
        """Select and label conserved residues from all chains."""
        conserved_sels = []
        for node in range(1, self.chain_table.total_nodes + 1):
            if self.chain_table.is_conserved(node):
                conserved_sels.append(self._node_sel(node))

        if conserved_sels:
            sel_str = ' '.join(conserved_sels)
            self._add_command(f'sel {sel_str}; label sel;')

    def visualize_conserved(self, df, by_domain=False):
        """Highlight conserved residues that appear in the edge DataFrame."""
        conserved_set = set()
        for _, row in df.iterrows():
            source, sink = row['source'], row['sink']
            if self.chain_table.is_conserved(source):
                conserved_set.add(source)
            if self.chain_table.is_conserved(sink):
                conserved_set.add(sink)

        if not conserved_set:
            return

        sels = [self._node_sel(n) for n in sorted(conserved_set)]
        self._add_command(f'sel {" ".join(sels)};')

        if by_domain:
            by_dom = {}
            for n in conserved_set:
                dom = self.chain_table.node_to_domain(n)
                if dom is not None:
                    by_dom.setdefault(dom, []).append(n)

            for dom, nodes in by_dom.items():
                dom_sels = [self._node_sel(n) for n in sorted(nodes)]
                color = domain_color(self.config, dom)
                self._add_command(
                    f'sel {" ".join(dom_sels)}; color sel {color}; '
                    f'color sel&~@C* byelement;'
                )
        else:
            self._add_command(f'color sel {self.conserved_color}; color sel&~@C* byelement;')

        if self.show == 'licorice':
            self._add_command(
                'show sel&~@H* a; color sel&~@C* byelement; '
                'style sel ball; size sel atomradius 2;'
            )

    def load_cxs(self, save=False):
        if self.output_path is None:
            raise ValueError("output_path must be set before calling load_cxs().")

        if not save:
            blank_path = os.path.join(
                self.output_path,
                f'figures/chimera-wisp/blank/{self.condition}-blank.cxs'
            )
            return f'open {blank_path};'
        else:
            save_path = os.path.join(
                self.output_path,
                f'figures/chimera-wisp/cxs/{self.condition}-wisp-{self.name}.cxs'
            )
            return f'save {save_path};'

    def write_cxc(self, output_path):
        """Write all accumulated commands to a .cxc file."""
        os.makedirs(output_path, exist_ok=True)
        file_name = f'{self.condition}-wisp-{self.name}.cxc'
        file_path = os.path.join(output_path, file_name)

        with open(file_path, 'w') as f:
            for command in self.commands:
                f.write(command + '\n')

        print(f"Wrote {len(self.commands)} commands to {file_path}")
        return file_path
