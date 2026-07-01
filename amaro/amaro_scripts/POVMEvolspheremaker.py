"""
Script for changing occupancy in POVME sphere based on the contents of a
processed POVME volume contig pdb

Purpose: in order to visualize the changing volume contig files in vmd

"""

#A binary search will need to be run on the input sphere, as the filebase
# input pdbs are entirely out of order

#will need to return an index of the line we need to change


def pdbbinsearch(query,dataset,lower=0,upper=-1):
    '''
    function finds the query within a dataset by using a binary search method
    returns the index
    '''
    xloc = (32,38)
    yloc = (40,46) #character locations and slices for a pdb file
    zloc = (48,54)
    
    if upper == -1: upper = len(dataset) #if this is the first time using this function then set the upper bound
    if lower == upper: #then we've found it
        return lower
    else:
        #we have to determine whether the line in question is above or below the middle of upper and lower
        avg = (upper+lower)//2 #returns an int result
        middle = dataset[avg]
        xval = float(middle[xloc[0]:xloc[1]])
        yval = float(middle[yloc[0]:yloc[1]])
        zval = float(middle[zloc[0]:zloc[1]])

        qxval = float(query[xloc[0]:xloc[1]])
        qyval = float(query[yloc[0]:yloc[1]])
        qzval = float(query[zloc[0]:zloc[1]])

        #now see if we need to search above, below or neither
        if xval > qxval: #then we are looking too high, bisect the lower half of the data
            upper = avg
            #lower remains the same
        elif xval < qxval: #then we are looking too low, bisect the upper half of the data
            lower = avg + 1
        else:
            if yval > qyval: #then we are looking too high, bisect the lower half of the data
                upper = avg
                #lower remains the same
            elif yval < qyval: #then we are looking too low, bisect the upper half of the data
                lower = avg + 1
            else:
                if zval > qzval: #then we are looking too high, bisect the lower half of the data
                    upper = avg
                    #lower remains the same
                elif zval < qzval: #then we are looking too low, bisect the upper half of the data
                    lower = avg + 1
                else:
                    lower = avg #assign both to have the same value, the search ends here
                    upper = avg

        return pdbbinsearch(query,dataset,lower,upper)

import time, sys

print "Running..."
starttime = time.time()


#this file contains the template sphere
inputspherefile = "/home/lvotapka/Desktop/scratch/lvotapka/projects/N1pocketanalysis/1nn2_apo_tet/snapshots/POVMEpoints3.pdb"
occupancylocation = (56,60)

#this string represents all the input volume files
filebase = "/home/lvotapka/Desktop/scratch/lvotapka/projects/N1pocketanalysis/1nn2_apo_tet/snapshots/x1nn2_apo_%d.pdb"
volmax = 500

#This string will be where all the new spheres will be written to
outputfilebase = "/home/lvotapka/Desktop/scratch/lvotapka/projects/N1pocketanalysis/1nn2_apo_tet/snapshots/xPOVMEsphere%d.pdb"

#first read the sphere file and make a default, constant list
defaultspherelist = []
for line in open(inputspherefile,'r'):
    defaultspherelist.append(line)

spherelist = defaultspherelist[:] #make a copy of the default sphere list
#for each file in the folder
for volnum in range(1,(volmax+1)):
    tempfilebase = filebase % volnum
    tempfile = open(tempfilebase, 'r')
    for line in tempfile:
        if line[0:4] == 'ATOM':
            #need to perform the binary search now
            index = pdbbinsearch(line,spherelist) #this will tell us where it belongs
            oldstring = spherelist[index] #get the old line in the sphere
            oldstringlist = [oldstring[:occupancylocation[0]],oldstring[occupancylocation[1]:]] #break in into a list, excluding the occupancy region
            newstring = ''.join([oldstringlist[0],'0.00',oldstringlist[1]]) # join the list together, with occupancy at a new setting
            spherelist[index] = newstring #insert the changed line into the sphere

        
    outputfilename = outputfilebase % volnum #generate the output filename
    outputfile = open(outputfilename,'w')
    for line in spherelist:
        outputfile.write(line)

    spherelist = defaultspherelist[:] #need to reset the sphere list each time
    outputfile.close()
    tempfile.close()


print "Time to completion: ", time.time()-starttime
print "Complete"
