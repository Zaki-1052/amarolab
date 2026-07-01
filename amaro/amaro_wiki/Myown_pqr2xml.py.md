# Myown pqr2xml.py

`
    
    
    
    # scans jacobs virus file for how many fields are in each line
    '''
    myown_pqr2xml.py
    
    by Lane Votapka, Amaro lab 2014
    
    uses pdb2.py to parse a pqr file, then write to a pqrxml. It's not optimally memory
    efficient, but as long as the structure can fit in memory, it works!
    
    usage:
    
    python myown_pqr2xml.py pqr_file pqrxml_file
    
    Maybe someday I can modify this program to slurp the pqr file and write the pqrxml file one line at a time
    
    '''
    
    
    import unittest, time, argparse, sys
    import pdb2 as pdb
    import numpy as np
    
    '''
    filename='virus_noh.pqr'
    
    ourfile = open(filename,'r')
    lastresname = ''
    lastresid = 0
    counter = 1
    
    print "<roottag>"
    
    def parse_pqr_line(pqr_line):
      return_lines = []
      line = (pqr_line.strip().split())
      atomname = line[2]
      resname = line[3]
      resid = int(line[4])
      x = float(line[5])
      y = float(line[6])
      z = float(line[7])
      chg = float(line[8])
      rad = float(line[9])
      if resname != lastresname or resid != lastresid:
        if lastresname != '': return_lines.append("  </residue>")
        lastresname = resname
        lastresid = resid
        #print "line number %d has %d fields" % (counter, numfields)
    
        return_lines.append("""  <residue>
        <residue_name>%s</residue_name>
        <residue_number>%d</residue_number>""" % (resname, resid))
    
      return_lines.append("""    <atom>
          <atom_name>%s</atom_name>
          <atom_number>%d</atom_number>
          <x>%f</x>
          <y>%f</y>
          <z>%f</z>
          <charge>%f</charge>
          <radius>%f</radius>
        </atom>""" % (atomname, counter, x, y, z, chg, rad))
    
      return '\n'.join(return_lines)
    
    for line in ourfile.xreadlines():
      if not line.startswith('ATOM'): continue
      print parse_pqr_line(line)
      counter +=1
    
    
    
    print """  </residue>
    </roottag>"""
    
    class Test_apbs_functions(unittest.TestCase):
      # several test cases to ensure the functions in this module are working properly
      def test_main(self): # test this function
        pass
    
    
    
    if __name__=="__main__":
      #unittest.main()
      pass
    '''
    starttime = time.time()
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    if len(sys.argv[3]) > 3:
      xmloutfilename = sys.argv[3]
    
    
    # read the pqr file,
    print "Opening pqr file... time:", time.time() - starttime
    parser=pdb.Big_PDBParser()
    pqr = parser.get_structure('pqr file',infilename, preserve_index = False, preserve_resid = True, pqr=True)
    
    print "Printing the output pqr file... time:", time.time()-starttime
    pqr.save(outfilename, remark=False, standard=False, endmdl=False, pqr=True) #pqrxml=True)
    
    if len(sys.argv[3]) > 3:
      xmloutfilename = sys.argv[3]
      print "Printing the output pqrxml file... time:", time.time()-starttime
      pqr.save(xmloutfilename, remark=False, standard=False, endmdl=False, pqrxml=True) #pqrxml=True)
    
    print "Complete. Total time:", time.time()-starttime
    
    

`
