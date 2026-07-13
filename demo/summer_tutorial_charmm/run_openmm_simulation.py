# Import all the packages we need for the tutorial
from openmm import *
from openmm.app import *
import openmm.unit as unit
from sys import stdout

############
#PARAMETERS#
############

# Load our .pdb and .psf filenames
pdb_filename = "step3_pbcsetup.pdb" # contains positions of atoms
psf_filename = "step3_pbcsetup.psf" # contains list of atoms and how they are connected

#Temperature for simulation (thermostat will keep it stable at this temp)
temperature = 298.15*unit.kelvin

# Total simulation time = num_steps * time_step
# 0.002 ps * 100000 = 200 ps
num_steps = 100000
time_step = 0.002 * unit.picoseconds

# Box vectors (check step3_pbcsetup.str if not in the pdb)
a = 64 * unit.angstrom
b = 64 * unit.angstrom
c = 64 * unit.angstrom
alpha = 90.0 * unit.degrees
beta  = 90.0 * unit.degrees
gamma = 90.0 * unit.degrees

# Information for DCD reporter
trajectory_filename = "trajectory.dcd"
steps_per_trajectory_update = 1000

# Information for stdout reporter
steps_per_energy_update = 1000

############
#SIMULATION#
############

# Turn these files into OpenMM objects
mypdb = PDBFile(pdb_filename)
mypsf = CharmmPsfFile(psf_filename)

# Update psf with box vectors
mypsf.setBox(a, b, c, alpha, beta, gamma)

# Load the CHARMM parameter filenames
myparams = CharmmParameterSet("par_all36m_prot.prm", "top_all36_prot.rtf", "toppar_water_ions.str")

# Create an OpenMM system
system = mypsf.createSystem(
            myparams, # pass the parameters to the system
            nonbondedMethod=PME, # Use particle mesh Ewald to compute long-range electrostatics
            nonbondedCutoff=1.0*unit.nanometer, # Cutoff past which to use long-range electrostatics (PME)
            constraints=HBonds # Constrain bonds to hydrogen to make more stable
)

# Create integrator
integrator = LangevinIntegrator(temperature, 1/unit.picosecond, time_step) #1/picosecond is the friction coefficient

# Create an OpenMM simulation object, which combines the positions and topology, the system, and the integrator.
simulation = Simulation(mypsf.topology, system, integrator)

# Update the simulation with the positions of all the atoms
simulation.context.setPositions(mypdb.positions)

# Add all our reporters (trajectory and stdout)
simulation.reporters.append(DCDReporter(trajectory_filename, steps_per_trajectory_update))
simulation.reporters.append(StateDataReporter(stdout, steps_per_energy_update, step=True, potentialEnergy=True, temperature=True))

# Minimize energy
simulation.minimizeEnergy(maxIterations=500)

# Set the initial velocities 
simulation.context.setVelocitiesToTemperature(temperature)

# Now we can run it!
simulation.step(num_steps)
