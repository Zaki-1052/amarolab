# Gaussian.py

`
    
    
    
    #Lane Votapka
    #UCI amaro lab
    
    '''
    Gaussian elimination program
     takes a matrix as an argument and finds
     the unique solution vector
    
    '''
    
    def _eschelonsolve(iarray,constants):
        '''
        resursive function that solves the eschelon
        '''
        if len(iarray) <= 1: #then we've reached the point where we can divide into the constant and return the result
            try:
                return [constants[0]/iarray[0][0]] #because these will be the only elements left
            except ZeroDivisionError:
                return ['No Solution']
        else: #then we are still dealing with a 2x2 array or larger
            #first find solution
            #print constants
            #print iarray
            #print 'constants:', constants
            try:
                solution = constants[-1]/iarray[-1][-1] #gives the solution to the final row of the eschelon
            except ZeroDivisionError:
                return ['No Solution']
            #now we need to calculate the new eschelon
            newarray = iarray[0:-1,:] #this is the upper left corner which will be called to the next recursion
            #need to calculate the new constants
            newconstants = constants[0:-1]
            
            #print 'newarray:', newarray
            for i in range(len(newconstants)): #excluding the last one
                #print i
                newconstants[i] = constants[i] - (newarray[i][-1]*solution)
            #print 'newconstants:', newconstants
            #print '======================================================='
            return _eschelonsolve(newarray[:,0:-1],newconstants) + [solution]
    
    from numpy import array,add,subtract,linalg
    import numpy
    import sys
    import math
    import time
    
    #Part 1: inputs
    M = array([[-4.0,0.0,4.0],
               [1.0,1.0,-1.0],
               [2.0,-3.0,1.0]])
    b = array([-1.0,2.0,1.0])
    size = len(M)
    print 'length:',size
    
    newM = M[:]
    newb = b[:]#[0] * len(M)
    eschelon = [M[0]]
    #print M[0]
    #Part 2: creating the eschelon
    for i in range(len(M)-1): #iteratively run through every L equation
        #print newM[0]
        Li = newM[0]
        pivot = float(Li[0]) #assign the pivot to the top corner
        newEqList=[]
        for f in range(1,len(newM)): #run through every OTHER equation now in newM
            #find the first element of the equation, compare to the pivot
            Lf = newM[f] #represents our L equation
            multiplier = -Lf[0]/pivot #find our multiplier
            scaledLi = Li * multiplier #scale our equation to cancel the pivot
            bi = newb[i] * multiplier #have to multiply the constant times the multiplier
            newLf = add(scaledLi, Lf) #add the equations
            newb[f+i] = bi + newb[f+i] #the new constant needs to be found for position f
            #print newLf
            newEqList.append([0]*(len(newM)-f)+newLf[1:]) #this will be a list of arrays
        #now we have the new equations in a list
        newM = array(newEqList[:])
        #print newM[0]
        eschelon.append(newM[0])
            
    #print eschelon
    #print newb
    eschelonmatrix = numpy.zeros((size,size))
    
    i=0
    for row in eschelon:
        #print row, eschelonmatrix,len(row)
        eschelonmatrix[i][-(len(row)):] = row
        i+=1
    print "U: ",eschelonmatrix
    print "b: ", newb
    #Part 3: solving the eschelon
    print _eschelonsolve(eschelonmatrix,newb)
    
    

`
