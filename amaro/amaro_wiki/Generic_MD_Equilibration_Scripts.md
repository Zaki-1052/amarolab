# Generic MD Equilibration Scripts

**Note** : Parameters that need to be changed are indicated by " * " 

## Energy Minimization[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=1> "Edit section: Energy Minimization")]

  * Performed at 0 K 



### First EM In Amber[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=2> "Edit section: First EM In Amber")]

  * Only hydrogens move



**system-min_1.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname     dummy
    set outname     *system-min_1
    firsttimestep   0
    
    # input 
    #BinCoordinates         $inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    #ExtendedSystem         $inpname.xsc
    
    amber                   yes
    parmfile                *system.prmtop
    ambercoor               *system.inpcrd
    readexclusions          yes
    
    fixedAtoms              on
    fixedAtomsFile          fxd1.pdb
    fixedAtomsCol           O
    
    rigidbonds              all
    rigidTolerance          0.0005
    
    # force field parameters
    exclude                 scaled1-4
    # the 1-4 scaling value is changed... from 1.0 to 0.83333
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin                  1.0
    
    # integrator params
    timestep                1.0
    nonbondedFreq           2
    #PME                     yes
    #PMEGridSizeX            
    #PMEGridSizeY            
    #PMEGridSizeZ            
    FullElectFrequency      4
    stepspercycle           20
    langevin                off    # don't do langevin dynamics in min.
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           298.15 # bath temperature
    langevinDamping        5      # damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     # don't couple langevin bath to hydrogens
    #temperature            298.15
    
    #PBC
    cellBasisVector1        *X.X     0.0     0.0
    cellBasisVector2         0.0    *X.X     0.0
    cellBasisVector3         0.0     0.0    *X.X
    cellOrigin              *X.X    *X.X    *X.X
    wrapWater               on
    wrapAll                 on
    wrapNearest             on
    xstFile                 $outname.xst
    xstFreq                 500
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500
    dcdfreq                 500
    binaryoutput            yes
    outputEnergies          500
    
    minimization            on
    minimize                5000
    

### First EM In Charmm[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=3> "Edit section: First EM In Charmm")]

  * Only hydrogens move



**system-min_1.namd** : 
    
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname     dummy
    set outname     system-min_1
    firsttimestep   0
    
    # input 
    #BinCoordinates         $inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    #ExtendedSystem         $inpname.xsc
    
    structure             *system.xplor.psf
    coordinates           *system.pdb
    paraTypeCharmm        on
    parameters            *par_lipid.prm
    
    fixedAtoms              on
    fixedAtomsFile          fxd1.pdb
    fixedAtomsCol           O
    
    rigidbonds              all
    rigidTolerance          0.0005
    
    # force field parameters
    exclude                 scaled1-4
    # the 1-4 scaling value is changed... from 1.0 to 0.83333
    1-4scaling              1.000000
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin                  1.0
    
    # integrator params
    timestep                1.0
    nonbondedFreq           2
    #PME                     yes
    #PMEGridSizeX            
    #PMEGridSizeY            
    #PMEGridSizeZ            
    FullElectFrequency      4
    stepspercycle           20
    langevin                off    # don't do langevin dynamics in min.
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           310.00 # bath temperature
    langevinDamping        5      # damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     # don't couple langevin bath to hydrogens
    #temperature            298.15
    
    #PBC
    cellBasisVector1        93.0     0.0     0.0
    cellBasisVector2         0.0    93.0     0.0
    cellBasisVector3         0.0     0.0    93.0
    cellOrigin               0.0     0.0     0.0
    wrapWater               on
    wrapAll                 on
    wrapNearest             on
    xstFile                 $outname.xst
    xstFreq                 500
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500
    dcdfreq                 500
    binaryoutput            yes
    outputEnergies          500
    
    minimization            on
    minimize                5000
    

### Second EM[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=4> "Edit section: Second EM")]

  * Hydrogens, waters and ions move



