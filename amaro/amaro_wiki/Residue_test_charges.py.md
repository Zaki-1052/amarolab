# Residue test charges.py

`
    
    
    <nowiki>
    ''' 
    By Lane Votapka
    Amaro lab 2014
    
    Generates test charge for each charged residue; 
    position is at center of charge for each residue. Uses standard 
    output. The input file must be pqr, the name is indicated in the 
    first argument
    *)
    '''
    
    import pdb2 as pdb
    import sys, re
    from cStringIO import StringIO # NOTE: may want to change this to cStringIO if more speed is needed in the future
    import numpy as np
    
    # helpfile
    if sys.argv[1].lower() in ['-h', '-help', '--help']:
      print "usage: python residue_test_charges INPUT_PQR_FILE > OUTPUT_XML_FILE"
      exit()
    
    # inherit the pqr parsers from pdb
    class Pqr_parser(pdb.Big_PDBParser):
      def test_charge_parse(self, filename, outfilename):
        '''this will parse a pqr file, calculate the test charges of each residue, and write that test charge at the center of charge'''
        if type(filename) == file or type(filename) == type(StringIO()): # then we're passing a file or file-like object
          pqrfile = filename
        elif type(filename) == str: # otherwise, try to open it as a string
          pqrfile = open(filename, 'r')
        counter = 1 # count each line of the file
        residcounter = 0
        oldresid = 0
        oldresname = ""
        this_resid_charge = 0.0 # the charge of the current residue
        this_resid_abs_charge = 0.0
        total_charge = 0.0 # the total charge of the entire molecule
        center_of_charge = np.array([0.0, 0.0, 0.0])
        outfile = open(outfilename, 'w')
        outfile.write("<root>\n")
        outfile.write("  <total-charge> 0.0000 </total-charge>\n")
        for pqrline in pqrfile:
          if not pqrline.startswith('ATOM') and not pqrline.startswith('HETATM'):
            continue
          rawlinelist = re.findall(pdb.pqrregex, pqrline)
    
          if not rawlinelist:
            linelist = pqrline.split() # then simply split on whitespace
            if len(linelist) == 10: # then the chain is missing
              linelist.insert(3,' ')
            #linelist.insert(2,'')
            #linelist.insert(6,'')
          try:
            linelist = rawlinelist[0]
            if oldresid == 0: 
              oldresid = linelist[5]
              oldresname = linelist[3]
            if linelist[5] != oldresid: # increment the resid counter
              # new residue - calculate the center of charge
              self.print_test_charge_xml(outfile, oldresname, int(oldresid), center_of_charge / this_resid_abs_charge, this_resid_charge)
              
              this_resid_charge = 0.0 # reset the charge of the current residue
              this_resid_abs_charge = 0.0
              center_of_charge = np.array([0.0, 0.0, 0.0]) # reset CoC
              residcounter += 1
              oldresid = linelist[5]
              oldresname = linelist[3]
            #if preserve_index:
            atomindex = linelist[1]
            #else:
              #atomindex = counter
            #if preserve_resid:
            resid_index = linelist[5]
            #else:
              #resid_index = str(residcounter)
            element=linelist[2][0]
            
            atom = pdb.Atom(record=linelist[0], index=atomindex, name=linelist[2], altloc='', resname=linelist[3], chain=linelist[4], resid=linelist[5], icode='', x=linelist[7], y=linelist[8], z=linelist[9], charge=linelist[10], radius=linelist[11], occupancy='1.0', beta='0.0', element=element)
            charge = float(linelist[11])
            x = float(linelist[7])
            y = float(linelist[8])
            z = float(linelist[9])
            pos = np.array([x, y, z]) # position of the atom
            center_of_charge += abs(charge) * pos # weigh the atom by its charge
            this_resid_charge += charge
            this_resid_abs_charge += abs(charge)
            total_charge += charge
          except IndexError:
            #print "failure line: %s" % pqrline
            #print "rawline: %s" % rawlinelist
            raise IndexError("failure line: %s, rawline: %s" % (pqrline, rawlinelist))
            
          #print atom.charge
        self.print_test_charge_xml(outfile, oldresname, int(oldresid), center_of_charge/this_resid_abs_charge, this_resid_charge)
        outfile.write("</root>\n")
        outfile.close()
        return total_charge
      
      def print_test_charge_xml(self, outfile, resname, resid, center_of_charge, charge):
        outfile.write("  <point>\n")
        outfile.write("    <residue> %s </residue>\n" % resname)
        outfile.write("    <residue_number> %d </residue_number>\n" % resid)
        outfile.write("    <atom-type> charge-center </atom-type>\n")
        outfile.write("    <x> %.4f </x> <y> %.4f </y> <z> %.4f </z>\n" % (center_of_charge[0], center_of_charge[1], center_of_charge[2]))
        outfile.write("    <charge> %.4f </charge>\n" % charge)
        outfile.write("  </point>\n")
        return 
        
    # make a number of important changes, such as requiring that the input pqr be 'slurped' and not loaded in all at once
    
    # load the pqr file and parse, writing while loading
    pqrfilename = sys.argv[1]
    newfilename = "DELETE_ME.xml"#sys.argv[2]
    parser = Pqr_parser()
    total_charge = parser.test_charge_parse(pqrfilename, newfilename)
    #print total_charge
    
    # now we need to reopen the file, and write to stdout in order to be able to write the total charge
    tmpfile = open(newfilename, 'r')
    index = 0
    for line in tmpfile.xreadlines(): # slurp the file
      if index == 1:
        print "  <total-charge> %.4f </total-charge>" % total_charge
      else:
        print line[:-1]
      index += 1
      
    
    </code>
    

</nowiki>`
