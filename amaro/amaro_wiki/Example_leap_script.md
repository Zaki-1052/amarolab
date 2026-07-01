# Example leap script

Here is an example LEAP script: 

Be sure to change "apo.pdb" to your protein. 
    
    
    source leaprc.protein.ff14SB
    source leaprc.gaff
    source leaprc.water.tip4pew
    set default PBRadii mbondi2
    WAT = T4E
    HOH = T4E
    loadAmberParams frcmod.ionsjc_tip4pew
    loadAmberParams frcmod.tip4pew
    
    apo = loadpdb apo.pdb
    
    solvateoct apo TIP4PEWBOX 8
    addIons2 apo K+ 0
    addIons2 apo K+ 8
    addIons2 apo Cl- 8
    
    
    saveamberparm apo apo.parm7 apo.rst7
    
    savepdb apo  apo_postleap.pdb
    
    
    check apo
    charge apo
    
    quit
    

Run this command by typing the following: 

tleap -f [name of leap script]
