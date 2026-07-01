# Restart constant volume apo.py

from simtk.openmm.app import *
    from simtk.openmm import *
    from simtk.unit import *
    from sys import stdout
    prmtop = AmberPrmtopFile('/home/mrogers/dualapo/1ZNJ_solv1.prmtop')
    inpcrd = AmberInpcrdFile('/home/mrogers/dualapo/1ZNJ_solv1.inpcrd')
    system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
            constraints=HBonds)
    
    mypdb = PDBFile('apo_npt1.pdb')
    
    integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
    
    platform = Platform.getPlatformByName('CUDA')
    properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
    simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
    #simulation.context.setPositions(mypdb.positions)
    #if inpcrd.boxVectors is not None:
        #simulation.context.setPeriodicBoxVectors((6.788333212118502, 0.0, 0.0), (-2.26277755479557, 6.400101994207949, 0.0), (-2.26277755479557, -3.2000506097990997, 5.542651137406062))
    #simulation.minimizeEnergy()
    simulation.loadState('restart_long_apo.state')''
    

**Make sure to change name of the output file so that you don't override the information from the first simulation**
    
    
    simulation.reporters.append(PDBReporter('/home/mrogers/dualapo/apo_nvt_long2.pdb', 1000000))
    simulation.reporters.append(StateDataReporter(stdout, 10000, step=True,
            potentialEnergy=True, temperature=True, volume=True))
    

**Make sure to change current_step to the last step completed (can be seen in VMD) so that simulation can start where it left off**
    
    
    total_num_steps = 500000000
    current_step = 243000000
    
    print "Simulation objectcreated. Now starting simulation timesteps."
    
    while current_step < total_num_steps:
      try:
        print "running 10000 steps"
        simulation.step(10000)
        simulation.saveState('restart_long_apo.state')
        current_step = current_step + 10000
      except ValueError:
        print "Alert! NaN error detected. Restarting from saved state."
        simulation.loadState('restart_long_apo.state')
