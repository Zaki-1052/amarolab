# CYP Membrane Integration - Aromatase System

## Introduction[edit](</mediawiki/index.php?title=CYP_Membrane_Integration_-_Aromatase_System&action=edit&section=1> "Edit section: Introduction")]

Proteins of the cytochrome P450 superfamily catalyze oxidation reactions for a variety of substrates and play an important role in drug metabolism, steroid biosynthesis, and other cellular processes. Some cytochrome P450 proteins are membrane-bound in specific locations of the cell, such as the endoplasmic reticulum, by an N-terminal anchor that sticks into and interacts with the membrane. Although crystallographic structures of these proteins exist, many of them lack the crucial N-terminus because of the rigorous conditions of the protein crystallization process, and thus complicate the relatively easy task of protein insertion into a membrane. Molecular dynamics simulations of a cytochrome P450/membrane system may provide valuable insight into these proteins, and can lead to the development of new inhibitors of the proteins 

Aromatase (CYP19A1) is a membrane-bound cytochrome P450 protein that catalyzes the synthesis of estrogens from androgens through a mechanism of three successive hydroxylations, then elimination of a formyl group and aromatization of the A-ring. Aromatase localizes to the endoplasmic membrane, where its N-terminal anchor attaches itself to the membrane. Membrane integration is essential because it allows hydrophobic steroids to enter the protein through an active site accessed only through the membrane bilayer. The only crystal structure of aromatase (PDB ID: 3EQM), reported by Ghosh et al. lacks the first 44 residues of the N-terminus and the last 7 residues of the C-terminus. The first 44 residues are identified as the residues that are associated with the membrane, and is necessary to build a protein/membrane system for molecular dynamics. By using Schrodinger's suite of programs, the N-terminus can be reconstructed from its amino acid and become ready for system preparation and molecular dynamics simulations. 

## N-terminus Construction - Maestro[edit](</mediawiki/index.php?title=CYP_Membrane_Integration_-_Aromatase_System&action=edit&section=2> "Edit section: N-terminus Construction - Maestro")]

The putative transmembrane helix constructed from residues 18-38 was constructed using the Maestro build tools. Residues 38-44 were constructed as an extended peptide (due to its unknown predicted structure, probably a disordered loop), while residues 18-38 were modelled as an alpha helix. However, residues 1-17 and 497-503 were not constructed due to its unknown and unpredicted secondary structure. The approximate membrane orientation of aromatase was predicted by OPM, and the dummy atoms from the OPM file were aligned with the new protein, and were manipulated to more closely match the orientation outlined in Ghosh et al. The dihedral angles of the newly constructed N-terminal fragment were manipulated so that the transmembrane helix would be approximately perpendicular to the plane of the membrane (shown by the dummy atoms) using Maestro. 

## Determination of Endoplasmic Reticulum Membrane Lipid Content[edit](</mediawiki/index.php?title=CYP_Membrane_Integration_-_Aromatase_System&action=edit&section=3> "Edit section: Determination of Endoplasmic Reticulum Membrane Lipid Content")]

Although Davison and Wills had precisely determined the endoplasmic reticulum membrane lipid content, many of their lipids were not available for use in CHARMM-GUI. Therefore, the lipid content had to be modified, with missing lipids replaced with the most similar lipids (similarity of lipids first determined by type, then overall structure). 

The final lipid content calculations were (Original lipids of the paper in parentheses): 

  * **Cholesterol: 10.0%** (Cholesterol)
  * **Dipalmitoylphosphatidy-PE (DPPE): 9.0%** (Palmitoyl-PE)
  * **Dioleylphosphatidyl-PE (DOPE): 11.0%** (Stearyl/Oleyl/Linoleyl/Arachidonyl/Docosahexaeonyl-PE)
  * **Stearyldocosahexaeonyl-PC (SDPC): 8.4%** (Stearyl/Docosahexaeonyl-PC)
  * **Diarachidonyl-PC (DAPC): 8.1%** (Arachidonyl-PC)
  * **Stearyloleyl-PC (SOPC): 13.2%** (Stearyl/Palmitoyl-PC)
  * **Dipalmitoyl-PC (DPPC): 6.3%** (Palmitoyl-PC)
  * **Dioleyl-PC (DOPC): 16.4%** (Oleyl/Linoleyl-PC)
  * **Palmitoyloleyl-PS (POPS): 17.6%** (PI/PS/SM)



_(PE - Phosphatidylethanolamine;_ PC - Phosphatidylcholine; PS - Phosphatidylserine; PI - Phosphatidylinositol; SM - Sphingomyelin) 

## System Construction - CHARMM-GUI[edit](</mediawiki/index.php?title=CYP_Membrane_Integration_-_Aromatase_System&action=edit&section=4> "Edit section: System Construction - CHARMM-GUI")]

The entire membrane-protein system was constructed using CHARMM-GUI. The new protein file was uploaded, and only the protein chain was read into CHARMM-GUI, due to problems with the heme and the androstenedione ligand. Aromatase was then oriented to the membrane using the dummy atoms in the OPM file, and then the numbers of each lipid for the upperleaflet and the lowerleaflet were entered (due to some portions of the protein displacing a portion of the lowerleaflet of the membrane, there were 12 more lipids in the upperleaflet than the lowerleaflet). There were a total of 266 lipids, with 129 lipids on the bottom and 139 lipids on the top. The number of lipids per type in the membrane were: 

  * **Cholesterol -**
  * **DPPE -**
  * **DOPE -**
  * **SDPC -**
  * **DAPC -**
  * **SOPC -**
  * **DPPC -**
  * **DOPC -**
  * **POPS -**
