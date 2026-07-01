# NAMD time steps, integrators and other topics

## NMD latest[edit](</mediawiki/index.php?title=NAMD_time_steps,_integrators_and_other_topics&action=edit&section=1> "Edit section: NMD latest")]

2.9b1 is the latest version- upgrading may be helpful, there is some small improvement in performance. For GPUs the increase in speed is enormous (ABOUT A FACTOR OF FOUR!). Here's the invokation of GPU-enabled single-machine NAMD on a machine with 24 (hyperthreading included) cores using the precompiled binary x86-64_multcore-CUDA build: 
    
    
    charmrun +p24 namd2 +idlepoll run.namd > run.out
    

Here's a sample Ranger script to submit a job with 192 cores in the "long" queue- just put the script in the working folder of the calculation: 
    
    
    
    #!/bin/bash
    #$ -S /bin/bash
    #$ -V
    #$ -cwd
    #$ -N NAMD
    #$ -pe 16way 192
    #$ -q long
    #$ -l h_rt=48:00:00
    
    ldd /share/home/00288/tg455591/NAMD_build.latest/NAMD_2.9b1_Linux-x86_64-ibverbs-Ranger/namd2
    
    export VIADEV_SMP_EAGERSIZE=64
    export VIADEV_SMPI_LENGTH_QUEUE=256
    export VIADEV_ADAPTIVE_RDMA_LIMIT=0
    export VIADEV_RENDEZVOUS_THRESHOLD=50000
    
    /share/home/00288/tg455591/NAMD_build.latest/NAMD_2.9b1_Linux-x86_64-ibverbs-Ranger/charmrun +p192 ++mpiexec ++remote-shell /share/home/00288/tg455591/NAMD_scripts/mpiexec ++runscript tacc_affinity /share/home/00288/tg455591/NAMD_build.latest/NAMD_2.9b1_Linux-x86_64-ibverbs-Ranger/namd2 run.namd >& run.out
    
    

To run with NAMD 2.8, use this script: 
    
    
    
    #$ -S /bin/bash
    #$ -V
    #$ -cwd
    #$ -N NAMD
    #$ -pe 16way 192
    #$ -q long
    #$ -l h_rt=48:00:00
    
    ldd /share/home/00288/tg455591/NAMD_2.8/NAMD_2.8_Linux-x86_64-ibverbs-Ranger/namd2
    
    export VIADEV_SMP_EAGERSIZE=64
    export VIADEV_SMPI_LENGTH_QUEUE=256
    export VIADEV_ADAPTIVE_RDMA_LIMIT=0
    export VIADEV_RENDEZVOUS_THRESHOLD=50000
    
    /share/home/00288/tg455591/NAMD_2.8/NAMD_2.8_Linux-x86_64-ibverbs-Ranger/charmrun +p192 ++mpiexec ++remote-shell /share/home/00288/tg455591/NAMD_scripts/mpiexec ++runscript tacc_affinity /share/home/00288/tg455591/NAMD_2.8/NAMD_2.8_Linux-x86_64-ibverbs-Ranger/namd2 run.namd >& run.out
    
    

### Simulation Parameters[edit](</mediawiki/index.php?title=NAMD_time_steps,_integrators_and_other_topics&action=edit&section=2> "Edit section: Simulation Parameters")]

In this section, the various parameters used in Molecular Dynamics are discussed and implemented with NAMD. One of these factors is the time step. In all-atom Molecular Dynamics, the scale of vibration of hydrogen atoms in water and biomolecules is comparable to a femtosecond (fs). Thus, short time steps must be used in integrating the equations of motion in order to properly treat hydrogen dynamics. This is customarily 1 fs, though 0.5 fs has been used as well. 

To circumvent the problem of treating such short time-scale dynamics within MD, various algorithms have been designed to impose constraints on the hydrogen bond lengths, since these hydrogen motions are not well-treated by Molecular Mechanics (MM) force fields and play little role in conformational dynamics. The use of such an algorithm (e.g., SHAKE and SETTLE, RATTLE) allows for the use of a longer time step. The currently accepted higher bound for the time step in state-of-the-art simulation work is 2 fs. However, using a time step that is twice as large does not necessarily translate to a factor of two speedup in integrating the equations of motion, since algorithms used to constrain bond lengths introduce additional computation and parallelization issues. 

Various factors will influence the overall efficiency of MD simulations. Important ones include the frequency of computing electrostatic and non-bonded interactions, as well as the cutoffs and switching used to truncate these interactions at reasonable distances, so that the computation of these interactions is computationally efficient. As the non-bonded forces are strongly dependent on distance (the inverse sixth and twelfth powers of distance), these forces must be computed most often. 

In order to demonstrate different configurations of these parameters for MD simulation, an example of simulation parameters used with a 2 fs time step is given below (for systems using the CHARMM force field), with shorter non-bonded/electrostatic cutoffs than some of other examples: 

See <http://www.ks.uiuc.edu/Research/namd/2.9/ug/> for a complete description of all the NAMD configuration file parameters. 
    
    
    
    temperature           310.0
    
    # needed for CHARMM force field
    exclude               scaled1-4
    1-4scaling            1.0
    
    cutoff                10.0
    # following may be helpful with lipid sims (?)
    # vdwforceswitching     on
    switching             on
    switchdist            9.0
    pairlistdist          11.0
    
    # larger cutoff
    #cutoff                  14.0
    #switching                 on
    #vdwforceswitching         on
    #switchdist              12.0
    #pairlistdist            16.0
    
    timestep              2.0
    rigidBonds            all
    # it seems you need "nonbondfreq = 1" to avoid constraint errors with 2fs!!!!!!
    nonbondedFreq         1
    fullElectFrequency    4
    stepspercycle         20
    
    useGroupPressure      yes     ;# needed for rigidBonds
    useFlexibleCell       no
    
    
    ## UNCOMMENT EITHER LANGEVIN OR LOWE-ANDERSEN
    
    #langevin             on
    #langevinDamping      5
    #langevinTemp         310.0
    #langevinHydrogen     off
    
    loweAndersen          on
    loweAndersenRate      75.0
    loweAndersenTemp      310.0
    
    
    ## UNCOMMENT EITHER LANGEVIN OR BERENDSEN
    
    # Langevin Piston (alternative to Berendsen)
    #langevinPiston        on
    #langevinPistonTarget  1.01325
    #langevinPistonPeriod  200.0
    #langevinPistonDecay   100.0    
    #langevinPistonTemp    310.0
    
    # Berendsen Pressure
    BerendsenPressure                on
    BerendsenPressureTarget          1.01325
    BerendsenPressureCompressibility 0.0000446
    BerendsenPressureRelaxationTime  100.0
    BerendsenPressureFreq            4
    
    PME                   on
    PMEGridSpacing        1.0
