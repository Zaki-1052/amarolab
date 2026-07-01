# Adding glycan parameters to PDB2PQR for simulation

# How to add glycan parameters to PDB2PQR[edit](</mediawiki/index.php?title=Adding_glycan_parameters_to_PDB2PQR_for_simulation&action=edit&section=1> "Edit section: How to add glycan parameters to PDB2PQR")]

Trying to build a system with glycans and unsure how to get AMBER to accept your glycans? Read on. But if you can use GROMACS, then just generate the input tpr on CHARMM-GUI, then use GROMACS and editconf -f [tpr file] -mead. (courtesy Matheus Ferraz). 

Note: This was built and tested using AMBER. It may work with other force fields but I will make no promises. I have referenced pymol throughout since the commands needed for this protocol are very easy on pymol, but feel free to use any other visualization program (VMD, Chimera, MOE, etc). 

  


## The necessary links:[edit](</mediawiki/index.php?title=Adding_glycan_parameters_to_PDB2PQR_for_simulation&action=edit&section=2> "Edit section: The necessary links:")]

  * [PDB2PQR overview](<https://www.cgl.ucsf.edu/chimera/docs/ContributedSoftware/apbs/pdb2pqr.html>)
  * [PDB2PQR web server](<http://nbcr-222.ucsd.edu/pdb2pqr_2.1.1/>)
  * [Adding parameters in PDB2PQR](<https://www.ics.uci.edu/~dock/pdb2pqr/userguide.html>)
  * [PDB2PQR programming guide](<https://www.ics.uci.edu/~dock/pdb2pqr/programmerguide.html#xml>)
  * [GLYCAM](<http://glycam.org/docs/news/2014/04/30/the-new-glycam-web-is-here/>), AMBER force field parameters for glycans
  * [Glyprot](<http://www.glycosciences.de/modeling/glyprot/php/main.php>), add glycans to your pdb



## The necessary files:[edit](</mediawiki/index.php?title=Adding_glycan_parameters_to_PDB2PQR_for_simulation&action=edit&section=3> "Edit section: The necessary files:")]

  * A protein pdb



## Procedure[edit](</mediawiki/index.php?title=Adding_glycan_parameters_to_PDB2PQR_for_simulation&action=edit&section=4> "Edit section: Procedure")]

### Add glycans to your protein pdb[edit](</mediawiki/index.php?title=Adding_glycan_parameters_to_PDB2PQR_for_simulation&action=edit&section=5> "Edit section: Add glycans to your protein pdb")]

Note: This step only works well if you have a small number of proteins to glycosylate. If you have a large number, i.e. whole virus, you will need to find another way to add glycans to your system. [doGlycans](<https://omictools.com/doglycans-tool>) is one option. 

Go to the Glyprot server and upload your pdb. After uploading, Glyprot will predict your glycosylation sites. Double check these to make sure they are correct. Then click "select glycans from DB", and put in the number of each type of monosaccharide, but do not input anything for the total number of oligosaccharides. From there, pick out the linkage you are looking for, and confirm that the identified glycosylation sites are consistent with your knowledge of your protein. Continue through the server, it is self-explanatory. 

### Modify the AMBER force fields to accept glycans[edit](</mediawiki/index.php?title=Adding_glycan_parameters_to_PDB2PQR_for_simulation&action=edit&section=6> "Edit section: Modify the AMBER force fields to accept glycans")]

1\. Copy the AMBER force field from the PDB2PQR directory, if you are using the McCammon workstations it is /net/software/pkg/pdb2pqr/2.0/dat or something similar. Do not touch the source files, only copy them to some safe directory where you can edit them as you wish. Also, copy the naming file into the same directory as the force field file you just copied. In my case, I wanted to modify AMBER99, so I copied the AMBER.DAT and AMBER.names files. 

2\. Find the GLYCAM parameters that will match up with the force field you selected from this [site](<http://glycam.org/docs/forcefield/all-parameters/>). If you aren't sure which version you should pick, consult [here](<http://glycam.org/docs/help/2014/07/02/which-protein-force-fields-are-compatible-with-glycam/>). Since I am using AMBER99, I used the GLYCAM_06h-1 series. 

3\. Once you have identified the glycans/monosaccharides you need, find their three-letter code on the [GLYCAM naming page](<http://glycam.org/docs/forcefield/glycam-naming-2/>). 

Hereafter use this in place of a normal amino acid three-letter code. 

As described in the link, the first letter in the three-letter code is the open valence position. In other words, this is the atoms number that contains a covalent bond to another monosaccharide, or the protein. 

The second letter tells which monosaccharide you are using, and can contain linkage information 

The third letter tells whether your linkage is an alpha- or a beta-linkage. You should be able to find this from the glycan you selected in Glyprot. If you do not know whether you have an alpha- or beta-linkage, make an educated guess based on what similar glycan/monosaccharides are using, again seeing this from finding similar glycans in Glyprot. 

**Be very careful with this linkage information!** The same monosaccharide may have different linkage information, for example all terminal monosaccharides have different linkages than any non-terminal monosaccharides. You can determine linkage information by examining the monosaccharide and labeling it in pymol. 

4\. Find the same three-letter code in the appropriate GLYCAM prep file, again from this [site](<http://glycam.org/docs/forcefield/all-parameters/>). Once again, mine was GLYCAM_06h-1.prep. Copy theinfo you find into the force field data file you copied in step 1. You can leave out the header lines, dummy atoms and the loop etc lines after the block of text. 

5\. Replace the numbers on the far left of your now-copied text with the three letter monosaccharide code you found in step 4. Align the first column of atom identifiers (i.e. C1) with the first column of atom identifiers in your force field file. Yank the second column of atom identifiers in your now-copied text to line up with the far right identifiers in the force field file (i.e. Cg). Also, make sure to have the monosaccharide naming in the AMBER.DAT file to be the same as in the pdb, i.e. MN3 (pdb default) not 3MA (equivalent GLYCAM default) 

It is important to be straight with which column you are using in the prep file. Use the column with the lowercase letters in the prep file to map to the .dat file radii. There will be confusing cases such as where the first column says "H1" but the second column says "H2", and but since the "H2" column is the one with lowercase letters, use the "H2" radius. This is because the .dat file contains only the lowercase column. 

6\. Delete the rest of the information except keep the far right column of numbers in your now-copied text; this is the partial charge information from GLYCAM. 

7\. One by one, copy the radii from the bottom of the appropriate [GLYCAM parameter file](<http://glycam.org/docs/forcefield/all-parameters/>) The radii is the first/larger column of numbers in the parameter file. Match up the radii with the appropriate atom identifiers in your edited force field file. 

8\. Try creating the pqr file, by doing pdb2pqr.py --userff=USER_FIELD_FILE --usernames=USER_NAME_FILE --apbs-input --with-ph=7.0 --ph-calc-method=propka --verbose --summary USER_FILE.pdb USER_FILE.pqr and of course replacing the all caps files with your own files. This is assuming you want an APBS input (needed for Browndye) and want to assign protonation states to your protein, which you probably do. Set it to whatever pH you need. 

9\. This should create an imperfect pqr, which will have some atoms still not recognized by pdb2pqr. Note down each atom that isn't recognized. Also, note down which atoms in the GLYCAM prep file were not used in recognizing glycan atoms in your pdb. Create a list of these for each glycan (i.e. one column with the atoms not recognized, and one column with the atoms left over from the parameter file). Do this by looking in the newly-created pqr to see which atoms were used and recognized, and then in the prep file to see which were not used. 

10\. Open up your protein with glycans in pymol, and temporarily delete everything except the first monosaccharide that isn't fully recognized. Select it, right click, and label the atoms in the monosaccharide. Using your lists from step 9, match up each unrecognized atom to an unused atom from the GLYCAM parameter file. Using logic, naming information, charge information, radius information etc this should not be too hard to do. For example, I had a C7 in my pdb that was not recognized by the parameter file. Looking at the pymol structure, C7 was on the other side of the single nitrogen as C2. The GLYCAM parameter file lists a C2N that previously did not match up with anything in the pdb. Logically, C2N in the parameter file matches up with the C7 of the pdb. 

If you run into the issue where the lists contain different numbers of atoms, do not panic. That simply means that your pdb has multiple atoms with the same identifier. If this happens, you need to: 

(a) Comment out one of the identical atoms, then open it up in pymol and see which one it is (b) Give both (or at least one) of the atoms different names. This protocol will not work if all atoms in each molecule do not have distinct names. Take a deep breath, you can now move on. 

11\. Once you have created pairs and matched up all the unrecognized atoms, enter this information in the the naming file you copied in step 1. Simply follow the format already in the naming file to add more entries, this is not hard to do. 

12\. Saving everything, you should now be able to have PDB2PQR recognize your glycans. 

13\. Live long and prosper. 

  


  
Protocol created by Christian Seitz with copious help from Robert Konecny, Mindy Huang, Lorenzo Casalino, Dan Mermelstein, and others.
