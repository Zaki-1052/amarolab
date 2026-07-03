from pdbfixer import PDBFixer
from openmm.app import PDBFile

# ---- Load the original file (has SEQRES records intact) ----
fixer = PDBFixer(filename='9AS8.pdb')

# ---- Remove chain E (scFv16, the engineering antibody) ----
chains_to_remove = []
for i, chain in enumerate(fixer.topology.chains()):
    if chain.id == 'E':
        chains_to_remove.append(i)
fixer.removeChains(chainIndices=chains_to_remove)

# ---- Remove all heterogens (psilocin, waters, anything non-protein) ----
# Psilocin was already saved separately from PyMOL (psilocin.pdb).
# It rejoins the system in CHARMM-GUI through the Ligand Reader module,
# where it gets its own force field parameters. PDBFixer doesn't know
# how to handle non-standard small molecules, so stripping them here
# avoids problems downstream.
fixer.removeHeterogens(keepWater=False)

# ---- Find missing residues ----
fixer.findMissingResidues()

# ---- Remove the gaps we decided to skip ----
chains_list = list(fixer.topology.chains())
keys_to_delete = []

for key, residues in fixer.missingResidues.items():
    chain_index, position = key
    chain_id = chains_list[chain_index].id

    if (chain_id == 'A' and position == 0):     # N-terminus, 78 res, disordered
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, position {position:>4}, {len(residues):>3} residues (disordered N-terminus)")
    elif (chain_id == 'A' and position == 185):  # ICL3, 49 res, too long
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, position {position:>4}, {len(residues):>3} residues (ICL3, too long)")
    elif (chain_id == 'A' and position == 262):  # C-terminus, 78 res, disordered
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, position {position:>4}, {len(residues):>3} residues (disordered C-terminus)")
    elif (chain_id == 'C' and position == 0):    # His-tag, not native protein
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, position {position:>4}, {len(residues):>3} residues (His-tag)")
    else:
        print(f"  MODEL: Chain {chain_id}, position {position:>4}, {len(residues):>3} residues")

for key in keys_to_delete:
    del fixer.missingResidues[key]

print(f"\nSkipped {len(keys_to_delete)} gaps. {len(fixer.missingResidues)} short gaps remaining to model.\n")

# ---- Find and add missing atoms ----
# This catches resolved residues that are missing side-chain atoms
# (common in low-resolution regions of cryo-EM structures).
fixer.findMissingAtoms()
print(f"Residues with missing atoms: {len(fixer.missingAtoms)}")
print(f"Chains with missing terminal atoms: {len(fixer.missingTerminals)}")

# Build everything: the short loops, any missing side-chain atoms,
# and terminal atoms.
fixer.addMissingAtoms()

# ---- Add hydrogens at pH 7.4 ----
# Standard protonation states. CHARMM-GUI will refine these later
# with its own PROPKA-based assignment, so this is provisional
# but gets the atom count right.
fixer.addMissingHydrogens(pH=7.4)

# ---- Save ----
with open('9AS8_fixed.pdb', 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

# ---- Summary ----
atom_count = sum(1 for _ in fixer.topology.atoms())
chain_count = sum(1 for _ in fixer.topology.chains())
print(f"\nDone. Saved 9AS8_fixed.pdb")
print(f"  {chain_count} chains, {atom_count} atoms (including hydrogens)")
