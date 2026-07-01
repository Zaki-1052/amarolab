# APBS

# APBS[edit](</mediawiki/index.php?title=APBS&action=edit&section=1> "Edit section: APBS")]

APBS is a program used to calculate molecular electrostatics using the Poisson-Boltzmann equation. 

## Installation[edit](</mediawiki/index.php?title=APBS&action=edit&section=2> "Edit section: Installation")]

Cd to someplace in your computer and clone the git repository: 
    
    
    git clone https://github.com/Electrostatics/apbs-pdb2pqr.git
    

  


## Alternative Installation[edit](</mediawiki/index.php?title=APBS&action=edit&section=3> "Edit section: Alternative Installation")]

Download from the following location: <https://sourceforge.net/projects/apbs/>

Save the tar.gz file somewhere. Then go to the location and type: 
    
    
    tar -xzf APBS-1.5-linux64.tar.gz
    

  
Update your bashrc: 
    
    
     
    export PATH="/home/*USERNAME*/Downloads/APBS-1.5-linux64/bin:$PATH"
    export LD_LIBRARY_PATH="/home/jfurrer/Downloads/APBS-1.5-linux64/lib:$LD_LIBRARY_PATH"
    

Now you can see that APBS is located in the bin/ folder. 

The "Inputgen" program is located in: share/apbs/tools/manip/inputgen.py
