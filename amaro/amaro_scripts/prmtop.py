'''
This program runs a pathfinding simulation of alanine dipeptide in a vacuum
Our goal is to find the lowest-energy conformation of alanine dipeptide
within a reasonable timeframe

Tasks:
1) load all alanine dipeptide starting structure and topology and ff information
  - will need to code a prmtop parser
  - objects for atoms, bonds, angles, dihedrals, etc. (look at c-code for it)

2) Discretize conformational space
  - Construct a vector to describe the entire conformational space of the dipeptide
    by bond lengths, angles, dihedrals. Both periodic and continual elements in this space
  - the protein COM will be constrained to one location
  - need a way to convert back and forth from the conformation vector to a cartesian
    vector the describes the locations of every atom.
  - Each conformation in the vector must be describable by a unique index. Must be able to construct
    the index from the conformation vector
  - Since we want to sample the conformation vector more thoughfully that just moving one degree of
    freedom at a time, we should rotate the conformation vector degrees of freedom into an orientation
    that maximizes the movement of all degrees of freedom, all at once.

    Challenges:
    - How do we find the rotation matrix that maximizes the uniformity of elements in all rotated
      conformation vectors? (Ideas: Lagrange multipliers,...)
    - Given this matrix and the ideal rotation of the conformation vectors, how to we ensure that
      all rotated grid points are within a predefined range of the original grid? (Ideas: see if each
      parameter is outside the range, and if so, then add/subtract by (grid_width * delta rotated conf.
      vector, perform all grid movements in unrotated grid, then to evaluate the conformation, rotate the
      grid, construct the conformation, evaluate!)
    - How do we interconvert between the system grid index and the conformation of the system? (Ideas:
      rotate the system conf. by the inverse of the rotate matrix, find the grid we are in. To go the
      other way, rotate the grid point, convert to conformation.

      I think a key will be to never work with a rotated grid, except to construct the configuration
      at a particular grid point.

3) Explore conformation space with the pathfinding algorithm

'''

import re, math
import numpy as np
import pdb2 as pdb

elect_const = 1.0 #18.2223 # the electrostatic constant in kcal A mol**-1 q**-2; I think it's already multiplied by this amount

# Classes for parsing a prmtop file


class Atom():
  'An atom in simulation'
  def __init__(self, index, atom_name):
    self.index = index + 1
    self.serial = index
    self.atom_name = atom_name
    self.resname = 'UNK'
    self.resid = 0
    self.charge = 0.0
    self.atomic_number = 0
    self.mass = 0.0
    self.atom_type_index = 0
    self.number_excluded_atoms = 0
    self.amber_atom_type = ''
    self.tree_chain_classification = ''
    self.radius = 0.0
    self.screen = 0.0
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0
    self.excluded_list = [] # a list of atom indeces that will be excluded from nonbonded calculations
    self.bonds = [] # keep track of all bonds this atom is a part of
    self.angles = [] # keep track of all angles this atom is a part of
    self.dihedrals = [] # keep track of all dihedrals this atom is a part of
'''
class Atom_type():
  'a type for an atom'
  def __init__():
    self.
'''
class Residue():
  'a collection of atoms'
  def __init__(self, label):
    self.label = label
    self.pointer = 0 # the index of the atom we are pointing to
    self.atoms = []

class Bond():
  'A bond connecting two atoms'
  def __init__(self, atom1, atom2, bond_type):
    self.atom1 = atom1
    self.atom2 = atom2
    self.bond_type = bond_type
    self.length = 0.0
    self.angles = [] # keep track of all angles this bond can be a part of
    self.dihedrals = [] # keep track of all dihedrals this bond is a part of
    #self.index = index # the index of the force const, eq. value
    atom1.bonds.append(self) # inform the child atoms that they are a part of this bond now
    atom2.bonds.append(self)

  def calc_length(self):
    ' this bond will calculate its own length'
    x1 = self.atom1.x; y1 = self.atom1.y; z1 = self.atom1.z # puts the coords into easy vars
    x2 = self.atom2.x; y2 = self.atom2.y; z2 = self.atom2.z
    self.length = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    return self.length

  def calc_energy(self):
    ' calculates the energy of this bond. The length must be properly computed before this point'
    length_eq = self.bond_type.equil_value # retrieve the constants
    k = self.bond_type.force_const
    energy = 0.5*k*(self.length - length_eq)**2 # harmonic potential
    return energy

  def print_atoms(self):
    return self.atom1.serial, self.atom2.serial

