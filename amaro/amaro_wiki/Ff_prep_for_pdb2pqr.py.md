# Ff prep for pdb2pqr.py

`
    
    
    
    #!/usr/bin/python
    
    # This script reads a CHARMM parameter ff file, and writes it out in a form that PDB2PQR could handle.
    
    # by Lane Votapka
    # Amaro lab 2015
    
    import sys
    
    def parse_ff(lines):
      ''' read each line and fill out an information dictionary of charge and radius info '''
      ff_dict = {}
      type_dict = {} # a dictionary with atom types as keys and their radii values
      residue = '' # the residue we are on
      nonbonded_mode = False # whether we are in a nonbonded section of the FF file
      for line in lines:
        line = line.strip().split() # first word in a line
        if not line: continue
        if line[0].startswith('!') or line[0].startswith('#'): continue # skip comments
        if line[0] in ["RESI","PRES"]: # then we are on a new residue
          residue = line[1] # switch the residue name
          if residue not in ff_dict.keys():
            ff_dict[residue] = [] # create a new list inside this residue to keep track of the atoms
           
        elif line[0] == "ATOM": # info about an atom
          try:
            atomname = line[1]
            atomtype = line[2]
            charge = line[3]
          except IndexError:
            raise Exception("problem with line:"+' '.join(line))
          ff_dict[residue].append([atomname, charge, 0.0, atomtype]) # create a list of all this atom's information
          
        elif line[0] == "NONBONDED": # contains VDW data
          nonbonded_mode = True
          
        if nonbonded_mode:
          if line[0] in ["HBOND", "END", "NBFIX"]: # we are in a new section, no longer looking at nonbonded terms
            nonbonded_mode = False
          else:
            try:
              atom_type = line[0] # atomtype is the first part of the line
              #epsilon = line[2] # we don't really use this
              radius = line[3] # the place where the LJ potential crosses the x-axis
            except IndexError:
              raise Exception("problem with line:"+' '.join(line))
            type_dict[atom_type] = radius # save which radius this atomtype has
          
      return ff_dict, type_dict
        
    
    #starttime = time.time()
    #print "Parsing arguments"
    src_filenames = sys.argv[1:] # all the parameter files
    
    # print Header
    print """# Forcefield parameters
    # found using ff_prep_for_pdb2pqr.py by Lane Votapka
    # RESNAME\tATOMNAME\tCHARGE\tRADIUS\tATOMTYPE
    #"""
    ff_dict = {}
    type_dict = {}
    for src_filename in src_filenames:
      src_file = open(src_filename, 'r') # open the source filename
      ff_dict_part, type_dict_part = parse_ff(src_file.readlines())
      ff_dict.update(ff_dict_part)
      type_dict.update(type_dict_part)
      
    # now run thru the ff_dict, and update all the radius info
    for residue in ff_dict.keys():
      for atomname in ff_dict[residue]:
        atomtype = atomname[3] # this is where we stored the atomtype info
        if atomtype not in type_dict.keys(): # then we are missing the radius information
          print "Warning: radius info does not appear to exist for residue: %s, atomname: %s." % (residue, atomname)
        else:
          atomname[2] = type_dict[atomtype]
          
    # now print out all the information in the correct format
    
    for residue in sorted(ff_dict.keys()):
      for atom in ff_dict[residue]:
        print "%s\t%s\t%s\t%s\t%s" % (residue, atom[0], atom[1], atom[2], atom[3])
    
    

`
