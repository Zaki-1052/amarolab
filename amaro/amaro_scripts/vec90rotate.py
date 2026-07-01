#By Lane Votapka
#Amarolab UCI Pharmaceutical Sciences
'''
A program to rotate a vector around the z-axis

This script takes two arguments:
  - a string representing a vector that will be rotated
  - a string representing a vector around which the other will be rotated
  the values of the vector should be separated by a ':'

It then returns a tuple of the other three rotated vectors

'''


import sys
import os
import numpy
import math
from numpy import array
from math import sin,cos,pi,sqrt

sep = ':'

def rotate90zaxis(vec,refvec=array([0,0,0])):
    '''
     this function rotates the 'vec' variable 90 degrees and returns the result
     --> clockwise
    '''
    #first specify the rotation matrix
    rot90matrix = array([[0.0, 1.0, 0.0],
                         [-1.0, 0.0, 0.0],
                         [0.0, 0.0, 1.0]])
    relvec = numpy.subtract(vec,refvec) #we now have the relative vector
    relvec = numpy.swapaxes(array([relvec]),0,1) #flip to become a column matrix
    print rot90matrix
    print relvec
    newvec = numpy.dot(rot90matrix,relvec)
    return newvec

def degstorads(degangle):
    radangle = degangle*(pi/180)
    return radangle

def length(ituple):
    '''
    takes a tuple or list of numbers, and finds the pythagorean distance between them and the origin
'''
    summation = 0
    for variable in ituple:
        square = variable * variable
        summation += square
    return math.sqrt(summation)

def rotatearbitrary(vec,angle,refvec=array((0,0,0)),rotatevec=array((0,0,1))):
    '''
    rotates a vector about a given point, around an arbitrary axis
    vec = the point to be rotated
    refvec = the point around which to rotate
    rotatevec = the axis around which to rotate

    returns the rotated vector
    '''

    #step 1: transpos all points so that the refvec is the origin
    # and center of rotation
    origvec = numpy.subtract(vec,refvec)
    if rotatevec[0] == 0.0 and rotatevec[1] == 0.0:
        #then skip the next few steps because its already parallel to the z-axis
        pass
    #step 2: rotate about z-axis so vector lies in xy plane
    x = vec[0]
    y = vec[1]
    z = vec[2]
    a = refvec[0]
    b = refvec[1]
    c = refvec[2]
    u=rotatevec[0]
    v=rotatevec[1]
    w=rotatevec[2]

    newx = (a*(v**2+w**2) + u*(-b*v-c*w+u*x+v*y+w*z) + ((x-a)*(v**2+w**2) + u*(b*v + c*w - v*y - w*z))*cos(angle)+sqrt(u**2 + v**2 + w**2)*(b*w - c*v - w*y + v*z)*sin(angle)) / (u**2 + v**2 + w**2)
    newy = (b*(u**2+w**2) + v*(-a*u-c*w+u*x+v*y+w*z) + ((y-b)*(u**2+w**2) + v*(a*u + c*w - u*x - w*z))*cos(angle)+sqrt(u**2 + v**2 + w**2)*(-a*w + c*u + w*x - u*z)*sin(angle)) / (u**2 + v**2 + w**2)
    newz = (c*(v**2+u**2) + w*(-a*u-b*v+u*x+v*y+w*z) + ((z-c)*(v**2+u**2) + w*(b*v + a*u - u*x - v*y))*cos(angle)+sqrt(u**2 + v**2 + w**2)*(a*v - b*u - v*x + u*y)*sin(angle)) / (u**2 + v**2 + w**2)

    newvec = array([newx,newy,newz])
    #origvec = numpy.swapaxes(array([origvec]),0,1) #make it a column matrix
    #rotatevec = numpy.swapaxes(array([rotatevec]),0,1) #make it a column matrix
    #xzplanematrix = array([[u/length((u,v)), v/length((u,v)), 0.0],
    #                      [-v/length((u,v)), u/length((u,v)), 0.0],
    #                      [0.0, 0.0, 1.0]])
    #xzvec = numpy.dot(xzplanematrix,origvec)
    #xzrotvec = numpy.dot(xzplanematrix,rotatevec)

    #step 3: rotate about y-axis so vector lies along z axis
    #zaxismatrix = array([[w/length((u,v,w)), 0.0, -length((u,v))/length((u,v,w))],
    #                      [0.0, 1.0, 0.0],
    #                      [length((u,v))/length((u,v,w)), 0.0, w/length((u,v,w))]])
    #zvec = numpy.dot(zaxismatrix,origvec)
    #zrotvec = numpy.dot(zaxismatrix,rotatevec)

    #step 4: rotate about z axis 90(?) degrees

    #step 5:

    
    
    #matrix = array([[1.0, 0.0, 0.0],
    #                      [0.0, 0.0, 0.0],
    #                      [0.0, 0.0, 0.0]])
    return newvec