class Bond_type():
  'A type for a generic bond'
  def __init__(self):
    self.force_const = 0.0
    self.equil_value = 0.0

class Angle():
  'A bond connecting two atoms'
  def __init__(self, atom1, atom2, atom3, angle_type):
    self.atom1 = atom1
    self.atom2 = atom2
    self.atom3 = atom3
    self.angle_type = angle_type
    self.angle = 0.0
    self.bonds = []
    self.dihedrals = []
    #self.index = None # the index of the force const, eq. value
    #bond_set = set() # a set of all possible bonds that this angle *might* have, we will have to sift through them later
    atom1.angles.append(self) # have our child atoms add this angle to their list of angles
    for bond in atom1.bonds:
      if (bond.atom1 == atom1 and bond.atom2 == atom2) or (bond.atom2 == atom1 and bond.atom1 == atom2):
        self.bonds.append(bond)
        bond.angles.append(self) # tell the child bonds they have this as an angle
    atom2.angles.append(self) # inform all child atoms that they are now a part of this angle
    for bond in atom2.bonds:
      if (bond.atom1 == atom2 and bond.atom2 == atom3) or (bond.atom2 == atom3 and bond.atom1 == atom3):
        self.bonds.append(bond)
        bond.angles.append(self) # tell the child bonds that they have this as an angle
    atom3.angles.append(self)
    #print "len(self.bonds):", len(self.bonds)
    #print "angle bonds", self.bonds[0].atom1.index, '-', self.bonds[0].atom2.index, " and ", self.bonds[1].atom1.index, '-', self.bonds[1].atom2.index, 'len(bonds):', len(self.bonds)
  def calc_angle(self):
    ' this bond will calculate its own length'
    x1 = self.atom1.x; y1 = self.atom1.y; z1 = self.atom1.z
    x2 = self.atom2.x; y2 = self.atom2.y; z2 = self.atom2.z # fill out the coords into easy vars
    x3 = self.atom3.x; y3 = self.atom3.y; z3 = self.atom3.z
    vec1 = np.array([x1-x2,y1-y2,z1-z2]) # the vectors pointing from atom2 to the others
    vec2 = np.array([x3-x2,y3-y2,z3-z2])
    #x = np.dot(vec1,vec2)
    #self.angle = np.arccos(np.dot(vec1/np.linalg.norm(vec1), vec2/np.linalg.norm(vec2))) # get the angle between the two normalized vectors
    self.angle = angle_from_points(vec1, vec2)
    return self.angle

  def calc_energy(self):
    ' calculates the energy of this bond. The length must be properly computed before this point'
    angle_eq = self.angle_type.equil_value # retrieve the constants
    k = self.angle_type.force_const
    energy = 0.5*k*(self.angle - angle_eq)**2 # harmonic potential
    return energy

  def print_atoms(self):
    return self.atom1.serial, self.atom2.serial, self.atom3.serial

class Angle_type():
  'A type for an angle'
  def __init__(self):
    self.force_const = 0.0
    self.equil_value = 0.0

class Dihedral():
  'A bond connecting two atoms'
  def __init__(self, atom1, atom2, atom3, atom4, dihedral_type, improper=False, calc_1_4=True):
    self.atom1 = atom1
    self.atom2 = atom2
    self.atom3 = atom3
    self.atom4 = atom4
    self.dihedral_type = dihedral_type
    self.phi = 0.0
    self.improper = improper
    self.calc_1_4 = calc_1_4
    #self.index = index # the index of the force const, eq. value
    self.atom1.dihedrals.append(self); self.atom2.dihedrals.append(self) # inform all child atoms that they are now a part of this dihedral
    self.atom3.dihedrals.append(self); self.atom4.dihedrals.append(self)
    # do we need to tell the angles and bonds?

  def calc_torsion(self):
    ' this bond will calculate its own length'
    x1 = self.atom1.x; y1 = self.atom1.y; z1 = self.atom1.z
    x2 = self.atom2.x; y2 = self.atom2.y; z2 = self.atom2.z # fill out the coords into easy vars
    x3 = self.atom3.x; y3 = self.atom3.y; z3 = self.atom3.z
    x4 = self.atom4.x; y4 = self.atom4.y; z4 = self.atom4.z
    vec1 = np.array([x2-x1,y2-y1,z2-z1])
    axis = np.array([x3-x2,y3-y2,z3-z2]) # the vectors of the bonds, from one to the other
    vec2 = np.array([x4-x3,y4-y3,z4-z3])
    cross1 = np.cross(vec1,axis) # find cross product between each vec and the axis
    cross2 = np.cross(axis,vec2)
    cross1 = cross1/np.linalg.norm(cross1) # normalize the cross products
    cross2 = cross2/np.linalg.norm(cross2) # could get arccos at this point, but...
    x = np.dot(cross1, cross2) # instead we are going to formulate things, so we can use atan2
    y = np.dot(np.cross(cross1, axis/np.linalg.norm(axis)), cross2)
    #self.angle = np.arccos(np.dot(vec1/np.linalg.norm(vec1), vec2/np.linalg.norm(vec2))) # get the angle between the two normalized vectors
    self.phi = -np.arctan2(y,x)
    return self.phi

  def calc_energy(self):
    ' calculates the energy of this bond. The length must be properly computed before this point'
    periodicity = self.dihedral_type.periodicity # retrieve the constants
    phase = self.dihedral_type.phase
    k_tor = self.dihedral_type.force_const
    energy = k_tor*np.cos(periodicity*self.phi - phase) # harmonic potential
    return energy

class Dihedral_type():
  'A type for an angle'
  def __init__(self):
    self.force_const = 0.0
    self.periodicity = 0.0
    self.phase = 0.0
    self.scee_scale_factor = 0.0
    self.scnb_scale_factor = 0.0

class LJ_pair_type():
  'represents an atom pair for Lennard-Jones calculations'
  def __init__(self):
    self.a_coeff = 0.0
    self.b_coeff = 0.0

# a list of values that will be found in the 'pointers' section of the prmtop
pointer_names = ["NATOM", "NTYPES", "NBONH", "MBONA", "NTHETH", "MTHETA", "NPHIH", "MPHIA", "NHPARM", "NPARM", "NNB", "NRES", "NBONA", "NTHETA", "NPHIA", "NUMBND", "NUMANG", "NPTRA", "NATYP", "NPHB", "IFPERT", "NBPER", "NGPER", "NDPER", "MBPER", "MGPER", "MDPER", "IFBOX", "NMXRS", "IFCAP", "NUMEXTRA",] # "NCOPY"]

class System():
  '''A molecular system for md simulation'''
  def __init__(self, pointers):
    '''given a 'POINTERS' list, will fill out useful simulation parameters'''
    print "len(pointers):", len(pointers)
    print "len(pointer_names):", len(pointer_names)
    for i in range(len(pointer_names)):
      exec_str = 'self.%s = pointers[%d]' % (pointer_names[i].lower(), i) # for each pointer, fill a variable for the system object
      exec(exec_str) # execute the string as python code
    self.atoms = []
    #self.atom_types = []
    self.residues = []
    self.bonds = [] # just create the empty bond list for now
    self.bond_types = []
    for i in range(self.numbnd): # create all bond_types
      self.bond_types.append(Bond_type())
    self.angles = [] # just create the empty angle list for now
    self.angle_types = []
    for i in range(self.numang): # create all angle_types
      self.angle_types.append(Angle_type())
    self.dihedrals = [] # just create the empty dihedral list for now
    self.dihedral_types = []
    for i in range(self.nptra): # create all dihedral types
      self.dihedral_types.append(Dihedral_type())
    self.lj_pairs = []
    self.lj_pair_types = []
    for i in range((self.ntypes*(self.ntypes+1))/2):
      self.lj_pair_types.append(LJ_pair_type())
    self.excluded_atoms_list = []


  def read_inpcrd(self, inpcrd_filename):
    ''' given a system found from a prmtop file, will read an inpcrd to fill out the atomic coordinates '''
    inpcrd_file = open(inpcrd_filename, 'r')
    entries = [] # a list of all entries for this flag
    counter = 0
    for line in inpcrd_file.xreadlines():
      line = line.rstrip()
      if counter >= 2: # this is where the coordinates start
        temp_list = chunks(line, 12) # read all coordinates into one long list
        entries += map(float, temp_list)
      counter += 1

    counter = 0
    for coord in chunks(entries, 3): # split all these numbers into groups of 3
      self.atoms[counter].x = coord[0]
      self.atoms[counter].y = coord[1] # fill out the coordinates of every atom
      self.atoms[counter].z = coord[2]
      counter += 1
    return

  def make_excluded_lists(self):
    ''' fills out each atom's non-nonbonded atom indeces not to compute nonbonded for'''
    on_index = 0
    for atom in self.atoms: # run through all the atoms
      num_excluded = atom.number_excluded_atoms # the number of other atoms to exclude for this atom
      atom.excluded_list = self.excluded_atoms_list[on_index: on_index+num_excluded] # take a slice of atom indeces
      #atom.excluded_list = map(lambda x:x-1, this_excluded_list) # subtract one from all of them (to get python indexing), and include in this atom
      on_index += num_excluded
    return

  def cartesian_to_conf(self):
    ''' given all the x,y,z coordinates of the atoms, will fill out bond lengths, angles, and dihedrals'''
    #total_energy = 0.0
    for bond in self.bonds: # For all bonds
      bond.calc_length()

    for angle in self.angles: # For all angles
      angle.calc_angle()

    for dihed in self.dihedrals: # For all dihedrals
      dihed.calc_torsion()

  def conf_to_cartesian(self):
    '''given the bond lengths, angles, dihedrals, will compute the cartesian coordinates of all the atoms'''
    remaining_bonds = self.bonds[1:]
    remaining_angles = self.angles[:]
    remaining_dihedrals = self.dihedrals[:]
    bonds = [self.bonds[0]]; atom1 = bond1.atom1; atom2 = bond1.atom2
    # now search the angle list for all angles that contain this bond



  def calc_energy(self, reconfigure=False):
    '''calculates the energy for the configuration of the system'''
    if reconfigure:
      self.cartesian_to_conf() # then we need to get the configuration of the system
    total_energy = 0.0

    for bond in self.bonds: # For all bonds
      energy = bond.calc_energy()
      #print "bond energy:", energy
      total_energy += energy

    for angle in self.angles: # For all angles
      energy = angle.calc_energy()
      #print "angle energy:", energy
      total_energy += energy

    for dihed in self.dihedrals: # For all dihedrals
      energy = dihed.calc_energy()
      #print "dihedral energy:", energy
      total_energy += energy

    # nonbonded energies
    for i in range(self.natom): # the index of each atom
      atom_i = self.atoms[i]
      excl_index = 0 # an easy way to find atoms to exclude from the
      for j in range(i+1, self.natom): # to each other atom (with a higher index)
        if excl_index<len(atom_i.excluded_list) and j == atom_i.excluded_list[excl_index]:
          excl_index += 1
          continue # continue to the next atom
        atom_j = self.atoms[j]
        x1 = atom_i.x; y1 = atom_i.y; z1 = atom_i.z # puts the coords into easy vars
        x2 = atom_j.x; y2 = atom_j.y; z2 = atom_j.z
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2) # calculate the distance between the two atoms
        inv_dist = 1/dist # invert this for quick math
        # coulombic energy
        energy = elect_const * atom_i.charge * atom_j.charge * inv_dist
        #print "coulombic energy:", energy, " dist:", dist
        total_energy += energy
        # LJ energy
        nonbonded_parm_index = self.ntypes * (atom_i.atom_type_index) + atom_j.atom_type_index # the index for the nonbonded_parm_index section
        #print "nonbonded_parm_index:", nonbonded_parm_index, "len(self.lj_pairs):", len(self.lj_pairs)
        lj_index = self.lj_pairs[nonbonded_parm_index] # the index for the LJ a & b coeffs
        a = self.lj_pair_types[lj_index].a_coeff; b = self.lj_pair_types[lj_index].b_coeff # the LJ coeffs
        inv_dist_3 = inv_dist*inv_dist*inv_dist # cube the inverted distance
        inv_dist_6 = inv_dist_3*inv_dist_3; inv_dist_12 = inv_dist_6*inv_dist_6 # get the other powers of the inverted distance cheaply
        energy = a*inv_dist_12 - b*inv_dist_6
        #print "LJ energy:", energy, " dist:", dist, " i:", i, " j:", j
        total_energy += energy

    return total_energy