**system-min_2.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-min_1
    set outname	*system-min_2
    firsttimestep	0
    
    # input 
    BinCoordinates         $inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem         $inpname.xsc
    
    amber			yes
    parmfile		*system.prmtop
    ambercoor		*system.inpcrd
    readexclusions		yes
    
    fixedAtoms		on
    fixedAtomsFile		fxd2.pdb
    fixedAtomsCol		O
    
    rigidbonds		all
    rigidTolerance		0.0005
    
    # force field parameters
    exclude                 scaled1-4
    # the 1-4 scaling value is changed... from 1.0 to 0.83333
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    # integrator params
    timestep                1.0
    nonbondedFreq           2
    #PME                     yes
    #PMEGridSizeX            system size X (multiple of 2 or 3)
    #PMEGridSizeY            system size Y (multiple of 2 or 3)
    #PMEGridSizeZ            system size Z (multiple of 2 or 3)
    FullElectFrequency      4
    stepspercycle           20
    langevin                off    # don't do langevin dynamics in min.
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           298.15 # bath temperature
    langevinDamping        5      # damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     # don't couple langevin bath to hydrogens
    #temperature            298.15
    
    #PBC
    #cellBasisVector1	75.687	 0.0	 0.0
    #cellBasisVector2	 0.0	76.987   0.0
    #cellBasisVector3	 0.0	 0.0	77.791
    #cellOrigin		39.402  40.022  40.456
    wrapWater              	on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 500
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    
    minimization	on
    minimize	5000
    

### Third EM[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=5> "Edit section: Third EM")]

  * Hydrogens, waters, ions & side chains move



**system-min_3.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-min_2
    set outname	*system-min_3
    firsttimestep	0
    
    # input 
    BinCoordinates         $inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem         $inpname.xsc
    
    amber			yes
    parmfile		*system.prmtop
    ambercoor		*system.inpcrd
    readexclusions		yes
    
    fixedAtoms		on
    fixedAtomsFile		fxd3.pdb
    fixedAtomsCol		O
    
    rigidbonds		all
    rigidTolerance		0.0005
    
    # force field parameters
    exclude                 scaled1-4
    # the 1-4 scaling value is changed... from 1.0 to 0.83333
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    # integrator params
    timestep                1.0
    nonbondedFreq           2
    #PME                     yes
    #PMEGridSizeX            X
    #PMEGridSizeY            Y
    #PMEGridSizeZ            Z
    FullElectFrequency      4
    stepspercycle           20
    langevin                off    # don't do langevin dynamics in min.
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           298.15 # bath temperature
    langevinDamping        5      # damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     # don't couple langevin bath to hydrogens
    #temperature            298.15
    
    #PBC
    #cellBasisVector1	75.687	 0.0	 0.0
    #cellBasisVector2	 0.0	76.987   0.0
    #cellBasisVector3	 0.0	 0.0	77.791
    #cellOrigin		39.402  40.022  40.456
    wrapWater              	on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 500
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    
    minimization	on
    minimize	10000
    

### Fourth EM[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=6> "Edit section: Fourth EM")]

  * All atoms move (no fixed atoms)



**system-min_4.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-min_3
    set outname	*system-min_4
    firsttimestep	0
    
    # input 
    BinCoordinates         $inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem         $inpname.xsc
    
    amber			yes
    parmfile		*system.prmtop
    ambercoor		*system.inpcrd
    readexclusions		yes
    
    #fixedAtoms		on
    #fixedAtomsFile		fxd3.pdb
    #fixedAtomsCol		O
    
    rigidbonds		all
    rigidTolerance		0.0005
    
    # force field parameters
    exclude                 scaled1-4
    # the 1-4 scaling value is changed... from 1.0 to 0.83333
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    # integrator params
    timestep                1.0
    nonbondedFreq           2
    #PME                     yes
    #PMEGridSizeX            
    #PMEGridSizeY            
    #PMEGridSizeZ            
    FullElectFrequency      4
    stepspercycle           20
    langevin                off    # don't do langevin dynamics in min.
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           298.15 # bath temperature
    langevinDamping        5      # damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     # don't couple langevin bath to hydrogens
    #temperature            298.15
    
    #PBC
    #cellBasisVector1	75.687	 0.0	 0.0
    #cellBasisVector2	 0.0	76.987   0.0
    #cellBasisVector3	 0.0	 0.0	77.791
    #cellOrigin		39.402  40.022  40.456
    wrapWater              	on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 500
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    
    minimization	on
    minimize	25000
    

## Harmonic Equilibration[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=7> "Edit section: Harmonic Equilibration")]

  * Performed with set temperature and velocity 
  * Harmonic Constraints (HC) - constrains atoms according to spring stiffness



### First HE[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=8> "Edit section: First HE")]

  * HC = 1.0 



