# Uniform sphere.py

`
    
    
    
    # Sukharev Grid generator
    # By Lane Votapka
    # Amaro lab 2012
    
    '''
    functions to generate uniform rotational Sukharev grids and other uniform sphere distributions.
    
    Based on the techniques by "Incremental Grid Sampling Strategies in Robotics"
    -Lindeman 2004
    
    uses interpolation of platonic solids to generate the grids
    By Lane Votapka
    '''
    
    import math
    import numpy as np
    
    from numpy import array
    from math import pi as PI
    
    def sphere3d_project(cart_point, unit_radius=1.0):
        '''takes a numpy.array cartesian point and normalizes to sphere surface'''
        newpoint = cart_point / np.linalg.norm(cart_point)
        return newpoint * unit_radius
    
    def square_interpolate(N):
        '''given N, will find the most uniform interpolation on a square'''
        return
    
    def cube3d(N):
        ''' spreads N points evenly over a cubic surface'''
        assert N >= 6, "N must be greater than 6"
    
    def euler_to_cart(phi,theta,psi):
        '''returns cartesian coords on the unit sphere corresponding to euler
        coords'''
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        return x, y, z
    
    def sphere_orientation(u1,u2,u3):
        '''u1, u2, & u3 are random numbers between 0 and 1
        returns equivalent euler coordinates angles'''
        phi = u1 * PI * 2
        theta = math.asin(u2)
        psi = PI * (2 * u3 - 1)
        return phi, theta, psi
        
    
    

`