def rotatexaxis(vec,angle):
    '''
    rotates vec around x axis, returning new vector
    '''
    rotmatrix = array([[1.0, 0.0, 0.0],
                        [0.0, cos(angle), sin(angle)],
                        [0.0, -sin(angle), cos(angle)]])
    
    vec = numpy.swapaxes(array([vec]),0,1) #flip to become a column matrix
    newvec = numpy.dot(rotmatrix,vec)
    return newvec

def rotateyaxis(vec,angle):
    '''
    rotates vec around x axis, returning new vector
    '''
    rotmatrix = array([[cos(angle), 0.0, -sin(angle)],
                         [0.0, 1.0, 0.0],
                         [sin(angle), 0.0, cos(angle)]])
    
    vec = numpy.swapaxes(array([vec]),0,1) #flip to become a column matrix
    newvec = numpy.dot(rotmatrix,vec)
    return newvec

def rotatezaxis(vec,angle):
    '''
    rotates vec around x axis, returning new vector
    '''
    rotmatrix = array([[cos(angle), sin(angle), 0.0],
                         [-sin(angle), cos(angle), 0.0],
                         [0.0, 0.0, 1.0]])
    
    vec = numpy.swapaxes(array([vec]),0,1) #flip to become a column matrix
    newvec = numpy.dot(rotmatrix,vec)
    return newvec


def _rotate90threetimes(vec,refvec=array([0.0,0.0,0.0]),rotvec=array([0.0,0.0,1.0])):
    '''
    this function calls the rotate90 function three times; returning the three results
    '''
    veclist = []
    curvec = vec
    veclist.append(curvec)
    deg = 90
    rad = degstorads(deg)
    for i in range(3):
        curvec = rotatearbitrary(curvec,rad,refvec,rotvec)
        veclist.append(curvec)

    return veclist

def _rotate120twotimes(vec,refvec=array([0.0,0.0,0.0]),rotvec=array([0.0,0.0,1.0])):
    '''
    this function calls the rotate90 function three times; returning the three results
    '''
    veclist = []
    curvec = vec
    veclist.append(curvec)
    deg = 120
    rad = degstorads(deg)
    for i in range(2):
        curvec = rotatearbitrary(curvec,rad,refvec,rotvec)
        veclist.append(curvec)

    return veclist
    
# main body of the script

if len(sys.argv) > 1:
    vec1string = sys.argv[1]
    refvecstring = sys.argv[2]
else:
    vec1string = '30:123:62'
    vec2string = '65.436:89.975:54.325'
    seedstring = '27:126:62'
    refvecstring = '66.0016:88.0989:50.8836'
    rotvecstring = '0.599656:-0.781090:0.173704'

vec1 = map(float,seedstring.strip().split(':'))
refvec = map(float,refvecstring.strip().split(':'))
rotvec = map(float,rotvecstring.strip().split(':'))
vec1 = array(vec1)
refvec = array(refvec)
rotvec = array(rotvec)

#veclist=_rotate90threetimes(vec1,refvec)
#veclist = [vec1].append(veclist)

testvec1 = array([2.0,0.0,0.0])
testvecref = array([0.0,0.0,0.0])
testrotref = array([0.0,0.0,1.0])

#print vec1
#print refvec
#print rotvec

#print rotatearbitrary(vec1,pi*2.0,refvec,testrotref)
endlist = _rotate120twotimes(vec1,refvec,rotvec)
print "sphere centers:"
for item in endlist:
    print tuple(item)
