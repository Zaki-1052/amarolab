from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
prmtop = AmberPrmtopFile('/home/astokely/camca-apos/camcaph.parm7')
inpcrd = AmberInpcrdFile('/home/astokely/camca-apos/camcaph.rst7')
system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer,
        constraints=HBonds)
integrator = LangevinIntegrator(277.8*kelvin, 1/picosecond, 0.002*picoseconds)
barostat = MonteCarloBarostat(1.0*bar, 277.8*kelvin, 25)
system.addForce(barostat)
platform = Platform.getPlatformByName('CUDA')
properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
simulation.context.setPositions(inpcrd.positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
simulation.minimizeEnergy()
simulation.reporters.append(PDBReporter('/home/astokely/camca-apos/apos-output.pdb', 1000))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
        potentialEnergy=True, temperature=True, volume=True))
simulation.step(100000)
state = simulation.context.getState()
print(state.getPeriodicBoxVectors())
