# this script is to run through a PQR file to find all instances of a
#protonated or deprotonated residue, whose names have been changed by
#pdb2pqr server.

#the script runs line by line, finding all instances where amino acid names
#fit a predefined tuple, it then writes a file containing the numbers of
# the residues that have had their names changed

#init
print "Running..."
import time
import pprint
starttime = time.time()
targets = ('GLH', 'LYN', 'ASH', 'ARN')
seqlist = []

# open necessary files
srcfile = "/scratch/lvotapka/projects/h3charge/1mql/1mql.pqr"

src = open(srcfile, 'r')
print "File successfully opened."

#now read through each line
lines = src.readlines()
#print lines[0]
for line in lines:
    line = line.strip().split()
    #print line
    if line[0] == 'ATOM':
        if line[3] in targets:
            if not (line[4] in seqlist):
                seqlist.append(line[4])

print seqlist
#NOTE: at this time, it only prints the results, this script does not yet write
# to a file!

#close the file
src.close()

#term
endtime = time.time()
print "Time elapsed: " + str(endtime - starttime)
print "Complete"
