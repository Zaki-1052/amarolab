# Surface spheres.py

`
    
    
    
    '''
    By Lane Votapka
    Amaro lab 2014
    
    For huge molecules
    
      Generates grid of 1's or 0's denoting the inside and outside of the molecule. If the lower corner and spacing are not
      specified, reasonable default values are computed.
    
      The following arguments with flags are used:
    
      -pqr : name of pqr file containing atoms data
      -corner" : sets lower corner of exclusion grid
      -ngrid"  : set number of grid points in each direction (default 100 100 100)
      -spacing : set grid point spacing
      -exclusion_distance : set size of exclusion distance from spheres (default: probe radius)
    
    
    '''
    
    import pdb2 as pdb
    import sys, re
    from cStringIO import StringIO # NOTE: may want to change this to cStringIO if more speed is needed in the future
    import numpy as np
    import argparse
    import time
    import xml.sax as sax
    
    class BrowndyeRxnHandler(sax.handler.ContentHandler):
      'parses a Browndye rxn file to find all the atomic pairs'
      def __init__(self):
        self.atoms_tags = []
        self._charBuffer = []
    
      def startElement(self, name, attrs):
        self.CurrentName = name
    
      def characters(self, content):
        if self.CurrentName == 'atoms':
          self._charBuffer.append(content.strip())
    
      def endElement(self, name):
        if name == 'atoms':
          self.atoms_tags.append(' '.join(self._charBuffer).strip())
          self._charBuffer = []
    
      def parse(self, f):
        sax.parse(f,self)
        return self.atoms_tags
    
    
    
    #probe_rad = 1.5
    starttime = time.time()
    #print "Consider using surface_spheres_multi.py for large structures. It performs the same calculation as this script, but in parallel." # not yet implemented
    print "Parsing arguments"
    # parse the arguments
    parser = argparse.ArgumentParser(description="Generates grid of 1's or 0's denoting the inside and outside of the molecule. If the lower corner and spacing are not specified, reasonable default values are computed.")
    parser.add_argument('-p', '-pqr', dest="pqr", required=True, type=str, help="name of pqr file containing atoms data")
    parser.add_argument('-o', '-output', dest="output", required=True, type=str, help="the output pqrxml file")
    parser.add_argument('-c', '-corner', dest="corner", default=[0.0,0.0,0.0], type=float, nargs=3, help="sets lower corner (origin) of exclusion grid")
    parser.add_argument('-n', '-ngrid', dest="ngrid", nargs=3, type=int, help="set number of grid points in each direction")
    parser.add_argument('-s', '-spacing', dest="spacing", nargs=3, default=[1.0,1.0,1.0], type=float, help="set grid point spacing")
    #parser.add_argument('-e', '-exclusion_distance', dest="exclusion", default=0.0, type=float, help="set size of exclusion distance from spheres")
    parser.add_argument('-r', '-probe_radius', dest="probe_radius", default=1.5, type=float, help="probe radius of volume outside of atoms that are 'rolled' over the surface of the molecule")
    #parser.add_argument('-x', '-rxn', dest="rxn", type=str, default='', help="name of Browndye reaction file containing atoms involved in reactions")
    parser.add_argument('-x1', '-rxn1', dest="rxn1", type=str, default='', help="name of Browndye reaction file containing atoms involved in reactions. Reaction file molecule 1.")
    parser.add_argument('-x2', '-rxn2', dest="rxn2", type=str, default='', help="name of Browndye reaction file containing atoms involved in reactions. Reaction file molecule 2. Cannot be used if -rxn1 is already specified.")
    #parser.add_argument('-f', '-rxn_field', dest="rxn_field", type=int, default=1, choices=[1,2], help="which field in the Browndye reaction file with the loaded molecule's atomic indeces. Options: 1 or 2")
    parser.add_argument('-i', '-ins', dest="ins", type=str, default='', help="Filename of an inside_points grid that is generated at the same time that we are finding surface atoms (it can save time if you're going to run inside_points anyways)")
    
    
    args = parser.parse_args() # parse the args into a dictionary
    args = vars(args)
    #print args
    origx = args['corner'][0]
    origy = args['corner'][1]
    origz = args['corner'][2]
    nx = args['ngrid'][0]
    ny = args['ngrid'][1]
    nz = args['ngrid'][2]
    dx = args['spacing'][0]
    dy = args['spacing'][1]
    dz = args['spacing'][2]
    pqr_filename = args['pqr']
    #exclusion_rad = args['exclusion']
    exclusion_rad = 0.0
    probe_rad = args['probe_radius']
    out_filename = args['output']
    ins_filename = args['ins']
    # create the empty grid in memory
    grid = np.zeros((nx, ny, nz), dtype=np.int8)
    #print grid.shape
    rxn_atoms = set() # a set of atoms that we must include
    assert not( args['rxn1'] and args['rxn2'] ), "both arguments -rxn1 and -rxn2 cannot be specified simultaneously"
    if args['rxn1'] or args['rxn2']: # if the reaction file is specified
      # open the reaction file, parse for the right indeces
      if args['rxn1']:
        rxn_filename = args['rxn1']
        rxn_index = 0
      elif args['rxn2']:
        rxn_filename = args['rxn2']
        rxn_index = 1
    
      rxn_atom_pairs = BrowndyeRxnHandler().parse(rxn_filename) #parse the xml file and get a list of all atoms pairs
      for pair in rxn_atom_pairs: # for each pair, get the desired index
        my_index = pair.split()[rxn_index] # got the index of the atom
        rxn_atoms.add(int(my_index)) # add the atom index to a set so that we can add it to the surface pqrxml
    
    #print "rxn_atoms:", rxn_atoms
    #exit()
    
    # read the pqr file,
    print "Opening pqr file... time:", time.time() - starttime
    parser=pdb.Big_PDBParser()
    pqr = parser.get_structure('pqr file',pqr_filename, preserve_index = True, preserve_resid = True, pqr=True)
    
    #pqr.save(out_filename, remark=False, endmdl=False, pqrxml=True)
    
    #print len(pqr.atoms)
    
    print "Looping thru atoms to find occupied grid points... time:", time.time()-starttime
    # loop through all the atoms, setting the nearby grid points equal to 1
    lastpoint = [0,0,0]
    inv_dx = 1.0 / dx; inv_dy = 1.0 / dy; inv_dz = 1.0 / dz # for quickness of computation
    max_dx_inv = 1.0 / max([dx, dy, dz])
    for atom in pqr.atoms:
      closegridx = int((atom.x - origx) * inv_dx)
      closegridy = int((atom.y - origy) * inv_dy) # find a close member of the grid
      closegridz = int((atom.z - origz) * inv_dz)
      radius = float(atom.radius) + probe_rad
      if atom.radius <= 0.0: continue # skip atoms with no radius
    
      proximity = int(radius * max_dx_inv) + 1 # FLAG FOR OPTIMIZATION
      for i in range(closegridx - proximity, closegridx + proximity + 1):
        if i < 0 or i >= nx: continue
        for j in range(closegridy - proximity, closegridy + proximity + 1):
          if j < 0 or j >= ny: continue
          for k in range(closegridz - proximity, closegridz + proximity + 1):
            if k < 0 or k >= nz: continue
            if grid[i,j,k] == 1: continue
            gridpoint = np.array([i * dx + origx, j * dy + origy, k * dz + origz])
            #print "gridpoint:", gridpoint
            dist = gridpoint - atom.coords
            #print "dist:", dist
            if np.dot(dist,dist) < radius*radius:
              #print "close:", i, j, k
              grid[i,j,k] = 1
              lastpoint = [i,j,k]
    
    # write the inside_points xml file
    if ins_filename:
      ins_file = open(ins_filename, 'w')
      ins_file.write("""<reduced_surface>
      <probe_radius> %.6f </probe_radius>
      <exclusion_radius> %.6f </exclusion_radius>
      <grid>
        <corner> %.6f %.6f %.6f </corner>
        <npts> %d %d %d </npts>
        <spacing> %.6f %.6f %.6f </spacing>
        <data>\n""" % (probe_rad, exclusion_rad, origx, origy, origz, nx, ny, nz, dx, dy, dz))
      for i in range(nx):
        ins_file.write("      <plane>\n")
        for j in range(ny):
          ins_file.write(' '.join(["        <row> ",' '.join(map(str, grid[i,j,:].tolist())), "</row>\n"]))
        ins_file.write("      </plane>\n")
    
      ins_file.write("""    </data>
      </grid>
    </reduced_surface>\n""")
      ins_file.close()
    
    i = lastpoint[0]; j = lastpoint[1]; k = lastpoint[2];
    while k < nz-1: # shimmy along z until we get to the border
      k += 1
      if grid[i,j,k] == 1:
        lastpoint = [i,j,k]
      #print "jumping..."
    
    #print "lastpoint:", lastpoint
    
    print "Looping thru grid points to find ones close to atoms... time:", time.time()-starttime
    # find all the grid points with value 0 that are next to a point with value 1
    curpos = lastpoint #[0, 0, 0] # the grid point we are currently on
    searchlist = [curpos] # the point we have yet to explore
    maxnum = 9e99 #130*130*130 # set a max so we don't get stuck in the while loop
    iterations = 0
    while searchlist:
      curpos = searchlist.pop() # get the last item in the list
      grid[curpos[0], curpos[1], curpos[2]] = 2 # set this node as explored already
      onsurf = False
      adj_list = []
      for i in range(curpos[0] - 1, curpos[0] + 2):
        if i < 0 or i >= nx: continue
        if i == curpos[0]:
          jvals = range(curpos[1] - 1, curpos[1] + 2)
        else:
          jvals = [curpos[1]]
        for j in jvals:
          if j < 0 or j >= ny: continue
          if j == curpos[1]:
            kvals = range(curpos[2] - 1, curpos[2] + 2)
          else:
            kvals = [curpos[2]]
          for k in kvals:
            if k < 0 or k >= nz: continue
            if grid[i,j,k] == 0: # then it is empty and unexplored
              adj_list.append([i,j,k])
            elif grid[i,j,k] == 1: # then we are right on the border with the protein
              grid[curpos[0], curpos[1], curpos[2]] = 3 # mark us as right in the solvent
              onsurf = True
      if onsurf: # then we can add adjacent grid cells to be evaluated
        searchlist += adj_list
    
      iterations += 1
      if iterations > maxnum: # break out if we're going too long
        break
    
    print "Finding atoms close to grid border... time:", time.time()-starttime
    # Now find all the atoms that are close to grid elements with a value of 3
    newatoms = []
    for atom in pqr.atoms:
      closegridx = int((atom.x - origx) * inv_dx)
      closegridy = int((atom.y - origy) * inv_dy) # find a close member of the grid
      closegridz = int((atom.z - origz) * inv_dz)
      radius = float(atom.radius) + probe_rad
      appended_this = False # keep track of whether we included this atom
      proximity = int(radius * max_dx_inv) + 1
      #print "proximity:", proximity
      for i in range(closegridx - proximity, closegridx + proximity + 1):
        for j in range(closegridy - proximity, closegridy + proximity + 1):
          for k in range(closegridz - proximity, closegridz + proximity + 1):
            if i < 0 or j < 0 or k < 0 or i >= nx or j >= ny or k >= nz or appended_this == True: # FLAG OPT
              continue
            #print "grid[i,j,k]:", grid[i,j,k]
    
            if grid[i,j,k] == 3 and atom.radius > 0.0: # then this atom is close to the boundary: write it
              #print "grid[%d,%d,%d]:" % (i,j,k), grid[i,j,k]
              #print "close:", i, j, k
              newatoms.append(atom)
              appended_this = True
              continue
            #else:
              #print "found grid point of 1"
      # check to see if the atom is in the reaction file
      if rxn_atoms:
        if atom.index in rxn_atoms:
          newatoms.append(atom)
    
    # print the pqr file
    print "Printing the output pqr file... time:", time.time()-starttime
    pqr.atoms = newatoms
    pqr.num_atoms = len(newatoms)
    #print "newatoms[0].name", newatoms[0].name
    pqr.save(out_filename, remark=False, standard=False, endmdl=False, pqrxml=True)
    #pqr.save('out_surface.pqr', remark=False, endmdl=False, pqrxml=True)
    
    endtime = time.time() - starttime
    print "Complete"
    print "total time:", endtime
    
    '''
    # write the xml file
    print """<reduced_surface>
      <probe_radius> %.6f </probe_radius>
      <exclusion_radius> %.6f </exclusion_radius>
      <grid>
        <corner> %.6f %.6f %.6f </corner>
        <npts> %d %d %d </npts>
        <spacing> %.6f %.6f %.6f </spacing>
        <data>""" % (probe_rad, exclusion_rad, origx, origy, origz, nx, ny, nz, dx, dy, dz)
    for i in range(nx):
      print "      <plane>"
      for j in range(ny):
        print "        <row>", ' '.join(map(str, grid[i,j,:].tolist())), "</row>"
      print "      </plane>\n"
    
    print """    </data>
      </grid>
    </reduced_surface>"""'''
    
    

`
