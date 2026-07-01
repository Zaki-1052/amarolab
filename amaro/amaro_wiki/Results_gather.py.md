# Results gather.py

`
    
    
    
    #!/usr/bin/python
    
    '''
    fhpd_consolidate.py
    descends into the fhpd file tree, recovers all results .xml files, and puts all the results into a single results.xml file in the current working directory
    '''
    import os, sys, glob
    import xml.etree.cElementTree as ET # for writing xml files
    from pprint import pprint
    
    results_files = sys.argv[1:] # get all results files that the user provides
    
    #fhpd_dir = "fhpd/wrongside"
    #lig_dir_glob = "lig*/"
    #results_name = "results.xml"
    
    def parse_bd_results(bd_results_filename):
      ''' given a BD results file name, will open the file and extract information about state transitions'''
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
              bd_dict['inf'] = int(tag2.text)
            elif tag2.tag == "n-trajectories":
              bd_dict['total'] = int(tag2.text)
            elif tag2.tag == "completed":
              site = tag2[0].text.strip() # need to remove the "rxn" from the beginning of the site string
              condensed_site = 'UNK'
              if site.startswith('site_2ndary') or site.startswith('secondary_site'):
                condensed_site = "NA_secondary"
              elif site.startswith('site_'):
                condensed_site = "NA_primary"
              elif site.startswith('hemagg'):
                condensed_site = "HA"
              n = tag2[1].text
              #name = outer_state[i] + '_' + str(site)
              if condensed_site not in bd_dict.keys():
                bd_dict[condensed_site] = int(n)
              else:
                bd_dict[condensed_site] += int(n)
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
    
    rxn_dict = {}
    #globlist = glob.glob(os.path.join(fhpd_dir, lig_dir_glob, results_name))
    results_filename = ""
    for ligfile in results_files:
      # read the results file
      #print "now reading result file:", ligdir
      results_filename = ligfile
      bd_dict = parse_bd_results(results_filename)
      rxn_dict = add_dictionaries(rxn_dict, bd_dict)
      
      
    
    # now we need to write a new results file
    #print "rxn_dict:", rxn_dict
    assert results_filename, "no results files were read."
    #print "results written to 'results_combined.xml'."
    #make_new_results_file("results_combined.xml", results_filename, rxn_dict)
    pprint(rxn_dict)
    
    

`
