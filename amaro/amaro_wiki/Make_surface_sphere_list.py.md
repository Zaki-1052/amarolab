# Make surface sphere list.py

`
    
    
    
    '''
    make_surface_sphere_list.py
    By Lane Votapka
    Amaro Lab 2015
    
    This program takes reaction criteria, the whole structure, and the surface structure, and generates a new surface structure including all atoms from the reaction file
    
    
    
    '''
    
    import pdb2 as pdb
    import sys, re, os
    from cStringIO import StringIO # NOTE: may want to change this to cStringIO if more speed is needed in the future
    import numpy as np
    import argparse
    import time
    import xml.sax as sax
    import cPickle as pickle
    #from surface_spheres import BrowndyeRxnHandler # reads Browndye reaction files. This does weird stuff to argparse when I import it
    
    pdb_parser=pdb.Big_PDBParser()
    
    class BrowndyeRxnHandler(sax.handler.ContentHandler):
      'parses a Browndye rxn file to find all the atomic pairs'
      def __init__(self):
        self.atoms_tags = []
        self._charBuffer = []
    
      def startElement(self, name, attrs):
        self.CurrentName = name
    
      def characters(self, content):
        if self.CurrentName == 'atoms':
          self._charBuffer.append(content.strip())
    
      def endElement(self, name):
        if name == 'atoms':
          ourbuffer = self._charBuffer
          print "ourbuffer", ourbuffer
          self.atoms_tags.append(''.join(ourbuffer).strip())
          self._charBuffer = []
    
      def parse(self, f):
        sax.parse(f,self)
        return self.atoms_tags
    
    def pickle_or_load(filename, picklename, struc_name="pickle",pqr=False, pqrxml=False):
      ''' for large files, instead of parsing, they can be saved and loaded much more quickly as a pickle. '''
      if os.path.exists(picklename) and os.path.getmtime(picklename) > os.path.getmtime(filename): # if the pickle has been most recently modified
        # load the pickle
        print "reading pickle:", picklename
        our_file=open(picklename, 'rb')
        our_obj=pickle.load(our_file)
        our_file.close()
      else:
        # then load the file itself and save the pickle
        our_obj = pdb_parser.get_structure(struc_name, filename, preserve_index = True, preserve_resid = True, pqrxml=pqrxml) # load the file
        print "writing pickle:", picklename
        our_file=open(picklename, 'wb')
        pickle.dump(our_obj, our_file, protocol=-1)
        our_file.close()
      return our_obj
    
    starttime = time.time()
    print "Parsing arguments"
    # parse the arguments
    parser = argparse.ArgumentParser(description="Takes reaction criteria, the whole structure, and the surface structure, and generates a new surface structure including all atoms from the reaction file. USE XML FILES FOR ALL ARGUMENTS!!")
    parser.add_argument('-s', '-spheres', dest="spheres", type=str, help="name of pqrxml file containing the entire molecule. Output of pqr2xml")
    parser.add_argument('-r', '-surface', dest="surface", type=str, help="name of pqrxml file containing the surface of the molecule. Output of surface_spheres")
    parser.add_argument('-o', '-output', dest="output", type=str, help="name of pqrxml output file of the new surface of the molecule")
    parser.add_argument('-1', '-rxn1', dest="rxn1", type=str, help="name of XML reaction file if molecule is first of pair")
    parser.add_argument('-2', '-rxn2', dest="rxn2", type=str, help="name of XML reaction file if molecule is second of pair")
    
    
    
    args = parser.parse_args() # parse the args into a dictionary
    args = vars(args)
    entire_filename = args['spheres']
    surface_filename = args['surface']
    output_filename = args['output']
    rxn1 = args['rxn1']
    rxn2 = args['rxn2']
    
    rxn_atoms = set() # a set of atoms that we must include
    assert not( args['rxn1'] and args['rxn2'] ), "both arguments -rxn1 and -rxn2 cannot be specified simultaneously"
    if args['rxn1'] or args['rxn2']: # if the reaction file is specified
      # open the reaction file, parse for the right indeces
      if args['rxn1']:
        rxn_filename = args['rxn1']
        rxn_index = 0
      elif args['rxn2']:
        rxn_filename = args['rxn2']
        rxn_index = 1
    
      rxn_atom_pairs = BrowndyeRxnHandler().parse(rxn_filename) #parse the xml file and get a list of all atoms pairs
      
      for pair in rxn_atom_pairs: # for each pair, get the desired index
        my_index = pair.split()[rxn_index] # got the index of the atom
        rxn_atoms.add(int(my_index)) # add the atom index to a set so that we can add it to the surface pqrxml
    
    # read the pqr files,
    print "Opening surface pqrxml file... time:", time.time() - starttime
    #surface=pickle_or_load(surface_filename, surface_filename+'.pkl', struc_name="surface", pqrxml=True)
    surface = pdb_parser.get_structure('surface file',surface_filename, preserve_index = True, preserve_resid = True, pqrxml=True)
    
    print "Opening entire pqrxml file... time:", time.time() - starttime
    #pdb_parser=pdb.Big_PDBParser()
    entire = pdb_parser.get_structure('entire file',entire_filename, preserve_index = True, preserve_resid = True, pqrxml=True)
    #entire=pickle_or_load(entire_filename, entire_filename+'.pkl', struc_name="entire", pqrxml=True)
    
    print "Looping thru atoms to find those involved with reactions... time:", time.time()-starttime
    
    i = 0
    next_surface_atom_index = surface.atoms[0].index
    
    #print "rxn_atoms:", rxn_atoms
    #print "len(surface.atoms):", len(surface.atoms)
    
    
    #exit()
    end_of_struct = False
    for atom in entire.atoms:
      if atom.index == next_surface_atom_index and end_of_struct == False:
        # increment to the next surface atom
        i += 1
        if i >= len(surface.atoms):
          end_of_struct = True
          continue
          
        try:
          next_surface_atom_index = surface.atoms[i].index
        except IndexError:
          print "encountered IndexError"
          print "i:", i
          print "next_surface_atom_index:", next_surface_atom_index
          print "atom.index:", atom.index
          raise Exception, "Printed status after error. Shutting down..."
        continue # we don't want to add this as a reaction atom unless its missing
      
      if atom.index in rxn_atoms:
        print "Adding atom index:", atom.index
        if end_of_struct:
          surface.atoms.append(atom)
        else:
          surface.atoms.insert(i,atom)
        surface.num_atoms += 1
        i += 1
    
    # print the pqr file
    print "Printing the output file... time:", time.time()-starttime
    #pqr.atoms = newatoms
    #pqr.num_atoms = len(newatoms)
    #print "newatoms[0].name", newatoms[0].name
    surface.save(output_filename, remark=False, standard=False, endmdl=False, pqrxml=True)
    #pqr.save('out_surface.pqr', remark=False, endmdl=False, pqrxml=True)
    
    endtime = time.time() - starttime
    print "Complete. total time:", endtime
    
    

`
