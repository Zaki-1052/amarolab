# Brownian Dynamics with Browndye

## Getting Acquainted with BrownDye[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=1> "Edit section: Getting Acquainted with BrownDye")]

BrownDye is a program used to perform Brownian Dynamics simulations. It gives you the 2nd-order association rate constant and the reaction probability of the encounter of two molecules. The two molecules are modeled as rigid bodies and the solvent is modeled as a continuum electrostatic field(implicit solvent). 

### Paper[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=2> "Edit section: Paper")]

BrownDye was developed by Gary Huber in the McCammon lab. For more information on the development of BrownDye, refer to the [[paper](<http://ac.els-cdn.com/S0010465510002559/1-s2.0-S0010465510002559-main.pdf?_tid=75e77e32-defa-11e4-87db-00000aab0f27&acdnat=1428612983_685c04f77614181ac37037181be69365>)] by Huber and McCammon. 

### Documentation[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=3> "Edit section: Documentation")]

Refer to the [[documentation manual](<http://browndye.ucsd.edu/browndye/doc/manual.html>)] for an explanation of the functionality of the programs. 

### Tutorial[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=4> "Edit section: Tutorial")]

For an example tutorial, refer to the BrownDye [[tutorial page](<http://browndye.ucsd.edu/browndye/thrombin-example/tutorial11.html>)] 

## Setting up your system for simulation[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=5> "Edit section: Setting up your system for simulation")]

BrownDye requires the following files as input to run BD simulations: 

1\. PQR files- molecular structure with charge and radius parameters 

2\. Electrostatics files- description of the electrostatic potential of each molecule 

3\. Encounter complex description- atomic interactions between two molecules 

4\. Input file for Browndye- Description of simulation including file names, number of iterations, and output 

### Creating your PQR Files[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=6> "Edit section: Creating your PQR Files")]

Since BrownDye uses electrostatics as the major force influencing diffusion, the program requires a charge and radius description of your molecule. After you download your file from the PDB database, you can create a PQR file in one of two ways: 

#### PDB2PQR[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=7> "Edit section: PDB2PQR")]

-Upload your pdb file into the [[PDB2PQR server](<http://nbcr-222.ucsd.edu/pdb2pqr_2.0.0/>)] 

-Choose the name of your forcefield input and output 

-In available options, make sure you check off "Create an APBS input file" and "Insert whitespaces between atom name and residue name, between x and y, and between y and z" 

-If you haven't titrated your protein, you can also choose to use the PROPKA to assign protonation states at a certain pH 

  
The server will output two files that you will use in the next step: 1) A .pqr file with the charge and radius parameters and 2) An APBS .in file that specifies the electrostatic properties of your molecule for use with APBS 

#### AmberTools[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_Browndye&action=edit&section=8> "Edit section: AmberTools")]

If PDB2PQR gives you errors, an alternative approach is to use Amber to create your PQR files. You may also want to use this approach if you have small molecules in your structure that need special parameterization (like ions or small organic molecules) 

You can use Amber to create .prmtop and .inpcrd files 

Then, you can run the following command: ambpdb -p name.prmtop -pqr <name.inpcrd> name.pqr
