# by Lane Votapka
#Amarolab UCI 2011

'''
Script that takes a file of coordinates (as taken over time) as input and
processes it by performing useful analyses such as:
- RMSF
- least squares line fitting
- fitting of other shapes...

Input:
 The file to read

Output:
 The information of the trajectory

'''
import sys, os
from amarolab.amaro.amaro_scripts.moduseful import length
from amarolab.amaro.amaro_scripts.moduseful import transpos #gets the transpos (reflected) of a 2D list
from math import sqrt, pi
import math
import time



testfilename = '/scratch/lvotapka/testdots.txt' #a test input

def time_average(coords):
    '''calculate the time avg. coordinates of all the coordinate set'''
    totaltime = len(coords) #number of coordinate sets
    sumx = 0; sumy = 0; sumz = 0 #setting all sum variables to initial values
    for i in coords: #an integer value counter for each entry in coords
        sumx += float(i[0])
        sumy += float(i[1]) #summing together all the coordinates
        sumz += float(i[2])
    avgx = sumx/totaltime
    avgy = sumy/totaltime #dividing by the total time to yield the average coordinate
    avgz = sumz/totaltime
    return (avgx,avgy,avgz) #returning a tuple of the time average

def RMSF(coords,timeavg=None):
    '''Calculates the RMSF for all coordinates
    NOTE: this function will calculate timeavg for itself if necessary, but it
    would save time if this was already calculated elsewhere to pass it as an
    argument
    '''
    totaltime = len(coords) #number of steps
    if not timeavg: timeavg = time_average(coords) #if we have no time average passed as an argument, then we'll calculate it ourselves
    diffsum = 0 #initializing variables representing the sum of fluctuation coordinates
    for i in coords: #for each timestep
        curx = float(i[0])
        cury = float(i[1])
        curz = float(i[2])
        diffx = curx - timeavg[0] #get the difference in X value
        diffy = cury - timeavg[1] #get the difference in Y value
        diffz = curz - timeavg[2] #get the difference in Z value
        diffsum += (length((diffx,diffy,diffz))) ** 2 #getting the square of this value
    rmsf = sqrt(diffsum/totaltime) #returns the rmsf
    return rmsf

def _Sfunct(xk1,xk2,xm1,xm2,n):
    '''takes two lists of coordinates, and their mean value, calculates
    S portion for least squares: '''
    sumS = 0.0
    for i in xrange(n): #for each coordinate
        sumS += (xk1[i]*xk2[i] - xm1*xm2) #find the sum of all points and their distance from the mean point
    S = sumS/n
    return S
        

