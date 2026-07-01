import numpy as np
from numpy import array
import random


######################################################################################################################
## 3D
######################################################################################################################

def get_seg_dict_num(seg_dict, seg_index):
  if seg_index[0][0] > seg_index[1][0]: # we want the index with the greater x-value
    index = seg_index
  else:
    index = seg_index[::-1]
  
  if index in seg_dict:
    return seg_dict[index]
  else:
    return 0

def increment_seg_dict(seg_dict, seg_index):
  if seg_index[0][0] > seg_index[1][0]: # we want the index with the greater x-value
    index = seg_index
  else:
    index = seg_index[::-1]
  
  "putting index:", index, "into seg_dict because", index[0][0], ">", index[1][0]  
  
  if index in seg_dict:
    seg_dict[index] += 1
  else:
    seg_dict[index] = 1
  return

def gift_wrapping_3d (raw_points):
  '''gift wrapping for 3d convex hull'''
  n = len(raw_points)
  point1 = array(raw_points[0])
  xaxis = array([1,0,0])
  maxx = raw_points[0][0]
  points = []
  seg_dict = {} # a dictionary that contains the number of triangles a seg is in
  
  for i in range(n): # find the n with the largest x value
    point = tuple(raw_points[i])
    points.append(point)
    if point[0] > maxx:
      maxx = point[0]
      point1 = point
  #print "points:", points, "n:", n
  
  #print "point with greatest x value:", point1
  
  best_dot = -1.0
  point2 = array(raw_points[1])
  for i in range(n):
    pointi = np.array(points[i])
    if np.array_equal(pointi, point1): 
      #print "throwing away point", pointi, "because its equal to", point1
      continue
    diff_vec = pointi - point1
    diff_len = np.linalg.norm(diff_vec)
    
    test_dot = np.dot(diff_vec/diff_len,xaxis)
    #print "dot for point", pointi, ":", test_dot
    if test_dot > best_dot:
      best_dot = test_dot
      point2 = pointi
  
  point1 = tuple(point1)
  point2 = tuple(point2)
  #print "starting segment:", point1, point2
  ref_vec = xaxis
  # now find the best triangle
  triangles = []
  
  seg_list = set([(point1, point2),])
  norm_dict = {(point1,point2):xaxis}
  #seg_dict[(point1,point2)] = 0
  increment_seg_dict( seg_dict, (point1,point2) )
  
  #max_iter = 200
  counter = 0
  first_time = True
  
  while seg_list:
    #print "seg_list:", seg_list
    counter += 1
    #if counter > max_iter:
      #raise Exception, "max_iter error"
    
    seg = seg_list.pop() # take something out of the seg_list
    tuple1 = seg[0]
    tuple2 = seg[1]
    point1 = np.array(seg[0])
    point2 = np.array(seg[1])
    result = get_seg_dict_num( seg_dict, (seg[0],seg[1]) ) 
    #print "number of triangles on seg:", tuple1, tuple2, ":", result
    if result >= 2: # then we already have 2 triangles on this segment
      continue # forget about drawing a triangle for this seg
    #print "norm_dict:", norm_dict
    ref_vec = norm_dict[(seg[0],seg[1])]
    #print "ref_vec:", ref_vec
    
    best_dot_cross = -1.0
    best_point = None
    for i in range(n): # look at each point
      #print "points[i]:", points[i]
      #print "point1:", point1
      #print "point2:", point2
      pointi = array(points[i])
      if np.array_equal(pointi, point1) or np.array_equal(pointi, point2): continue # if we are trying one of the points that are point1 or point2
      diff_vec1 = point2-point1
      diff_len1 = np.linalg.norm(diff_vec1)
      diff_vec2 = pointi - point2
      diff_len2 = np.linalg.norm(diff_vec2)
    
      test_cross = np.cross(diff_vec1/diff_len1,diff_vec2/diff_len2)
      test_cross_len = np.linalg.norm(test_cross)
      test_cross = test_cross / test_cross_len
      #print "test_cross for point", points[i], ":", test_cross
      dot_cross = np.dot(test_cross, ref_vec)
      if dot_cross > best_dot_cross:
        best_cross = test_cross
        best_dot_cross = dot_cross
        best_point = pointi
        tuple3 = points[i]
      
    point3 = best_point
    
    #point1 = tuple(point1)
    #point2 = tuple(point2)
    #point3 = tuple(point3)
    if get_seg_dict_num( seg_dict, (tuple2,tuple1) ) > 2: continue
    if get_seg_dict_num( seg_dict, (tuple3,tuple2) ) > 2: continue
    if get_seg_dict_num( seg_dict, (tuple1,tuple3) ) > 2: continue
    
    # now we have a triangle from point1 -> point2 -> point3
    #print "triangle points:", point1, point2, point3
    # must test each edge
    if first_time:
      increment_seg_dict( seg_dict, (tuple2,tuple1) )
      seg_list.add((tuple2, tuple1))
      norm_dict[(tuple2,tuple1)] = best_cross
    
    increment_seg_dict( seg_dict, (tuple3,tuple2) )
    seg_list.add((tuple3, tuple2))
    norm_dict[(tuple3,tuple2)] = best_cross
    
    increment_seg_dict( seg_dict, (tuple1,tuple3) )
    seg_list.add((tuple1, tuple3))
    norm_dict[(tuple1,tuple3)] = best_cross
    
    triangles.append((tuple1,tuple2,tuple3))
    
    #print "="*20
    first_time = False
  
  #for point in points:
    #print "draw sphere {", point[0], point[1], point[2], "} radius 0.05"
  
  #print "triangles:", triangles
  #for triangle in triangles:
    #print "draw triangle {",triangle[0][0],triangle[0][1],triangle[0][2],"} {",triangle[1][0],triangle[1][1],triangle[1][2],"} {",triangle[2][0],triangle[2][1],triangle[2][2],"}"
  return triangles


