# Brownian Dynamics with SDA 5

## Converting your PDB to PQR using PDB2PQR[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=1> "Edit section: Converting your PDB to PQR using PDB2PQR")]

The first step is to turn your two protein PDB files into PQR files. PQR files are identical to PDB files with two exceptions - the occupancy column and onwards from the PDB have been replaced by charge (Q) and atomic radius (R). 

To carry out this conversion, we use PDB2PQR. Either the [command-line version](<http://www.poissonboltzmann.org/pdb2pqr/>) or the [online server](<http://kryptonite.nbcr.net/pdb2pqr/>) can be used. In this tutorial, we use the command-line version. 

The PDB2PQR syntax is 
    
    
    pdb2pqr.py [options] --ff=<forcefield> <path> <output-path>
    

  


### At pH of 7.0[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=2> "Edit section: At pH of 7.0")]

The command (using the AMBER force field with the 1NN2 crystal structure pdb) would be: 
    
    
    pdb2pqr.py --verbose --ff=AMBER 1NN2.pdb 1nn2.pqr
    

This generates the files 1nn2.pqr and 1nn2-typemap.pqr. The 1nn2-typemap.html is a page containing the names of all the atoms, but is not necessary for BD simulations. 

### Using PROPKA for non-7.0 pH's[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=3> "Edit section: Using PROPKA for non-7.0 pH's")]

PDB2PQR also is able to use PROPKA to handle protonation states at various pH's. This is done by using the --with-ph option. 

For example, to have PDB2PQR generate the atom charges at physiological pH (7.2), use: 
    
    
    pdb2pqr.py --verbose --ff=AMBER --with-ph=7.2 1NN2.pdb 1nn2.pqr
    

This generates the files 1nn2.pqr, 1nn2-typemap.html, and 1nn2.propka. The 1nn2-typemap.html is a list of atoms not necessary for the simulations. The 1nn2.propka file is a list of pKa values for charged sidechains, which can be used to correct any mistakes PDB2PQR may have made in creating the PQR. 

### Adding in missing species[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=4> "Edit section: Adding in missing species")]

PDB2PQR might be unable to add in atoms/ions whose names it does not recognize. In that case, the pqr file should be manually edited to add in the missing species. 

### Checking the PQR file[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=5> "Edit section: Checking the PQR file")]

It is important to check the PQR file generated, because PDB2PQR ignores factors such as a crystal structure's failure to represent the flexibility of a protein. As a result, PDB2PQR might place or remove spurious hydrogen bonds, leading to incorrect overall charge. 

When re-adding (or re-removing) hydrogen atoms that were incorrectly removed (or added), it is important to remember to replace PDB2PQR's assigned atomic charges with the appropriate charges from the force field being used. 

### Small molecule issues[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=6> "Edit section: Small molecule issues")]

PDB2PQR was written primarily for proteins, and may have difficulties with small molecules. In that case, the charges will need to be calculated using Gaussian, and the atomic radii taken from the force field parameters, and the PQR file will have to be generated manually. 

### Calculating hydrodynamic properties using Hydropro[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=7> "Edit section: Calculating hydrodynamic properties using Hydropro")]

Now that we have a PQR, the next step is to calculate some hydrodynamic data of the proteins. This data will be needed later in the SDA input files. 

To calculate the hydrodynamic data, we use [Hydropro](<http://leonardo.inf.um.es/macromol/programs/hydropro/hydropro.htm>). 

Hydropro works by using a Shell Method. Since viscosity is caused by friction between the surface of the protein and the solvent, the only hydrodynamically relevant part of the protein is its surface. Thus, hydropro generates a "shell" made up of a number of minibeads within the surface of the protein. Hydropro then decreases the minibead radii and increases the number of minibeads, until the surface area of the shells converges to the actual surface area of the protein (in the radius->infinity limit). 

Hydropro requires an input file, _hydropro.dat_. Here is an example: 
    
    
    3.1-h1n1                      !Name of molecule
    h1n1                          !Name for output file 
    cal-bii-h1n1_ecm.pdb          !Strucutural (PBD) file       
    3.1,                          !AER, radius of the atomic elements
    6,              !NSIG
    1.0,            !Minimum radius of beads in the shell (SIGMIN)	
    2.0,            !Maximum radius of beads in the shell (SIGMAX)	
    293.,           !T (temperature, K)
    0.01,           !ETA (Viscosity of the solvent in poises)
    14320.,         !RM (Molecular weigth)
    0.702,	    !Partial specific volume, cm3/g
    1.0,            !Solvent density, g/cm3
    21              !Number of values of H
    2.e+7,          !HMAX
    30,             !Number of intervals for the distance distribution
    -1.,            !RMAX
    1000,           !Number of trials for MC calculation of covolume
    1               !IDIF=1 (yes) for full diffusion tensors
    *                             !End of file
    

**NSIG** corresponds to the number of minibead radii that hydropro should use in generating a shell of the protein. A value of -1 tells hydropro to automatically determine the number of radii to try. Normally, this should be sufficient. 

However, in the event that hydropro is unable to automatically determine a range of minibead radii to try, something that seems to occur for small molecules and ligands, NSIG can be manually set. In that case, NSIG must be a positive number greater than 2. If NSIG is set, then the next two lines must be the minimum and maximum values for the minibead radii to try. For example, 
    
    
    6,              !NSIG
    1.0,            !Minimum radius of beads in the shell (SIGMIN)	
    2.0,            !Maximum radius of beads in the shell (SIGMAX)
    

If the surface area of the shells does not converge, hydropro will note this and abort. 

**RM** is the protein molecular weight. If set to -1, hydropro will calculate it based on data in the PDB or PQR file. 

**Partial specific volume** is the protein's partial specific volume. If set to -1, hydropro will calculate it based on the PDB or PQR file. 

The lines after the **solvent density** are flags for non-hydrodynamic calculations that are not needed for our purposes. 

A more in-depth explanation of the hydropro input file can be found [here](<http://leonardo.fcu.um.es/macromol/programs/hydropro/hydropro7c.pdf>). 

The Hydropro executable is: 
    
    
     hydropro7c2lnx.exe
    

The hydrodynamic data will be found in the .res file. From the example hydropro.dat file above, it would be in cal-bii-h1n1-tetra.res. 

**WARNING:** The starting column of the comments in the example input file had better NOT be changed. Or the program is likely to not be able to recognize the input file. 

## Creating an electrostatic potential grid in APBS[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=8> "Edit section: Creating an electrostatic potential grid in APBS")]

The electrostatic potential grids are a fundamental part of Brownian Dynamics simulations. In this tutorial we use [APBS v. 0.5.0](<http://www.poissonboltzmann.org/apbs/>) to do this. 

APBS also requires an input file. It contains specifications for grid dimensions - coarse and fine, protein and solvent dielectric constants, etc. 

Here is an example, _cal-bii-h1n1_ecm.in_ , with comments: 
    
    
    read
        mol pqr cal-bii-h1n1_ecm.pqr
    end
    
    # CALCULATION IN SOLVENT solvent dielectric constant = 78.54
    elec name acc
        mg-auto
        dime 160 160 160
    
        cglen 191 191 191
        fglen 160 160 160
    
        cgcent mol 1
        fgcent mol 1
    
        mol 1                              # Which molecule (1, 2, ...)
        lpbe                               # lpbe/npbe = linear/nonlinear PBE
        bcfl sdh                           # Boundary condition flag
                                           # 1 => Single DH sphere
        ion 1 0.15 1.36375                 # 0.1, Counterion declaration: 0.15, 2.0
        ion -1 0.15 2.27                   # ion <charge> <conc (M)> <radius>
    
        pdie 4.0000                        # Solute dielectric 4.0
        sdie 78.5400                       # Solvent dielectric 78
        srfm smol                          # Surface calculation method
                                           # 0 => Mol surface for epsilon;
        chgm spl2                          # charge is mapped onto nearest-neighbor
                                           # grid points
        sdens 10.00
        srad 1.40                          # Solvent radius
        swin 0.30                          # Surface cubic spline window
        temp 310                           # Temperature
        calcenergy total                   # Energy I/O (to stdout)
                                           # 1 => write out total energy
        calcforce no                       # Atomic forces I/O (to stdout)
        write pot uhbd cal-bii-h1n1_ecm
    end
    quit
    

More information about APBS is available at the 

[APBS Documentation](<http://apbs.wustl.edu/MediaWiki/index.php/APBS_user_guide>). 

The syntax for using APBS is: 
    
    
    APBS_EXECUTABLE INPUT_FILE
    

That is, in this example: 
    
    
    apbs-0.5.0 cal-bii-h1n1_ecm.in
    

The grid generated is the .grd file. This grid file is in the ASCII APBS format. However, SDA requires the binary UHBD grid format. Fortunately, one of SDA 5's included auxiliary programs, **apbs2uhbd** is for converting the ASCII APBS format to the required binary UHBD format. 

The syntax for this is: 
    
    
    apbs2uhbd ASCII_GRID BINARY_GRID
    

In this example, it would be: 
    
    
    apbs2uhbd cal-bii-h1n1_ecm.grd cal-bii-h1n1_ecm.grd
    

We now have an electrostatic potential grid for the protein. 

## Creating of a regularized effective charge electrostatic potential grid[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=9> "Edit section: Creating of a regularized effective charge electrostatic potential grid")]

Now we have a binary-format charge grid. However, SDA does not use this grid directly. Instead, SDA uses the Effective Charge Method (ECM), which considerably simplifies calculations, thus decreasing the computational time, but at the cost of some loss in accuracy. ECM was developed to avoid having to deal with boundary-value problems by setting the dielectric constant of the protein to that of the solvent, and then creating a set of effective charges that, at long range, has the same potential as the actual charges. 

This process is detailed below. 

### Creating the test charge file with ecm_mksites[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=10> "Edit section: Creating the test charge file with ecm mksites")]

The program ecm_mksites (included in the ecm directory of the SDA distribution) takes the (usual) charged species from the PQR and puts them in a file, along with their usual charges – -1 for ASP/GLU, +1 for LYS, etc. 

However, ecm_mksites is does not know where the N- and C-terminii are in the protein. Thus, this needs to be manually input into the PQR file. Any N-terminus atom should have its amino acid name changed to **NTRM** and any C-terminus atoms should have their amino acid names changed to **CTRM**. 

The syntax for ecm_mksites is: 
    
    
    ecm_mksites <PQR_FILE> TEST_CHARGE_FILE.tcha
    

So, in this example, 
    
    
    ecm_mksites <cal-bii-h1n1.pqr> cal-bii-h1n1.tcha
    

this will generate the tcha test charge file. ecm_mksites might miss ions or other charged species, so it is important to check to make sure all of the charged species have been placed in the tcha file. 

### Creating an effective charge file using ecm_expand[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=11> "Edit section: Creating an effective charge file using ecm expand")]

#### Using ecm_expand[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=12> "Edit section: Using ecm expand")]

Now the value of the effective charges in the tcha file must be determined. This can be done using ecm_expand. 

SDA 5 includes 4 ecm_expand programs: ecm_expand, ecm_expand150, ecm2_expand, and ecm2_expand150. ecm_expand, ecm_expand150, or any such variant thereof is what we need to run to generate the effective charges to be used in the protein. ecm2_expand, ecm2_expand150, and any variant thereof are designed for setting up the effective charges in a spherical potential, and so are not necessary for our purposes here. 

ecm_expand requires an input file, a commented example one of which, _cal-bii-h1n1_ecm.in_ , is shown below: 
    
    
    ------------------ pdb file name
    ../cal-1nn2-tetra.pqr
    ------------------ file with test charges for a molecule
    cal-1nn2-tetra.tcha
    ------------------ grid file name and its form (0-binary, 1 -asci) UHBD format
    ../apbs/cal-1nn2-tetra-bin.grd
    0
    ------------------ probe, skin: expansion happens in [probe; probe+skin] interval
    4.0, 3.0
    ------------------ ionic strength, solvent dielectric
    150., 78.54
    ------------------ file to write effective charges
    cal-1nn2-tetra.echa
    ------------------ nothing else
    

The syntax for ecm_expand is 
    
    
    ecm_expand < ECM_EXPAND_INPUT_FILE 
    

ecm_expand should have created an echa effective charge file. However an examination of this file will show that the total amount of charge is a ridiculously large number (the total effective charge for the protein from this tutorial, 1nn2, was 122.966). 

#### Limitations of ecm_expand[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=13> "Edit section: Limitations of ecm expand")]

The stuff about array sizes here. 

### Regularizing the effective charges[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=14> "Edit section: Regularizing the effective charges")]

What now needs to be done is regularization of the effective charges. This process involves fitting the potential to the distribution of effective charges, in a way that minimizes the error and maximizes the similarity of the effective potential to the actual potential. 

First, the program **ecm_regularize** should be used to generate the regularization information. The syntax is 
    
    
    ecm_regularize > FILE_TO_STORE_REGULARIZATION_DATA
    

For example, 
    
    
    ecm_regularize > ecm_regularize.out
    

The file with regularization data contains various regularization levels, each of which has a specific net charge, RM1D, charge RMSD, and other information. 

The regularization level that should work best is the one whose absolute value of RM1D is the closest to but below **1.0**. 

The program **ecm_mkreglev** can find the necessary regularization level, with the syntax 
    
    
    ecm_mkreglev RM1D_VALUE < FILE_TO_STORE_REGULARIZATION_DATA > FILE_TO_STORE_PROPER_REGULARIZATION_LEVEL
    

In this example, the command would be 
    
    
    ecm_mkreglev 1.0 < ecm_regularize.out > reg_lev
    

And the proper regularization level would be stored in the file **reg_lev**. 

To create the requisite regularized effective charge files, we use **ecm_mkecharges**. 

The syntax for ecm_mkecharges is: 
    
    
    ecm_mkecharges < FILE_TO_STORE_PROPER_REGULARIZATION_LEVEL
    

In this example, it would be: 
    
    
    ecm_mkecharges < reg_lev
    

This will lead to the creation of echa_E and echa_R files. The echa_R file contains the regularized charges, and the echa_E file contains the regularized charges divided by the solvent dielectric constant. The **echa_R** file is the one used by SDA. We have now created regularized effective charges for the protein. 

## Creating desolvation grids[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=15> "Edit section: Creating desolvation grids")]

Desolvation grids are used to handle solvent effects caused by implicit solvent instead of explicit solvent and hydrophobic effects. 

### Electronic Desolvation[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=16> "Edit section: Electronic Desolvation")]

#### Using mk_ed_grd[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=17> "Edit section: Using mk ed grd")]

To make the electronic desolvation grid, we use the program **mk_ed_grd**. This generates a grid that takes into account electronic desolvation. 

The program requires an input file, a commented example of which, **cal-bii-h1n1-tetra_ds.in** , is here below: 
    
    
    #------------------------------ h,ndimx,ndimy,ndimz
    1, 161,161,161
    #------------------------------ iostr,epssol,rion
    150.  78.54  2.27
    #------------------------------ pfile
    ../cal-bii-h1n1-tetra.pqr
    #------------------------------ efile, iform, the name of the output file
    cal-bii-h1n1-tetra_ds.grd
    0
    

The syntax for mk_ed_grd is 
    
    
    mk_ed_grd < INPUT_FILE
    
    

So in this example, 
    
    
    mk_ed_grd < cal-bii-h1n1-tetra_ds.in
    

The resultant grid is already in binary format. 

#### Limitations on mk_ed_grd[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=18> "Edit section: Limitations on mk ed grd")]

Array size info goes here. 

### Hydrophobic Desolvation[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=19> "Edit section: Hydrophobic Desolvation")]

Goes here. 

#### Using mk_hd_grd[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=20> "Edit section: Using mk hd grd")]

To make the hydrophobic desolvation grid, we use the program **mk_hd_grd**. This generates a grid that takes into account hydrophobic interactions. 

The program requires an input file, a commented example of which, **cal-bii-h1n1-tetra_hd.in** , is here below: 
    
    
    #------------------------------ h,ndimx,ndimy,ndimz
    1, 161,161,161
    #------------------------------ iostr,epssol,rion
    150.  78.54  2.27
    #------------------------------ pfile
    ../cal-bii-h1n1-tetra.pqr
    #------------------------------ efile, iform, the name of the output file
    cal-bii-h1n1-tetra_hd.grd
    0
    

The syntax for mk_hd_grd is 
    
    
    mk_hd_grd < INPUT_FILE 
    

So in this example, 
    
    
    mk_hd_grd < cal-bii-h1n1-tetra_hd.in
    

The resultant grid is already in binary format. 

#### Limitations on mk_hd_grd[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=21> "Edit section: Limitations on mk hd grd")]

Array size stuff goes here. 

## Checking your setup[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=22> "Edit section: Checking your setup")]

Checking instructions here 

## Preparing files for running[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=23> "Edit section: Preparing files for running")]

sda.in/submit.job file info here 

## Run simulation[edit](</mediawiki/index.php?title=Brownian_Dynamics_with_SDA_5&action=edit&section=24> "Edit section: Run simulation")]

Run info here
