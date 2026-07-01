#TetramerVector

'''
This script takes a pdb that contains a tetramer (or potentially a dimer
or trimer with some modification) and finds all equivalent atoms within the
backbone of the protein, finds the planes of them all, and returns the
average normal vector

'''
from numpy import array,subtract,linalg,add
from numpy import cross
import numpy
import sys
import time
from pprint import pprint

filename = '/scratch/lvotapka/projects/N1pocketanalysis/3nss_apo_tet/3nss_apo_tet_nowater_align.pdb'
chainlen = 387
monomers = 4

residuenum = (22,26)
backboneatoms = ('N','CA','C','O')

def findnorm(coordlist):
    '''
    takes a list argument of exactly three strings, which are coordinates
    separated by a space.

    finds the cross product of the vectors
    returns the cross product in the form of a vector
    '''
    assert len(coordlist) == 3, 'findnorm function reqires exactly three coordinates'
    coord1 = array(map(float,coordlist[0].split())) #this will be the reference coordinate
    coord2 = array(map(float,coordlist[1].split()))
    coord3 = array(map(float,coordlist[2].split()))

    #print coord1
    #print coord2
    #print coord3
    
    a = subtract(coord2, coord1)
    #print a
    b = subtract(coord3, coord1)
    #print b
    norm = cross(a,b) #use the numpy function 'cross' to get the normal
    if norm[2] < 0: #then the z is a negative number and we want it pointing the other way
        norm = norm * -1.0
    #print "norm:"
    #print norm
    return norm


def normalize(vec):
    return vec/linalg.norm(vec)
    

def findcombosinset(iset,combolen,depth=0,index=0,triangle=[]):
    '''
    NOTE: nonfunctional
    this function finds all triplet combinations in a set

    then returns a list of all combinations
    '''
    setlen = len(iset)
    if depth == 0: #we're just starting
        trianglelist = []
        depth = 0
        
        triangle = []
    
    #depth += 1 #if the depth is zero(top of list) we are not checking element #1
    if (depth == combolen): #then we have three of our elements
        print triangle
        triangle.pop()
        return
    else:
        for i in range(index,setlen):
            triangle.append(iset[i])
            findcombosinset(iset,combolen,depth+1,i+1,triangle)
        if triangle: triangle.pop()

def averagevectors(veclist):
    '''
    function returns the average of a list of vectors
    '''
    numvecs = len(veclist)
    totvecs = array([0,0,0])
    for vec in veclist:
        totvecs = add(totvecs,vec)

    avg = totvecs/numvecs
    #print avg
    return avg

def avgnorm(coordlist):
    '''
    this function takes a list of strings, each containing coordinates

    it returns the norm of these coordinates
    '''
    coordlistlen = len(coordlist)
    if coordlistlen < 3:
        raise Exception('cannot find norm with only two coordinates')
    elif coordlistlen == 3:
        norm = findnorm(coordlist)
    elif coordlistlen == 4:
        normlist = []
        for i in range(coordlistlen):
            previndex = i-1
            if previndex < 0: previndex = coordlistlen-1 #its going to wrap to the other side
            nextindex = i+1
            if nextindex >= coordlistlen: nextindex = 0 #its goign wrap to the beginning
            tripletlist = (coordlist[i],coordlist[previndex],coordlist[nextindex])
            #print "tripletlist: "
            #print tripletlist
            normlist.append(findnorm(tripletlist))
        avgvec = averagevectors(normlist)
        return avgvec

    #else: #then we have some other arbitrary number of coordinates
    #    #so for each element of the coordlist, we need to get all possible
    #    #triangles, and find the norm of them all, averaging them#

    #    #the number of triangles is going to be len(coordlist) factorial
    #    trianglelist = findcombosinset(coordlist)
    #    normlist=[]
    #    for element in trianglelist:
    #        normlist.append(findnorm(trianglelist[i]))
    #    avgvec = averagevectors(normlist)
    #    return avgvec
        

starttime = time.time()
print "Running..."



#Main body
#step 1: Read pdbs and assign all backbone atoms to lists

pdblinelist = []
tetlist = [] #contains the lists that will hold
oldresnum = 0
index = 0
for line in open(filename,'r'):
    if line[0:4] == "ATOM":
        #pdblinelist.append(line) #only append if its an atom
        newresnum = int(line[22:26].strip())
        
        if newresnum <> oldresnum: #then we're moving to a different residue
            #now is the time to check if we need to append to a new list
            if (index % (chainlen) == 0) and (index <> 0): #then its a time to append to a new list
                tetlist.append(pdblinelist[:])
                pdblinelist = []
            index += 1
        #now we must check to add only backbone atom lines
        curatom = line[13:16].strip()
        #print curatom
        if curatom in backboneatoms:
            pdblinelist.append(line[31:54])
        oldresnum = newresnum
tetlist.append(pdblinelist[:]) #at the end we want to append the last chain
#we now have all the backbone atoms of a pdb file separated into four tetramers

#pprint(tetlist)


#step 2: read coordinates of each of the equivalent atom sets, giving us
# 4 coordinates each. Find the 4 planes, then the normals of the planes,
# then normalize and average the normals

tetchainlen = len(tetlist[0])
#print len(tetlist[0])
#print len(tetlist[1])
#print len(tetlist[2])
#print len(tetlist[3])
normlist = []
for i in range(tetchainlen):
    fourvecs = []
    #print len(tetlist)
    #print len(tetlist[0])
    for f in range(monomers):
        fourvecs.append(tetlist[f][i])
    # we should now have a list fourvecs which contains strings specifying
    # the four coordinates of our plane
    #print "fourvecs: "
    #pprint(fourvecs)
    norm = avgnorm(fourvecs) #get the normal vector to the four coordinates
    #print "oldnorm: ", norm
    norm = normalize(norm) #we must normalize this vector
    #print "normalized: ", norm
    normlist.append(norm)

#step 3: take all the normals and average them, returning the average normal
#print normlist
universalnormal = averagevectors(normlist)
print "universal norm: ", universalnormal

print "Complete"
print "Time Elapsed: ", time.time() - starttime
