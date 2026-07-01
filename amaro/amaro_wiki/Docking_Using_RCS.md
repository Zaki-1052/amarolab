# Docking Using RCS

## Tutorial on Docking Using Relaxed Complex Scheme (RCS)[edit](</mediawiki/index.php?title=Docking_Using_RCS&action=edit&section=1> "Edit section: Tutorial on Docking Using Relaxed Complex Scheme \(RCS\)")]

Before you begin, if you are unsure how to run multiple commands in a series check out the end of the tutorial for instructions. This is useful if you are trying to dock many ligands into many conformational structures. This may be obvious to some. 

  1. Place all ligands.pdb and non_redundant_protein_structures.pdb into two separate directories. Also for the receptors, put each of those in their own directories. Rename each of those receptors receptor.pdb. 
  2. Convert all ligand and protein _pdb_ files to _pdbqt_ files 

**Set the environmental variables for the _pdb to pdbqt_ scripts. This should be done in the terminal before running the conversion script**
    
    source /net/data/ddadon/screen_scripts/mglenv
    

**If the protein does not have hydrogens use _pbd2pqr_ to prepare the protein**
    
    <http://www.nbcr.net/pdb2pqr/>
    

**(This might be one of those places where you might want to run multiple commands in a series.)The script for actually converting the ligand.pdb to ligand.pdbqt is:**
    
    /net/linux/src/MGLTools/share/lib/python2.4/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l  <PDBFILENAME.PDB> -o <PDBQTFILENAME.PDBQT>
    

**The script for converting the receptor.pdb to receptor.pdbqt is:**
    
    /net/linux/src/MGLTools/share/lib/python2.4/site-packages/AutoDockTools/Utilities24/prepare_receptor4.py -r  <PDBFILENAME.PDB> -o receptor.pdbqt
    

  3. If using **AutoDock 4** continue. If using **AutoDock Vina skip** to step _**4**_. 

**First create the grid parameter file (.gpf) for each structure with any ligand**
    
    /net/linux/src/MGLTools/share/lib/python2.4/site-packages/AutoDockTools/Utilities24/prepare_gpf4.py -l <LIGAND_FILENAME.pdbqt> -r <RECEPTOR_FILENAME.pdbqt> -o <FILENAME>.gpf
    

**Once you have made the gpf, edit it using gedit or vi**

     * Edit grid center (this is the center of your grid map)
     * Edit the number of points in the **x, y, and z** directions. (Points are separated by the size of your grid spacing. Usually, the default is **0.375A**.)
     * Set your spacing size, though the default, 0.375A, is usually appropriate.
     * Edit the **"atom types"**

To find all the atoms in your ligand library, go to the directory with all the _ligand.pdbqt_ files at type: 
    
    cat *.pdbqt | awk '{print $11 "\n" $12}' | sort | uniq
    

Do not just modify the ligand types but also modify the part in that file that says something like _map filename.atomtype.map_ **You now have your _.gpf's_ for each protein conformation. Make sure that each receptor is being done in its own directory. ** **Create .map files for all of the receptors using autogrid - > start with a grid parameter file (.gpf) and output a grid log file (.glg). The map files will be created as a result of this command in the current working directory and need not be included in this command. **
    
    /net/linux/src/autodocksuite-4.0.1/src/autogrid-4.0.0/autogrid4 -p GRIDFILENAME.gpf -l GRIDFILENAME.glg
       example   
    
    
    find -name *Cluster_* | awk '{print "cd " $1 "/; /net/linux/src/autodocksuite-4.0.1/src/autogrid-4.0.0/autogrid4 -p autogrid.gpf -l autogrid.glg; cd /net/data/ddadon/mutant_influenza/mutant_screens/mutant_structures/"}'
    

  
**Make docking parameter files (.dpf)**
    
    /net/linux/src/MGLTools/share/lib/python2.4/site-packages/AutoDockTools/Utilities24/prepare_dpf4.py -l <LIGANDFILENAME.pdbqt> -r <RECEPTORFILENAME.pdbqt> -o autodock.dpf
    

Change the parameters using **gedit**. Tweak these parameters until AutoDock can redock a positive control correctly: 
    
    ga_pop_size, ga_num_evals, ga_num_generations,rmstol, ga_run
    

Run the docking each time to check the control. From the dlg that will be created, you can find out whether to use the lowest energy or the most populated score. This can be found in the dlg after the eigth time the word "CLUSTER" appears in the text. 
    
    /net/linux/src/autodocksuite-4.0.1/src/autodock-4.0.1/autodock4 -p <FILENAME.dpf> -l  <FILENAME>.dlg
    

