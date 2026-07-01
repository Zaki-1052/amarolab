# by Lane Votapka

threshold = 5.0
goodlist = []
weightlist = []
src_node = 430
dest_node = 454

print "running..."
# recursive graph path method
print "parsing graph"
import numpy as np
from numpy import reshape, fromfile
import sys, os
import networkx as nx
import matplotlib.pyplot as plt
from time import time
starttime = time()

from pprint import pprint


def recurse(oldlength, parentnode, pastlist, destnode, depth):
    '''brute force method '''
    if oldlength > threshold: return #we've gone past our maximum length, take a step back
    #successors = G.neighbors(parentnode)

    for i in G[parentnode].keys(): #successors:
        if i in pastlist: continue # don't want to take any steps back
        newlength = oldlength + G.edge[parentnode][i]['weight'] #add the newest weight to the path
        if newlength > threshold: continue # then the path is too long, we don't want it
        newlist = pastlist + [i]
        if i == destnode: #then we have found a path under the threshold
            goodlist.append((newlength,newlist[:])) # add this path to our goodlist
            print "good path: ", newlist[:]
            weightlist.append(newlength) # add this weight to our weightlist
            return # this branch has been fully explored
        else: # then continue the search
            if depth == 0: print "exploring another branch from source node"
            recurse(newlength,i,newlist[:],destnode, depth + 1)
            
    return


bestpaths = [] #a list that is pushed and popped for the best paths
resdict = {}
# bestpath tuple: (pathlength,path)
def bubblesort(mainlist,newelement):
    '''bubble sorts the newelement into the mainlist'''
    #divide and conquer
    listlen = len(mainlist)
    if listlen == 0: # its the only element in the list so far
        mainlist.append(newelement)
        return
    
    low = 0 #our lower bound is the first index
    high = listlen - 1 #our upper bound is the last index
    mid = high / 2 #get the middle index of the list
    curweight = newelement[0] #have to get the weight from the tuple
    #print mainlist, newelement
    while high <> low:
        checkweight = mainlist[mid][0] # get the weigth from the mid tuple
        if curweight > checkweight: # then we are going to the lower half
            high = mid #reset the high index to the previous middle
            mid = (high + low)/2
        else: # going to the upper half
            low = mid+1
            mid = (high + low)/2
        #print high, ',', low

    checkweight = mainlist[high][0]
    if curweight > checkweight: #then insert before
        mainlist.insert(high,newelement)
    else:
        mainlist.insert(high+1,newelement)
        
    return

def heurist(parentnode,currentpath, currentpathlength):
    '''heuristic method for searching for the best path'''
    global bestpaths
    global resdict
    # check to see if we've found
    if parentnode == dest_node:
        print "bestpath", currentpathlength, currentpath
        goodlist.append((currentpathlength,currentpath))
        return
    
    # look for all children of the parentnode
    #successors = G.neighbors(parentnode)
    #successorlist = []
    for i in G[parentnode].keys():
        if i in currentpath: continue # don't want to take any steps where we've already been
        
        segdist = G.edge[parentnode][i]['weight'] #get the distance from the parent to this successor
        newdist = segdist + currentpathlength
        ''' #activate this section if you are interested in the optimal path ONLY - it keeps track of the best way to get to any given node
        if i in resdict: #then there may be a better way to get to this node
            recorddist = resdict[i] #get the old recorded weight
            if newdist < recorddist: #then we've found a new best way to get to this residue, so change the record entry and continue
                resdict[i] = newdist #make the new entry
                #allow to finish this iteration
            else: #then we have a previous better way to reach this node, there's no need to continue down this path
                continue
        else: #there is no entry yet for this node
            resdict[i] = newdist # add it
        '''
        if newdist <= threshold: #only if this child node will possibly give us a good path
            newpath = currentpath + [i]
            maketuple = (newdist,newpath)
            #print "adding something to bestpaths"
            bubblesort(bestpaths,maketuple)
            #print "current best paths", bestpaths
            #if len(bestpaths) > 20: return

    
    return

########## parsing ################



# 1: parse section

A=reshape(fromfile('contact.dat', sep=' '),(456,456))
G=nx.Graph(data=A)
#print G.edges()


########## recursion ##############
print "now performing recursive search for optimal paths"
recurse(0.0, src_node, [src_node], dest_node,depth=0)

#now that all possibilities have been added to bestlist, choose the best to continue down
'''
bestpaths = [(0.0,[src_node])]
counter = 0
while bestpaths:
    bestpath = bestpaths.pop() # get the best member of the list
    newlength = bestpath[0]
    newpath = bestpath[1]
    newnode = newpath[-1] # the last member of the path will be the new node
    #print "calling new recursion"
    heurist(newnode,newpath,newlength)
    counter += 1
    if counter % 1000 == 0: print "current iteration: ", counter, "length of bestpaths: ", len(bestpaths)

#heurist(src_node,[src_node],0.0)
'''
goodlist.sort()
pprint(goodlist)
print "elapsed time: ", time() - starttime, "s"
print "complete"
