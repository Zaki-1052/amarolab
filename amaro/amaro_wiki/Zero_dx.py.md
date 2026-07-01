# Zero dx.py

`
    
    
    <nowiki>
    #!/usr/bin/python
    
    # by Lane Votapka
    # Amaro lab 2014
    
    '''
    zero_dx.py
    
    This script creates a dx file of defined size that contains zeroes at every data point. It is a zero potential field.
    
    Input:
    
    python zero_dx.py (grid size) [grid size] [grid size]
    
    Output: the DX file to standard output
    
    '''
    
    import sys, os
    
    resolution = 0.5
    
    assert len(sys.argv) in [2, 4, 5], "Wrong number of arguments. Must be: zero_dx (grid width) or zero_dx (grid_width) (grid length) (grid height)"
    
    grid_width = int(sys.argv[1])
    if len(sys.argv) >= 4:
      grid_length = int(sys.argv[2])
      grid_height = int(sys.argv[3])
    else: # then its a cubic grid
      grid_length = grid_height = grid_width
      
    if len(sys.argv) == 5:
      resolution = float(sys.argv[4])
    
      
    #print "grid width:", grid_width, "grid length:", grid_length, "grid height:", grid_height
    total_points = grid_width*grid_length*grid_height
    
    originx = -grid_width*resolution*0.5
    originy = -grid_length*resolution*0.5
    originz = -grid_height*resolution*0.5
    
    header = """# Data from zero_dx.py
    #
    # POTENTIAL (kT/e)
    #
    object 1 class gridpositions counts %d %d %d
    origin  %8.6e  %8.6e  %8.6e
    delta %8.6e 0.000000e+00 0.000000e+00
    delta 0.000000e+00 %8.6e 0.000000e+00
    delta 0.000000e+00 0.000000e+00 %8.6e
    object 2 class gridconnections counts %d %d %d
    object 3 class array type double rank 0 items %d data follows""" % (grid_width, grid_length, grid_height, originx, originy, originz, resolution, resolution, resolution, grid_width, grid_length, grid_height, total_points)
    
    tailer = """attribute "dep" string "positions"
    object "regular positions regular connections" class field
    component "positions" value 1
    component "connections" value 2
    component "data" value 3"""
    
    print header
    #print "tailer: \n%s" % tailer
    data_list = []
    for i in range(total_points):
      data_list.append("%8.6e" % 0.0)
      if i % 3 == 2: 
        print ' '.join(data_list)
        data_list = []
        
    print tailer
      
      
    </code>
    

</nowiki>`
