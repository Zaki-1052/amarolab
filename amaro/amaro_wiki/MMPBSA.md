# MMPBSA

## This wiki page is for MMPBSA.py implemented in AmberTools.[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=1> "Edit section: This wiki page is for MMPBSA.py implemented in AmberTools.")]

For AmberTools 13, you can use the .dcd files generated from NAMD to run MMPBSA. However, if you plan to use any older Amber versions, you need to convert your .dcd files into .mdcrd first. 

To convert .dcd files into .mdcrd files, you can just use ptraj. If you want to stride the trajectories to fewer frames, you can also do it with ptraj. 

## ptraj[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=2> "Edit section: ptraj")]

Here is an example input for ptraj: 
    
    
      
    trajin NAMD_trajectory.dcd firstframe lastframe stride
    trajout AMBER_trajectory.mdcrd trajectory
    go
    

This will convert a NAMD .dcd file to Amber .mdcrd file. 

## MMPBSA[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=3> "Edit section: MMPBSA")]

To run MMPBSA, you need parameter files (*.prmtop) for ligands and receptors. For Amber11, you also need a solvated .prmtop file if you have water or other ions in your trajectories. However, if you have nothing that you would like to strip, you can specify in your input file that you do not want to strip anything from trajectories. Also, if you are using Amber 13, you can totally ignore the solvated .prmtop part if your system is not solvated. 

In a terminal, you would type this to start MMPBSA.py: 
    
    
    $AMBERHOME/bin/MMPBSA.py.MPI -O -i input.in -o FINAL_RESULTS_MMPBSA.dat -sp solvated.prmtop -cp complex.prmtop -rp receptor.prmtop -lp ligand.prmtop -y trajectory.mdcrd > progress.log 

As you see, you need several .prmtops to run the calculations and you can easily generate them by using parmed.py or xparmed.py. The .prmtop file that you use to run simulations will probably be your solvated .prmtop if you include a waterbox. 

There are two verisons of parmed.py. For advanced programmers, you may want to use the command version of it. For beginners, you may want to skip to the next section, xparmed.py. 

### parmed.py[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=4> "Edit section: parmed.py")]
    
    
    strip !:XXX-XXX    #XXX is the residue number; XXX-XXX describes the range.
    parmout new.prmtop
    

The script above would strip all the atoms except the residues that you specified in the command strip. Then it will create a new .prmtop file with only the residues that you listed. Be aware, when you create the new .prmtop, AMBER automatically renumbers the residues. 

After you write your own new.parmEd, type the following command and parmed.py will excute the job for you: 
    
    
    /soft/linux/amber12/bin/parmed.py solvated.prmtop new.parmEd 

The command creates a new .prmtop through parmEd. 

### xparmed.py[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=5> "Edit section: xparmed.py")]

xparmed.py is a graphic version of parmed.py and it runs more slowly. However, you can just click, click, click. 

To start up xparmed.py, you type: 
    
    
    /soft/linux/amber12/bin/xparmed.py solvated.prmtop
    

Here is what you would see 

[![Xparmed py.png](/mediawiki/images/d/d8/Xparmed_py.png)](</mediawiki/index.php/File:Xparmed_py.png>)

Click "strip" in the third column to specify which residues you want kept by typing: 
    
    
    !:XXX-XXX
    

Then you can save to a new .prmtop by clicking on the lower left corner where it says "Write a New Topology File Now." 

### Next step is to write an input file.[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=6> "Edit section: Next step is to write an input file.")]

Here is an example input file for **PB calculation**.(Please see below for more details!) 
    
    
      Input file for running MMPBSA free energy calculation
      &general
        interval=1, endframe=1, verbose=2, keep_files=1,
      /
      &pb
        indi=1.0,
        exdi=80.0,
        scale=2.0,
        linit=1000,
        prbrad=1.4,
        istrng=0.02,
        cavity_surften=0.00542,
        cavity_offset=-1.008,
        fillratio=2.0,
        radiopt=0,
        sander_apbs=0,
    

The parameters in &general apply to all the calculations you call for in the input file. In the above template, only PB is specified. Nevertheless, you can ask MMPBSA.py to run gb, pb, alanine scanning, nmode (entropy), and energy decompositon calculations. For complete details of all the calculations that MMPBSA.py is able to perform, please see the AMBER manual. 