To dock all ligands into one receptor, use: id for the job, directory for the ligands, directory of the rec. 
    
    php set_up_screen.php bound-fr289_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr289_R/
    

**To set up the whole screen, mimic the contextual example below:**

[jdurrant@ctbp1 screen]$ ls -1 ../receptors_QR/ bound-fr105_R bound-fr117_R bound-fr129_R bound-fr133_R bound-fr135_R bound-fr13_R bound-fr145_R bound-fr155_R bound-fr163_R bound-fr173_R bound-fr197_R bound-fr19_R bound-fr205_R bound-fr229_R bound-fr235_R bound-fr249_R bound-fr255_R bound-fr269_R bound-fr277_R bound-fr289_R bound-fr305_R bound-fr313_R bound-fr31_R bound-fr327_R bound-fr347_R bound-fr351_R bound-fr367_R bound-fr387_R bound-fr397_R bound-fr53_R bound-fr69_R bound-fr75_R bound-fr95_R 

[jdurrant@ctbp1 screen]$ ls -1 ../receptors_QR/ | awk '{print "php set_up_screen.php " $1 " ../ligands_final_pdbqt/ ../receptors_QR/" $1 "/"}' 

php set_up_screen.php bound-fr105_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr105_R/ 

php set_up_screen.php bound-fr117_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr117_R/ 

php set_up_screen.php bound-fr129_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr129_R/ 

php set_up_screen.php bound-fr133_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr133_R/ 

php set_up_screen.php bound-fr135_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr135_R/ 

php set_up_screen.php bound-fr13_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr13_R/ 

php set_up_screen.php bound-fr145_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr145_R/ 

php set_up_screen.php bound-fr155_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr155_R/ 

php set_up_screen.php bound-fr163_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr163_R/ 

php set_up_screen.php bound-fr173_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr173_R/ 

php set_up_screen.php bound-fr197_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr197_R/ 

php set_up_screen.php bound-fr19_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr19_R/ 

php set_up_screen.php bound-fr205_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr205_R/ 

php set_up_screen.php bound-fr229_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr229_R/ 

php set_up_screen.php bound-fr235_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr235_R/ 

php set_up_screen.php bound-fr249_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr249_R/ 

php set_up_screen.php bound-fr255_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr255_R/ 

php set_up_screen.php bound-fr269_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr269_R/ 

php set_up_screen.php bound-fr277_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr277_R/ 

php set_up_screen.php bound-fr289_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr289_R/ 

php set_up_screen.php bound-fr305_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr305_R/ 

php set_up_screen.php bound-fr313_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr313_R/ 

php set_up_screen.php bound-fr31_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr31_R/ 

php set_up_screen.php bound-fr327_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr327_R/ 

php set_up_screen.php bound-fr347_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr347_R/ 

php set_up_screen.php bound-fr351_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr351_R/ 

php set_up_screen.php bound-fr367_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr367_R/ 

php set_up_screen.php bound-fr387_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr387_R/ 

php set_up_screen.php bound-fr397_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr397_R/ 

php set_up_screen.php bound-fr53_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr53_R/ 

php set_up_screen.php bound-fr69_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr69_R/ 

php set_up_screen.php bound-fr75_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr75_R/ 

php set_up_screen.php bound-fr95_R ../ligands_final_pdbqt/ ../receptors_QR/bound-fr95_R/ 

[jdurrant@ctbp1 screen]$ ls -1 ../receptors_QR/ | awk '{print "php set_up_screen.php " $1 " ../ligands_final_pdbqt/ ../receptors_QR/" $1 "/"}' | csh 

**Then to submit the entire screen at once, qsub all of these bash files:**
    
    ls -1 *.bash | awk '{print "qsub " $1}'  | csh
    

  4. To run Vina: 
    
    net/linux/pkg/autodock-vina-1/vina --receptor receptor.pdbqt --ligand ligand.pdbqt  --center_x 	72.67 --center_y 59.50 --center_z 127.76 --size_x 35.42 --size_y 25.22 --size_z 21.35 --out 	ligand.out
    

**How to do multiple things in a series example:**
    
    ls -1 *.pdb | awk '{print ""}'
    
      ls -1 *.pdb | awk '{print "/net/linux/src/MGLTools/share/lib/python2.4/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l " $1 " -o " $1 "qt"}'
    
      ls -1 *.pdb | awk '{print "/net/linux/src/MGLTools/share/lib/python2.4/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l " $1 " -o " $1 "qt"}' | csh
