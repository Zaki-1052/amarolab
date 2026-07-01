# CADD

## Computer-Aided Drug Design Pipeline Tutorials[edit](</mediawiki/index.php?title=CADD&action=edit&section=1> "Edit section: Computer-Aided Drug Design Pipeline Tutorials")]

### Tutorial files[edit](</mediawiki/index.php?title=CADD&action=edit&section=2> "Edit section: Tutorial files")]

Example output tarball/PDBs? 

### Preparing the System[edit](</mediawiki/index.php?title=CADD&action=edit&section=3> "Edit section: Preparing the System")]

### Get the PDB[edit](</mediawiki/index.php?title=CADD&action=edit&section=4> "Edit section: Get the PDB")]

Today we will be working with the N1 neuraminidase protein. This first section will take place in a terminal on your desktop or laptop. 

  * Download 2HU4 from the [[website](<http://www.rcsb.org/pdb/home/home.do%7CRCSB>)] (PDB databank)



### Process in VMD[edit](</mediawiki/index.php?title=CADD&action=edit&section=5> "Edit section: Process in VMD")]

Launch VMD. On your local terminal, type: 
    
    
     vmd
    

Load the _2HU4.pdb_ structure into VMD (by now we assume you are familiar with VMD. If you need help, ask a proctor!) 

  * In the VMD Main window, select File -> New Molecule
  * Browse for _2HU4.pdb_



Notice that the structure is a tetramer. As the binding site does not bridge across multiple domains (i.e. it only involves one subunit) we only need to extract and work with one of the 8 chains resolved in the file. 

  * In the graphics window, select "chain B" and set the display type to **New Cartoon**
  * Make an additional selection for "resid 801" and set the display type to **VDW**



This shows you tamiflu (aka oseltamivir) bound in the active site of the N1 neuraminidase. We want to make separate files for the protein and the ligand. Although we can do this in many ways, we will do it here in VMD. 

  * Open a TkCon window by selecting Extensions -> Tk Console
  * At the prompt make the protein selection by typing: 


    
    
    set prot [atomselect top "chain B"]
    

  * Then write the selection to a pdb file by typing:


    
    
    $prot writepdb 2HU4_B.pdb
    

  * Now make another selection for tamiflu by typing:


    
    
    set tami [atomselect top "resid 801"]
    

  * Then write the selection to another pdb file:


    
    
    $tami writepdb oseltamivir.pdb
    

### GPF/DPF templates[edit](</mediawiki/index.php?title=CADD&action=edit&section=6> "Edit section: GPF/DPF templates")]

To run the screen, we need affinity and electrostatic grids for all the atom types in the screen set. To generate these files, we need to create templates for the GPF (grid parameter file) and DPF (docking parameter file) files that AutoGrid will use. Instead of actually creating the grid and docking parameter files, we will just provide templates that will be processed in the pipeline to create the files. If we fail to do this, AutoDock will not be able to perform the docking for the missing atoms types. 

### GPF[edit](</mediawiki/index.php?title=CADD&action=edit&section=7> "Edit section: GPF")]

You will need to know the gridcenter and grid size of the grid box you wish to create. Typically, we change the gridcenter to the center of the active site and the npts (number of points) to something that you will know will encompass the entire active site. If you are doing this for the first time, it may be helpful to switch to the ADT GUI to confirm correct box placement, like you did in the AutoDock tutorials. If you already know the parameters you wish to use, you may enter them in command line. 

For this neuraminidase protein, the center of the active site is at {3.73 20.236 113.925} and the npts should be changed to {64 72 66} to be sure the grids will cover the entire binding site. Therefore, the _2HTY_A.gpf_ file should like this: 
    
    
     npts 64 72 66
     gridcenter 3.73 20.236 113.925
    

### DPF[edit](</mediawiki/index.php?title=CADD&action=edit&section=8> "Edit section: DPF")]

This file contains all the different docking options utilized in AD4. A lot of these you can probably safely use without changing, but you will want to modify / optimize some parameters in the docking parameter file in order to validate the program for your target. A good first place to start is by altering the default values for ga_num_evals (total number of energy evaluations), ga_pop_size (population size), and ga_num_generations (number of generations). The default ga_num_evals is about 2 orders of magnitude too small for most ligands. In particular, when you perform a virtual screen, you need to set the ga_num_evals high enough that it allows all ligands in your screening set to converge. Typically this is 5-10 million. 

To improve the clustering of the docking results, you may need to do system-specific parameter optimization for AutoDock. We don’t have time today to go through a full iteration of this. 

Specifically for neuraminidase, we want the population size to be 200, 10 total dockings, 50000 energy evaluations and an RMS tolerance of 2. For your real research projects, you will probably want to set ga_run to 50 or 100 (in order to generate better statistics). Here is what the _2HTY_A.dpf_ file looks like: 
    
    
     ga_pop_size 200 
     ga_run 10                          
     ga_num_evals 50000 
     rmstol 2.0
    

Remember, these are just templates! They're not the actual grid and docking parameter files- those will be made in the pipeline. 

## Running the Virtual Screen[edit](</mediawiki/index.php?title=CADD&action=edit&section=9> "Edit section: Running the Virtual Screen")]

### Small molecule databases[edit](</mediawiki/index.php?title=CADD&action=edit&section=10> "Edit section: Small molecule databases")]

In virtual screening, you will dock many ligands (from a library of small molecules) to a single receptor of choice. Ligand libraries can be prepared with a simple script but many come already prepared. There are a few well-curated, publicly available small molecule databases that can be used for a variety of virtual screen or docking applications. 

The **NCI diversity set 2** is distributed from the National Cancer Institute and contains approximately 1900 chemically diverse compounds. It is a good place to start for efficient "search in the dark" type applications. The NCI makes these compounds (and those listed in the full NCI database) available for the experimentalists to test, so it is a good place to start. It has been processed for use in AutoDock4 and is available from NBCR for your docking experiments. The **ZINC database** is maintained by the Shoichet lab at UCSF and is an excellently curated very large small molecule database. A variety of file formats are maintained. See <http://blaster.docking.org/zinc>. The NBCR also houses an AutoDock4 curated version of one of the recent ZINC library distributions. The **Available Chemicals Directory** (ACD) and **Hit2Lead** are other popular small molecule databases. 

We will perform a virtual screen of the crystal structure against the NCI diversity set (NCIDS). It is a reduced and representative set of full NCI database, which contains approximately 250,000 compounds. 

### Specify Parameters[edit](</mediawiki/index.php?title=CADD&action=edit&section=11> "Edit section: Specify Parameters")]

Open Vision 1.5.6 (download). Choose File -> Open to load the workflow file (filename goes here). This opens up a network of nodes which are connected to each other. Running this pipeline will call a preset order of different applications and operations. Each node will lead you to another workflow that is a subset of this one. For example, if you double-click on the VirtualScreening node, the virtual screening workflow appears. This is the workflow that's called when the VirtualScreening node is highlighted. 

The following is a description of the different nodes that are in the network. The top 4 nodes are the inputs: 

  * **GetStructuresFromDir** node will get a list of PDBs/PQRs/PDBQTs from the user as a list of input receptors and each one of the these receptor files will be later used to run virtual screening. This directory should also contain a template GPF and a template DPF for each receptor. The workflow assumes that the receptor PDB file and its corresponding template GPF/DPF have the same base filename. Browse for the directory where the PDB files and template GPFs and DPFs are stored.


  * **PublicServerLigandDB** allows the user to choose a ligand library from our server. For neuraminidase, we will be using the NCI_DS2 library. Note that this node can be replaced by LocalLigandDirectory or UrlLigandDB.


  * **FilterLigandNode** allows the user to filter the ligands. Note that our server are unable to support ligand libraries that have more than 2500 ligands. This option will be left at the default.


  * **PreserverChargers?** is a checkButton node so that the charges are preserved for PrepareReceptor if checked. Make sure this is checked.


  * In this workflow, the **Iterate** node will go through the PDB list and perform virtual screening on each receptor.


  * The **DownloadSaveDir** node at the bottom downloads the virtual screening results to the parent directory that contains the input directory to the GetStructuresFromDir node.



### Running the Pipeline[edit](</mediawiki/index.php?title=CADD&action=edit&section=12> "Edit section: Running the Pipeline")]
    
    
    The **VirtualScreening** node is where all the information is sent and the screen is ran. Here's a break down of what is contained in that node:
    

  
Click the yellow lightening bolt button on the task bar to run the workflow. You know the workflow is running when nodes are outlined in bright red. When no nodes have the bright red border, the virtual screen is complete. 

### Analysis[edit](</mediawiki/index.php?title=CADD&action=edit&section=13> "Edit section: Analysis")]

When the run is finished, there are several things we need to do in order to evaluate the results: 

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



## See also[edit](</mediawiki/index.php?title=CADD&action=edit&section=14> "Edit section: See also")]

[Docking Programs](</mediawiki/index.php/Docking_Programs> "Docking Programs")

[Glide](</mediawiki/index.php/Glide> "Glide")
