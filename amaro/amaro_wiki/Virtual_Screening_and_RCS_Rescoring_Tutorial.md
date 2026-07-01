# Virtual Screening and RCS Rescoring Tutorial

## Tutorial files[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=1> "Edit section: Tutorial files")]

  * If you are doing this tutorial on your own at your home institution, and would like a copy of the files, you can grab them in this **tarball**.



## Preparing the system for the virtual screen[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=2> "Edit section: Preparing the system for the virtual screen")]

### Get PDB from pdb databank[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=3> "Edit section: Get PDB from pdb databank")]

Today we will be working with the N1 neuraminidase protein. This first section will take place in a terminal on your desktop or laptop. 

  * Download 2HU4 from the [RCSB website](<http://www.rcsb.org/pdb/home/home.do>), or you can do it with the following command: 


    
    
    wget <http://www.rcsb.org/pdb/files/2hu4.pdb> -O 2HU4.pdb
    

### Process in VMD, extract protein, extract tamiflu[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=4> "Edit section: Process in VMD, extract protein, extract tamiflu")]

Launch VMD. On your local terminal, type: 
    
    
    vmd
    

Load the _2HU4.pdb_ structure into VMD (by now we assume you are familiar with VMD. If you need help, ask a proctor!) 

  * In the VMD Main window, select File -> New Molecule
  * Browse for _2HU4.pdb_



Notice that the structure is a tetramer. As the binding site does not bridge across multiple domains (i.e. it only involves one subunit) we only need to extract and work with one of the 8 chains resolved in the file. 

  * In the graphics window, select "chain B" and set the display type to **New Cartoon**
  * Make an additional selection for "resid 801" and set the display type to **VDW**



This shows you tamiflu (aka oseltamivir) bound in the active site of the N1 neuraminidase. We want to make separate files for the protein and the ligand. Although we can do this in many ways, we will do it here in VMD. 

  * Open a Tkcon window by selecting Extensions -> Tk Console 
  * At the prompt make the protein selection by typing:


    
    
    set prot [atomselect top "chain B"]
    

  * Then write the selection to a pdb file by typing:


    
    
    $prot writepdb 2HU4_B.pdb
    

  * Now make another selection for tamiflu by typing:


    
    
    set tami [atomselect top "resid 801"]
    

  * Then write the selection to another pdb file:


    
    
    $tami writepdb oseltamivir.pdb
    

### Process/assign protonation states at pH 6.5 using PDB2PQR website[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=5> "Edit section: Process/assign protonation states at pH 6.5 using PDB2PQR website")]

Before we try to redock the tamiflu ligand into the N1 crystal structure, we need to assign the proper protonation states for the protein. We want the protein to be protonated according to pH 6.5, which is the pH at which the experimentalists will run the inhibition assays. To do this, we will use a tool called **PDB2PQR**. 

  * Go to <http://nbcr.net/pdb2pqr>
  * Scroll down and select Upload a PDB, then browse to select the _2HU4_B.pdb_ file you created above.
  * Select the Amber force field
  * Select **Amber** for the output naming scheme 
  * For the available options, be sure the top three are selected. In the box for PROPKA, type **6.5** : 
    * Use PROPKA to assign protonation states at pH 6.5
  * Click Submit.



This job will take a couple of minutes. 

Wait for the file to be processed and when it's finished, click on the first link, the file with the .pqr extension. Open and look at this file in a text editor. Notice that it has comments at the top. Scroll down and see the protonation states assigned to the various histidines and other residues. When you are finished checking it out, rename the file as //2HU4_pH65.pdb//. You can do that in your text editor or with a simple "mv" on the command line (if you are unsure how to do this, ask your neighbor or a lab proctor). 

### Setting your environment for AutoDock4[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=6> "Edit section: Setting your environment for AutoDock4")]

Log in to ieng6 and then kryptonite using the login and password given to you by the Summer Institute. To do this: 

  * Open a Terminal window on your local machine and type:


    
    
    ssh ieng6-203.ucsd.edu
    ssh kryptonite.nbcr.net
    

  * Once logged into kryptonite, set the proper environmental variables:


    
    
    source /nas3/rommie/SI2008-day2/setup.bash
    

This will set all the necessary program executable paths and environmental variables. It is important to note that if you log out of kryptonite during this session, you will have to repeat the above command! 

  * Now, copy the required tutorial files into your local directory (we've prepared the files already for you and copied them onto the cluster where we will be doing today's work):


    
    
    cp -r /nas3/rommie/SI2009-RCS .
    

Now you need to move into the directory you just copied: 
    
    
    cd SI2009-RCS
    

### Process protein for AD4[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=7> "Edit section: Process protein for AD4")]

  * First, we will prepare the receptor PDB file. Note that this file is the same as the one you just processed with PDB2PQR.:


    
    
    prepare_receptor4.py -r 2HU4_pH65.pdb -o 2hu4_ph65.pdbqt
    

### Process ligand for AD4[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=8> "Edit section: Process ligand for AD4")]

To prepare the ligand file for AD4 we need to process with the prepare_ligand script in AutoDock. This script will merge the non-polar hydrogens so the ligand can be correctly docked in AD4. (Note: the -A option adds hydrogens using Babel, internal to AD; of course you can always use an external program to add hydrogens and in any case should check that Babel does it correctly.) Sometimes the automated programs do not do exactly what you want them to do, and in those cases, you will need to use other programs or manually edit your ligand file. For example, PRODRG can be used to add polar hydrogens. 
    
    
    prepare_ligand4.py -l oseltamivir.pdb -o oseltamivir.pdbqt
    

  * Check the output. Look where AD4 put hydrogens. Are all hydrogens all present? Why or why not?



### Make the grid and docking parameter files (.gpf, .dpf)[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=9> "Edit section: Make the grid and docking parameter files \(.gpf, .dpf\)")]

Next it’s time to prepare the grid and docking parameter files for AD4. 

  * First, for this receptor, you must prepare a grid parameter file (GPF).



Here you will need to know the gridcenter and grid size of the grid box you wish to create. Typically, we change the gridcenter to the center of the active site and the npts (number of points) to something that you will know will encompass the entire active site. If you are doing this for the first time, it may be helpful to switch to the ADT GUI to confirm correct box placement, like you did in the AutoDock tutorials. If you already know the parameters you wish to use, you may enter them in command line. 

For this neuraminidase protein, the center of the active site is at {3.73 20.236 113.925} and the npts should be changed to {64 72 66} to be sure the grids will cover the entire binding site. You can also modify the .gpf file as it is created, by using the following command-line options: 
    
    
    prepare_gpf4.py -l oseltamivir.pdbqt -r 2hu4_ph65.pdbqt -p gridcenter="3.73 20.236 113.925" -p npts="64 72 66" -o 2hu4_ph65.gpf 

  * Now we need to prepare the docking parameter file (DPF). 



This file contains all the different docking options utilized in AD4. A lot of these you can probably safely use without changing, but you will want to modify / optimize some parameters in the docking parameter file in order to validate the program for your target. A good first place to start is by altering the default values for ga_num_evals (total number of energy evaluations), ga_pop_size (population size), and ga_num_generations (number of generations). The default ga_num_evals is about 2 orders of magnitude too small for most ligands. In particular, when you perform a virtual screen, you need to set the ga_num_evals high enough that it allows all ligands in your screening set to converge. Typically this is 5-10 million. 

To improve the clustering of the docking results, you may need to do system-specific parameter optimization for AutoDock. We don’t have time today to go through a full iteration of this. Here we give you the optimized parameters for neuraminidase (a discussion of which was presented in the lecture). Note that in this example we will set ga_run to 15, which is the number of dockings we will actually perform. For your real research projects, you will probably want to set ga_run to 50 or 100 (in order to generate better statistics). 

For this docking, change ga_pop to 200, ga_num_evals to 3000000, and rms_tol to 2.0. We can do this in the command line as follows: 
    
    
    prepare_dpf4.py -l oseltamivir.pdbqt -r 2hu4_ph65.pdbqt -p ga_pop_size=200 -p ga_num_evals=3000000 -p rmstol=2.0 -o oseltamivir-2hu4_ph65.dpf
    

## Control case: redocking oseltamivir into the N1 crystal[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=10> "Edit section: Control case: redocking oseltamivir into the N1 crystal")]

  * Now it’s finally time to run the docking!



To do this, first we have to run AutoGrid, which will make all the atomic affinity and electrostatic grids for the receptor and all the different atoms types in your ligand. After the grids are generated, we call run AutoDock. 

The .glg and .dlg are the grid log file and docking log file, respectively. 

We will submit this job on Kryptonite with the following script, which is called "submit-autogrid-autodock.csh". In case you'd like to see it, here is what the job submission script looks like: 
    
    
    #!/bin/bash
    #$ -N autogrid-set
    #$ -o autogrid-set.std.out
    #$ -e autogrid-set.std.err
    #$ -S /bin/bash
    #$ -cwd
    #$ -l h_cpu=00:45:00
    #$ -l h_rt=00:55:00
    #$ -m e
    
    export STACK_SIZE="unlimited"
    
    /home/install/usr/apps/autodock4/bin/autogrid4 -p 2hu4_ph65.gpf -l 2hu4_ph65.glg 
    
    /home/install/usr/apps/autodock4/bin/autodock4 -p oseltamivir-2hu4_ph65.dpf  -l oseltamivir-2hu4_ph65.dlg
    

You should already have a copy of this file in your directory. When you are ready to submit it, type: 
    
    
    qsub submit-autogrid-autodock.csh
    

The docking job will take approximately 15 minutes. 

To check your job's status, you can type: 
    
    
    qstat -u username
    

When the run is finished, there are several things we need to do in order to evaluate the results: Do the following on your local computer terminal that you set up in the beginning: 

  * Compare docking pose(s) to crystal structure
  * Read the _oseltamivir-2hu4_ph65.dlg_ file into VMD as a PDB file 
    * Read the _2HU4_B.pdb_ into VMD as a separate PDB file 
    * Read the _oseltamivir.pdb_ file into VMD 
    * How close does AutoDock get to finding the crystal binding pose? 
  * Look at the clusters 
    * Listed at the end of the .dlg file, depicted as a text-style histogram 
    * How many clusters are there? Is the clustering good? The ideal case is that the lowest energy cluster is also the most populated. How did we do? 
  * Look at the energy 
    * Is AutoDock able to repeatedly find a low-energy docking pose? 
    * What is the energy of the first cluster? 
    * What is the energy of the biggest cluster?
  * Interpret 
    * All of these results of need to be taken into account in the final interpretation and evaluation of the docking results. If the results are good, you can proceed to the virtual screen, feeling confident that AutoDock can work for your system. If the results are not good (i.e. poor clustering, high energies, large deviation from the crystal pose), you should consider modifying the AutoDock docking parameters.
    * For the control case, are our parameters good?



## Performing the virtual screen[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=11> "Edit section: Performing the virtual screen")]

Now that we are sure we have a good set of AutoDock parameters, we will start the virtual screening process. We will perform a virtual screen of the crystal structure against the NCI diversity set (NCIDS), which has about 2000 compounds. These compounds are typically available for free by the National Cancer Institute when investigating HIV, cancer, or any related diseases. It is a reduced and representative set of full NCI database, which contains approximately 250,000 compounds. 

We have a version of the NCIDS preprocessed on kryptonite for use in AutoDock4. It takes many hours of computing time to screen even this reduced database with AD4, but a lot less time if you're using AutoDock VINA. Because our time today is limited, we will try to screen a small subset of this database. 

### Small molecule databases[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=12> "Edit section: Small molecule databases")]

In virtual screening, you will dock many ligands (from a library of small molecules) to a single receptor of choice. You will still need to prepare the receptor as previously shown. Ligand libraries can be prepared with a simple script but many come already prepared. There are a few well-curated, publicly available small molecule databases that can be used for a variety of virtual screen or docking applications. 

The **NCI diversity set 2** is distributed from the National Cancer Institute and contains approximately 1900 chemically diverse compounds. It is a good place to start for efficient "search in the dark" type applications. The NCI makes these compounds (and those listed in the full NCI database) available for the experimentalists to test, so it is a good place to start. It has been processed for use in AutoDock4 and is available from NBCR for your docking experiments. The **ZINC database** is maintained by the Shoichet lab at UCSF and is an excellently curated very large small molecule database. A variety of file formats are maintained. See <http://blaster.docking.org/zinc> . The NBCR also houses an AutoDock4 curated version of one of the recent ZINC library distributions. The **Available Chemicals Directory** (ACD) and **Hit2Lead** are other popular small molecule databases. 

### Prepare the grids for the ligand set[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=13> "Edit section: Prepare the grids for the ligand set")]

To run the screen, we need affinity and electrostatic grids for all the atom types in the screen set. To generate these files, we need to rerun AutoGrid with all the ligand atoms types contained in the screen set. If we fail to do this, AutoDock will not be able to perform the docking for the missing atoms types. To make all the necessary grid files, we need to modify the .gpf file that we generated above. 

  * We will now make a new grid parameter file for the screen (be sure that you copy the entire command, which is quite long!):


    
    
    prepare_gpf4.py -l oseltamivir.pdbqt -r 2hu4_ph65.pdbqt -p gridcenter="3.73 20.236 113.925" -p npts="64 72 66" -p ligand_types="A C HD N NA OA SA Fe F S P Mg Mn I Zn Br Cl" -o 2hu4_ph65-screen.gpf
    

  * Now, we need to rerun AutoGrid to generate all the new map files:


    
    
    qsub submit-screen-autogrid.csh
    

It will take approximately 3 minutes to generate these new files. 

### Setting up the screening directories[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=14> "Edit section: Setting up the screening directories")]

Now, we will set up a directory of directories that will contain one ligand docking to the crystal structure (for the purpose of this tutorial, each person will generate 16 directories, one docking per directory). You don't have to set up the directory structure in this way, but we have found that it is easiest to keep things organized if we keep the "one-directory-one-docking" file structure. Typical screens will have thousands of ligands, and you will need to keep things very organized so as not to get lost in the data. 

The script to prepare the VS docking directories is called "prepare_dpfs_set1.csh" and looks like this: 
    
    
    #!/bin/csh
    
    mkdir 2hu4_screen
    cd 2hu4_screen
    
    foreach f (`ls /nas3/rommie/SI2008-day2/Set1/*.pdbqt`)
    set name = `basename $f .pdbqt`
    echo $name
    mkdir "$name"_2hu4
    cd "$name"_2hu4
    cp "$f" .
    ln -s ../../2hu4_ph65.pdbqt .
    ln -s ../../2*map* .
    ln -s ../../2hu4_ph65-screen.gpf .
    prepare_dpf4.py -l  `basename $f` -r 2hu4_ph65.pdbqt -p ga_pop_size=200 -p ga_num_evals=2500000 -p ga_run=10 -p rmstol=2.0
    cd ..
    end
    

We have already put a copy of this script in your directory. You can run the script by typing 
    
    
    tcsh
    source prepare_dpfs_set1.csh
    

Note that as each directory is created, it will list the associated ligand on the screen. 

When the script is finished, you will see that it has created a new directory in your working directory, called //2hu4_screen//. 

### Submitting the virtual screen[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=15> "Edit section: Submitting the virtual screen")]

Now you will see that you have created a nested set of directories in one directory called 2hu4_screen, and you are ready to submit your screen: 
    
    
    qsub submit-screen-SI.csh
    

To check on the status of your job, you can type either of the qstat commands listed here: 
    
    
    qstat –u username
    qstat
    

The job will take ~15 minutes to run. 

### Run the scripts to extract the energies[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=16> "Edit section: Run the scripts to extract the energies")]

Now that the virtual screen jobs have completed, we have a lot of data to look through! The easiest way to sort through all the data is with scripts that sort the results by lowest energy of the highest populated cluster for each ligand. 

We have created some scripts to help you analyze the results of the screen. When you are ready to run it, type: 
    
    
    source summary-script.csh
    

This creates a new file called _receptor.summary.txt_ , which summarizes the docking results for each ligand. 

Now we will sort the file by binding energy results: 
    
    
    cat receptor.summary.txt | sort -k11g -t, > receptor.summary.sort.txt
    

### Analyzing the results of the virtual screen[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=17> "Edit section: Analyzing the results of the virtual screen")]

You can look at the results of your virtual screen by opening the _receptor.summary.sort.csv_ output file in any text editor. Do this (look at the results) and report the top binders for your set, which can be found ranked from best to worst in the _receptor.summary.sort.csv_ file. 

Try loading the structures of the top 2-3 binders into VMD (load the .dlg output file into VMD as a PDB file, each cluster is represented as a frame that you can step through with the arrow buttons in the VMD Main window). Do you see any interesting features? Did you find any promising candidates? 

#### On running additional virtual screens with MD-generated protein structures[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=18> "Edit section: On running additional virtual screens with MD-generated protein structures")]

One aspect of the relaxed complex scheme is to use the structures generated in the MD simulations in new virtual screens. This could, for example, allow you to assess the binding of compounds to newly revealed binding pockets found through the simulations. 

You can perform additional virtual screens with any number of protein structures, so long as you have the structure in PDB format, using the steps outlined above. In this case we walked you through a screen of the crystal structure, but you could have also used one of the most dominant structures that you generated from the MD-tutorial. 

##### Relaxed Complex Scheme Rescoring[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=19> "Edit section: Relaxed Complex Scheme Rescoring")]

In this section, we will walk you through a relaxed complex scheme (RCS) rescoring. The general idea behind the technique is to take advantage of the new structural information provided by molecular dynamics simulations in the binding energy estimates that we use for ranking the ligands. Instead of docking one ligand into one protein structure, we will dock one ligand into many structures extracted from the MD. Therefore, instead of one single binding energy estimate, you will actually compute many binding energy estimates, resulting in a "binding spectrum" for each compound. We can then take a weighted average of the spectrum values in order to determine a new mean binding energy estimate that accounts for receptor flexibility. 

We have prepared a separate tutorial on setting up molecular dynamics simulations that you can access [here](<https://www.nbcr.net/pub/wiki/index.php?title=Relaxed_Complex_Scheme%2C_Part_I:_Molecular_Dynamics_and_Clustering>). Clustering the structures extracted from MD is an efficient way to reduce the number of structures we use for docking, without losing too much important structural information. Today we will use clustered structures from a thorough analysis of the neuraminidase simulations that we have previously performed. This RMSD-based clustering approach was performed with GROMOS and various validation protocols were employed. It has been fully described in a recent [paper](<http://www3.interscience.wiley.com/cgi-bin/fulltext/119422880/HTMLSTART?CRETRY=1&SRETRY=0>). 

As you work through this part of the tutorial, you will find that it is very similar to the previous section. The only difference is that we will use scripts to automate the process of doing dockings to each receptor structure. 

### Preparing the receptor files[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=20> "Edit section: Preparing the receptor files")]

The aligned clustered pdbs are in a directory called receptor_pdbs. The RMSD-based clustering analysis that we performed for the neuraminidase simulations (with inhibitor bound) reduced the initial set of 40,000 structures to 28! We can further reduce this number by only redocking into 90% of the ensemble structures. In the case of these simulations, 90% of the holo ensemble can be represented by only 5 structures. 

  * Take a look at the structures in VMD. How similar are they? Where are they different? </li>



These 5 protein structures are what we will redock into for the RCS application. This will save us considerable time and resources for the relaxed complex scheme redocking. 

  * Now we must prepare each of these pdb's for docking in AutoDock4. </li>


    
    
    source receptor-prep-all.csh
    

This last command will prepare all the receptor pdbqt files that are required for AutoDock4. You will see that as it runs it outputs which receptor file it is working on to the screen. When it is finished, it will return the prompt. Note that it created a new directory called receptor_pdbqts in your working directory. 

### Preparing the ligand files[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=21> "Edit section: Preparing the ligand files")]

The ligands we are interested to dock into the MD ensemble will also need to be prepared for use in AutoDock4. Be sure you have your ligand(s) in the directory "ligands" that you want to dock. Since our time is limited today, we will only do the relaxed complex scheme rescoring on oseltamivir. So if you list the contents of the "ligands" directory, you will see the _oseltamivir.pdbqt_ file. The preparation of the ligand was the same as before, using the prepare_ligand4.py script that is distributed with AutoDock (since we've already done this earlier today, we will reuse this file). 

Please note that no matter how many ligands you would like to rescore with the relaxed complex scheme, you would simply add the prepared _ligand.pdbqt_ files into the "ligand" directory. You could have any number of ligands in the directory and the scripts below will process them. 

### Creating the grid and docking parameter files[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=22> "Edit section: Creating the grid and docking parameter files")]

Now we need to create the grid and docking parameter files (the .gpf and .dpf files). To do this, we will use another script. As usual, with this script, it is important to note the following if you are trying this at home: 

  * change the grid center to the appropriate place (make sure all your receptor structures are aligned!)
  * change the number of grid points (npts) to the desired values 
  * change all the paths so they point to the right places 
  * consider adding a variable or two to allow the automated file creation for a directory of ligands 



We have already changed these key parameters within our prepare_rcdocking_gpf_dpf.csh script. So all we have to do is run it now: 
    
    
    source prepare_rcdocking_gpf_dpf.csh
    

As this script runs, it will output which receptor file it is working on to the screen. When it is finished, it will return the prompt. 

### Running the RCS docking experiment[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=23> "Edit section: Running the RCS docking experiment")]

You are now ready to perform the rescoring. You will need to run autogrid for each receptor structure, and then autodock. You can do this using the submission script for the kryptonite cluster here at NBCR: 
    
    
    qsub submit-rc-n1.csh
    

This job will take about 15 minutes to run. 

### Analyzing the results from the RCS docking experiment[edit](</mediawiki/index.php?title=Virtual_Screening_and_RCS_Rescoring_Tutorial&action=edit&section=24> "Edit section: Analyzing the results from the RCS docking experiment")]

We have created scripts that will extract the predicted binding energies from the AutoDock docking log file. There are several ways to do the analysis. For example, you can extract the lowest binding energy found overall, or use the binding energy associated with the most populated cluster. Based on a handful of recent studies, we now think that using the most populated cluster is the best idea, however, success has been demonstrated using the overall lowest energy as well (regardless of cluster size). 

To run the script, type: 
    
    
    qsub submit_summary-rc.sge
    

This creates a file called _summary_osel.csv_ , which has extracted the lowest binding energy in the most populated cluster. Now we can take a weighted mean of these values, according to the population of each of the cluster structures. 

You can do this in Excel, Matlab, or any other number of programs. We know the cluster size from our clustering analysis, and from that we can determine the weight we will apply. Below the cluster populations are listed next to the cluster number. You can see that by using the top 5 clusters, we are able to account for over 90% of the receptor ensemble that was sampled through the MD simulations. 
    
    
    Cluster     % Population
    n1ho_cl1      37.8
    n1ho_cl2      22.1
    n1ho_cl3      14.5
    n1ho_cl4       9.0
    

How would you calculate a weighted average? Think about it. Is your weighted average lower than, higher than, or the same as the single crystal structure - oseltamivir docking you performed? Dynamics changes things! 

If time allows, take a look at some of the RCS DLG files and examine how AutoDock docks oseltamivir in these new structures. Do they all bind in the sialic acid pocket?
