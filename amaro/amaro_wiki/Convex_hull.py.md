# Convex hull.py

`
    
    
    
    import numpy as np
    from math import atan2
    import random
    
    # convex hull
    
    def find_min(points):
      min_point = points[0]
      min_index = 0
      for i in range(len(points)):
        if points[i][0] < min_point[0]:
          min_point = points[i]
          min_index = i
      return min_index, min_point
      
    def find_max(points):
      max_point = points[0]
      max_index = 0
      for i in range(len(points)):
        if points[i][0] > max_point[0]:
          max_point = points[i]
          max_index = i
      return max_index, max_point
    
    def search_for_tangent(refpoint, startindex, points, direc):
      '''
      given a "refpoint": a point of reference, will search in the direction "direc" along a clockwise ordered set of 
      "points" starting from "startindex", until the angle goes around a corner, (reverses). This gives us the tangent point
      between "refpoint" and the set of points. If this function is called iteratively from two sets of points, eventually
      the extreme tangents will be found.
      
      In the 3d case, it will convert to the 2d case in the xy plane
      '''
      counter = 0
      maxiter = 20000
      exit_outta_here = False
      other_stuck = True
      refpoint = np.array(refpoint[0:2])
      i = startindex
      curpoint = np.array(points[i][0:2])
      curindex = i
      #print "curindex:", curindex, "curpoint:", curpoint, "refpoint:", refpoint
      while not exit_outta_here:
        i += direc # move along the hull
        i = i % len(points)
        counter += 1
        if counter > maxiter: 
          print "infinite loop error"
          break
        nextpoint = np.array(points[i][0:2])
        oldvec = curpoint - refpoint
        newvec = nextpoint - refpoint
        cross = np.cross(oldvec, newvec)
        #print "i:", i, "curpoint:", curpoint, "nextpoint:", nextpoint, "oldvec:", oldvec, "newvec:", newvec, "cross:", cross
        if cross * direc > 0: # then we are moving there next
          curpoint = nextpoint
          curindex = i
          other_stuck = False
          
        else: # then the current point is the last point
          exit_outta_here = True
          return curindex, other_stuck
    
    def circular_list(our_list, index1, index2):
      '''A convenient function to circle around to the beginning of a list if the indeces go out of bounds'''
      if index1 < index2: # simple
        return our_list[index1:index2]
      else: # then we need to get the two pieces and splice them
        return our_list[index2:] + our_list[:index1]
    
    
    def divide_and_conquer_2d (points):
      if len(points) <= 2: # base case
        return points # this is part of the convex hull
        
      if len(points) == 3: # another base case, but needs to be sorted by clockwise order
        vec1 = (points[1][1] - points[0][1], points[1][0] - points[0][0]) # NOTE: these are backwards vectors! (Y,X)
        vec2 = (points[2][1] - points[0][1], points[2][0] - points[0][0]) # this will be from the leftmost point to the others
        if atan2(*vec1) > atan2(*vec2): # then the angle to vec1 is larger than the angle to vec2
          return(points)
        else:
          return([points[0],points[2],points[1]])
          
      
      else: # recursive case
        halflen = len(points)/2
        leftpoints = points[:halflen]
        rightpoints = points[halflen:]
        #print "leftpoints:", leftpoints
        #print "rightpoints:", rightpoints
        lefthull = divide_and_conquer_2d(leftpoints) # left half, in clockwise order
        righthull = divide_and_conquer_2d(rightpoints)  #right half, in clockwise order
        #print "lefthull:", lefthull
        #print "righthull:", righthull
        # this gets the rightmost point in the left hull, and the leftmost point in the right hull
        closest_index_left, closest_point_left = find_max(lefthull)
        closest_index_right, closest_point_right = find_min(righthull)
        #print "closest_index_left:", closest_index_left
        #print "closest_index_right:", closest_index_right
        
        left_stuck = right_stuck = False
        lefti = closest_index_left
        righti = closest_index_right
        counter = 0
        maxiter = 20000
        # this finds the upper tangent
        while left_stuck == False or right_stuck == False:
          counter += 1
          if counter > maxiter: 
            print "infinite loop error"
            break
          lefti, right_stuck = search_for_tangent(righthull[righti], lefti, lefthull, 1) # the left side
          left_stuck = True
          righti, left_stuck = search_for_tangent(lefthull[lefti], righti, righthull, -1) # the right side
          right_stuck = True
          
        lower_lefti = lefti
        lower_righti = righti
        
        print "Find upper tangent"
        # this finds the lower tangent
        counter = 0
        left_stuck = right_stuck = False
        lefti = closest_index_left
        righti = closest_index_right
    
        while left_stuck == False or right_stuck == False:
          counter += 1
          if counter > maxiter: 
            print "infinite loop error"
            break
          lefti, right_stuck = search_for_tangent(righthull[righti], lefti, lefthull, -1) # the left side
          left_stuck = True
          righti, left_stuck = search_for_tangent(lefthull[lefti], righti, righthull, 1) # the right side
          right_stuck = True
          
        upper_lefti = lefti
        upper_righti = righti
        
        #print "upper_lefti", upper_lefti
        #print "upper_righti", upper_righti
        #print "lower_lefti", lower_lefti
        #print "lower_righti", lower_righti
        
        # the convex hull consists of the indeces: lefthull[lower_lefti : upper_lefti] and righthull[upper_righti : lower_righti]
        
        total_hull = circular_list(lefthull, lower_lefti, upper_lefti+1) + circular_list(righthull, upper_righti, lower_righti+1)
        return total_hull
    
    
    ######################################################################################################################
    ## 3D
    ######################################################################################################################
    def array_list_search(query_array, our_list, remove=True):
      '''given a query array, will search our_list (a list of arrays) and optionally remove the value if it exists'''
      n = len(our_list)
      for i in range(n):
        this_array = our_list[i]
        if (this_array[0].all() == query_array[0].all()) and (this_array[1].all() == query_array[1].all()):
          if remove:
            our_list.pop(i) # remove this index from the list
          return True
          
      return False
    
    
    def gift_wrapping_3d (raw_points):
      '''gift wrapping for 3d convex hull'''
      n = len(raw_points)
      point1 = np.array(raw_points[0])
      xaxis = np.array([1,0,0])
      maxx = raw_points[0][0]
      points = []
      done_seg_dict = {} # a dictionary that allows for quick & easy lookup of segments
      for i in range(n): # find the n with the largest x value
        points.append(np.array(raw_points[i]))
        done_seg_dict[tuple(points[i])] = []
        if points[i][0] > maxx:
          maxx = points[i][0]
          point1 = points[i]
      print "points:", points
      
      print "point with greatest x value:", tuple(point1)
      
      best_dot = -1.0
      next_point = None
      for i in range(n):
        diff_vec = points[i]-point1
        diff_len = np.linalg.norm(diff_vec)
        #print "vector pointing from", endpoint, "to", points[i], ":", diff_vec, ',', diff_len
        test_dot = np.dot(diff_vec/diff_len,xaxis)
        #print "dot:", test_dot
        if test_dot > best_dot:
          best_dot = test_dot
          point2 = points[i]
          
      print "starting segment:", point1, point2
      ref_vec = xaxis
      # now find the best triangle
      triangles = []
      
      seg_list = set([(tuple(point1), tuple(point2)),])
      norm_dict = {tuple(point1):xaxis}
      
      max_iter = 200
      counter = 0
      first_time = True
      
      while seg_list:
        print "seg_list:", seg_list
        counter += 1
        if counter > max_iter:
          raise Exception, "max_iter error"
        
        seg = seg_list.pop() # take something out of the seg_list
        point1 = np.array(seg[0])
        point2 = np.array(seg[1])
        print "norm_dict:", norm_dict
        ref_vec = norm_dict[tuple(point1)]
        print "ref_vec:", ref_vec
        #del norm_dict[tuple(point1)]
         # then this segment has already been tried, get outta here
        
        best_dot_cross = -1.0
        best_point = None
        for i in range(n): # look at each point
          #print "points[i]:", points[i]
          #print "point1:", point1
          #print "point2:", point2
          if (points[i] == point1).all() or (points[i] == point2).all(): continue
          diff_vec1 = points[i]-point1
          diff_len1 = np.linalg.norm(diff_vec1)
          diff_vec2 = point2 - point1
          diff_len2 = np.linalg.norm(diff_vec2)
        
          test_cross = np.cross(diff_vec1/diff_len1,diff_vec2/diff_len2)
          test_cross_len = np.linalg.norm(test_cross)
          test_cross = test_cross / test_cross_len
          print "test_cross for point", points[i], ":", test_cross
          dot_cross = np.dot(test_cross, ref_vec)
          if dot_cross > best_dot_cross:
            best_cross = test_cross
            best_dot_cross = dot_cross
            best_point = points[i]
          
        point3 = best_point
        
        #if 
        print "triangle points:", point1, point2, point3
        print "done_seg_dict", done_seg_dict
        if (tuple(point2) not in done_seg_dict) or (tuple(point1) not in done_seg_dict[tuple(point2)]):
          print "adding segments:", point2, "to", point1
          seg_list.add((tuple(point2),tuple(point1)))
          norm_dict[tuple(point2)] = best_cross/np.linalg.norm(best_cross)
        #elif not first_time:
          #array_list_search([point2,point1], seg_list, remove=False)
          
        if (tuple(point3) not in done_seg_dict) or (tuple(point2) not in done_seg_dict[tuple(point3)]):
          print "adding segments:", point3, "to", point2
          seg_list.add((tuple(point3),tuple(point2))) # append these three segments to the list
          norm_dict[tuple(point3)] = best_cross/np.linalg.norm(best_cross)
        #elif not first_time:
          #array_list_search([point3,point2], seg_list, remove=False)
          
        if (tuple(point1) not in done_seg_dict) or (tuple(point3) not in done_seg_dict[tuple(point1)]):
          print "adding segments:", point1, "to", point3
          seg_list.add((tuple(point1),tuple(point3)))
          norm_dict[tuple(point1)] = best_cross/np.linalg.norm(best_cross)
        #elif not first_time:
          #array_list_search([point1,point3], seg_list, remove=False)
        
        
        print "marking segment", point2, "to", point1, "as already done"
        done_seg_dict[tuple(point1)].append(tuple(point2))
        done_seg_dict[tuple(point2)].append(tuple(point3))
        done_seg_dict[tuple(point3)].append(tuple(point1))
        
        triangles.append((point1, point2, point3))
        first_time = False
        print "="*25
      
      for point in points:
        print "draw sphere {", point[0], point[1], point[2], "} radius 0.1"
      
      print "triangles:", triangles
      for triangle in triangles:
        print "draw triangle {",triangle[0][0],triangle[0][1],triangle[0][2],"} {",triangle[1][0],triangle[1][1],triangle[1][2],"} {",triangle[2][0],triangle[2][1],triangle[2][2],"}; display update ui; display update; sleep 3"
      return triangles
    
    def outside_hull(our_point, triangles):
      '''given the hull as defined by a list of triangles, will return whether a point is within these or not'''
      our_point = np.array(our_point) # convert it to an array
      #within = False
      for triangle in triangles:
        #triangle = np.array(triangle)
        rel_point = our_point - np.array(triangle[0]) # vector from triangle corner to point
        vec1 = np.array(triangle[1]) - np.array(triangle[0])
        vec2 = np.array(triangle[2]) - np.array(triangle[1])
        print "vec1:", vec1
        print "vec2:", vec2
        our_cross = np.cross(vec1, vec2)
        if np.dot(rel_point,our_cross) > 0.0: # then its outside
          return True
          
      return False
    
    def test_gift_wrap_3d(n):
      '''test the 3D gift-wrap implementation'''
      points = []
      for i in range(n):
        points.append([random.random(),random.random(),random.random()])
      
      triangles = gift_wrapping_3d(points)
      
      for point in points:
        outside = outside_hull(point,triangles)
        if outside == False:
          raise Exception, "Found a point outside of the hull!:", point
          
      print "All is well..."
    
    def divide_and_conquer_3d (points): 
      if len(points) <= 4: # base case
        return points # this is part of the convex hull
    
      else: # recursive case
        halflen = len(points)/2
        leftpoints = points[:halflen]
        rightpoints = points[halflen:]
        
        lefthull = divide_and_conquer_3d(leftpoints) # left half, in clockwise order
        righthull = divide_and_conquer_3d(rightpoints)  #right half, in clockwise order
        
        # this gets the rightmost point in the left hull, and the leftmost point in the right hull
        closest_index_left, closest_point_left = find_max(lefthull)
        closest_index_right, closest_point_right = find_min(righthull)
        
        # we need to find the first bridge that connects the two hulls; this phase is identical to the 2D case
        left_stuck = right_stuck = False
        lefti = closest_index_left
        righti = closest_index_right
        counter = 0
        maxiter = 20000
        # this finds the upper tangent
        while left_stuck == False or right_stuck == False:
          counter += 1
          if counter > maxiter: 
            print "infinite loop error"
            break
          lefti, right_stuck = search_for_tangent(righthull[righti], lefti, lefthull, 1) # the left side
          left_stuck = True
          righti, left_stuck = search_for_tangent(lefthull[lefti], righti, righthull, -1) # the right side
          right_stuck = True
          
        lower_lefti = lefti
        lower_righti = righti
        
        # we now have a bridge connecting the two hulls
        
    class Point():
      def __init__(self, x, y, z, prev, next):
        self.x = x; self.y = y; self.z = z
        
        # we need to keep track of adjacent members within the point list
        self.next = next
        self.prev = prev
        
      def act(self):
        if self.prev.next != self:
          self.prev.next = self.next.prev = self # insert self
        else:
          self.prev.next = self.next
          self.next.prev = self.prev # delete self from linked list
          
      def display(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)
    
    INF = 1e99
    nil = Point(INF, INF, INF, 0, 0)
    NIL = nil # pointer to nil (??)
    
    def turn(p,q,r):
      if (p == nil or q == nil or r == nil): return 1.0
      #print "p:", p.x, p.y, p.z
      #print "q:", q.x, q.y, q.z
      #print "r:", r.x, r.y, r.z
      return (q.x-p.x)*(r.y-p.y) - (r.x-p.x)*(q.y-p.y)
      
    def time(p, q, r): # when turn changes
      if (p == nil or q == nil or r == nil): return INF
      return ((q.x-p.x) * (r.z-p.z) - (r.x-p.x)*(q.z-p.z)) / turn(p,q,r)
    
    def chan_hull( point_list, n, A, B ): # Chan's Algorithm
      # define a bunch of variables
      
      if n==1:
        A[0] = point_list[0].prev = point_list[0].next = nil
        print "A:"
        for a in A: print a.display()
        print "================ returning ==================="
        return A, point_list
      
      u = point_list[0]
      mid = v = point_list[n/2]
      leftB, left_point_list = chan_hull(point_list[0:n/2], n/2, B[0:n/2*2], A[0:n/2*2]) # recurse on the left and right sides
      rightB, right_point_list = chan_hull(point_list[n/2:], n - n/2, B[n/2*2:], A[n/2*2:])
      B = leftB + rightB
      point_list = left_point_list + right_point_list
      
      print "B:"
      for b in B: print b.display()
      
      counter = 0
      max_iter = 200
      while 1: # find initial bridge
        counter += 1 
        if counter > max_iter:
          raise Exception,  "Max_iter Error"
        if turn(u,v,v.next) < 0:
          v = v.next # then move to the next v
        elif turn(u.prev,u,v) < 0:
          u = u.prev # then move to the previous u
        else:
          break
      # u and v are the points that make the initial bridge
      
      print "u:", u.display()
      print "v:", v.display()
      
      # merge by tracking bridge uv over time
      i = k = 0
      j = n/2*2
      oldt = -INF
      while 1:
        t = range(6)
        t[0] = time(B[i].prev, B[i], B[i].next)
        t[1] = time(B[j].prev, B[j], B[j].next)
        t[2] = time(u, u.next, v)			# the six pointers
        t[3] = time(u.prev, u, v)
        t[4] = time(u, v.prev, v)
        t[5] = time(u, v, v.next)
        
        newt = INF
        for ell in range(6):
          if t[ell] > oldt and t[ell] < newt:
            minl = ell
            newt = t[ell]
        if newt == INF: break
        
        print "minl", minl
        
        if minl == 0:
          if B[i].x < u.x: 
            A[k] = B[i]
            k += 1
          B[i].act()
          i += 1
          #break
          
        if minl == 1:
          if B[j].x < v.x: 
            A[k] = B[j]
            k += 1
          B[j].act()
          j += 1
          #break
          
        if minl == 2:
          A[k] = u = u.next
          k += 1
          #break
          
        if minl == 3:
          A[k] = u
          u = u.prev
          k += 1
          #break
          
        if minl == 4:
          A[k] = v = v.prev
          k += 1
          #break
          
        if minl == 5:
          A[k] = v
          v = v.next
          k += 1
          #break
          
        oldt = newt
    
      A[k] = nil
      
      u.next = v
      v.prev = u # go back in time to update pointers
      k_ = k
      for k in range(k_-1, -1, -1): # ranging from k down to zero
        if A[k].x <= u.x or A[k].x >= v.x:
          A[k].act()
          if A[k] == u: 
            u = u.prev
          elif A[k] == v:
            v = v.next
        else:
          u.next = A[k]
          A[k].prev = u
          v.prev = A[k]
          A[k].next = v
          if A[k].x < mid.x:
            u = A[k]
          else:
            v = A[k]
      
      print "A:"
      for a in A: print a.display()
      print "================ returning ==================="
      
      return A, point_list
    
    # main section
    
    n = 6 # the number of points
    test_points = [[1.0,0.0,0.0],[0.05,0.0,0.05],[0.0,1.0,0.0],[0.0,0.0,1.0], [0.15,0.01,0.0], [0.1, 0.2,0.1],[-2.0,-2.0,-2.0]]
    
    sorted_points = sorted(test_points, key=lambda point: point[0])
    P = []
    A = []
    B = []
    #sort the points
    
    i = 0
    max_i = len(sorted_points)
    for point in sorted_points:
      x = point[0]
      y = point[1]
      z = point[2]
      if i == 0:
        me = Point(x,y,z, None, None)
        P.append(me)
      elif i == max_i-1:
        me = Point(x,y,z, P[-1], None)
        P.append(me)
        P[-2].next = me
      else:
        me = Point(x,y,z, P[-1], None)
        P.append(me)
        P[-2].next = me
        
      A.append(Point(0, 0, 0, None, None)); A.append(Point(0, 0, 0, None, None)) # construct the A and B lists
      B.append(Point(0, 0, 0, None, None)); B.append(Point(0, 0, 0, None, None))
      i += 1
      
    
    hull_list, point_list = chan_hull(P,n,A,B)
    
    i=0
    max_iter = 200
    while hull_list[i] != nil:
      if i > max_iter:
        raise Exception, "max iter error"
      
      print "hull point:", hull_list[i].prev.display(), ',' , hull_list[i].display(), ',' , hull_list[i].next.display()
      i += 1
      hull_list[i].act
    
    
    
    
    '''
    
    test_points = [[-10.0,0.0],[0.0,10.0],[1.0,0.0], [-1.0,1.0],[-2.0,1.0],[-3.0,2.0]]
    test_points2 = [[0,0],[1,10],[2,20],[10,0],[11,10],[12,20],[20,0],[21,10], [22,20], [15,-200]]
    
    #print "graham scan:", graham_scan_2d(test_points_ed)
    sorted_test = sorted(test_points2, key=lambda point: point[0])
    
    # test search_for_tangent
    #points = [(0,0),(0.5,1), (1,1.5),(3,0),(2,-1),]
    #highest, refstuck = search_for_tangent((5,0), 3, points, -1)
    #print "highest:", highest
    #print "refstuck:", refstuck
    
    hull = divide_and_conquer_2d(sorted_test)
    print "hull:", hull
    
    
    '''
    test_points = [[1,0,0],[-0.05,-0.4,0],[0,1,0],[0,0,1], [-0.1,0,0.5], [0.1, 0.1,0.1]]
    
    
    

`
