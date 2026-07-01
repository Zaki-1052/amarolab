# BD preparation procedure for a large virus

# Virus Preparation Procedure for Brownian Dynamics (BD)[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=1> "Edit section: Virus Preparation Procedure for Brownian Dynamics \(BD\)")]

This manual specifies the process taken in order to prepare and run BD simulations of the virus structure. 

## You will need:[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=2> "Edit section: You will need:")]

### The necessary programs:[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=3> "Edit section: The necessary programs:")]

  * The BrownDye package (<http://browndye.ucsd.edu/>)
  * APBS (<http://www.poissonboltzmann.org/>)
  * Python 2.7



### The necessary scripts[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=4> "Edit section: The necessary scripts")]

(you can download these from the [scripts page](</mediawiki/index.php/ScriptsMain> "ScriptsMain")) 

  * myown_pdb2pqr.py
  * pqr_fix_radii.py (place this in the PYTHONPATH)
  * big_pb.py
  * myown_mergedx.py (optional)
  * residue_test_charges.py
  * surface_spheres.py
  * surface_spheres_exclude.py (optional)
  * make_surface_sphere_list.py
  * results_gather.py
  * virus_resubmit.py



### The necessary files:[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=5> "Edit section: The necessary files:")]

  * A PDB structure of the virus (or other large object). From now on, assume its called virus.pdb
  * A PBD structure of the ligand with each of the atoms assigned to a different residue name/number. This will allow for more accurate simulations. If included, assume it's called ligand.pdb. (optional)
  * A PDB structure of the ligand with all the atoms in a single residue name/number. From now on, assume its called ligand_one_resid.pdb (unless you don't have the ligand with atoms assigned to different residue name/numbers, then assume its just called ligand.pdb)
  * A Charmm forcefield .dat file: [Example CHARMM.DAT](</mediawiki/index.php/Example_CHARMM.DAT> "Example CHARMM.DAT")
  * An input.xml file for Browndye with the desired parameters. [Example input.xml](</mediawiki/index.php/Example_input.xml> "Example input.xml")



## File Preparation Procedure[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=6> "Edit section: File Preparation Procedure")]

Note: It is HIGHLY recommended that you are familiar with Browndye and APBS before attempting simulation of such a large and complicated system as a virus. Both programs include tutorial and sample systems that are much smaller and simpler, and once you have mastered these, you will find dealing with the large system much easier. It is also recommended that you have at least a basic understanding of Python and script importing so that you will have the ability to deal with small errors that may occur. I also assume that you have basic knowledge of Linux shell programs such as 'grep'. 

Many of the commands below will take hours or days to run, so be prepared for some long waits if you have a large structure with many atoms. 

Most or all of the programs below will provide helpful instructions if run with the '-h' argument. 

BrownDye will need to be compiled on any computers or supercomputers you are planning to run on. 

### make PQRs and PQRXMLs from PDBs:[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=7> "Edit section: make PQRs and PQRXMLs from PDBs:")]

If you already have a PQR of either structure, you can skip this step for that structure... 

`python myown_pdb2pqr.py -x virus.pqrxml -r -f ../dat/CHARMM.DAT -t charmm virus.pdb virus.pqr   
python myown_pdb2pqr.py -x ligand.pqrxml -r -f ../dat/CHARMM.DAT -t charmm ligand.pdb ligand.pqr   
python myown_pdb2pqr.py -x ligand_one_resid.pqrxml -r -f ../dat/CHARMM.DAT -t charmm ligand_one_resid.pdb ligand_one_resid.pqr `

  
You may prefer to use the PDB2PQR program instead, and if it runs without errors, this may be the preferred option. My structure was too big to run successfully on the ordinary PDB2PQR. After running PDB2PQR, you will have to use the pqr2xml program that comes with BrownDye 

Using 'grep' or other similar program, see if there are any atoms with a radius of X.XXX, and modify pqr_fix_radii.py if necessary. The simulation will fail if any atoms have a non-numerical radius. 

### Make spaces in the pqr file for APBS[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=8> "Edit section: Make spaces in the pqr file for APBS")]

When we are dealing with very large PQR files, sometimes fields will abut one another in the file, and this will confuse APBS. The command below should at least place a space between the X,Y,Z coordinates. If APBS complains anyways, you may need to see if it's because other columns in the PQR file are touching without a space between them. 

` sed 's/-/ -/g' virus.pqr > virus_forapbs.pqr `

### make APBS input:[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=9> "Edit section: make APBS input:")]

Replace the --fadd argument with the number of Angstroms of buffer between the edge of the molecule and the edge of the grid. Replace the --space argument with the maximum resolution of the DX grid. 

` python big_pb.py --fadd=50 --space=1.1 virus_forapbs.pqr `

### run all of the APBS calcs[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=10> "Edit section: run all of the APBS calcs")]

This will create a folder called apbs_async_all. Go into that folder and run the following command, which will run a series of APBS commands for all the pieces of the grid. ` bash run_all.bash ` Now you will have several DX files in the same folder. 

### figure out how many data points in each direction[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=11> "Edit section: figure out how many data points in each direction")]

You'll need to figure out how many data points will be in the final DX file. You can do this by looking at the header of one of the DX files and multiplying the number of data points in each of the X,Y, and Z directions by the number of parallel grids in each of those directions. 

Note: you don't need to find the number of data points in each direction if you use the script myown_mergedx.py as an alternative. 

Run the command below, replacing the '1340's and the '1176' with the number of grid points in each of the X,Y,Z directions. Notice that the pot?_*.dx followed by pot??_*.dx lists the DX files in proper numerical order. (If you have more than 100 DX files, add pot???_*.dx to the end of these commands). 

` mergedx 1340 1340 1176 pot?_*.dx pot??_*.dx `

rename the 'gridmerged.dx' file into 'virus.dx'. Then also make a DX file for the ligand. (big_pb.py should not be necessary for small structures, but be careful to use the same paramters as the virus when running APBS.) 

### make reaction file[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=12> "Edit section: make reaction file")]

You will need to make a reaction criteria file for the Brownian dynamics simulations. Run the virus_rxn_find.py python script with the '-h' argument only to see a help documentation for how to construct the arguments. 

` python virus_rxn_find.py -r virus.pqr -l ligand_one_resid.pqr -n 3 -o rxns.xml -d 7.500000 -x ARG-368-NH2:SIA-1-O1B,ARG-368-NH1:SIA-1-O1A,ARG-152-NH2:SIA-1-O10,ARG-293-NE:SIA-1-O8 `

If you are making several different sites on the virus (such as the active site and secondary site on neuraminidase, and the site on hemagglutinin), then you can combine these reaction XML files easily by hand. 

### Run bd_top[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=13> "Edit section: Run bd top")]

Make sure the input.xml file has the virus.pqrxml, ligand.pqrxml, and virus.dx files in their respective fields of input.xml. 

` bd_top input.xml `

With each of the subsequent steps, if you kill bd_top, by immediately running again after the command was entered, bd_top should start up where you left off. 

### kill residue_test_charges and run the python script instead[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=14> "Edit section: kill residue test charges and run the python script instead")]

If residue_test_charges dies because of the large system, then use the script I prepared for the occasion. 

` python residue_test_charges.py virus.pqr > virus-charges.xml `

### kill surface_spheres and run the python script instead[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=15> "Edit section: kill surface spheres and run the python script instead")]

If surface_spheres dies because of the size of the system, use the following command. Use the '-h' argument to documentation about this program. 

You can run this command beforehand when you first obtain the virus.pqr file and copy over the premade surface atoms file. This command seems to take an especially long time. 

Obviously, you should add your own numbers to this command from the header of the virus.dx file that you made. 

` python surface_spheres.py -p virus.pqr -o virus_surface.pqrxml -c "-613.3415" "-613.0740" "-634.2800" -n 1340 1340 1176 -s 0.904 0.899 1.10 -r 3.0 -i ins-virus.xml `

This next step is optional, and will simply remove any atoms on the interior of the virus that will otherwise diminish the efficiency of the program. (Use xml2pqr to make a pqr file of the virus-surface.pqrxml file before running the command below.) python2.7 surface_spheres_exclude.py -p virus_surface.pqr -o virus_surface.pqrxml -c "-613.3415" "-613.0740" "-634.2800" -n 1340 1340 1176 -s 0.904 0.899 1.10 -r 8.0 

Make backups of ins-virus.xml and virus-surface.xml and save them in a different place or under a different name so that bd_top won't write over them with subsequent commands or if you run bd_top a second time. 

### kill inside_points[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=16> "Edit section: kill inside points")]

If inside_points fails, then make a new ins-virus.xml from your backup that you should have done in the previous step. 

### Run compute_effective_volumes with the surface atoms instead of the full structure[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=17> "Edit section: Run compute effective volumes with the surface atoms instead of the full structure")]

If compute_effective_volumes fails, run it with the surface of the virus instead of the full virus structure. (replace the solvent and solute dielectric values if desired) 

` compute_effective_volumes -solvent 78 -inside ins-virus.xml -spheres h1n1-virus.xml -solute 2 > virus-volume.xml `

### if make_surface_sphere_list fails, run this command[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=18> "Edit section: if make surface sphere list fails, run this command")]

` python make_surface_sphere_list.py -s virus.pqrxml -r virus-surface.xml -1 rxns.xml -o virus-surface-atoms-hard.xml `

After bd_top is complete, you'll have all the files you need to run a BD simulation of your system. 

  


## Running Procedure[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=19> "Edit section: Running Procedure")]

Once you have all the preparatory files generated, you can run your simulation. 

` nam_simulation virus-ligand-simulation.xml `

### Running BrownDye on a supercomputer[edit](</mediawiki/index.php?title=BD_preparation_procedure_for_a_large_virus&action=edit&section=20> "Edit section: Running BrownDye on a supercomputer")]

You will need to transfer all your relevant files used in the simulation to a supercomputer (I used Comet and Gordon). You will also need to have a version of BrownDye compiled on the supercomputer. 

Because BrownDye simulations are embarassingly parallel, you can run as many simulations as you want, but you'll probably want to run one instance of BrownDye per node. So I always request one node with all the cores, and set BrownDye to use all those cores. 

You can create a submission script and simulation file by hand. But for each run, you'll want to create a new BrownDye simulation file, with the "results", "trajectory", and "random seed" options changed between each ones. 

But given a template submission and simulation files, the script virus_resubmit.py is intended to perform this task in an automatic fashion. Assuming that simulation_TEMPLATE.xml and submit_TEMPLATE.xml are both in the current directory, you can run the following command to request 10 nodes and launch them to the queue: 

` python virus_resubmit 10 `

If you run the command again, it should relaunch some more jobs without overwriting the previous ones. Delete the results files before running virus_resubmit.py to start the simulations over. 

The script results_gather.py is intended to construct statistics from the results XML files after the simulations are complete. 

` python results_gather.py results*.xml `

You may need to modify the script to act properly depending on how you named your binding sites in the reactions XML file.
