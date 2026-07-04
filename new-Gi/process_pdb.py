from pdbfixer import PDBFixer
from openmm.app import PDBFile

# ---- Load the original file (has SEQRES records intact) ----
fixer = PDBFixer(filename='9LL8.pdb')

# ---- No chains to remove ----
# 9LL8 has no scFv16 or antibody fragment. All four chains
# (R=receptor, A=Gαi1, B=Gβ1, C=Gγ2) are kept.
print("Chains in structure:")
for i, chain in enumerate(fixer.topology.chains()):
    n_residues = sum(1 for _ in chain.residues())
    print(f"  Index {i}: Chain {chain.id}, {n_residues} residues")
print()

# ---- Save psilocin binding pose BEFORE stripping heterogens ----
# Psilocin rejoins the system later during the CHARMM-GUI merge step.
# We need its 9LL8 binding pose coordinates for that. Extract the
# HETATM lines for residue 91Q directly from the raw PDB file,
# since this is simpler and more transparent than going through
# OpenMM's topology API.
psilocin_lines = []
with open('9LL8.pdb', 'r') as f:
    for line in f:
        if line.startswith('HETATM') and ' 91Q ' in line:
            psilocin_lines.append(line)

with open('psilocin_9LL8.pdb-py', 'w') as f:
    for line in psilocin_lines:
        f.write(line)
    f.write('END\n')

print(f"Saved psilocin binding pose: {len(psilocin_lines)} HETATM lines "
      f"-> psilocin_9LL8-py.pdb")

# ---- Remove all heterogens (psilocin, cholesterol, waters) ----
# This strips:
#   - 91Q (psilocin, already saved above)
#   - CLR (cholesterol, stripped by decision: 9AS8 had none, and
#     the membrane builder will place its own ~46% cholesterol)
#   - HOH (10 crystallographic waters)
# PDBFixer can't handle non-standard small molecules, and we don't
# want the cholesterol introducing an uncontrolled variable.
fixer.removeHeterogens(keepWater=False)

# ---- Find missing residues ----
fixer.findMissingResidues()

print(f"\nFound {len(fixer.missingResidues)} gaps across all chains.\n")

# ---- Remove the gaps we decided to skip ----
# Decision framework (same as 9AS8):
#   - Short internal loops (<~15 residues): MODEL
#   - Long disordered stretches (termini, ICL3, AHD): SKIP
#   - PDBFixer models loops as extended chain; equilibration
#     relaxes them. Only meaningful for short gaps.
chains_list = list(fixer.topology.chains())
keys_to_delete = []

for key, residues in sorted(fixer.missingResidues.items()):
    chain_index, position = key
    chain_id = chains_list[chain_index].id

    # --- Receptor (chain R) ---
    if chain_id == 'R' and position == 0:
        # Disordered N-terminus, 79 residues (was 78 in 9AS8)
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, pos {position:>4}, "
              f"{len(residues):>3} res (disordered N-terminus)")

    elif chain_id == 'R' and position == 183:
        # ICL3, 52 residues (was 49 in 9AS8). Too long, genuinely
        # disordered, primary G protein coupling surface.
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, pos {position:>4}, "
              f"{len(residues):>3} res (ICL3, too long)")

    elif chain_id == 'R' and position == 258:
        # Disordered C-terminus, 78 residues (same as 9AS8)
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, pos {position:>4}, "
              f"{len(residues):>3} res (disordered C-terminus)")

    # --- Gαi1 (chain A) ---
    elif chain_id == 'A' and position == 53:
        # Alpha-helical domain (AHD), 124 residues. Disordered in
        # the nucleotide-free state (GDP released, AHD swings open).
        # 9AS8's mini-GαqiN had the AHD truncated by design;
        # 9LL8's Gαi1 has it in sequence but it's unresolved.
        # Same outcome: both builds lack AHD coordinates.
        keys_to_delete.append(key)
        print(f"  SKIP:  Chain {chain_id}, pos {position:>4}, "
              f"{len(residues):>3} res (Gαi1 AHD, disordered)")

    # --- Everything else: MODEL ---
    else:
        print(f"  MODEL: Chain {chain_id}, pos {position:>4}, "
              f"{len(residues):>3} res")

for key in keys_to_delete:
    del fixer.missingResidues[key]

print(f"\nSkipped {len(keys_to_delete)} gaps. "
      f"{len(fixer.missingResidues)} short gaps remaining to model.\n")

# ---- Find and add missing atoms ----
# Catches resolved residues with missing side-chain atoms
# (common in low-resolution cryo-EM regions).
fixer.findMissingAtoms()
print(f"Residues with missing atoms: {len(fixer.missingAtoms)}")
print(f"Chains with missing terminal atoms: {len(fixer.missingTerminals)}")

# Build the short loops, missing side-chain atoms, and terminal atoms.
fixer.addMissingAtoms()

# ---- Add hydrogens at pH 7.4 ----
# Standard protonation states. CHARMM-GUI will refine with PROPKA
# later, so this is provisional but gets the atom count right.
fixer.addMissingHydrogens(pH=7.4)

# ---- Save ----
with open('9LL8_fixed.pdb', 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

# ---- Summary ----
atom_count = sum(1 for _ in fixer.topology.atoms())
chain_count = sum(1 for _ in fixer.topology.chains())
print(f"\nDone. Saved 9LL8_fixed.pdb")
print(f"  {chain_count} chains, {atom_count} atoms (including hydrogens)")
