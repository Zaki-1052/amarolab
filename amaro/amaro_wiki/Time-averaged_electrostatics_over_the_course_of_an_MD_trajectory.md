# Time-averaged electrostatics over the course of an MD trajectory

## Averaging APBS frames over the course of a trajectory[edit](</mediawiki/index.php?title=Time-averaged_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=1> "Edit section: Averaging APBS frames over the course of a trajectory")]

[APBS User's Guide](<http://www.poissonboltzmann.org/apbs/user-guide>)

The adaptive Poisson-Boltzmann solver (APBS) program package can compute the protein electrostatics for any static structure. What if you want to know the average electrostatic field that the protein exhibits over the course of the trajectory? 

APBS is an Poisson-Boltzmann equation solver package that uses parallel adaptive finite-element methods. All of these features make APBS very attractive as a solver. 

APBS has been built to allow parallel calculations by breaking the regions of space around the structure into partitions, each of which has the electrostatics calculated for that region. Afterward, the user may stitch the individual electrostatic maps (.dx files) together by using the **mergedx** program. 

Although APBS is utilizes parallel calculations, they do not all need to be performed at the same time on a cluster. The parallel runs can be calculated _asynchronously_ on a single core using the "async" option. 

### InputGen[edit](</mediawiki/index.php?title=Time-averaged_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=2> "Edit section: InputGen")]

APBS requires an input file and a PQR structure to run. The PQR structure may be prepared from a PDB file using the program **pdb2pqr**. 

**inputgen** can be found in the **pdb2pqr** package:
