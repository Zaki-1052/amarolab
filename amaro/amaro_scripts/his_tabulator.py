#By Lane Votapka
# Amarolab 2011

'''
This script reads a pdb file and puts out a list of every Histidine, including
its residue number and resname in two different columns

Input:
 pdb file(s)

Output:
 text files containing a the residue number and residue name of each Histidine
'''

import sys, os
prefix = "histable_" #every file this script puts out will have this prefix

for pdbfilename in sys.argv[1:]: #for each file listed in arguments
    #open the file
    curfile = open(pdbfilename,'r')
    srcpdbname = pdbfilename.split('/')[-1]
    basename = srcpdbname.split('.')[0]
    destfilename = "%s%s.txt" % (prefix,basename)
    destfile = open(destfilename,'w')
    print destfilename
    #for each line in the file
    curresid = 0
    for line in curfile:
        splitline = line.strip().split()
        if splitline[0] == "ATOM":
            #print " ".join(line)
            resname = line[17:20]
            checkresid = int(line[22:26].strip())
            if checkresid > curresid: #then we have a new residue to report
                curresid = checkresid
                #print resname, checkresid
                if (resname == "HID") or (resname == "HIE") or (resname == "HIP") or (resname == "HIS"):
                    #write to the file
                    outline = '\t'.join((str(curresid),resname,'\n'))
                    #print outline
                    destfile.write(outline)
                    
    
    curfile.close()
    destfile.close()
