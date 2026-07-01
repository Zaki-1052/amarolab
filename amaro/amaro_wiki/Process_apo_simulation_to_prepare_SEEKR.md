# Process apo simulation to prepare SEEKR

...Lots of stuff to add here... 

Here is a script to postprocess your apo simulations through LEAP to replace missing atoms (replace 'frame997.pdb' with a PDB from your apo simulation: 

Make sure that the HIS's are correctly named in the input PDB file 
    
    
    source leaprc.protein.ff14SB
    source leaprc.gaff
    source leaprc.water.tip4pew
    set default PBRadii mbondi2
    WAT = T4E
    HOH = T4E
    loadAmberParams frcmod.ionsjc_tip4pew
    loadAmberParams frcmod.tip4pew
    
    apo = loadpdb frame997.pdb
    
    savepdb apo  apo_wet.pdb
    
    check apo
    charge apo
    
    quit
    

MAKE SURE YOU NEUTRALIZE WITH ADDIONS2 IF NECESSARY
