# Closest coord.py

`
    
    
    
    # closest_coord.py
    # By Lane Votapka
    # Amaro lab 2013
    
    '''
    This script contains functions that allow us to find the closest pair of points
    in O(n) time using a randomized algorithm.
    
    May be used in NNScore by Jacob Durrant
    '''
    
    import numpy as np
    from numpy import array, matrix,
    from numpy.linalg import norm
    
    import math, os, sys, rand, re
    
    test_points = [ array([1,1,1]),
      array([0,0,5]),
      array([4,0,0]),
      array([0,6,0]),
      ]
    
    '''
    Algorithm Description:
    
    points P are in random order. Condense them all to fit within the unit square
    
    at most, n-2 stages:
    delta = dist(P[0], P[1]), we need to find if delta is the smallest distance
    or if there is a smaller one.
    gradually add points in order, terminate stage when we reach a point P[i],
    so that for some j<i, we have dist(P[i], P[j]) < delta, then we let delta
    for the next stage be equal to the closest distance so far.
    
    Each stage will take constant time.
    The stage tests a proposed distance, whether distance delta remains the
    closest pair of points, and if not, find the new pair.
    
    Idea:
    Subdivide the unit square into subsquares whose sides have length delta/2.
    There will be N**2 (in the 2-d case) subsquares, where N = 1/(2*delta). Then
    make each of these subsquares the indeces for a dictionary and the values will
    be the points that fall within its respective subsquare. If there is a
    pair that is closer than delta, there will either be 2 or more points in
    the same square, or they will be
    
    
    
    
    
    '''
    
    

`