def least_squares_linear(coords,timeavg=None):
    '''Calculates the least-squares line L for a set of 3D points. The ends of the
    line correspond to the furthest out points. Also returns the overall
    uniformity of the points (how closely they match the line)

    Formulas copied from article "3D Linear Regression" by Jean Jacquelin

    Input:
        3D coordinates

    Output:
        2 coordinates indicating the ends of the line (tuple)
        uniformity of the points (float)
    '''
    if not timeavg: timeavg = time_average(coords) #if we have no time average passed as an argument, then we'll calculate it ourselves
    #forgive my terse variable names, I'm doing this for consistency with a formula
    n = len(coords) #total number of points
    transcoords = transpos(coords) #getting the transpos of the input coordinates, to separate x from y from z
    xcoords = transcoords[0]; ycoords = transcoords[1]; zcoords = transcoords[2] #assigning the full sets of x,y,z coordinates
    Xm = timeavg[0]
    Ym = timeavg[1] #mean coordinate set
    Zm = timeavg[2]
    #print "Xm:", Xm, "Ym:", Ym, "Zm:", Zm
    Sxx = _Sfunct(xcoords,xcoords,Xm,Xm,n)
    Syy = _Sfunct(ycoords,ycoords,Ym,Ym,n)
    Szz = _Sfunct(zcoords,zcoords,Zm,Zm,n) #this represents the mean distance of every point from the mean point
    Sxy = _Sfunct(xcoords,ycoords,Xm,Ym,n)
    Sxz = _Sfunct(xcoords,zcoords,Xm,Zm,n)
    Syz = _Sfunct(ycoords,zcoords,Ym,Zm,n)
    #print "S: ", Sxx, Syy, Szz, Sxy, Sxz, Syz
    c0 = Sxy*Sxz*(Szz-Syy) + Syz*(Sxy**2-Sxz**2) #terms of an equation that will help us find 'a'
    c1 = Sxz*Syz*(2*Sxx - Syy - Szz) + Sxy*(-(Sxy**2) - Sxz**2 + 2*(Syz**2)) + Sxy*(Szz-Sxx)*(Szz-Syy)
    c2 = Sxy*Sxz*(Sxx + Syy - 2*Szz) + Syz*(Sxz**2 + Syz**2 - 2*(Sxy**2)) + Syz*(Sxx-Syy)*(Szz-Sxx)
    c3 = Sxz*Syz*(Syy-Sxx) + Sxy*(Sxz**2 - Syz**2)
    #print "c:", c0, c1, c2, c3
    #a is a root of the cubic equation: C3a^3+c2a^2+c1^a+c0 = 0
    r = c2/c3; s = c1/c3; t= c0/c3 #just solving the above equation...
    #print "r:", r, "s:", s, "t:", t
    p = s - (r**2/3); q = (2*(r**3))/27 - (r*s/3) + t; R = (q**2)/4 + (p**3)/27 #solving the above equation
    #print "p:", p, "q:", q, "R:", R
    if R > 0:
        a = -(r/3) + (-q/2 + sqrt(R))**(1.0/3) + (-q/2 - sqrt(R))**(1.0/3)
        #print "a:", a
        a = [a]
    else: #if R < 0
        rho = sqrt(-p**3 / 27)
        phi = math.acos(-q/(2*rho))
        a1 = -(r/3) + 2*(rho**(1.0/3))*math.cos(phi/3)
        a2 = -(r/3) + 2*(rho**(1.0/3))*math.cos((phi + 2*pi)/3) #NOTE: I had to make sure that any integer division was changed to float
        a3 = -(r/3) + 2*(rho**(1.0/3))*math.cos((phi + 4*pi)/3)
        #print "rho:", rho, "phi:", phi, "a:", a1, a2, a3
        a = [a1,a2,a3]
    #a and b represent the perp plane of our line L in the formula z=ax+by
    minSigmadk = None #this variable stores the current lowest
    secminSigmadk = None #our second lowest (useful for plane)
    b=0;u=0;v=0;w=0 #setting our secondary plane coordinates first to avoid errors
    distlist = []; secdistlist = []
    dictinfo = {} #dictionary that will store the information for all three principal axes
    for temp_a in a: #since we may have up to three different possible values for a, we need to make sure to account for each one
        temp_b = (temp_a*(Szz-Sxx) + (1 - temp_a**2)*Sxz)/(Sxy + temp_a*Syz)
        temp_u = (1+temp_a**2+temp_b**2)**(-1) * ((1+temp_b**2)*Xm - temp_a*temp_b*Ym + temp_a*Zm)
        temp_v = (1+temp_a**2+temp_b**2)**(-1) * ((1+temp_a**2)*Ym - temp_a*temp_b*Xm + temp_b*Zm) #these coordinate correspond to where the line L crosses the plane PI
        temp_w = (1+temp_a**2+temp_b**2)**(-1) * ((temp_a**2 + temp_b**2)*Zm + temp_b*Ym + temp_a*Xm)
        sum_xk = 0; sum_yk = 0; sum_zk = 0
        temp_distlist = [] #keeps track of all point-to-line distance values
        tplanexlist = []; tplaneylist = []; tplanezlist = []
        for i in xrange(n):   #need to iterate through every coordinate to calculate the complete Sigmadk
            Xk = xcoords[i]; Yk = ycoords[i]; Zk = zcoords[i] #retrieve our point coordinates
            temp_xk = (1+temp_a**2+temp_b**2)**(-1) * ((1+temp_b**2)*Xk - temp_a*temp_b*Yk + temp_a*Zk)
            temp_yk = (1+temp_a**2+temp_b**2)**(-1) * ((1+temp_a**2)*Yk - temp_a*temp_b*Xk + temp_b*Zk) #these coordinate correspond to where the line L crosses the plane PI
            temp_zk = (1+temp_a**2+temp_b**2)**(-1) * ((temp_a**2 + temp_b**2)*Zk + temp_b*Yk + temp_a*Xk)
            sum_xk += (temp_xk - temp_u)**2
            sum_yk += (temp_yk - temp_v)**2 #summing all the orthogonal projection terms
            sum_zk += (temp_zk - temp_w)**2
            tplanexlist.append(temp_xk)
            tplaneylist.append(temp_yk)
            tplanezlist.append(temp_zk)
            temp_distlist.append(sqrt((temp_xk - temp_u)**2 + (temp_yk - temp_v)**2 + (temp_zk - temp_w)**2)) #add every distance to our list
        tempSigmadk = sum_xk + sum_yk + sum_zk
        avgdist = sum(distlist) / n #gets the average of all our point-to-line distances
        #print temp_a, temp_b, temp_u, temp_v, temp_w, tempSigmadk
        dictinfo[tempSigmadk] = [temp_a,temp_b, temp_u, temp_v, temp_w]
        '''             
        if (minSigmadk == None) or (tempSigmadk < minSigmadk): #then make this our new set of info
            if (secminSigmadk == None) or (minSigmadk < secminSigmadk): #then make this our new set of secondary minimum info
                secminSigmadk = minSigmadk #assign everything to be the final candidate
                secb=b; secu=u; secv=v; secw=w #assign secondary plane coordinates
            minSigmadk = tempSigmadk #assign everything to be the minimum line
            b=temp_b; u=temp_u; v=temp_v; w=temp_w
            distlist = temp_distlist #need to take the correct distlist (list of distances)
        elif (secminSigmadk == None) or (tempSigmadk < secminSigmadk): #then make this our new set of secondary minimum info
            secminSigmadk = tempSigmadk #assign everything to be the secondary minimal line
            secb=temp_b; secu=temp_u; secv=temp_v; secw=temp_w
        '''
    keyslist = dictinfo.keys() #the keys correspond to sigma d
    keyslist.sort() #
    firstline = dictinfo[keyslist[0]] #all the information for plane normal to L
    secondline = dictinfo[keyslist[1]]# perpendicular plane that matches the most points
    thirdline = dictinfo[keyslist[2]] # perpendicular plane that matches the least points; useful as plane for mapping non-linear least-squares
    a,b,u,v,w = firstline[0],firstline[1],firstline[2],firstline[3],firstline[4]
    #print firstelement, secondelement, thirdelement
    #now we have everything we need to make this line
    print "Lowest dk is:", minSigmadk
    print "Mean coordinates:", Xm, Ym, Zm
    print "Plane coordiates:", u, v, w
    #print "Secondary Plane coordinates:", secu, secv, secw
    rmsd = sqrt(minSigmadk/n) #quadratic mean distance
    print "Root Mean Square Distance between points and line:", rmsd
    print "Average Distance between points and line:", avgdist

    endpoints = ((Xm, Ym, Zm),(u, v, w))
    uniformity = rmsd
    return endpoints,uniformity

