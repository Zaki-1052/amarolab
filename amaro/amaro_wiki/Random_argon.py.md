# Random argon.py

`
    
    
    
    # By Lane Votapka
    
    '''
    Places N random argon molecules within a box whose origin is 0,0,0 and of specified side lengths
    '''
    
    import os, sys, random
    import pdb2 as pdb
    from math import sqrt
    import numpy as np
    
    
    check_clashing = True # before placing atom, check whether its clashing with any others
    
    x_orig = 0.0
    y_orig = 0.0 # origins of the box
    z_orig = 0.0
    
    x_width = 36.7978
    y_width = 36.7978 # width of the box sides
    z_width = 36.7978
    
    N = 864 # number of argon molecules to place
    
    sigma = 3.4
    
    max_tries = 10000 # maximum number of tries before giving up
    
    # create a new structure
    structure = pdb.Structure('argon_box')
    
    def dist(atom1, atom2):
      '''find distance between 2 atoms'''
      #return sqrt((atom1.coords[0]-atom2.coords[0])**2 + (atom1.coords[1]-atom2.coords[1])**2 + (atom1.coords[2]-atom2.coords[2])**2)
      coord_dist = np.array(atom1.coords) - np.array(atom2.coords)
      return np.linalg.norm(coord_dist)
    
    
    
    # place new atoms into the structure
    totalN = 0
    tries = 0
    for i in range(N):
      if i % 100 == 0: print "now on atom:", i, ". Last number of tries: ", tries
      tries = 0
      
      while True: # as long as we haven't exceeded the largest possible number of tries
        if tries < max_tries:
          clashing = False
          x = random.uniform(x_orig,x_width) #0.01 + 3.631 * int(i / 100) #
          y = random.uniform(y_orig,y_width) #0.01 + 3.631 * (int(i / 10) % 10) #
          z = random.uniform(z_orig,z_width) #0.01 + 3.631 * (i % 10) #
          newatom = pdb.Atom('ATOM', i, 'Ar','', 'Ar', '', str(i), '', x,y,z, 0.00, 0.00, '', '' )
          if check_clashing:
            for oldatom in structure.atoms:
              our_dist = dist(oldatom,newatom)
              #print our_dist
              if our_dist < sigma: # then there's a clash, we have to try again
                #print "skipping distance:", our_dist
                tries += 1
                clashing = True
                break
            pass
          if not clashing:
            structure.atoms.append(newatom) # adding atom
            structure.num_atoms += 1 # incrementing counter
            totalN += 1
            break
          
        else:
          print "Alert: Maximum number of tries exceeded"
          break
        
        
        
    print "now writing %d atoms to file" % totalN
    
    structure.save('lower_density_cube.pdb')
    
    

`