def angle_from_points(vec1, vec2):
  #x = np.dot(vec1,vec2)
  return np.arccos(np.dot(vec1/np.linalg.norm(vec1), vec2/np.linalg.norm(vec2))) # get the angle between the two normalized vectors


def chunks(our_str, n):
  'Splits a string/list into a list of evenly sized strings/lists of length n'
  our_list = []
  for i in range(0, len(our_str), n): # could use xrange and yield if I want a generator
    our_list.append(our_str[i:i+n])
  return our_list

def digest_section(system, mode, entries):
  if mode == "pointers": # then construct the simulation system
    system = System(entries)
    print "system.natom", system.natom
  # atomic parameters
  elif mode == "atom_name":
    for i in range(len(entries)):
      atom = Atom(i, entries[i])
      system.atoms.append(atom)
  elif mode == "charge":
    for i in range(len(entries)):
      system.atoms[i].charge = entries[i]
  elif mode == "atomic_number":
    for i in range(len(entries)):
      system.atoms[i].atomic_number = entries[i]
  elif mode == "mass":
    for i in range(len(entries)):
      system.atoms[i].mass = entries[i]
  elif mode == "atom_type_index":
    for i in range(len(entries)):
      system.atoms[i].atom_type_index = entries[i] -1 # subtract one to make the indeces pythonic
  elif mode == "number_excluded_atoms":
    for i in range(len(entries)):
      system.atoms[i].number_excluded_atoms = entries[i]
  elif mode == "amber_atom_type":
    for i in range(len(entries)):
      system.atoms[i].amber_atom_type = entries[i]
  elif mode == "tree_chain_classification":
    for i in range(len(entries)):
      system.atoms[i].tree_chain_classification = entries[i]
  elif mode == "radii":
    for i in range(len(entries)):
      system.atoms[i].radius = entries[i]
  elif mode == "screen":
    for i in range(len(entries)):
      system.atoms[i].screen = entries[i]

  # residue params
  elif mode == "residue_label":
    print "now doing residues..."
    for i in range(len(entries)):
      print "adding residue:", entries[i]
      system.residues.append(Residue(entries[i]))
  elif mode == "residue_pointer":
    for i in range(len(entries)):
      system.residues[i].pointer = int(entries[i])

    # residue assignment
    print "len(system.residues):", len(system.residues)
    resid = 0
    resname = system.residues[resid].label

    for atom in system.atoms:
      #print "atom index:", atom.index, "atom name:", atom.atom_name, "resid:", resid, "resname:", resname
      if len(system.residues) > resid+1:
        if atom.index >= system.residues[resid+1].pointer-1:
          resid += 1
          resname = system.residues[resid].label
      atom.resid = resid+1
      atom.resname = resname
      system.residues[resid].atoms.append(atom)

  # bond parameters
  elif mode == "bond_force_constant":
    for i in range(len(entries)):
      system.bond_types[i].force_const = entries[i]
  elif mode == "bond_equil_value":
    for i in range(len(entries)):
      system.bond_types[i].equil_value = entries[i]

  # angle parameters
  elif mode == "angle_force_constant":
    for i in range(len(entries)):
      system.angle_types[i].force_const = entries[i]
  elif mode == "angle_equil_value":
    for i in range(len(entries)):
      system.angle_types[i].equil_value = entries[i]

  # dihedral parameters
  elif mode == "dihedral_force_constant":
    for i in range(len(entries)):
      system.dihedral_types[i].force_const = entries[i]
  elif mode == "dihedral_periodicity":
    for i in range(len(entries)):
      system.dihedral_types[i].periodicity = entries[i]
  elif mode == "dihedral_phase":
    for i in range(len(entries)):
      system.dihedral_types[i].phase = entries[i]
  elif mode == "scee_scale_factor":
    for i in range(len(entries)):
      system.dihedral_types[i].scee_scale_factor = entries[i]
  elif mode == "scnb_scale_factor":
    for i in range(len(entries)):
      system.dihedral_types[i].scnb_scale_factor = entries[i]

  # lj pairs
  elif mode == "nonbonded_parm_index":
    for i in range(len(entries)):
      system.lj_pairs.append(entries[i]-1)

  # lj pair types
  elif mode == "lennard_jones_acoef":
    for i in range(len(entries)):
      system.lj_pair_types[i].a_coeff = entries[i]
  elif mode == "lennard_jones_bcoef":
    for i in range(len(entries)):
      system.lj_pair_types[i].b_coeff = entries[i]

  # Bonds
  #  at this time, we don't care about hydrogen or not...
  elif mode in ["bonds_inc_hydrogen", "bonds_without_hydrogen"]:
    all_bonds = chunks(entries, 3) # makes a new list of 3 elements each
    for bond_list in all_bonds:
      bond_type_index = bond_list[2] - 1 # the index for the bond_type for this particular bond
      #print "len(system.atoms):", len(system.atoms), " bond_list:", bond_list
      system.bonds.append(Bond(system.atoms[bond_list[0]/3], system.atoms[bond_list[1]/3], system.bond_types[bond_type_index]))

  # Angles
  #  at this time, we don't care about hydrogen or not...
  elif mode in ["angles_inc_hydrogen", "angles_without_hydrogen"]:
    all_angles = chunks(entries, 4) # makes a new list of 4 elements each
    for angle_list in all_angles:
      angle_type_index = angle_list[3] - 1
      system.angles.append(Angle(system.atoms[angle_list[0]/3], system.atoms[angle_list[1]/3], system.atoms[angle_list[2]/3], system.angle_types[angle_type_index]))

  # Dihedrals
  #  at this time, we don't care about hydrogen or not...
  elif mode in ["dihedrals_inc_hydrogen", "dihedrals_without_hydrogen"]:
    all_diheds = chunks(entries, 5) # makes a new list of 4 elements each
    for dihed_list in all_diheds:
      dihed_type_index = dihed_list[4]
      improper = False
      calc_1_4 = True
      if dihed_list[2] < 0: # if this term is negative...
        calc_1_4 = False # then 1-4 nonbonded interactions for this torsion is not calculated
        dihed_list[2] = abs(dihed_list[2])
      if dihed_list[3] < 0: # if this term is negative...
        improper = True# then this torsion is improper
        dihed_list[3] = abs(dihed_list[3])

      dihed_type_index = dihed_type_index - 1
      #print "dihed_type_index:", dihed_type_index
      system.dihedrals.append(Dihedral(system.atoms[dihed_list[0]/3], system.atoms[dihed_list[1]/3], system.atoms[dihed_list[2]/3], system.atoms[dihed_list[3]/3], system.dihedral_types[dihed_type_index], improper = improper, calc_1_4 = calc_1_4))

  # excluded nonbonded
  elif mode == "excluded_atoms_list":
    for i in range(len(entries)):
      system.excluded_atoms_list.append(entries[i]-1)




  return system

