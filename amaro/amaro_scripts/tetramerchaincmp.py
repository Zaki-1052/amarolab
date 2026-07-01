#this script is going to try and read a pdb file with a tetramer of two subunits
# and compare the contents of them

from pprint import pprint
import amarolab.amaro.amaro_scripts.moduseful as moduseful

def checkiflisthomogeneous(ilist):
    if len(ilist) == 0: return True
    firstelement = ilist[0]
    for i in range(len(ilist)):
        #check every element and see if its equal to first element
        if ilist[i] <> firstelement:
            return False
    #if it makes it this far, its true
    return True

#first, open the pdb

filename = '/scratch/lvotapka/projects/h3charge/MS1985/fxd1.pdb'
chainAlen = 328
chainBlen = 175
chaintotlen = chainAlen + chainBlen
chainAlist = []
chainBlist = []
reslist = []
i=0
terminateloop = 1510
onresid = 0
resid = ''

src = open(filename, 'r')

while onresid < terminateloop:
    line = src.readline()
    curresid = int(line[22:26].strip()) #get the residue number on the current line, and convert it to an integer
    #print "curresid: ",curresid
    line = line.strip().split()
    if (curresid > onresid): #if we have a new residue
        if (onresid <> 0):
            reslist.append(resid)
            #print "resid: ",resid
        resnum = onresid % chaintotlen
        #onresid = curresid
        
        resid = line[3]
        #now check if this one is the beginning of a new chain
        if (resnum == 0) and (onresid <> 0):
            #that means it belongs in the chainAlist
            chainAlist.append(reslist[:chainAlen])  #append the A portion to this list
            chainBlist.append(reslist[chainAlen:])  #append the B portion to this other list
            reslist = [] #reset the temporary list
        onresid = curresid
    i += 1 #count every line

print len(chainAlist)
print len(chainAlist[0])
print len(chainAlist[1])
print len(chainAlist[2])

for chainlist in (chainAlist,chainBlist):
    for i in range(len(chainlist[0])):
        quicklist = []
        for f in range(len(chainlist)):
            quicklist.append(chainlist[f][i])
        if checkiflisthomogeneous(quicklist) == False:
            quicklist.append("*misidentity*")
        nstring = "\t".join(quicklist)
        print nstring



#for line in src: #for every line
#    line = line.strip().split() #strip and split
#    resid = line[3] #get the AA residue name
#    resnum = i % chaintotlen #get the relative position on the tetramer subunit
#    reslist.append(resid)   #append the residue name to the temporary list
#    
#    if (resnum == 0) and i <> 0: #if we reach a new chain and if its not the beginning
#        #that means it belongs in the chainAlist
#        chainAlist.append(reslist[:chainAlen])  #append the A portion to this list
#        chainBlist.append(reslist[chainAlen:])  #append the B portion to this other list
#        reslist = [] #reset the temporary list
#    i += 1 #count all of these

    #NOTE: this counts by line, we need something that will count by residue
    #use while loop less than terminating resid number. Check for new resid
    #number and place the resid into a list
