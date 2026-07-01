# Running standard amber simulations

## Globular MD simulations[edit](</mediawiki/index.php?title=Running_standard_amber_simulations&action=edit&section=1> "Edit section: Globular MD simulations")]

The run configuration files can be found here: /extra/moana/amarolab1/Default_MD_Parameter_Test/Default-Scripts 

Remember to switch $USERDEF to your ligand residue name definition in "S03-Min03-Focused.in" 

(Jeff in Jan 2017) Note that these files have last-modified tags in 2014, however they were the ones that we gave out in BioChemCore 2016. I think they can be assumed to be current. 

## Running jobs[edit](</mediawiki/index.php?title=Running_standard_amber_simulations&action=edit&section=2> "Edit section: Running jobs")]

### Minimization[edit](</mediawiki/index.php?title=Running_standard_amber_simulations&action=edit&section=3> "Edit section: Minimization")]

Minimization should be run on the CPU - see further notes on this here: [AMBER GPU Accuracy ](<http://ambermd.org/gpus/#Accuracy>)
    
    
    export NSLOTS=24
    mpirun -v -np $NSLOTS $AMBERHOME/bin/pmemd.MPI -O -i S01-Min01-Proton.in -o S01-Min01.out -p system.prmtop -c system.inpcrd -r S01-Min01.rst -ref system.inpcrd 
    mpirun -v -np $NSLOTS $AMBERHOME/bin/pmemd.MPI -O -i S02-Min02-Solvent.in -o S02-Min02.out -p system.prmtop -c S01-Min01.rst -r S02-Min02.rst -ref system.inpcrd
    mpirun -v -np $NSLOTS $AMBERHOME/bin/pmemd.MPI -O -i S03-Min03-Focused.in -o S03-Min03.out -p system.prmtop -c S02-Min02.rst -r S03-Min03.rst -ref system.inpcrd
    mpirun -v -np $NSLOTS $AMBERHOME/bin/pmemd.MPI -O -i S04-Min04-Sidechains.in -o S04-Min04.out -p system.prmtop -c S03-Min03.rst -r S04-Min04.rst -ref system.inpcrd
    mpirun -v -np $NSLOTS $AMBERHOME/bin/pmemd.MPI -O -i S05-Min05-All.in -o S05-Min05.out -p system.prmtop -c  S04-Min04.rst -r S05-Min05.rst -ref system.inpcrd
    

### Equilibration[edit](</mediawiki/index.php?title=Running_standard_amber_simulations&action=edit&section=4> "Edit section: Equilibration")]

This below assumes you are running on a GPU cluster using the SLURM scheduler 
    
    
    srun $AMBERHOME/bin/pmemd.cuda -O -i S06-Eql01-Heating.in -o S06-Eql01.out -p system.prmtop -c S05-Min05.rst -ref S05-Min05.rst -r S06-Eql01.rst  -x S06-Eql01.nc 
    srun $AMBERHOME/bin/pmemd.cuda -O -i S07-Eql02-EqlOnlyStage01.in -o S07-Eql02.out -p system.prmtop -c S06-Eql01.rst  -ref S06-Eql01.rst -r S07-Eql02.rst  -x S07-Eql02.nc 
    srun $AMBERHOME/bin/pmemd.cuda -O -i S08-Eql03-EqlOnlyStage02.in -o S08-Eql03.out -p system.prmtop -c S07-Eql02.rst  -ref S07-Eql02.rst -r S08-Eql03.rst  -x S08-Eql03.nc
    

### Production MD Simulation[edit](</mediawiki/index.php?title=Running_standard_amber_simulations&action=edit&section=5> "Edit section: Production MD Simulation")]

This below assumes you are running on a GPU cluster using the SLURM scheduler 
    
    
    srun $AMBERHOME/bin/pmemd.cuda -O -i S09-Pro01-MD_10ns.in -o S09-Pro01.out  -p system.prmtop -c S08-Eql03.rst -ref S08-Eql03.rst -r S09-Pro01.rst  -x S09-Pro01.nc
