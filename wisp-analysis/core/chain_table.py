# wisp-analysis/core/chain_table.py
"""Chain boundary table for multi-chain WISP node index resolution.

Replaces the MPro pipeline's scalar 306-offset convention with a lookup
table built from a YAML config that works for any multi-chain system.
"""

from collections import namedtuple

NodeInfo = namedtuple('NodeInfo', ['chain', 'resid', 'resname', 'domain', 'conserved'])

AA3TO1 = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'HSD': 'H',
    'HSE': 'H', 'HSP': 'H', 'HID': 'H', 'HIE': 'H', 'HIP': 'H',
    'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'LYN': 'K', 'MET': 'M',
    'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
    'TYR': 'Y', 'VAL': 'V', 'ASH': 'D', 'GLH': 'E', 'CYX': 'C',
}


def _expand_domains(domains_dict):
    """Expand {domain_name: [start, end]} into {resid: domain_name}."""
    lookup = {}
    for name, bounds in domains_dict.items():
        start, end = bounds
        for resid in range(start, end + 1):
            lookup[resid] = name
    return lookup


class ChainTable:
    """Maps 1-indexed WISP node IDs to chain/residue/domain metadata.

    Constructed from the 'chains' list in a system YAML config. Nodes are
    numbered sequentially across chains in the order they appear in the
    WISP input PDB (and thus in the config).
    """

    def __init__(self, chains_config):
        self._nodes = {}
        self._chain_ranges = {}
        self._chain_order = []

        node = 1
        cumulative_0idx = 0

        for chain in chains_config:
            cid = chain['id']
            n = chain['num_residues']

            if chain['wisp_start_0idx'] != cumulative_0idx:
                raise ValueError(
                    f"chain {cid}: wisp_start_0idx={chain['wisp_start_0idx']} "
                    f"but cumulative count is {cumulative_0idx} -- "
                    f"check chain order and num_residues"
                )

            is_ligand = chain.get('is_ligand', False)
            if not is_ligand and len(chain['sequence']) != n:
                raise ValueError(
                    f"chain {cid}: sequence length {len(chain['sequence'])} "
                    f"!= num_residues {n}"
                )

            start = node
            domain_lookup = _expand_domains(chain.get('domains', {}))
            conserved_set = set(chain.get('conserved_residues', []))

            for resid in range(1, n + 1):
                if is_ligand:
                    resname = chain.get('residue_name', 'LIG')
                else:
                    resname = chain['sequence'][resid - 1]

                self._nodes[node] = NodeInfo(
                    chain=cid,
                    resid=resid,
                    resname=resname,
                    domain=domain_lookup.get(resid),
                    conserved=resid in conserved_set,
                )
                node += 1

            self._chain_ranges[cid] = (start, node - 1)
            self._chain_order.append(cid)
            cumulative_0idx += n

        self._total_nodes = node - 1

    def _get(self, node):
        try:
            return self._nodes[node]
        except KeyError:
            raise ValueError(f"node {node} out of range 1..{self._total_nodes}")

    @property
    def total_nodes(self):
        return self._total_nodes

    @property
    def chain_ids(self):
        return list(self._chain_order)

    def node_to_chain(self, node):
        return self._get(node).chain

    def node_to_resid(self, node):
        return self._get(node).resid

    def node_to_resname(self, node):
        return self._get(node).resname

    def node_to_domain(self, node):
        return self._get(node).domain

    def is_conserved(self, node):
        return self._get(node).conserved

    def node_to_label(self, node):
        info = self._get(node)
        return f"{info.chain}:{info.resname}{info.resid}"

    def edge_chains(self, src, sink):
        return (self.node_to_chain(src), self.node_to_chain(sink))

    def is_interchain(self, src, sink):
        return self.node_to_chain(src) != self.node_to_chain(sink)

    def is_interdomain(self, src, sink):
        if self.is_interchain(src, sink):
            return True
        return self.node_to_domain(src) != self.node_to_domain(sink)

    def chain_node_range(self, chain_id):
        return self._chain_ranges[chain_id]

    def verify_against_structure(self, pdb_path):
        """Compare config sequences against a WISP average_structure.pdb.

        Walks the PDB in file order, extracts the first occurrence of each
        (chain, resid) pair, converts 3-letter resnames via AA3TO1, and
        compares against node_to_resname() at the same sequential position.

        Returns a list of (node, (chain, resid), expected, actual, raw_resname)
        tuples. Empty list means all 1-letter codes match.
        """
        seen = {}
        order = []
        with open(pdb_path) as fh:
            for line in fh:
                if not line.startswith(('ATOM', 'HETAT')):
                    continue
                chain_id = line[21]
                resid = int(line[22:26])
                key = (chain_id, resid)
                if key not in seen:
                    seen[key] = line[17:20].strip()
                    order.append(key)

        mismatches = []
        for node, key in enumerate(order, start=1):
            expected = self.node_to_resname(node)
            raw = seen[key]
            actual = AA3TO1.get(raw, raw)
            if expected != actual:
                mismatches.append((node, key, expected, actual, raw))
        return mismatches
