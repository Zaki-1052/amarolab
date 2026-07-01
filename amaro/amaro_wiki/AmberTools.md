# AmberTools

# Amber Tools Tutorial[edit](</mediawiki/index.php?title=AmberTools&action=edit&section=1> "Edit section: Amber Tools Tutorial")]

AmberTools is a suite of software that has been designed to prepare and analyze molecular dynamics simulations. 

## Installation[edit](</mediawiki/index.php?title=AmberTools&action=edit&section=2> "Edit section: Installation")]

Go to ambermd.org/AmberTools.php 

Click Download AmberTools 

Under option 1: Getting source code, Enter your information to register 

After file has completed downloading, open the directory where it was downloaded and untar the AmberTools file (NOTE: gfortran, flex, xorg-dev, xserver-xorg-core, xserver-xorg, bison, tcsh and csh must be installed by someone with Sudo privileges) 

  

    
    
    tar -xjf AmberTools18.tar.bz2
    

To .bashrc add the following (or wherever you downloaded amber18) 
    
    
    export AMBERHOME="/home/*username*/Downloads/amber18" 
    
    
    
    cd amber18
    ./configure gnu
    

When it asks you to install miniconda, type y 
    
    
    source amber.sh
    make install
    

## Antechamber[edit](</mediawiki/index.php?title=AmberTools&action=edit&section=3> "Edit section: Antechamber")]

This section describes a quick and easy way to get your small molecule parametrized using Antechamber. 

To start, we will need a CIF (PDB is also possible) file of your ligand. The example I'm going to use is benzamidine, and it's CIF file is here: [BEN.cif](</mediawiki/index.php?title=BEN.cif&action=edit&redlink=1> "BEN.cif \(page does not exist\)"). You can replace "benzamidine" with your own molecule. 

First, see if you have Antechamber: 
    
    
    which antechamber
    

If this returns a path, you should be good. Otherwise, you'll need to install AmberTools or add AMBERHOME to your PATH variable in your .bashrc file. 

This procedure uses a semiempirical method to assign charges, and GAFF (Generalized Amber Forcefield) to assign parameters to the small molecule. 

**Make sure that you check all outputs carefully for errors, warnings, and ATTN checks.**

### Download the CIF file from the PDB[edit](</mediawiki/index.php?title=AmberTools&action=edit&section=4> "Edit section: Download the CIF file from the PDB")]

If your ligand exists in the PDB, then go to the PDB website, scroll down to the section labeled "Small Molecules" (I used PDBID: 3PTB). Find your small molecule, and click "Download CCD file". This file contains optimized geometries and missing hydrogens. 

### Run Antechamber and associated programs[edit](</mediawiki/index.php?title=AmberTools&action=edit&section=5> "Edit section: Run Antechamber and associated programs")]
    
    
    antechamber -i BEN.cif -fi ccif -bk BEN -o benz.mol2 -fo mol2 -c bcc -nc 0
    

I had to look inside the .cif file to see what the "-bk" argument should be: it's the residue name. 

Notice that I'm using the "AM1-BCC" semi-empirical method to get the partial charges of the atoms. Alternatively, you can run GAMESS to find the partial charges (This tutorial coming later...) and just enter those partial charges into the mol2 file (I should write an automatic script to do this...). 

A few things are missing from the mol2 file, so run Parmchk2 to generate a frcmod file of the missing information: 
    
    
    parmchk2 -i benz.mol2 -f mol2 -o benz.frcmod
    

Now we need to make a .lib file for easy future reference in simulations: 
    
    
    tleap
    source leaprc.gaff
    BEN = loadmol2 benz.mol2
    saveoff BEN benz.lib
    quit
    

Now, when you have a system that contains this ligand, just add the following lines early on to the LEAP script (after forcefield definitions but before you load the PDB structure): 
    
    
    source leaprc.gaff
    loadoff /path/to/benz.lib
    loadamberparams /path/to/benz.frcmod
    

### Make a PQR file[edit](</mediawiki/index.php?title=AmberTools&action=edit&section=6> "Edit section: Make a PQR file")]

Now that you've made all the parameter files, reopen tleap and run the following commands: 
    
    
    tleap
    source leaprc.gaff
    loadamberparams benz.frcmod
    BEN = loadmol2 benz.mol2
    saveamberparm BEN benz_vac.parm7 benz_vac.rst7
    quit
    

I believe it's important to make sure that your naming scheme is consistent with the resname (for instance, BEN is the name of the residue. I looked in the CIF file to see what its resname is) 

Now let's run Ambpdb to generate the PQR file. 
    
    
    ambpdb -p benz_vac.parm7 -c benz_vac.rst7 -pqr > benz.pqr
