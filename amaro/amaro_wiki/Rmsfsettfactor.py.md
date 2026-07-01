# Rmsfsettfactor.py

`
    
    
    
    '''This script sets the occupancy of every residue to 
    argument 1: input pdb
    argument 2: RMSF program output
    argument 3: output pdb
    '''
    
    import sys
    byres = False # set to True if each line should be counted by residue, False if counted by atom
    filelist = []
    rmsflist = []
    xfile = open(sys.argv[1], 'r') #first argument: read pdb file
    for resid in open(sys.argv[2], 'r'): #read the rmsf output file
        resid = resid.strip().split()
        rmsflist.append(float(resid[1]))
    for line in xfile:
        linelist = line.strip().split()
        if linelist[0] ==  "ATOM":
            resnum = int(line[22:26].strip())
            atomnum = int(line[4:11].strip())
            #print rmsflist[resnum]
            if byres == True: # then we are counting by residue number
                line = ''.join((line[:56],'%.2f' % rmsflist[resnum-1],line[60:]))
            else: # then we are counting by atom number
                line = ''.join((line[:56],'%.2f' % rmsflist[atomnum-1],line[60:]))
                
        filelist.append(line)
    
    xfile.close()
    
    xfile = open(sys.argv[3], 'w') #third argument write pdb file
    for line in filelist:
        xfile.write(line)
    
    xfile.close()
                 
    
    

`
