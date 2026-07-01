# Constant volume apo.py

from simtk.openmm.app import *
    from simtk.openmm import *
    from simtk.unit import *
    from sys import stdout
    prmtop = AmberPrmtopFile('/home/astokely/camca-apos/camcaph.parm7')
    inpcrd = AmberInpcrdFile('/home/astokely/camca-apos/camcaph.rst7')
    system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
            constraints=HBonds)
    
    mypdb = PDBFile('camca-apo-last-frame.pdb')
    
    integrator = LangevinIntegrator(277.8*kelvin, 1/picosecond, 0.002*picoseconds)
    
    platform = Platform.getPlatformByName('CUDA')
    properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
    simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
    simulation.context.setPositions(mypdb.positions)
    if inpcrd.boxVectors is not None:
        simulation.context.setPeriodicBoxVectors((7.019540479818371, 0.0, 0.0), (-2.3398466378103624, 6.618086298873436, 0.0), (-2.3398466378103624, -3.309042748940427, 5.731431090488755))
    simulation.minimizeEnergy()
    simulation.reporters.append(PDBReporter('/home/astokely/camca-apos/apos-output_nvt.pdb', 1000))
    simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
            potentialEnergy=True, temperature=True, volume=True))
    simulation.step(10000000)
