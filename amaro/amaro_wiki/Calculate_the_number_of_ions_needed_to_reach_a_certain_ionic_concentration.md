# Calculate the number of ions needed to reach a certain ionic concentration

## Preparing the input files[edit](</mediawiki/index.php?title=Calculate_the_number_of_ions_needed_to_reach_a_certain_ionic_concentration&action=edit&section=1> "Edit section: Preparing the input files")]

First prepare the PDB file to match the AMBER force field specifications Residue naming: 

  * HIP - Histidinium Ion
  * HIE - N-epsilon protonated Histidine 
  * HID - N-delta protonated Histidine 
  * ASH - Protonated Aspartic acid 
  * GLH - Protonated Glutamic acid 
  * CYX - Cysteine residues with disulfid-bridges 



Delete ALL hydrogen atoms (if the pdb was created in maestro, rename NMA terminal group to NME and CA in NMA/NME to CH3) (if appropriate, check TER line is present between protein and ligand) 
    
    
    export AMBERHOME=/usr/local/amber9
    export PATH=$PATH:$AMBERHOME/exe
    tleap
    

In xleap (example using 3CMS_jesper_noh.pdb): 
    
    
    mol = loadpdb 3CMS_jesper_noh.pdb
    

First check for errors 
    
    
    check mol
    

Fix any errors that might occur. It is much easier to remove the hydrogens and let AMBER add these itself. Close contact errors are not FATAL, but check them to see if something seems wrong Next bond the disulfid-bridges: 
    
    
    bond mol.47.SG mol.52.SG
    bond mol.207.SG mol.211.SG
    bond mol.250.SG mol.283.SG
    

Next, solvate the system: 
    
    
    solvatebox mol TIP3PBOX 10     
    

This solvates in a rectangular box - solvateoct solvates in a truncated octahedral box TIP3PBOX is a specific water model, others are available The number 10 is the buffer distance, meaning the distance from the solute to the box-wall. 

Next thing to do is adding ions, firstly to neutralize, but secondly it may be important for your simulation to include a certain ionic strength. In this setup a ionic strength of 0.07 mol/L is used. In leap the box-dimensions are given after solvation, use these to calculate the volume in Liters (angstroms to decimeters is 10^-9) 
    
    
    V = 66E-9 x 75E-9 x 92E-9 = 4.6E-22 L
    Number of ions = V * ionic strength * Na
    Number of ions = 4.6E-22 L * 0.07 mol/L * 6.0221414E23 = 20
    

Check the current charge: 
    
    
    charge mol
    

The system currently has a charge of -12 The system needs to be neutralized, so in this case there needs to be added 16 Sodium-ions(Na+) and 4 Chlorid-ions (Cl-) 
    
    
    addions mol Na+ 16 Cl- 4
    

Check your unit again, and if there are no errors write the paramters files needed for the simulation. 
    
    
    saveamberparm mol 3cms_apo.prmtop 3cms_apo.incrd
    quit
    

In the current folder there is a log-file leap.log which contains all the commands you have entered and the output of these commands for future reference.
