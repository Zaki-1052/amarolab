# CYP Transmembrane Helices

## Creating Missing Transmembrane Helices in Cytochrome P450s Using Maestro[edit](</mediawiki/index.php?title=CYP_Transmembrane_Helices&action=edit&section=1> "Edit section: Creating Missing Transmembrane Helices in Cytochrome P450s Using Maestro")]

Many crystal structures of Cytochrome P450s do not include the N-terminal transmembrane domain of the protein due to weak electron density and difficulties in crystallizing membrane-bound proteins. The transmembrane domain, usually a 20-residue alpha helix, anchors the protein to the lipid membrane and serves other structural functions. Maestro can be used to reconstruct these missing transmembrane helices. 

  1. Download the PDB file from the Protein Data Bank by clicking on "Get PDB", and then entering the PDBID.
  2. Run the Protein Preparation Wizard to process the structure, and delete any insignificant heteroatoms such as waters or phosphates from the crystallization process.
  3. Open the Build panel from Edit > Build > Fragments and then select "Amino acids" from the fragments list. 
  4. Change the build option from "Place" to "Grow", and change the grow directions from "forward(N-to-C)" to "backward(C-to-N)".
  5. Define the grow bond by clicking the nitrogen atom of the terminal amino group, and then the hydrogen atom of the terminal amino group.
  6. Choose the desired residues by clicking on them, in backwards order (from C-terminus to N-terminus). The secondary structure of the non-transmembrane region should be extended unless the secondary structure is known. The secondary structure should be changed to alpha helix once you have reached a transmembrane residue. Stop building once the transmembrane helix is constructed.
  7. Delete the acetyl capping group that Maestro automatically inserts by deleting the residue named "X" on the bottom sequence toolbar, and then re-add the missing hydrogen using the Protein Preparation Wizard.
  8. Export the file in Maestro and save it as a PDB file, and then open the file in UCSF Chimera. (Note: You may have to modify the PDB file by moving the newly created residue data into the correct place)
  9. Download the PDB structure file with membrane positioning from the OPM Database, and open that in UCSF Chimera.
  10. Align the two proteins using MatchMaker from Tools > Structure Comparison > MatchMaker, and select the PDB file from Maestro as the reference structure, and the PDB file from OPM as the structure to match.
  11. Save the aligned PDB file from OPM, and save it relative to the PDB file from Maestro.
  12. Copy the dummy atoms from the newly created aligned PDB file from OPM, and paste it onto the PDB file from Maestro.
  13. Open the newly saved file in Maestro, and you will notice that the transmembrane helix is way off from the predicted membrane region. Thus, you need to modify some of the dihedrals in the extended peptide region of the protein.
  14. Click "Adjust" and the choose a peptide bond to rotate the helix in (Note: Make sure the chosen peptide bond was not part of the original crystal structure). Rotate the peptide bond and modify other peptide bonds until the transmembrane helix is roughly perpendicular to the plane of dummy atoms and the helix starts near the plane of dummy atoms.
  15. Save the new file, and then run it with CHARMM-GUI and NAMD.
