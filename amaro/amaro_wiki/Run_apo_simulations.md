# Run apo simulations

Copy the constant pressure python script from the scripts section of the Wiki into the directory with your prmtop and inpcrd files for the apo simulation. An example of the script is below. Change the integrator and barostat to the temperature of your system. Note, the name of the files in the prmtop and inpcrd are just examples, you should type your name and the location of where your files reside. Name your output file in the simulation.reporters.append line, note this will be used in future simulations. 
    
    
    from simtk.openmm.app import *
    from simtk.openmm import *
    from simtk.unit import *
    from sys import stdout
    prmtop = AmberPrmtopFile('/home/yourName/locationOfFiles/name.prmtop')
    inpcrd = AmberInpcrdFile('/home/yourName/locationOfFiles/name.inpcrd')
    system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
            constraints=HBonds)
    integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
    barostat = MonteCarloBarostat(1.0*bar, 300*kelvin, 25)
    system.addForce(barostat)
    platform = Platform.getPlatformByName('CUDA')
    properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
    simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
    simulation.context.setPositions(inpcrd.positions)
    if inpcrd.boxVectors is not None:
        simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
    simulation.minimizeEnergy()
    simulation.reporters.append(PDBReporter('/home/yourname/locationOfFiles/npt.pdb', 1000))
    simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
            potentialEnergy=True, temperature=True, volume=True))
    simulation.step(10000)
    state = simulation.context.getState()
    print(state.getPeriodicBoxVectors())
    

When you are done editing the file to fit your simulation and you are ready to run your apo simulation, make sure that you are in the correct directory, and type the code seen below, the name after python being what you named your constant volume input file. 
    
    
    python constantpressureapo.py
    

After a minute, your simulation should begin running, and every few seconds a new line should appear containing numbers. If your constant pressure simulation is successfully completed, it should show box vectors in the terminal at the end of running, as well as produce the output pdb file that you named in the script. 

  
After that, copy the constant volume python script from the scripts section of the Wiki. Similar to the constant pressure simulation, you should change the integrator to the temperature of your system, and change the prmtop and inpcrd to your path. You should change the mypdb to the name you chose from the constant pressure script in the simulation.reporters.append line. In the simulation.context.setPeriodicBoxVectors line, you should copy and paste the box vector lines from the output in the constant pressure simulation. 
    
    
    from simtk.openmm.app import *
    from simtk.openmm import *
    from simtk.unit import *
    from sys import stdout
    prmtop = AmberPrmtopFile('/home/home/yourName/locationOfFiles/name.prmtop')
    inpcrd = AmberInpcrdFile('/home/home/yourName/locationOfFiles/name.inpcrd')
    system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
            constraints=HBonds)
    
    mypdb = PDBFile('apo_npt1.pdb')
    
    integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
    
    platform = Platform.getPlatformByName('CUDA')
    properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
    simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
    simulation.context.setPositions(mypdb.positions)
    if inpcrd.boxVectors is not None:
        simulation.context.setPeriodicBoxVectors((6.788333212118502, 0.0, 0.0), (-2.26277755479557, 6.400101994207949, 0.0), (-2.26277755479557, -3.2000506097990997, 5.542651137406062))
    simulation.minimizeEnergy()
    simulation.reporters.append(PDBReporter('/home/yourName/locationOfFiles/name.pdb', 1000))
    simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
            potentialEnergy=True, temperature=True, volume=True))
    simulation.step(1000000)
    

When you are ready to run your constant volume simulation, make sure that you are in the correct directory and type the code seen below, the name after python being what you named your constant volume input file. 
    
    
    python constantvolumeapo.py