**system-hc_eq_1.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-min_4
    set outname	*system-hc_eq_1
    firsttimestep	0
    
    # input 
    amber                   yes
    parmfile                *system.prmtop
    ambercoor               *system.inpcrd
    readexclusions          yes
    BinCoordinates		$inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem          $inpname.xsc
    
    # Harmonic constraint part
    constraints 		on
    consRef 		restrain_backbone_ref.pdb
    consKFile 		restrain_backbone_ref.pdb
    consKCol 		O 
    constraintScaling	1.0
    
    # force field parameters
    exclude                 scaled1-4
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    rigidBonds		all
    rigidTolerance		0.0005
    
    # integrator params
    timestep                1.0
    numsteps                250000 
    nonbondedFreq           2
    PME                     yes
    PMEGridSizeX            *system size X (multiple of 2 or 3)
    PMEGridSizeY            *system size Y (multiple of 2 or 3)
    PMEGridSizeZ            *system size Z (multiple of 2 or 3)
    FullElectFrequency      2
    stepspercycle           20
    langevin                on     	# do langevin dynamics
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           310 	# bath temperature
    langevinDamping        5      	# damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     	# don't couple langevin bath to hydrogens
    temperature            310
    
    # Pressure Control for NPT ensemble
    useFlexibleCell         no
    langevinPiston          on
    langevinPistonTarget    1.01325 #  in bar -> 1 atm
    langevinPistonPeriod    100
    langevinPistonDecay     50
    langevinPistonTemp      310
    
    #PBC
    #cellBasisVector1       78.27    0.0     0.0
    #cellBasisVector2        0.0    78.45    0.0
    #cellBasisVector3        0.0     0.0    76.62
    #cellOrigin             -0.062  0.069 0.009          
    wrapWater               on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 10000
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    

### Second HE[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=9> "Edit section: Second HE")]

  * HC = 0.75



**system-hc_eq_2.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-hc_eq_1
    set outname	*system-hc_eq_2
    firsttimestep	0
    
    # input 
    amber                   yes
    parmfile                *system.prmtop
    ambercoor               *system.inpcrd
    readexclusions          yes
    BinCoordinates		$inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem          $inpname.xsc
    
    # Harmonic constraint part
    constraints 		on
    consRef 		restrain_backbone_ref.pdb
    consKFile 		restrain_backbone_ref.pdb
    consKCol 		O 
    constraintScaling	0.75
    
    # force field parameters
    exclude                 scaled1-4
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    rigidBonds		all
    rigidTolerance		0.0005
    
    # integrator params
    timestep                1.0
    numsteps                250000 
    nonbondedFreq           2
    PME                     yes
    PMEGridSizeX            *
    PMEGridSizeY            *
    PMEGridSizeZ            *
    FullElectFrequency      2
    stepspercycle           20
    langevin                on     	# do langevin dynamics
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           310 	# bath temperature
    langevinDamping        5      	# damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     	# don't couple langevin bath to hydrogens
    temperature            310
    
    # Pressure Control for NPT ensemble
    useFlexibleCell         no
    langevinPiston          on
    langevinPistonTarget    1.01325 #  in bar -> 1 atm
    langevinPistonPeriod    100
    langevinPistonDecay     50
    langevinPistonTemp      310
    
    #PBC
    #cellBasisVector1       78.27    0.0     0.0
    #cellBasisVector2        0.0    78.45    0.0
    #cellBasisVector3        0.0     0.0    76.62
    #cellOrigin             -0.062  0.069 0.009          
    wrapWater               on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 10000
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    

### Third HE[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=10> "Edit section: Third HE")]

  * HC = 0.50



**system-hc_eq_3.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-hc_eq_2
    set outname	*system-hc_eq_3
    firsttimestep	0
    
    # input 
    amber                   yes
    parmfile                *system.prmtop
    ambercoor               *system.inpcrd
    readexclusions          yes
    BinCoordinates		$inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem          $inpname.xsc
    
    # Harmonic constraint part
    constraints 		on
    consRef 		restrain_backbone_ref.pdb
    consKFile 		restrain_backbone_ref.pdb
    consKCol 		O 
    constraintScaling	0.50
    
    # force field parameters
    exclude                 scaled1-4
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    rigidBonds		all
    rigidTolerance		0.0005
    
    # integrator params
    timestep                1.0
    numsteps                250000 
    nonbondedFreq           2
    PME                     yes
    PMEGridSizeX            *
    PMEGridSizeY            *
    PMEGridSizeZ            *
    FullElectFrequency      2
    stepspercycle           20
    langevin                on     	# do langevin dynamics
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           310 	# bath temperature
    langevinDamping        5      	# damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     	# don't couple langevin bath to hydrogens
    temperature            310
    
    # Pressure Control for NPT ensemble
    useFlexibleCell         no
    langevinPiston          on
    langevinPistonTarget    1.01325 #  in bar -> 1 atm
    langevinPistonPeriod    100
    langevinPistonDecay     50
    langevinPistonTemp      310
    
    #PBC
    #cellBasisVector1       78.27    0.0     0.0
    #cellBasisVector2        0.0    78.45    0.0
    #cellBasisVector3        0.0     0.0    76.62
    #cellOrigin             -0.062  0.069 0.009          
    wrapWater               on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 10000
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    

