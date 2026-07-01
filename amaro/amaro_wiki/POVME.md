# POVME

# POVME 3.0[edit](</mediawiki/index.php?title=POVME&action=edit&section=1> "Edit section: POVME 3.0")]

[POVME3.0 is hosted on GitHub. The landing page has installation and running instructions.](<https://github.com/POVME/POVME>)

  


## Running POVME on the TSCC[edit](</mediawiki/index.php?title=POVME&action=edit&section=2> "Edit section: Running POVME on the TSCC")]

Log into TSCC 
    
    
       username@tscc-login.sdsc.edu
    

Check if you have conda 
    
    
       conda init
    

If you do not, install the conda package 
    
    
       wget <https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh>
    

Run the conda installer script 
    
    
       bash Anaconda3-2022.05-Linux-x86_64.sh
    

Exit the machine and log in again 
    
    
       exit
       username@tscc-login.ucsd.edu
    

Run the following commands to clean up and delete the unnecessary files after installation 
    
    
       conda install -c anaconda anaconda-clean
       anaconda-clean
    

Install RDKit 
    
    
       conda install -c rdkit rdkit
    

## Set your environment[edit](</mediawiki/index.php?title=POVME&action=edit&section=3> "Edit section: Set your environment")]

POVME3 needs python2.7 to run, so create that environment with conda 
    
    
       conda create -n povme python=2.7
    

Install POVME with pip 
    
    
        pip install povme
    

  
Now, activate the POVME environment with conda 
    
    
        conda activate povme
    

# POVME 2.0[edit](</mediawiki/index.php?title=POVME&action=edit&section=4> "Edit section: POVME 2.0")]

[POVME 2.0 and a complete tutorial for it can be found here](<http://rocce-vm0.ucsd.edu/data/sw/hosted/POVME/>)
