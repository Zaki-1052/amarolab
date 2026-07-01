# Renumberpdb.py

`
    
    
    
    #This script sets the resnum of every residue to 
    import sys
    #from Bio.PDB.PDBParser import PDBParser
    
    constant = -1543
    counter = 1
    xfile = open(sys.argv[1], 'r') #first argument: read pdb file
    filelist = []
    for line in xfile:
        linelist = line.strip().split()
        if linelist[0] ==  "ATOM":
            resnum = line[22:26].strip()
            newresnum = int(resnum.replace(' ',''))
            newresnum = newresnum+constant
            #print rmsflist[resnum]
            newresnum = str(newresnum)
            newresnum = " "*(4-len(newresnum)) + newresnum
    
            atomnum = "%7d" % counter # makes sure that the atom numbers start with 1
            line = ''.join((line[:4], atomnum, line[11:22], newresnum, line[26:]))
            counter +=1
        filelist.append(line)
        
    
    xfile.close()
    
    xfile = open(sys.argv[1], 'w') #second argument write pdb file
    for line in filelist:
        xfile.write(line)
    
    xfile.close()
                 
    
    

`
