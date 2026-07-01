# Dx.py

`
    
    
    
    #!/usr/bin/python
    
    # by Lane Votapka
    # Amaro lab 2014
    
    '''
    dx.py
    
    This script creates a dx file based on a set of data points.
    
    '''
    
    import sys, os
    num_header_lines = 7 # the number of lines in a DX file header before the actual data starts
    
    
    def parse_dx_header(header_list):
      ''' takes a list of the first few lines of a DX file, returns a dictionary with all the useful quantities associated with a DX file '''
      header_dict = {} # dictionary of all the headers' useful information
      # a very rough parsing of the DX file
      header_dict['width'] = int(header_list[0].strip().split()[5])
      header_dict['height'] = int(header_list[0].strip().split()[6])
      header_dict['depth'] = int(header_list[0].strip().split()[7])
      header_dict['originx'] = float(header_list[1].strip().split()[1])
      header_dict['originy'] = float(header_list[1].strip().split()[2])
      header_dict['originz'] = float(header_list[1].strip().split()[3])
      header_dict['resx'] = float(header_list[2].strip().split()[1])
      header_dict['resy'] = float(header_list[3].strip().split()[2])
      header_dict['resz'] = float(header_list[4].strip().split()[3])
      header_dict['num_data'] = int(header_list[6].strip().split()[9])
      return header_dict
    
    def read_by_tokens(fileobj): # read a file token by token (separated by whitespace instead of newlines)
      for line in fileobj:
        for token in line.split():
          yield token
    
    def make_dx_header_footer(width, height, depth, originx, originy, originz, resx, resy, resz, total_points):
      '''Makes a header and footer string for writing to the file.'''
      #print "grid width:", len_x, "grid length:", len_y, "grid height:", len_z
      header = """# Data from dx.py
    # 
    # POTENTIAL (kT/e)
    # 
    object 1 class gridpositions counts %d %d %d
    origin %8.6e %8.6e %8.6e
    delta %8.6e 0.000000e+00 0.000000e+00
    delta 0.000000e+00 %8.6e 0.000000e+00
    delta 0.000000e+00 0.000000e+00 %8.6e
    object 2 class gridconnections counts %d %d %d
    object 3 class array type double rank 0 items %d data follows
    """ % (width, height, depth, originx, originy, originz, resx, resy, resz, width, height, depth, total_points)
    
      footer = """
    attribute "dep" string "positions"
    object "regular positions regular connections" class field
    component "positions" value 1
    component "connections" value 2
    component "data" value 3
    """
      return header, footer
    
    
    def make_dx(filename, data, len_x, len_y, len_z, resolution, originx=None, originy=None, originz = None):
      #print "grid width:", len_x, "grid length:", len_y, "grid height:", len_z
      total_points = len_x*len_y*len_z
      ourfile = open(filename, 'w')
    
    
      if originx == None: originx = -len_x*resolution*0.5
      if originy == None: originy = -len_y*resolution*0.5
      if originz == None: originz = -len_z*resolution*0.5
    
      header = """# Data from dx.py
    #
    # POTENTIAL (kT/e)
    #
    object 1 class gridpositions counts %d %d %d
    origin  %8.6e  %8.6e  %8.6e
    delta %8.6e 0.000000e+00 0.000000e+00
    delta 0.000000e+00 %8.6e 0.000000e+00
    delta 0.000000e+00 0.000000e+00 %8.6e
    object 2 class gridconnections counts %d %d %d
    object 3 class array type double rank 0 items %d data follows
    """ % (len_x, len_y, len_z, originx, originy, originz, resolution, resolution, resolution, len_x, len_y, len_z, total_points)
    
      tailer = """
    attribute "dep" string "positions"
    object "regular positions regular connections" class field
    component "positions" value 1
    component "connections" value 2
    component "data" value 3"""
    
      #print header
      ourfile.write(header)
      #print "tailer: \n%s" % tailer
      data_list = []
      for i in range(total_points):
        data_list.append("%8.6e" % data[i])
        if (i % 3 == 2) or (i == total_points-1):
          #print ' '.join(data_list)
          ourfile.write(' '.join(data_list))
          ourfile.write('\n')
          data_list = []
    
      #print tailer
      ourfile.write(tailer)
    
    def read_dx(dx_filename):
      '''
      Input: 
        dx_filename: a string the defines the location of a .dx file
      
      Output:
        header_dict: a dictionary of all the information in the .dx file header
        tokenized: a generator that will release one piece of data at a time by 
          calling the attribute next()
        file_obj: the DX file object. Make sure to close this when finished.
      
      Usage instructions:
      
      # creates 1-D list of data
      my_header, data_gen, file_obj = read_dx('my_filename.dx')
      num_data = my_header['num_data']
      my_data = []
      for i in range(num_data):
        my_data.append(data_gen.next())
      file_obj.close()
      
      # create 3-D numpy array of data
      import numpy
      my_header, data_gen, file_obj = read_dx('my_filename.dx')
      width = my_header['width']
      height = my_header['height']
      depth = my_header['depth']
      my_data = numpy.zeros((width, height, depth))
      for i in range(width):
        for j in range(height):
          for k in range(depth):
            my_data[i,j,k] = data_gen.next()
      file_obj.close()
      
      '''
      # reads a dx file and returns all the relevent information
      #print "Opening DX files for reading and writing... Time:", time.time() - start_time
      dx_file = open(dx_filename,'r') # make a list of open files for reading
      tokenized = read_by_tokens(dx_file) # make an iterator to read the file word by word
      
      # 2. process DX file header information & construct an outline of the final map
      #print "Processing DX file headers... Time.:", time.time() - start_time
      header_dict = {} # a list of every dx files' header dictionary
      #header_sort_list = []
      dx_header_temp = [] # a variable to store the header of this file in a list of stings
      i = 0
      #for i in range(num_header_lines):
      while (i < num_header_lines):
        curline = dx_file.readline() # read another line
        if curline.startswith("#"): continue # this is just a comment, so skip
        dx_header_temp.append(curline)
        i += 1
      header_dict = parse_dx_header(dx_header_temp) # convert to a dictionary of useful quantities
      
      # Ensure that the DX files all have the same widths, heights, depths, and resolutions
      #num_data = header_dict['width']*header_dict['height']*header_dict['depth'] # total number of data points
      # use the origin from the first corner of all the grids
      
      return header_dict, tokenized, dx_file
    
    def load_data_array(dx_filename):
      '''Loads the DX data into a 3D numpy array'''
      my_header, data_gen, file_obj = dx.read_dx(dx_filename)
      width = my_header['width']
      height = my_header['height']
      depth = my_header['depth']
      my_data = numpy.zeros((width, height, depth)) # leave a little rim around the edges for boundaries
      for i in range(width):
        for j in range(height):
          for k in range(depth):
            my_data[i,j,k] = data_gen.next()
      file_obj.close()
      return my_data
      
    
    

`
