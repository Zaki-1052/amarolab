# Myown mergedx.py

`
    
    
    
    
    # By Lane Votapka
    # UCSD Chemistry
    
    '''
    Replacement for mergedx and mergedx2 in the APBS software suite.
    
    usage:
    python myown_mergedx.py [FLAGS] file1.dx [file2.dx ...]
    
    FLAGS:
      -o   Output DX file (default: gridmerged.dx)
    
    These don't work but might be added later
      -r   Resolution of gridpoints (default: resolution of DX files)
      -b   Bounds of output map as xmin ymin zmin xmax ymax zmax (default: calculates full map)
      -s   Prints bounds of merged input DX files. Doesn't generate a merged map.
      -i [integer]  interpolation allowed. If -r argument is not a multiple of the maps, will calculated the value between points using interpolation. The [integer] field specifies the order of interpolation: default 3
      NOTE: -i OPTION NOT YET IMPLEMENTED
      -h   Prints this message
    
    '''
    
    # imports & constants
    import sys, os, unittest, time
    #from optparse import OptionParser # handle program options
    import argparse
    start_time = time.time()
    num_header_lines = 11 # the number of lines in a DX file header before the actual data starts
    
    # DX class
    class DX():
      def __init__(self,filename=""):
        if not filename: # then there's nothing to read, just assign default values
          self.n = (0,0,0) # width, length, and height of this grid
          self.origin = (0.0,0.0,0.0) # origin of the grid
          self.h = (0.0,0.0,0.0) # grid point spacing: x,y,z
          datapoints = 0 # number of data points to follow in the table
        else: # first read the file
          # Assuming we're reading from the output of an APBS run
          pass
    
    class Test_pdb_functions(unittest.TestCase):
      # several test cases to ensure the functions in this module are working properly
      def test_main(self):
        print "WARNING: myown_mergedx.py does not have comprehensive unittests"
    
      def test_parse_dx_header(self): # test this function
        test_header = '''# Data from APBS 1.2
    # 
    # POTENTIAL (kT/e)
    # 
    object 1 class gridpositions counts 268 268 294
    origin -4.024714e+02 -4.054260e+02 -6.580975e+02
    delta 9.821777e-01 0.000000e+00 0.000000e+00
    delta 0.000000e+00 9.691001e-01 0.000000e+00
    delta 0.000000e+00 0.000000e+00 9.092934e-01
    object 2 class gridconnections counts 268 268 294
    object 3 class array type double rank 0 items 21116256 data follows
    -2.123705e-08 -2.129190e-08 -2.134676e-08 
    -2.140167e-08 -2.145658e-08 -2.151058e-08 
    -2.156407e-08 -2.161757e-08 -2.167117e-08 
    -2.172477e-08 -2.177761e-08 -2.182978e-08 
    '''.split('\n')
        test_header_dict = parse_dx_header(test_header)
        self.assertEqual(test_header_dict['width'], 268)
        self.assertEqual(test_header_dict['height'], 268)
        self.assertEqual(test_header_dict['depth'], 294)
        self.assertEqual(test_header_dict['originx'], -4.024714e+02)
        self.assertEqual(test_header_dict['originy'], -4.054260e+02)
        self.assertEqual(test_header_dict['originz'], -6.580975e+02)
        self.assertEqual(test_header_dict['resx'], 9.821777e-01)
        self.assertEqual(test_header_dict['resy'], 9.691001e-01)
        self.assertEqual(test_header_dict['resz'], 9.092934e-01)
        self.assertEqual(test_header_dict['num_data'], 21116256)
    
    
    def parse_dx_header(header_list):
      ''' takes a list of the first few lines of a DX file, returns a dictionary with all the useful quantities associated with a DX file '''
      header_dict = {} # dictionary of all the headers' useful information
      # a very rough parsing of the DX file
      header_dict['width'] = int(header_list[4].strip().split()[5])
      header_dict['height'] = int(header_list[4].strip().split()[6])
      header_dict['depth'] = int(header_list[4].strip().split()[7])
      header_dict['originx'] = float(header_list[5].strip().split()[1])
      header_dict['originy'] = float(header_list[5].strip().split()[2])
      header_dict['originz'] = float(header_list[5].strip().split()[3])
      header_dict['resx'] = float(header_list[6].strip().split()[1])
      header_dict['resy'] = float(header_list[7].strip().split()[2])
      header_dict['resz'] = float(header_list[8].strip().split()[3])
      header_dict['num_data'] = int(header_list[10].strip().split()[9])
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
    
    
    # test cases for program
    
    # 0. Parse arguments
    
    print "WARNING: this program may not be working properly. More testing needed..."
    #exit()
    
    print "Now parsing arguments... Time:", time.time() - start_time
    parser = argparse.ArgumentParser(description="Merges a number of smaller DX files into a single DX file.")
    parser.add_argument("-o", "--output", dest="output", help="Output DX file.", default="gridmerged.dx")
    parser.add_argument('-t', "--test", dest="test", default=False, help="Run unit tests.", action="store_true")
    parser.add_argument('-f', "--force_run", dest="force_run", default=False, help="Force program to run regardless of grid sizes and resolutions.", action="store_true")
    parser.add_argument('dx', metavar='DX_PATH', type=str, nargs='+', help="Names of DX files to merge")
    
    #parser.add_option("-r", "--resolution", dest="resolution", help="Resolution of gridpoints.", type="float")
    #parser.add_option("-b", "--bounds", dest="bounds", help="Bounds of output map as xmin ymin zmin xmax ymax zmax.")
    #parser.add_option("-s", "--print_bounds", action="store_true", dest="print_bounds", help="Prints bounds of merged input DX files. Doesn't generate a merged map.", default=False)
    #parser.add_option("-i", "--interpolation", action="store_true", dest="interpolation", help="prints help messageinterpolation allowed. If -r argument is not a multiple of the maps, will calculated the value between points using interpolation. The [integer] field specifies the order of interpolation.", default=None)
    
    args = parser.parse_args() # parse the args into a dictionary
    args = vars(args)
    if args['output']:
      output_filename = args['output']
    else:
      output_filename = 'gridmerged.dx'
      
    dx_filename_list = args['dx']
    force_run = args['force_run'] # force the program to run even if DX files are uneven
    if args['test']:
      del sys.argv[1:] # delete arguments so they don't interfere with the unittests
      unittest.main() # then run unit tests
      exit()
    width = 0 # number of points in x
    height = 0 # number of points in y
    depth = 0 # number of points in z
    resx = 0
    resy = 0 # resolutions in each direction
    resz = 0
    
    # 1. Open input DX files for reading & open output DX file for writing
    print "Opening DX files for reading and writing... Time:", time.time() - start_time
    dx_file_list = []
    tokenized = []
    outfile = open(output_filename,'w') # open the output file for writing
    for dx_filename in dx_filename_list:
      dx_file = open(dx_filename,'r') # make a list of open files for reading
      tokenized.append(read_by_tokens(dx_file)) # make a list of iterators to read the file word by word
      dx_file_list.append(dx_file)
      
    # 2. process DX file header information & construct an outline of the final map
    print "Processing DX file headers... Time.:", time.time() - start_time
    header_dicts = [] # a list of every dx files' header dictionary
    header_sort_list = []
    counter = 0
    for dx_file in dx_file_list: # loop thru the files  
      dx_header_temp = [] # a variable to store the header of this file in a list of stings
      for i in range(num_header_lines):
        curline = dx_file.readline() # read another line
        dx_header_temp.append(curline)
      header_dict = parse_dx_header(dx_header_temp) # convert to a dictionary of useful quantities
      
      # Ensure that the DX files all have the same widths, heights, depths, and resolutions
      if not force_run:
        if width == 0:
          width = header_dict['width']
        else:
          assert width == header_dict['width'], "Discrepancy between widths of DX grids. Problem in DX grid number: " + counter + ". File name: " + dx_filename_list[counter]
        if height == 0:
          height = header_dict['height']
        else:
          assert height == header_dict['height'], "Discrepancy between heights of DX grids. Problem in DX grid number: " + counter + ". File name: " + dx_filename_list[counter]
        if depth == 0:
          depth = header_dict['depth']
        else:
          assert depth == header_dict['depth'], "Discrepancy between depths of DX grids. Problem in DX grid number: " + counter + ". File name: " + dx_filename_list[counter]
        if resx == 0:
          resx = header_dict['resx']
        else:
          assert resx == header_dict['resx'], "Discrepancy between X-resolution of DX grids. Problem in DX grid number: " + counter + ". File name: " + dx_filename_list[counter]
        if resy == 0:
          resy = header_dict['resy']
        else:
          assert resy == header_dict['resy'], "Discrepancy between Y-resolution of DX grids. Problem in DX grid number: " + counter + ". File name: " + dx_filename_list[counter]
        if resz == 0:
          resz = header_dict['resz']
        else:
          assert resz == header_dict['resz'], "Discrepancy between Z-resolution of DX grids. Problem in DX grid number: " + counter + ". File name: " + dx_filename_list[counter]
      else:
        print "You have enabled the --forced_run option. Therefore it is your responsibility to ensure that the DX files have the proper resolution, widths, etc."
      
      header_dicts.append(header_dict)
      header_sort_list.append((header_dict, dx_file)) # put the dictionary and the filename into the same list for easy sorting
      counter += 1
      
    # 3. Sort the DX files into the correct order and find the total width of the final grid
    print "Sorting DX files into the correct order and finding grid dimensions. Time:", time.time() - start_time
    sorted_list = sorted(header_sort_list, key=lambda entry: entry[0]['originx']) # first sort by the x-coordinate
    sorted_list = sorted(sorted_list, key=lambda entry: entry[0]['originy']) # then sort by the y-coordinate
    sorted_list = sorted(sorted_list, key=lambda entry: entry[0]['originz']) # lastly sort by the z-coordinate
    dx_files_sorted = []
    total_width = sorted_list[0][0]['width']
    total_height = sorted_list[0][0]['height']
    total_depth = sorted_list[0][0]['depth']
    originx = last_origin_x = sorted_list[0][0]['originx']
    originy = last_origin_y = sorted_list[0][0]['originy'] # keeping track of old origin coordinates
    originz = last_origin_z = sorted_list[0][0]['originz']
    box_width = 1
    box_height = 1
    box_depth = 1
    for item in sorted_list: # for each pair of dictionary and dx_file objects...
      #print "item x:", item[0]['originx'], "y:", item[0]['originy'], "z:", item[0]['originz'] # test
      dx_files_sorted.append(item[1])
      
      if item[0]['originx'] < last_origin_x:
        total_width = sorted_list[0][0]['width']
        box_width = 1
      elif item[0]['originx'] > last_origin_x:
        total_width += item[0]['width']
        box_width += 1
      if item[0]['originy'] < last_origin_y:
        total_height = sorted_list[0][0]['height']
        box_height = 1
      elif item[0]['originy'] > last_origin_y:
        total_height += item[0]['height']
        box_height += 1
      if item[0]['originz'] < last_origin_z:
        total_depth = sorted_list[0][0]['depth']
        box_depth= 1
      elif item[0]['originz'] > last_origin_z:
        total_depth += item[0]['depth']
        box_depth += 1
      last_origin_x = item[0]['originx']
      last_origin_y = item[0]['originy']
      last_origin_z = item[0]['originz']
    
    print "  nx = %d, ny = %d, nz = %d" % (total_width, total_height, total_depth)
    print "  hx = %.3f, hy = %.3f, hz = %.3f" % (resx, resy, resz)
    print "  xmin = %.3f, ymin = %.3f, zmin = %.3f" % (originx, originy, originz)
    print "  xmax = %.3f, ymax = %.3f, zmax = %.3f" % (originx + total_width * resx, originy + total_height * resy, originz + total_depth * resz)
    
    num_data = total_width*total_height*total_depth # total number of data points
    # use the origin from the first corner of all the grids
    header, footer = make_dx_header_footer(total_width, total_height, total_depth, sorted_list[0][0]['originx'], sorted_list[0][0]['originy'], sorted_list[0][0]['originz'], resx, resy, resz, num_data)
    # write the header
    outfile.write(header)
    # 4. stream input DX files and write as we go
    print "Streaming data from input files into output file... Time:", time.time() - start_time
    counter = 1
    for i in range(total_width):
      for j in range(total_height):
        for k in range(total_depth):
          box_x = i / width
          box_y = j / height # which file we are currently reading from
          box_z = k / depth
          which_file_index = box_width * box_height * box_z + box_width * box_y + box_x # the index of the file we are currently reading from
          index_x = i - box_x * width
          index_y = j - box_y * height
          index_z = k - box_z * depth
          # PROBLEM: DX data comes in triples... can't just readline, must readline(), then keep track - resolved
          #this_data = dx_files_sorted[which_file_index].readline() # read the current piece of data from the correct file
          this_data = next(tokenized[which_file_index])
          outfile.write(this_data) # write it to the output file
          if counter % 3 == 0 and counter < num_data: 
            outfile.write(" \n")
          else:
            outfile.write(" ")
          
          counter += 1
    outfile.write(footer)
    
    # 5. Interpolation & refinement
    
    # 6. Close all files and wrap stuff up
    for dx_file in dx_file_list:
      dx_file.close()
    outfile.close()
    print "Complete. Time elapsed:", time.time() - start_time
    
    

`
