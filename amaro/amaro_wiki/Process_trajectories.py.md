# Process trajectories.py

'''
    process_trajectories.py
    By Lane Votapka
    Amaro Lab 2015
    
    This program makes use of and replaces the Browndye programs process_trajectories and xyz_trajectory.
    
    It is intended to make it easy to retrieve a VMD-readable pdb or pqr trajectory from a Browndye file
    
    '''
    
    import sys, re, os
    from cStringIO import StringIO # NOTE: may want to change this to cStringIO if more speed is needed in the future
    import xml.etree.cElementTree as ET # for writing xml files
    import numpy as np
    import argparse
    import time
    import xml.sax as sax
    
    max_structures = 1e9 # a maximum number of trajectories to safely write
    #empty = "/extra/banzai/lvotapka/projects/seekr/empty.pqrxml"
    
    def find_first_rxn_state(rxn_filename):
      rxn_dict = {}
      if os.path.getsize(rxn_filename) == 0:
        print "Error: There was a problem with the provided rxn file. Are you sure it's in XML?"
        return rxn_dict
      try:
        tree = ET.parse(rxn_filename)
      except SyntaxError:
        print "Error: There was a problem with the provided rxn file. Unable to parse using ETree."
        return rxn_dict
      root = tree.getroot()
      for tag in root: # open particular tags in the xml file
        if tag.tag == "first-state":
          first_state = tag.text.strip()
          return first_state
    
      raise Exception, "Unable to use provided reaction file to find the first reaction state."
    
    
    def parse_inputfile(input_filename):
      ''' given a input xml file name, will open the file and extract information about the simulation that has ran'''
      input_dict = {}
      if not input_filename: # then no file was specified
        return input_dict
      basedir = os.path.dirname(input_filename)
      if os.path.getsize(input_filename) == 0:
        print "Error: There was a problem with the provided input file. Are you sure it's in XML?"
        return input_dict
      try:
        tree = ET.parse(input_filename)
      except SyntaxError:
        print "Error: There was a problem with the provided input file. Unable to parse using ETree."
        return input_dict
      root = tree.getroot()
      for tag in root: # open particular tags in the xml file
        if tag.tag == "trajectory-file":
          traj_file = tag.text.strip()
        elif tag.tag == "n-threads":
          input_dict['n-threads'] = tag.text.strip()
        elif tag.tag == "molecule0":
          i = 0
          for tag2 in tag:
            if tag2.tag == "atoms":
              input_dict['mol0'] = os.path.join(basedir, tag2.text).strip()
            i += 1
        elif tag.tag == "molecule1":
          i = 0
          for tag2 in tag:
            if tag2.tag == "atoms":
              input_dict['mol1'] = os.path.join(basedir, tag2.text).strip()
            i += 1
        elif tag.tag == "molecule-pair":
          i = 0
          for tag2 in tag:
            if tag2.tag == "molecule0":
              for tag3 in tag2:
                if tag3.tag == "atoms":
                  input_dict['mol0'] = os.path.join(basedir, tag3.text).strip()
            elif tag2.tag == "molecule1":
              for tag3 in tag2:
                if tag3.tag == "atoms":
                  input_dict['mol1'] = os.path.join(basedir, tag3.text).strip()
            elif tag2.tag == "reaction-file":
              input_dict['rxnfile'] = tag2.text.strip()
            i += 1
            #print "tag2:", tag2
    
        elif tag.tag == "reactions":
          input_dict['rxnfile'] = tag.text.strip()
        #print "tag:", tag
      #print "bd_dict:", bd_dict
      input_dict['traj'] = [] # a list of the trajectory files for each of the threads
      input_dict['index'] = []
      for i in range(0,int(input_dict['n-threads'])):
        input_dict['traj'].append(traj_file+str(i)+".xml")
        input_dict['index'].append(traj_file+str(i)+".index.xml")
    
      return input_dict
    
    def count_num_trajs(traj_filename):
      '''given a traj file outputted from Browndye, will return the total number of trajectories in that file'''
      n = 0
      assert os.path.getsize(traj_filename), "Error: There was a problem with the provided input file. Are you sure it's in XML?"
      try:
        tree = ET.parse(traj_filename)
      except SyntaxError:
        print "Error: There was a problem with the provided trajectory file. Unable to parse using ETree."
        return n
      root = tree.getroot()
      for tag in root: # open particular tags in the xml file
        if tag.tag == "trajectory":
          n += 1
      return n
    
    def modify_pqr(pqr_filename, to_pdb=False):
      '''edits the pqr file by removing any line except lines that begin with ATOM because BrownDye has weird pqr output'''
      pqrread = open(pqr_filename, 'r')
      raw_pqr = pqrread.readlines()
      pqrread.close
      #basename = os.path.basename(pqr_filename)
      total_endmdl = 0
      for line in raw_pqr:
        if re.match("Molecule",line):
          total_endmdl += 1
      pdbname = pqr_filename #+'.pdb'
      if to_pdb:
        pqrwrite = open(pdbname,'w')
      else:
        pqrwrite = open(pqr_filename, 'w')
      counter = 0
      endmdl_counter = 0
      for line in raw_pqr:
        if re.match("ATOM",line):
          # first fix the coordinates so they are in the correct column
          linelist = line.split()
          x = float(linelist[5])
          y = float(linelist[6])
          z = float(linelist[7])
          line = line[:30] + "% 8.3f% 8.3f% 8.3f" % (x,y,z) + line[55:]
          # then determine whether we are writing a pdb line or a pqr line
          if to_pdb:
            pqrwrite.write(line[:54]+"  1.00  0.00\n")
          else:
            pqrwrite.write(line)
        elif re.match("Molecule",line) and counter > 1:
          pqrwrite.write("ENDMDL\n")
          endmdl_counter += 1
        counter += 1
      pqrwrite.write("ENDMDL\n")
      pqrwrite.close()
      return
    
    def decipher_number_string(number_str, endnum):
      s = number_str.split(":")
      assert len(s) > 0 and len(s) < 4, "the indexing of string %s makes no sense. Use the format start:end:stride, where end and stride are optional" % number_str
      if len(s) == 1:
        return map(int, s)
      elif len(s) == 2:
        if not s[0]:
          s[0] = 0
        if not s[1]:
          s[1] = endnum
        return range(int(s[0]), int(s[1]))
      elif len(s) == 3:
        if not s[0]:
          s[0] = 0
        if not s[1]:
          s[1] = endnum
        assert s[2], "improper formatting of slice: %s Please include either stride after second colon or omit second colon" % number_str
        return range(int(s[0]), int(s[1]), int(s[2]))
    
    if __name__ == "__main__":
      starttime = time.time()
      print "Parsing arguments"
      # parse the arguments
      parser = argparse.ArgumentParser(description="Takes trajectory output from Browndye and generates a pdb or pqr trajectory.")
      parser.add_argument('-i', '-input', dest="input", type=str, help="name of Browndye input file containing all the useful information we need. Can be used to fill out the -traj, -index, -mol0, -mol1, -rxnfile options. Although any of those defined explicitly in the arguments will overwhelm what is read from the input file.")
      parser.add_argument('-t', '-traj', dest="traj", type=str, help="trajectory file from nam_simulation. Can be neglected if -i option is provided.")
      parser.add_argument('-d', '-index', dest="index", type=str, help="trajectory index file from nam_simulation. Can be neglected if -i option is provided.")
      parser.add_argument('-n', '-number', dest="number", type=str, default="0", help="trajectory number in file (starting with 0, but may be a range in the following formats beginning:end or beginning:end:stride. Omitting any argument defaults to the furthest in that direction - just like python indexing. Examples: 1, 0:5, 10:20:2, 10:, : )")
      parser.add_argument('-sn', '-subnumber', dest="subnumber", type=str, default="0", help="subtrajectory trajectory number in file. Only takes one number at this time")
      #parser.add_argument('-e', '-n_needed', dest="n_needed", type=str, default="1", help="number of sequential trajectories to write")
      parser.add_argument('-o', '-out', dest="out", type=str, default="traj", help="name of the output trajectory prefix. Output will be in this format: PREFIX##.pqr")
      parser.add_argument('-x', '-srxn', dest="srxn", type=str, help="which reaction we are pulling out of the file. Keywords 'all' and 'escape' are allowed.")
      parser.add_argument('-0', '-mol0', dest="mol0", type=str, help="molecule0 pqrxml file. Can be neglected if -i option is provided.")
      parser.add_argument('-1', '-mol1', dest="mol1", type=str, help="molecule1 pqrxml file. Can be neglected if -i option is provided.")
      parser.add_argument('-w', '-workdir', dest="workdir", default="/usr/tmp", help="the directory in which to generate all temporary files")
      parser.add_argument('-r', '-rxnfile', dest="rxnfile", default="", help="The file defining the reaction criteria. Can be neglected if -i option is provided.")
      parser.add_argument('-s', '-stride', dest="stride", default="1", help="The stride for the trajectories.")
      parser.add_argument('-c', '-write_rec', dest="write_rec", default=False, help="Write a structure of the receptor as well.", action="store_true")
    
      args = parser.parse_args() # parse the args into a dictionary
      args = vars(args)
    
      inputdict = parse_inputfile(args['input'])
      #print "inputdict:", inputdict
      if 'n-threads' in inputdict.keys():
        n_threads = int(inputdict['n-threads']) # the number of trajectory files to open
      else:
        n_threads = 1
    
      if args['traj']:
        inputdict['traj'] = [args['traj']]
      if args['index']:
        inputdict['index'] = [args['index']]
      if args['mol0']:
        inputdict['mol0'] = args['mol0']
      if args['mol1']:
        inputdict['mol1'] = args['mol1']
      if args['rxnfile']:
        inputdict['rxnfile'] = args['rxnfile']
    
      out_prefix = args['out']
      number_string = args['number']
      subnumber_string = args['subnumber']
      sn = int(subnumber_string)
      rxn_string = args['srxn']
      workdir = args['workdir']
      stride = args['stride']
      write_rec = args['write_rec']
    
      wrote_rec = False
      counter = 0
    
      #assert rxn_string, "An argument for -srxn must be provided."
      number_lists = []
      subtraj_lists = []
      print "now extracting all successful reaction numbers..."
      #if not os.path.exists(workdir): 
        #os.mkdir(workdir) # create the working directory
      assert os.path.exists(workdir), "The provided working directory: %s does not exist." % workdir
      quitting = False
      total_number = 0
      for i in range(n_threads):
        if quitting: break
        print "parsing trajectories from thread number:", i
        outputfilename = os.path.join(workdir, "rxn_output%d.txt" % i)
        traj_filename = inputdict['traj'][i]
        trajindex_filename = inputdict['index'][i]
        if not rxn_string or rxn_string.lower() in ['all', 'everything']:
          #cmd = "echo 'Browndye Trajectory number' > %s; process_trajectories -traj %s -index %s >> %s" % (outputfilename, traj_filename, trajindex_filename, outputfilename)
          n = count_num_trajs(inputdict['traj'][i])
          #print "n:", n
          number_list = range(n)
          subtraj_list = [sn]*n
        else:
          if rxn_string.lower() in ["escape", "ucomp", "uncomp"]: # maybe add support for stuck trajectories
            first_state = find_first_rxn_state(inputdict['rxnfile'])
            cmd = "echo 'Browndye Trajectory number' > %s; process_trajectories -traj %s -index %s -uncomp %s >> %s" % (outputfilename, traj_filename, trajindex_filename, first_state, outputfilename)
          else:
            cmd = "echo 'Browndye Trajectory number' > %s; process_trajectories -traj %s -index %s -srxn %s >> %s" % (outputfilename, traj_filename, trajindex_filename, rxn_string, outputfilename)
          print "running command:", cmd
          os.system(cmd) # run the command to extract successful trajectories
    
          rxn_output = open(outputfilename, 'r')
          number_list = []
          subtraj_list = []
          for line in rxn_output.xreadlines():
            if re.search("<number>",line):
              number_list.append(int(line.strip().split()[1])) # pull out the text within the center of the tag
            elif re.search("<subtrajectory>",line):
              subtraj_list.append(int(line.strip().split()[1])) # pull out the text within the center of the tag
    
          rxn_output.close()
        numlines = len(number_list)
        #print "number_list:", number_list
        #print "subtraj_list:", subtraj_list
        number_lists.append(number_list)
        subtraj_lists.append(subtraj_list)
        total_number += numlines
      # now decipher the number string
      number_range = decipher_number_string(number_string, total_number)
      subnumber_range = decipher_number_string(subnumber_string, total_number)
    
      print "number_range:", number_range
      print "subnumber_range:", subnumber_range
      print "number_lists:", number_lists
    
      #write empty pqrxml file
      emptyname = os.path.join(workdir, "empty.pqrxml")
      empty = open(emptyname, 'w')
      empty.write("<roottag>\n</roottag>\n")
      empty.close()
    
      counter = 0
      for i in range(n_threads):
        if quitting: break
        print "extracting trajectories from thread number:", i
        number_list = number_lists[i]
        numlines = len(number_list)
        subtraj_list = subtraj_lists[i]
        traj_filename = inputdict['traj'][i]
        trajindex_filename = inputdict['index'][i]
        for f in range(numlines):
          # first get the indeces of the trajectory number and subtrajectory
    
          if counter > max_structures:
            quitting = True
            print "ALERT: maximum number of structures exceeded. Exiting..."
            break
          if counter not in number_range: # then we are skipping this one
            continue
          if counter > number_range[-1]: # if we are never going to do any more trajectories, then we may as well break
            print "ALERT: maximum number range exceeded. Exiting..."
            break
          rxn_number = number_list[f]
          rxn_subtraj = subtraj_list[f]
          # we need to run process_trajectories to pull out all the trajectory information
          stem = os.path.join(workdir,"proc_traj%d_%d" % (i, f))
          xmltrajfilename = "%s.xml" % (stem,)
          cmd = "process_trajectories -traj %s -index %s -n %d -sn %d -nstride %s > %s" % (traj_filename, trajindex_filename, rxn_number, rxn_subtraj, stride, xmltrajfilename)
          print "running command:", cmd
          os.system(cmd)
          # read each trajectory, and pull out the frames
          #trajfile = open(xmltrajfilename,'r')
          #trajfilelist = trajfile.readlines()
          #trajfile.close()
          #lastframelist = trajfilelist[:3] + trajfilelist[-9:]
          #lastframename = stem + "_last.xml"
          #lastframe = open(lastframename, 'w')
          #lastframe.writelines(lastframelist) # write the last frame
          #lastframe.close()
          # write the last frame as a pqr file
          pqrfile = "%s%d.pdb" % (out_prefix,counter)
          #pdbfilename = "%s%d.pdb" % (out_prefix,counter)
          cmd = "xyz_trajectory -mol0 %s -mol1 %s -trajf %s -pqr > %s" % (emptyname, inputdict['mol1'], xmltrajfilename, pqrfile)
          print "running command:", cmd
          os.system(cmd)
          # the pqr files must be modified
          modify_pqr(pqrfile,  to_pdb=True)
          # write the receptor pqr
          if i == 0 and f == 0 and write_rec:
            #pqrfile = '.'.join(os.path.basename('receptor_dry_pqr.pqrxml').split('.')[:-1])
            pqrfile = "%sreceptor.pqr" % (out_prefix)
            cmd = "xyz_trajectory -mol0 %s -mol1 %s -trajf %s -pqr > %s" % (inputdict['mol0'], emptyname, xmltrajfilename, pqrfile)
    
            print "running command:", cmd # we don't necessarily want to run this for large receptors
            os.system(cmd)
            # the pqr files must be modified
            modify_pqr(pqrfile)
            wrote_rec = True
    
    
           #cmd = "pqr2xml < %s.pqr> %s.pqrxml; apbs %s.pqr.in > %s.pqr.out" % (pqrfile, pqrfile, pqrfile, pqrfile)
            #print "running command:", cmd
            #os.system(cmd)
    
          #os.remove(xmltrajfilename)
          counter += 1
    
      if wrote_rec == False and write_rec == True:
        pqrfile = "%sreceptor.pqr" % (out_prefix)
        cmd = "xyz_trajectory -mol0 %s -mol1 %s -trajf %s -pqr > %s" % (inputdict['mol0'], emptyname, xmltrajfilename, pqrfile)
    
        print "running command:", cmd # we don't necessarily want to run this for large receptors
        os.system(cmd)
        # the pqr files must be modified
        modify_pqr(pqrfile)
        wrote_rec = True