def akl_toussaint(points):
  '''The Akl-Toussaint Heuristic:
  given a set of points, will create an octahedron whose corners are the extremes in x, y, and z directions.
  every point within this octahedron will be removed.
  This causes any expected running time for a convex hull algorithm to be reduced to linear time'''
  x_high = (-1e99,0,0); x_low = (1e99,0,0); y_high = (0,-1e99,0); y_low = (0,1e99,0); z_high = (0,0,-1e99); z_low = (0,0,1e99)
  
  
  for point in points: # find the corners of the octahedron
    if point[0] > x_high[0]: x_high = point
    if point[0] < x_low[0]: x_low = point
    if point[1] > y_high[1]: y_high = point
    if point[1] < y_low[1]: y_low = point
    if point[2] > z_high[2]: z_high = point
    if point[2] < z_low[2]: z_low = point
    
  octahedron = [
  (x_high,y_high,z_high),
  (x_high,z_low,y_high),
  (x_high,y_low,z_low),
  (x_high,z_high,y_low),
  (x_low,y_low,z_high),
  (x_low,z_low,y_low),
  (x_low,y_high,z_low),
  (x_low,z_high,y_high),
  ]
  new_points = [] # everything outside of the octahedron
  for point in points: # now check to see if a point is inside or outside the octahedron
    outside = outside_hull(point, octahedron, epsilon=-1.0e-5)
    if outside:
      new_points.append(point)
      
  return new_points

def outside_hull(our_point, triangles, epsilon=1.0e-5):
  '''given the hull as defined by a list of triangles, will return whether a point is within these or not.
  
  epsilon needed for imprecisions in the floating-point operations.
  '''
  our_point = np.array(our_point) # convert it to an array
  #within = False
  for triangle in triangles:
    #triangle = np.array(triangle)
    rel_point = our_point - np.array(triangle[0]) # vector from triangle corner to point
    vec1 = np.array(triangle[1]) - np.array(triangle[0])
    vec2 = np.array(triangle[2]) - np.array(triangle[1])
    #print "vec1:", vec1
    #print "vec2:", vec2
    our_cross = np.cross(vec1, vec2)
    our_dot = np.dot(rel_point,our_cross)
    #print "dot between", rel_point, "and", our_cross, ":", our_dot
    if np.dot(rel_point,our_cross) > epsilon: # then its outside
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
    if outside == True:
      print "Found a point outside of the hull!:", point
      raise Exception 
      
  print "All is well..."

test_points = [[1,0,0],[-0.05,-0.4,0],[0,1,0],[0,0,1],[0.1, 0.1,0.1], [-0.1,0,0.5],]
test_points2 = []
for x in [-2.0,0.0,2.0]:
  for y in [-2.0,0.0,2.0]:
    for z in [-2.0,0.0,2.0]:
      print [x,y,z]
      test_points2.append([x,y,z])
test_points2 = test_points2 + [[-7.0,0.0,0.0],[7.0,0.0,0.0],[0.0,-7.0,0.0],[0.0,7.0,0.0],[0.0,0.0,-7.0],[0.0,0.0,7.0]]

#test_points = [[1.0,0.0,0.0],[0.01,1.0,0.0],[0.02,0.0,1.0], [0.1, 0.1,0.1]]
