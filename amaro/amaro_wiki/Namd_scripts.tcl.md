# Namd scripts.tcl

`
    
    
    
    ###########################################################################
    #                       Initial job parameters                            # 
    ###########################################################################
    
    set old [format eq%02d [expr $jobindex - 1]]
    
    if { $jobindex == 1 } {
            set old equil2
    }
    
    if { $jobindex > 1 } {
      set fd [open $old.restart.xsc r]
      gets $fd
      gets $fd
      firstTimestep [lindex [gets $fd] 0]
    }
    
    ###########################################################################
    #                       Restart from last run                             # 
    ###########################################################################
    
    # load recentered coordinates
    bincoordinates $old.coor
    binvelocities  $old.vel
    extendedSystem $old.xsc
    
    ###########################################################################
    #                       Force field parameters                            #
    ###########################################################################
    
    amber on
    parmfile  1XDN_TIP4PEW.prmtop
    ambercoor 1XDN_TIP4PEW.incrd
    
    
    ###########################################################################
    #                  Non-bonded force field parameters                      #
    ###########################################################################
    
    switching    on
    switchDist   9
    cutoff       10
    pairListDist 11
    LJcorrection on
    
    readexclusions yes
    exclude scaled1-4
    scnb 2.0
    1-4scaling   0.8333333
    
    ###########################################################################
    #                           Electrostatics                                #
    ###########################################################################
    
    dielectric 1.0
    
    Pme on
    PMETolerance 1.0e-6
    PMEInterpOrder 4
    pmeGridSpacing 1.0
    
    ###########################################################################
    #                            WATER                               	  # 
    ###########################################################################
    
    watermodel tip4
    
    ###########################################################################
    #                       Constraints                                       #
    ###########################################################################
    
    rigidBonds all
    rigidTolerance 1.0e-8
    rigidIterations 100
    useSettle on
    
    ###########################################################################
    #                       Periodic Boundary System                          # 
    ###########################################################################
    
    wrapWater     on
    wrapAll       off
    
    ###########################################################################
    #                            Temperature                                  #
    ###########################################################################
    
    # Use langevin thermostat
    langevin          on
    langevinDamping   2
    langevinHydrogen  no
    langevinTemp      310
    
    ###########################################################################
    #                       Pressure parameters                               #
    ###########################################################################
    
    useGroupPressure        on
    langevinPiston          on
    langevinPistonTarget    1.01325
    langevinPistonPeriod    100
    langevinPistonDecay     50
    langevinPistonTemp      310
    
    
    ###########################################################################
    #                       Simulation parameters                             #
    ###########################################################################
    
    timestep        2.0
    
    stepspercycle   20
    
    nonBondedFreq 2
    fullElectFrequency 4
    
    ###########################################################################
    #                       Energies and output                               #
    ###########################################################################
    
    outputname     [format eq%02d $jobindex]
    outputEnergies 5000
    outputTiming   25000
    dcdFreq        5000
    restartFreq    25000
    
    ###########################################################################
    #                       Run simulation                                    #
    ###########################################################################
    
    ###########################################################################
    
    

`