### Fourth HE[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=11> "Edit section: Fourth HE")]

  * HC = 0.25



**system-hc_eq_4.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-hc_eq_3
    set outname	*system-hc_eq_4
    firsttimestep	0
    
    # input 
    amber                   yes
    parmfile                *system.prmtop
    ambercoor               *system.inpcrd
    readexclusions          yes
    BinCoordinates		$inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem          $inpname.xsc
    
    # Harmonic constraint part
    constraints 		on
    consRef 		restrain_backbone_ref.pdb
    consKFile 		restrain_backbone_ref.pdb
    consKCol 		O 
    constraintScaling	0.25
    
    # force field parameters
    exclude                 scaled1-4
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    rigidBonds		all
    rigidTolerance		0.0005
    
    # integrator params
    timestep                1.0
    numsteps                250000 
    nonbondedFreq           2
    PME                     yes
    PMEGridSizeX            *
    PMEGridSizeY            *
    PMEGridSizeZ            *
    FullElectFrequency      2
    stepspercycle           20
    langevin                on     	# do langevin dynamics
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           310 	# bath temperature
    langevinDamping        5      	# damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     	# don't couple langevin bath to hydrogens
    temperature            310
    
    # Pressure Control for NPT ensemble
    useFlexibleCell         no
    langevinPiston          on
    langevinPistonTarget    1.01325 #  in bar -> 1 atm
    langevinPistonPeriod    100
    langevinPistonDecay     50
    langevinPistonTemp      310
    
    #PBC
    #cellBasisVector1       78.27    0.0     0.0
    #cellBasisVector2        0.0    78.45    0.0
    #cellBasisVector3        0.0     0.0    76.62
    #cellOrigin             -0.062  0.069 0.009          
    wrapWater               on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 10000
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
    

## Free Dynamics[edit](</mediawiki/index.php?title=Generic_MD_Equilibration_Scripts&action=edit&section=12> "Edit section: Free Dynamics")]

  * No constraints
  * Uses output of free equilibration



**system-eq.namd** : 
    
    
    #**********************************************************
    #  Name
    #  Date
    #  *items to be changed are marked with a star*
    #**********************************************************
    
    set inpname	*system-hc_eq_4
    set outname	*system-eq
    firsttimestep	0
    
    # input 
    amber                   yes
    parmfile                *system.prmtop
    ambercoor               *system.inpcrd
    readexclusions          yes
    BinCoordinates		$inpname.restart.coor
    #BinVelocities          $inpname.restart.vel
    ExtendedSystem          $inpname.restart.xsc
    
    # force field parameters
    exclude                 scaled1-4
    1-4scaling              0.833333
    cutoff                  14
    switching               On
    switchdist              12
    pairlistdist            16
    margin			1.0
    
    rigidBonds		all
    rigidTolerance		0.0005
    
    # integrator params
    timestep                2.0
    numsteps                10000000 
    nonbondedFreq           2
    PME                     yes
    PMEGridSizeX            *
    PMEGridSizeY            *
    PMEGridSizeZ            *
    FullElectFrequency      2
    stepspercycle           20
    langevin                on     # do langevin dynamics
    #langevinFile            tempfile.pdb 
    #langevinCol             O
    langevinTemp           310    # bath temperature
    langevinDamping        5      # damping coefficient (gamma) of 5/ps
    langevinHydrogen       no     # don't couple langevin bath to hydrogens
    temperature            310
    
    # Pressure Control for NPT ensemble
    useFlexibleCell         no
    langevinPiston          on
    langevinPistonTarget    1.01325 #  in bar -> 1 atm
    langevinPistonPeriod    100
    langevinPistonDecay     50
    langevinPistonTemp      310
    
    #PBC
    #cellBasisVector1       78.27    0.0     0.0
    #cellBasisVector2        0.0    78.45    0.0
    #cellBasisVector3        0.0     0.0    76.62
    #cellOrigin             -0.062  0.069 0.009          
    wrapWater               on
    wrapAll			on
    wrapNearest		on
    xstFile                 $outname.xst  
    xstFreq                 10000
    
    # output
    outputname              $outname
    dcdfile                 $outname.dcd
    restartname             $outname.restart
    restartfreq             500 
    dcdfreq                 500
    binaryoutput            yes 
    outputEnergies          500
