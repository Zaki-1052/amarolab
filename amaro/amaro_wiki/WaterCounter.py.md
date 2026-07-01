# WaterCounter.py

`
    
    
    
    #By Lane Votapka
    #Amarolab at University of California, Irvine
    
    '''
    This script runs through a PDB, counting how many water residues there are
    and then using the number to calculate the number of ions that should be
    added, printing the value
    
    commandline (1 script argument):
    python WaterCounter.py <input pdb> <desired ion concentration(mol/L)> [<resid column>]
    
    '''
    import sys
    #resindex = 3
    
    def ioncalc(numwater,molarity):
        #(0.02 mol/L)(1E-27 L/Angstrom)(Volume)(6.022E23 atoms/mol) = # atoms
        numions = (0.0187 * numwater * molarity)/3
        return numions
    
    def processPdb(filename,resindex):
        numwater = 0
        for line in open(filename,'r'):
            linelist = line.strip().split()
            if linelist[0] == "ATOM":
                resid = linelist[resindex]
                if resid == 'WAT' or resid == 'HOH': numwater += 1
        return numwater
    
    
        
    
    if __name__ == "__main__":
        #print "Water Counter Running..."
        import time
        import pprint
        starttime = time.time()
        try:
            pdb = sys.argv[1]
            molarity = float(sys.argv[2])
            try:
                resindex = int(sys.argv[3])#assign which column in pdb has water designation
            except IndexError: #then go to default
                resindex = 3
            numwater = processPdb(pdb,resindex)
            numions = ioncalc(numwater,molarity)
            print numions
        except IndexError:
            raise Exception, "incorrect arguments entered. Arg1=<file>, Arg2=<molarity>, [Arg3=<residue column>]"
        endtime = time.time()
        #print "Time elapsed: " + str(endtime - starttime)
        #print "Complete"
    
    

`
