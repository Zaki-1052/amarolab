# Electrostatics of large structures using APBS

## Electrostatics of Large Structures Using APBS[edit](</mediawiki/index.php?title=Electrostatics_of_large_structures_using_APBS&action=edit&section=1> "Edit section: Electrostatics of Large Structures Using APBS")]

[APBS User's Guide](<http://www.poissonboltzmann.org/apbs/user-guide>)

APBS is an Poisson-Boltzmann equation solver package that uses parallel adaptive finite-element methods. All of these features make APBS very attractive as a solver. 

APBS has been built to allow parallel calculations by breaking the regions of space around the structure into partitions, each of which has the electrostatics calculated for that region. Afterward, the user may stitch the individual electrostatic maps (.dx files) together by using the **mergedx** program. 

Although APBS is utilizes parallel calculations, they do not all need to be performed at the same time on a cluster. The parallel runs can be calculated _asynchronously_ on a single core using the "async" option. 

### InputGen[edit](</mediawiki/index.php?title=Electrostatics_of_large_structures_using_APBS&action=edit&section=2> "Edit section: InputGen")]

APBS requires an input file and a PQR structure to run. The PQR structure may be prepared from a PDB file using the program **pdb2pqr**. 

**inputgen** can be found in the **pdb2pqr** package: 
    
    
    /path/to/pdb2pqr/src/inputgen.py

Once the PQR is obtained, the auxiliary program **inputgen** may be used to generate input files for APBS. If given a PQR file named "mystructure.pqr", the usage of **inputgen** at its simplest would appear as below: 
    
    
    python inputgen.py mystructure.pqr

In the example above, all the defaults would be used. Some useful options for **inputgen** are listed below: 

  * \--help  : gives the syntax of inputgen usage, as well as all program options
  * \--potdx  : calculate potential map (.dx file)
  * \--method  : used to control whether APBS job will be manual, parallel, or asynchronous
  * \--space  : define spacing between grid points
  * \--gmemceil : defines the maximum MB allowed for a sequential calculation, will automatically split the structure for parallelization if job will exceed defined memory.



To view more options, run **inputgen** with the "--help" flag. 

### Electrostatics of a Virus[edit](</mediawiki/index.php?title=Electrostatics_of_large_structures_using_APBS&action=edit&section=3> "Edit section: Electrostatics of a Virus")]

Large viral structures will tend to bring out a lot of software bugs/incapabilities. As of the time of this writing (4/9/13), the parallel feature of APBS has a severe bug: a memory leak that appears to blow out of proportion when given large structures. This means that the auxiliary program **inputgen** will not properly partition large structures. However, since we want to get the research underway and don't want to wait until the APBS developers fix the bug, there is a way to calculate for large structures, but it takes a great deal of "MacGyvering" with the software and code. 

Also, **inputgen** will want to use the "smol" option for the "srfm" parameter of the inputfile by default. There is _another_ bug in APBS that causes this option to fail for large structures/dense grids. The way around this bug is to change all "smol" values into "spl2" in the input file. Unfortunately, this requires special radii for the PQR file. Details can be found here: [srfm keywords](<http://www.poissonboltzmann.org/apbs/user-guide/running-apbs/input-files/elec-input-file-section/elec-keywords/srfm>). 

Because of the memory leak, finding the size of the parallel partitions will require some experimentation. I've discovered that for the influenza viral particles, the ideal size to feed **inputgen** is about 7500MB (even though my computer is supposed to be able to handle about 96000, very annoying). So given the large PQR viral structure named "virus.pqr", I can run this command: 
    
    
    python inputgen.py --gmemceil=7500 virus.pqr

If I want to specify the grid spacing to be 1.0Å, I can use this command: 
    
    
    python inputgen.py --space=1.0 --gmemceil=7500 virus.pqr

Once finished, I can look at the new APBS input file, which will be named "virus.in" 

The important things to notice are the variables specified "dime", "pdime", "cglen", and "fglen". For example: 
    
    
    ...
    dime 321 321 353
    pdime 9 9 9
    ...
    cglen 1979.7486 1966.0483 2088.6064
    fglen 1184.5580 1176.4990 1248.5920
    ...

  * The "dime" parameter tells us the number of grid points in each X,Y,Z dimension.
  * The "pdime" parameter specifies how the space has been divided into parallel partitions (In this example, there are 9*9*9 partitions: a total of 729 separate calculations will be run)
  * The "cglen" and "fglen" each define the lengths of the course grid and fine grid respectively in each dimension.



The "--method=async" option of **inputgen** could be used to generate all your input files, however this is inconvenient because you will have to go back and change all the "smol" options to "spl2", etc. Also, I'm not sure why it does this, but an asynchronous job will sometimes write over other jobs' .dx files. (_Very_ annoying. The APBS team obviously has a lot of work to do for the parallel features) 

To deal with all of these problems, I written up a simple Bash script that does a lot of the menial work for you: [virus_async.bash](</mediawiki/index.php/Virus_async.bash> "Virus async.bash")

The script takes a single, required argument (otherwise it will throw an error) equal to the number of partitions, that is, each of the "pdime" numbers multiplied. 

But before I run the script, I have to modify it slightly (annoying, I know, but I haven't taken the time to come up with a better way). You'll need to open up the virus_async.bash file in your text editor and change the four values listed above: "dime", "pdime", "cglen", and "fglen" to be the same as what the input file of your latest run of **inputgen** yielded. 

Once that is done, take a look at the template within the virus_async.bash script, make sure everything looks OK. Then run the script: 
    
    
    bash virus_async.bash ###

In our example, ### would be replaced by 729. The script will create a directory called "apbs_async_all". Enter that directory. 

Inside should be a bunch of input files as well as a file called "run_all.bash". This is a generated script that will run every APBS job sequentially. To start your APBS jobs, type this: 
    
    
    bash run_all.bash

The calculation may take a long time, perhaps days depending on the grid spacing, structure size, etc. Note that you can put this onto a supercomputer such as Gordon by requesting a single node with a single processor for the maximum amount of time. 

Once the calculation is complete, you should have a bunch of input, output, and .dx files in the directory. 

## mergedx[edit](</mediawiki/index.php?title=Electrostatics_of_large_structures_using_APBS&action=edit&section=4> "Edit section: mergedx")]

A bunch of .dx files can be stitched together using the **mergedx** program. **mergedx** can be found in the APBS directory: 
    
    
    /path/to/apbs/share/tools/mesh/mergedx

For instance: 
    
    
    mergedx *.dx

will merge all .dx files in the directory. Use the "mergedx -h" option to see more information. 

Notice that **mergedx2** also exists, but I've had more luck with **mergedx** with our large structures.
