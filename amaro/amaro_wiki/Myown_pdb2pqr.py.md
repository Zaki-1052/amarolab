# Myown pdb2pqr.py

`
    
    
    
    #!/usr/bin/python
    
    # This script creates pqr files for excessively large .pdb files using
    # specified Forcefield charge and radius files
    
    # by Lane Votapka
    # Amaro lab 2015
    
    import sys, os, argparse, time
    import pdb2 as pdb
    import pqr_fix_radii
    
    verbose = True
    
    
    def charmm_ff_particulars(atomname, resname):
      # copied from PDB2PQR.py
      
      # Residue substitutions
                
      # Residue substitutions
      if resname == "ACE":
        if atomname == "CH3": atomname = "CAY"
        if atomname == "C": atomname = "CY"
        if atomname == "O": atomname = "OY"
        if atomname == "1H": atomname = "HY1"
        if atomname == "2H": atomname = "HY2"
        if atomname == "3H": atomname = "HY3"
      
      '''    
      if resname == "ILE":
        if atomname == "CD1": atomname = "CD"
        elif atomname == "HD11": atomname = "HD1"
                elif atomname == "HD12": atomname = "HD2"
                elif atomname == "HD13": atomname = "HD3"
                elif atomname == "HG12": atomname = "HG11"
                elif atomname == "HG13": atomname = "HG12"
      elif resname == "CYS" and "HG" not in residue.get("map"):
                resname = "CYS"
                if atomname == "CB":
                    resname = "DISU"
                    atomname = "1CB"
                elif atomname == "SG":
                    resname = "DISU"
                    atomname = "1SG"
      elif resname == "HIS":
                if "HD1" in residue.get("map") and "HE2" in residue.get("map"):
                    resname = "HSP"
                elif "HD1" in residue.get("map"):
                    resname = "HSD"
                elif "HE2" in residue.get("map"):
                    resname = "HSE"
      elif resname == "GLU" or resname == "GLH":
                if "HE1" in residue.get("map"):
                    if atomname == "HE1": atomname = "HE2"
                    elif atomname == "OE1": atomname = "OE2"
                    elif atomname == "OE2": atomname = "OE1"
                    if atomname in ["CG","HG3","HG1","HG2","CD","OE1","OE2","HE2"]: resname = "GLUP"
                    else: resname = "GLU"
                elif "HE2" in residue.get("map"):
                    if atomname in ["CG","HG3","HG1","HG2","CD","OE1","OE2","HE2"]: resname = "GLUP"
                    else: resname = "GLU"
      elif resname == "ASP" or resname == "ASH":
                if "HD1" in residue.get("map"):
                    if atomname == "HD1": atomname = "HD2"
                    elif atomname == "OD1": atomname = "OD2"
                    elif atomname == "OD2": atomname = "OD1"
                    if atomname in ["CB","HB3","HB1","HB2","CG","OD1","OD2","HD2"]: resname = "ASPP"
                    else: resname = "ASP"
                elif "HD2" in residue.get("map"):
                    if atomname in ["CB","HB3","HB1","HB2","CG","OD1","OD2","HD2"]: resname = "ASPP"
                    else: resname = "ASP"
      
      '''
      # Hydrogen Substitutions: 
      if atomname == "H": atomname = "HN"
      elif atomname == "HA2": atomname = "HA1"
      elif atomname == "HA3": atomname = "HA2"
      elif atomname == "HB2" and resname not in ["ALA"]: atomname = "HB1"
      elif atomname == "HB3" and resname not in ["ALA"]: atomname = "HB2"
      elif atomname == "HD2" and resname not in ["HSP","HSE","HSD","ASP"]: atomname = "HD1"
      elif atomname == "HD3" and resname not in ["HIS","HSE","HSD"]: atomname = "HD2"
      elif atomname == "HE2" and resname not in ["TRP","HSP","HSE","HSD","GLU"]: atomname = "HE1"
      elif atomname == "HE3" and resname not in ["TRP","HSP","HSE","HSD",]: atomname = "HE2"
      elif atomname == "HG2": atomname = "HG1"
      elif atomname == "HG3": atomname = "HG2"
      elif atomname == "HG" and resname in ["SER","CYS"]: atomname = "HG1"
      return atomname, resname
    
    def parse_ff_file(filename, ff_type):
      '''function that parses a pdb2pqr.py type data file containing a forcefield.
      It returns a dictionary of dictionaries, whose first layer is the resname.
      The second layer is the atomname. The values of the dictionary are  a list of
      charge and radius data, respectively.
      '''
      ff_dict = {}
      ourfile = open(filename,'r') # open the forcefield file
      for line in ourfile.xreadlines(): # read each line in the file
        line = line.strip().split() # split the line by whitespace and strip off whitespace
        if not line or line[0].startswith('#'): continue # skip comments
        resname = line[0] # first field is the resname
        atomname = line[1] # second field is the atomname
        charge = line[2] # third field is the charge
        radius = line[3] # fourth field is the radius
        atomtype = line[4] # fifth field is the atomtype
        
        if resname not in ff_dict.keys(): # see whether we already have an entry for this residue in the ff_dict
          ff_dict[resname] = {} # if not, then create an empty dictionary for this residue
        ff_dict[resname][atomname] = [float(charge),float(radius)] # assign this residue and this atom to have the proper charge and radius
      
      ourfile.close()
      return ff_dict # return our parameter dictionary
    
    ff_filedict = {
    'CHARMM':'/soft/pdb2pqr/latest/dat/CHARMM.DAT',
    'AMBER':'/soft/pdb2pqr/latest/dat/AMBER.DAT',
    }
    ff_dict = {} # a dictionary of all atom and resid types for assignment
    
    starttime = time.time()
    print "Parsing arguments"
    # parse the arguments
    parser = argparse.ArgumentParser(description="An alternative to pdb2pqr.py. This program is intended to make PQR files from very large structures. It performs no debumping or hydrogen optimizations/additions of any kind whatsoever.")
    parser.add_argument('pdb', metavar='PDB_PATH', type=str, help="name of PDB file to convert")
    parser.add_argument('pqr', metavar='PQR_OUTPUT_PATH', type=str, help="name of the output PQR file")
    parser.add_argument('-x', '--xml', metavar='XML_FILE_NAME', dest="pqrxml", default="", type=str, help="Optionally writes PQRXML file. Argument is name of PQRXML file.")
    parser.add_argument('-f', '--ff', metavar='FIELD_NAME', dest="ff", type=str, help="one or more files that contain the desired forcefields. Separate filenames with colons (:)")
    parser.add_argument('-t', '--ff_type', metavar='FIELD_TYPE', dest='ff_type', type=str, default="", help="the type of forcefield that we are using to parse this structure.")
    parser.add_argument('-r', '--fix_radii', dest='fix_radii', default=True, help="Assign radii according to fix_pqr_radii.py", action="store_true")
    
    args = parser.parse_args() # parse the args into a dictionary
    args = vars(args)
    pdb_filename = args['pdb']
    pqr_filename = args['pqr']
    xml_filename = args['pqrxml']
    ff_filename_list = args['ff'].split(':') # get all the different files that will be used as forcefield files
    ff_type = args['ff_type']
    fix_radii = args['fix_radii']
    
    for ff_filename in ff_filename_list:
      if ff_filename in ff_filedict.keys(): # first see if we can retrieve this forcefield file from a convenient place
        if not ff_type: ff_type = ff_filename
        ff_filename = ff_filedict[ff_filename]
      assert os.path.exists(ff_filename), "Forcefield file: %s does not appear to exist." % ff_filename
      ff_dict.update(parse_ff_file(ff_filename,ff_type))
        
    #print "ff_dict['ASN']['HB2']:", ff_dict['ASN']['HB2']
    
    # read the pdb files,
    if verbose: print "Opening pdb file... time:", time.time() - starttime
    parser=pdb.Big_PDBParser()
    #ourpdb = parser.get_structure('pdb file', pdb_filename, preserve_index = False, preserve_resid = True, conventional=True)
    ourpdb = parser.get_structure('pdb file', pdb_filename, preserve_index = False, preserve_resid = True, conventional=True, pqr=False)
    if not ff_type: ff_type = "charmm" # if it's blank then just assign a default of charmm
    ff_type = ff_type.lower()
    if verbose: print "Assigning charge and radii values... time:", time.time() - starttime
    # first loop thru and create all the residue types
    last_resname = ""
    atomname_list = []
    for atom in ourpdb.atoms:
      if atom.resname != last_resname and last_resname: # then we have a new residue
        # do something with residue_obj
        last_resname = atom.resname
        atomname_list = []
      atomname_list.append(atom.name) # add this member to the list
        
    #print "atom[0].name", ourpdb.atoms[0].resname
    # now assign the charges and radii
    key_errors = [] # keep track of all parameters for atoms which are misnamed or unknown
    for atom in ourpdb.atoms:
      resname = atom.resname
      atomname = atom.name
      #if ff_type == "charmm":
        #atomname, resname = charmm_ff_particulars(atomname, resname) # refine the ff file to make sure that we have consistent naming
      # elif ff_type.lower() == "amber":
        #atomname, resname = amber_ff_particulars(atomname, resname) # refine the ff file to make sure that we have consistent naming
      try: 
        charge, radius = ff_dict[resname][atomname]
      except KeyError:
        key_errors.append("%s %s" % (resname,atomname))
        charge = 0.0
        radius = 0.0
        #print "error with residue:", resname, "atomname:", atomname #, ff_dict[resname]
        #exit()
      atom.charge = charge
      if fix_radii: # then use Jacob's script to assign the proper radius
        radius = pqr_fix_radii.assign_radius(resname, atomname)
      atom.radius = radius
    
    if key_errors:
      print "parameters for residues and/or atoms below not found:"
      for key_error in key_errors:
        print key_error
    #exit()
    
    
    #print "atom[0].charge", ourpdb.atoms[0].charge, "atom[0].radius", ourpdb.atoms[0].radius
    if verbose: print "Writing PQR file... time:", time.time() - starttime
    ourpdb.save(pqr_filename, standard=False, pqr=True) 
    if xml_filename:
      ourpdb.save(xml_filename, standard=False, pqrxml=True) 
    
    if verbose: print "Complete. Total time:", time.time() - starttime
    
    

`
