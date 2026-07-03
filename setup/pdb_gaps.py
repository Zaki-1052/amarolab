from pdbfixer import PDBFixer

fixer = PDBFixer(filename='9AS8.pdb')

# Remove chain E (scFv16) inside PDBFixer
# removeChains takes chain indices (0-based) and a list of chain IDs to remove
chains_to_remove = []
for i, chain in enumerate(fixer.topology.chains()):
    if chain.id == 'E':
        chains_to_remove.append(i)

fixer.removeChains(chainIndices=chains_to_remove)

# Now find missing residues with SEQRES intact
fixer.findMissingResidues()

print(f"Found {len(fixer.missingResidues)} gaps across all chains.\n")

for key, residues in sorted(fixer.missingResidues.items()):
    chain_index, position = key
    chain_id = list(fixer.topology.chains())[chain_index].id
    print(f"Chain {chain_id}, position {position}: {len(residues)} missing residues")
    print(f"  Sequence: {', '.join(residues[:10])}{'...' if len(residues) > 10 else ''}")
    print()
