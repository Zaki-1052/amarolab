# ResidueComparePairwise.py

`
    
    
    
    #By Lane Votapka
    #Amarolab UCI 2011
    
    '''
    Pairwise protein Residue distance calculator
    
    Takes a pdb, parses the residues by coordinates, then makes a matrix containing
    the a given comparison between every residue type
    '''
    import sys, os, time
    from pprint import pprint
    
    import math
    from math import sqrt
    from numpy import subtract
    from numpy.linalg import norm
    from Bio.PDB.PDBParser import PDBParser
    p=PDBParser(PERMISSIVE=1)
    
    #==============================================================================
    #decision functions
    
    def mean(iterable):
        '''returns the mean of an iterable'''
        num=len(iterable)
        assert num > 0, "iterable must not be empty to find the mean"
        return sum(iterable)/float(num)
    
    def median(iterable):
        '''returns the median of an iterable'''
        num=len(iterable)
        assert num > 0, "iterable must not be empty to find the median"
        if num%2 == 1: #the list contains an odd number of elements
            index = math.floor(num/2.0) #find the index of the middle element
            return iterable(index)
        else: #the list contains an even number of elements
            index = num/2.0 #this is the upper number's index
            value = (iterable[index-1] + iterable[index])/2.0 #get the average of the middle two elements
            return value
    
    #=============================================================================
    #comparison functions
    
    def pairwise_distance(querylist,probelist):
        distspread=[]
        for g in xrange(len(querylist)): #for each coordinate, get an index
            qcoord=querylist[g]
            for k in xrange(len(probelist)): #for each coordinate in the probe, get an index
                pcoord=probelist[k]
                diffvec = subtract(qcoord,pcoord)
                dist=norm(diffvec)
                #print "dist: ",dist
                if dist > 0.0: distspread.append(dist)
        return distspread
    
    
    #=============================================================================
    #procedure functions
    def _get_resdict(pdbfilename):
        '''
        parses and returns the coordinates of every CA atom within a PDB file
    
        returns as a dictionary, the key of which is a RESNAME, the items
        '''
        totalreslist=[]
        resdict={}
        totalresidues=0
        #first parse the PDB file:
        parser=PDBParser()
        s=parser.get_structure('pdb',pdbfilename) #this gets the structure
        m=s[0]
        #for each chain, get all the residues into a list
        for chainname in m.child_dict.keys():
            chain = m[chainname]
            reslist = chain.get_list()
            totalreslist=totalreslist+reslist
            #now that we have all the residues in a list, go through each one
        for residue in totalreslist:
            resid=residue.get_id() #this will give us the name of our residue
            resname=residue.get_resname()
            #print "resname: ",resname
            if residue.has_id("CA") and resid[0]==" ":
                ca=residue['CA']#alpha carbon
                rescoord=ca.get_coord() #coordinates of the alpha carbon
                if resname not in resdict.keys(): #then we need to add a new entry
                    resdict[resname]=[rescoord]
                else:
                    #in this part, we're appending every coordinate of a given residue
                    oldrescoordlist = resdict[resname]
                    oldrescoordlist.append(rescoord)
                    resdict[resname]=oldrescoordlist
                totalresidues+=1
        #print "total number of residues:",totalresidues
        return resdict
    
    def _get_distlist(resdict,decisionfunction,comparisonfunction,ESCHELON=True):
        '''
        returns the pairwise minimum matrix for every residue
    
        function can be min,mean,median,etc. as long as it takes a list
        as an argument and returns a value
        '''
        restuple = tuple(resdict.keys())
        distmatrix=[]
        #iterate through each element in the dictionary, pulling out the minimum
        for i in xrange(len(restuple)):
            #we are going to query every residue
            query = restuple[i]
            matrixrow = [] #the list that represents the current row in the matrix
            if ESCHELON==True: #Eschelon variable determines whether we assume that this will identical to either side of the diagonal
                startprobe=i #we only need a decreasing iteration
            else: #otherwise, we think that the matrix will be non-identical across the diagonal
                startprobe=0 #every element pairwise, this takes twice as long
            for f in xrange(startprobe,len(restuple)):
            #we are going to probe every other residue down the line
                probe = restuple[f]
                distspread = [] #represents every distance between the query and each probe
                #now we will need to measure the distance of every single query
                # and probe coordinate
                querylist = resdict[query]
                probelist = resdict[probe]
                distspread=comparisonfunction(querylist,probelist)#we have all the distances in a list for a particular residue pair
                #print "distspread:", distspread
                if len(distspread) > 0:
                    value = decisionfunction(distspread) #value represents the number that we want after processing the entire list of distances
                else:
                    value = None
                matrixrow.append(value) #keep adding elements to the current row in the matrix
            distmatrix.append(matrixrow)
        return distmatrix
        
    if __name__ == "__main__":
        print "Running..."
        starttime = time.time()
        pdbfilename = '/home/lvotapka/tmp/1UBQ.pdb'
        resdict=_get_resdict(pdbfilename)
        distmatrix=_get_distlist(resdict,decisionfunction=mean,comparisonfunction=pairwise_distance, ESCHELON=False)
        #pprint(distmatrix)
        #get the residues in their proper order
        reslist=resdict.keys()
        topline=['---'] + reslist
        #sideline = reslist #redundant
        #write the matrix:
        dest=open('/home/lvotapka/tmp/UBQdistmatrixmean.txt','w')
        dest.write('\t'.join(topline))
        dest.write('\n')
        for i in xrange(len(distmatrix)):
            line = distmatrix[i]#concatenate the line string with the resname
            #print the beginnning of each line
            dest.write(reslist[i] + '\t')
            for value in line:
                #print value
                #write appropriate spaces
                numspaces=len(distmatrix)-len(line)
                dest.write("   \t"*numspaces)
                #write the numbers
                if value == None: value = 0.0
                dest.write("%5.2f" % value)
                dest.write('\t')
            dest.write('\n')
        dest.close()
    
        endtime = time.time()
        print "Complete"
        print "Total running time: ", endtime-starttime
    
    

`
