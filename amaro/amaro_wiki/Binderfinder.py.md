# Binderfinder.py

`
    
    
    
    '''
    binderfinder.py
    
    This script takes # arguments:
    
    -rec: The PQRXML structure that contains the receptor molecules
    -rxn: The reaction criteria file
    -results: one or more results files that contain the binding information for each site
    
    The script returns:
    
    the "rec" structure with the occupancy column of a molecule numbered by how many reaction events there are for that molecule
    
    '''
    
    import pdb2 as pdb
    import sys, re, os
    #from cStringIO import StringIO # NOTE: may want to change this to cStringIO if more speed is needed in the future
    import numpy as np
    import argparse
    import time
    import xml.sax as sax
    import xml.etree.cElementTree as ET # for writing xml files
    from pprint import pprint
    
    def parse_bd_results(bd_results_filename):
      ''' given a BD results file name, will open the file and extract the number of reactions for each site'''
      #bd_results_file = open(bd_results_filename, 'r')
      bd_dict = {}
      if os.path.getsize(bd_results_filename) == 0:
        return bd_dict
      try:
        tree = ET.parse(bd_results_filename)
      except SyntaxError:
        return bd_dict
      root = tree.getroot()
      for tag in root:
        if tag.tag == "reactions":
          reactions = tag
          for tag2 in reactions:
            i = 0
            if tag2.tag == "escaped":
              #bd_dict['inf'] = int(tag2.text)
              pass
            elif tag2.tag == "n-trajectories":
              #bd_dict['total'] = int(tag2.text)
              pass
            elif tag2.tag == "completed":
              site = tag2[0].text.strip() # need to remove the "rxn" from the beginning of the site string
              '''
              condensed_site = 'UNK'
              if site.startswith('site_2ndary') or site.startswith('secondary_site'):
                condensed_site = "NA_secondary"
              elif site.startswith('site_'):
                condensed_site = "NA_primary"
              elif site.startswith('hemagg'):
                condensed_site = "HA"
              '''
              n = tag2[1].text
              #name = outer_state[i] + '_' + str(site)
              if site not in bd_dict.keys():
                bd_dict[site] = int(n)
              else:
                bd_dict[site] += int(n)
              i += 1
      #print "bd_dict:", bd_dict
    
      return bd_dict
    
    def add_dictionaries(dict1, dict2):
      '''
      adds the values numerically within each dictionary
      NOTE: dict1 is updated and returned BY REFERENCE
      '''
      new_dict = dict1
      for key in dict2.keys():
        if key in dict1.keys():
          dict1[key] += dict2[key]
        else:
          dict1[key] = dict2[key]
    
      return dict1
    
    
    def make_rxn_dict(rxn_filename):
      ''' given a reaction XML file, will parse the XMl, piling the reaction names into a dictionary with the atom ID pairs as the values'''
      atomid_dict = {}
      rxn_file = open(rxn_filename,'r')
      
      if os.path.getsize(rxn_filename) == 0:
        return atomid_dict
      try:
        tree = ET.parse(rxn_filename)
      except SyntaxError:
        return atomid_dict
        
      root = tree.getroot()
      for tag in root:
        if tag.tag == "reactions":
          reactions = tag
          for tag2 in reactions:
            if tag2.tag == "reaction":
              reaction = tag2
              for tag3 in reaction:
                if tag3.tag == "name":
                  name = tag3.text.strip()
                  atomid_dict[name] = []
                elif tag3.tag == "criterion":
                  criterion = tag3
                  for tag4 in criterion:
                    if tag4.tag == "pair":
                      pair = tag4
                      atoms = pair[0].text.strip().split()
                      atomid_dict[name].append(atoms[0])
      
      rxn_file.close()
      return atomid_dict
    
    def bisect_atoms(atom_list, query, lower_index = 0, upper_index = None):
      ''' a recursive function to find a particular atom index query, returning that atom object '''
      if upper_index == None:
        upper_index = len(atom_list)
      listlen = upper_index - lower_index
      if listlen == 0: # then we have a problem
        return "Error"
      elif listlen == 1: # then we have the base case
        return lower_index # this is the index we desire
      else: # then we must subdivide this list
        halfpoint = lower_index + listlen / 2 # an integer division
        halfpoint_id = atom_list[halfpoint].index
        if query < halfpoint_id: # then we found it
          return bisect_atoms(atom_list, query, lower_index, halfpoint)
        else:
          return bisect_atoms(atom_list, query, halfpoint, upper_index)
          
      
    
    starttime = time.time()
    print "Parsing arguments"
    # parse the arguments
    parser = argparse.ArgumentParser(description="Takes a PQRXML structure, a Browndye reaction criteria file, and a results XML and returns a structure file with the molecule's occupancies numbered by the binding events to a particular molecule.")
    parser.add_argument('-r', '-rec', dest="rec", type=str, help="name of PDB file containing receptor")
    parser.add_argument('-x', '-rxn', dest="rxn", type=str, help="name of reaction file containing reaction names and atomID pairs.")
    parser.add_argument('-s', '-res', nargs='+', dest="res", type=str, help="a list of one or more Browndye results XML files")
    parser.add_argument('-o', '-out', dest="out", type=str, help="The name of an output pdb file")
    parser.add_argument('-c', '-color', dest="color", type=str, help="option for which structures to color: atom, residue, or molecule.")
    
    args = parser.parse_args() # parse the args into a dictionary
    args = vars(args)
    
    rec_pdb_filename = args['rec']
    out_filename = args['out']
    results_files = args['res']
    rxn_filename = args['rxn']
    colormode = args['color']
    
    max_rxns = 0.0
    
    print "Parsing reaction file information... time:", time.time() - starttime
    atomid_dict = make_rxn_dict(rxn_filename)
    #print "atomid_dict:", atomid_dict
    
    print "Parsing BD simulation results file... time:", time.time() - starttime
    #bd_dict = parse_bd_results(results_filename)
    bd_dict = {}
    for results_filename in results_files: # first, combine all results files
      # read the results file
      #print "now reading result file:", ligdir
      single_bd_dict = parse_bd_results(results_filename)
      bd_dict = add_dictionaries(single_bd_dict, bd_dict)
    
    for rxn_name in bd_dict.keys(): # find the site with the largest number of reactions
      if bd_dict[rxn_name] > max_rxns:
        max_rxns = bd_dict
    
    #print "bd_dict:", bd_dict
    
    print "Opening pqrxml file... time:", time.time() - starttime
    parser=pdb.Big_PDBParser()
    ourpdb = parser.get_structure('pqrxml file', rec_pdb_filename, preserve_index = True, preserve_resid = True, pqrxml = True)
    
    print "Now searching for all relevant atoms, changing occupancy score to match reaction ratio... time:", time.time() - starttime
    for rxn_name in atomid_dict.keys(): # iterate thru all the different named reactions
      atomids = atomid_dict[rxn_name]
      if colormode == 'molecule':
        atomids = [atomid_dict[rxn_name][0]]
      for atomid in atomids: # iterate thru the atom indeces
        #print "atomid:", atomid
        list_index = bisect_atoms(ourpdb.atoms, int(atomid))
        print "atomid:", atomid, " list_index:", list_index, " rxn_name:", rxn_name, " bd_dict[rxn_name]:", bd_dict[rxn_name]
        ourpdb.atoms[list_index].beta += bd_dict[rxn_name] # make the index
        #ourpdb.atoms[list_index].occupancy += bd_dict[rxn_name] # make the index
        if colormode == 'residue': # change the beta of the entire residue
          ref_resid = ourpdb.atoms[list_index].resid
          cur_resid = ref_resid
          for incr in [1, -1]:
            i = incr
            while True:
              if list_index+i < 0 or list_index+i >= len(ourpdb.atoms): break
              cur_resid = ourpdb.atoms[list_index+i].resid
              if cur_resid != ref_resid: break
              ourpdb.atoms[list_index+i].beta += bd_dict[rxn_name] # make the index
              #ourpdb.atoms[list_index+i].beta += bd_dict[rxn_name] # make the index
              i += incr
            
        elif colormode == 'molecule': # walk through the entire molecule, changing the betas
          ref_resid = int(ourpdb.atoms[list_index].resid)
          cur_resid = int(ref_resid)
          last_resid = int(cur_resid)
          for incr in [1, -1]:
            i = incr
            while True:
              if list_index+i < 0 or list_index+i >= len(ourpdb.atoms): break
              cur_resid = int(ourpdb.atoms[list_index+i].resid)
              if cur_resid != last_resid: 
                resid_diff = abs(cur_resid - last_resid)
                if resid_diff > 1: break
                last_resid = cur_resid
              ourpdb.atoms[list_index+i].beta += bd_dict[rxn_name] # make the index
              #ourpdb.atoms[list_index+i].occupancy += bd_dict[rxn_name] # make the index
              i += incr
        
    print "Now writing the structure... time:", time.time() - starttime
    print "Writing PDB file... time:", time.time() - starttime
    ourpdb.save(out_filename, standard=False, pqr=False) 
    
    print "Complete. Total time:", time.time() - starttime
    
    
    

`