There are several parameters that you may want to pay special attention to: 

  * strip_mdcrd=0 (This tells MMPBSA.py that you do not want it to strip anything from the trajectories. Specifying this parameter is required if you do not have a solvant .prmtop. Default is 1, which will strip anything that is missing from the complex .prmtop. You can put this parameter in &general)
  * receptor_mask=:XXX-XXX:XXX-XXX (XXX is your receptor residue number. You can specify where your receptor is if your ligand is in the middle of the residues. For example, if your receptor is from 1-2004 and 2093-2772, you would want to specify it. AMBER11 is not very good at guessing if your ligand is not in the beginning or the end. AMBER13 is a lot smarter, so you don't necessarily need to specify your mask even if the ligand is in the middle of the .prmtop file.)
  * ligand_mask=:XXX-XXX (XXX is your ligand residues number. Your ligand residues cannot be broken apart. For example, if your ligand is from 293-319 and 431-489, you can only either claim 293-319 as your ligand or 431-489. There is also a problem with the receptor and ligand mask: if you specify them in your input, MMPBSA.py will not be able to understand strip_mdcrd. The best solution to solve this is to use AMBER13.)
  * istrng=XXX (This parameter should be the salt concentration you used to run your simulation. Its unit is in M. So if you have 20mM salt, you will write istrng=0.02.)



Here is an example input file for **GB calculation**.(Please see below for more details!) 
    
    
      Input file for running MMPBSA free energy calculation
      &general
         interval=1, verbose=2, keep_files=1,
      /
      &gb
         saltcon=0.02,
         igb=2,
      /
    

  * The default value for igb is 5; however, in one of Rommie's papers, it was discovered that igb=2 gave better results with N1 neuramindase. 
  * saltcon should be the salt concentration for your system. 



MMPBSA.py is capable of doing more than just PB and GB calculations. For example, it can decompose residues into different energy terms. 

Here is a sample input file for **GB calculation and free energy decomposition**. GB or PB is required to do decomposition. **NOTE:** PB non-polar solvation energies are currently not decomposable. 
    
    
      Input file for running MMPBSA free energy calculation
        &general
           interval=1, verbose=2, keep_files=1,
        /
        &gb
           saltcon=0.02,
           igb=2,
        /
        &decomp
           idecomp=2,
           print_res="120,121,122,124,125,153-164,166,193,194,243,245,520"
           dec_verbose=0,
    

  * idecomp specifies whether you would like to do per-residue decomposition (1 or 2) or pair-wise decomposition (3 or 4). Pair-wise decompositon requires a lot of memory to complete. Per-residue decomposition will print out energy for the residues you wanted (print_res) while pair-wise decomposition will pair the resdiues you specify with their surrounding residue and print out their energy values. 
  * print_res is where you specify what residues you want MMPBSA.py to decompose. You need at least one residue from both receptor and ligand. 
  * dec_verbose sets the level of output to be printed. dec_verbose=0 (DELTA energy of the residues only), dec_verbose=1 (DELTA energy, total, sidechain, and backbone contributions), etc. 
  * To run energy decomposition, MMPBSA.py has to specify receptor and ligand masks for it. It has to guess them correctly in order to calculate the Delta energy. Amber 11 has some problem with it if the ligand is in the middle of the complex .prmtop. Amber13 is better at guessing. Even if Amber13 cannot guess it for you, you can still specify the receptor and ligand mask in your input file. Amber13 is capable in reading your mask for energy decomposition. However, Amber11 will think you are crazy if you try to specify receptor and ligand mask when you try to do energy decomposition. 



To run energy decomposition, you need one more flag in the command line when you run MMPBSA.py. Here is an example: 
    
    
    $AMBERHOME/bin/MMPBSA.py -O -i input.in -o FINAL_RESULTS_MMPBSA.dat -do FINAL_RESULTS_DECOMP.dat -sp solvated.prmtop -cp complex.prmtop -rp receptor.prmtop -lp ligand.prmtop -y trajectory.mdcrd > progress.log
    

MMPBSA.py can also be run in parallel. The command will be similar to the others. However, you need to make sure you have this environment in your bash file: 
    
    
    export PATH=$PATH:/usr/lib64/openmpi/bin
    

If this is the first time you put the above line in your bash file, remember to source your bashrc file. 
    
    
    source .bashrc
    

Finally, if you would like to run MMPBSA in parallel, this is an example of what command you would type in a terminal: 
    
    
    mpirun -np 4 $AMBERHOME/bin/MMPBSA.py.MPI -O -i mmpbsa.in -o FINAL_RESULTS_MMPBSA.dat -sp solvated.prmtop -cp complex.prmtop -rp receptor.prmtop -lp ligand.prmtop -y trajectory.mdcrd > progress.log
    

  * You would specify how many processers you want to run after -np. Right now, it is set to run in 4 processors.



  


### Using the Alanine Scan option[edit](</mediawiki/index.php?title=MMPBSA&action=edit&section=7> "Edit section: Using the Alanine Scan option")]

The alanine scan option allows you to calculate the thermodynamic effect of mutating one or a few residues to alanine over a simulation that you have run. Essentially, in each frame of a simulation that you have run, the free energy is calculated for the wild-type structure and then for the alanine mutant structure. The naming of this calculation is misleading - a full alanine scan (in which every residue is mutated to alanine) is not performed. The calculation can only compare the free energies of two different structures, one is wild-type and one is a mutant with your choice of alanine mutations. Here is the tutorial that was combined with the tutorial above to perform these MMPBSA and MMGBSA calculations: <http://ambermd.org/tutorials/advanced/tutorial3/py_script/section3.htm>

You will want to generate the following input files: 
    
    
    Wild-type_complex.prmtop (used to run your simulation)
    Wild-type_nosolvent_complex.prmtop
    Wild-type_nosolvent_receptor.prmtop
    Wild-type_nosolvent_ligand.prmtop
    Mutant_nosolvent_ligand.prmtop
    Mutant_nosolvent_complex.prmtop
    

Generate the Wild-type prmtop files with xparmed.py above. 

To generate the mutant prmtop files you will need to go in and mutate the wild-type complex pdb file. For example, to make a D to A mutant you would do the following: 
    
    
    ATOM    196  N   ASP X  14      37.866  43.343  60.357  0.00  0.00            
    ATOM    197  H   ASP X  14      38.240  42.514  59.917  0.00  0.00            
    ATOM    198  CA  ASP X  14      38.675  44.017  61.438  0.00  0.00            
    ATOM    199  HA  ASP X  14      38.207  44.974  61.668  0.00  0.00            
    ATOM    200  CB  ASP X  14      38.625  43.060  62.701  0.00  0.00            
    ATOM    201  HB2 ASP X  14      37.791  42.360  62.653  0.00  0.00            
    ATOM    202  HB3 ASP X  14      39.593  42.571  62.805  0.00  0.00            
    ATOM    203  CG  ASP X  14      38.650  43.905  63.997  0.00  0.00            
    ATOM    204  OD1 ASP X  14      39.115  43.416  65.050  0.00  0.00            
    ATOM    205  OD2 ASP X  14      37.894  44.927  64.056  0.00  0.00            
    ATOM    206  C   ASP X  14      40.091  44.445  61.060  0.00  0.00            
    ATOM    207  O   ASP X  14      40.592  45.462  61.520  0.00  0.00        
    

  * Delete the lines corresponding to atom-types OD1 and OD2. Change the CG atom-type to HB1. You do not need to renumber each atom for xparmed. 


  * Open the mutated complex pdb file with xleap or tleap and save the parameter files. Do not have salt in your final pdb structure - you need to save the prmtop file with the native charge of you system. 


  * Open the mutated complex prmtop file in xparmed as described above. Remove the part of the complex that was not mutated.



Click "strip" in the third column to specify which residues you want kept by typing: 
    
    
    !:XXX-XXX
    

  * Then you can save to a new .prmtop by clicking on the lower left corner where it says "Write a New Topology File Now" and save this as the mutant_ligand.prmtop. 


  * Now that you have all the prmtop files that you need, here is a sample input file for an alanine scan GBSA and PBSA calculation:


    
    
    Input file for running PB and GB
    &general
       startframe=1, endframe=9999, interval=5, receptor_mask=:1-756, ligand_mask=:757-1011, verbose=1,
    /
    &gb
      igb=5, saltcon=0.150
    /
    &pb
      istrng=0.100
    /
    &decomp
      idecomp=1, print_res="179-199; 556-576; 777-810"
      dec_verbose=1,
    /
    &alanine_scanning
    /
    

  * Finally to set up the MMPBSA calculations run the following command:


    
    
     $AMBERHOME/MMPBSA.py -O -i mmpbsa.in -o FINAL_RESULTS_MMPBSA.dat -sp Wildtype_solvated_complex.prmtop -cp Wildtype_nosolvent_complex.prmtop -rp
    Wildtype_nosolvent_receptor.prmtop -lp Wildtype_nosolvent_ligand.prmtop -y *.nc -mc mutant_complex_.prmtop -ml mutant_ligand_fixed.prmtop 
    

  *     * You can also run in parallel using the command above!
