# Povme plus.py

`
    
    
    
    """This script uses rolling probes over a protein surface to find the surface atoms
    of a structure
    
    """
    import numpy as np
    from copy import deepcopy
    from math import sqrt, acos, asin, atan2
    
    def _find_first_point(points, first_point_vec):
      '''finds the point furthest in the direction of arg "first_point_vec" and returns the index'''
      n = len(points)
      endpoint = None
      best_dot = -99999999.9
      for i in range(n):
        cur_dot = np.dot(first_point_vec, points[i]) #get the dot product in the direction of the first_point_vec
        if cur_dot > best_dot: # then we've found a better point
          endpoint = i
          best_dot = cur_dot
    
      assert endpoint != None, "no point found along first_point_vec... possibly because the initial best_dot value is not low enough"
      return endpoint
    
    def _find_best_triangle(points, segment, norm_vec):
      '''finds the best point among a list that makes a triangle of the hull'''
      n = len(points)
      norm_vec = norm_vec / np.linalg.norm(norm_vec) # just in case its not normalized
      endpoint = None # the best point we have come up with so far
      best_dot = -1.0
      seg_vec = points[segment[1]] - points[segment[0]] # vec_seg: the vector that points from one segment to another
      for i in range(n): # for each point
        if i in segment: continue # if any of the points are already in the segment, then skip them
        cur_vec = points[i] - points[segment[0]] # cur_vec: points from 0th end of the segment to point i
        cross_vec = np.cross(seg_vec, cur_vec) # get cross product between segment vector and currently testing vector
        cross_vec_norm = cross_vec / np.linalg.norm(cross_vec) # normalize the cross product
        cur_dot = np.dot(norm_vec, cross_vec_norm) # dot the cross product with the norm_vec
        if cur_dot > best_dot: # if we find a dot product that's more positive, then use that one
          endpoint = i
          best_dot = cur_dot
    
      if endpoint == None: raise Exception, "no points found to construct triangle" # if nothing was every found better than the default
      triangle = list(segment) + [endpoint] # concatenate the segment list to the best endpoint => best hull triangle
      return triangle
        
    def _triangle_to_segments(triangle):
      '''makes a 3-tuple into a list of 3 segments arranged in a standard order (all clockwise/ counterclockwise)'''
      # assuming that the triangle was composed of points in order...
      seg0 = tuple(triangle[0:2]) # elements 0 -> 1, the original segment
      seg1 = tuple(triangle[1:]) # elements 1 -> 2,
      seg2 = tuple([triangle[-1]] + [triangle[0]]) # elements 2 -> 0
      return [seg0, seg1, seg2]
      
    
    def find_convex_hull (points, method="gift_wrapping"):
      '''finds the convex hull of a set of n points'''
      n = len(points)
      assert n >= 4, "the number of points must be greater than or equal to 4" # otherwise none of this will work
      first_point_vec=np.array([1,0,0]) # the vector direction in which to search for the furthest point, which is the first_point
      #remaining_points = deepcopy(points) # list of all points that are not in outer_points
      #outer_points = [] # a list of all points that are considered on the outside
      first_point = _find_first_point(points, first_point_vec=first_point_vec) # index of the first point
      print "first_point:", first_point
      #outer_points.append[first_point]
      #remaining_points.remove(first_point)
      remaining_segments = [] # a list of segments that need a point found for them
      triangles = []
      if method=="gift_wrapping": # Order(nh)
        # given the first point, must find another point on the hull to make the first segment: O(n)
        endpoint = None
        best_dot = -1.0
        for i in range(n): # search for another point to find its angle relative to the first_point_vec to make the first segment
          if i == first_point: continue # skip this point if its the first_point
          rel_vec_norm = points[i] - points[first_point] # get the relative vector (not normalized yet)
          rel_vec_norm = rel_vec_norm / np.linalg.norm(rel_vec_norm) # normalize the vector
          cur_dot = np.dot(first_point_vec, rel_vec_norm)
          print "dot for point %d:%s" % (i,cur_dot)
          if cur_dot > best_dot: # then we have found a point with a better angle
            endpoint = i
            best_dot = cur_dot      
    
        if endpoint == None: raise Exception, "no points found to construct first segment"
        first_segment = (first_point,endpoint)
        print "first_segment:", first_segment
        # given the first segment, must now find the first triangle, each side remains as a segment
        triangle = _find_best_triangle(points, first_segment, first_point_vec)
        remaining_segments = _triangle_to_segments(triangle) # get the segments from the triangle
        triangles.append(triangle)
        print "remaining_segments:", remaining_segments
        print "triangle:", triangle
        # now for each segment remaining, pop it, reverse it, and find a new triangle with it as one side, the other sides of which must become more segments
        for i in range(n): # this should only have to happen less than n times
          if len(remaining_segments) == 0: break # then we're finished
          print "remaining_segments:", remaining_segments
          rev_cur_seg = remaining_segments[0] # choose one of the segments
          cur_seg = rev_cur_seg[::-1] # must reverse the segment, otherwise we would be getting redundant answers
          point_vec = points[cur_seg[0]] # use one member of the segment to be a reference vector
          new_triangle = _find_best_triangle(points, cur_seg, point_vec) # find a good triangle from this segment
          new_segments = _triangle_to_segments(new_triangle) # get all the segments from this triangle
          triangles.append(new_triangle)
          # if any of the segments are shared with currently existing triangles, then don't append to remaining_segments, and remove them from remaining_segments
          for seg in new_segments:
            print "seg:",seg, "  seg[::-1]:", seg[::-1]
            if seg[::-1] in remaining_segments:
              print "removing segment:", seg, "because it was found in the list remaining_segments"
              remaining_segments.remove(seg[::-1]) # we have to reverse it for it to be meaningful
            else: # otherwise, append to the list, we will want these for later
              print "adding segment:", seg
              remaining_segments.append(seg)
          print "="*25
    
        if method == "divide_and_conquer": # Order(n log(n))
          pass # not yet implemented
          
      return triangles # at the end, return the triangles generated
    
    
    def graham_recursion(points, remaining_indeces, hull, cur_two_points):
      '''the recursive function that allows the gram scan to work'''
      if len(remaining_indeces) == 0: # then we've found the entire convex hull
        print "found convex hull!"
        return hull
      
      else:
        first_index = cur_two_points[0]
        second_index = cur_two_points[1]
        (x1, y1) = points[first_index]
        (x2, y2) = points[second_index]
        maxiter = 200
        counter = 0
        
        while len(remaining_indeces) > 0 and counter < maxiter:
          print "remaining_indeces",remaining_indeces
        #for third_index in remaining_indeces:
          third_index = remaining_indeces[0]
          print "trying index", third_index
          (x3, y3) = points[third_index]
          turn = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
          print "trying the angle between", first_index, "and", second_index, "and", third_index 
          if turn <= 0.0: # then its a right turn, the second to last point is not part of the hull
            print "ouch! right turn: get rid of index", hull[-1]
            print "==============================================================================================="
            hull.pop()
            return False
            
          else: #elif turn > 0.0: # then its a left turn
            popped=remaining_indeces.pop(0) # because we are going to remove it from future consideration; its either in the hull or not
            print "good, left turn. Removing point", popped, "and adding it to the hull"
            hull.append(third_index)
            print "================================================================================================"
            result = graham_recursion(points, remaining_indeces, hull, (second_index, third_index))
            if result == False: # then we took a wrong turn previously, try another point
              continue
            else: # then its returned the convex hull and our process is complete
              return hull
          #else: # then its colinear
          counter += 1
            
        
    
    def graham_scan_2d(points):
      '''given a list of 2d points, will perform a Graham scan to determine the convex hull'''
      # first, find P, the value with the lowest y value
      n = len(points)
      P = (99999999.9, 99999999.9)
      lowest_index = -1
      for i in xrange(n):
        if points[i][1] < P[1]: # then we've found a lower p value
          P = points[i]
          lowest_index = i
        if points[i][1] == P[1]: # then take the one with the lowest x value
          if points[i][0] < P[0]:
            P = points[i]
            lowest_index = i
      
      #points.pop(lowest_index) # remove P from the list    
      p_index = lowest_index
      print "lowest point:", P
      # P is now the point with the lowest y-value
      # now find the angle between P and every point
      angles = []
      for i in xrange(n):
        if i == p_index: continue # skip if its the same index as P
        P_to_i = (points[i][0]-P[0], points[i][1]-P[1])
        P_to_i_length = sqrt((points[i][0]-P[0])**2 + (points[i][1]-P[1])**2)
        P_to_i_normalized = (P_to_i[0]/P_to_i_length, P_to_i[1]/P_to_i_length)
        angle = atan2(P_to_i_normalized[1], P_to_i_normalized[0]) 
        angles.append((angle,i)) # need to include the angle as well as the index of the point
        
      angles_sorted = sorted(angles, key=lambda angle_tuple: angle_tuple[0]) # sort by angle
      remaining_indeces = []
      for angle_point in angles_sorted:
        remaining_indeces.append(angle_point[1])
      
      print "remaining_indeces", remaining_indeces
      
      #hull_list = [p_index, angles_sorted[-1]]
      first_two_indeces = (p_index, remaining_indeces[0])
      remaining_indeces.pop(0)
      hull = list(first_two_indeces)
      final_hull = graham_recursion(points, remaining_indeces, hull, first_two_indeces)
      print "final hull:", final_hull 
      
    def divide_and_conquer_2d(points, side='left'):
      print "side:", side, "points:", points
      # base case
      if len(points) == 3:
        # first, need to construct the order clockwise
        if side == 'right': 
          vec1 = (points[1][1] - points[0][1], points[1][0] - points[0][0]) # NOTE: these are backwards vectors! (Y,X)
          vec2 = (points[2][1] - points[0][1], points[2][0] - points[0][0]) # vectors from the leftmost point to the others
          if atan2(*vec1) > atan2(*vec2):
            clockwise = [0,1,2]
          else:
            clockwise = [0,2,1]
            
        elif side == 'left':
          vec1 = (points[2][1] - points[0][1], points[2][0] - points[0][0]) # NOTE: these are backwards vectors! (Y,X)
          vec2 = (points[2][1] - points[1][1], points[2][0] - points[1][0]) # vectors from the rightmost point to the others
          if atan2(*vec1) < atan2(*vec2):
            clockwise = [2,1,0]
          else:
            clockwise = [2,0,1]
        
        return points, clockwise
        
      elif len(points) <= 2:
        # then its the base case
        if side == 'right': return points[:], range(len(points[:]))
        if side == 'left': return points[::-1], range(len(points[::-1]))
    
      else: 
        # first divide the points into 2 equal parts
        
        halflen = len(points)/2
        hull1, hull1_index_clockwise = divide_and_conquer_2d(points[:halflen], 'left') # left half
        hull2, hull2_index_clockwise = divide_and_conquer_2d(points[halflen:], 'right')  #right half
        #new_hull = hull1 + hull2
        #new_hull_clockwise = hull1_index_clockwise + hull2_index_clockwise
        to_remove = set()
        
        # now merge the two hulls
        # first start by choosing the closest two points
        print "hull1:", hull1, "hull1_indeces:", hull1_index_clockwise 
        print "hull2:", hull2, "hull2_indeces:", hull2_index_clockwise 
        bridges = []
        for updown in [1, -1]: # to find the upper and lower bridging lines to merge the groups
          if updown == 1: print "Searching for the upper bridge"
          if updown == -1: print "Searching for the lower bridge"
          index1 = hull1_index_clockwise[0]
          index2 = hull2_index_clockwise[0]
          point1 = np.array(hull1[index1]) # the rightmost point in the left set
          point2 = np.array(hull2[index2])  # the leftmost point in the right set
        
        
          maxiter = 1000
          counter = 0
        
        
          left_stuck = right_stuck = False
          trying = 'left'
          lefti = 0
          righti = 0
        
          while left_stuck == False or right_stuck == False:
            print '============================================================================'
            print "trying:", trying
            counter += 1
            if trying == 'left':
              curpoint = point1
              curindex = index1
              refpoint = point2
              curhull = hull1
              curhull_clockwise = hull1_index_clockwise
              direc = -1 * updown
              i = lefti + 1
              
            elif trying == 'right':
              curpoint = point2
              curindex = index2
              refpoint = point1
              curhull = hull2
              curhull_clockwise = hull2_index_clockwise
              direc = 1 * updown
              i = righti + 1
              
            
            print "starting this round at points:", refpoint, curpoint
            exit_outta_here = False
            while not exit_outta_here:
              i = i % len(curhull)
              counter += 1
              if counter > maxiter: 
                print "infinite loop error"
                break
              nextindex = curhull_clockwise[i*direc]
              nextpoint = np.array(curhull[nextindex])
              print "trying nextpoint:", nextpoint, 'nextindex', nextindex
              print "refpoint:", refpoint
              oldvec = curpoint - refpoint
              newvec = nextpoint - refpoint
              print "oldvec:", oldvec, 'newvec', newvec
              cross = np.cross(oldvec, newvec)
              print "cross:", cross
              if (trying == 'right' and updown * cross > 0) or (trying == 'left' and updown * cross < 0): # if the angle from curpoint to the nextpoint is positive, then we can keep searching; we're not stuck
                print "newvec:", newvec, "has a higher angle than", oldvec, "so we are moving there next"
                
                curpoint = nextpoint
                curindex = nextindex
                if trying == 'left': right_stuck = False
                if trying == 'right': left_stuck = False
              else:
                print "curpoint:", curpoint, "is the best point of the", trying, 'side.'
                print "breaking out of the", trying, 'side'
                if trying == 'left': 
                  
                  point1 = curpoint
                  index1 = curindex
                  left_stuck = True
                  
                  trying = 'right'
                  lefti = i
                elif trying == 'right':
                  point2 = curpoint 
                  index2 = curindex
                  right_stuck = True
                  
                  trying = 'left'
                  righti = i
                
                exit_outta_here = True
              i += 1
              
            print "left_stuck:", left_stuck, 'right_stuck', right_stuck
          bridges.append([point1,point2])
          
        print "bridges:", bridges
        
        
        all_points = hull1 + hull2
        all_point_clockwise = hull1_index_clockwise
        increment = len(hull1)
        for i in hull2_index_clockwise:
          all_point_clockwise.append(i + increment)
        
        final_hull = []
        final_hull_clockwise = []
        extreme_index = 0
        extreme_point = all_points[all_point_clockwise[0]]
        
        
        for i in range(len(all_points)):
          if side == 'left': # should find the greatest x-value
            index = all_point_clockwise[i]
            point = all_points[index]
            if point[0] > extreme_point[0]:
              extreme_index = i
              extreme_point = point
          if side == 'right': # should find the least x-value
            index = all_point_clockwise[i]
            point = all_points[index]
            if point[0] < extreme_point[0]:
              extreme_index = i
              extreme_point = point
              
        all_point_clockwise = all_point_clockwise[extreme_index:] + all_point_clockwise[:extreme_index]
        
        
        for i in range(len(all_points)):
          testindex = all_point_clockwise[i]
          testpoint = np.array(all_points[testindex])
          print "now testing index:", testindex, "point:", testpoint
          cross1 = np.cross(bridges[0][1] - bridges[0][0],testpoint - bridges[0][0])
          cross2 = np.cross(bridges[1][0] - bridges[0][0],testpoint - bridges[0][0])
          cross3 = np.cross(bridges[1][0] - bridges[1][1],testpoint - bridges[1][1])
          cross4 = np.cross(bridges[0][1] - bridges[1][1],testpoint - bridges[1][1])
          print "crosses:", cross1, cross2, cross3, cross4
          if cross1 < 0 and cross2 > 0 and cross3 < 0 and cross4 > 0: # then this point is within the convex hull and should be discarded
            print "discarding point:", testpoint
            pass
          else: # then its in the convex hull
            print "keepingoint:", testpoint
            final_hull_clockwise.append(testindex)
            final_hull.append(testpoint)
            
          #if side == 'left': # then we need to find the side with the lowest
          #  if testpoint[0] 
            
        #for i in 
            
        return final_hull, final_hull_clockwise
              
        return
          
        
        #if point1
    
    
    if __name__ == "__main__":
      # test
      '''test_points = [[1,0,0],[-0.05,0,0],[0,1,0],[0,0,1], [-0.1,0,0], [0.1, 0.1,0.1]]
      test_array=[]
      for point in test_points:
        test_array.append(np.array(point))
    
      result = find_convex_hull(test_array)
      print "result:", result'''
      
      test_points_ed = [[3.0, 1.0], [1.0, 1.0], [2.0, 2.0], [2.0, 0.0]] #, [2.0, 1.0], [3.0, 4.0], [1.0, 4.0], [-4.0, 0.0]]
      
      
      test_points = [[-10.0,0.0],[0.0,10.0],[0.0,0.0], [-1.0,1.0],[-2.0,1.0],[-1.0,2.0]]
      #print "graham scan:", graham_scan_2d(test_points_ed)
      sorted_test = sorted(test_points, key=lambda point: point[0])
      print "sorted_test",sorted_test
      #exit()
      result, clockwise = divide_and_conquer_2d(sorted_test)
      print result
      print clockwise
      
      
    
    

`
