# CYP MD IN CHARMM

## Building a CYP membrane system with the CHARMM force field[edit](</mediawiki/index.php?title=CYP_MD_IN_CHARMM&action=edit&section=1> "Edit section: Building a CYP membrane system with the CHARMM force field")]

__**THIS PAGE IS CURRENTLY UNDER DEVELOPMENT**__

  * **[CYP Group Utilities](<http://amarolab.ics.uci.edu/Public/CHARMM/>) \- Topology and Parameters for CHARMM 27 that include heme and necessary patches as CYSA and FHEM, sample CHARMM input files "heme.inp" illustrating the application to PDB inputs for 1TQN (substrate-free 3A4).**


  * Basic documentation on CHARMM [Topology files](<http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node22.html>) and [Parameter files](<http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node23.html>)
  * Documentation on [CHARMM software](<http://www.charmm.org/documentation/c35b1/index.html>)
  * [OPM database](<http://opm.phar.umich.edu/>) provides some PDB files for membrane proteins aligned to the predicted membrane position



### Important items needed for build[edit](</mediawiki/index.php?title=CYP_MD_IN_CHARMM&action=edit&section=2> "Edit section: Important items needed for build")]

  1. Patch for heme CHARMM parameters, residue HEME
  2. Patch for cysteine (number 442 in P450 3A4) to cysteinate (a thiolate)
  3. Patch for S-Fe bond for CYS to HEME residue



### Lipid parameters and membrane building[edit](</mediawiki/index.php?title=CYP_MD_IN_CHARMM&action=edit&section=3> "Edit section: Lipid parameters and membrane building")]

  * Original CHARMM C36 parameters and patches [CHARMM ff params page (UMaryland)](<http://mackerell.umaryland.edu/CHARMM_ff_params.html>)
  * Our modified CHARMM inputs and top/par files for CYP (NAMD-compatible data) are [HERE.](<http://amarolab.ics.uci.edu/Public/CHARMM/lipid_C36>)
  * Membrane building - orientation of protein in lipid bilayer, adding lipid and also solvating system with water and ions


  1. [OPM database](<http://opm.phar.umich.edu/>) protein orientation data
  2. [Membrane Builder](<http://www.charmm-gui.org/?doc=input/membrane>) Sample script generator for CHARMM using OPM PDB files, other tools for generating CHARMM inputs



### Biologically relevant waters[edit](</mediawiki/index.php?title=CYP_MD_IN_CHARMM&action=edit&section=4> "Edit section: Biologically relevant waters")]

  * In the substrate-free P450, there is an essential water bound to the heme iron, thus Iron (Fe) has octehedral geometry. Drugs coordinate at this iron as well, displacing the bound water.
  * Numerous other waters exist in the crystal structures within the binding pocket and this hydration must be properly incorporated in simulation.



## Production runs with NAMD[edit](</mediawiki/index.php?title=CYP_MD_IN_CHARMM&action=edit&section=5> "Edit section: Production runs with NAMD")]

  * Required inputs, assembly.XPLOR.PSF and assembly.PDB for your resulting protein-membrane assembly
  * Sample MD NAMD input configuration file "mdrun.namd" found in [[group utilities folder](<http://amarolab.ics.uci.edu/Public/CHARMM/%7CCYP>)]
