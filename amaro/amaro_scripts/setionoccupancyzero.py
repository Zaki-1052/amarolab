#This script sets the occupancy of Na+ and Cl- ions in a pdb file to zero
import sys
filelist = []
xfile = open(sys.argv[1], 'r') #first argument: read pdb file
for line in xfile:
    linelist = line.strip().split()
    if linelist[0] ==  "ATOM" and (linelist[3] == 'Na+' or linelist[3] == 'Cl-' or linelist[3] == 'K+'):
        line = ''.join((line[:56],'0',line[57:]))
    filelist.append(line)

xfile.close()

xfile = open(sys.argv[2], 'w') #second argument write pdb file
for line in filelist:
    xfile.write(line)

xfile.close()
