from pdbfixer import PDBFixer

# ---- Load the ORIGINAL file (SEQRES records intact) ----
# Remember: never use a PyMOL-saved file here. PyMOL strips
# SEQRES records, which is what PDBFixer compares against to
# find missing residues.
fixer = PDBFixer(filename='9LL8.pdb')

# ---- Verify we have the right chains ----
# Expected: R (receptor), A (Gαi1), B (Gβ1), C (Gγ2)
# No chain to remove this time (no scFv16 equivalent)
print("Chains in structure:")
for i, chain in enumerate(fixer.topology.chains()):
    n_residues = sum(1 for _ in chain.residues())
    print(f"  Index {i}: Chain {chain.id}, {n_residues} residues")
print()

# ---- Find missing residues ----
fixer.findMissingResidues()

print(f"Found {len(fixer.missingResidues)} gaps across all chains.\n")

for key, residues in sorted(fixer.missingResidues.items()):
    chain_index, position = key
    chain_id = list(fixer.topology.chains())[chain_index].id
    print(f"Chain {chain_id}, position {position:>4}: "
          f"{len(residues):>3} missing residues")
    # Show the first few residue names so we can see what's there
    preview = ', '.join(residues[:8])
    if len(residues) > 8:
        preview += f', ... ({len(residues)} total)'
    print(f"  Sequence: {preview}")
    print()

chains = list(fixer.topology.chains())
print("Second Chain R (index 4) contents:")
for res in chains[4].residues():
    print(f"  {res.name:>4}  id={res.id}")