def read_prmtop(prmtop_filename):
  '''Peforms the tedious task of parsing a prmtop file to create the necessary objects for simulation'''
  prmtop_file = open(prmtop_filename, 'r')
  mode = 'nominal' # we aren't doing anything yet
  entries = [] # a list of all entries for this flag
  for line in prmtop_file.xreadlines():
    line = line.rstrip()
    if line.startswith('%FLAG'): # this will tell us what parameter we are filling out
      # process the data from the previous section...
      #print "mode:", mode, "entries:", entries
      if mode in ['title','nominal']:
        pass
      elif mode == "pointers":
        system = digest_section(None, mode, entries) # no system yet, so passing as a "None"
      else:
        system = digest_section(system, mode, entries)
      mode = line.strip().split()[1].lower()
      entries = []
    elif line.startswith('%FORMAT'): # this will tell us the format of subsequent lines till the next section
      inside = line.strip().split('(')[1].strip(')') # get the string inside the parentheses
      if 'I' in inside: # then we have an integer
        inside = inside.split('I')
        section_func = int
      elif 'E' in inside: # then we have a float
        inside = re.split('E|\.',inside)
        section_func = float
      elif 'a' in inside: # then we have a string
        inside = inside.split('a')
        section_func = str

      num_entries = int(inside[0]) # the number of entries per line
      num_chars = int(inside[1]) # the number of characters per entry
    elif line.startswith('%'):
      pass # don't do anything because we don't care about the version or comments at this time
    else: # then we are reading the data for this section
      temp_list = chunks(line, num_chars) # get the list of entries on this line
      entries += map(section_func, temp_list) # add what's on this line to the overall list of entries

  # Now that we've read in the prmtop file, it's time to do some postprocessing
  system.make_excluded_lists()

  return system

def write_pdb(system, filename):
  pdb_struct = pdb.Structure('from_prmtop')
  for atom in system.atoms: # loop thru all our own atoms
    pdb_atom = pdb.Atom('ATOM', str(atom.index), atom.atom_name, '', atom.resname, 'X', str(atom.resid), '', atom.x, atom.y, atom.z, '0.00','0.00', '','0.00')
    pdb_struct.atoms.append(pdb_atom)
    pdb_struct.num_atoms += 1
  pdb_struct.num_resids = len(system.residues)
  pdb_struct.save(filename)
  return


if __name__=="__main__":
  prmtop_filename = "/scratch/lvotapka/projects/folding/alanine_dipeptide/adi_dry.prmtop"
  inpcrd_filename = "/scratch/lvotapka/projects/folding/alanine_dipeptide/adi_dry.inpcrd"
  prmtop = read_prmtop(prmtop_filename)
  prmtop.read_inpcrd(inpcrd_filename)
  prmtop.cartesian_to_conf()
  total_energy = prmtop.calc_energy()
  print "total_energy:", total_energy
