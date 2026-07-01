# Zmatrix.py

`
    
    
    
    '''
    This program creates and reads z-matrices (in an object-oriented format)
    in order to allow for conversion between cartesian and torsional (internal)
    coordinates.
    
    '''
    
    '''
    Need: an algorithm for creating a graph, where all nodes are connected by
    pairs of either angle/angle, or angle/dihedral. Each node is an atom in the
    system. Then, by assigning angle/angle edges a lower weight, and lower
    weights to non-hydrogen-containing angles, we can use the minimum spanning
    tree algorithm
    
    
    '''
    
    import prmtop
    import numpy as np
    import pprint, Queue, math
    from heapq import heappush, heappop
    
    MAX_ITER = 10000
    
    def isclose(a,b,tol=1e-8):
      'tests whether two float values are close to one another. A replacement for numpy.isclose()'
      diff = abs(a-b)
      if diff < tol:
        return True
      else:
        return False
    
    def atom_from_angles(Ax, Ay, Az, Bx, By, Bz, Cx, Cy, Cz, theta1, theta2, length):
      '''Computes the placement of an atom D based on known locations of 3 previous atoms: A, B, and C, the angles theta1 & theta2,
      and the bond length.
      There are actually two solutions to this problem (in most cases), this finds the "right hand" solution by
      computing the cross product of CA and CB.
      Derivation located in July 28 2015 entry in research log.'''
      #print "Ax:", Ax, "Ay:", Ay, "Az:", Az
      #print "Bx:", Bx, "By:", By, "Bz:", Bz
      #print "Cx:", Cx, "Cy:", Cy, "Cz:", Cz
      #print "theta1:", theta1, "theta2:", theta2, "length:", length
      C = np.array([Cx, Cy, Cz])
      CAx = Ax-Cx; CAy = Ay-Cy; CAz = Az-Cz # find all the vectors in this system
      CBx = Bx-Cx; CBy = By-Cy; CBz = Bz-Cz
      CA = np.array([CAx, CAy, CAz]); CB = np.array([CBx, CBy, CBz])
      CA = CA/np.linalg.norm(CA); CB = CB/np.linalg.norm(CB)
      CAx = CA[0]; CAy = CA[1]; CAz = CA[2]
      CBx = CB[0]; CBy = CB[1]; CBz = CB[2]
    
      right_hand = np.cross(np.array([CAx, CAy, CAz]), np.array([CBx, CBy, CBz])) # a vector that points toward the right-hand direction of this angle
      #print "right_hand:", right_hand
      len_cos_theta1 = length * math.cos(theta1)
      len_cos_theta2 = length * math.cos(theta2)
      #print "length_cos_theta1:", len_cos_theta1, " length_cos_theta2:", len_cos_theta2
      d = (CAy*CBz - CAz*CBy)
      alpha = (CAz*CBx - CAx*CBz) #/(CAy*CBz - CAz*CBy)
      beta  = (CAy*CBx - CAx*CBy) #/(CAz*CBy - CAy*CBz)
      gamma = (CBz*len_cos_theta1 - CAz*len_cos_theta2) #/(CAy*CBz - CAz*CBy)
      delta = (CBy*len_cos_theta1 - CAy*len_cos_theta2) #/(CAz*CBy - CAy*CBz)
      # now use the quadratic formula to get the roots of the function: 0 = ax**2 + bx + c
      a = -(alpha**2 + beta**2 + d**2)
      b = -2*(alpha*gamma + beta*delta)
      c = d**2 * length**2 - gamma**2 - delta**2
      in_sqrt = b**2 - 4*a*c
      #print "a:", a, " b:", b, " c:", c, " d:", d, "b**2 - 4*a*c:", in_sqrt
      if isclose(in_sqrt, 0.0): in_sqrt = 0.0
      #CDx1 = (2*alpha*gamma + 2*beta*delta + math.sqrt((2*alpha*gamma + 2*beta*delta)**2 - 4*(alpha**2+beta**2+d**2)*(length**2*d**2 - gamma**2 - delta**2)))/2*(alpha**2+beta**2+d**2) #(-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
      #CDx2 = (2*alpha*gamma + 2*beta*delta - math.sqrt((2*alpha*gamma + 2*beta*delta)**2 - 4*(alpha**2+beta**2+d**2)*(length**2*d**2 - gamma**2 - delta**2)))/2*(alpha**2+beta**2+d**2) #(-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
      CDx1 = (-b + math.sqrt(in_sqrt)) / (2*a)
      CDx2 = (-b - math.sqrt(in_sqrt)) / (2*a)
    
      d = (CAx*CBz - CAz*CBx)
      alpha = (CAz*CBy - CAy*CBz) #/(CAy*CBz - CAz*CBy)
      beta  = (CAx*CBy - CAy*CBx) #/(CAz*CBy - CAy*CBz)
      gamma = (CBz*len_cos_theta1 - CAz*len_cos_theta2) #/(CAy*CBz - CAz*CBy)
      delta = (CBx*len_cos_theta1 - CAx*len_cos_theta2) #/(CAz*CBy - CAy*CBz)
      a = -(alpha**2 + beta**2 + d**2)
      b = -2*(alpha*gamma + beta*delta)
      c = d**2 * length**2 - gamma**2 - delta**2
      in_sqrt = b**2 - 4*a*c
      #print "a:", a, " b:", b, " c:", c, " d:", d, "b**2 - 4*a*c:", in_sqrt
      if isclose(in_sqrt, 0.0): in_sqrt = 0.0
      CDy1 = (-b + math.sqrt(in_sqrt)) / (2*a)
      CDy2 = (-b - math.sqrt(in_sqrt)) / (2*a)
      #CDy1 = CDx1 * alpha + gamma
      #CDy2 = CDx2 * alpha + gamma
    
      d = (CAx*CBy - CAy*CBx)
      alpha = (CAy*CBz - CAz*CBy) #/(CAy*CBz - CAz*CBy)
      beta  = (CAx*CBz - CAz*CBx) #/(CAz*CBy - CAy*CBz)
      gamma = (CBy*len_cos_theta1 - CAy*len_cos_theta2) #/(CAy*CBz - CAz*CBy)
      delta = (CBx*len_cos_theta1 - CAx*len_cos_theta2) #/(CAz*CBy - CAy*CBz)
      a = -(alpha**2 + beta**2 + d**2)
      b = -2*(alpha*gamma + beta*delta)
      c = d**2 * length**2 - gamma**2 - delta**2
      in_sqrt = b**2 - 4*a*c
      #print "a:", a, " b:", b, " c:", c, " d:", d, "b**2 - 4*a*c:", in_sqrt
      if isclose(in_sqrt, 0.0): in_sqrt = 0.0
      CDz1 = (-b + math.sqrt(in_sqrt)) / (2*a)
      CDz2 = (-b - math.sqrt(in_sqrt)) / (2*a)
      #CDz1 = CDx1 * beta + delta
      #CDz2 = CDx2 * beta + delta
      goodvecs = [] # vectors that recreate the correct angles
      for CDx in [CDx1, CDx2]:
        for CDy in [CDy1, CDy2]:
          for CDz in [CDz1, CDz2]:
            CD = np.array([CDx, CDy, CDz])
            test_angle1 = prmtop.angle_from_points(CA, CD)
            test_angle2 = prmtop.angle_from_points(CB, CD)
            #print "test_angle1:", test_angle1, "test_angle2:", test_angle2
            if isclose(test_angle1, theta1, tol=1e-4) and isclose(test_angle2, theta2, tol=1e-4):
              #print "this one is close: theta1:", theta1, " theta2:", theta2
              goodvecs.append(CD)
    
      #vec1 = np.array([CDx1, CDy1, CDz1])
      #vec2 = np.array([CDx2, CDy2, CDz2])
      '''
      if np.dot(vec1, -right_hand) > 0.0:
        Dx = Cx + CDx1; Dy = Cy + CDy1; Dz = Cz + CDz1
        print "angle-angle: vec1 worked"
      else:
        Dx = Cx + CDx2; Dy = Cy + CDy2; Dz = Cz + CDz2
        print "angle-angle: vec2 worked"
      '''
      for CD in goodvecs:
        right_hand_dot = np.dot(CD, -right_hand)
        #print "right_hand_dot:", right_hand_dot
        if right_hand_dot > 0.0 or isclose(right_hand_dot, 0.0):
          #Dx = Cx + CDx1; Dy = Cy + CDy1; Dz = Cz + CDz1
          D = C + CD
          return D[0], D[1], D[2]
      raise Exception, "No suitable location found for new atom"
      return
    
    def NERF(Ax, Ay, Az, Bx, By, Bz, Cx, Cy, Cz, theta, phi, length):
      '''uses the NERF algorithm defined by Parsons, et. al. "Practical Conversion from Torsion Space to Cartesian
      Space for In Silico Protein Synthesis" to convert from torsional space into cartesian space.
      '''
      #origCx = Cx; origCy = Cy; origCz = Cz
      #Ax -= Cx; Ay -= Cy; Az -= Cz # set the origin to be at atom C
      #Bx -= Cx; By -= Cy; Bz -= Cz
      #Cx = 0.0; Cy = 0.0; Cz = 0.0
      C = np.array([Cx,Cy,Cz])
      ABx = Bx-Ax; ABy = By-Ay; ABz = Bz-Az # find all the vectors in this system
      BCx = Cx-Bx; BCy = Cy-By; BCz = Cz-Bz
      AB = np.array([ABx, ABy, ABz]); BC = np.array([BCx, BCy, BCz])
      AB = AB/np.linalg.norm(AB); BC = BC/np.linalg.norm(BC)
      n = np.cross(AB,BC)
      n = n/np.linalg.norm(n)
      n_cross_bc = np.cross(n,BC)
    
      M = np.zeros((3,3)) # construct a rotation matrix to do what we want
      M[:,0] = BC; M[:,1] = n_cross_bc; M[:,2] = n # fill out the columns of the matrix
      #print "theta:", theta, "phi:", phi
      #print "M:", M
      D2x = length * -math.cos(theta); D2y = length * math.cos(phi)*math.sin(theta); D2z = length * math.sin(phi)*math.sin(theta); # initial placement
      D2 = np.array([D2x,D2y,D2z])
      #print "D2:", D2
      #print "C:", C
      D = np.dot(M,D2) + C # transform back into the proper coordinates
      #print "D:", D
      return D[0], D[1], D[2]
    
    # build minimum-spanning tree for a system class
    def minimum_spanning_tree_of_system(system):
      '''
      Given a system object from the prmtop library, this function finds the minimum sets of angles and dihedrals required
      to describe the internal coordinates of the system. That is, it constructs the members of the z-matrix (though not
      the explicit values in the z-matrix).
      '''
      '''angle_angle_noh_weight = 10.0 # if either angle contains no hydrogen
      angle_angle_h_weight = 20.0 # if either angle contains hydrogen
      angle_dihedral_noh_weight = 100.0 # we prefer that angle_angle terms are used when possible; no hydrogens
      angle_dihedral_noh_weight = 200.0 # we prefer that angle_angle terms are used when possible; hydrogens '''
      angle_angle_weight = 10.0
      angle_dihedral_weight = 100.0
      # first we need to construct the graph
      graph = [] # a list of all nodes
      #edge_dict = {} # a dictionary of edges that each atom will have...
      '''
      print "atom0 dihedrals:"
      i = 0
      for dih in system.atoms[4].dihedrals:
        print "i:", i, "atom1:", dih.atom1.serial, "atom2:", dih.atom2.serial, "atom3:", dih.atom3.serial, "atom4:", dih.atom4.serial
        i += 1
      return
      '''
      for i in range(len(system.atoms)):
        node = [i,[]]
        graph.append(node)
    
      atoms_to_go = [] # all the atoms we have yet to add to the tree
      for i in range(len(system.atoms)): # count through the atoms in the system
        atom = system.atoms[i] # get the atom object
        atoms_to_go.append(i)
        for a1 in range(len(atom.angles)):
          for a2 in range(a1+1, len(atom.angles)): # but we need to include other angles
            # we need a way to keep these arrangements in order: based on a right-handed rule or something
            # for now, leave the angles in whatever order they appeared in the atom's list ALERT: Chirality will be lost in this scheme!
            angle1 = atom.angles[a1]; angle2 = atom.angles[a2]
            if angle1.atom2 == angle2.atom2 and (angle1.atom1 == angle2.atom1 or angle1.atom1 == angle2.atom3 or angle1.atom3 == angle2.atom1 or angle1.atom3 == angle2.atom3):  #and angle1.atom2 != atom and angle2.atom2 != atom: # only if they share the same middle atom, and the atom we are on is not the middle one
              edge = ('angle_angle', (angle1, angle2), i)
              #edges.append(edge)
              for angle_atom in [angle1.atom1, angle1.atom2, angle1.atom3, angle2.atom1, angle2.atom2, angle2.atom3]:
                j = angle_atom.serial
                graph[j][1].append(edge)
    
    
          for dih in range(len(atom.dihedrals)): # all angle-dihedral combinations
            angle1 = atom.angles[a1]; dihedral1 = atom.dihedrals[dih]
            '''
            if dihedral1.atom1.serial == i: # then the previous three atoms are defined as the last 3 atoms of the dihedral
              if (angle1.atom2.serial == dihedral1.atom2.serial and angle1.atom3.serial == dihedral1.atom3.serial) or (angle1.atom2.serial == dihedral1.atom2.serial and angle1.atom1.serial == dihedral1.atom3.serial):
                edge = ('angle_dihedral', (a1, dih), i) # we can always keep this order... because it's enough info to reconstruct what we need
                edges.append(edge)
            elif dihedral1.atom4.serial == i: # then the previous three atoms are defined as the first 3 atoms of the dihedral
              if (angle1.atom2.serial == dihedral1.atom3.serial and angle1.atom3.serial == dihedral1.atom2.serial) or (angle1.atom2.serial == dihedral1.atom3.serial and angle1.atom1.serial == dihedral1.atom2.serial):
                edge = ('angle_dihedral', (a1, dih), i) # we can always keep this order... because it's enough info to reconstruct what we need
                edges.append(edge)
                '''
            if dihedral1.atom2.serial == i: # then the previous three atoms are defined as the last 3 atoms of the dihedral
              if angle1.atom2.serial == i and ((angle1.atom1.serial == dihedral1.atom1.serial and angle1.atom3.serial == dihedral1.atom3.serial) or (angle1.atom3.serial == dihedral1.atom1.serial and angle1.atom1 == dihedral1.atom3.serial)):
                edge = ('angle_dihedral', (angle1, dihedral1), i) # we can always keep this order... because it's enough info to reconstruct what we need
                #edges.append(edge)
                graph[i][1].append(edge)
            elif dihedral1.atom3.serial == i: # then the previous three atoms are defined as the first 3 atoms of the dihedral
              if angle1.atom2.serial == i and ((angle1.atom1.serial == dihedral1.atom4.serial and angle1.atom3 == dihedral1.atom2.serial) or (angle1.atom3.serial == dihedral1.atom4.serial and angle1.atom1.serial == dihedral1.atom2.serial)):
                edge = ('angle_dihedral', (angle1, dihedral1), i) # we can always keep this order... because it's enough info to reconstruct what we need
                #edges.append(edge)
                graph[i][1].append(edge)
    
        #node = [i, edges]
        #edge_dict[i] = len(graph) # the last index of the graph
        #graph[i][1] += edges
      #print "graph:", graph
    
      # then compute the minimum spanning tree
      tree = []
    
      edge_heap = [] #keep track of all currently possible edges
      # get the first atom in the molecule
      first_atom_index = graph[0][0]
      tree.append(('first_atom', first_atom_index, system.atoms[first_atom_index]))
      first_bond = system.atoms[first_atom_index].bonds[0] # find a bond to grow along
      atoms_to_go.remove(first_atom_index) # remove this index because we have explored it
      # based on the first bond, go get the 2nd atom
      if first_bond.atom1.serial == first_atom_index:
        second_atom_index = first_bond.atom2.serial
      else:
        second_atom_index = first_bond.atom1.serial
      atoms_to_go.remove(second_atom_index) # remove this index because we have explored it
      atoms_added = [first_atom_index, second_atom_index] # start with just one bond of the graph
      first_bond_edge = ('first_bond',first_atom_index, second_atom_index, first_bond, )
      tree.append(first_bond_edge)
      # get the 3rd atom based on the bond and angle from first 2 atoms
      #print "bond:", first_bond.print_atoms()
      angles = system.atoms[first_atom_index].angles # an set of angles containing the first atom
      for angle in angles: # for all the angles in this node
        #print "angle:", angle.print_atoms()
        if angle.atom1.serial == first_atom_index:
          if angle.atom2.serial == second_atom_index:
            third_atom_index = angle.atom3.serial
            atoms_to_go.remove(third_atom_index) # remove this atom from atoms_to_go
            atoms_added.append(third_atom_index) # add this atom to our list of areas explored
            break
        elif angle.atom3.serial == first_atom_index:
          if angle.atom2.serial == second_atom_index:
            third_atom_index = angle.atom1.serial
            atoms_to_go.remove(third_atom_index) # remove this atom from atoms_to_go
            atoms_added.append(third_atom_index) # add this atom to our list of areas explored
            break
        elif angle.atom2.serial == first_atom_index:
          if angle.atom1.serial == second_atom_index:
            third_atom_index = angle.atom3.serial
            second_atom_index = angle.atom2.serial
            first_atom_index = angle.atom1.serial
            atoms_to_go.remove(third_atom_index) # remove this atom from atoms_to_go
            atoms_added.append(third_atom_index) # add this atom to our list of areas explored
            break
          elif angle.atom3.serial == second_atom_index:
            third_atom_index = angle.atom1.serial
            second_atom_index = angle.atom2.serial
            first_atom_index = angle.atom3.serial
            atoms_to_go.remove(third_atom_index) # remove this atom from atoms_to_go
            atoms_added.append(third_atom_index) # add this atom to our list of areas explored
            break
    
      first_angle_edge = ('first_angle', third_atom_index, second_atom_index, first_atom_index, angle)
      tree.append(first_angle_edge)
    
      #print "atoms_added:", atoms_added
      #print "atoms_to_go:", atoms_to_go
      #print "edge_dict:", edge_dict
      counter = 0
      #chosen_atom = 2 # chooseing first atom to explore. NOTE: is this OK? do we need to base this decision off of angles covered by this one
    
      atoms_just_added = atoms_added[:] # all the atoms we've just added
    
    
      while atoms_to_go: # iterate limited number of times. Replace this later with a while loop: while atoms_to_go
        #tree.append(just_added)
        for atom_index in atoms_just_added:
          #print "graph[atom_index]:", graph[atom_index]
          for edge in graph[atom_index][1]: # all the edges that we may have just added
            #print "THIS:", edge
            #bad_edge = False
            num_new_atoms1 = 0
            num_new_atoms2 = 0
            if edge[0] == 'angle_angle':
              #angle_index1 = edge[1][0]; angle_index2 = edge[1][1]
              #angle1 = system.atoms[atom_index].angles[angle_index1]
              #angle2 = system.atoms[atom_index].angles[angle_index2]
              angle1 = edge[1][0]; angle2 = edge[1][1]
              #print "new angle-angle"
              new_atom_serial1 = new_atom_serial2 = None
              for serial in [angle1.atom1.serial, angle1.atom2.serial, angle1.atom3.serial]:
                #print "serial:", serial
                if serial not in atoms_added: #then check to see if it's an atom that we are looking at
                  #print "it's not atoms_added"
                  num_new_atoms1 += 1
                  new_atom_serial1 = serial # keep track of this as a possible new atom we are adding
              for serial in [angle2.atom1.serial, angle2.atom2.serial, angle2.atom3.serial]:
                #print "serial:", serial
                if serial not in atoms_added: #then check to see if it's an atom that we are looking at
                  #print "it's not atoms_added"
                  num_new_atoms2 += 1
                  new_atom_serial2 = serial # keep track of this as a possible new atom we are adding
              #print "atoms_added:", atoms_added
              #print "new_atom_serial1:",new_atom_serial1, "new_atom_serial2:", new_atom_serial2, "num_new_atoms1:", num_new_atoms1, "num_new_atoms2:", num_new_atoms2
              if num_new_atoms1 == 1 and num_new_atoms2 == 1 and new_atom_serial1 == new_atom_serial2: # if this edge is proper to be added to our tree
                #print "new_atom_serial1:", new_atom_serial1, " angle1.atom1.serial:", angle1.atom1.serial, " angle1.atom3.serial:", angle1.atom3.serial
                #print "new_atom_serial2:", new_atom_serial2, " angle2.atom1.serial:", angle2.atom1.serial, " angle2.atom3.serial:", angle2.atom3.serial
                if angle1.atom1.serial == new_atom_serial1:
                  prev_atom_index1a = angle1.atom3.serial
                  prev_atom_index2 = angle1.atom2.serial
                elif angle1.atom3.serial == new_atom_serial1:
                  prev_atom_index1a = angle1.atom1.serial
                  prev_atom_index2 = angle1.atom2.serial
                else:
                  continue
                if angle2.atom1.serial == new_atom_serial2:
                  prev_atom_index1b = angle2.atom3.serial
                  prev_atom_index2 = angle2.atom2.serial
                elif angle2.atom3.serial == new_atom_serial2:
                  prev_atom_index1b = angle2.atom1.serial
                  prev_atom_index2 = angle2.atom2.serial
                else:
                  continue
                # NOTE: this requires that a x,y,z coordinates be provided for every atom as a starting guide for the proper molecular topology
                A = np.array([system.atoms[prev_atom_index1a].x, system.atoms[prev_atom_index1a].y, system.atoms[prev_atom_index1a].z]) # location of atom A
                B = np.array([system.atoms[prev_atom_index1b].x, system.atoms[prev_atom_index1b].y, system.atoms[prev_atom_index1b].z])
                C = np.array([system.atoms[prev_atom_index2].x, system.atoms[prev_atom_index2].y, system.atoms[prev_atom_index2].z])
                D = np.array([system.atoms[new_atom_serial1].x, system.atoms[new_atom_serial1].y, system.atoms[new_atom_serial1].z])
                if np.dot(np.cross(A-C, B-C), D-C) > 0.0: # then keep this config
                  new_edge = [angle_angle_weight, new_atom_serial1, prev_atom_index2, prev_atom_index1a, prev_atom_index1b, angle2, angle1,'angle_angle']
                else: # then try the opposite angle arrangement
                  new_edge = [angle_angle_weight, new_atom_serial1, prev_atom_index2, prev_atom_index1b, prev_atom_index1a, angle1, angle2,'angle_angle']
                #print "adding edge:", new_edge
                heappush(edge_heap,new_edge)
            elif edge[0] == 'angle_dihedral':
              angle1 = edge[1][0]; dihedral1 = edge[1][1]
              for serial in [angle1.atom1.serial, angle1.atom2.serial, angle1.atom3.serial]:
                if serial not in atoms_added: #then check to see if it's an atom that we are looking at
                  num_new_atoms1 += 1
                  new_atom_serial1 = serial # keep track of this as a possible new atom we are adding
              for serial in [dihedral1.atom1.serial, dihedral1.atom2.serial, dihedral1.atom3.serial, dihedral1.atom4.serial]:
                if serial not in atoms_added: #then check to see if it's an atom that we are looking at
                  num_new_atoms2 += 1
                  new_atom_serial2 = serial # keep track of this as a possible new atom we are adding
    
              if num_new_atoms1 == 1 and num_new_atoms2 == 1 and new_atom_serial1 == new_atom_serial2: # if this edge is proper to be added to our tree
                if dihedral1.atom1.serial == new_atom_serial2:
                  prev_atom_index1 = dihedral1.atom4.serial
                  prev_atom_index2 = dihedral1.atom3.serial
                  prev_atom_index3 = dihedral1.atom2.serial
                elif dihedral1.atom4.serial == new_atom_serial2:
                  prev_atom_index1 = dihedral1.atom1.serial
                  prev_atom_index2 = dihedral1.atom2.serial
                  prev_atom_index3 = dihedral1.atom3.serial
                else:
                  continue
                new_edge = [angle_dihedral_weight, new_atom_serial1, prev_atom_index3, prev_atom_index2, prev_atom_index1, angle1, dihedral1,'angle_dihedral']
                #print "adding edge:", new_edge
                heappush(edge_heap, new_edge)
    
            else:
              print "unknown z-matrix code:", edge[0]
    
        chosen_atom = atoms_added[0]
        while chosen_atom in atoms_added and len(edge_heap) > 0:
          lowest_edge = heappop(edge_heap) # find the lowest-costing edge to pop off of the edge list
          chosen_atom = lowest_edge[1]
          #print "just popped atom:", chosen_atom
          atoms_just_added = [chosen_atom] # which atom did we choose?
    
        atoms_added.append(chosen_atom)
        atoms_to_go.remove(chosen_atom)
        lowest_edge[0] = lowest_edge.pop() # get the last entry to the edge: the name of the interaction, and put it in the front
        tree.append(lowest_edge)
    
        counter += 1
        #print "counter:", counter
        if counter > MAX_ITER: break
    
      return tree
    
    def find_bond(atom_index1, atom_index2, system):
      'given two atoms and the system, will find a bond that connects the two'
      atom1 = system.atoms[atom_index1]
      atom2 = system.atoms[atom_index2]
      for bond in atom1.bonds: # search thru the bonds in atom 1
        if bond.atom1 == atom1: # we need to look on both sides of the bond (annoying)
          if bond.atom2 == atom2: # if the other side of the bond contains atom 2, return
            return bond
        elif bond.atom2 == atom1: # same as above but opposite side of the bond
          if bond.atom1 == atom2:
            return bond
      #print "atom1.bonds:"
      for bond in atom1.bonds:
        print "  ", bond.atom1.atom_name, bond.atom1.serial, "-", bond.atom2.atom_name, bond.atom2.serial
      raise Exception, "No bond between atom1: %s %d and atom2: %s %d" % (atom1.atom_name, atom1.serial,atom2.atom_name, atom2.serial)
    
    
    def z_matrix_from_tree(tree, system):
      '''Given a tree structure computed for a system from the function "minimum_spanning_tree_of_system" above,
      computes a z-matrix for the given system.'''
      z_matrix = []
    
      for node in tree: # run through the tree, the z-matrix will be in the same order...
        if node[0] == 'first_atom': # add the first atom
          first_atom = node[2]
          #atom_name = first_atom.atom_name # I'm going to break from tradition, and keep track of the serials, not the atomnames
          z_matrix.append([first_atom.serial])
        elif node[0] == 'first_bond':
          first_atom_serial = node[1]; second_atom_serial = node[2]
          first_bond = node[3]
          z_matrix.append([second_atom_serial, first_atom_serial, first_bond.length])
        elif node[0] == 'first_angle':
          first_atom_serial = node[1]; second_atom_serial = node[2]; third_atom_serial = node[3]
          second_bond = find_bond(second_atom_serial, third_atom_serial, system)
          first_angle = node[4]
          line = [first_atom_serial, second_atom_serial, second_bond.length, third_atom_serial, first_angle.angle]
          z_matrix.append(line)
        elif node[0] == 'angle_dihedral':
          atom1_serial = node[1]; atom2_serial = node[2]; atom3_serial = node[3]; atom4_serial = node[4]
          bond = find_bond(atom1_serial, atom2_serial, system)
          angle = node[5]
          dihedral = node[6]
          z_matrix.append([atom1_serial, atom2_serial, bond.length, atom3_serial, angle.angle, atom4_serial, dihedral.phi, 0]) # the zero indicates an angle-dihedral pair
        elif node[0] == 'angle_angle':
          atom1_serial = node[1]; atom2_serial = node[2]; atom3a_serial = node[3]; atom3b_serial = node[4]
          bond = find_bond(atom1_serial, atom2_serial, system)
          angle_a = node[5]
          angle_b = node[6]
          z_matrix.append([atom1_serial, atom2_serial, bond.length, atom3a_serial, angle_a.angle, atom3b_serial, angle_b.angle, 1]) # the one indicates an angle-angle pair
        else:
          print "unknown z-matrix code:", node[0]
    
      return z_matrix
    
    def print_z_matrix(z_matrix, system):
      'given a z_matrix object, will return a string representing a z_matrix'
      counter = 0
      z_matrix_list = []
      for line in z_matrix:
        if len(line) > 4: # converting to degrees
          line[4] *= (180/math.pi)
        if len(line) > 6: # converting to degrees
          line[6] *= (180/math.pi)
        entry = ' '.join([system.atoms[counter].atom_name]+ map(str,line[1:]))
        z_matrix_list.append(entry)
        counter += 1
      return '\n'.join(z_matrix_list)
    
    # follow NERF algorithm for angle-dihedral pairs
    # for angle-angle pairs, use the function above: atoms_from_angles
    def z_matrix_to_cartesian(z_matrix, system):
      'uses the NERF algorithm and the angle-angle pairs function above to calculate the cartesian coordinates of all the atoms'
      # assign the location of the first atom
      first_atom_serial = z_matrix[0][0]
      system.atoms[first_atom_serial].x = 0.0; system.atoms[first_atom_serial].y = 0.0; system.atoms[first_atom_serial].z = 0.0
      # assign the location of the second atom
      first_bond_length = z_matrix[1][2]
      bond_first_atom_serial = z_matrix[1][0] #; second_atom_serial = z_matrix[1][1]
      system.atoms[bond_first_atom_serial].x = 0.0; system.atoms[bond_first_atom_serial].y = 0.0; system.atoms[bond_first_atom_serial].z = first_bond_length
      #print "first bond xyz:", system.atoms[bond_first_atom_serial].x, system.atoms[bond_first_atom_serial].y, system.atoms[bond_first_atom_serial].z
      # assign the location of the third atom
      angle_first_atom_serial = z_matrix[2][0]; angle_second_atom_serial = z_matrix[2][1] #; third_atom_serial = z_matrix[2][3]
      second_bond_length = z_matrix[2][2]; first_angle = z_matrix[2][4]
      if angle_second_atom_serial == bond_first_atom_serial:
        system.atoms[angle_first_atom_serial].x = 0.0; system.atoms[angle_first_atom_serial].y = second_bond_length * math.sin(first_angle); system.atoms[angle_first_atom_serial].z = first_bond_length - second_bond_length * math.cos(first_angle)
      else:
        system.atoms[angle_first_atom_serial].x = 0.0; system.atoms[angle_first_atom_serial].y = second_bond_length * math.sin(first_angle); system.atoms[angle_first_atom_serial].z = second_bond_length * math.cos(first_angle)
    
      counter = 3
      # now for all subsequent entries, they will be pairs of angles, or angle-dihedral
      for line in z_matrix[3:]:
        serial1 = line[0]; serial2 = line[1]; serial3 = line[3]; serial4 = line[5]
        x2 = system.atoms[serial2].x;  y2 = system.atoms[serial2].y;  z2 = system.atoms[serial2].z; # retrieve the positions of the previous atoms
        x3 = system.atoms[serial3].x;  y3 = system.atoms[serial3].y;  z3 = system.atoms[serial3].z;
        x4 = system.atoms[serial4].x;  y4 = system.atoms[serial4].y;  z4 = system.atoms[serial4].z;
        bond_length = line[2]; angle1 = line[4]; angle2 = line[6] # angle2 could be referring to torsion or a 2nd angle
        type_code = line[-1]
        if type_code == 0: # then it's a dihedral, use the NERF algorithm
          system.atoms[serial1].x, system.atoms[serial1].y, system.atoms[serial1].z = NERF(x4,y4,z4,x3,y3,z3,x2,y2,z2, angle1, angle2, bond_length)
        elif type_code == 1: # then its a pair of angles
          system.atoms[serial1].x, system.atoms[serial1].y, system.atoms[serial1].z = atom_from_angles(x4,y4,z4,x3,y3,z3,x2,y2,z2, angle1, angle2, bond_length)
        #print "atom",counter, system.atoms[counter].atom_name, "x:", system.atoms[counter].x, "y:", system.atoms[counter].y, "z:", system.atoms[counter].z
        counter += 1
    
    def count_zmatrix(z_matrix):
      'given a z-matrix, will count and return the number of bonds, angles, and dihedrals'
      num_bonds = 2; num_angles = 1; num_dihedrals = 0
      for line in z_matrix[3:]:
        type_code = line[-1]
        if type_code == 0: # then it's a dihedral
          num_bonds += 1
          num_angles += 1
          num_dihedrals += 1
        elif type_code == 1: # then its two angles
          num_bonds += 1
          num_angles += 2
      return num_bonds, num_angles, num_dihedrals
    
    if __name__=="__main__":
      #Ax = -1.01; Ay = 1.02; Az = 1.03; Bx = 1.1; By = 1.2; Bz = 1.3; Cx = 0; Cy = 0; Cz = 0; theta1 = 90.0; theta2 = 90.0; b = 2.0
      #Ax = 1.0; Ay = 0.0; Az = 0.0; Bx = 0; By = 0; Bz = -1; Cx = 0; Cy = 0; Cz = 0; theta1 = 120*math.pi/180; theta2 = 120*math.pi/180; length = 2.0
      #Ax = 0.0; Ay = 0.0; Az = 0.0; Bx = 0.0; By = 1.027; Bz = 1.454; Cx = 0.0; Cy = 0.0; Cz = 1.090; theta1 = 109.5*math.pi/180; theta2 = 109.5*math.pi/180; length = 1.09
      #x = atom_from_angles(Ax, Ay, Az, Bx, By, Bz, Cx, Cy, Cz, theta1, theta2, length)
      #print "x:", x
    
    
      prmtop_filename = "/scratch/lvotapka/projects/folding/alanine_dipeptide/adi_dry.prmtop"
      inpcrd_filename = "/scratch/lvotapka/projects/folding/alanine_dipeptide/adi_dry.inpcrd"
      #prmtop_filename = "/scratch/lvotapka/projects/folding/trp_cage/trp_cage.prmtop"
      #inpcrd_filename = "/scratch/lvotapka/projects/folding/trp_cage/trp_cage.inpcrd"
      myprmtop = prmtop.read_prmtop(prmtop_filename)
      myprmtop.read_inpcrd(inpcrd_filename)
      myprmtop.cartesian_to_conf()
      tree = minimum_spanning_tree_of_system(myprmtop)
      z_matrix = z_matrix_from_tree(tree, myprmtop)
      #print print_z_matrix(z_matrix, myprmtop)
      z_matrix_to_cartesian(z_matrix, myprmtop)
    
    
      #prmtop.write_pdb(myprmtop, '/scratch/lvotapka/projects/folding/trp_cage/trp_cage_rewrite.pdb')
      prmtop.write_pdb(myprmtop, '/scratch/lvotapka/projects/folding/alanine_dipeptide/adi_dry_rewrite.pdb')
      #print "tree:", tree
    
    
    

`