def least_squares_quadratic():
    pass

def parse(handler):
    '''parses file by line, and then by spaces; placing them into a 2D list'''
    coords = []
    for line in handler:
        linelist = line.strip().split() #split by spaces to a new little list
        linelist = map(float,linelist)
        coords.append(linelist) #append the little list to the big list
    return coords

if __name__=="__main__":
    starttime = time.time()
    print "Running..."
    if len(sys.argv) > 1: #then we have arguments to this script
        filename = sys.argv[1] #get the filename passed
    else:
        filename = testfilename #'/scratch/lvotapka/testdots.txt' #a test input

    inputfile = open(filename, 'r')
    coords = parse(inputfile) #coords: a 2D array of our coordinates
    timeavg = time_average(coords)
    rmsf = RMSF(coords,timeavg)
    #print the results
    print "Time Averaged Coordinates: ", ' '.join(map(str,timeavg)) #convert every element of the timeavg list into a string and print them
    print "RMSF:", str(rmsf)
    print "======Least Squares test======"
    testcoords = [[33.44, 12.63, 0.314],
                  [28.58, 10.23, 2.729],
                  [30.74, 11.37, 1.618],
                  [32.35, 12.09, 0.820],
                  [17.09, 4.55, 8.409],
                  [15.63, 3.88, 9.173],
                  [27.48, 9.79, 3.279],
                  [19.60, 5.75, 7.180],
                  [27.40, 9.65, 3.295],
                  [17.44, 4.74, 8.257]]
    endpoints,uniformity=least_squares_linear(coords)

    
    print "Complete"
    print "Total running time:", time.time()-starttime
