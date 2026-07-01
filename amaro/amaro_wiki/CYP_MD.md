# CYP MD

**Note** : Everything <in between less/more than symbols> needs to be specified by the user. 

Adam: 2C8 & 2C9 

Tiffany: 1A2 & 3A4 

Jason: aromatase 

## Pre-MD[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=1> "Edit section: Pre-MD")]

### Make a PowerPoint about the enzyme(s)[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=2> "Edit section: Make a PowerPoint about the enzyme\(s\)")]

  1. Find research articles online about the particular cytochrome(s) you are studying. 
     1. The [RCSB Protein Data Bank](<http://www.pdb.org/pdb/home/home.do>) is a good place to start.
     2. Another good place you should visit is called [PubMed](<http://www.ncbi.nlm.nih.gov/pubmed/>) . This website lists all the articles about the cytochrome P450's (for the most part). To find articles about your particular cytochrome, type "cytochrome 3A4", "cytochrome 1A2", etc. in the search box. Sift through the resulting articles to find ones that you think are useful / interesting. 
  2. Search for all the different P450 structures of your assigned kind in the PDB database (e.g. search for "cytochrome 3A4" or "cytochrome 1A2") 
     1. write down all the PDB identifiers (4 character descriptor of each structure in the PDB)
     2. for each structure: 
        1. download it
        2. open it in VMD and check it out
        3. print out and read carefully through the primary citation associated with the PDB entry (do this for each one)
        4. is there anything unique about this structure? (this will probably be highlighted in the primary citation)
        5. YOU are the expert for your particular P450... write down everything you think will be important to know about your protein
  3. Describe the different hemes 
     1. What are they? Which ones have which? Etc.
  4. How would the substrates/inhibitors gain entry? 
     1. Are the structures closed? Open? What about any channels?
  5. Where are the cytochromes located? In the liver? 
     1. What is the pH there?
  6. Make the sure the structure is complete 
     1. Look to see if there are missing residues, breaks in the protein chain, etc.
     2. In places where structure is missing, keep track of this so we really know what is going on.
  7. Look at the water molecules 
     1. How many are around the heme?
     2. How many are inside the protein?
  8. Are there any ions? 
     1. What are they? Where are they? How many are there? Etc.
  9. Are the chains mostly the same? 
     1. Compare in VMD (multiseq)
     2. Keep track of major differences



## Setting the pH[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=3> "Edit section: Setting the pH")]

Before setting the pH, identify all histidine residues (if any), and write their resid's in a list. We need to predict the protonation state of each histidine in the protein, and must rename them for AMBER. 

  * Open the pdb file in VMD
  * Save the selection: 
    * Open the TK Console
    * At the prompt make the selection by typing:


    
    
    set sel [atomselect top "<changes to the original pdb file>"] 

For example, entering "chain A" will select chain A of the cytochrome protein. Any specific modifications such as excluding the heme group from the selection or excluding ions should also be made now. If there are any incomplete residues, you may also want to get rid of them. 

ie. There was a lone nitrogen from a histidine residue at the end of the chain A sequence. I used "chain A and not (resname HEC or HIS 491)" to select chain A, get rid of the heme and to get rid of the incomplete histidine residue.. 

  * Write the selection to a _pdb_ file by typing:


    
    
    $sel writepdb <filename>.pdb
    

  * Run PDB2PQR 
    * Go to <http://kryptonite.nbcr.net/pdb2pqr/>
    * Scroll down and select Upload a PDB, then browse to select the _pdb_ file you created above.
    * Select the Amber force field
    * Select Amber for the output naming scheme
    * For the available options, be sure the top three are selected. In the box for PROPKA, type pH 7: Use PROPKA to assign protonation states at pH 7
    * Click Submit.



## Preparing the System for AMBER[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=4> "Edit section: Preparing the System for AMBER")]

The AMBER naming/number scheme differs slightly. Before loading the molecule into AMBER, some things need to be adjusted. These things are: 

  * Disulfide bonded cysteine residues
  * Residues
  * TER cards



### Disulfide Bonds[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=5> "Edit section: Disulfide Bonds")]

Rename CYS to CYX for disulfide bonded CYS residues. To see which cysteines are in disulfide bonds, view all cysteines in VMD and visually determine which are in contact with one another. The sulfide groups will be pointing at each other and will be within ~2.5 A of each other. Make note of the residue numbers. 

### Protonated/Deprotonated Residues[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=6> "Edit section: Protonated/Deprotonated Residues")]

When the macromolecule is processed in the NBCR PDB2PQR server, some amino acids are protonated or deprotonated and the PDB2PQR server changes the last letter of three letter amino acid code to N (deprotonated) or H (protonated). These name changes may be changed back before processing in AMBER. For example: any lysine with the three letter code _LYN_ would be changed to _LYS_. 

Known culprits are: 

  * GLH (protonated GLU)
  * LYN (deprotonated LYS)
  * ASH (protonated ASP)
  * ARN (deprotonated ARG)



Wait for the file to be processed in PDB2PQR and when it's finished, click on the first link, the file with the _.pqr_ extension. Open and look at this file in a text editor. Notice that it has comments at the top. Scroll down and see the protonation states assigned to the various residues. If any of the residues listed above are protonated or deprotonated, you can change them back to their original names. Write down the resid of all changed residues. To change residue names: 

  * Open the _pdb_ (NOT the _pqr_) in VMD
  * Open the TKConsole and type:


    
    
    set sel [atomselect top "resid <residue IDs of protonated/deprotonated residue(s)> and protein"] 

This command sets the selection named "sel" to the residues that you would like to change in the protein. Make sure the resid's you enter are all for the same residue. Next, type: 
    
    
    $sel get resname 

This command will list the residue names associated with each atom in the selection. It's just to make sure you selected the correct residues. Now, enter: 
    
    
    $sel set resname <original resname of residue before alteration> 

By entering this command, the "sel" selection resname will be changed to the original resname prior to using PDB2PQR. 

Also, you must change the name of all the protonated histidines in the original _pdb_ so AMBER can recognize them as protonated. Follow the exact same steps as above, but instead of entering the orignal resname of the altered residues in the last step, enter either HID, HIE or HIP, depending on what PDB2PQR predicted. This will assign each histidine the correct predicted protonation state. XLeap will add the hydrogens in the next step. 

When you are finished changing the residue names, including all of the histidines, rename the file with a _.pdb_ extension: 
    
    
    [atomselect top "all"] writepdb <new pdb filename>.pdb 

### TER Cards[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=7> "Edit section: TER Cards")]

TER cards are inserted to separate protein from ions from water: 

  * Add TER between protein and ions
  * Add TER between ions and water
  * If there are no ions, add TER between protein and water



In addition, when working with cytochromes containing substrate or heme, you also need to add TER to seperate the rest of the file from them. This can be done in a text editor - open the _pdb_ with gedit and simply add TER on a seperate line where needed. Don't forget to save! 

## Editing PDB Using AMBER[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=8> "Edit section: Editing PDB Using AMBER")]

### Open XLeap[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=9> "Edit section: Open XLeap")]

Make sure that you've visited the [Getting Started](</mediawiki/index.php/Getting_Started> "Getting Started") page and have completed step 4. Chagning the .tcshrc file is important because the environment for XLeap & AMBER has already been set in the new one. 

Before launching XLeap, make sure all _pdb_ files and any parameter files are in the same directory that XLeap is launched from. Make sure NUMLOCK is off. Launch XLeap: 
    
    
    $AMBERHOME/exe/xleap -s -f $AMBERHOME/dat/leap/cmd/leaprc.ff99SB 

This will launch XLeap with the ff99SB forcefield. 

### Load Macromolecule[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=10> "Edit section: Load Macromolecule")]

The prepared macromolecules are now ready to be loaded into AMBER. Make sure you load the pdb that's been most recently modified (with TER cards, changed residues, etc). 
    
    
    <name> = loadpdb <pdb>.pdb 

If the file is loaded correctly, you should receive no error messages. 

### Set Disulfide Bonds[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=11> "Edit section: Set Disulfide Bonds")]

When the macromolecule is loaded into XLeap, some re-numbering may occur. Before setting the disulfide bonds, we must check new numbering of the CYX residues. 

To display all residues and their new residue numbers, type: 
    
    
    desc <name> 

This will output all residues. Search through the list for CYX residues and make note of the new resid's. The numbers should be the same or close to the numbers noted in VMD. 

Finally, for each CYX pair (if there are any), set the disulfide bond by typing: 
    
    
    bond <name>.<resid>.SG <name>.<other resid>.SG 

You can only set one bond at a time. 

### Add Neutralizing Counterions[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=12> "Edit section: Add Neutralizing Counterions")]

If the system is not neutral, Na+ or Cl- ions will need to be added to balance the charge. AMBER can automatically add necessary ions. 

Type the following commands into the prompt: 
    
    
    addions <name> Na+ 0 

OR 
    
    
    addions <name> Cl- 0 

If ions are needed, they will automatically be added and a message will appear. If they are not needed, nothing will happen. If it turns out that the charge needed is the opposite of what you entered, a message will appear telling you to add the opposite charged ions. 

### Add Solvent Box[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=13> "Edit section: Add Solvent Box")]

The macromolecule must be solvated. Solvent can be automatically added by the TIP3P tool in AMBER. Type: 
    
    
    solvatebox <name> TIP3PBOX 10.0 

Note: After solvation, residues will be renumbered by AMBER. 

### Write Output Files[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=14> "Edit section: Write Output Files")]

Save the _prmtop_ and _inpcrd_ files: 
    
    
    saveamberparm <name> <other name>.prmtop <other name>.inpcrd 

#### Adding Salts[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=15> "Edit section: Adding Salts")]

  * These steps are **optional**



The system will be simulated in 20 mM NaCl (salt solution). Therefore, Na+ and Cl- ions will need to be added arbitrarily to the system. This is done by replacing a number of existing water molecules with either Na+ or Cl-. 

### Measure Box Dimensions[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=16> "Edit section: Measure Box Dimensions")]

In order to calculate how many ions should be added, the dimensions of the system must be measured. 

  * Open AMBER parameter files in VMD 
    * prmtop > Amber7 PARM
    * inpcrd > Amber7 RESTART
  * Open VMD TK Console
  * At the prompt, type the following:


    
    
    set sel [atomselect top all]
    measure minmax $sel
    

To calculate the box size, subtract the maximum XYZ coordinates by the minimum XYZ coordinations. Multiply to calculate the volume. 

### Calculate Number of Atoms to Add[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=17> "Edit section: Calculate Number of Atoms to Add")]

To achieve a 20 mM NaCl solution, use the following formula to determine the number of NaCl ions to add to the system: 
    
    
    (0.02 mol/L)(1E-27 L/Angstrom)(Volume)(6.022E23 atoms/mol) = # atoms
    

If the calculated number is a fraction, use your judgment to round to a whole number. Keep in mind that, for this system, one ion was already added for neutralization. 

### Place Na+/Cl- Ions[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=18> "Edit section: Place Na+/Cl- Ions")]

Water molecules are selected arbitrarily and replaced with Cl- or Na+. Selections should be evenly spaced and within 9 A of the protein. Changes are entered manually into the _pdb_ using the following format/naming: 
    
    
    Na+ Na+ ###
    Cl- Cl- ###
    

When finished, the file is saved as <other name>-salts.pdb. 

### Respecify Disulfide Bonds[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=19> "Edit section: Respecify Disulfide Bonds")]

Upload the finished file to kryptonite and respecify the disulfide bonds using AMBER/XLeap. Again, the file must be in the same direction from which XLeap is launched. Parameter files (for calcium) must be loaded before loading the system. 

Keep in mind the numbering has now changed. Check the numbering and specify bonds accordingly: 
    
    
    desc sys
    bond sys.##.SG sys.##.SG
    

Save the _prmtop_ , _incprd_ , and _pdb_ file when done. 

### Check Work[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=20> "Edit section: Check Work")]

Before proceeding, check the preparation steps complete thus far. 

  * Open _< name>.incprd_ and _< name>.prmtop_ in VMD


  1.      1. Check for ions (mass < # and mass > #)
     2. Check disulfide bonds



## Prepare system for MD (Section update 6/30/11)[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=21> "Edit section: Prepare system for MD \(Section update 6/30/11\)")]

CHARMM-GUI is an alternative way for building the system. However, the system cannot recognize things like heme, drug, or inhibitor. Therefore, those items have to be built in afterwords. 

### Using CHARMM-GUI for system with membrane:[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=22> "Edit section: Using CHARMM-GUI for system with membrane:")]

  1. Go to <http://www.charmm-gui.org/?doc=input/membrane>.
  2. Enter four digits PDB ID and select OPM for download source,then click next. OPM orient the protein parallel to Z axis. 



The pdb file includes DUM values that form two thin plates, suggesting where membrane should be. For additional information on the OPM file,visit [[[1]](<http://opm.phar.umich.edu/>)]. 

  1. Follow the steps.
  2. Download the _charmm-gui.tgz_ files at the end of the step.
  3. Follow the instructions below for Minimization/Equilibration.



### Using CHARMM-GUI for system in a water box:[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=23> "Edit section: Using CHARMM-GUI for system in a water box:")]

  1. Go to <http://www.charmm-gui.org/?doc=input/solvator>.
  2. Enter four digits PDB ID then click next.
  3. Select the protein only.
  4. Skip to next step.
  5. Select the size of the water box. e.g. Edge Distance: 50.
  6. Include ions. e.g.~150-250 ions total.
  7. Hit next step. The program starts the calculation for the water box. It may take some times for the calculation work to be done.
  8. Download the _charmm-gui.tgz_ files at the end of the step. 
  9. Patch the missing parts.
  10. Follow the instructions below for Minimization/Equilibration.



## Performing the MD[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=24> "Edit section: Performing the MD")]

### Energy Minimization[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=25> "Edit section: Energy Minimization")]

Now we are ready to begin simulation. First the system must undergo energy minimization. Energy minimization will be performed in four steps in which atoms are gradually allowed to move. 

  * The first step holds everything fixed and allows only hydrogens to move.
  * The second step lets hydrogens, waters and ions move.
  * The third step lets hydrogens, waters, ions and sidechains to move.
  * The fourth step lets everything move.



For each step, a fixed atom file is needed that specifies which atoms are allowed to move. This is done by specifying a 1 or 0 in the occupancy column of the _pdb_ file. Fixed atoms have an occupancy of 1. Free atoms have an occupancy of 0. 

If there is a ligand bound to the system, the hydrogens of the ligand should be allowed to move with the rest of the system hydrogens. The rest of the ligand should be held fixed until after the sidechains have moved. 

### First Fixed Atom File[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=26> "Edit section: First Fixed Atom File")]

  * Load the _prmtop_ & _inpcrd_ files into VMD



Before we write the fixed atom files, we should save the parameter and topology files together in a _pdb_. 

  * Open VMD TKConsole. Enter:


    
    
    set sel [atomselect top "all"]
    $sel writepdb <name>.pdb
    

  * Write first fixed atom file - free hydrogens.


    
    
    set sel1 [atomselect top "all"]
    set sel2 [atomselect top "hydrogen"]
    $sel1 set occupancy 1
    $sel2 set occupancy 0
    $sel1 writepdb fxd1.pdb
    

Check the _pdb_ file. It should have 0 after every free hydrogen and 1 everywhere else. 

### Second Fixed Atom File[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=27> "Edit section: Second Fixed Atom File")]

  * Write second first atom file - free hydrogens, waters, and ions. If there are no ions in your system, don't add anything for ion specifications.


    
    
    set sel2 [atomselect top "hydrogen or water or <ion specifications>"]
    $sel2 set occupancy 0
    $sel1 writepdb fxd2.pdb
    

### Third Fixed Atom File[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=28> "Edit section: Third Fixed Atom File")]

  * Write third fixed atom file - free hydrogens, waters, ions and sidechains.


    
    
    set sel2 [atomselect top "hydrogen or water or <ion specifications> or sidechain"]
    $sel2 set occupancy 0
    $sel1 writepdb fxd3.pdb
    

The fourth minimization lets everything move and therefore does not require a fixed atom file to be written. 

### Re-measure Box Dimensions[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=29> "Edit section: Re-measure Box Dimensions")]

The NAMD files require box dimensions and coordinates of the box center. (The numbers will have changed from the previous measurements, but the dimensions should be the same.) 

Before running the scripts, some user specified parameters are needed for them. Do the following: 

  * Open AMBER parameter files in VMD 
    * _prmtop_ file -> Amber7 PARM
    * _inpcrd_ file -> Amber7 RESTART
  * Open Charmm parameter files in VMD 
    * _psf_ file -> similar to prmtop file in amber 
    * _pdb_ file -> similar to inpcrd file in amber


  * Open VMD TK Console. Type:


    
    
    set sel [atomselect top all]
    measure minmax $sel
    measure center $sel
    

Make note of the center coordinates (cellOrigin) and the min/max values. The coordinates of the box center should be very close to 1/2 of the XYZ coordinates. To calculate the box size (cellBasisVector values), subtract the minimum XYZ coordinates from the maximum XYZ coordinates. 

### Running NAMD[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=30> "Edit section: Running NAMD")]

To open NAMD: First, open each of the the MD Equilibration Scripts below using gedit. Save them as .inp files. (minimization1.inp, minimization2.inp, etc.) 

### Scripts[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=31> "Edit section: Scripts")]

All scripts can be found on the page [Generic MD Equilibration Scripts](</mediawiki/index.php/Generic_MD_Equilibration_Scripts> "Generic MD Equilibration Scripts")

In general, the scripts are the same with the following important differences for the successive minimizations: 

  * min_1: 
    * minimize - 5000
    * fixedAtomFile - fxd1.pdb
  * min_2: 
    * minimize - 5000
    * fixedAtomFile - fxd2.pdb
  * min_3: 
    * minimize - 10000
    * fixedAtomFile - fxd3.pdb
  * min_4 (all): 
    * minimize 25000
    * no fixedAtomFile



To run the scripts: 

First make sure that the all of the parameters with "*" next to them are specified: 

**output file**

  * Choose a name for the output file. I would recommend keeping all the names the same for each minimization step.



**input file**

  * Only in the last 3 minimization steps. Use the name of the previous minimization without any extensions.



**_prmtop_ & _inpcrd_ files**

  * Use the _prmtop_ & _inpcrd_ files that you made in XLeap for all four minimizations.



**cell basis vectors & cell origin**

  * Enter the values you got from re-measuring the box dimensions where indicated.
  * Only in the **first** minimization step do box center and size need to be specified.



All other parameters are pre-set and will stay the same for all four energy minimizations. For reference or more info on these parameters, see the [NAMD tutorial](<http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node8.html>). 

After you've specified everything, save this with a _.inp_ extension. 

Here is the bash file you will need to run the script: 
    
    
    #!/bin/bash
    
    CHARMRUN=/pkg/namd/2.7b1/charmrun
    NAMD=/pkg/namd/2.7b1/namd2
    NSLOTS=6
    inputfile=./<inputfile>.inp
    outputfile=./<outputfile>.out
    
    ${CHARMRUN} ++local +p ${NSLOTS} ${NAMD} ${inputfile} >& ${outputfile} &
    

Save this in the same directory that the other files being used are with a //.bash// extension. The //inp// file you just created will be the input file. 

Type: 
    
    
     module load namd2
     bash <filename>.bash
    

### Alternatively:[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=32> "Edit section: Alternatively:")]

You can use the command below to specify the number of processors and run NAMD directly from the Terminal: 
    
    
    /pkg/namd/2.7b1/charmrun ++local +p {# of processors you choose} /pkg/namd/2.7b1/namd2 {your NAMD script} > & {the name of your output file}.out &
    

You can check on the job and view the end of the output file (_.out_) by entering: 
    
    
    tail -f <output filename>.out 

Each minimization step will take longer than the one before it, with the first one taking about 20 minutes on 6 processors. 

## Harmonic Constraints[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=33> "Edit section: Harmonic Constraints")]

After energy minimizations are completed, the next step is to set harmonic constraints. The _min_4_ file from energy minimizations is fed into the first harmonic constraint script, _hc_eq_1_. There are four steps of harmonic constrains, each slightly less constrained than the one before. 

### Restrain Backbone[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=34> "Edit section: Restrain Backbone")]

In the same window on TKConsole, reset all occupancies to 0. Then select the backbone and set the occupancy for the backbone to 4. Write this file. 
    
    
    $sel1 set occupancy 0
    set sel2 [atomselect top "backbone"]
    $sel2 set occupancy 4
    $sel1 writepdb restrain_backbone_ref.pdb
    

In the _pdb_ file, everything should be 0 except for the backbone, which should be at 4. 

### Scripts[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=35> "Edit section: Scripts")]

The harmonic equilibration scripts can be found here: [Generic MD Equilibration Scripts](</mediawiki/index.php/Generic_MD_Equilibration_Scripts> "Generic MD Equilibration Scripts")

There is one new parameter that must now be specified: 

**PME grid size**

  * The box dimensions must be a multiple of 2 or 3. Take each coordinate of the box size (cellBasisVectors), and choose a number that is close-to and preferably equal-to or slightly larger than each of them. Enter these as your PMEGridSizeX, Y and Z values, corresponding to the cellBasisVectors 1, 2 and 3, respectively.



Make sure to specify all the PME stuff, in addition to the other parameters listed under the energy minimization scripts. Also, you do not need to specify any of the cell basis vectors - this information is contained in the restart coordinate input file. 

You probably want to run all of the equilibration on a supercomputer because it takes considerably longer to run than the minimization. See [SuperComputing](</mediawiki/index.php/SuperComputing> "SuperComputing") for instructions. Follow the same steps as the EM, but instead of the bash file listed above, use the files under NAMD in the [SuperComputing](</mediawiki/index.php/SuperComputing> "SuperComputing") page. 

Parameters that need to be changed are: your_job_name, your_que, number_of_nodes, processors_per_node, input and output. You may name the job whatever you want. See the GreenPlanet link under the home page of this wiki for detailed queue and GP runtime information. Typically, for every 1000 atoms in a system, 1 processor is used. You can use VMD to find out how many atom the system you are equilibrating has. There are 8 processors per node. 

The scripts for each step are generally the same except for the constraintScaling option. This value changes as the system becomes less constrained. 

  * hc_eq_1: 
    * constraintScaling - 1.0
  * hc_eq_2: 
    * constraintScaling - 0.75
  * hc_eq_3: 
    * constraintScaling - 0.50
  * hc_eq_4: 
    * constraintScaling - 0.25
  * eq: 
    * constraintScaling - 0



The final step (eq) allows the whole system to move. Naturally, each step will take longer than the step before it with the final step taking the longest. 

Note: In the test scripts, the 1-4scaling is set to 0.833333. This is specific to using Amber force fields with NAMD and should be set to 1.0 if you are following part of this tutorial but using CHARMM. 

#### Check Results[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=36> "Edit section: Check Results")]

After completion of the final equilibration step, all the minimization and equilibration outputs should be concatenated chronologically into one large file, starting with the first energy minimization and ending with the free equilibration. 

  * Load _.dcd_ files for minimizations and equilibration into VMD
  * Play
  * Check for errors (i.e. big movements) 
    * Check water only
    * Check protein only
  * Extensions > Analysis > RMSD Trajectory Tool 
    * Check average
    * Check standard deviation
  * File > Plot Data 
    * Options > Multiplot
    * RMSD less than 1 is good
  * Backbone RMS should be less than total RMSD



If all the criteria are met, you may commence with free dynamic simulations. 

## Free Dynamics[edit](</mediawiki/index.php?title=CYP_MD&action=edit&section=37> "Edit section: Free Dynamics")]

If all previous steps were completed and the system looks good in equilibration, then we can proceed to free dynamics. Free dynamics starts with the output of the free equilibration and continues until you decide to stop. 

  * Make new directory
  * Copy the following files into the new directory: _prmtop_ , _inpcrd_ , _coor_ and _xsc_
  * See templates from previous MD simulations
