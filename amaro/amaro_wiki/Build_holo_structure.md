# Build holo structure

Sometimes it can be useful to have the 'native' holo structure in .PARM7 and .RST7 formats - it includes the ligand and the protein in the configuration that exists in the X-ray crystal structure. This is necessary to run 'dig_deeper.py' in 'similar' mode. 

In order to make the holo structure from the crystal structure, first create a folder in which to do your calculations. I recommend doing this within or near the directory that you made the apo structure in. 
    
    
    mkdir holo_native
    cd holo_native
    

Now download the PDB structure to the 'holo_native' directory. I'm running calculations on HSP90, so I downloaded the PDB structure 1YET. So now I have the file '1yet.pdb' in my holo_native directory. 

Now let's create a LEAP script that will generate our holo files. I named it 'make_holo_files.leap': 
    
    
    source leaprc.protein.ff14SB
    source leaprc.gaff
    source leaprc.water.tip4pew
    set default PBRadii mbondi2
    loadoff ../ligand/gdm.lib
    loadamberparams ../ligand/gdm.frcmod
    WAT = T4E
    HOH = T4E
    loadAmberParams frcmod.ionsjc_tip4pew
    loadAmberParams frcmod.tip4pew
    
    holo = loadpdb 1yet.pdb
    
    saveamberparm holo holo.parm7 holo.rst7
    
    savepdb holo holo_postleap.pdb
    
    check holo
    charge holo
    
    quit
    

Note that you will need to change the 'loadoff' and 'loadamberparams' file to point to the .lib and .frcmod files that you made when you parametrized your ligand. You will also need to change the 'loadpdb' command to point to your own PDB file. 

Then, run this command thru TLEAP: 
    
    
    tleap -f make_holo_files.leap
    

Make sure that no errors occurred and you can ignore the charge warnings (unless you want to simulate this, then you'll need to include code to solvate and add counterions like you did with the apo structure). 

This should have created holo.parm7 and a holo.rst7 files. You can then use these files for, say, dig_deeper.py.
