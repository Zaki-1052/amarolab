# NAMD MD Minimization and Equilibration

## Editing the Macromolecule[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=1> "Edit section: Editing the Macromolecule")]

At the end of this step, the system will contain: 

  * The monomer of 2HU4 set at pH 6.5
  * Calcium in/near the binding site
  * Water molecules withint 5 A of the protein 



### Selecting the Monomer[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=2> "Edit section: Selecting the Monomer")]

The macromolecule is a monomer of neuraminidase N1 in the closed loop conformation (2HU4). The original PDB contains a tetramer of neuraminidase, but only one monomer is needed in this case. The crystal structure also contains Tamiflu (oseltamivir), but it is also not needed in this example. 

  * Launch VMD 
  * Load _2HU4_
  * Select _chain B_
  * Set display type to _New Cartoon_



Alternatively, one could manually copy/paste _chain B_ directly from the original PDB file and save this to a new PDB file. 

### Set the pH[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=3> "Edit section: Set the pH")]

First, save the selection: 

  * Open the TK Console
  * At the prompt make the protein selection by typing:


    
    
    set prot [atomselect top "chain B"]
    

  * Then write the selection to a pdb file by typing:


    
    
    $prot writepdb 2HU4_B.pdb
    

We want the protein to be protonated according to pH 6.5, which is the pH at which the experimentalists will run the inhibition assays. To do this, we will use a tool called PDB2PQR. 

  * Go to [http://nbcr.net/pdb2pqr/](<http://kryptonite.nbcr.net/pdb2pqr/>)
  * Scroll down and select Upload a PDB, then browse to select the _2HU4_B.pdb_ file you created above.
  * Select the Amber force field 
  * Select Amber for the output naming scheme
  * For the available options, be sure the top three are selected. In the box for PROPKA, type 6.5: Use PROPKA to assign protonation states at pH 6.5
  * Click Submit. 



Wait for the file to be processed and when it's finished, click on the first link, the file with the _.pqr_ extension. Open and look at this file in a text editor. Notice that it has comments at the top. Scroll down and see the protonation states assigned to the various histidines and other residues. When you are finished checking it out, rename the file as _2HU4_pH65.pdb_. 

### Add Water Molecules[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=4> "Edit section: Add Water Molecules")]

The 2HU4 crystal structure contains no water. Thus, water must be imported from another system, 2HTY (the apo N1 structure). The water from 2HTY is superimposed on 2HU4. 

  * Load _2HTY_
  * Select _chain B or water within 5 of chain B_
  * Save the selection 
  * Open the output _2HU4_pH65.pdb_ and manually copy/paste the water molecules into the file.



### Add Calcium[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=5> "Edit section: Add Calcium")]

The crystal structure contains calcium ions which many affect the binding properties of the protein. Thus, calcium in or near the binding site should be included. Calcium far away from the binding site can be excluded. 

The monomer of 2HU4 contains one calcium in the binding pocket. 

  * Load _2HU4_
  * Select _resname CAL_
  * Click on the calcium in the binding site to see the resid number
  * Select _resid ###_
  * Open the output _2HU4_pH65.pdb_ and manually copy/paste the calcium ion into the file. The final file is saved _2hu4_wats_ca.pdb_.



## Preparing the System for AMBER[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=6> "Edit section: Preparing the System for AMBER")]

The AMBER naming/number scheme differs slightly. Before loading the molecule into AMBER, some things need to be adjusted. These things are: 

  * Disulfide bonded cysteine residues
  * Lysine
  * Calcium
  * TER cards



### Disulfide Bonds[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=7> "Edit section: Disulfide Bonds")]

Rename CYS to CYX for disulfide bonded CYS residues. To see which cysteines are in disulfide bonds, view all cysteines in VMD and visually determine which are in contact with one another. Make note of the residue numbers. 

The following disulfide bonds are known to be the same for 2hty, 2hu4 and 2hu0. Refer back to these numbers later (it will be helpful in setting the disulfide bonds) ... The first pair of numbers is the residue numbers before AMBER re-numbering. The second pair of numbers is the residue numbers after loading into AMBER. The third set of numbers is after adding the solvent box. 
    
    
    92-417 > 92-417 > 10-335
    124-129 > 124-129 > 42-47
    182-230 > 184-231 > 102-149
    232-237 > 233-238 > 151-156
    278-291 > 279-292 > 197-210
    280-289 > 281-290 > 199-208
    318-336 > 318-335 > 236-253
    421-447 > 421-446 > 339-364
    

### Protonated/Deprotonated Residues[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=8> "Edit section: Protonated/Deprotonated Residues")]

When the macromolecule is processed in the NBCR PDB2PQR server, some amino acids are protonated or deprotonated and the PDB2PQR server changes the last letter of three letter amino acid code to N (deprotonated) or H (protonated). These name changes must be changed back before processing in AMBER. For example: any lysine with the three letter code _LYN_ must be changed to _LYS_. 

Known culprits are: 

  * GLH (protonated GLU)
  * LYN (deprotonated LYS)
  * ASH (protonated ASP) 
  * ARN (deprotonated ARG)
  * Histidines - HIE, HID, and HIP 



### Calcium[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=9> "Edit section: Calcium")]

Rename the lone calcium ion to a form that is recognized by AMBER. 

Thus, 
    
    
    CA 999
    

becomes... 
    
    
    Ca+ CAL X 999
    

### TER Cards[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=10> "Edit section: TER Cards")]

TER cards are inserted to separate protein from ions from water: 

  * Add TER between protein and ions 
  * Add TER between ions and water



## Editing PDB Using AMBER[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=11> "Edit section: Editing PDB Using AMBER")]

Upload the PDB file from the last step onto your directory on Kryptonite. 

### Open XLeap[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=12> "Edit section: Open XLeap")]

XLeap is graphical, so log-in Puzzle/Kryptonite with -Y 
    
    
    ssh -Y username@puzzle.nbcr.net
    ssh -Y username@kryptonite.nbcr.net
    

On kryptonite, AMBER is located in the following directory: 
    
    
    /home/install/usr/src/amber9-mpich-patch
    

This version of AMBER has the latest bug fixes (as of 08/28/07). To make things easier, set variable $AMBERHOME to this directory. 
    
    
    export AMBERHOME=/home/install/usr/src/amber9-mpich-patch
    

Launch XLeap. Before launching XLeap, make sure all _pdb_ files and any parameter files are in the same directory that XLeap is launched from. Make sure NUMLOCK is off. 
    
    
    $AMBERHOME/exe/xleap -s -f $AMBERHOME/dat/leap/cmd/leaprc.ff99SB
    

### Load Parameter Files[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=13> "Edit section: Load Parameter Files")]

In AMBER, parameter files are required for calcium and small molecules. 

In this example, the macromolecule contains one ion of calcium. This requires us to load a file called _cal.prep_ before loading the macromolecule into AMBER. 

The file below is _cal.prep_. 
    
    
    0 0 2
    
    Calcium Ion
    CAL.res
    CAL INT 0
    CORR OMIT DU BEG
    0.000000
    1 DUMM DU M 0 -1 -2 0.0000 0.0000 0.0000 0.000
    2 DUMM DU M 1 0 -1 1.0000 0.0000 0.0000 0.000
    3 DUMM DU M 2 1 0 1.0000 90.0000 0.0000 0.000
    4 Ca+ C0 M 3 2 1 1.0000 90.0000 180.0000 2.000
    
    DONE
    STOP
    

After XLeap is open and before loading the macromolecule, load the parameter files. The cal.prep file can be loaded as follows: 
    
    
    loadamberprep cal.prep
    

If the system contained Tamiflu, additional parameter files would be needed. Those additional parameters could be loaded as follows: 
    
    
    > source leaprc.gaff
    > loadoff tam-rea.lib
    > loadamberparams frcmod.tam
    > loadamberprep  cal.prep
    

It is important to make sure that the .gaff file contains the correct paths. The leaprc.gaff file that has paths specific to kryptonite is located here: 
    
    
    /home/install/usr/src/amber9/dat/leap/cmd/leaprc.gaff
    

### Load Macromolecule[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=14> "Edit section: Load Macromolecule")]

The prepared macromolecules are now ready to be loaded into AMBER. 
    
    
    n1 = loadpdb N1-wats-cal.pdb
    

If the file is loaded correctly, you should receive no error messages. 

### Set Disulfide Bonds[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=15> "Edit section: Set Disulfide Bonds")]

When the macromolecule is loaded into XLeap, some re-numbering may occur. Before setting the disulfide bonds, we must check new numbering of the CYX residues. 

To display all residues and their new residue numbers, type: 

desc n1 

This will output all residues. Search through the list for CYX residues and make note of the new resid. The numbers should be the same or close to the numbers noted in VMD. 

Finally, for each CYX pair, set the disulfide bond by typing: 
    
    
    bond n1.##.SG n1.##.SG
    

You can only set one bond at a time. 

### Add Neutralizing Counterions[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=16> "Edit section: Add Neutralizing Counterions")]

If the system is not neutral, Na+ or Cl- ions will need to be added to balance the charge. AMBER can automatically add necessary ions. 

Type the following commands into the prompt: 
    
    
    addions n1 Na+ 0
    

OR 
    
    
    addions n1 Cl- 0
    

If ions are needed, they will automatically be added and a message will appear. If they are not needed, nothing will happen. 

### Add Solvent Box[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=17> "Edit section: Add Solvent Box")]

The macromolecule must be solvated. Solvent can be automatically added by the TIP3P tool in AMBER. Type: 
    
    
    solvatebox n1 TIP3PBOX 10.0
    

Note: After solvation, residues will be renumbered by AMBER. 

### Write Output Files[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=18> "Edit section: Write Output Files")]

Save the _prmtop_ and _inpcrd_ files: 
    
    
    saveamberparm n1 N1-apo.prmtop N1-apo.inpcrd
    

Save the _pdb_ file: 

File -> Save PDB file -> n1 (unit) -> N1-apo.pdb 

## Adding Salts[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=19> "Edit section: Adding Salts")]

The system will be simulated in 20 mM NaCl (salt solution). Therefore, Na+ and Cl- ions will need to be added arbitrarily to the system. This is done by replacing a number of existing water molecules with either Na+ or Cl-. 

### Measure Box Dimensions[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=20> "Edit section: Measure Box Dimensions")]

In order to calculate how many ions should be added, the dimensions of the system must be measured. 

  * Open AMBER parameter files in VMD


    
    
    prmtop > Amber7 PARM
    inpcrd > Amber7 RESTART
    

  * Open VMD TK Console
  * At the prompt, type the following:


    
    
    set sel [atomselect top all]
    measure minmax $sel
    

To calculate the box size, subtract the maximum XYZ coordinates by the minimum XYZ coordinations. Multiply to calculate the volume. 

### Calculate Number of Atoms to Add[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=21> "Edit section: Calculate Number of Atoms to Add")]

To achieve a 20 mM NaCl solution, use the following formula to determine the number of NaCl ions to add to the system: 
    
    
    (0.02 mol/L)(1E-27 L/Angstrom)(Volume)(6.022E23 atoms/mol) = # atoms
    

If the calculated number is a fraction, use your judgment to round to a whole number. Keep in mind that, for this system, one ion was already added for neutralization. 

### Place Na+/Cl- Ions[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=22> "Edit section: Place Na+/Cl- Ions")]

Water molecules are selected arbitrarily and replaced with Cl- or Na+. Selections should be evenly spaced and within 9 A of the protein. Changes are entered manually into the PDB using the following format/naming: 
    
    
    Na+ Na+ ###
    Cl- Cl- ###
    

When finished, the file is saved as _N1-apo-salts.pdb_. 

### Respecify Disulfide Bonds[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=23> "Edit section: Respecify Disulfide Bonds")]

Upload the finished file to kryptonite and respecify the disulfide bonds using AMBER/XLeap. Again, the file must be in the same direction from which XLeap is launched. Parameter files (for calcium) must be loaded before loading the system. 

Keep in mind the numbering has now changed. Check the numbering and specify bonds accordingly: 
    
    
    desc sys
    bond sys.##.SG sys.##.SG
    

Save the _PRMTOP_ , _INCPRD_ , and _PDB_ file when done. 

### Check Work[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=24> "Edit section: Check Work")]

Before proceeding, check the preparation steps complete thus far. 

  * Open _N1-apo-salt.incprd_ and _N1-apo-salt.prmtop_ in VMD 


  1. Check for ions (mass < # and mass > #)
  2. Check disulfide bonds



### Re-measure Box Dimensions[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=25> "Edit section: Re-measure Box Dimensions")]

The NAMD files in the next step require box dimensions and coordinates of the box center. (The numbers will have changed from the previous measurements, but the dimensions should be the same.) 

  * Open AMBER parameter files in VMD 
    * prmtop > Amber7 PARM
  * inpcrd > Amber7 RESTART
  * Open VMD TK Console



At the prompt, type the following: 
    
    
    set sel [atomselect top all]
    measure minmax $sel
    measure center $sel
    

  
Make note of the center coordinates and the min/max values. The coordinates of the box center should be very close to zero. 

## Energy Minimization[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=26> "Edit section: Energy Minimization")]

Now we are ready to begin simulation. First the system must undergo energy minimization. Energy minimization will be performed in four steps in which atoms are gradually allowed to move. 

  * The first step holds everything fixed and allows only hydrogens to move.
  * The second step lets hydrogens, waters and ions move.
  * The third step lets hydrogens, waters, ions and sidechains to move.
  * The fourth step lets everything move. 



For each step, a fixed atom file is needed that specifies which atoms are allowed to move. This is done by specifying a 1 or 0 in the occupancy column of the PDB file. Fixed atoms have an occupancy of 1. Free atoms have an occupancy of 0. 

If there is a ligand bound to the system, the hydrogens of the ligand should be allowed to move with the rest of the system hydrogens. The rest of the ligand should be held fixed until after the sidechains have moved. 

### First Fixed Atom File[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=27> "Edit section: First Fixed Atom File")]

  * Open VMD TKConsole
  * Write first fixed atom file - free hydrogens


    
    
    set sel1 [atomselect top "all"]
    set sel2 [atomselect top "hydrogen"]
    $sel1 set occupancy 1
    $sel2 set occupancy 0
    $sel1 writepdb fxd1.pdb
    

Check the PDB file. It should have 0 after every free hydrogen and 1 everywhere else. 

### Second Fixed Atom File[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=28> "Edit section: Second Fixed Atom File")]
    
    
     *Write second first atom file - free hydrogens, waters, and ions
    
    
    
    set sel2 [atomselect top "hydrogen or water or (mass < 37 and mass > 34) or (mass < 24 and mass > 22) or resname CAL"]
    $sel2 set occupancy 0
    $sel1 writepdb fxd2.pdb
    

### Third Fixed Atom File[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=29> "Edit section: Third Fixed Atom File")]

  * Write third fixed atom file - free hydrogens, waters, ions and sidechains


    
    
    set sel2 [atomselect top "hydrogen or water or (mass < 37 and mass > 34) or (mass < 24 and mass > 22) or resname CAL or sidechain"]
    $sel2 set occupancy 0
    $sel1 writepdb fxd3.pdb
    

The fourth minimization lets everything move and therefore does not require a fixed atom file to be written. 

### Scripts[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=30> "Edit section: Scripts")]

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



In the first minimization step, system specific coordinates such as box dimensions and box center need to be specified. The box dimensions (PMDGridSize) must be a multiple of 2 or 3. The cellBasisVector and the cellOrigin may be in decimal form. 

## Harmonic Constraints Equilibration[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=31> "Edit section: Harmonic Constraints Equilibration")]

After energy minimizations are completed, the next step is to add heat into the system. As we warm the system up from 0K, we do this in a slow sequence of steps, in order to maintain, as much as possible, the experimental structure that we have set the system up with. We typically use a procedure called "harmonic constraints" to slowly ramp the system up to free dynamics. The _min_4_ file from energy minimizations is fed into the first harmonic constraint script, _hc_eq_1_. There are four steps of harmonic constrains, each slightly less constrained than the one before. 

### Restrain Backbone[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=32> "Edit section: Restrain Backbone")]

In the same window on TKConsole, reset all occupancies to 0. Then select the backbone and set the occupancy for the backbone to 4. Write this file. 
    
    
    $sel1 set occupancy 0
    set sel2 [atomselect top "backbone"]
    $sel2 set occupancy 4
    $sel1 writepdb restrain_backbone_ref.pdb
    

In the PDB file, everything should be 0 except for the backbone, which should be at 4. 

### Scripts[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=33> "Edit section: Scripts")]

The harmonic equilibration scripts can be found here: [Generic MD Equilibration Scripts](</mediawiki/index.php/Generic_MD_Equilibration_Scripts> "Generic MD Equilibration Scripts")

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

### Check Results[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=34> "Edit section: Check Results")]

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

## Free Dynamics[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=35> "Edit section: Free Dynamics")]

If all previous steps were completed and the system looks good in equilibration, then we can proceed to free dynamics. Free dynamics starts with the output of the free equilibration and continues until you decide to stop. 

  * Make new directory
  * Copy the following files into the new directory: _prmtop_ , _inpcrd_ , _coor_ and _xsc_
  * See templates from previous MD simulations



## Job Execution[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=36> "Edit section: Job Execution")]

### namd2.bash File[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=37> "Edit section: namd2.bash File")]

Before running jobs, make sure the file namd2.bash is in the origin directory. 
    
    
    #!/bin/bash
    
    # Justin Gullingsrud
    # jgulling@mccammon.ucsd.edu
    # 17 October 2003
    # $Id: namd2.sh,v 1.1 2005/03/30 17:17:46 root Exp root $
    
    # This script enables NAMD to be run either interactively, or on the
    # PBS cluster, using the same command interface in each case:
    # namd2.csh input.conf > output.log
    
    # BINDIR: the location of the NAMD binaries, charmrun and namd2.  May
    # be overridden by the user.
    #export LD_LIBRARY_PATH=/soft/linux/share/intel/compiler70/ia32/lib
    #export BINDIR=/soft/linux/pkg/NAMD-gm
    #export BINDIR=/home/cmura/bin/NAMD-gm
    # Use /gpfs copy for now due to trouble with some nodes not knowing where /home is due to
    # some weird DNS problem w/ ctbp2 (which is physical location of exported /home dirs - see
    # emails of 07/17/2005 with Robert):
    #export BINDIR=/gpfs/cmura/bin/NAMD-gm
    export BINDIR=/home/install/usr/apps/namd26
    
    # Use ssh to launch NAMD on remote nodes
    export CONV_RSH=ssh
    
    NODELIST=$TMPDIR/namd2.nodelist
    cp $TMPDIR/machines ~/
    rm -f $NODELIST
    echo "group main" > $NODELIST
    nprocs=0
    
    for elem in  `cat $TMPDIR/machines`
      do
      echo "host $elem" >> $NODELIST
      nprocs=`expr $nprocs + 1`
    done
    
    exec $BINDIR/charmrun $BINDIR/namd2 +p$nprocs ++nodelist $NODELIST $*
    

### Job Script[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=38> "Edit section: Job Script")]
    
    
    #!/bin/csh
    #$ -cwd
    #$ -V
    #$ -v ORIGINDIR=/nas3/lscheng/MD_N1-apo
    #$ -j y
    #$ -M lscheng@ucsd.edu
    #$ -m beas
    #$ -N N1-apo-salt-eq_1.namd
    #$ -l h_rt=48:00:00
    #$ -pe mpi 42-64
    #$ -o N1-apo-salt-eq_1.namd.sge_job.output
    
    
    #-------------------------------------------------------------------------------
    # Submit this script to SGE using the qsub command, like so:
    # $] qsub cam_sample.conf.sge_job
    
    setenv MYDIR /state/partition1/scratch/lscheng/$JOB_ID
    #export MYDIR=/state/partition1/scratch/lscheng/$JOB_ID
    mkdir -p $MYDIR
    rsync -rLptgoDvzu --progress -e ssh --exclude "*.dcd" ${ORIGINDIR}/* ${MYDIR}/.
    
    #-------------- ACTUAL TASKS TO EXECUTE: ---------------------------------------
    echo "%%%%%%%%%%%%%%%%%%%%%%%%%%" > ${JOB_NAME}-${JOB_ID}-testfile.txt
    echo "JOB started at: `date`" >> ${JOB_NAME}-${JOB_ID}-testfile.txt
    echo "IN directory: `pwd`" >> ${JOB_NAME}-${JOB_ID}-testfile.txt
    echo "ON host:  ${HOSTNAME} " >> ${JOB_NAME}-${JOB_ID}-testfile.txt
    echo "%%%%%%%%%%%%%%%%%%%%%%%%%%" >> ${JOB_NAME}-${JOB_ID}-testfile.txt
    echo ${HOSTNAME}
    $MYDIR/namd2.bash $ORIGINDIR/N1-apo-salt-eq_1.namd >! $ORIGINDIR/N1-apo-salt-eq_1.namd.out
    #-------------------------------------------------------------------------------
    
    cp -a -u ${MYDIR}/* ${ORIGINDIR}/.
    # Clean-up local scratch:
    \rm -rf ${MYDIR}
    

### Submission[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=39> "Edit section: Submission")]

To submit a job, use the following: 
    
    
    qsub -P nbcr_safi -R y N1-apo-salt-eq_1.namd.sge_qsub
    

Specifying the nbcr_safi project and using the reservation mechanism increases the priority of the job for early execution than other queued jobs. 

### Resubmission[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=40> "Edit section: Resubmission")]

Sometimes, due to time constrains on kryptonite, the job will be aborted. To restart the job, follow the following resubmission procedure. 

For _N1-apo-salt-eq_1.namd_ file, the following parameters need to be updated: 
    
    
    set inpname     N1-apo-salt-eq        #the outname below becomes the inpname for restart
    set outname     N1-apo-salt-eq_1      #this needs to be incremented for restart
    firsttimestep   2669500               #this needs to be updated to new time step in $ioutname.restart.xsc file
    BinVelocities   $inpname.restart.vel  #this needs to be uncommented for restart
    #temperature    310                   #this needs to be commented out for restart
    

and copied to _N1-apo-salt-eq_2.namd_ file. 
    
    
    set inpname     N1-apo-salt-eq_1
    set outname     N1-apo-salt-eq_2
    firsttimestep   3152000               #this multiplies 2 gives the number of fs.
    

The submission script needs to be updated from _N1-apo-salt-eq_1.namd.sge_qsub_ to _N1-apo-salt-eq_2_.... 
    
    
    #$ -o N1-apo-salt-eq_2.namd.sge_job.output
    #$ -N N1-apo-salt-eq_2.namd
    $MYDIR/namd2.bash $ORIGINDIR/N1-apo-salt-eq_2.namd >! $ORIGINDIR/N1-apo-salt-eq_2.namd.out
    

Then submit the job: 
    
    
    qsub -R y -P nbcr_safi N1-apo-salt-eq_2.namd.sge_qsub
    

### Current Queue Policy[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=41> "Edit section: Current Queue Policy")]
    
    
    Quick Queue Summary: 
    qstat -g c --> to see which queue has empty slots.
    qalter -l <short,medium,long,debug> <job> --> to switch queues for submitted jobs.
    qalter -l q=all.q <job> --> to switch to default low priority queue.
    Please see https://nbcr.net/pub/wiki/index.php?title=Understanding_SGE_job_status
    
    SGE Job Submission to Different Queues: 
    qsub -l urgent <job>  --> urgent.q  max run time 16 hr; NBCR users only. 
    qsub -l short <job>   --> rack0.q  max run time 4 hr; 
    qsub -l medium <job>  --> rack1.q  max run time 16 hr; 
    qsub -l long <job>    --> rack2.q  max run time 48 hr; 
    qsub -l debug <job>   --> rack3.q  max run time 0.5 hr; 2 nodes/4 processors max.
    qsub (no param) <job> --> all.q    max run time 48 hr; subordinate queue; lowest priority.
    Please see https://nbcr.net/pub/wiki/index.php?title=Main_Page#How_To...
    
    Reservation for parallel jobs requesting more than 8 CPU's:
    qsub -R y <job>       --> blocks smaller jobs through reservation
    

### Check and Alter Jobs[edit](</mediawiki/index.php?title=NAMD_MD_Minimization_and_Equilibration&action=edit&section=42> "Edit section: Check and Alter Jobs")]

To check the status of a submitted job: 
    
    
    qstat -ext -s p
    
    job-ID  prior   ntckts  name       user         project          department state cpu        mem     io      tckts ovrts otckt ftckt stckt share queue                          slots ja-task-ID 
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      41871 100.01500 1.00000 N1-apo-sal lscheng      nbcr_safi        Dept_nbcr  qw                               101666     0 20000 81666     0 0.99                                    42        
      41787 0.03242 0.00027 fine_r30_j ikhavru      NA               Dept_chem  qw                                  27     0     0    26     0 0.00                                     4        
      41851 0.02356 0.00018 fine_r19_j ikhavru      NA               Dept_chem  qw                                  18     0     0    18     0 0.00                                     4  
    

To modify the reservation behavior of a job: 
    
    
     qalter -R y 41871
    

To check the cluster queue: 
    
    
    qstat -g c
    
    CLUSTER QUEUE                   CQLOAD   USED  AVAIL  TOTAL aoACDS  cdsuE  
    -------------------------------------------------------------------------------
    all.q                             0.95    128      8    196    180      0 
    rack0.q                           0.90      0     64     64      0      0 
    rack1.q                           1.05     64      0     64      0      0 
    rack2.q                           0.89     60      4     64      0      0 
    rack3.q                           1.01      0      4      4      0      0 
    urgent.q                          0.95      0    196    196      0      0
