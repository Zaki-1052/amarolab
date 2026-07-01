# Inside points.py

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
    
    probe_rad = 1.5
    
    # parse the arguments
    parser = argparse.ArgumentParser(description="Generates grid of 1's or 0's denoting the inside and outside of the molecule. If the lower corner and spacing are not specified, reasonable default values are computed.")
    parser.add_argument('-p', '-pqr', dest="pqr", type=str, help="name of pqr file containing atoms data")
    parser.add_argument('-c', '-corner', dest="corner", default=[0.0,0.0,0.0], type=float, nargs=3, help="sets lower corner of exclusion grid")
    parser.add_argument('-n', '-ngrid', dest="ngrid", nargs=3, type=int, help="set number of grid points in each direction")
    parser.add_argument('-s', '-spacing', dest="spacing", nargs=3, default=[1.0,1.0,1.0], type=float, help="set grid point spacing")
    parser.add_argument('-e', '-exclusion_distance', dest="exclusion", default=0.0, type=float, help="set size of exclusion distance from spheres")
    
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
    pqrfilename = args['pqr']
    exclusion_rad = args['exclusion']
    # create the empty grid in memory
    grid = np.zeros((nx, ny, nz), dtype=np.int8)
    #print grid.shape
    
    
    # read the pqr file, 
    #print "Opening pqr file... time:", time.time() - starttime
    parser=pdb.Big_PDBParser()
    pqr = parser.get_structure('pqr file',pqrfilename, preserve_index = False, preserve_resid = False, pqr=True)
    
    #print len(pqr.atoms)
    inv_dx = 1.0 / dx; inv_dy = 1.0 / dy; inv_dz = 1.0 / dz # for quickness of computation
    max_dx_inv = 1.0 / max([dx, dy, dz])
    
    # loop through all the atoms, setting the nearby grid points equal to 1
    #print "Looping thru atoms to find occupied grid points... time:", time.time()-starttime
    for atom in pqr.atoms:
      closegridx = int((atom.x - origx) / dx)
      closegridy = int((atom.y - origy) / dy) # find a close member of the grid
      closegridz = int((atom.z - origz) / dz)
      radius = float(atom.radius) + exclusion_rad
      
      #proximity = int(radius / max([dx, dy, dz])) + 1
      proximity = int(radius * max_dx_inv) + 1
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
              
              
    # find all the cavities and exclude them
    
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
    </reduced_surface>"""
    
    

`
