from pdbfixer import PDBFixer

fixer = PDBFixer(filename='9AS8_protein.pdb')
fixer.findMissingResidues()

print(f"Found {len(fixer.missingResidues)} gaps across all chains.\n")

for key, residues in sorted(fixer.missingResidues.items()):
    chain_index, position = key
    chain_id = list(fixer.topology.chains())[chain_index].id
    print(f"Chain {chain_id}, position {position}: {len(residues)} missing residues")
    print(f"  Sequence: {', '.join(residues[:10])}{'...' if len(residues) > 10 else ''}")
    print()
