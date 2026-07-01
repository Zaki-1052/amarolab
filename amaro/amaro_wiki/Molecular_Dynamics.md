# Molecular Dynamics

## Obtaining Stuctures[edit](</mediawiki/index.php?title=Molecular_Dynamics&action=edit&section=1> "Edit section: Obtaining Stuctures")]

Get your structures from the [Protein Data Bank.](<http://www.rcsb.org/pdb/home/home.do>) Use the search tool to look for relevant and related structures. 

## Building the System[edit](</mediawiki/index.php?title=Molecular_Dynamics&action=edit&section=2> "Edit section: Building the System")]

  * By all means, use the precompiled [PDBREPORT](<http://swift.cmbi.ru.nl/gv/pdbreport/>) to find out what problems there might be with the structure.
  * You can also upload to the Richardson lab's [Molprobity](<http://molprobity.biochem.duke.edu/>) for an evaluation of the PDB structure.
  * [WHAT IF](<http://swift.cmbi.kun.nl/whatif/>) can be used to add polar and aliphatic hydrogens.
  * The UHBD pKa calculation determines the protonation states of the ionizable residues. The preferred procedure is to use WHAT IF to add the hydrogens first, then run the UHBD pKa calculation, compare the results, and make the necessary adjustments.
  * [Reduce](<http://kinemage.biochem.duke.edu/software/reduce.php>) is useful to add protons because it examines the local environment of histidine residues. If you ran Molprobity, it is part of the computation and you can download the hydrogenated PDB file. 
  * You can also download a precompiled standalone executable from the Reduce page. Reduce will also suggest whether the side chain amine, oxygen and nitrogen atoms in glutamine and asparagine are correctly oriented or should be flipped (the orientation cannot be determined from only electron density). The precompiled source works well on our Linux desktops. Run it with the --build option to flip histidines and side chains and add polar and aliphatic hydrogen atoms.
  * After running Reduce, the PDB file will have to be edited to change the histidine names, depending on the force field you plan on using (heating and equilibrating, sampling conformations, or studying dynamics).
